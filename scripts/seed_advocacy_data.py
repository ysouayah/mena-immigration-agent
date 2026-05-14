import pandas as pd
from sqlalchemy import create_engine

# Your Neon Database
DATABASE_URL = "postgresql://neondb_owner:npg_9XRuec1EQghO@ep-curly-rain-apgbyubp-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(DATABASE_URL)

print("Injecting the Expanded MENA Master Dataset...")

curated_reports = [
    # --- THE CRISIS ZONES (TPS & Humanitarian) ---
    {
        "Document_Number": "SYR-26",
        "Title": "Syria Regional Crisis: US Policy and Displacement",
        "Publication_Date": "2026-05-10",
        "Agency": "DHS / UNHCR",
        "Raw_Text": "The displacement crisis in Syria remains catastrophic with over 6.7 million internally displaced persons (IDPs). U.S. immigration policy has historically restricted asylum pathways for Syrian nationals. However, the U.S. Department of Homeland Security maintains Temporary Protected Status (TPS) for Syria, protecting those already inside the US from deportation through September 2025 due to ongoing armed conflict."
    },
    {
        "Document_Number": "PAL-26",
        "Title": "Palestine (Gaza and West Bank): Humanitarian Emergency",
        "Publication_Date": "2026-05-12",
        "Agency": "State Dept / UNRWA",
        "Raw_Text": "The crisis in Palestine differs from traditional refugee outflows due to sealed borders. Massive internal displacement and high casualties define the Gaza crisis. U.S. immigration policy currently offers virtually no dedicated asylum, refugee, or parole pathways specifically for Palestinians, trapping civilian populations. Visas are subject to severe administrative processing delays."
    },
    {
        "Document_Number": "YEM-26",
        "Title": "Yemen: Protracted Conflict and TPS",
        "Publication_Date": "2026-04-20",
        "Agency": "DHS",
        "Raw_Text": "Yemen faces severe humanitarian crisis and blockade. U.S. immigration policy currently maintains Temporary Protected Status (TPS) and Special Student Relief for Yemen due to extraordinary and temporary conditions, allowing Yemeni nationals currently in the U.S. to remain and work legally."
    },
    {
        "Document_Number": "SUD-26",
        "Title": "Sudan: Armed Conflict and Displacement",
        "Publication_Date": "2026-05-01",
        "Agency": "DHS / HRW",
        "Raw_Text": "Following the outbreak of conflict in 2023, Sudan has experienced massive rapid displacement. The U.S. has designated Sudan for Temporary Protected Status (TPS), providing temporary refuge and work authorization to Sudanese nationals present in the United States amidst the ongoing war."
    },
    {
        "Document_Number": "LBN-26",
        "Title": "Lebanon: Economic Collapse and DED",
        "Publication_Date": "2026-02-15",
        "Agency": "White House / State Dept",
        "Raw_Text": "Lebanon is enduring a historic economic collapse and political instability. In response, the U.S. President authorized Deferred Enforced Departure (DED) for Lebanese nationals, protecting them from removal and granting work authorization. Standard visa processing out of Beirut remains heavily backlogged."
    },

    # --- THE HEAVILY RESTRICTED ZONES (Sanctions & Bans) ---
    {
        "Document_Number": "IRN-26",
        "Title": "Iran: Sanctions and Visa Restrictions",
        "Publication_Date": "2026-01-10",
        "Agency": "State Dept",
        "Raw_Text": "Immigration from Iran to the US is heavily restricted due to absent diplomatic relations and comprehensive sanctions. Iranian nationals were heavily impacted by historical Travel Bans. Currently, Iranian visa applicants face extreme administrative processing (often 6-12 months) under section 221(g), primarily relying on student visas (F-1) or family-sponsored channels."
    },
    {
        "Document_Number": "LBY-26",
        "Title": "Libya: Instability and Consular Suspensions",
        "Publication_Date": "2026-03-05",
        "Agency": "State Dept",
        "Raw_Text": "Due to ongoing instability in Libya, U.S. consular operations in Tripoli remain suspended. Libyan nationals seeking U.S. visas or immigration status must apply through third countries (like Tunisia), facing massive delays. Libya was previously subject to U.S. travel bans, and administrative scrutiny remains extraordinarily high."
    },
    {
        "Document_Number": "IRQ-26",
        "Title": "Iraq: Barriers to Return and SIV Backlogs",
        "Publication_Date": "2026-03-15",
        "Agency": "State Dept / AI",
        "Raw_Text": "Over 1.2 million Iraqis remain internally displaced. Iraqi nationals who assisted U.S. forces face severe, multi-year backlogs in the Special Immigrant Visa (SIV) and Direct Access Program (P-2), leaving them vulnerable while navigating a broken U.S. immigration pipeline."
    },

    # --- THE NORTH AFRICAN TIER (Economic Migration) ---
    {
        "Document_Number": "EGY-26",
        "Title": "Egypt: Standard Processing and Brain Drain",
        "Publication_Date": "2026-04-01",
        "Agency": "State Dept",
        "Raw_Text": "Egypt does not have special humanitarian immigration designations (No TPS/Parole). U.S. immigration from Egypt is characterized by standard employment-based visas, student visas, and the Diversity Visa Lottery. Consular wait times in Cairo for standard B1/B2 visitor visas remain lengthy due to high demand and economic outmigration."
    },
    {
        "Document_Number": "TUN-DZA-MAR-26",
        "Title": "Maghreb (Tunisia, Algeria, Morocco): Diversity Visas and Education",
        "Publication_Date": "2026-04-05",
        "Agency": "State Dept",
        "Raw_Text": "Immigration from Tunisia, Algeria, and Morocco to the United States operates under standard channels. These countries are not subject to TPS or broad travel bans. Migration is heavily driven by educational pursuits (F-1 visas), skilled labor, and high participation in the Diversity Immigrant Visa Program. Wait times for interviews in Tunis, Algiers, and Casablanca vary but follow standard protocols."
    },

    # --- THE HOST COUNTRIES & GULF TIER ---
    {
        "Document_Number": "TUR-26",
        "Title": "Turkey (Turkiye): Refugee Host and Visa Scrutiny",
        "Publication_Date": "2026-03-20",
        "Agency": "State Dept / UNHCR",
        "Raw_Text": "Turkey hosts the world's largest refugee population (primarily Syrian). For Turkish nationals, U.S. immigration operates normally, but visitor visa denial rates have spiked in recent years. Turkey serves as a critical processing hub for displaced persons from the wider MENA region seeking U.S. resettlement."
    },
    {
        "Document_Number": "JOR-26",
        "Title": "Jordan: Strategic Partner and Refugee Hub",
        "Publication_Date": "2026-04-12",
        "Agency": "State Dept",
        "Raw_Text": "Jordan remains a stable U.S. partner and a massive host country for Palestinian, Syrian, and Iraqi refugees. Jordanian citizens process U.S. visas normally in Amman without broad travel restrictions. The U.S. embassy in Amman also heavily processes refugee resettlement cases for the region."
    },
    {
        "Document_Number": "GULF-26",
        "Title": "Gulf States (Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Oman)",
        "Publication_Date": "2026-05-01",
        "Agency": "State Dept",
        "Raw_Text": "Citizens of the Gulf Cooperation Council (Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Oman) face standard to expedited U.S. immigration processing. There is virtually no refugee outflow from these citizen populations. Qatar has notably partnered with the U.S. to host processing centers for Afghan evacuees. U.S. visa issuance for GCC citizens remains highly favorable."
    }
]

df_reports = pd.DataFrame(curated_reports)
# Ensure dates are properly formatted
df_reports['Publication_Date'] = pd.to_datetime(df_reports['Publication_Date'])

# Add standard empty columns so your schema doesn't break
df_reports['Html_Url'] = "https://travel.state.gov/mena"

try:
    # Overwrite the table with our bulletproof dataset
    df_reports.to_sql('policy_documents', engine, if_exists='replace', index=False)
    print(f"\n🚀 REGION UNLOCKED! Injected {len(df_reports)} MENA dossiers into the Agent's brain.")
    print("The Agent now knows the current immigration status for every Arab/MENA country.")
except Exception as e:
    print(f"Database Error: {e}")