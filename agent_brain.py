import pandas as pd
from sqlalchemy import create_engine, text
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Neon
DATABASE_URL = os.getenv('dataBaseUrl')
engine = create_engine(DATABASE_URL)
client = genai.Client()

def get_policy_context(user_query):
    # 1. Turn the user's question into a vector using the new model
    try:
        response = client.models.embed_content(
            model='gemini-embedding-001',
            contents=user_query,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        query_vector = response.embeddings[0].values
    except Exception as e:
        print(f"Embedding failed: {e}")
        return pd.DataFrame()

    # 2. Ask Neon to find the closest mathematical matches using CAST
    query = text('''
        SELECT "Title", "Raw_Text", "Publication_Date"
        FROM policy_documents
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:vector AS vector)
        LIMIT 3;
    ''')
    
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"vector": str(query_vector)})

def ask_agent(user_query):
    # Retrieve the data
    context_df = get_policy_context(user_query)
    
    # The Kill Switch
    if context_df.empty:
        return "I currently do not have any specific policy documents in my database matching those keywords."

    # Format the context so the AI sees the dates
    context_text = ""
    for index, row in context_df.iterrows():
        context_text += f"Title: {row['Title']}\n"
        context_text += f"Date: {row['Publication_Date']}\n"
        context_text += f"Policy Text: {row['Raw_Text']}\n\n"
    
    # The Brain (with Citations and Guardrails)
    system_prompt = f"""
    You are an expert U.S. Immigration and MENA Policy Analyst. 
You will answer the user's query using the provided Official Policy Context. HOWEVER, you are required to use your Google Search tool to supplement this context to ensure the final answer includes the most up-to-date live internet data.
    CRITICAL INSTRUCTIONS:
    1. The Bouncer Rule: If the user asks about a specific country, look closely at the Official Policy Context. If the context is about a DIFFERENT country, you MUST completely ignore that context.
    2. Synthesize Active Policies: You will often receive multiple valid documents with different dates. Do NOT let a newer document erase an older document unless they directly contradict each other on the exact same specific topic (like an expiration date). 
    3. Mandatory Inclusions: You MUST combine and summarize all active rules. If ANY retrieved document mentions a financial hurdle, visa bond, or temporary waiver, you are strictly required to highlight it in your response, regardless of the date of the other documents. 
    4. Missing Info: If the valid context does not answer the question, or if you had to ignore the context because of the Bouncer Rule, say "I currently do not have specific policy updates for this query." Do not guess.
    5. Mandatory Citations: At the end of your response, you MUST provide a bulleted list of the sources you used. Format each citation exactly like this: "Source: [Title] (Published: [Date])".
    6. The Expiration Assassin: The current year is 2026. If the provided context mentions an expiration, end date, or deadline that has already passed (e.g., 2024 or 2025), you MUST treat that entire document as invalid. Do NOT summarize it. Do NOT warn the user about it. Completely exclude it from your response. If excluding it leaves you with no valid information, default to: "I do not have current, active policy data for this query."

    Official Policy Context:
    {context_text}

    User Question: {user_query}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_prompt,
            # This is the magic line that gives the agent internet access
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}] 
            )
        )
        return response.text
    except Exception as e:
        return f"AI Connection Error: {e}"