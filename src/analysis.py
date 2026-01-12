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

plt.figure(figsize=(12,5))
plt.plot(df["date"], df["revenue"])
plt.title("Daily Revenue Over Time (Raw Data)")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.savefig(
    PROJECT_ROOT / "visuals" / "daily_revenue_raw.png",
    bbox_inches="tight"
)
plt.show() 
plt.close()


print("\n*** TIME AXIS VALIDATION ***")

df = df.sort_values("date")

full_date_range = pd.date_range(
    start=df["date"].min(),
    end=df["date"].max(),
    freq="D"
)

missing_dates = full_date_range.difference(df["date"])

print("Expected number of days:", len(full_date_range))
print("Actual number of days:", df.shape[0])
print("Missing days:", len(missing_dates))

if len(missing_dates) > 0:
    print("\nMissing dates detected:")
    print(missing_dates)
else:
    print("\nNo missing dates detected.")

print("\n*** RESTORING TIME AXIS ***")

df_full = (
    df.set_index("date")
    .reindex(full_date_range)
    .reset_index()
)

# Rename index column back to "date"
df_full = df_full.rename(columns={"index": "date"})


df_full_columns = ["date", "revenue"]

print("Rows after restoring time axis:", df_full.shape[0])
print("Missing revenue values after restoration:")
print(df_full["revenue"].isna().sum())

print("\n*** ANOMALY DETECTION (IQR METHOD) ***")

q1 = df_full["revenue"].quantile(0.25)
q3 = df_full["revenue"].quantile(0.75)
iqr = q3 - q1 

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

anomalies = df_full[
    (df_full["revenue"] < lower_bound)  |
    (df_full["revenue"] > upper_bound)
]

print("Anomalies count:", anomalies.shape[0])

plt.figure(figsize=(12, 5))

# Main time series 
plt.plot(
    df_full["date"],
    df_full["revenue"],
    label="Daily revenue",
    alpha=0.6
)

# Overlay anomalies 
plt.scatter(
    anomalies["date"],
    anomalies["revenue"],
    color="red",
    label="Anomalies",
    zorder=5
)

plt.title("Daily Revenue with Detected Anomalies")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.savefig(
    PROJECT_ROOT / "visuals" / "daily_revenue_with_anomalies.png",
    bbox_inches="tight"
)
plt.show()

# Save clean dataset ( restored time axis , no imputation yet)

processed_path = PROJECT_ROOT / "data" / "processed" / "daily_revenue_clean.csv"
df_full.to_csv(processed_path, index=False)
print(f"Clean dataset saved to: {processed_path}")



print("\n*** LOAD CLEAN DATA ***")
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "daily_revenue_clean.csv"
df_clean = pd.read_csv(PROCESSED_DATA_PATH)
df_clean["date"] = pd.to_datetime(df_clean["date"])

print(df_clean.info())


print("\n*** METRICS COMPARISON ( RAW vs CLEAN ) ***")

raw_mean = df["revenue"].mean()
clean_mean = df_clean["revenue"].mean()

raw_median = df["revenue"].median()
clean_median = df_clean["revenue"].median()

print("Raw mean revenue:", raw_mean)
print("Clean mean revenue:", clean_mean)

print("Raw median revenue:", raw_median)
print("Clean median revenue", clean_median)


print("\n*** MOVING AVERAGE TREND ***")

df_clean = df_clean.sort_values("date")

df_clean["rolling_mean_7d"] = (
    df_clean["revenue"]
    .rolling(window=7, min_periods=1)
    .mean()
)

plt.figure(figsize=(12, 5))

# Clean daily revenue 
plt.plot(
    df_clean["date"],
    df_clean["revenue"],
    label="Clean daily revenue",
    alpha=0.5
)

# 7-day moving average
plt.plot(
    df_clean["date"],
    df_clean["rolling_mean_7d"],
    label="7-day moving average",
    linewidth=2
)

plt.title("Clean Daily Revenue with 7-Days Moving Average")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()

plt.savefig(
    PROJECT_ROOT / "visuals" / "clean_revenue_trend.png",
    bbox_inches="tight"
)
plt.show()
plt.close()