"""
Practical 7: Multi-File CSV/JSON Pipeline & Incremental Loading
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: JSON Validation Rules & Incremental Load =====
import pandas as pd
import json
import sqlite3

with open("orders.json") as f:
    df_json = pd.DataFrame(json.load(f))

valid_cond = (
    (df_json["sales"] > 0) &
    (df_json["quantity"] > 0) &
    (df_json["customer_id"].notna())
)

df_valid = df_json[valid_cond]

conn = sqlite3.connect("etl_database.db")

df_valid[["order_id", "customer_id", "sales", "quantity"]].to_sql(
    "validated_orders", conn, if_exists="append", index=False
)



# ===== Task 3 & 4: Extract JSON Data, Data Validation & Filtering Invalid Records =====
import json

with open("orders.json", "r") as f:
    json_data = json.load(f)

df_json = pd.DataFrame(json_data)

valid_condition = (
    (df_json["sales"] > 0) &
    (df_json["quantity"] > 0) &
    (df_json["customer_id"].notna())
)

df_valid = df_json[valid_condition].copy()
df_invalid = df_json[~valid_condition].copy()

print(f"Valid Records: {len(df_valid)}")
print(f"Invalid Records Removed: {len(df_invalid)}")

selected_fields = ["order_id", "customer_id", "sales", "quantity"]
df_valid[selected_fields].to_sql(
    "validated_orders", conn, if_exists="replace", index=False
)



# ===== Task 5: Implement Incremental Data Loading =====
def load_incremental(new_data_df, db_conn, table_name):
    try:
        existing_ids = pd.read_sql(
            f"SELECT order_id FROM {table_name}", db_conn
        )["order_id"].tolist()
    except Exception:
        existing_ids = []

    incremental_df = new_data_df[
        ~new_data_df["order_id"].isin(existing_ids)
    ]

    if not incremental_df.empty:
        incremental_df.to_sql(
            table_name, db_conn, if_exists="append", index=False
        )
        print(f"Incremental update complete: {len(incremental_df)} new records added.")
    else:
        print("No new records to load.")

# Example:
# load_incremental(df_valid, conn, "validated_orders")

