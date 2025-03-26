import streamlit as st
import bcrypt
import json
import os
import base64

# Set up page layout
st.set_page_config(page_title="Atmosphere - Social Connect", page_icon="🏡", layout="wide")

# Database files
USER_DB = "users.json"
POSTS_DB = "posts.json"

# Ensure database files exist
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

# Password hashing and verification
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Sidebar updates
def show_sidebar_updates():
    st.sidebar.subheader("📢 Latest Updates")
    posts = load_posts()

    if posts:
        for post in reversed(posts[-5:]):  # Show last 5 posts (latest first)
            user = post.get("user", "Unknown User")
            caption = post.get("caption", "No caption provided.")
            image_data = post.get("image")

            if image_data:
                try:
                    st.sidebar.image(base64.b64decode(image_data), caption=f"📸 {user}: {caption}", use_container_width=True)
                except Exception:
                    st.sidebar.warning(f"⚠️ Error loading image for {user}")
            else:
                st.sidebar.write(f"**{user}**: {caption}")
    else:
        st.sidebar.info("No updates yet!")

# Navigation Menu
st.title("🏡 Atmosphere - Social Connect")
page = st.radio("Navigation", ["Home", "Log In / Sign Up", "Profile", "Explore", "Business Dashboard", "Circles", "Upload"])

# Home Page
if page == "Home":
    st.subheader("🌍 Welcome to Atmosphere")
    st.write("Explore locations, join circles, and engage with events!")
    show_sidebar_updates()

# Log In / Sign Up Page
elif page == "Log In / Sign Up":
    st.subheader("🔑 Log In or Sign Up")
    choice = st.radio("Choose an option", ["Log In", "Sign Up"])

    if choice == "Log In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            users = load_users()
            if username in users and verify_password(password, users[username]["password"]):
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password!")

    elif choice == "Sign Up":
        account_type = st.radio("Account Type", ["General User", "Business"])
        new_username = st.text_input("Choose a Username")
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

# Profile Page (Show user's own posts)
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()

        if username in users:
            user_data = users[username]
            st.subheader(f"👤 {username}'s Profile")
            st.write(f"**Account Type:** {user_data['account_type']}")
            st.write(f"**Followers:** {len(user_data.get('followers', []))}")
            st.write(f"**Following:** {len(user_data.get('following', []))}")

            st.subheader("📸 Your Posts")
            posts = load_posts()
            user_posts = [post for post in posts if post["user"] == username]

            if user_posts:
                for post in reversed(user_posts):
                    st.write(f"**{username}** posted:")
                    if post.get("image"):
                        st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
                    else:
                        st.write(post.get("caption", "No caption."))
            else:
                st.info("You haven't posted anything yet.")
        else:
            st.error("User not found!")
    else:
        st.warning("You need to log in first.")

# Explore Page (View Recent Uploads)
elif page == "Explore":
    st.subheader("📸 Explore Recent Uploads")
    posts = load_posts()

    if posts:
        for post in reversed(posts):  # Show latest first
            st.write(f"**{post['user']}** uploaded a new photo:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))
    else:
        st.info("No posts yet!")

# Business Dashboard
elif page == "Business Dashboard":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_users()

        if users[username]["account_type"] == "Business":
            st.subheader("📊 Business Dashboard")
            promo_text = st.text_area("Write a Promotion")

            if st.button("Post Promotion"):
                posts = load_posts()
                posts.append({"user": username, "caption": promo_text, "image": None})
                save_posts(posts)
                st.success("Promotion posted successfully!")
                st.experimental_rerun()
        else:
            st.error("You must be a business user to access this page.")
    else:
        st.warning("You need to log in first.")

# Circles (Creating & Joining)
elif page == "Circles":
    st.subheader("🌐 Join or Create Circles")
    st.write("Connect with communities and join interest-based circles.")
    circles = ["Tech Enthusiasts", "Travel Lovers", "Foodies", "Fitness Gurus"]

    for circle in circles:
        if st.button(f"Join {circle}"):
            st.success(f"You joined {circle}!")

# Upload Page (Image Uploading)
elif page == "Upload":
    if "user" in st.session_state:
        st.subheader("📸 Upload & Share Your Moments")

        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        caption = st.text_area("Write a caption")

        if st.button("Upload"):
            if uploaded_file:
                image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                posts = load_posts()
                posts.append({"user": st.session_state["user"], "image": image_data, "caption": caption})
                save_posts(posts)
                st.success("Image uploaded successfully!")
                st.experimental_rerun()
            else:
                st.error("Please upload an image.")
    else:
        st.warning("You need to log in first.")

# Logout Button
if "user" in st.session_state:
    if st.button("Log Out"):
        del st.session_state["user"]
        st.experimental_rerun()


