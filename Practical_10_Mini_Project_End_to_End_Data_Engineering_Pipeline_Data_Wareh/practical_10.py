"""
Practical 10: Mini Project — End-to-End Data Engineering Pipeline & Data Warehouse Architecture
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: Multi-Source Data Ingestion & Raw Catalog Setup =====
print("Name: Shivam Singh")
print("=== TASK 1: MULTI-SOURCE DATA INGESTION ===")

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta

np.random.seed(42)

# Source 1: Raw Customers
raw_customers = pd.DataFrame({
    "customer_id": [f"C{100+i}" for i in range(1, 11)],
    "customer_name": ["Alice Smith", "Bob Jones", "Charlie Brown", "David Lee", "Emma Watson",
                      "Frank Miller", "Grace Hopper", "Henry Ford", "Ivy Taylor", "Jack Ryan"],
    "city": ["Mumbai", "Pune", "Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad", "Bangalore", "Chennai", "Delhi"],
    "signup_date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-04-05", "2025-05-12",
                    "2025-06-18", "2025-07-22", "2025-08-30", "2025-09-14", "2025-10-01"]
})

# Source 2: Raw Products Catalog
raw_products = pd.DataFrame({
    "product_id": [f"P{200+i}" for i in range(1, 7)],
    "product_name": ["Ultra Laptop Pro", "Ergonomic Mouse", "Mechanical Keyboard", 
                     "4K Monitor 27inch", "USB-C Hub Multiport", "Noise-Cancelling Headphones"],
    "category": ["Computers", "Accessories", "Accessories", "Displays", "Accessories", "Audio"],
    "unit_price": [1200.0, 35.0, 85.0, 350.0, 45.0, 180.0],
    "unit_cost": [850.0, 15.0, 40.0, 220.0, 20.0, 95.0]
})

# Source 3: Raw Transactional Orders (Simulating dirty real-world batch data)
n_orders = 30
order_dates = [datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 90))) for _ in range(n_orders)]
raw_orders = pd.DataFrame({
    "order_id": [f"ORD{1000+i}" for i in range(n_orders)],
    "customer_id": [f"C{100 + np.random.randint(1, 11)}" for _ in range(n_orders)],
    "product_id": [f"P{200 + np.random.randint(1, 7)}" for _ in range(n_orders)],
    "order_date": [d.strftime("%Y-%m-%d") for d in order_dates],
    "quantity": [np.random.randint(1, 6) for _ in range(n_orders)],
    "discount_pct": [np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20]) for _ in range(n_orders)]
})

# Inject dirty data: 2 duplicates, 2 null values, 1 negative quantity anomaly
raw_orders = pd.concat([raw_orders, raw_orders.iloc[[2]], raw_orders.iloc[[7]]], ignore_index=True)
raw_orders.loc[4, "quantity"] = -3  # Anomaly: negative quantity
raw_orders.loc[12, "discount_pct"] = np.nan  # Missing discount
raw_orders.loc[18, "customer_id"] = np.nan  # Missing customer

print(f"Ingested Customers : {len(raw_customers)} records")
print(f"Ingested Products  : {len(raw_products)} records")
print(f"Ingested Orders    : {len(raw_orders)} records")



# ===== Task 2: Data Cleaning & Automated Quality Auditing =====
print("=== TASK 2: DATA CLEANING & AUDITING ===")
init_count = len(raw_orders)

# 1. Deduplication
df_orders = raw_orders.drop_duplicates(subset=["order_id"]).copy()
dups_removed = init_count - len(df_orders)

# 2. Filtering invalid anomalies (negative or zero quantities)
invalid_qty_mask = df_orders["quantity"] <= 0
invalid_removed = invalid_qty_mask.sum()
df_orders = df_orders[~invalid_qty_mask].copy()

# 3. Handling missing values
df_orders = df_orders.dropna(subset=["customer_id"]).copy()
df_orders["discount_pct"] = df_orders["discount_pct"].fillna(0.0)

print(f"Duplicate records removed : {dups_removed}")
print(f"Invalid quantity records  : {invalid_removed}")
print(f"Cleaned validated orders  : {len(df_orders)} records retained")



# ===== Task 3: Pipeline Transformation & Financial Feature Enrichment =====
print("=== TASK 3: TRANSFORMATION & ENRICHMENT ===")
df_transformed = df_orders.merge(raw_products[["product_id", "unit_price", "unit_cost"]], on="product_id", how="inner")
df_transformed["gross_amount"] = (df_transformed["quantity"] * df_transformed["unit_price"]).round(2)
df_transformed["discount_amount"] = (df_transformed["gross_amount"] * df_transformed["discount_pct"]).round(2)
df_transformed["net_amount"] = (df_transformed["gross_amount"] - df_transformed["discount_amount"]).round(2)
df_transformed["total_cost"] = (df_transformed["quantity"] * df_transformed["unit_cost"]).round(2)
df_transformed["profit"] = (df_transformed["net_amount"] - df_transformed["total_cost"]).round(2)

print("Sample Transformed Records:")
print(df_transformed[["order_id", "customer_id", "product_id", "quantity", "gross_amount", "discount_amount", "net_amount", "profit"]].head(5).to_string(index=False))



# ===== Task 4: Operational Data Store (ODS) Relational Storage =====
print("=== TASK 4: OPERATIONAL STORAGE (ODS DATABASE) ===")
ods_conn = sqlite3.connect("enterprise_data_warehouse.db")
ods_cursor = ods_conn.cursor()

raw_customers.to_sql("ods_customers", ods_conn, if_exists="replace", index=False)
raw_products.to_sql("ods_products", ods_conn, if_exists="replace", index=False)
df_transformed.to_sql("ods_orders", ods_conn, if_exists="replace", index=False)

print("ODS Staging Tables Successfully Created: ods_customers, ods_products, ods_orders")



# ===== Task 5: Data Warehouse Architecture — Star Schema Dimensional Modeling =====
print("=== TASK 5: STAR SCHEMA DATA WAREHOUSE MODELING ===")

ods_cursor.executescript("""
DROP TABLE IF EXISTS Fact_Sales;
DROP TABLE IF EXISTS Dim_Customer;
DROP TABLE IF EXISTS Dim_Product;
DROP TABLE IF EXISTS Dim_Date;

