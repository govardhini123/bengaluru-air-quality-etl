import os
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load secrets from the .env file in the same folder as this script
load_dotenv(Path(__file__).parent / ".env")

def run():
    df = pd.read_csv("clean_aq.csv", parse_dates=["measured_at"])
    df = df.astype(object).where(pd.notna(df), None)

    cols = ["measured_at", "latitude", "longitude", "pm10", "pm2_5",
            "carbon_monoxide", "nitrogen_dioxide", "source_file"]
    rows = list(df[cols].itertuples(index=False, name=None))

    sql = f"""
    INSERT INTO air_quality_hourly ({", ".join(cols)})
    VALUES %s
    ON CONFLICT (measured_at, latitude, longitude) DO UPDATE SET
        pm10             = EXCLUDED.pm10,
        pm2_5            = EXCLUDED.pm2_5,
        carbon_monoxide  = EXCLUDED.carbon_monoxide,
        nitrogen_dioxide = EXCLUDED.nitrogen_dioxide,
        source_file      = EXCLUDED.source_file,
        loaded_at        = now();
    """

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    with conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, rows)
            cur.execute("SELECT COUNT(*) FROM air_quality_hourly;")
            print("Rows in table:", cur.fetchone()[0])
    conn.close()

if __name__ == "__main__":
    run()