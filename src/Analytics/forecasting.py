import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_next_month_sales(df):
    forecast_df = df.copy()

    forecast_df["month"] = (
        forecast_df["order_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_sales = (
        forecast_df.groupby("month")
        .agg(total_sales=("sales", "sum"))
        .reset_index()
        .sort_values("month")
    )

    monthly_sales["month_index"] = range(len(monthly_sales))

    X = monthly_sales[["month_index"]]
    y = monthly_sales["total_sales"]

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = len(monthly_sales)
    forecast_value = model.predict([[next_month_index]])[0]

    next_month = monthly_sales["month"].max() + pd.DateOffset(months=1)

    forecast_row = pd.DataFrame({
        "month": [next_month],
        "total_sales": [forecast_value],
        "type": ["Forecast"]
    })

    historical_df = monthly_sales[["month", "total_sales"]].copy()
    historical_df["type"] = "Historical"

    forecast_chart_df = pd.concat(
        [historical_df, forecast_row],
        ignore_index=True
    )

    return forecast_value, forecast_chart_df