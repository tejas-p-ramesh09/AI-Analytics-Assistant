from src.Analytics.data_loader import get_sales_dataset
from src.Analytics.insights import generate_insights

df = get_sales_dataset()

for insight in generate_insights(df):
    print(insight)