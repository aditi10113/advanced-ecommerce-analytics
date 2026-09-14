import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "ecommerce_sales_advanced.csv"
OUT = BASE / "outputs"

OUT.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA)

# 2. Convert date
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# 3. Keep completed orders
df = df[df["is_completed"] == 1].copy()

# 4. Remove invalid records
df = df.dropna(subset=["customer_id", "order_date", "revenue"])

# 5. Customer-level metrics
customer = (
    df.groupby("customer_id")
    .agg(
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max")
    )
    .reset_index()
)

# 6. Customer lifetime in months
customer["lifetime_days"] = (
    customer["last_order"] - customer["first_order"]
).dt.days

customer["lifetime_months"] = (
    customer["lifetime_days"] / 30.44
).round(2)

# 7. Average order value
customer["avg_order_value"] = (
    customer["total_revenue"] /
    customer["total_orders"]
)

# 8. Purchase frequency
customer["purchase_frequency"] = (
    customer["total_orders"] /
    customer["lifetime_months"].replace(0, 1)
)

# 9. Profit margin
customer["profit_margin"] = (
    customer["total_profit"] /
    customer["total_revenue"]
) * 100

# 10. Estimated CLV
customer["estimated_clv"] = (
    customer["avg_order_value"]
    * customer["purchase_frequency"]
    * customer["profit_margin"]
    / 100
)

# Round values
numeric_cols = [
    "total_revenue",
    "total_profit",
    "avg_order_value",
    "purchase_frequency",
    "profit_margin",
    "estimated_clv"
]

customer[numeric_cols] = customer[numeric_cols].round(2)

# Sort by CLV
customer = customer.sort_values(
    "estimated_clv",
    ascending=False
)

# Save customer CLV
customer.to_csv(
    OUT / "customer_clv.csv",
    index=False
)

# CLV summary
clv_summary = pd.DataFrame({
    "metric": [
        "Customers",
        "Total Revenue",
        "Total Profit",
        "Average Customer Revenue",
        "Average Order Value",
        "Average Purchase Frequency",
        "Average Estimated CLV",
        "Median Estimated CLV",
        "Maximum Estimated CLV"
    ],
    "value": [
        customer["customer_id"].nunique(),
        customer["total_revenue"].sum(),
        customer["total_profit"].sum(),
        customer["total_revenue"].mean(),
        customer["avg_order_value"].mean(),
        customer["purchase_frequency"].mean(),
        customer["estimated_clv"].mean(),
        customer["estimated_clv"].median(),
        customer["estimated_clv"].max()
    ]
})

clv_summary.to_csv(
    OUT / "clv_summary.csv",
    index=False
)

print("CLV analysis completed successfully.")
print()
print(f"Customers analyzed: {len(customer):,}")
print(f"Total revenue: {customer['total_revenue'].sum():,.2f}")
print(f"Total profit: {customer['total_profit'].sum():,.2f}")
print(f"Average estimated CLV: {customer['estimated_clv'].mean():,.2f}")
print(f"Median estimated CLV: {customer['estimated_clv'].median():,.2f}")
print()
print("Generated:")
print(" - outputs/customer_clv.csv")
print(" - outputs/clv_summary.csv")