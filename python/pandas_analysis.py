import pandas as pd

# Load and prepare data

df = pd.read_csv("ecommerce_sales_2026.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.month_name()

# Data validation

print("\n--- DATA VALIDATION ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Missing values:", df.isnull().sum().sum())
print("Duplicate Order IDs:", df["Order_ID"].duplicated().sum())
print("Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Unit Price <= 0:", (df["Unit_Price"] <= 0).sum())
print("Sales <= 0:", (df["Sales"] <= 0).sum())

# Sales by category

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- SALES BY CATEGORY ---")
print(category_sales)

# Sales by region

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- SALES BY REGION ---")
print(region_sales)

# Sales by product

product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- SALES BY PRODUCT ---")
print(product_sales)

# Units sold by product

product_quantity = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- UNITS SOLD BY PRODUCT ---")
print(product_quantity)

# Average sales by category

category_aov = (
    df.groupby("Category")["Sales"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- AVERAGE SALES BY CATEGORY ---")
print(category_aov)

# Monthly sales

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August"
]

df["Month_Name"] = pd.Categorical(
    df["Month_Name"],
    categories=month_order,
    ordered=True
)

monthly_sales = (
    df.groupby("Month_Name", observed=True)["Sales"]
    .sum()
)

print("\n--- MONTHLY SALES ---")
print(monthly_sales)

# Overall KPIs

total_sales = df["Sales"].sum()
total_orders = df["Order_ID"].nunique()
average_order_value = df["Sales"].mean()
total_units = df["Quantity"].sum()

print("\n--- OVERALL KPIs ---")
print(f"Total Sales: {total_sales:,.2f} Kč")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: {average_order_value:,.2f} Kč")
print(f"Total Units Sold: {total_units:,}")

# Sales by discount level

discount_sales = (
    df.groupby("Discount")["Sales"]
    .agg(["sum", "mean", "count"])
    .sort_index()
)

print("\n--- SALES BY DISCOUNT ---")
print(discount_sales)

# Sales by payment method

payment_sales = (
    df.groupby("Payment_Method")["Sales"]
    .agg(["sum", "mean", "count"])
    .sort_values("sum", ascending=False)
)

print("\n--- SALES BY PAYMENT METHOD ---")
print(payment_sales)

# Top customers

customer_sales = (
    df.groupby("Customer")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 10 CUSTOMERS ---")
print(customer_sales.head(10))

# Discount analysis

df["Discount_Amount"] = (
    df["Sales"] * df["Discount"] / (100 - df["Discount"])
)

total_discount = df["Discount_Amount"].sum()
gross_sales = df["Sales"].sum() + total_discount
discount_rate = total_discount / gross_sales * 100

print("\n--- DISCOUNT ANALYSIS ---")
print(f"Gross Sales: {gross_sales:,.2f} Kč")
print(f"Total Discount Given: {total_discount:,.2f} Kč")
print(f"Overall Discount Rate: {discount_rate:.2f}%")
