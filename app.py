import streamlit as st
import bcrypt
import json
import os
import base64
from datetime import datetime

# File paths for data storage
USER_DB = "users.json"
POSTS_DB = "posts.json"
CIRCLES_DB = "circles.json"

def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

# Ensure necessary files exist
ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(CIRCLES_DB, {})

# Load and save functions for persistent storage
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Authentication system
if "user" not in st.session_state:
    st.session_state["user"] = None

# Main Login & Sign-up Page
if st.session_state["user"] is None:
    st.title("🌍 Welcome to Atmosphere")
    choice = st.radio("Select an option", ["Log In", "Sign Up"], horizontal=True)
    
    if choice == "Log In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            users = load_data(USER_DB)
            if username in users and verify_password(password, users[username]["password"]):
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password!")

    elif choice == "Sign Up":
        account_type = st.selectbox("Account Type", ["General User", "Business"])
        new_username = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                users = load_data(USER_DB)
                if new_username in users:
                    st.error("Username already exists!")
                else:
                    users[new_username] = {
                        "email": email,
                        "password": hash_password(new_password),
                        "account_type": account_type,
                        "followers": [],
                        "following": []
                    }
                    save_data(USER_DB, users)
                    st.success("Account created! You can now log in.")
    st.stop()

# Home Page
st.title("🏡 Atmosphere - Social Connect")
page = st.radio("Navigation", ["Home", "Profile", "Explore", "Business Dashboard", "Circles"], horizontal=True)

# Image Upload & Display Feature
st.subheader("📸 Upload & Share Your Moments")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
caption = st.text_area("Write a caption")
if st.button("Upload"):
    if uploaded_file:
        posts = load_data(POSTS_DB)
        image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
        posts.append({"user": st.session_state["user"], "image": image_data, "caption": caption, "likes": 0})
        save_data(POSTS_DB, posts)
        st.success("Image uploaded successfully!")
        st.rerun()

# Explore Page - View & Like Posts
if page == "Explore":
    st.subheader("🌍 Explore Recent Uploads")
    posts = load_data(POSTS_DB)
    if posts:
        for post in reversed(posts):
            st.image(base64.b64decode(post["image"]), caption=post["caption"], use_container_width=True)
            if st.button(f"❤️ Like ({post['likes']})", key=post["caption"]):
                post["likes"] += 1
                save_data(POSTS_DB, posts)
                st.rerun()
    else:
        st.info("No posts yet!")

# Profile Page
if page == "Profile":
    username = st.session_state["user"]
    users = load_data(USER_DB)
    st.subheader(f"👤 {username}'s Profile")
    st.write(f"**Account Type:** {users[username]['account_type']}")
    st.write(f"**Followers:** {len(users[username].get('followers', []))}")
    st.write(f"**Following:** {len(users[username].get('following', []))}")

# Circles Feature
if page == "Circles":
    st.subheader("🔵 Circles - Join & Create Groups")
    circles = load_data(CIRCLES_DB)
    circle_name = st.text_input("Create a new circle")
    if st.button("Create Circle"):
        if circle_name not in circles:
            circles[circle_name] = {"members": [st.session_state["user"]]}
            save_data(CIRCLES_DB, circles)
            st.success(f"Circle '{circle_name}' created!")
            st.rerun()
        else:
            st.error("Circle name already exists!")
    st.subheader("Available Circles")
    for circle, data in circles.items():
        if st.button(f"Join {circle}", key=circle):
            data["members"].append(st.session_state["user"])
            save_data(CIRCLES_DB, circles)
            st.success(f"Joined '{circle}'!")
            st.rerun()

# Business Dashboard
if page == "Business Dashboard":
    username = st.session_state["user"]
    users = load_data(USER_DB)
    if users[username]["account_type"] == "Business":
        st.subheader("📊 Business Promotions")
        promo_text = st.text_area("Write a Promotion")
        if st.button("Post Promotion"):
            st.success("Promotion posted successfully!")
    else:
        st.error("You must be a business user to access this page.")

# Logout
if st.button("Log Out"):
    st.session_state["user"] = None
    st.rerun()

