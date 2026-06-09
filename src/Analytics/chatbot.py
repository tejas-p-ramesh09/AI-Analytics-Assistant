from src.Analytics.kpis import get_category_performance
from src.Analytics.sales_analysis import get_sales_by_region
from src.Analytics.customer_analysis import get_top_customers
from src.Analytics.product_analysis import get_worst_subcategories


def answer_question(question: str, df):

    question = question.lower()

    region_keywords = ["region", "area", "market"]
    sales_keywords = ["sales", "revenue", "best", "highest"]
    customer_keywords = ["customer", "buyer", "client"]
    category_keywords = ["category", "categories"]
    profit_keywords = ["profit", "margin", "profitable"]
    worst_keywords = ["worst", "loss", "underperform", "underperforming", "lowest"]

    if df.empty:
        return "No data available for the selected filters.", None

    if (
        any(word in question for word in region_keywords)
        and any(word in question for word in sales_keywords)
    ):
        result_df = (
            df.groupby("region")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum")
            )
            .reset_index()
            .sort_values("total_sales", ascending=False)
        )

        top = result_df.iloc[0]

        return (
            f"{top['region']} has the highest sales with ${top['total_sales']:,.2f} for the selected filters.",
            result_df
        )

    if (
        any(word in question for word in category_keywords)
        and any(word in question for word in profit_keywords)
    ):
        result_df = (
            df.groupby("category")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum"),
                units_sold=("quantity", "sum")
            )
            .reset_index()
        )

        result_df["profit_margin_pct"] = (
            result_df["total_profit"] / result_df["total_sales"] * 100
        ).round(2)

        best = result_df.sort_values("total_profit", ascending=False).iloc[0]

        return (
            f"{best['category']} is the most profitable category with ${best['total_profit']:,.2f} profit for the selected filters.",
            result_df.sort_values("total_profit", ascending=False)
        )

    if any(word in question for word in customer_keywords):

        result_df = (
            df.groupby(["customer_name", "segment"])
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum"),
                total_orders=("order_id", "nunique")
            )
            .reset_index()
            .sort_values("total_sales", ascending=False)
            .head(10)
        )

        top = result_df.iloc[0]

        return (
            f"{top['customer_name']} is the top customer with ${top['total_sales']:,.2f} in sales for the selected filters.",
            result_df
        )

    if any(word in question for word in worst_keywords):

        result_df = (
            df.groupby("sub_category")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum")
            )
            .reset_index()
            .sort_values("total_profit", ascending=True)
            .head(10)
        )

        result_df["profit_margin_pct"] = (
            result_df["total_profit"] / result_df["total_sales"] * 100
        ).round(2)

        worst = result_df.iloc[0]

        return (
            f"{worst['sub_category']} is the worst performing sub-category with ${worst['total_profit']:,.2f} profit for the selected filters.",
            result_df
        )

    return (
        "I can answer questions about sales, revenue, customers, categories, profits, and underperforming products.",
        None
    )