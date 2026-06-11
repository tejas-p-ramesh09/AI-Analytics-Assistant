import pandas as pd
from sqlalchemy import create_engine


import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://tejaspramesh@localhost:5432/ai_analytics_assistant"
)
FILE_PATH = "data/raw/Global Superstore.xls"


def main():
    print("Reading Excel file...")

    orders_raw = pd.read_excel(FILE_PATH, sheet_name="Orders")
    returns_raw = pd.read_excel(FILE_PATH, sheet_name="Returns")
    people_raw = pd.read_excel(FILE_PATH, sheet_name="People")

    print("Orders raw:", orders_raw.shape)
    print("Returns raw:", returns_raw.shape)
    print("People raw:", people_raw.shape)

    # Customers table
    customers = orders_raw[[
        "Customer ID",
        "Customer Name",
        "Segment"
    ]].drop_duplicates()

    customers.columns = [
        "customer_id",
        "customer_name",
        "segment"
    ]

    print("Customers:", customers.shape)

    # Products table
    products = orders_raw[[
        "Product ID",
        "Product Name",
        "Category",
        "Sub-Category"
    ]].drop_duplicates(subset=["Product ID"], keep="first")

    products.columns = [
        "product_id",
        "product_name",
        "category",
        "sub_category"
    ]

    print("Products:", products.shape)

    # Orders table
    orders = orders_raw[[
        "Order ID",
        "Customer ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Order Priority",
        "City",
        "State",
        "Country",
        "Postal Code",
        "Market",
        "Region"
    ]].drop_duplicates(subset=["Order ID"], keep="first")

    orders.columns = [
        "order_id",
        "customer_id",
        "order_date",
        "ship_date",
        "ship_mode",
        "order_priority",
        "city",
        "state",
        "country",
        "postal_code",
        "market",
        "region"
    ]

    orders["postal_code"] = orders["postal_code"].astype("string")

    print("Orders:", orders.shape)
    print(orders.head())

        # Order items table
    order_items = orders_raw[[
        "Row ID",
        "Order ID",
        "Product ID",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "Shipping Cost"
    ]].copy()

    order_items.columns = [
        "row_id",
        "order_id",
        "product_id",
        "sales",
        "quantity",
        "discount",
        "profit",
        "shipping_cost"
    ]

    print("Order Items:", order_items.shape)
    print(order_items.head())

        # Returns table
    returns = returns_raw[[
        "Order ID",
        "Returned",
        "Market"
    ]].drop_duplicates(subset=["Order ID"], keep="first")

    returns.columns = [
        "order_id",
        "returned",
        "market"
    ]

    print("Returns:", returns.shape)
    print(returns.head())

    # People table
    people = people_raw[[
        "Region",
        "Person"
    ]].copy()

    people.columns = [
        "region",
        "person"
    ]

    print("People:", people.shape)
    print(people.head())

    engine = create_engine(DATABASE_URL)

    print("Loading data into PostgreSQL...")

    customers.to_sql("customers", engine, if_exists="append", index=False)
    products.to_sql("products", engine, if_exists="append", index=False)
    orders.to_sql("orders", engine, if_exists="append", index=False)
    order_items.to_sql("order_items", engine, if_exists="append", index=False)
    returns.to_sql("returns", engine, if_exists="append", index=False)
    people.to_sql("people", engine, if_exists="append", index=False)

    print("Data loaded successfully.")


if __name__ == "__main__":
    main()