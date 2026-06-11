import pandas as pd
from sqlalchemy import create_engine

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://tejaspramesh@localhost:5432/ai_analytics_assistant"
)

def get_engine():
    return create_engine(DATABASE_URL)

def run_query(query: str) -> pd.DataFrame:
    engine = get_engine()

    with engine.connect() as connection:
        return pd.read_sql(query, connection)