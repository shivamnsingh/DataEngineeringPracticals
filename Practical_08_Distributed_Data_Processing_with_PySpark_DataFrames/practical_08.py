"""
Practical 8: Distributed Data Processing with PySpark DataFrames
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Task 1: PySpark Schema Display, Filtering & Join Aggregations =====
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

spark = SparkSession.builder.appName("Practical_8").getOrCreate()

# Requires sales_data.csv and a df_customers DataFrame.
df_sales = spark.read.csv("sales_data.csv", header=True, inferSchema=True)

df_distinct = df_sales.dropDuplicates()

# Example join:
# joined_df = df_distinct.join(df_customers, on="customer_id", how="inner")

average_sales = df_distinct.groupBy("category").agg(
    avg("sales").alias("average_sales")
)

average_sales.show()

