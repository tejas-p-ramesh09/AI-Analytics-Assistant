from src.Analytics.database import run_query

def get_overall_kpis():
    query = """
        SELECT
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(quantity) AS total_quantity
        FROM order_items;
    """

    return run_query(query)

def get_category_performance():
    query = """
        SELECT
            p.category,
            ROUND(SUM(oi.sales), 2) AS total_sales,
            ROUND(SUM(oi.profit), 2) AS total_profit,
            SUM(oi.quantity) AS units_sold,
            ROUND((SUM(oi.profit) / SUM(oi.sales)) * 100, 2) AS profit_margin_pct
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_sales DESC;
    """

    return run_query(query)