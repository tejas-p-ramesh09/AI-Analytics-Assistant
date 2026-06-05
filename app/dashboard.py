import streamlit as st
import plotly.express as px
import pandas as pd
from src.Analytics.insights import generate_insights
from src.Analytics.data_loader import get_sales_dataset
from src.Analytics.product_analysis import get_worst_subcategories

st.set_page_config(
    page_title="AI Analytics Assistant",
    layout="wide"
)

st.title("AI-Powered Business Analytics Assistant")
st.write("Interactive business analytics dashboard powered by PostgreSQL and Python.")


# Load data
df = get_sales_dataset()
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year


# Sidebar filters
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["year"].unique().tolist())
)

selected_region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["region"].unique().tolist())
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique().tolist())
)

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    ["All"] + sorted(df["segment"].unique().tolist())
)


# Apply filters
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if selected_segment != "All":
    filtered_df = filtered_df[filtered_df["segment"] == selected_segment]

st.subheader("Executive Insights")
insights = generate_insights(filtered_df)
for insight in insights:
    st.info(insight)

# KPI cards
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Units Sold", f"{int(total_quantity):,}")

st.divider()


# Category Performance
st.subheader("Category Performance")

category_df = (
    filtered_df.groupby("category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        units_sold=("quantity", "sum")
    )
    .reset_index()
)

category_df["profit_margin_pct"] = (
    category_df["total_profit"] / category_df["total_sales"] * 100
).round(2)

st.dataframe(category_df, use_container_width=True)


# Sales by Region
st.subheader("Sales by Region")

region_df = (
    filtered_df.groupby("region")
    .agg(total_sales=("sales", "sum"))
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

fig_region = px.bar(
    region_df,
    x="region",
    y="total_sales",
    title="Total Sales by Region",
    text_auto=".2s"
)

st.plotly_chart(fig_region, use_container_width=True)


# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_df = (
    filtered_df.copy()
)

monthly_df["month"] = monthly_df["order_date"].apply(lambda x: x.replace(day=1))

monthly_df = (
    monthly_df.groupby("month")
    .agg(total_sales=("sales", "sum"))
    .reset_index()
    .sort_values("month")
)

fig_monthly = px.line(
    monthly_df,
    x="month",
    y="total_sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig_monthly, use_container_width=True)


# Top Customers
st.subheader("Top Customers")

customers_df = (
    filtered_df.groupby(["customer_name", "segment"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
    .head(10)
)

st.dataframe(customers_df, use_container_width=True)

st.subheader("Worst Performing Sub-Categories")

worst_df = get_worst_subcategories()

fig_worst = px.bar(
    worst_df,
    x="total_profit",
    y="sub_category",
    orientation="h",
    title="Lowest Profit Sub-Categories",
    text_auto=".2s"
)
st.plotly_chart(fig_worst, use_container_width=True)
st.dataframe(worst_df, use_container_width=True)

st.subheader("Business Recommendations")
st.success(
    "Focus sales efforts on high-performing Technology products."
)
st.warning(
    "Review pricing and discount strategies for Furniture and Tables."
)
st.info(
    "Increase marketing investment in the Central region where revenue is strongest."
)