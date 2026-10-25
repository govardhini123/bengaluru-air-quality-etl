import requests, json
from datetime import datetime

def run():
    URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 12.97,
        "longitude": 77.59,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide",
        "past_days": 7,
        "timezone": "Asia/Kolkata",
    }

    resp = requests.get(URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    fname = f"raw_aq_{datetime.now():%Y%m%d_%H%M}.json"
    with open(fname, "w") as f:
        json.dump(data, f, indent=2)

    print("Saved", fname)
    print("Rows:", len(data["hourly"]["time"]))

if __name__ == "__main__":
    run()