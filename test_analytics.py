from src.Analytics.kpis import get_overall_kpis, get_category_performance
from src.Analytics.sales_analysis import get_sales_by_region, get_monthly_sales_trend
from src.Analytics.customer_analysis import get_top_customers

print("Overall KPIs")
print(get_overall_kpis())

print("\nCategory Performance")
print(get_category_performance())

print("\nSales by Region")
print(get_sales_by_region())

print("\nMonthly Sales Trend")
print(get_monthly_sales_trend())

print("\nTop Customers")
print(get_top_customers())