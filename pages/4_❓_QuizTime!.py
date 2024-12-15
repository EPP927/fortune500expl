import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quiz Time", page_icon="❓")

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


# Load the data
df = load_data()

# Prepare data for the quiz
most_revenue_company = df.nlargest(1, 'REVENUES')['NAME'].iloc[0]
state_summary = df['STATE'].value_counts()
most_companies_state = state_summary.idxmax()

# Quiz Time Page
st.title("🧠 Quiz Time!")
st.write("Test your knowledge about Fortune 500 companies! Answer the following questions:")

# Question 1: Which company has the most revenue?
st.subheader("1. Which company has the highest revenue?")
company_guess = st.text_input("Enter the company name:")#[ST2-1]
if company_guess:
    if company_guess.lower() == most_revenue_company.lower():
        st.success(f"🎉 Correct! {most_revenue_company} has the highest revenue.")
    else:
        st.error(f"❌ Incorrect. The correct answer is {most_revenue_company}.")

# Question 2: Which state has the most Fortune 500 companies?
st.subheader("2. Which state has the most Fortune 500 companies?")
state_guess = st.text_input("Enter the state abbreviation (e.g., CA, NY):")#[ST2-1]
if state_guess:
    if state_guess.upper() == most_companies_state:
        st.success(f"🎉 Correct! {most_companies_state} has the most Fortune 500 companies.")
    else:
        st.error(f"❌ Incorrect. The correct answer is {most_companies_state}.")

# Question 3: Do you want to work in a Fortune 500 company?
st.subheader("3. Do you want to work in a Fortune 500 company?")
work_in_fortune = st.radio("Select your answer:", ["Yes", "No", "Maybe"])#[ST3]
if work_in_fortune:
    if work_in_fortune == "Yes":
        st.write("💼 Great! Working in a Fortune 500 company can be a fantastic experience.")
    elif work_in_fortune == "No":
        st.write("👍 That's perfectly fine. There are many great opportunities outside of Fortune 500 companies!")
    else:
        st.write("🤔 It's good to stay open to possibilities.")

# Conclusion
st.markdown("---")
st.write("Thanks for participating in the quiz! 🎉 Let us know if you want to explore more about Fortune 500 companies.")
