import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Set random seed for reproducibility
random.seed(42)
Faker.seed(42)

# Generate users.csv
print("Generating users.csv...")
users = []
for i in range(1, 51):
    users.append({
        'user_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'city': fake.city()
    })
users_df = pd.DataFrame(users)
users_df.to_csv('data/users.csv', index=False)

# Generate products.csv
print("Generating products.csv...")
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food']
products = []
for i in range(1, 51):
    products.append({
        'product_id': i,
        'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
        'category': random.choice(categories),
        'price': round(random.uniform(5.99, 999.99), 2)
    })
products_df = pd.DataFrame(products)
products_df.to_csv('data/products.csv', index=False)

# Generate orders.csv
print("Generating orders.csv...")
orders = []
end_date = datetime.now()
start_date = end_date - timedelta(days=730)  # 2 years ago

for i in range(1, 201):
    random_days = random.randint(0, 730)
    order_date = start_date + timedelta(days=random_days)
    orders.append({
        'order_id': i,
        'user_id': random.randint(1, 50),
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_amount': 0  # Will calculate after order_items
    })
orders_df = pd.DataFrame(orders)

# Generate order_items.csv
print("Generating order_items.csv...")
order_items = []
item_id = 1

for order in orders:
    num_items = random.randint(1, 5)
    order_total = 0
    
    for _ in range(num_items):
        product_id = random.randint(1, 50)
        quantity = random.randint(1, 5)
        product_price = products_df[products_df['product_id'] == product_id]['price'].values[0]
        
        order_items.append({
            'item_id': item_id,
            'order_id': order['order_id'],
            'product_id': product_id,
            'quantity': quantity
        })
        
        order_total += product_price * quantity
        item_id += 1
    
    # Update order total_amount
    orders_df.loc[orders_df['order_id'] == order['order_id'], 'total_amount'] = round(order_total, 2)

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv('data/order_items.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)

# Generate reviews.csv
print("Generating reviews.csv...")
review_texts = [
    "Great product, highly recommend!",
    "Good quality for the price.",
    "Not what I expected, disappointed.",
    "Excellent! Will buy again.",
    "Average product, nothing special.",
    "Poor quality, would not recommend.",
    "Amazing! Exceeded my expectations.",
    "Decent product, does the job.",
    "Terrible experience, waste of money.",
    "Love it! Perfect for my needs."
]

reviews = []
for i in range(1, 151):
    reviews.append({
        'review_id': i,
        'user_id': random.randint(1, 50),
        'product_id': random.randint(1, 50),
        'rating': random.randint(1, 5),
        'review_text': random.choice(review_texts)
    })
reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv('data/reviews.csv', index=False)

print("CSV generation completed")
