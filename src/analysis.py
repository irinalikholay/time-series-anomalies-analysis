import pandas as pd 
import matplotlib.pyplot as plt 
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "daily_revenue_raw.csv"

df = pd.read_csv(RAW_DATA_PATH)

print("\n*** BASIC INFO *** ")
print(df.info())

print("\n*** FIRST ROWS ***")
print(df.head())

df["date"] = pd.to_datetime(df["date"])

print("\n*** DATA RANGE ***")
print("Start date:", df["date"].min())
print("End date:", df["date"].max())
print("Total days:", df.shape[0])

print("\n*** DESCRIPTIVE STATISTICS ***")
print(df["revenue"].describe())

plt.figure()
plt.plot(df["date"], df["revenue"])
plt.title("Daily Revenue Over Time (Raw Data)")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.show()