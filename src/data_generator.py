import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "daily_revenue_raw.csv"

np.random.seed(42)

dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

base_revenue = np.random.normal(loc=1000, scale=200, size=len(dates))
base_revenue = np.clip(base_revenue, 100, None)

df = pd.DataFrame({
"date": dates,
"revenue": base_revenue
})

missing_days = np.random.choice(df.index, size=20, replace=False)
df = df.drop(missing_days)

spike_days = np.random.choice(df.index, size=5, replace=False)
df.loc[spike_days, "revenue"] *= 8

drop_days = np.random.choice(df.index, size=5, replace=False)
df.loc[drop_days, "revenue"] *= 0.1

df = df.sort_values("date")

df.to_csv(RAW_DATA_PATH, index=False)

print("Raw time series data generated:", RAW_DATA_PATH)