/*
Practical 2: ETL Pipeline Implementation & Data Transformation (MySQL Workbench)
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
*/

-- ===== Task 1: Relational Schema Setup & Staging Data Load =====
-- PRACTICAL 2: ETL PIPELINE IMPLEMENTATION & DATA TRANSFORMATION
CREATE DATABASE IF NOT EXISTS ETL_Lab_Practical2;
USE ETL_Lab_Practical2;

CREATE TABLE stg_Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10,2),
    UnitsInStock INT
);

CREATE TABLE stg_Orders (
    OrderID INT PRIMARY KEY,
    ProductID INT,
    CustomerName VARCHAR(100),
    Quantity INT,
    Discount DECIMAL(5,2),
    OrderDate DATE
);

INSERT INTO stg_Products VALUES
(101, 'LAPTOP PRO 15', 'ELECTRONICS', 1200.00, 15),
(102, 'WIRELESS MOUSE', 'ELECTRONICS', 25.00, 100),
(104, 'MECHANICAL KEYBOARD', 'ELECTRONICS', 85.00, 40);


-- ===== Task 2: Stored Procedure Transformation & Pricing Aggregations =====
-- Execute ETL Pipeline Stored Procedure
CALL sp_Run_ETL_Pipeline();

SELECT
    CASE WHEN Discount > 0 THEN 'Discounted Order' ELSE 'Full Price Order' END AS Pricing_Category,
    COUNT(OrderID) AS Order_Count,
    SUM(GrossAmount) AS Total_Gross,
    SUM(NetAmount) AS Total_Net,
    ROUND(SUM(GrossAmount - NetAmount), 2) AS Total_Discount_Amount
FROM Fact_Sales
GROUP BY Pricing_Category;

