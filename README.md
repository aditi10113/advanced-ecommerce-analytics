# Advanced E-Commerce Analytics & Business Intelligence

## Overview
A complete Data Analyst portfolio project that analyzes e-commerce sales,
profitability, customer behavior, retention, and operational performance.

The project demonstrates an end-to-end analytics workflow:
**data quality → transformation → SQL analysis → Python analytics → Excel reporting → Power BI storytelling**.

## Business Objectives
1. Measure revenue, profit, AOV, margin, and order volume.
2. Identify high-performing categories, products, regions, and channels.
3. Segment customers using RFM analysis.
4. Understand repeat purchases and cohort retention.
5. Detect unusually high-value orders using IQR outlier detection.
6. Analyze returns, cancellations, and operational performance.
7. Convert analysis into actionable business recommendations.

## Technology Stack
- Python: Pandas, NumPy, Matplotlib
- SQL: PostgreSQL
- BI: Power BI
- Spreadsheet: Microsoft Excel
- Version control: Git/GitHub

## Folder Structure
```text
advanced_ecommerce_analytics_project/
├── data/
│   └── ecommerce_sales_advanced.csv
├── src/
│   └── advanced_analysis.py
├── sql/
│   ├── schema.sql
│   └── advanced_business_queries.sql
├── powerbi/
│   └── powerbi_dashboard_guide.md
├── excel/
│   └── analytics_report.xlsx
├── outputs/
│   ├── executive_kpis.csv
│   ├── category_performance.csv
│   ├── rfm_customer_segments.csv
│   ├── cohort_retention.csv
│   └── charts and quality reports
├── docs/
│   └── data_dictionary.csv
└── README.md
```

## Setup
```bash
pip install -r requirements.txt
python src/advanced_analysis.py
```

The analysis script creates summary tables, RFM segments, cohort retention,
outlier reports, data-quality checks, and charts in the `outputs/` directory.

## Suggested Business Recommendations
After running the project, review the output tables to identify:
- Categories with high revenue but low profit margin.
- Regions with strong order volume but weak profitability.
- RFM segments that may need retention campaigns.
- Products responsible for a large share of cumulative revenue.
- High-return or high-cancellation areas requiring operational improvement.

## Resume-Ready Description
**Advanced E-Commerce Analytics & Business Intelligence | Python, SQL, Power BI, Excel**
- Built an end-to-end analytics pipeline for 5,000 e-commerce transactions, including data-quality validation, KPI reporting, profitability analysis, and trend analysis using Python and Pandas.
- Developed advanced PostgreSQL queries with CTEs, window functions, ranking, customer lifetime value, repeat-purchase, and cohort-retention analysis.
- Performed RFM customer segmentation and IQR-based outlier detection, then prepared Power BI and Excel reporting layers for business decision-making.

## Interview Talking Points
- Why delivered orders should be separated from cancelled and returned orders.
- How RFM scoring works and how segments can support retention campaigns.
- Difference between revenue, profit, margin, and average order value.
- Why window functions are useful for rankings and month-over-month growth.
- How cohort analysis measures customer retention over time.
- How data-quality checks prevent misleading dashboard metrics.

## Dataset Note
The dataset is synthetic and created for portfolio and learning purposes.
