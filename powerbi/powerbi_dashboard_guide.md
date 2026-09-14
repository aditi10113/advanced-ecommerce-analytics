# Power BI Executive Dashboard

## Import
Import `data/ecommerce_sales_advanced.csv` into Power BI Desktop.

## Data Types
- `order_date`: Date
- `revenue`, `cost`, `profit`, `gross_sales`: Decimal/Currency
- `discount`, `profit_margin`: Percentage
- `is_completed`, `is_returned`, `is_cancelled`: Whole number

## Core Measures

```DAX
Total Revenue =
CALCULATE(
    SUM(ecommerce_sales_advanced[revenue]),
    ecommerce_sales_advanced[order_status] = "Delivered"
)

Total Profit =
CALCULATE(
    SUM(ecommerce_sales_advanced[profit]),
    ecommerce_sales_advanced[order_status] = "Delivered"
)

Total Orders =
CALCULATE(
    DISTINCTCOUNT(ecommerce_sales_advanced[order_id]),
    ecommerce_sales_advanced[order_status] = "Delivered"
)

Units Sold =
CALCULATE(
    SUM(ecommerce_sales_advanced[quantity]),
    ecommerce_sales_advanced[order_status] = "Delivered"
)

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Profit Margin = DIVIDE([Total Profit], [Total Revenue])

Return Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(ecommerce_sales_advanced[order_id]),
        ecommerce_sales_advanced[order_status] = "Returned"
    ),
    DISTINCTCOUNT(ecommerce_sales_advanced[order_id])
)

Cancellation Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(ecommerce_sales_advanced[order_id]),
        ecommerce_sales_advanced[order_status] = "Cancelled"
    ),
    DISTINCTCOUNT(ecommerce_sales_advanced[order_id])
)
```

## Recommended Report Pages

### 1. Executive Overview
- KPI cards: Revenue, Profit, Orders, AOV, Margin
- Line chart: Monthly revenue and profit
- Bar chart: Revenue by category
- Map or bar chart: Revenue by region
- Slicers: Date, category, region, channel

### 2. Product & Profitability
- Top 10 products by revenue
- Profit margin by product
- Category revenue vs. profit
- Discount vs. profit scatter plot
- Conditional-formatting product table

### 3. Customer Intelligence
- Customer count
- Repeat customer rate
- RFM segment distribution
- Revenue by customer segment
- Top customers by lifetime value

### 4. Retention & Operations
- Cohort retention matrix
- Monthly repeat purchase trend
- Returned vs. cancelled vs. delivered orders
- Payment method performance
- Channel conversion proxy analysis

## Design Guidance
Use a consistent layout, descriptive titles, tooltips, drill-through pages,
date slicers, and conditional formatting. Add a tooltip page for product and
customer details.
