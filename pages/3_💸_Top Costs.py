import streamlit as st
import pandas as pd

st.set_page_config(page_title="Top Costs", page_icon="💸")

# Load the dataset
@st.cache_data
def load_data():
    """Load and preprocess the dataset."""
    try:
        file_path = "fortune_500_hq.csv"
        data = pd.read_csv(file_path, encoding="utf-8")
        return data
    except FileNotFoundError:
        st.error("The data file was not found.")
        return pd.DataFrame()

# Clean the data
def clean_data(data):
    """Clean the data by dropping missing values."""
    return data.dropna(subset=['REVENUES', 'PROFIT'])

# Calculate Costs
def calculate_cost(data):
    """Calculate cost as REVENUES - PROFIT."""
    data['COST'] = data['REVENUES'] - data['PROFIT']
    return data

# Highlight the cost column
def highlight_cost(row):
    """Highlight the COST column."""
    return ['background-color: #ffcccb' if col == 'COST' else '' for col in row.index]

# Load and preprocess the data
df = load_data()
df = clean_data(df)
df = calculate_cost(df)

# Page Title
st.title("💸 Top Costs in Fortune 500 Companies")
st.write("This page displays the calculated costs for Fortune 500 companies, derived from their revenue and profit.")
st.write("(in millions, $)")

# Display Costs Table [VIZ3]
st.subheader("Companies Sorted by Cost (Highest to Lowest)")
sorted_cost_df = df.sort_values(by="COST", ascending=False)

# Apply Styler to highlight the COST column
styled_table = sorted_cost_df[['NAME', 'REVENUES', 'PROFIT', 'COST']].style.apply(
    highlight_cost, axis=1
).format({
    'REVENUES': '${:,.2f}',
    'PROFIT': '${:,.2f}',
    'COST': '${:,.2f}'
})

st.write(styled_table.to_html(), unsafe_allow_html=True)

# Display Total Cost
total_cost = sorted_cost_df['COST'].sum() #[DA9]
st.write(f"### 💰 Total Cost Across All Companies: ${total_cost:,.2f}")
