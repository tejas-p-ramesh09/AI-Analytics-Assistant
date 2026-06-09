def analyze_trends(df):

    trend_df = df.copy()

    trend_df["month"] = (
        trend_df["order_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_sales = (
        trend_df.groupby("month")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .reset_index()
        .sort_values("month")
    )

    return monthly_sales


def answer_trend_question(question, df):

    question = question.lower()

    trend_df = analyze_trends(df)

    # Highest sales month
    if (
        "highest month" in question
        or ("month" in question and "highest sales" in question)
        or ("month" in question and "best sales" in question)
    ):

        best_month = (
            trend_df.sort_values(
                "total_sales",
                ascending=False
            )
            .iloc[0]
        )

        return (
            f"{best_month['month'].strftime('%B %Y')} had the highest sales with ${best_month['total_sales']:,.2f}.",
            trend_df
        )

    # Highest profit month
    if (
        "highest profit" in question and "month" in question
    ):

        best_month = (
            trend_df.sort_values(
                "total_profit",
                ascending=False
            )
            .iloc[0]
        )

        return (
            f"{best_month['month'].strftime('%B %Y')} had the highest profit with ${best_month['total_profit']:,.2f}.",
            trend_df
        )

    # Lowest sales month
    if (
        "lowest sales month" in question
        or ("month" in question and "lowest sales" in question)
    ):

        worst_month = (
            trend_df.sort_values(
                "total_sales",
                ascending=True
            )
            .iloc[0]
        )

        return (
            f"{worst_month['month'].strftime('%B %Y')} had the lowest sales with ${worst_month['total_sales']:,.2f}.",
            trend_df
        )

    # Lowest profit month
    if (
        "lowest profit month" in question
        or ("month" in question and "lowest profit" in question)
    ):

        worst_month = (
            trend_df.sort_values(
                "total_profit",
                ascending=True
            )
            .iloc[0]
        )

        return (
            f"{worst_month['month'].strftime('%B %Y')} had the lowest profit with ${worst_month['total_profit']:,.2f}.",
            trend_df
        )
    

    yearly_df = analyze_yearly_trends(df)

    if "year" in question and "highest sales" in question:
        best_year = yearly_df.sort_values("total_sales", ascending=False).iloc[0]

        return (
            f"{int(best_year['year'])} had the highest sales with ${best_year['total_sales']:,.2f}.",
            yearly_df
        )

    if "year" in question and "highest profit" in question:
        best_year = yearly_df.sort_values("total_profit", ascending=False).iloc[0]

        return (
            f"{int(best_year['year'])} had the highest profit with ${best_year['total_profit']:,.2f}.",
            yearly_df
        )

    if "grew fastest" in question or "fastest growth" in question:
        growth_df = yearly_df.dropna(subset=["sales_growth_pct"])

        best_growth = growth_df.sort_values("sales_growth_pct", ascending=False).iloc[0]

        return (
            f"{int(best_growth['year'])} had the fastest sales growth at {best_growth['sales_growth_pct']:.2f}% compared to the previous year.",
            yearly_df
        )
    
    if "2013" in question and "2014" in question:
        return compare_years(df, 2013, 2014)

    if "2012" in question and "2013" in question:
        return compare_years(df, 2012, 2013)

    if "2011" in question and "2012" in question:
        return compare_years(df, 2011, 2012)

    return None, None



def analyze_yearly_trends(df):

    yearly_df = (
        df.groupby("year")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_orders=("order_id", "nunique")
        )
        .reset_index()
        .sort_values("year")
    )

    yearly_df["sales_growth_pct"] = (
        yearly_df["total_sales"]
        .pct_change()
        .mul(100)
        .round(2)
    )

    return yearly_df



def compare_years(df, year_1, year_2):

    yearly_df = analyze_yearly_trends(df)

    y1 = yearly_df[yearly_df["year"] == year_1]
    y2 = yearly_df[yearly_df["year"] == year_2]

    if y1.empty or y2.empty:
        return None, None

    sales_1 = y1.iloc[0]["total_sales"]
    sales_2 = y2.iloc[0]["total_sales"]

    growth_pct = (
        (sales_2 - sales_1)
        / sales_1
        * 100
    )

    answer = (
        f"Sales increased from ${sales_1:,.2f} in {year_1} "
        f"to ${sales_2:,.2f} in {year_2}, "
        f"representing {growth_pct:.2f}% year-over-year growth."
    )

    return answer, yearly_df