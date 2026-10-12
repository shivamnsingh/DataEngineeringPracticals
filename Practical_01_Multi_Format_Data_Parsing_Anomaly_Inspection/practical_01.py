"""
Practical 1: Multi-Format Data Parsing & Anomaly Inspection
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: Parse Text Files & Inspect Data Quality =====
import pandas as pd

def parse_text_file(filepath):
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            record = {}
            for part in parts:
                if ":" in part:
                    k, v = part.split(":", 1)
                    record[k.strip()] = v.strip() if v.strip() != "None" else None
            if record:
                records.append(record)
    return pd.DataFrame(records)

# Example:
# df_txt = parse_text_file("sample.txt")
# inspect_data(df_txt, "TXT Document")



# ===== Task 2: Parse CSV Files & Identify Domain Anomalies =====
def parse_csv_file(filepath):
    return pd.read_csv(filepath)

# Example:
# df_csv = parse_csv_file("sample.csv")
# inspect_data(df_csv, "CSV Document")



# ===== Task 3: Search, Split & Replace Strings Using Regular Expressions =====
import re

def search_pattern(text, pattern):
    return re.findall(pattern, text)

def split_pattern(text, pattern):
    return re.split(pattern, text)

def replace_pattern(text, pattern, replacement):
    return re.sub(pattern, replacement, text)

data = "Contact: shivam.singh@email.com, Phone: 987-654-3210, Backup: admin@company.org"

emails = search_pattern(data, r"[\w.-]+@[\w.-]+\.\w+")
print("Emails found :", emails)

tokens = split_pattern(data, r"[,:\s]+")
print("Split tokens :", tokens)

masked = replace_pattern(data, r"\d{3}-\d{3}-\d{4}", "XXX-XXX-XXXX")
print("Masked text :", masked)



# ===== Task 4: Relational Database Design & CRUD Operations Using SQL =====
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("""
CREATE TABLE Books (
    BookID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Author TEXT,
    Genre TEXT,
    Price REAL,
    Stock INTEGER
)
""")

cur.executemany("INSERT INTO Books VALUES (?,?,?,?,?,?)", [
    (1, "Clean Code", "Robert Martin", "Programming", 450.00, 12),
    (2, "Atomic Habits", "James Clear", "Self-Help", 320.00, 20),
    (3, "The Alchemist", "Paulo Coelho", "Fiction", 250.00, 8),
])
conn.commit()

# READ
print(pd.read_sql("SELECT * FROM Books", conn))

# UPDATE
cur.execute("UPDATE Books SET Stock = Stock - 3 WHERE BookID = 3")
conn.commit()

# DELETE
cur.execute("DELETE FROM Books WHERE BookID = 2")
conn.commit()

print(pd.read_sql("SELECT * FROM Books", conn))

