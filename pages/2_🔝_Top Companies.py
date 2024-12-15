import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Top Companies", page_icon="🔝")

# Load the dataset [PY3]
@st.cache_data
def load_data(): #[PY3] Error checking with try/except
    """Load and preprocess the dataset."""
    try:
        file_path = "fortune_500_hq.csv"
        data = pd.read_csv(file_path, encoding="utf-8")
        return data
    except FileNotFoundError:
        st.error("The data file was not found.")
        return pd.DataFrame()


# [DA1] Clean the data
def clean_data(data):
    """Clean the data by dropping missing values."""
    data = data.dropna()
    return data

# [PY1] Function with default parameter
def format_currency(value, currency="$"):
    return f"{currency}{value:,.2f}"

# [PY2] A function that returns more than one value
def calculate_statistics(data):
    """Calculate total companies and unique states."""
    total_companies = len(data)
    unique_states = data['STATE'].nunique()
    return total_companies, unique_states

# Load and preprocess the data
df = load_data()
df = clean_data(df)

# Sidebar Navigation
#[ST1-1] A radio button to select a view
st.sidebar.title("Top Companies")
view_option = st.sidebar.radio("Select a View", ["By Revenue", "By State", "By Profit"])

# By Revenue View
if view_option == "By Revenue":
    st.markdown("# 🔝 Top 10 Companies by Revenue")
    st.write("Displaying the top 10 companies based on their revenue.")

    # Find top 10 companies by revenue [DA3]
    top_companies = df.nlargest(10, 'REVENUES')

    # Plot the bar chart [VIZ1]
    plt.figure(figsize=(10, 6))
    plt.barh(top_companies['NAME'], top_companies['REVENUES'], color='skyblue')
    plt.xlabel("Revenue (in millions,$)")
    plt.ylabel("Company Name")
    plt.title("Top 10 Companies by Revenue")
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest value on top
    st.pyplot(plt.gcf())

# By State View
elif view_option == "By State":
    st.markdown("# 📊 Companies by State")
    st.write("Top 10 states with the most Fortune 500 companies:")

    # State Summary
    #[PY5] A dictionary where you write code to access its keys, values, or items
    state_summary = df['STATE'].value_counts()

    # Separate top 10 states and group others as "Other States" [DA3]
    top_10_states = state_summary.nlargest(10)
    other_states = state_summary.iloc[10:].sum()

    # Combine top 10 with "Other States"
    labels = list(top_10_states.index) + ["Other States"]
    sizes = list(top_10_states.values) + [other_states]

    # Generate the pie chart
    #[VIZ2] A pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.tab20.colors[:len(labels)],
        textprops={'fontsize': 8}
    )
    ax.set_title("Distribution of Companies by State (Top 10 and Others)", fontsize=10)
    st.pyplot(fig)

    # Display raw state summary data
    st.write("Top 10 States:")
    top_10_states_df = top_10_states.reset_index()
    top_10_states_df.columns = ['State', 'Number of Companies']
    st.write(top_10_states_df)
    st.write("Other States Total:", other_states)

# By Profit View
elif view_option == "By Profit":
    st.markdown("# 💰 Top 10 Companies by Profit")
    st.write("Displaying the top 10 companies based on their profit.")

    # Find top 10 companies by profit [DA3]
    top_profit_companies = df.nlargest(10, 'PROFIT')

    # Plot the bar chart [VIZ1]
    plt.figure(figsize=(10, 6))
    plt.barh(top_profit_companies['NAME'], top_profit_companies['PROFIT'], color='lightgreen')
    plt.xlabel("Profit (in millions,$)")
    plt.ylabel("Company Name")
    plt.title("Top 10 Companies by Profit")
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest value on top
    st.pyplot(plt.gcf())

    # Display the raw profit data
    st.write("Top 10 Companies by Profit:")
    st.dataframe(top_profit_companies[['NAME', 'PROFIT']])