CREATE TABLE Dim_Customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT UNIQUE,
    customer_name TEXT,
    city TEXT,
    tier TEXT
);

CREATE TABLE Dim_Product (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE,
    product_name TEXT,
    category TEXT,
    unit_price REAL,
    unit_cost REAL
);

CREATE TABLE Dim_Date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    day_name TEXT
);

CREATE TABLE Fact_Sales (
    sales_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_key INTEGER,
    product_key INTEGER,
    date_key INTEGER,
    order_id TEXT,
    quantity INTEGER,
    gross_amount REAL,
    discount_amount REAL,
    net_amount REAL,
    profit REAL,
    FOREIGN KEY (customer_key) REFERENCES Dim_Customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES Dim_Product(product_key),
    FOREIGN KEY (date_key) REFERENCES Dim_Date(date_key)
);
""")

# Populate Dim_Customer
customer_spend = df_transformed.groupby("customer_id")["net_amount"].sum()
def assign_tier(c_id):
    spend = customer_spend.get(c_id, 0)
    if spend > 2500: return "Gold Tier"
    elif spend > 1000: return "Silver Tier"
    else: return "Bronze Tier"

dim_cust = raw_customers.copy()
dim_cust["tier"] = dim_cust["customer_id".apply(assign_tier) if False else "customer_id"].apply(assign_tier)
for _, r in dim_cust.iterrows():
    ods_cursor.execute("INSERT INTO Dim_Customer (customer_id, customer_name, city, tier) VALUES (?, ?, ?, ?)",
                       (r["customer_id"], r["customer_name"], r["city"], r["tier"]))

# Populate Dim_Product
for _, r in raw_products.iterrows():
    ods_cursor.execute("INSERT INTO Dim_Product (product_id, product_name, category, unit_price, unit_cost) VALUES (?, ?, ?, ?, ?)",
                       (r["product_id"], r["product_name"], r["category"], r["unit_price"], r["unit_cost"]))

# Populate Dim_Date
unique_dates = pd.to_datetime(df_transformed["order_date"].unique())
for d in unique_dates:
    date_key = int(d.strftime("%Y%m%d"))
    full_date = d.strftime("%Y-%m-%d")
    ods_cursor.execute("""
        INSERT INTO Dim_Date (date_key, full_date, year, quarter, month, month_name, day, day_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date_key, full_date, d.year, d.quarter, d.month, d.strftime("%B"), d.day, d.strftime("%A")))

