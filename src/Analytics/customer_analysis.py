from src.Analytics.database import run_query


def get_top_customers(limit=10):
    query = f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.segment,
            ROUND(SUM(oi.sales), 2) AS total_sales,
            ROUND(SUM(oi.profit), 2) AS total_profit,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN customers c
            ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name, c.segment
        ORDER BY total_sales DESC
        LIMIT {limit};
    """
    return run_query(query)