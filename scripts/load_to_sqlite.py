import sqlite3
import pandas as pd
import os

# Create database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect('database/ecommerce.db')

# Load users.csv
print("Loading users.csv...")
users_df = pd.read_csv('data/users.csv')
users_df.to_sql('users', conn, if_exists='replace', index=False)

# Load products.csv
print("Loading products.csv...")
products_df = pd.read_csv('data/products.csv')
products_df.to_sql('products', conn, if_exists='replace', index=False)

# Load orders.csv
print("Loading orders.csv...")
orders_df = pd.read_csv('data/orders.csv')
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# Load order_items.csv
print("Loading order_items.csv...")
order_items_df = pd.read_csv('data/order_items.csv')
order_items_df.to_sql('order_items', conn, if_exists='replace', index=False)

# Load reviews.csv
print("Loading reviews.csv...")
reviews_df = pd.read_csv('data/reviews.csv')
reviews_df.to_sql('reviews', conn, if_exists='replace', index=False)

# Close connection
conn.close()

print("Database loaded successfully")