# Populate Fact_Sales via Dimensional Lookups
dim_cust_df = pd.read_sql("SELECT customer_key, customer_id FROM Dim_Customer", ods_conn)
dim_prod_df = pd.read_sql("SELECT product_key, product_id FROM Dim_Product", ods_conn)
dim_date_df = pd.read_sql("SELECT date_key, full_date FROM Dim_Date", ods_conn)

fact_prep = df_transformed.merge(dim_cust_df, on="customer_id", how="inner") \
                           .merge(dim_prod_df, on="product_id", how="inner") \
                           .merge(dim_date_df, left_on="order_date", right_on="full_date", how="inner")

fact_records = fact_prep[["customer_key", "product_key", "date_key", "order_id", 
                          "quantity", "gross_amount", "discount_amount", "net_amount", "profit"]]
fact_records.to_sql("Fact_Sales", ods_conn, if_exists="append", index=False)
ods_conn.commit()

print("Star Schema Data Warehouse Populated Successfully:")
print(f"  - Dim_Customer : {ods_cursor.execute('SELECT COUNT(*) FROM Dim_Customer').fetchone()[0]} rows")
print(f"  - Dim_Product  : {ods_cursor.execute('SELECT COUNT(*) FROM Dim_Product').fetchone()[0]} rows")
print(f"  - Dim_Date     : {ods_cursor.execute('SELECT COUNT(*) FROM Dim_Date').fetchone()[0]} rows")
print(f"  - Fact_Sales   : {ods_cursor.execute('SELECT COUNT(*) FROM Fact_Sales').fetchone()[0]} rows")



# ===== Task 6: Business Intelligence, Analytical Queries & Executive Reporting =====
print("=== TASK 6: BUSINESS INTELLIGENCE & ANALYTICAL REPORTING ===")

print("\n--- KPI REPORT 1: EXECUTIVE FINANCIAL OVERVIEW ---")
kpi1_query = """
SELECT 
    COUNT(sales_key) AS total_orders,
    SUM(quantity) AS total_units_sold,
    PRINTF('$%,.2f', SUM(gross_amount)) AS total_gross_sales,
    PRINTF('$%,.2f', SUM(discount_amount)) AS total_discounts,
    PRINTF('$%,.2f', SUM(net_amount)) AS total_net_revenue,
    PRINTF('$%,.2f', SUM(profit)) AS total_profit,
    PRINTF('%.2f%%', (SUM(profit) / SUM(net_amount)) * 100) AS overall_profit_margin
FROM Fact_Sales;
"""
print(pd.read_sql(kpi1_query, ods_conn).to_string(index=False))

print("\n--- KPI REPORT 2: CATEGORY PERFORMANCE & PROFITABILITY ---")
kpi2_query = """
SELECT 
    p.category,
    COUNT(f.sales_key) AS transactions,
    SUM(f.quantity) AS units_sold,
    PRINTF('$%,.2f', SUM(f.net_amount)) AS net_revenue,
    PRINTF('$%,.2f', SUM(f.profit)) AS net_profit,
    PRINTF('%.2f%%', (SUM(f.profit) / SUM(f.net_amount)) * 100) AS margin_pct
FROM Fact_Sales f
JOIN Dim_Product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY SUM(f.net_amount) DESC;
"""
print(pd.read_sql(kpi2_query, ods_conn).to_string(index=False))

print("\n--- KPI REPORT 3: REGIONAL REVENUE & CUSTOMER TIER BREAKDOWN ---")
kpi3_query = """
SELECT 
    c.city,
    c.tier,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    SUM(f.quantity) AS total_items,
    PRINTF('$%,.2f', SUM(f.net_amount)) AS regional_revenue
FROM Fact_Sales f
JOIN Dim_Customer c ON f.customer_key = c.customer_key
GROUP BY c.city, c.tier
ORDER BY SUM(f.net_amount) DESC;
"""
print(pd.read_sql(kpi3_query, ods_conn).to_string(index=False))

print("\n--- KPI REPORT 4: MONTHLY SALES TREND ANALYSIS ---")
kpi4_query = """
SELECT 
    d.year,
    d.month_name AS month,
    COUNT(f.sales_key) AS order_volume,
    SUM(f.quantity) AS units,
    PRINTF('$%,.2f', SUM(f.net_amount)) AS monthly_revenue,
    PRINTF('$%,.2f', AVG(f.net_amount)) AS avg_order_value
FROM Fact_Sales f
JOIN Dim_Date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
"""
print(pd.read_sql(kpi4_query, ods_conn).to_string(index=False))

ods_conn.close()

