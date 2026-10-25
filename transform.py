import json, glob
import pandas as pd

def run():
    raw_file = sorted(glob.glob("raw_aq_*.json"))[-1]
    with open(raw_file) as f:
        data = json.load(f)

    hourly = data["hourly"]

    lengths = {k: len(v) for k, v in hourly.items()}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Column lengths don't match: {lengths}")

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={"time": "measured_at"})

    now = pd.Timestamp.now().floor("h")
    df = df[df["measured_at"] <= now]

    pollutants = ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide"]
    df = df.dropna(subset=pollutants, how="all")

    df.insert(1, "latitude", data["latitude"])
    df.insert(2, "longitude", data["longitude"])
    df["source_file"] = raw_file

    df.to_csv("clean_aq.csv", index=False)
    print("Rows kept:", len(df))

if __name__ == "__main__":
    run()