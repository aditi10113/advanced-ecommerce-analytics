import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[1]
df = pd.read_csv(root / "data" / "ecommerce_sales_advanced.csv")

assert len(df) == 5000
assert df["order_id"].is_unique
assert (df["revenue"] >= 0).all()
assert ((df["discount"] >= 0) & (df["discount"] <= 1)).all()
assert set(df["order_status"].unique()) <= {"Delivered", "Returned", "Cancelled", "Pending"}
print("All data validation tests passed.")
