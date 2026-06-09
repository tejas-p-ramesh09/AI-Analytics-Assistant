from src.Analytics.data_loader import get_sales_dataset
from src.Analytics.report_generator import generate_report

df = get_sales_dataset()

report = generate_report(df)

print(report)