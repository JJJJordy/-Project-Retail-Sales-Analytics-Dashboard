import pandas as pd

# --- LOAD ---
df = pd.read_csv('Sample - Superstore.csv', encoding='latin-1')

# --- CLEAN ---

# Fix 1: Convert dates from text to proper datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Fix 2: Postal Code should be a string, not a number
df['Postal Code'] = df['Postal Code'].astype(str)

# --- ENGINEER NEW COLUMNS ---

# Days it took to ship each order
df['Days to Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

# Extract year and month from Order Date (useful for trend charts)
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%b')  # e.g. "Jan"

# Profit Margin % per order
df['Profit Margin %'] = ((df['Profit'] / df['Sales']) * 100).round(2)

# --- VERIFY ---
print("=== Cleaned Data Types ===")
print(df.dtypes)

print("\n=== New Columns Preview ===")
print(df[['Order Date', 'Days to Ship', 'Order Year', 'Order Month', 'Profit Margin %']].head(10))

print("\n=== Unique Years in Dataset ===")
print(sorted(df['Order Year'].unique()))

print("\n=== Unique Categories ===")
print(df['Category'].unique())

print("\n=== Unique Regions ===")
print(df['Region'].unique())

print("\n=== Orders with Negative Profit (Losses) ===")
losses = df[df['Profit'] < 0]
print(f"{len(losses)} orders are operating at a loss ({round(len(losses)/len(df)*100, 1)}% of all orders)")

# --- SAVE CLEANED FILE ---
df.to_csv("Superstore_clean.csv", index=False)
print("\n Cleaned file was saved as superstore_clean.csv")
