import streamlit as st
import bcrypt
import json
import os
import base64
from datetime import datetime

# File Storage
USER_DB = "users.json"
POSTS_DB = "posts.json"
CIRCLES_DB = "circles.json"

def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(CIRCLES_DB, {})

# Password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

# Login / Signup Page
if st.session_state.user is None:
    st.title("🌍 Welcome to Atmosphere")
    choice = st.radio("", ["Log In", "Sign Up"])
    
    if choice == "Log In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            users = load_data(USER_DB)
            if username in users and verify_password(password, users[username]["password"]):
                st.session_state.user = username
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials!")
    
    elif choice == "Sign Up":
        new_username = st.text_input("Username")
        email = st.text_input("Email")
        account_type = st.radio("Account Type", ["General User", "Business User"])
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
                    st.success("Account created! Log in now.")
else:
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.update(user=None))
    st.title("📸 Atmosphere Feed")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    caption = st.text_area("Add a caption")
    
    if st.button("Post Image") and uploaded_file:
        posts = load_data(POSTS_DB)
        image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
        posts.append({"user": st.session_state.user, "image": image_data, "caption": caption, "likes": []})
        save_data(POSTS_DB, posts)
        st.success("Image uploaded!")
    
    st.subheader("Recent Posts")
    posts = load_data(POSTS_DB)
    if posts:
        for post in reversed(posts):
            st.image(base64.b64decode(post["image"]), caption=post["caption"], use_container_width=True)
            if st.button(f"❤️ Like ({len(post['likes'])})", key=post['caption']):
                if st.session_state.user not in post["likes"]:
                    post["likes"].append(st.session_state.user)
                    save_data(POSTS_DB, posts)
                    st.experimental_rerun()
    
    st.subheader("🌍 Circles")
    circles = load_data(CIRCLES_DB)
    circle_name = st.text_input("Create a New Circle")
    if st.button("Create Circle"):
        if circle_name not in circles:
            circles[circle_name] = {"members": [st.session_state.user]}
            save_data(CIRCLES_DB, circles)
            st.success(f"Created circle: {circle_name}")
    
    st.write("### Join an Existing Circle")
    for circle, data in circles.items():
        if st.session_state.user not in data["members"]:
            if st.button(f"Join {circle}"):
                data["members"].append(st.session_state.user)
                save_data(CIRCLES_DB, circles)
                st.experimental_rerun()
    
    if "Business User" in load_data(USER_DB).get(st.session_state.user, {}).get("account_type", ""):
        st.subheader("📊 Business Dashboard")
        promo_text = st.text_area("Write a Promotion")
        if st.button("Post Promotion"):
            st.success("Promotion posted successfully!")
