import streamlit as st
import bcrypt
import json
import os
import base64
import random
from datetime import datetime

# Initialize session storage for images and posts
if "images" not in st.session_state:
    st.session_state.images = []
if "posts" not in st.session_state:
    st.session_state.posts = []

# File Storage
USER_DB = "users.json"
POSTS_DB = "posts.json"

def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

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

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Ensure storage files exist
ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])

st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "Upload", "Profile", "Explore", "Business Dashboard", "Circles"])

def show_sidebar_updates():
    """Displays recent posts and activities on the sidebar."""
    st.sidebar.subheader("Recent Activity")
    posts = load_posts()
    if posts:
        for post in reversed(posts[-5:]):
            st.sidebar.write(f"**{post['user']}** uploaded:")
            st.sidebar.image(base64.b64decode(post['image']), caption=post['caption'], use_container_width=True)
    else:
        st.sidebar.info("No recent uploads yet!")

if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.write("Explore locations, join circles, and engage with events!")
    show_sidebar_updates()

elif page == "Upload":
    st.title("📸 Upload & Share Your Moments")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    caption = st.text_area("Write a caption")
    if st.button("Upload"):
        if uploaded_file:
            image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            st.session_state.images.append({"name": uploaded_file.name, "data": image_data})
            posts = load_posts()
            posts.append({"user": st.session_state.get("user", "Guest"), "image": image_data, "caption": caption})
            save_posts(posts)
            st.success("Image uploaded successfully!")
        else:
            st.error("Please upload an image.")
    
    show_sidebar_updates()

elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()
        if username in users:
            st.title(f"👤 {username}'s Profile")
            st.write(f"**Account Type:** {users[username]['account_type']}")
            st.write(f"**Followers:** {len(users[username].get('followers', []))}")
            st.write(f"**Following:** {len(users[username].get('following', []))}")
        else:
            st.error("User not found!")
    else:
        st.warning("You need to log in first.")
    show_sidebar_updates()

elif page == "Explore":
    st.title("🌍 Explore Recent Posts")
    posts = load_posts()
    if posts:
        for post in reversed(posts[-10:]):
            st.write(f"**{post['user']}** uploaded a new photo:")
            st.image(base64.b64decode(post['image']), caption=post['caption'], use_container_width=True)
    else:
        st.info("No posts yet!")
    show_sidebar_updates()

elif page == "Business Dashboard":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()
        if users[username]["account_type"] == "Business":
            st.title("📊 Business Dashboard")
            promo_text = st.text_area("Write a Promotion")
            if st.button("Post Promotion"):
                st.success("Promotion posted successfully!")
        else:
            st.error("You must be a business user to access this page.")
    else:
        st.warning("You need to log in first.")
    show_sidebar_updates()

elif page == "Circles":
    st.title("🔵 Circles - Community Groups")
    st.write("Join or create circles to share experiences and engage with like-minded people.")
    circle_name = st.text_input("Create a new Circle")
    if st.button("Create Circle"):
        st.success(f"Circle '{circle_name}' created!")
    show_sidebar_updates()

# Login/Signup system
st.sidebar.subheader("🔑 User Authentication")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_action = st.sidebar.radio("Action", ["Log In", "Sign Up"])

if st.sidebar.button("Proceed"):
    users = load_users()
    if login_action == "Log In":
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state["user"] = username
            st.sidebar.success(f"Welcome back, {username}!")
        else:
            st.sidebar.error("Invalid username or password!")
    elif login_action == "Sign Up":
        account_type = st.sidebar.radio("Account Type", ["General User", "Business"])
        if username in users:
            st.sidebar.error("Username already exists!")
        else:
            users[username] = {"email": "", "password": hash_password(password), "account_type": account_type, "followers": [], "following": []}
            save_users(users)
            st.sidebar.success("Account created! You can now log in.")

if "user" in st.session_state:
    if st.sidebar.button("Log Out"):
        del st.session_state["user"]
        st.sidebar.success("Logged out!")
