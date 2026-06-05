from src.Analytics.database import run_query


def get_sales_by_region():
    query = """
        SELECT
            o.region,
            ROUND(SUM(oi.sales), 2) AS total_sales,
            ROUND(SUM(oi.profit), 2) AS total_profit
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        GROUP BY o.region
        ORDER BY total_sales DESC;
    """
    return run_query(query)

def get_monthly_sales_trend():
    query = """
        SELECT
            DATE_TRUNC('month', o.order_date)::date AS month,
            ROUND(SUM(oi.sales), 2) AS total_sales,
            ROUND(SUM(oi.profit), 2) AS total_profit
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        GROUP BY month
        ORDER BY month;
    """
    return run_query(query)