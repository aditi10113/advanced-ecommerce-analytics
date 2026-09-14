"""
Advanced E-Commerce Analytics Pipeline
--------------------------------------
Produces quality checks, KPI summaries, RFM segmentation, cohort retention,
product analysis, and charts.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecommerce_sales_advanced.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["order_date"])

# 1. Data quality checks
quality = pd.DataFrame({
    "metric": [
        "row_count", "duplicate_order_ids", "missing_values",
        "negative_revenue", "invalid_discount", "date_min", "date_max"
    ],
    "value": [
        len(df),
        int(df["order_id"].duplicated().sum()),
        int(df.isna().sum().sum()),
        int((df["revenue"] < 0).sum()),
        int(((df["discount"] < 0) | (df["discount"] > 1)).sum()),
        df["order_date"].min().date(),
        df["order_date"].max().date()
    ]
})
quality.to_csv(OUT / "data_quality_report.csv", index=False)

# 2. Derived fields
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["profit"] = df["revenue"] - df["cost"]
df["profit_margin"] = np.where(df["revenue"] != 0, df["profit"] / df["revenue"], 0)
completed = df[df["order_status"] == "Delivered"].copy()

# 3. Executive KPIs
kpis = pd.DataFrame([{
    "total_revenue": completed["revenue"].sum(),
    "total_profit": completed["profit"].sum(),
    "total_orders": completed["order_id"].nunique(),
    "units_sold": completed["quantity"].sum(),
    "average_order_value": completed["revenue"].sum() / completed["order_id"].nunique(),
    "profit_margin": completed["profit"].sum() / completed["revenue"].sum(),
    "return_rate": (df["order_status"] == "Returned").mean(),
    "cancellation_rate": (df["order_status"] == "Cancelled").mean()
}])
kpis.to_csv(OUT / "executive_kpis.csv", index=False)

# 4. Category, region, channel and product analysis
def summary(group_cols, filename):
    result = completed.groupby(group_cols, as_index=False).agg(
        revenue=("revenue","sum"),
        profit=("profit","sum"),
        orders=("order_id","nunique"),
        units=("quantity","sum"),
        avg_order_value=("revenue", lambda x: x.sum() / x.count())
    )
    result["profit_margin"] = result["profit"] / result["revenue"]
    result.sort_values("revenue", ascending=False).to_csv(OUT / filename, index=False)

summary(["category"], "category_performance.csv")
summary(["region"], "region_performance.csv")
summary(["channel"], "channel_performance.csv")
summary(["product"], "product_performance.csv")

# 5. Monthly trend
monthly = completed.groupby("month", as_index=False).agg(
    revenue=("revenue","sum"),
    profit=("profit","sum"),
    orders=("order_id","nunique"),
    units=("quantity","sum")
)
monthly["profit_margin"] = monthly["profit"] / monthly["revenue"]
monthly.to_csv(OUT / "monthly_trends.csv", index=False)

# 6. RFM segmentation
snapshot_date = completed["order_date"].max() + pd.Timedelta(days=1)
rfm = completed.groupby("customer_id").agg(
    recency=("order_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("revenue", "sum")
).reset_index()

rfm["R_score"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

def segment(score):
    if score >= 13: return "Champions"
    if score >= 10: return "Loyal Customers"
    if score >= 7: return "Potential Loyalists"
    if score >= 5: return "At Risk"
    return "Needs Attention"

rfm["segment"] = rfm["RFM_score"].apply(segment)
rfm.to_csv(OUT / "rfm_customer_segments.csv", index=False)

# 7. Cohort retention
customer_first = completed.groupby("customer_id")["order_date"].min().rename("first_order_date")
cohort = completed.merge(customer_first, on="customer_id")
cohort["order_month"] = cohort["order_date"].dt.to_period("M")
cohort["cohort_month"] = cohort["first_order_date"].dt.to_period("M")
cohort["period_number"] = (
    (cohort["order_month"].dt.year - cohort["cohort_month"].dt.year) * 12
    + cohort["order_month"].dt.month - cohort["cohort_month"].dt.month
)
cohort_counts = cohort.groupby(["cohort_month","period_number"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_counts.pivot(index="cohort_month", columns="period_number", values="customer_id")
cohort_retention = cohort_pivot.divide(cohort_pivot.iloc[:,0], axis=0)
cohort_retention.to_csv(OUT / "cohort_retention.csv")

# 8. Outlier detection using IQR
q1, q3 = completed["revenue"].quantile([.25,.75])
iqr = q3 - q1
lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
outliers = completed[(completed["revenue"] < lower) | (completed["revenue"] > upper)]
outliers.to_csv(OUT / "revenue_outliers.csv", index=False)

# 9. Charts
plt.figure(figsize=(11,5))
monthly.plot(x="month", y="revenue", kind="line", marker="o", legend=False)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month"); plt.ylabel("Revenue")
plt.xticks(rotation=60); plt.tight_layout()
plt.savefig(OUT/"monthly_revenue_trend.png", dpi=160); plt.close()

plt.figure(figsize=(9,5))
category = pd.read_csv(OUT/"category_performance.csv").sort_values("revenue")
category.plot(x="category", y="revenue", kind="barh", legend=False)
plt.title("Revenue by Category")
plt.xlabel("Revenue"); plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT/"revenue_by_category.png", dpi=160); plt.close()

plt.figure(figsize=(9,5))
rfm["segment"].value_counts().plot(kind="bar")
plt.title("Customer Segments by RFM")
plt.xlabel("Segment"); plt.ylabel("Customers")
plt.xticks(rotation=30); plt.tight_layout()
plt.savefig(OUT/"rfm_segments.png", dpi=160); plt.close()

print("Pipeline completed successfully.")
print(f"Rows analyzed: {len(df)}")
print(f"Delivered orders: {len(completed)}")
print(f"Revenue: {completed['revenue'].sum():,.2f}")
print(f"Profit: {completed['profit'].sum():,.2f}")
