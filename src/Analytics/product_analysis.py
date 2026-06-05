from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "postgresql+psycopg2://tejaspramesh@localhost:5432/ai_analytics_assistant"


def get_worst_subcategories():

    engine = create_engine(DATABASE_URL)

    query = """
    SELECT
        p.sub_category,
        ROUND(SUM(oi.sales),2) AS total_sales,
        ROUND(SUM(oi.profit),2) AS total_profit,
        ROUND(
            SUM(oi.profit) / NULLIF(SUM(oi.sales),0) * 100,
            2
        ) AS profit_margin_pct
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.sub_category
    ORDER BY total_profit ASC
    LIMIT 10;
    """

    return pd.read_sql(query, engine)