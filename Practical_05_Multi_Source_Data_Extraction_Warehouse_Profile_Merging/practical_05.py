"""
Practical 5: Multi-Source Data Extraction & Warehouse Profile Merging
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: API & CSV Extraction Pipeline =====
import pandas as pd
import requests

def extract_api_data(url):
    data = requests.get(url, timeout=10).json()
    return pd.json_normalize(data)

api_df = extract_api_data("https://jsonplaceholder.typicode.com/users")[["id", "name", "email", "company.name"]]
api_df.rename(columns={"company.name": "company"}, inplace=True)

# Requires locations.csv in the working directory.
# csv_df = pd.read_csv("locations.csv")
# merged_df = pd.merge(api_df, csv_df, on="id", how="inner")
# merged_df.to_csv("cleaned_warehouse_profiles.csv", index=False)

api_df.head()

