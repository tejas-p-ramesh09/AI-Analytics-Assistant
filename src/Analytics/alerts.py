def generate_alerts(df):

    alerts = []

    # Category margins
    category_df = (
        df.groupby("category")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .reset_index()
    )

    category_df["profit_margin_pct"] = (
        category_df["total_profit"]
        / category_df["total_sales"]
        * 100
    )

    for _, row in category_df.iterrows():

        if row["profit_margin_pct"] < 10:

            alerts.append(
                f"Low margin alert: {row['category']} margin is only {row['profit_margin_pct']:.2f}%."
            )

    # Sub-category losses
    subcategory_df = (
        df.groupby("sub_category")
        .agg(
            total_profit=("profit", "sum")
        )
        .reset_index()
    )

    loss_categories = subcategory_df[
        subcategory_df["total_profit"] < 0
    ]

    for _, row in loss_categories.iterrows():

        alerts.append(
            f"Loss alert: {row['sub_category']} has generated ${row['total_profit']:,.0f} profit."
        )

    return alerts