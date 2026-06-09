from src.Analytics.insights import generate_insights, generate_recommendations


def generate_report(df):
    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_quantity = df["quantity"].sum()

    insights = generate_insights(df)
    recommendations = generate_recommendations(df)

    report = f"""
Executive Business Summary

Revenue: ${total_sales:,.2f}
Profit: ${total_profit:,.2f}
Total Orders: {total_orders:,}
Units Sold: {int(total_quantity):,}

Key Insights:
"""

    for insight in insights:
        report += f"- {insight}\n"

    report += "\nRecommendations:\n"

    for recommendation in recommendations:
        report += f"- {recommendation}\n"

    return report