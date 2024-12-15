import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="Mapping", page_icon="🌍")

# Load the dataset
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

st.markdown("# 🌍Mapping of Fortune 500")
st.sidebar.header("Mapping of Fortune 500")

st.subheader("Geographic Distribution of Headquarters")
st.write("Visualizing the locations of Fortune 500 company headquarters.")

# Filters [DA4], [DA5]
# Checkbox to select all states [ST1]
all_states = st.checkbox("Select All States", value=True)
if all_states:
    filtered_df = df
else: #[ST2] Multiselect
    selected_states = st.multiselect("Select State(s)", df['STATE'].unique())
    filtered_df = df[df['STATE'].isin(selected_states)]
# [ST3] Slider
revenue_filter = st.slider(
    "Select Revenue Range (in millions, $)",
    float(df['REVENUES'].min()),
    float(df['REVENUES'].max()),
    (float(df['REVENUES'].min()), float(df['REVENUES'].max()))
)
filtered_df = filtered_df[
    (filtered_df['REVENUES'] >= revenue_filter[0]) &
    (filtered_df['REVENUES'] <= revenue_filter[1])
    ]

# [MAP] Detailed map with interactivity
st.subheader("Interactive Map")
# Map center
if len(filtered_df) > 0:
    initial_lat = filtered_df['LATITUDE'].mean()
    initial_lon = filtered_df['LONGITUDE'].mean()
else:
    initial_lat, initial_lon = 37.7749, -122.4194  # Default to San Francisco

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=initial_lat,
        longitude=initial_lon,
        zoom=4,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position=["LONGITUDE", "LATITUDE"],
            get_radius=15000,
            get_color=[255, 140, 0],
            pickable=True,
        ),
    ],
))

# Display filtered summary [DA2], [PY5]
total_companies, unique_states = calculate_statistics(filtered_df)
st.write(f"Total Companies: {total_companies}")
st.write(f"Unique States: {unique_states}")


