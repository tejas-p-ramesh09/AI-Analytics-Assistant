import streamlit as st
import plotly.express as px

from src.Analytics.kpis import get_overall_kpis, get_category_performance
from src.Analytics.sales_analysis import get_sales_by_region, get_monthly_sales_trend
from src.Analytics.customer_analysis import get_top_customers


st.set_page_config(
    page_title="AI Analytics Assistant",
    layout="wide"
)

st.title("AI-Powered Business Analytics Assistant")
st.write("Business analytics dashboard powered by PostgreSQL and Python.")


# Overall KPIs
kpis = get_overall_kpis().iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${kpis['total_sales']:,.2f}")
col2.metric("Total Profit", f"${kpis['total_profit']:,.2f}")
col3.metric("Total Orders", f"{int(kpis['total_orders']):,}")
col4.metric("Units Sold", f"{int(kpis['total_quantity']):,}")


st.divider()

# Category performance
st.subheader("Category Performance")
category_df = get_category_performance()
st.dataframe(category_df, use_container_width=True)


# Sales by region
st.subheader("Sales by Region")
region_df = get_sales_by_region()
fig_region = px.bar(
    region_df,
    x="region",
    y="total_sales",
    title="Total Sales by Region",
    text_auto=".2s"
)

st.plotly_chart(fig_region, use_container_width=True)


# Monthly sales trend
st.subheader("Monthly Sales Trend")
monthly_df = get_monthly_sales_trend()
fig_monthly = px.line(
    monthly_df,
    x="month",
    y="total_sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig_monthly, use_container_width=True)


# Top customers
st.subheader("Top Customers")
customers_df = get_top_customers()
st.dataframe(customers_df, use_container_width=True)