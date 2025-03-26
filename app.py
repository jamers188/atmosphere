import streamlit as st
import bcrypt
import json
import os
import base64
from datetime import datetime

# File to store users and posts
USER_DB = "users.json"
POSTS_DB = "posts.json"
CIRCLES_DB = "circles.json"

# Ensure data files exist
for file, default in [(USER_DB, {}), (POSTS_DB, []), (CIRCLES_DB, {})]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)

# Load and save functions
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
page = st.sidebar.radio("Navigation", ["Home", "Profile", "Explore", "Circles", "Business Dashboard"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- Home Page ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.write("Share moments, connect with circles, and explore content!")
    
    # Upload an Image
    st.subheader("📸 Upload an Image")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    caption = st.text_area("Add a caption")
    
    if st.button("Upload"):
        if uploaded_file and st.session_state.user:
            posts = load_data(POSTS_DB)
            image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            posts.append({"user": st.session_state.user, "image": image_data, "caption": caption, "likes": 0, "comments": []})
            save_data(POSTS_DB, posts)
            st.success("Image uploaded successfully!")
        else:
            st.error("Please log in to upload an image!")

# --- Profile Page ---
elif page == "Profile":
    if st.session_state.user:
        st.title(f"👤 {st.session_state.user}'s Profile")
        users = load_data(USER_DB)
        user_data = users.get(st.session_state.user, {})
        st.write(f"**Email:** {user_data.get('email', 'N/A')}")
        st.write(f"**Account Type:** {user_data.get('account_type', 'General')}")

        st.subheader("📸 Your Posts")
        posts = [p for p in load_data(POSTS_DB) if p['user'] == st.session_state.user]
        if posts:
            for post in posts:
                st.image(base64.b64decode(post['image']), caption=post['caption'], use_container_width=True)
                st.write(f"❤️ {post['likes']} Likes")
        else:
            st.write("No posts yet.")
    else:
        st.warning("You need to log in first.")

# --- Explore Page ---
elif page == "Explore":
    st.title("🌍 Explore Recent Posts")
    posts = load_data(POSTS_DB)
    if posts:
        for post in reversed(posts[-10:]):  # Show last 10 posts
            st.write(f"**{post['user']}** posted:")
            st.image(base64.b64decode(post['image']), caption=post['caption'], use_container_width=True)
            st.write(f"❤️ {post['likes']} Likes")
            if st.button(f"Like {post['caption']}"):
                post['likes'] += 1
                save_data(POSTS_DB, posts)
                st.rerun()
    else:
        st.info("No posts yet!")

# --- Circles Page ---
elif page == "Circles":
    st.title("👥 Circles")
    circles = load_data(CIRCLES_DB)
    
    if st.session_state.user:
        st.subheader("Create a Circle")
        circle_name = st.text_input("Circle Name")
        if st.button("Create"):
            if circle_name not in circles:
                circles[circle_name] = {"members": [st.session_state.user]}
                save_data(CIRCLES_DB, circles)
                st.success(f"Circle '{circle_name}' created!")
            else:
                st.error("Circle already exists!")
        
        st.subheader("Join a Circle")
        for circle in circles:
            if st.button(f"Join {circle}"):
                if st.session_state.user not in circles[circle]["members"]:
                    circles[circle]["members"].append(st.session_state.user)
                    save_data(CIRCLES_DB, circles)
                    st.success(f"Joined '{circle}'!")
                else:
                    st.warning("Already a member!")
    else:
        st.warning("Log in to create or join circles.")

# --- Business Dashboard ---
elif page == "Business Dashboard":
    if st.session_state.user:
        users = load_data(USER_DB)
        if users.get(st.session_state.user, {}).get("account_type") == "Business":
            st.title("📊 Business Dashboard")
            promo_text = st.text_area("Write a Promotion")
            if st.button("Post Promotion"):
                st.success("Promotion posted successfully!")
        else:
            st.error("You must be a business user to access this page.")
    else:
        st.warning("You need to log in first.")

# --- Log In / Sign Up ---
if not st.session_state.user:
    st.sidebar.subheader("🔑 Log In / Sign Up")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    users = load_data(USER_DB)
    if st.sidebar.button("Log In"):
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state.user = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials!")
    
    st.sidebar.subheader("📝 Sign Up")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Sign Up"):
        if new_username in users:
            st.error("Username already exists!")
        else:
            users[new_username] = {"password": hash_password(new_password), "account_type": "General"}
            save_data(USER_DB, users)
            st.success("Account created! Log in now.")

