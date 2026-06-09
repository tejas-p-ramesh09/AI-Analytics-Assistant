def explain_business_metric(question, df):

    question = question.lower()

    # Furniture
    if "furniture" in question:

        furniture_df = df[df["category"] == "Furniture"]

        sales = furniture_df["sales"].sum()
        profit = furniture_df["profit"].sum()

        margin = (
            profit / sales * 100
            if sales > 0 else 0
        )

        worst_subcategory = (
            furniture_df.groupby("sub_category")["profit"]
            .sum()
            .sort_values()
            .index[0]
        )

        worst_profit = (
            furniture_df.groupby("sub_category")["profit"]
            .sum()
            .sort_values()
            .iloc[0]
        )

        return (
            f"Furniture generated ${sales:,.0f} in sales and "
            f"${profit:,.0f} in profit, resulting in a "
            f"{margin:.2f}% profit margin. "
            f"{worst_subcategory} contributed the lowest profit "
            f"(${worst_profit:,.0f}) and appears to be the main driver "
            f"of underperformance."
        )

    # Technology
    if "technology" in question:

        tech_df = df[df["category"] == "Technology"]

        sales = tech_df["sales"].sum()
        profit = tech_df["profit"].sum()

        margin = (
            profit / sales * 100
            if sales > 0 else 0
        )

        return (
            f"Technology generated ${sales:,.0f} in sales and "
            f"${profit:,.0f} in profit, producing a "
            f"{margin:.2f}% profit margin. "
            f"It is one of the strongest performing categories "
            f"in the selected dataset."
        )

    # Region
    if "region" in question:

        region_sales = (
            df.groupby("region")
            .agg(
                sales=("sales", "sum"),
                profit=("profit", "sum")
            )
            .sort_values("sales", ascending=False)
        )

        best_region = region_sales.index[0]

        sales = region_sales.iloc[0]["sales"]
        profit = region_sales.iloc[0]["profit"]

        return (
            f"{best_region} generated "
            f"${sales:,.0f} in sales and "
            f"${profit:,.0f} in profit, making it the "
            f"best-performing region in the selected data."
        )

    return None