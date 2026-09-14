import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"

# Load RFM and CLV data
rfm = pd.read_csv(OUT / "rfm_customer_segments.csv")
clv = pd.read_csv(OUT / "customer_value_segments.csv")

# Keep required columns from RFM
rfm = rfm[
    [
        "customer_id",
        "segment",
        "recency",
        "frequency",
        "monetary"
    ]
]

# Keep required CLV columns
clv = clv[
    [
        "customer_id",
        "total_revenue",
        "total_profit",
        "total_orders",
        "estimated_clv",
        "value_segment"
    ]
]

# Combine datasets
df = rfm.merge(
    clv,
    on="customer_id",
    how="inner"
)

# Business-oriented customer intelligence segment
def classify_customer(row):

    rfm_segment = row["segment"]
    value_segment = row["value_segment"]

    if rfm_segment == "Champions" and value_segment == "High Value":
        return "VIP Customers"

    elif rfm_segment == "Loyal Customers" and value_segment == "High Value":
        return "Loyal High-Value"

    elif rfm_segment == "At Risk" and value_segment == "High Value":
        return "At-Risk High-Value"

    elif (
        rfm_segment == "Potential Loyalists"
        and value_segment in ["High Value", "Medium Value"]
    ):
        return "Growth Opportunities"

    elif (
        rfm_segment == "Needs Attention"
        and value_segment == "Low Value"
    ):
        return "Low-Value / Low-Engagement"

    elif value_segment == "High Value":
        return "High-Value Customers"

    elif value_segment == "Medium Value":
        return "Medium-Value Customers"

    else:
        return "Low-Value Customers"


df["customer_intelligence_segment"] = df.apply(
    classify_customer,
    axis=1
)

# Segment summary
summary = (
    df.groupby("customer_intelligence_segment")
    .agg(
        customers=("customer_id", "nunique"),
        revenue=("total_revenue", "sum"),
        profit=("total_profit", "sum"),
        avg_clv=("estimated_clv", "mean"),
        avg_orders=("total_orders", "mean"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean")
    )
    .reset_index()
)

summary["revenue_share"] = (
    summary["revenue"] / summary["revenue"].sum()
) * 100

summary = summary.round(2)

# Sort by revenue
summary = summary.sort_values(
    "revenue",
    ascending=False
)

# Save outputs
df.to_csv(
    OUT / "customer_intelligence_segments.csv",
    index=False
)

summary.to_csv(
    OUT / "customer_intelligence_summary.csv",
    index=False
)

print("Customer intelligence analysis completed successfully.")
print()
print("Generated:")
print(" - outputs/customer_intelligence_segments.csv")
print(" - outputs/customer_intelligence_summary.csv")
print()
print(summary.to_string(index=False))