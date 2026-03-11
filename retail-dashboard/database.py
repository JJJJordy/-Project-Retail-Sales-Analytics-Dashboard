import pandas as pd
import sqlite3

# --- LOAD CLEANED DATASET ---
df = pd.read_csv("Superstore_clean.csv")

# --- CREATE SQLITE DATABASE ---
conn = sqlite3.connect("superstore.db")

# Load the dataframe into a SQL table called "orders"
df.to_sql("orders", conn, if_exists="replace", index=False)
print("Data loaded into superstore.db")


# --- SQL QUERIES ---

# Query 1: Total sales, Profit and Orders by Year
print("\n=== Total Sales & Profit by Year ===")
q1 = pd.read_sql_query("""
    SELECT 
        "Order Year",
        COUNT(DISTINCT "Order ID") AS total_orders,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(AVG("Profit Margin %"), 2) AS avg_margin
    FROM orders
    GROUP BY "Order Year"
    ORDER BY "Order Year"
""", conn)
print(q1)

# Query 2: Sales & Profit by Category
print("\n=== Sales & Profit by Category ===")
q2 = pd.read_sql_query("""
    SELECT 
        Category,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(AVG("Profit Margin %"), 2) AS avg_margin,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY Category
    ORDER BY total_sales DESC
""", conn)
print(q2)

# Query 3: Sales & Profit by Region
print("\n=== Sales & Profit by Region ===")
q3 = pd.read_sql_query("""
    SELECT 
        Region,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(AVG("Profit Margin %"), 2) AS avg_margin
    FROM orders
    GROUP BY Region
    ORDER BY total_profit DESC
""", conn)
print(q3)

# Query 4: Top 10 Most Profitable Products
print("\n=== Top 10 Most Profitable Products ===")
q4 = pd.read_sql_query("""
    SELECT 
        "Product Name",
        Category,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit
    FROM orders
    GROUP BY "Product Name", Category
    ORDER BY total_profit DESC
    LIMIT 10
""", conn)
print(q4)

# Query 5: Top 10 Worst Performing Products (Biggest Losses)
print("\n=== Top 10 Loss-Making Products ===")
q5 = pd.read_sql_query("""
    SELECT 
        "Product Name",
        Category,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit
    FROM orders
    GROUP BY "Product Name", Category
    ORDER BY total_profit ASC
    LIMIT 10
""", conn)
print(q5)

# Query 6: Monthly Sales Trend
print("\n=== Monthly Sales Trend ===")
q6 = pd.read_sql_query("""
    SELECT 
        "Order Year",
        "Order Month",
        "Order Month Name",
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit
    FROM orders
    GROUP BY "Order Year", "Order Month", "Order Month Name"
    ORDER BY "Order Year", "Order Month"
""", conn)
print(q6)

# Query 7: Customer Segment Performance
print("\n=== Performance by Customer Segment ===")
q7 = pd.read_sql_query("""
    SELECT 
        Segment,
        COUNT(DISTINCT "Customer ID") AS unique_customers,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(AVG(Sales), 2) AS avg_order_value
    FROM orders
    GROUP BY Segment
    ORDER BY total_sales DESC
""", conn)
print(q7)

conn.close()
print("\n✅ All queries ran successfully!")