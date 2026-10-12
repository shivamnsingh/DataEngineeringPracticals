"""
Practical 9: End-to-End E-Commerce Multi-Entity Pipeline & Stream Merging
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: Multi-Entity E-Commerce Pipeline & Stream Merging =====
import pandas as pd
import sqlite3

conn = sqlite3.connect("ecommerce_pipeline.db")

def process_new_data(incoming_df, db_conn):
    existing = pd.read_sql(
        "SELECT order_id FROM cleaned_orders", db_conn
    )["order_id"].tolist()

    new_data = incoming_df[
        ~incoming_df["order_id"].isin(existing)
    ].copy()

    if not new_data.empty:
        new_data["total_amount"] = new_data["quantity"] * new_data["price"]
        new_data.to_sql(
            "cleaned_orders", db_conn, if_exists="append", index=False
        )
        print(f"Successfully processed and appended {len(new_data)} new records.")

# Example:
# process_new_data(new_arriving_data, conn)

