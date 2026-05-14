import pandas as pd
from sqlalchemy import create_engine
from google import genai
import os

# --- Configurations ---
DATABASE_URL = ""
engine = create_engine(DATABASE_URL)

# New 2026 Client Structure
client = genai.Client()

def get_policy_context(user_query):
    # 1. Smarter Keyword Extraction
    stop_words = {'are', 'there', 'any', 'recent', 'updates', 'regarding', 'is', 'the', 'a', 'an', 'what', 'how'}
    # Remove punctuation and split into words
    words = user_query.lower().replace('?', '').split()
    keywords = [w for w in words if w not in stop_words]
    
    if not keywords:
        return pd.DataFrame()

    # 2. Build a more targeted SQL query
    # Notice the double quotes around the column names!
    conditions = " OR ".join([f' "Title" ILIKE \'%%{k}%%\' OR "Raw_Text" ILIKE \'%%{k}%%\' ' for k in keywords])

    query = f"""
    SELECT "Title", "Raw_Text", "Html_Url"
    FROM policy_documents
    WHERE {conditions}
    ORDER BY "Publication_Date" DESC
    LIMIT 3;
    """
    return pd.read_sql(query, engine)

def ask_agent(user_query):
    # 1. Retrieve the hard data from your Neon database
    context_df = get_policy_context(user_query)
    
    if context_df.empty:
        return "I couldn't find any official policies in the database matching those keywords."

    # 2. Format the retrieved data into a readable string
    context_string = "\n\n".join([f"Document Title: {row['Title']}\nSummary: {row['Raw_Text']}" for _, row in context_df.iterrows()])
    
    # 3. Build the prompt (This is where you give the AI its personality and rules)
    system_prompt = f"""
    You are a highly professional MENA Immigration Policy Advocate. 
    Your goal is to answer the user's question clearly and concisely.
    
    CRITICAL RULE: You must base your answer ONLY on the official policy context provided below. 
    If the context does not contain the answer, explicitly state that the information is not in the current database. Do not hallucinate.

    Official Policy Context:
    {context_string}

    User Question: {user_query}
    """
    
    # 4. Call the Gemini API
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Connection Error: {e}"
