import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

# Set paths
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
CREDENTIAL_PATH = ROOT_DIR / "secrets" / "bigquery-key.json"

# Set credential environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIAL_PATH)

# Load your cleaned CSV
df = pd.read_csv(DATA_DIR / "ai_energy_clean.csv")
df = df.drop_duplicates(subset=["year"])

# Set up BigQuery client
client = bigquery.Client()

# Define table ID (project.dataset.table)
table_id = "ai-dc-energy-demand.energy_demand.ai_us_energy_clean"


# Push the data
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # <-- This is key
)

job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()

print(f"[✓] Load complete. Data pushed to BigQuery table: {table_id}")

