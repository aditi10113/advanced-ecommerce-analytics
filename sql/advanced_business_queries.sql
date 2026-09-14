-- Advanced E-Commerce Analytics SQL
-- PostgreSQL-compatible queries

-- 1. Monthly revenue and month-over-month growth
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(revenue) AS revenue
    FROM ecommerce_sales_advanced
    WHERE order_status = 'Delivered'
    GROUP BY 1
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
       ROUND(
         100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
         / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2
       ) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- 2. Category ranking by revenue
SELECT category,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit,
       RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM ecommerce_sales_advanced
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY revenue_rank;

-- 3. Top 3 products in every category
WITH ranked AS (
    SELECT category, product,
           SUM(revenue) AS revenue,
           DENSE_RANK() OVER (
             PARTITION BY category ORDER BY SUM(revenue) DESC
           ) AS product_rank
    FROM ecommerce_sales_advanced
    WHERE order_status = 'Delivered'
    GROUP BY category, product
)
SELECT * FROM ranked
WHERE product_rank <= 3
ORDER BY category, product_rank;

-- 4. Customer lifetime value
SELECT customer_id,
       COUNT(DISTINCT order_id) AS total_orders,
       SUM(revenue) AS lifetime_value,
       SUM(profit) AS lifetime_profit,
       MAX(order_date) AS last_order_date
FROM ecommerce_sales_advanced
WHERE order_status = 'Delivered'
GROUP BY customer_id
ORDER BY lifetime_value DESC;

-- 5. Repeat purchase rate
WITH customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
    FROM ecommerce_sales_advanced
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE order_count > 1) AS repeat_customers,
    ROUND(
      100.0 * COUNT(*) FILTER (WHERE order_count > 1) / COUNT(*), 2
    ) AS repeat_customer_rate_pct
FROM customer_orders;

-- 6. Return and cancellation analysis
SELECT order_status,
       COUNT(*) AS orders,
       SUM(revenue) AS revenue,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS order_share_pct
FROM ecommerce_sales_advanced
GROUP BY order_status
ORDER BY orders DESC;

-- 7. Pareto analysis: cumulative revenue contribution by product
WITH product_revenue AS (
    SELECT product, SUM(revenue) AS revenue
    FROM ecommerce_sales_advanced
    WHERE order_status = 'Delivered'
    GROUP BY product
),
ranked AS (
    SELECT product, revenue,
           SUM(revenue) OVER () AS total_revenue,
           SUM(revenue) OVER (
             ORDER BY revenue DESC
             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS cumulative_revenue
    FROM product_revenue
)
SELECT product, revenue,
       ROUND(100.0 * cumulative_revenue / total_revenue, 2)
         AS cumulative_revenue_pct
FROM ranked
ORDER BY revenue DESC;

-- 8. Cohort retention by first purchase month
WITH first_orders AS (
    SELECT customer_id, DATE_TRUNC('month', MIN(order_date))::date AS cohort_month
    FROM ecommerce_sales_advanced
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
),
activity AS (
    SELECT DISTINCT e.customer_id,
           f.cohort_month,
           DATE_TRUNC('month', e.order_date)::date AS activity_month
    FROM ecommerce_sales_advanced e
    JOIN first_orders f USING (customer_id)
    WHERE e.order_status = 'Delivered'
)
SELECT cohort_month,
       activity_month,
       COUNT(DISTINCT customer_id) AS active_customers
FROM activity
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;
