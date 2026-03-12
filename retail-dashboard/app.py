import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)


# --- LOAD DATA ---
@st.cache_data
def load_data():
    conn = sqlite3.connect("Superstore.db")

    orders = pd.read_sql_query("SELECT * FROM orders", conn)
    
    sales_by_year = pd.read_sql_query("""
        SELECT
            "Order Year",
            COUNT(DISTINCT "Order ID") AS total_orders,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
                                      ROUND(AVG("Profit Margin %), 2) AS avg_margin
        FROM orders
        GROUP BY "Order Year"
        ORDER BY "Order Year"
    """, conn)

    sales_by_category = pd.read_sql_query("""
        SELECT
            Category,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            ROUND(AVG("Profit Margin %), 2) AS avg_margin,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY Category
        ORDER BY total_sales DESC
    """, conn)

    sales_by_region = pd.read_sql_query("""
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

    top_products = pd.read_sql_query("""
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

    loss_products = pd.read_sql_query("""
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

    monthly_trend = pd.read_sql_query("""
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

    segments = pd.read_sql_query("""
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

    conn.close()
    return orders, sales_by_year, sales_by_category, sales_by_region, top_products, loss_products, monthly_trend, segments

orders, sales_by_year, sales_by_category, sales_by_region, top_products, loss_products, monthly_trend, segments = load_data()


# --- SIDEBAR FILTERS ---
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-cart/png", width=60)
st.sidebar.title("Filters")

selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=sorted(orders["Order Year"].unique()),
    default=sorted(orders["Order Year"].unique())
)

selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=orders["Region"].unique(),
    default=orders["Region"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=orders["Category"].unique(),
    default=orders["Category"].unique()
)

# Filter the main roders dataframe
filtered_df = orders[
    (orders["Order Year"].isin(selected_years)) &
    (orders["Region"].isin(selected_regions)) &
    (orders["Category"].isin(selected_categories))
]

# --- HEADER ---
st.title("🛒 Retail Sales Analytics Dashboard")
st.markdown("An interactive analysis of sales performance, profitability, and customer trends.")
st.markdown("---")

# --- KPI CARDS ---
k1, k2, k3, k4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_margin = filtered_df["Profit Margin %"].mean()

k1.metric("💰 Total Sales", f"${total_sales:,.0f}")
k2.metric("📈 Total Profit", f"${total_profit:,.0f}")
k3.metric("🧾 Total Orders", f"{total_orders:,}")
k4.metric("📊 Avg Profit Margin", f"{avg_margin:.1f}%")

st.markdown("---")

# --- ROW 1: YEARLY TREND + CATEGORY BREAKDOWN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales & Profit by Year")
    filtered_yearly = filtered_df.groupby("Order Year").agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum")
    ).reset_index()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=filtered_yearly["Order Year"],
        y=filtered_yearly["total_sales"],
        name="Sales",
        marker_color="#4C78A8"
    ))
    fig1.add_trace(go.Bar(
        x=filtered_yearly["Order Year"],
        y=filtered_yearly["total_profit"],
        name="Profit",
        marker_color="#72B7B2"
    ))
    fig1.update_layout(barmode="group", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Sales by Category")
    filtered_category = filtered_df.groupby("Category").agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum")
    ).reset_index()

    fig2 = px.pie(
        filtered_category,
        values="total_sales",
        names="category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# --- ROW 2: MONTHLY TREND ---