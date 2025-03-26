import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/atmosphere.db", check_same_thread=False)
cursor = conn.cursor()

# Fetch analytics
def get_analytics():
    return {
        "profile_views": 1245,
        "engagement": "24%",
        "new_followers": 86,
        "checkins": 124
    }

st.title("📊 Analytics Dashboard")

analytics = get_analytics()

st.metric(label="👀 Profile Views", value=analytics["profile_views"])
st.metric(label="📈 Engagement", value=analytics["engagement"])
st.metric(label="➕ New Followers", value=analytics["new_followers"])
st.metric(label="📍 Check-ins", value=analytics["checkins"])
