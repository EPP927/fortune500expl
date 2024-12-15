import streamlit as st
# Set page configuration [ST4] navigation
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

# Streamlit app title
st.title("Fortune 500 Corporate Headquarters Explorer")
st.write("Created by Linnuo Yi")

# Add pictures [ST4]
st.image("fortune500.jpg", width=700)

# Introduction and home page

st.subheader("Welcome to the Home Page")
st.write("Explore the dataset and uncover insights into the Fortune 500 companies.")
st.write(
    "The Fortune 500 is an annual list compiled and published by Fortune magazine that ranks 500 of the largest United States corporations by total revenue for their respective fiscal years.")
st.write("Use the dropdown on the left 👈 to navigate between features.")
st.write("Data Source: [Fortune 500 Headquarters](https://www.kaggle.com/datasets/mannmann2/fortune-500-corporate-headquarters)")