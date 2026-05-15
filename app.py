import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import agent_brain
import os
from dotenv import load_dotenv
load_dotenv() # This looks for the .env file in the root

# Connect to your Neon Database
DATABASE_URL = os.getenv('dataBaseUrl')
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="MENA Immigration Advocate", layout="wide")
st.title("🌍 MENA Immigration & Advocacy Dashboard")
st.markdown("Understanding the human reality behind U.S. immigration policy.")

# 2. Pull the Migration Data (The Tableau Data)
@st.cache_data # Caches the data so the map loads instantly on refresh
def load_migration_data():
    df = pd.read_sql('SELECT * FROM cleaned_mena_migration ORDER BY year', engine)
    return df

df_migration = load_migration_data()

# 3. The Geographic Bubble Map
st.divider()
st.subheader("The Reality of Displacement (2000-Present)")
st.markdown("*Note: Bubble size represents Total Affected Population (Refugees, Asylum Seekers, and IDPs). Palestinian populations under UNRWA mandate are tracked separately.*")

# Create the animated map natively in Python!
fig = px.scatter_geo(
    df_migration,
    locations="country_iso",       # Uses the ISO codes to place the bubbles perfectly
    color="country",
    hover_name="country",
    size="total_affected_population",
    animation_frame="year",        # This creates the timeline Play button!
    projection="natural earth",    # Gives it a nice curved globe look
    size_max=60,                   # Inflates the bubbles so the big crises are visible
    hover_data={
        "country_iso": False, 
        "refugees": True, 
        "asylum_seekers": True, 
        "internal_displacement": True
    }
)

# Focus the map strictly on the Middle East / North Africa / Europe region
fig.update_geos(
    center=dict(lon=35, lat=30),
    projection_scale=3.5,  # Zooms in on MENA
    showcountries=True, 
    countrycolor="lightgrey"
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# 4. The Agent Interface
st.divider()
st.subheader("Chat with the Policy Agent")
st.markdown("Ask about specific US policies, travel bans, or TPS updates for the MENA region.")

user_input = st.text_input("Ask a question (e.g., 'What is the current TPS status for Syria?')")

if user_input:
    with st.spinner(f"Agent is searching government records for: {user_input}..."):
        try:
            actual_response = agent_brain.ask_agent(user_input)
            st.success("Analysis Complete")
            st.write(actual_response)
        except Exception as e:
            st.error(f"Error connecting to Agent Brain: {e}")
