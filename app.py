import streamlit as st
import bcrypt
import json
import os
import datetime

# Database Files
USER_DB = "users.json"
POST_DB = "posts.json"

# Ensure database files exist
for db in [USER_DB, POST_DB]:
    if not os.path.exists(db):
        with open(db, "w") as f:
            json.dump({}, f)

# Load users from file
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Load posts from file
def load_posts():
    with open(POST_DB, "r") as f:
        return json.load(f)

# Save posts to file
def save_posts(posts):
    with open(POST_DB, "w") as f:
        json.dump(posts, f)

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Set up Streamlit app
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "Log In", "Sign Up", "Your Circles", "Create Post", "Search"])  

# Authentication session
if "user" not in st.session_state:
    st.session_state["user"] = None

# **Log In Page**
if page == "Log In":
    st.title("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        users = load_users()
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state["user"] = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password!")

# **Sign Up Page**
elif page == "Sign Up":
    st.title("Create an Account")
    account_type = st.radio("Account Type", ["General User", "Business"])
    full_name = st.text_input("Full Name")
    new_username = st.text_input("Username")
    email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    signup_btn = st.button("Create Account")

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
                    "account_type": account_type
                }
                save_users(users)
                st.success("Account created! You can now log in.")

# **Create Post Page**
elif page == "Create Post":
    if st.session_state["user"]:
        st.title("Create a Post")
        caption = st.text_area("Caption")
        image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        post_btn = st.button("Post")

        if post_btn and image:
            posts = load_posts()
            timestamp = str(datetime.datetime.now())
            posts[timestamp] = {
                "username": st.session_state["user"],
                "caption": caption,
                "image": image.name
            }
            save_posts(posts)
            st.success("Post uploaded successfully!")
    else:
        st.warning("Please log in to create a post.")

# **Home Page with Feed**
elif page == "Home":
    st.title("📸 Atmosphere Feed")
    posts = load_posts()

    if posts:
        for timestamp, post in reversed(posts.items()):
            st.write(f"**{post['username']}**")
            st.write(post["caption"])
            st.image(post["image"], use_container_width=True)
            st.write(f"_Posted on {timestamp}_")
            st.markdown("---")
    else:
        st.info("No posts available. Create your first post!")

# **Search Page**
elif page == "Search":
    st.title("🔍 Search Circles, Events & Businesses")
    query = st.text_input("Search...")
    results = []  # This should fetch data from a proper source
    
    if query:
        st.write("### Results:")
        for result in results:
            st.write(result)
