import pandas as pd
from sqlalchemy import create_engine

# Connect to your Neon Database
DATABASE_URL = "postgresql://neondb_owner:npg_9XRuec1EQghO@ep-curly-rain-apgbyubp-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(DATABASE_URL)

# Load the local CSV you downloaded from UNHCR
print("Reading local CSV...")
df = pd.read_csv('persons_of_concern.csv')

# Push it to the Neon Database as a raw table
print("Uploading raw migration data to Neon...")
df.to_sql('persons_of_concern', engine, if_exists='replace', index=False)

print("✅ Successfully uploaded to 'persons_of_concern' table!")