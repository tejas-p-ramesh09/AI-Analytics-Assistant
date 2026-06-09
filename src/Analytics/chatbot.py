from src.Analytics.kpis import get_category_performance
from src.Analytics.sales_analysis import get_sales_by_region
from src.Analytics.customer_analysis import get_top_customers
from src.Analytics.product_analysis import get_worst_subcategories
from src.Analytics.explanations import explain_business_metric

def compare_entities(df, column_name, entity_1, entity_2):

    comparison_df = (
        df[df[column_name].isin([entity_1, entity_2])]
        .groupby(column_name)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_orders=("order_id", "nunique"),
            units_sold=("quantity", "sum")
        )
        .reset_index()
    )

    comparison_df["profit_margin_pct"] = (
        comparison_df["total_profit"] / comparison_df["total_sales"] * 100
    ).round(2)

    if len(comparison_df) < 2:
        return "I could not find both items to compare in the selected data.", comparison_df

    best = comparison_df.sort_values("total_profit", ascending=False).iloc[0]

    answer = (
        f"{best[column_name]} performs better based on profit, "
        f"with ${best['total_profit']:,.2f} profit and "
        f"{best['profit_margin_pct']:.2f}% profit margin."
    )

    return answer, comparison_df


def answer_question(question: str, df):

    question = question.lower()

    if df.empty:
        return "No data available for the selected filters.", None
    
    if "compare" in question:

        if "technology" in question and "furniture" in question:
            return compare_entities(
                df,
                "category",
                "Technology",
                "Furniture"
            )

        if "technology" in question and "office supplies" in question:
            return compare_entities(
                df,
                "category",
                "Technology",
                "Office Supplies"
            )

        if "furniture" in question and "office supplies" in question:
            return compare_entities(
                df,
                "category",
                "Furniture",
                "Office Supplies"
            )

        if "central" in question and "east" in question:
            return compare_entities(
                df,
                "region",
                "Central",
                "East"
            )

        if "consumer" in question and "corporate" in question:
            return compare_entities(
                df,
                "segment",
                "Consumer",
                "Corporate"
            )

        if "consumer" in question and "home office" in question:
            return compare_entities(
                df,
                "segment",
                "Consumer",
                "Home Office"
            )

        if "corporate" in question and "home office" in question:
            return compare_entities(
                df,
                "segment",
                "Corporate",
                "Home Office"
            )

        return (
            "I can compare Technology, Furniture, Office Supplies, regions like Central/East, and segments like Consumer/Corporate/Home Office.",
            None
        )
    
    if "why" in question:
        explanation = explain_business_metric(
            question,
            df
        )
        if explanation:
            return explanation, None

    # Region with highest sales
    if "region" in question and ("sales" in question or "revenue" in question or "best" in question or "highest" in question):
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
        return f"{top['region']} has the highest sales with ${top['total_sales']:,.2f}.", result_df

    # Region with lowest profit
    if "region" in question and ("lowest" in question or "worst" in question or "loss" in question):
        result_df = (
            df.groupby("region")
            .agg(total_profit=("profit", "sum"))
            .reset_index()
            .sort_values("total_profit", ascending=True)
        )

        worst = result_df.iloc[0]
        return f"{worst['region']} has the lowest profit with ${worst['total_profit']:,.2f}.", result_df

    # Category profitability
    if "category" in question and ("profit" in question or "margin" in question or "profitable" in question):
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
        return f"{best['category']} is the most profitable category with ${best['total_profit']:,.2f} profit.", result_df

    # Customer analysis
    if "customer" in question or "client" in question or "buyer" in question:
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
        return f"{top['customer_name']} is the top customer with ${top['total_sales']:,.2f} in sales.", result_df

    # Year analysis
    if "year" in question and ("sales" in question or "revenue" in question or "best" in question or "highest" in question):
        result_df = (
            df.groupby("year")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum"),
                total_orders=("order_id", "nunique")
            )
            .reset_index()
            .sort_values("total_sales", ascending=False)
        )

        top = result_df.iloc[0]
        return f"{int(top['year'])} had the highest sales with ${top['total_sales']:,.2f}.", result_df

    # Segment analysis
    if "segment" in question and ("profit" in question or "sales" in question or "revenue" in question):
        result_df = (
            df.groupby("segment")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum"),
                total_orders=("order_id", "nunique")
            )
            .reset_index()
            .sort_values("total_sales", ascending=False)
        )

        top = result_df.iloc[0]
        return f"{top['segment']} is the top customer segment with ${top['total_sales']:,.2f} in sales.", result_df

    # Worst sub-category
    if "worst" in question or "loss" in question or "underperform" in question or "lowest" in question:
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
        return f"{worst['sub_category']} is the worst performing sub-category with ${worst['total_profit']:,.2f} profit.", result_df

    return (
        "I can answer questions about regions, categories, customers, years, segments, revenue, profit, and worst-performing sub-categories.",
        None
    )