import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv() # This looks for the .env file in the root

# Connect to your Neon Database
DATABASE_URL = os.getenv('dataBaseUrl')
engine = create_engine(DATABASE_URL)

# Load the local CSV you downloaded from UNHCR
print("Reading local CSV...")
df = pd.read_csv('/Users/ysfsouayah/Downloads/mena_immigration_agent/data/persons_of_concern.csv')

# Push it to the Neon Database as a raw table
print("Uploading raw migration data to Neon...")

# 1. Empty the table without destroying its structure
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE persons_of_concern;"))

# 2. Append the new data into the empty table
df.to_sql('persons_of_concern', engine, if_exists='append', index=False)

print("✅ Successfully uploaded to 'persons_of_concern' table!")
