# Advanced E-Commerce Analytics

An end-to-end e-commerce analytics project that combines **Python, SQL, Excel, and Power BI** to analyze sales performance, customer behavior, profitability, retention, and customer lifetime value.

## Project Overview

This project transforms raw e-commerce transaction data into actionable business insights through data cleaning, exploratory analysis, customer segmentation, and interactive dashboards.

The analysis focuses on answering questions such as:

* How much revenue and profit does the business generate?
* Which categories, products, and regions perform best?
* Which customers are loyal, valuable, or at risk?
* How does customer retention change over time?
* Which customer segments should receive targeted marketing campaigns?
* Where can the business improve revenue and profitability?

## Business Objectives

* Measure overall sales and profit performance.
* Identify high-performing products and categories.
* Compare regional revenue and profitability.
* Segment customers using RFM analysis.
* Estimate customer lifetime value.
* Analyze customer retention using cohort analysis.
* Develop actionable recommendations for customer growth and retention.

## Technology Stack

| Area                  | Tools              |
| --------------------- | ------------------ |
| Programming           | Python             |
| Data Analysis         | Pandas, NumPy      |
| Data Visualization    | Matplotlib         |
| Database              | SQL                |
| Spreadsheet Analysis  | Microsoft Excel    |
| Business Intelligence | Microsoft Power BI |
| Development           | VS Code            |
| Version Control       | Git and GitHub     |

## Project Structure

```text
advanced-ecommerce-analytics/
│
├── data/
│   └── ecommerce_sales_advanced.csv
│
├── docs/
│
├── excel/
│
├── outputs/
│   ├── rfm_customer_segments.csv
│   ├── rfm_segment_summary.csv
│   ├── cohort_retention.csv
│   ├── customer_clv.csv
│   ├── clv_summary.csv
│   ├── customer_intelligence_segments.csv
│   ├── customer_intelligence_summary.csv
│   └── generated charts
│
├── powerbi/
│   ├── advanced_ecommerce_analytics_dashboard.pbix
│   └── dashboard_preview.png
│
├── sql/
│
├── src/
│   ├── advanced_analysis.py
│   ├── cohort_analysis.py
│   ├── clv_analysis.py
│   ├── customer_value_segmentation.py
│   └── customer_intelligence.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Key Analysis Modules

### 1. Sales Performance Analysis

Analyzes:

* Total revenue
* Total profit
* Order volume
* Average order value
* Revenue by category
* Revenue by product
* Revenue by region
* Monthly sales trends
* Profitability and outliers

### 2. RFM Customer Segmentation

Customers are segmented using:

* **Recency:** How recently the customer purchased
* **Frequency:** How often the customer purchased
* **Monetary:** How much the customer spent

The segmentation identifies groups such as:

* Champions
* Loyal Customers
* Potential Loyalists
* At Risk
* Needs Attention

### 3. Cohort Retention Analysis

Cohort analysis groups customers according to their first purchase month and measures their repeat purchasing behavior over time.

This helps identify:

* Customer retention trends
* Repeat purchase patterns
* Cohorts with stronger engagement
* Potential retention problems

### 4. Customer Lifetime Value Analysis

Customer lifetime value analysis estimates the long-term value of each customer using purchase behavior and profitability metrics.

It supports:

* Customer prioritization
* Retention planning
* Marketing budget allocation
* High-value customer identification

### 5. Customer Intelligence Segmentation

Combines customer revenue, profit, order behavior, recency, frequency, and CLV to create more actionable customer groups, including:

* VIP Customers
* Loyal High-Value Customers
* Growth Opportunities
* Medium-Value Customers
* At-Risk High-Value Customers
* Low-Value Customers

## Power BI Dashboard

The Power BI dashboard provides an interactive executive overview of the business.

### Dashboard Features

* Total Revenue KPI
* Total Profit KPI
* Total Orders KPI
* Total Customers KPI
* Average Order Value KPI
* Monthly Revenue Trend
* Revenue by Category
* Revenue by Region
* Profit by Region

## Sample Business Insights

The analysis identifies several important customer and business patterns:

* Medium-value customers contribute a substantial share of total revenue.
* VIP and loyal customers represent important revenue-generating segments.
* Growth-opportunity customers may respond well to targeted campaigns and repeat-purchase offers.
* At-risk high-value customers should be prioritized for retention campaigns.
* Regional and category-level analysis can help identify opportunities for improving revenue and profit.

> Note: The exact business recommendations should be reviewed against the latest generated output files and dashboard filters.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/advanced-ecommerce-analytics.git
cd advanced-ecommerce-analytics
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the analysis scripts

```powershell
python src/advanced_analysis.py
python src/cohort_analysis.py
python src/clv_analysis.py
python src/customer_value_segmentation.py
python src/customer_intelligence.py
```

Generated datasets and charts will be saved in the `outputs/` folder.

### 5. Open the Power BI report

Open:

```text
powerbi/advanced_ecommerce_analytics_dashboard.pbix
```

If required, update the data source path in Power BI to point to the local CSV file.

## Future Improvements

* Add interactive Power BI slicers and drill-through pages.
* Add product-level profitability analysis.
* Add predictive customer churn modeling.
* Add automated data refresh.
* Add SQL-based data pipelines.
* Publish the dashboard to Power BI Service.
* Add scheduled reporting and alerting.

## Author

**Aditi**

This project was created as a portfolio project to demonstrate skills in data analytics, business intelligence, customer segmentation, and data-driven decision-making.

## License

This project is intended for educational and portfolio purposes.
