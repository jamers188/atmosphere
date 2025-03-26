import streamlit as st
import bcrypt
import json
import os
import base64
import random
from datetime import datetime

# ======================== CONFIGURATION ==========================
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# ======================== DATABASE FILES =========================
USER_DB = "users.json"
POSTS_DB = "posts.json"

def ensure_file(filename, default_data):
    """Ensure a file exists with default data."""
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])

# ======================== DATA HANDLING =========================
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def load_posts():
    with open(POSTS_DB, "r") as f:
        return json.load(f)

def save_posts(posts):
    with open(POSTS_DB, "w") as f:
        json.dump(posts, f, indent=4)

# ======================== AUTHENTICATION =========================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ======================== SESSION MANAGEMENT =========================
if "user" not in st.session_state:
    st.session_state["user"] = None

if "images" not in st.session_state:
    st.session_state.images = []

# ======================== NAVIGATION =========================
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home", "Log In", "Sign Up", "Profile", "Explore", "Business Dashboard"])

# ======================== IMAGE UPLOAD FUNCTION =========================
def upload_image(uploaded_file, caption):
    """Encodes and saves an uploaded image to session state."""
    if uploaded_file:
        image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
        posts = load_posts()
        posts.append({
            "user": st.session_state["user"],
            "image_data": image_data,
            "caption": caption,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_posts(posts)
        return True
    return False

# ======================== GENERATE BOT ACTIVITY =========================
def generate_bot_activity():
    bot_users = ["Alice", "Bob", "Charlie", "Diana"]
    activities = ["just posted a photo", "joined a new circle", "commented on a post"]
    return [f"{random.choice(bot_users)} {random.choice(activities)}"]

# ======================== PAGE: HOME =========================
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

# ======================== PAGE: LOGIN =========================
elif page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        users = load_users()
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state["user"] = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password!")

# ======================== PAGE: SIGN UP =========================
elif page == "Sign Up":
    st.title("📝 Create an Account")
    account_type = st.radio("Account Type", ["General User", "Business"])
    new_username = st.text_input("Username")
    email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users = load_users()
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
                save_users(users)
                st.success("Account created! You can now log in.")

# ======================== PAGE: EXPLORE =========================
elif page == "Explore":
    st.title("🌍 Explore Recent Posts")
    st.subheader("📸 Recent Uploads")
    
    posts = load_posts()
    if posts:
        for post in reversed(posts[-5:]):  # Show latest first
            st.write(f"**{post['user']}** uploaded a new photo")
            st.image(base64.b64decode(post['image_data']), caption=post['caption'], use_container_width=True)
    else:
        st.info("No posts yet!")

# ======================== CENTER IMAGE UPLOAD =========================
if st.session_state["user"]:
    st.markdown("### 📸 Upload a New Photo")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], key="image_upload")
    caption = st.text_area("Add a caption", key="caption_upload")
    
    if st.button("Upload", key="upload_button", use_container_width=True):
        if upload_image(uploaded_file, caption):
            st.success("Image uploaded successfully!")
        else:
            st.error("Please upload an image.")
