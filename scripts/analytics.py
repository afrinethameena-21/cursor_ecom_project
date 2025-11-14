import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("database", "ecommerce.db")
REPORTS_DIR = "reports"

def make_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)

def user_spending_summary(conn):
    sql = """
    SELECT
        u.user_id,
        u.name,
        u.city,
        COALESCE(o.num_orders, 0) AS num_orders,
        COALESCE(o.total_spent, 0.0) AS total_spent,
        ROUND(COALESCE(r.avg_rating, NULL), 2) AS avg_rating
    FROM users u
    LEFT JOIN (
        SELECT user_id, COUNT(*) AS num_orders, SUM(total_amount) AS total_spent
        FROM orders
        GROUP BY user_id
    ) o ON u.user_id = o.user_id
    LEFT JOIN (
        SELECT user_id, AVG(rating) AS avg_rating
        FROM reviews
        GROUP BY user_id
    ) r ON u.user_id = r.user_id
    ORDER BY total_spent DESC;
    """
    return pd.read_sql_query(sql, conn)

def top_selling_products(conn, top_n=10):
    sql = """
    SELECT
        p.product_id,
        p.name,
        p.category,
        SUM(oi.quantity) AS total_quantity_sold,
        SUM(oi.quantity * p.price) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.name, p.category, p.price
    ORDER BY total_quantity_sold DESC
    LIMIT ?
    """
    return pd.read_sql_query(sql, conn, params=(top_n,))

def main():
    make_reports_dir()

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run load_to_sqlite.py first.")

    conn = sqlite3.connect(DB_PATH)

    users_summary = user_spending_summary(conn)
    users_summary.to_csv(os.path.join(REPORTS_DIR, "user_spending_summary.csv"), index=False)
    print("\nTop 20 users by total_spent:\n")
    print(users_summary.head(20).to_string(index=False))

    top_products = top_selling_products(conn, top_n=10)
    top_products.to_csv(os.path.join(REPORTS_DIR, "top_products.csv"), index=False)
    print("\nTop selling products (top 10):\n")
    print(top_products.to_string(index=False))

    total_revenue = users_summary['total_spent'].sum()
    total_orders = int(pd.read_sql_query("SELECT COUNT(*) AS cnt FROM orders", conn).iloc[0]['cnt'])
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    summary = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2)
    }
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(os.path.join(REPORTS_DIR, "summary_stats.csv"), index=False)

    print("\nSummary stats:")
    print(summary_df.to_string(index=False))

    conn.close()
    print("\nAnalytics completed — reports written to the 'reports/' folder.")

if __name__ == "__main__":
    main()
