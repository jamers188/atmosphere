import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/atmosphere.db", check_same_thread=False)
cursor = conn.cursor()

# Fetch circles
def get_circles():
    return pd.read_sql("SELECT id, name, description FROM circles WHERE is_public = 1", conn)

st.title("🔵 Circles")

circles = get_circles()
for _, row in circles.iterrows():
    with st.container():
        st.subheader(row["name"])
        st.write(row["description"])
        if st.button(f"Join {row['name']}"):
            cursor.execute("INSERT INTO circle_members (circle_id, user_id) VALUES (?, ?)", (row["id"], st.session_state["user_id"]))
            conn.commit()
            st.success(f"Joined {row['name']}!")
        st.markdown("---")
