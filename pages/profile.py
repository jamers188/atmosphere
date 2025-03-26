import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/atmosphere.db", check_same_thread=False)
cursor = conn.cursor()

# Fetch user details
def get_user(user_id):
    query = "SELECT username, full_name, avatar_url, location FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

# Fetch user's posts
def get_user_posts(user_id):
    query = "SELECT caption, media_url FROM posts WHERE user_id = ? ORDER BY created_at DESC"
    return pd.read_sql(query, conn, params=(user_id,))

# Get user session info
if "user_id" not in st.session_state:
    st.error("Please log in first.")
    st.stop()

user_id = st.session_state["user_id"]
user = get_user(user_id)

if user:
    st.title(f"👤 {user[1]}'s Profile")
    st.image(user[2], width=100)
    st.write(f"📍 Location: {user[3]}")

    # Fetch and show user posts
    user_posts = get_user_posts(user_id)
    st.subheader("📸 Your Posts")
    for _, row in user_posts.iterrows():
        with st.container():
            st.image(row["media_url"], use_column_width=True)
            st.write(row["caption"])
            st.markdown("---")
else:
    st.error("User not found.")
