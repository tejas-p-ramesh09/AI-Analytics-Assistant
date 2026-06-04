DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS people;

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255),
    segment VARCHAR(100)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT,
    category VARCHAR(100),
    sub_category VARCHAR(100)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES customers(customer_id),

    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(100),
    order_priority VARCHAR(100),

    city VARCHAR(150),
    state VARCHAR(150),
    country VARCHAR(150),
    postal_code VARCHAR(50),
    market VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE order_items (
    row_id INTEGER PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES orders(order_id),
    product_id VARCHAR(50) REFERENCES products(product_id),

    sales NUMERIC(12, 4),
    quantity INTEGER,
    discount NUMERIC(6, 4),
    profit NUMERIC(12, 4),
    shipping_cost NUMERIC(12, 4)
);

CREATE TABLE returns (
    order_id VARCHAR(50) PRIMARY KEY REFERENCES orders(order_id),
    returned VARCHAR(20),
    market VARCHAR(100)
);

CREATE TABLE people (
    region VARCHAR(100) PRIMARY KEY,
    person VARCHAR(255)
);