import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"

# Load CLV data
df = pd.read_csv(OUT / "customer_clv.csv")

# Remove invalid CLV values
df = df.dropna(subset=["estimated_clv"])

# Create value segments using quartiles
q25 = df["estimated_clv"].quantile(0.25)
q75 = df["estimated_clv"].quantile(0.75)

def assign_segment(value):
    if value >= q75:
        return "High Value"
    elif value >= q25:
        return "Medium Value"
    else:
        return "Low Value"

df["value_segment"] = df["estimated_clv"].apply(assign_segment)

# Segment summary
summary = (
    df.groupby("value_segment")
    .agg(
        customers=("customer_id", "nunique"),
        revenue=("total_revenue", "sum"),
        profit=("total_profit", "sum"),
        avg_clv=("estimated_clv", "mean"),
        avg_orders=("total_orders", "mean"),
        avg_order_value=("avg_order_value", "mean")
    )
    .reset_index()
)

summary["revenue_share"] = (
    summary["revenue"] / summary["revenue"].sum()
) * 100

summary = summary.round(2)

# Order segments
segment_order = ["High Value", "Medium Value", "Low Value"]

df["value_segment"] = pd.Categorical(
    df["value_segment"],
    categories=segment_order,
    ordered=True
)

summary["value_segment"] = pd.Categorical(
    summary["value_segment"],
    categories=segment_order,
    ordered=True
)

summary = summary.sort_values("value_segment")

# Save outputs
df.to_csv(
    OUT / "customer_value_segments.csv",
    index=False
)

summary.to_csv(
    OUT / "customer_value_segment_summary.csv",
    index=False
)

# Chart 1: Customer distribution
plt.figure(figsize=(9, 5))

counts = df["value_segment"].value_counts().reindex(segment_order)

counts.plot(kind="bar")

plt.title("Customer Value Segment Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    OUT / "customer_value_distribution.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

# Chart 2: Revenue contribution
plt.figure(figsize=(9, 5))

summary.set_index("value_segment")["revenue"].plot(kind="bar")

plt.title("Revenue Contribution by Customer Value")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    OUT / "revenue_by_customer_value.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

print("Customer value segmentation completed successfully.")
print()
print("Generated:")
print(" - outputs/customer_value_segments.csv")
print(" - outputs/customer_value_segment_summary.csv")
print(" - outputs/customer_value_distribution.png")
print(" - outputs/revenue_by_customer_value.png")