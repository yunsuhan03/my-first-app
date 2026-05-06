import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Global Travel Dashboard", layout="wide")

# ---------------------------
# Title
# ---------------------------
st.title("🌍✈️ Global Travel Planning Dashboard")
st.markdown("Plan your dream trips and manage your travel budget 💰")

# ---------------------------
# Sample Data
# ---------------------------
if "travel_data" not in st.session_state:
    st.session_state.travel_data = pd.DataFrame({
        "Country": ["France", "Japan", "USA", "Indonesia", "Italy"],
        "City": ["Paris", "Tokyo", "New York", "Bali", "Rome"],
        "Date": ["2026-06-10", "2026-07-15", "2026-08-20", "2026-09-05", "2026-10-12"],
        "Budget (₩)": [2500000, 2000000, 3000000, 1800000, 2200000],
        "Theme": ["Romantic", "Food Tour", "City Life", "Relaxation", "History"]
    })

# ---------------------------
# Sidebar Inputs
# ---------------------------
st.sidebar.header("✈️ Add New Destination")

country = st.sidebar.text_input("Country")
city = st.sidebar.text_input("City")
date = st.sidebar.date_input("Travel Date")
budget = st.sidebar.number_input("Budget (₩)", min_value=0)
theme = st.sidebar.selectbox("Travel Theme",
                            ["Relaxation", "Adventure", "Food Tour", "Romantic", "History"])

if st.sidebar.button("➕ Add Destination"):
    new_data = pd.DataFrame({
        "Country": [country],
        "City": [city],
        "Date": [str(date)],
        "Budget (₩)": [budget],
        "Theme": [theme]
    })
    st.session_state.travel_data = pd.concat(
        [st.session_state.travel_data, new_data], ignore_index=True
    )
    st.success(f"{city} added successfully! 🎉")

# ---------------------------
# Main Layout
# ---------------------------
df = st.session_state.travel_data

col1, col2 = st.columns(2)

# Metrics
total_destinations = len(df)
total_budget = df["Budget (₩)"].sum()

col1.metric("🌍 Total Destinations", total_destinations)
col2.metric("💰 Total Budget (₩)", f"{total_budget:,}")

st.divider()

# ---------------------------
# Data Table
# ---------------------------
st.subheader("📋 Travel Plans Overview")
st.dataframe(df, use_container_width=True)

st.divider()

# ---------------------------
# Charts
# ---------------------------
col3, col4 = st.columns(2)

# Bar Chart (Budget per City)
with col3:
    st.subheader("💰 Budget by City")
    fig, ax = plt.subplots()
    ax.bar(df["City"], df["Budget (₩)"])
    ax.set_ylabel("Budget (₩)")
    ax.set_xlabel("City")
    ax.set_title("City Budget Comparison")
    plt.xticks(rotation=30)
    st.pyplot(fig)

# Pie Chart (Theme Distribution)
with col4:
    st.subheader("🎯 Travel Theme Distribution")
    theme_counts = df["Theme"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(theme_counts, labels=theme_counts.index, autopct="%1.1f%%")
    ax2.set_title("Theme Breakdown")
    st.pyplot(fig2)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
