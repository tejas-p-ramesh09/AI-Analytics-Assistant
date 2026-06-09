from src.Analytics.kpis import get_category_performance
from src.Analytics.sales_analysis import get_sales_by_region
from src.Analytics.customer_analysis import get_top_customers
from src.Analytics.product_analysis import get_worst_subcategories


def answer_question(question: str):

    question = question.lower()

    region_keywords = [
        "region",
        "area",
        "market"
    ]

    sales_keywords = [
        "sales",
        "revenue",
        "best",
        "highest"
    ]

    customer_keywords = [
        "customer",
        "buyer",
        "client"
    ]

    category_keywords = [
        "category",
        "categories"
    ]

    profit_keywords = [
        "profit",
        "margin",
        "profitable"
    ]

    worst_keywords = [
        "worst",
        "loss",
        "underperform",
        "underperforming",
        "lowest"
    ]

    if (
        any(word in question for word in region_keywords)
        and
        any(word in question for word in sales_keywords)
    ):
        df = get_sales_by_region()

        top = df.iloc[0]

        return (
            f"{top['region']} has the highest sales with "
            f"${top['total_sales']:,.2f}.",
            df
        )

    if (
        any(word in question for word in category_keywords)
        and
        any(word in question for word in profit_keywords)
    ):
        df = get_category_performance()

        best = df.sort_values(
            "total_profit",
            ascending=False
        ).iloc[0]

        return (
            f"{best['category']} is the most profitable "
            f"category with ${best['total_profit']:,.2f} profit.",
            df
        )

    if any(word in question for word in customer_keywords):

        df = get_top_customers()

        top = df.iloc[0]

        return (
            f"{top['customer_name']} is the top customer "
            f"with ${top['total_sales']:,.2f} in sales.",
            df
        )

    if any(word in question for word in worst_keywords):

        df = get_worst_subcategories()

        worst = df.iloc[0]

        return (
            f"{worst['sub_category']} is the worst performing "
            f"sub-category with ${worst['total_profit']:,.2f} profit.",
            df
        )

    return (
        "I can answer questions about sales, revenue, customers, categories, profits, and underperforming products.",
        None
    )