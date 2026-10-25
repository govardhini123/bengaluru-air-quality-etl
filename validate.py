import pandas as pd

def run():
    df = pd.read_csv("clean_aq.csv", parse_dates=["measured_at"])
    errors = []

    # Rule 1: not empty
    if len(df) == 0:
        errors.append("No rows to load")

    # Rules 2 and 3: no negatives, no absurd values
    limits = {"pm10": 1000, "pm2_5": 1000,
              "carbon_monoxide": 20000, "nitrogen_dioxide": 1000}
    for col, max_val in limits.items():
        neg = (df[col] < 0).sum()
        high = (df[col] > max_val).sum()
        if neg:
            errors.append(f"{col}: {neg} negative values")
        if high:
            errors.append(f"{col}: {high} values above {max_val}")

    # Rule 4: PM2.5 cannot exceed PM10 (0.5 allowed for rounding)
    bad = (df["pm2_5"] > df["pm10"] + 0.5).sum()
    if bad:
        errors.append(f"{bad} rows where pm2_5 > pm10")

    # Rule 5: no future timestamps, no duplicate hours
    future = (df["measured_at"] > pd.Timestamp.now()).sum()
    dupes = df["measured_at"].duplicated().sum()
    if future:
        errors.append(f"{future} future timestamps")
    if dupes:
        errors.append(f"{dupes} duplicate timestamps")

    if errors:
        raise ValueError("DATA QUALITY FAILED:\n  - " + "\n  - ".join(errors))
    print(f"All checks passed ({len(df)} rows)")

if __name__ == "__main__":
    run()