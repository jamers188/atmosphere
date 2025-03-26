import streamlit as st
import bcrypt
import json
import os
import random
from datetime import datetime
import pandas as pd

# File to store users and posts
USER_DB = "users.json"
POSTS_DB = "posts.json"

def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])

# Load users and posts
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def load_posts():
    with open(POSTS_DB, "r") as f:
        return json.load(f)

def save_posts(posts):
    with open(POSTS_DB, "w") as f:
        json.dump(posts, f)

# Hashing password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# App UI
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "Log In", "Sign Up", "Profile", "Explore", "Business Dashboard"])

# Simulated bot users
def generate_bot_activity():
    bot_users = ["Alice", "Bob", "Charlie", "Diana"]
    activities = ["just posted a photo", "joined a new circle", "commented on a post"]
    return [f"{random.choice(bot_users)} {random.choice(activities)}"]

# Home Page
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.write("Explore locations, join circles, and engage with events!")
    st.subheader("📢 Latest Updates")
    for update in generate_bot_activity():
        st.info(update)
    
    st.subheader("🌍 Ongoing Events")
    events = ["Live Music Night", "Bike Marathon", "Food Festival", "Tech Meetup"]
    for event in events:
        st.write(f"- {event}")

# Log In Page
elif page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")
    
    if login_btn:
        users = load_users()
        if username in users and verify_password(password, users[username]["password"]):
            st.success(f"Welcome back, {username}!")
            st.session_state["user"] = username
        else:
            st.error("Invalid username or password!")

# Sign Up Page
elif page == "Sign Up":
    st.title("📝 Create an Account")
    account_type = st.radio("Account Type", ["General User", "Business"])
    full_name = st.text_input("Full Name")
    new_username = st.text_input("Username")
    email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    signup_btn = st.button("Sign Up")
    
    if signup_btn:
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users = load_users()
            if new_username in users:
                st.error("Username already exists!")
            else:
                users[new_username] = {
                    "full_name": full_name,
                    "email": email,
                    "password": hash_password(new_password),
                    "account_type": account_type,
                    "followers": [],
                    "following": []
                }
                save_users(users)
                st.success("Account created! You can now log in.")

# Profile Page
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()
        st.title(f"👤 {username}'s Profile")
        st.write(f"**Account Type:** {users[username]['account_type']}")
        st.write(f"**Followers:** {len(users[username]['followers'])}")
        st.write(f"**Following:** {len(users[username]['following'])}")
    else:
        st.warning("You need to log in first.")

# Explore Page
elif page == "Explore":
    st.title("🌍 Explore Circles, Events, and Promotions")
    st.subheader("📸 Recent Uploads")
    posts = load_posts()
    if posts:
        for post in posts[-5:]:
            st.write(f"**{post['user']}** uploaded a new photo")
            st.image(post['image_url'], use_container_width=True)
            st.write(post['caption'])
    else:
        st.info("No posts yet!")

    st.subheader("📌 Popular Circles")
    st.write("Coffee Lovers, Biking Club, Grand Hotel Guests")

# Business Dashboard (for Business Users Only)
elif page == "Business Dashboard":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()
        if users[username]["account_type"] == "Business":
            st.title("📊 Business Dashboard")
            st.write("Manage promotions and engage with customers.")
            promo_text = st.text_area("Write a Promotion")
            if st.button("Post Promotion"):
                st.success("Promotion posted successfully!")
        else:
            st.error("You must be a business user to access this page.")
    else:
        st.warning("You need to log in first.")

# Upload Image Feature
st.sidebar.subheader("📸 Upload a Photo")
if "user" in st.session_state:
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    caption = st.sidebar.text_area("Add a caption")
    if st.sidebar.button("Upload"):
        if uploaded_file:
            posts = load_posts()
            posts.append({"user": st.session_state["user"], "image_url": "https://via.placeholder.com/300", "caption": caption})
            save_posts(posts)
            st.sidebar.success("Image uploaded!")
        else:
            st.sidebar.error("Please upload an image.")
