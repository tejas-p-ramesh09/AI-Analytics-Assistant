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

    return None, None