def generate_insights(df):

    insights = []

    # Revenue by category
    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_sales.index[0]
    top_category_sales = category_sales.iloc[0]

    total_sales = df["sales"].sum()

    contribution = (
        top_category_sales / total_sales * 100
    )

    insights.append(
        f"{top_category} contributes {contribution:.1f}% of total revenue (${top_category_sales:,.0f})."
    )

    # Profit margin
    category_metrics = (
        df.groupby("category")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
    )

    category_metrics["margin"] = (
        category_metrics["profit"]
        / category_metrics["sales"]
        * 100
    )

    lowest_margin_category = category_metrics["margin"].idxmin()
    lowest_margin = category_metrics["margin"].min()

    insights.append(
        f"{lowest_margin_category} has the lowest profit margin ({lowest_margin:.2f}%), indicating pricing or discount pressure."
    )

    # Best region
    region_sales = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_sales.index[0]
    best_region_sales = region_sales.iloc[0]

    insights.append(
        f"{best_region} is the highest-performing region with ${best_region_sales:,.0f} in sales."
    )

    # Top customer
    customer_sales = (
        df.groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_customer = customer_sales.index[0]
    top_customer_sales = customer_sales.iloc[0]

    insights.append(
        f"{top_customer} is the highest-value customer with ${top_customer_sales:,.0f} in revenue."
    )

    # Tables issue
    subcategory_profit = (
        df.groupby("sub_category")["profit"]
        .sum()
        .sort_values()
    )

    worst_subcategory = subcategory_profit.index[0]
    worst_profit = subcategory_profit.iloc[0]

    insights.append(
        f"{worst_subcategory} is the largest loss-making sub-category with ${worst_profit:,.0f} profit."
    )

    return insights



def generate_recommendations(df):

    recommendations = []

    if df.empty:
        return ["No recommendations available for the selected filters."]

    # Category margin analysis
    category_metrics = (
        df.groupby("category")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
    )

    category_metrics["margin"] = (
        category_metrics["profit"] / category_metrics["sales"] * 100
    )

    lowest_margin_category = category_metrics["margin"].idxmin()
    lowest_margin = category_metrics["margin"].min()

    recommendations.append(
        f"Review pricing and discount strategy for {lowest_margin_category}, which has the lowest profit margin at {lowest_margin:.2f}%."
    )

    # Best category by revenue
    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_sales.index[0]

    recommendations.append(
        f"Prioritize growth opportunities in {top_category}, the highest revenue-generating category for the selected filters."
    )

    # Worst sub-category
    subcategory_profit = (
        df.groupby("sub_category")["profit"]
        .sum()
        .sort_values()
    )

    worst_subcategory = subcategory_profit.index[0]
    worst_profit = subcategory_profit.iloc[0]

    if worst_profit < 0:
        recommendations.append(
            f"Investigate {worst_subcategory}, which is currently loss-making with ${worst_profit:,.0f} profit."
        )
    else:
        recommendations.append(
            f"Monitor {worst_subcategory}, which has the lowest profit contribution among sub-categories."
        )

    # Best region
    region_sales = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_sales.index[0]

    recommendations.append(
        f"Use {best_region} as a benchmark region to study successful sales patterns."
    )

    return recommendations