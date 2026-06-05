import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://tejaspramesh@localhost:5432/ai_analytics_assistant"


def get_sales_dataset():
    engine = create_engine(DATABASE_URL)

    query = """
    SELECT
        o.order_id,
        o.order_date,
        o.region,
        o.market,
        c.customer_name,
        c.segment,
        p.category,
        p.sub_category,
        oi.sales,
        oi.profit,
        oi.quantity
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN products p
        ON oi.product_id = p.product_id
    """

    return pd.read_sql(query, engine)