import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/atmosphere.db", check_same_thread=False)
cursor = conn.cursor()

# Fetch business profiles
def get_business_profiles():
    return pd.read_sql("SELECT business_name, location, description FROM business_profiles", conn)

st.title("🏢 Business Profiles")

businesses = get_business_profiles()
for _, row in businesses.iterrows():
    with st.container():
        st.subheader(row["business_name"])
        st.write(f"📍 Location: {row['location']}")
        st.write(row["description"])
        st.markdown("---")
