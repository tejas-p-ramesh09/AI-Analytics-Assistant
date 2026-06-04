import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = "postgresql+psycopg2://tejaspramesh@localhost:5432/ai_analytics_assistant"
FILE_PATH = "data/raw/Global Superstore.xls"


def main():
    print("Reading Excel file...")

    orders_raw = pd.read_excel(FILE_PATH, sheet_name="Orders")
    returns_raw = pd.read_excel(FILE_PATH, sheet_name="Returns")
    people_raw = pd.read_excel(FILE_PATH, sheet_name="People")

    print("Orders:", orders_raw.shape)
    print("Returns:", returns_raw.shape)
    print("People:", people_raw.shape)


if __name__ == "__main__":
    main()