import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create reports directory if it doesn't exist
os.makedirs('reports', exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect('database/ecommerce.db')

# Load tables into DataFrames
print("Loading data from database...")
users_df = pd.read_sql_query("SELECT * FROM users", conn)
products_df = pd.read_sql_query("SELECT * FROM products", conn)
orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
order_items_df = pd.read_sql_query("SELECT * FROM order_items", conn)
reviews_df = pd.read_sql_query("SELECT * FROM reviews", conn)

conn.close()

print("\n=== EXPLORATORY DATA ANALYSIS ===\n")

# 1. Count of users
user_count = len(users_df)
print(f"Total Users: {user_count}")

# 2. Count of products
product_count = len(products_df)
print(f"Total Products: {product_count}")

# 3. Monthly order trends
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['year_month'] = orders_df['order_date'].dt.to_period('M')
monthly_orders = orders_df.groupby('year_month').size().reset_index(name='order_count')
print(f"\nMonthly Order Trends:")
print(monthly_orders.to_string(index=False))

# 4. Top 10 selling products
product_sales = order_items_df.groupby('product_id')['quantity'].sum().reset_index()
product_sales = product_sales.merge(products_df[['product_id', 'name']], on='product_id')
product_sales = product_sales.sort_values('quantity', ascending=False).head(10)
print(f"\nTop 10 Selling Products:")
print(product_sales.to_string(index=False))

# 5. Average order value
avg_order_value = orders_df['total_amount'].mean()
print(f"\nAverage Order Value: ${avg_order_value:.2f}")

# 6. Category-wise revenue
order_items_with_products = order_items_df.merge(products_df[['product_id', 'category', 'price']], on='product_id')
order_items_with_products['revenue'] = order_items_with_products['quantity'] * order_items_with_products['price']
category_revenue = order_items_with_products.groupby('category')['revenue'].sum().reset_index()
category_revenue = category_revenue.sort_values('revenue', ascending=False)
print(f"\nCategory-wise Revenue:")
print(category_revenue.to_string(index=False))

# 7. Most active users
user_orders = orders_df.groupby('user_id').size().reset_index(name='order_count')
user_orders = user_orders.merge(users_df[['user_id', 'name']], on='user_id')
user_orders = user_orders.sort_values('order_count', ascending=False).head(10)
print(f"\nTop 10 Most Active Users:")
print(user_orders.to_string(index=False))

# 8. Product rating distribution
rating_distribution = reviews_df['rating'].value_counts().sort_index()
print(f"\nProduct Rating Distribution:")
print(rating_distribution.to_string())

# 9. Correlation between price and rating
products_with_ratings = reviews_df.groupby('product_id')['rating'].mean().reset_index()
products_with_ratings = products_with_ratings.merge(products_df[['product_id', 'price']], on='product_id')
correlation = products_with_ratings['price'].corr(products_with_ratings['rating'])
print(f"\nCorrelation between Price and Rating: {correlation:.4f}")

print("\n=== GENERATING VISUALIZATIONS ===\n")

# Visualization 1: Top 10 products by sales volume
plt.figure(figsize=(12, 6))
plt.barh(product_sales['name'], product_sales['quantity'], color='steelblue')
plt.xlabel('Sales Volume (Quantity)')
plt.ylabel('Product Name')
plt.title('Top 10 Products by Sales Volume')
plt.tight_layout()
plt.savefig('reports/top_10_products.png', dpi=300, bbox_inches='tight')
print("Saved: reports/top_10_products.png")
plt.close()

# Visualization 2: Monthly orders line chart
plt.figure(figsize=(12, 6))
monthly_orders['year_month_str'] = monthly_orders['year_month'].astype(str)
plt.plot(monthly_orders['year_month_str'], monthly_orders['order_count'], marker='o', linewidth=2, color='green')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.title('Monthly Order Trends')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/monthly_orders.png', dpi=300, bbox_inches='tight')
print("Saved: reports/monthly_orders.png")
plt.close()

# Visualization 3: Category revenue bar chart
plt.figure(figsize=(10, 6))
plt.bar(category_revenue['category'], category_revenue['revenue'], color='coral')
plt.xlabel('Category')
plt.ylabel('Revenue ($)')
plt.title('Category-wise Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('reports/category_revenue.png', dpi=300, bbox_inches='tight')
print("Saved: reports/category_revenue.png")
plt.close()

# Visualization 4: Product ratings histogram
plt.figure(figsize=(10, 6))
plt.hist(reviews_df['rating'], bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], color='purple', edgecolor='black', alpha=0.7)
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Product Rating Distribution')
plt.xticks([1, 2, 3, 4, 5])
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('reports/rating_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: reports/rating_distribution.png")
plt.close()

print("\nEDA Completed Successfully")
