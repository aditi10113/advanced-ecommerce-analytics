import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "ecommerce_sales_advanced.csv"
OUT = BASE / "outputs"

OUT.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA)

# 2. Convert order date
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# 3. Keep valid customer/date records
df = df.dropna(subset=["customer_id", "order_date"])

# 4. Use completed orders only
df = df[df["is_completed"] == 1].copy()

# 5. Create order month
df["order_month"] = df["order_date"].dt.to_period("M")

# 6. Find each customer's first purchase month
df["cohort_month"] = df.groupby("customer_id")["order_month"].transform("min")

# 7. Calculate months since first purchase
df["cohort_index"] = (
    (df["order_month"].dt.year - df["cohort_month"].dt.year) * 12
    + (df["order_month"].dt.month - df["cohort_month"].dt.month)
)

# 8. Count unique customers in each cohort
cohort_data = (
    df.groupby(["cohort_month", "cohort_index"])["customer_id"]
    .nunique()
    .reset_index()
)

cohort_table = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="customer_id"
)

# 9. Calculate retention percentage
retention = cohort_table.divide(
    cohort_table.iloc[:, 0],
    axis=0
) * 100

retention = retention.round(2)

# Save retention table
retention.index = retention.index.astype(str)
retention.to_csv(OUT / "cohort_retention.csv")

# Save customer count table
cohort_table.index = cohort_table.index.astype(str)
cohort_table.to_csv(OUT / "cohort_customer_counts.csv")

# 10. Create heatmap
plt.figure(figsize=(16, 9))

plt.imshow(
    retention.fillna(0),
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(label="Retention %")

plt.title("Customer Cohort Retention Analysis")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.xticks(
    range(len(retention.columns)),
    retention.columns
)

plt.yticks(
    range(len(retention.index)),
    retention.index
)

# Add retention values
for i in range(len(retention.index)):
    for j in range(len(retention.columns)):
        value = retention.iloc[i, j]

        if pd.notna(value):
            plt.text(
                j,
                i,
                f"{value:.0f}%",
                ha="center",
                va="center",
                fontsize=8
            )

plt.tight_layout()
heatmap_path = str(OUT / "cohort_retention_heatmap.png")

plt.savefig(
    heatmap_path,
    dpi=120,
    bbox_inches="tight",
    format="png"
)

plt.close()


plt.close()

print("Cohort analysis completed successfully.")
print(f"Customers analyzed: {df['customer_id'].nunique():,}")
print(f"Completed orders analyzed: {len(df):,}")
print()
print("Generated files:")
print(" - outputs/cohort_retention.csv")
print(" - outputs/cohort_customer_counts.csv")
print(" - outputs/cohort_retention_heatmap.png")