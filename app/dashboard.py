import streamlit as st
import plotly.express as px
import pandas as pd
from src.Analytics.insights import generate_insights
from src.Analytics.data_loader import get_sales_dataset
from src.Analytics.product_analysis import get_worst_subcategories
from src.Analytics.chatbot import answer_question
from src.Analytics.insights import generate_insights, generate_recommendations
from src.Analytics.report_generator import generate_report
from src.Analytics.pdf_generator import create_pdf
from src.Analytics.alerts import generate_alerts
from src.Analytics.forecasting import forecast_next_month_sales

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

# Executive insights
st.subheader("Executive Insights")
insights = generate_insights(filtered_df)
for insight in insights:
    st.info(insight)


# Business recommendations
st.subheader("Business Alerts")
alerts = generate_alerts(filtered_df)
if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.success("No business alerts detected.")


# Chatbot interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.header("Ask Your Data")
question = st.text_input(
    "Ask a business question",
    placeholder="Which region has the highest sales?"
)
if question:
    answer, result_df = answer_question(question, filtered_df)
    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )
    st.code(answer)
    if result_df is not None:
        st.dataframe(result_df, use_container_width=True)
st.subheader("Conversation History")

if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()
recent_history = st.session_state.chat_history[-5:]
for item in reversed(recent_history):
    st.markdown(f"**Question:** {item['question']}")
    st.write("**Answer:**")
    st.code(item["answer"])
    st.divider()


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


# Sales Forecast
st.subheader("Sales Forecast")

forecast_value, forecast_chart_df = forecast_next_month_sales(filtered_df)

st.metric(
    "Predicted Next Month Sales",
    f"${forecast_value:,.2f}"
)

fig_forecast = px.line(
    forecast_chart_df,
    x="month",
    y="total_sales",
    color="type",
    markers=True,
    title="Historical Sales with Next Month Forecast"
)

st.plotly_chart(fig_forecast, use_container_width=True)


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

recommendations = generate_recommendations(filtered_df)

for recommendation in recommendations:
    st.success(recommendation)


st.subheader("Executive Report")

report_text = generate_report(filtered_df)

st.text_area(
    "Generated Report",
    value=report_text,
    height=400
)


st.download_button(
    label="Download Executive Report",
    data=report_text,
    file_name="executive_report.txt",
    mime="text/plain"
)



pdf_file = create_pdf(report_text)

st.download_button(
    label="Download Executive Report as PDF",
    data=pdf_file,
    file_name="executive_report.pdf",
    mime="application/pdf"
)