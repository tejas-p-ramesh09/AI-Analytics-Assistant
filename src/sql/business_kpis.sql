-- Overall business KPIs -- Total Sales, Total Profit, Total Orders, Total Quantity Sold
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_quantity
FROM order_items;

-- Sales and profit by region -- This will help us understand which regions are performing well and which ones need attention.  We can also identify any regional trends or patterns in sales and profitability.

SELECT
    o.region,
    ROUND(SUM(oi.sales), 2) AS total_sales,
    ROUND(SUM(oi.profit), 2) AS total_profit
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
GROUP BY o.region
ORDER BY total_sales DESC;

-- Sales and profit by category -- This will help us identify which product categories are driving the most sales and profit. We can also analyze the performance of different categories and make informed decisions about inventory management and marketing strategies.

SELECT
    p.category,
    ROUND(SUM(oi.sales), 2) AS total_sales,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;

-- Profit margin by category -- This will help us understand which categories are the most profitable and which ones have lower profit margins. We can use this information to optimize our product mix and focus on high-margin categories.

SELECT
    p.category,
    ROUND(SUM(oi.sales), 2) AS total_sales,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / SUM(oi.sales)) * 100,
        2
    ) AS profit_margin_pct
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY profit_margin_pct DESC;

--- Profit margin by sub-category -- This will help us drill down further into the profitability of specific sub-categories within each category. We can identify which sub-categories are performing well and which ones may need attention. This information can guide our inventory and marketing strategies to focus on high-margin sub-categories.

SELECT
    p.sub_category,
    ROUND(SUM(oi.sales), 2) AS total_sales,
    ROUND(SUM(oi.profit), 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / SUM(oi.sales)) * 100,
        2
    ) AS profit_margin_pct
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE p.category = 'Furniture'
GROUP BY p.sub_category
ORDER BY total_profit ASC;

--- Average discount and total profit by sub-category -- This will help us understand the relationship between discounts and profitability for different sub-categories. We can identify which sub-categories are offering higher discounts and how it impacts their overall profit. This information can guide our pricing and promotional strategies to optimize profitability.

SELECT
    p.sub_category,
    ROUND(AVG(oi.discount) * 100, 2) AS avg_discount_pct,
    ROUND(SUM(oi.profit), 2) AS total_profit
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE p.category = 'Furniture'
GROUP BY p.sub_category
ORDER BY avg_discount_pct DESC;

--- Sales and profit by region for a specific sub-category (e.g., Tables) -- This will help us analyze the performance of a specific sub-category across different regions. We can identify which regions are driving the most sales and profit for that sub-category, and which regions may need attention. This information can guide our regional marketing and inventory strategies for that specific sub-category.

SELECT
    o.region,
    ROUND(SUM(oi.sales), 2) AS total_sales,
    ROUND(SUM(oi.profit), 2) AS total_profit
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE p.sub_category = 'Tables'
GROUP BY o.region
ORDER BY total_profit ASC;