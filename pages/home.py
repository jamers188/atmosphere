import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/atmosphere.db", check_same_thread=False)
cursor = conn.cursor()

# Fetch posts from DB
def get_posts():
    query = "SELECT posts.caption, posts.media_url, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC"
    df = pd.read_sql(query, conn)
    return df

# Streamlit UI
st.title("🌍 Atmosphere Feed")

# Fetch posts
posts = get_posts()

# Display posts as cards
for index, row in posts.iterrows():
    with st.container():
        st.write(f"**{row['username']}**")
        st.image(row['media_url'], use_column_width=True)
        st.write(row['caption'])
        st.markdown("---")
