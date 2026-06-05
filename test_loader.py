from src.Analytics.data_loader import get_sales_dataset

df = get_sales_dataset()

print(df.head())
print(df.shape)