import streamlit as st
import bcrypt
import json
import os
import base64

# Page Config
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Database Files
USER_DB = "users.json"
POSTS_DB = "posts.json"
EVENTS_DB = "events.json"

# Ensure database files exist
def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(EVENTS_DB, [
    {"title": "Tech Meetup", "date": "April 15, 2025", "location": "Downtown Hall"},
    {"title": "Live Music Night", "date": "March 30, 2025", "location": "City Square"},
    {"title": "Startup Pitching Event", "date": "April 22, 2025", "location": "Tech Park"},
])

# Load & Save Data
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Password Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/150", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Profile", "Upload Media", "Explore", "Upcoming Events", "Log In", "Sign Up"])

# --- Home Page ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("🌍 Connect, Share & Discover!")
    
    # Display recent uploads
    st.subheader("📸 Recent Uploads")
    posts = load_data(POSTS_DB)
    
    if posts:
        for post in reversed(posts[-5:]):  # Show last 5 uploads
            st.write(f"**{post['user']}** uploaded:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))
    else:
        st.info("No uploads yet!")

# --- Profile Page ---
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_data(USER_DB)
        
        st.title(f"👤 {username}'s Profile")
        st.write(f"**Account Type:** {users[username]['account_type']}")

        # Display user uploads
        st.subheader("📸 Your Uploads")
        posts = load_data(POSTS_DB)
        user_posts = [post for post in posts if post["user"] == username]
        
        if user_posts:
            for post in reversed(user_posts):
                st.write(f"**{username}** posted:")
                if post.get("image"):
                    st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
                else:
                    st.write(post.get("caption", "No caption."))
        else:
            st.info("You haven't uploaded anything yet.")
    else:
        st.warning("You need to log in first.")

# --- Upload Media Page ---
elif page == "Upload Media":
    if "user" in st.session_state:
        st.title("📸 Upload Your Moments")
        
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        caption = st.text_area("Write a caption")

        if st.button("Upload"):
            if uploaded_file:
                image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                posts = load_data(POSTS_DB)
                posts.append({"user": st.session_state["user"], "image": image_data, "caption": caption})
                save_data(POSTS_DB, posts)
                st.success("Image uploaded successfully!")
                st.experimental_rerun()
            else:
                st.error("Please upload an image.")
    else:
        st.warning("You need to log in first.")

# --- Explore Page ---
elif page == "Explore":
    st.title("🔍 Explore Community Uploads")
    posts = load_data(POSTS_DB)

    if posts:
        for post in reversed(posts):
            st.write(f"**{post['user']}** uploaded:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))
    else:
        st.info("No posts yet!")

# --- Upcoming Events Page ---
elif page == "Upcoming Events":
    st.title("🎉 Upcoming Events")
    events = load_data(EVENTS_DB)

    for event in events:
        st.subheader(event["title"])
        st.write(f"📅 Date: {event['date']}")
        st.write(f"📍 Location: {event['location']}")
        st.markdown("---")

# --- Log In Page ---
elif page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        users = load_data(USER_DB)
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state["user"] = username
            st.success(f"Welcome back, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

# --- Sign Up Page ---
elif page == "Sign Up":
    st.title("🆕 Create an Account")
    account_type = st.radio("Account Type", ["General User", "Business"])
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
                }
                save_data(USER_DB, users)
                st.success("Account created! You can now log in.")

# Logout Button
if "user" in st.session_state:
    if st.sidebar.button("Log Out"):
        del st.session_state["user"]
        st.experimental_rerun()

