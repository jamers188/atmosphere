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
CIRCLES_DB = "circles.json"

# Ensure database files exist
def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(CIRCLES_DB, {})

# Load & Save functions
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# Password hashing & verification
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Sidebar updates
def show_sidebar_updates():
    st.sidebar.subheader("📢 Latest Updates")
    posts = load_json(POSTS_DB)

    if posts:
        for post in reversed(posts[-5:]):  # Show last 5 posts
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

# Navigation Menu (Sidebar)
st.sidebar.image("https://via.placeholder.com/150", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Profile", "Upload", "Circles", "Log In / Sign Up"])

# --- Home Page ---
if page == "Home":
    st.title("🏡 Atmosphere - Social Connect")
    st.subheader("Explore locations, join circles, and engage with events!")
    show_sidebar_updates()

# --- Explore Page ---
elif page == "Explore":
    st.title("🔍 Explore Recent Uploads & Circles")

    st.subheader("📸 Recent Uploads")
    posts = load_json(POSTS_DB)
    if posts:
        for post in reversed(posts):
            st.write(f"**{post['user']}** uploaded:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))

    st.subheader("🌐 Explore Circles")
    circles = load_json(CIRCLES_DB)

    if circles:
        for circle_name, details in circles.items():
            if st.button(f"Join {circle_name}"):
                user = st.session_state.get("user", "Guest")
                if user not in details["members"]:
                    details["members"].append(user)
                    save_json(CIRCLES_DB, circles)
                    st.success(f"Joined Circle: {circle_name}!")

    st.subheader("⭐ Recommended for You")
    recommended_circles = ["Tech Enthusiasts", "Travel Lovers", "Foodies", "Fitness Gurus"]
    for rec_circle in recommended_circles:
        if st.button(f"Join {rec_circle}"):
            st.success(f"Joined Circle: {rec_circle}!")

# --- Profile Page ---
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_json(USER_DB)

        if username in users:
            user_data = users[username]
            st.subheader(f"👤 @{username}'s Profile")
            st.write(f"**Account Type:** {user_data['account_type']}")
            st.write(f"**Followers:** {len(user_data.get('followers', []))}")
            st.write(f"**Following:** {len(user_data.get('following', []))}")

            st.button("✏️ Edit Profile")

            st.subheader("📸 My Posts")
            posts = load_json(POSTS_DB)
            user_posts = [post for post in posts if post["user"] == username]
            if user_posts:
                for post in reversed(user_posts):
                    st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.info("You haven't posted anything yet.")
        else:
            st.error("User not found!")
    else:
        st.warning("You need to log in first.")

# --- Upload Page ---
elif page == "Upload":
    if "user" in st.session_state:
        st.subheader("📸 Upload & Share Your Moments")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        caption = st.text_area("Write a caption")

        if st.button("Upload"):
            if uploaded_file:
                image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                posts = load_json(POSTS_DB)
                posts.append({"user": st.session_state["user"], "image": image_data, "caption": caption})
                save_json(POSTS_DB, posts)
                st.success("Image uploaded successfully!")
                st.experimental_rerun()
            else:
                st.error("Please upload an image.")
    else:
        st.warning("You need to log in first.")

# --- Circles Page ---
elif page == "Circles":
    st.subheader("🌐 Join or Create Circles")

    if "user" in st.session_state:
        circles = load_json(CIRCLES_DB)

        st.subheader("🔗 Join a Circle")
        if circles:
            selected_circle = st.selectbox("Select a Circle", list(circles.keys()))
            if st.button("Join Circle"):
                user = st.session_state["user"]
                if user not in circles[selected_circle]["members"]:
                    circles[selected_circle]["members"].append(user)
                    save_json(CIRCLES_DB, circles)
                    st.success(f"Joined Circle: {selected_circle}!")

        st.subheader("➕ Create a New Circle")
        new_circle = st.text_input("Circle Name")
        if st.button("Create Circle"):
            if new_circle and new_circle not in circles:
                circles[new_circle] = {"members": [st.session_state["user"]]}
                save_json(CIRCLES_DB, circles)
                st.success(f"Circle *{new_circle}* created!")
            elif new_circle in circles:
                st.error("Circle name already exists!")
    else:
        st.warning("You need to log in first.")

# --- Log In / Sign Up Page ---
elif page == "Log In / Sign Up":
    st.subheader("🔑 Log In or Sign Up")
    choice = st.radio("Choose an option", ["Log In", "Sign Up"])

    if choice == "Log In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            users = load_json(USER_DB)
            if username in users and verify_password(password, users[username]["password"]):
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password!")

    elif choice == "Sign Up":
        new_username = st.text_input("Choose a Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            users = load_json(USER_DB)
            users[new_username] = {"email": email, "password": hash_password(new_password)}
            save_json(USER_DB, users)
            st.success("Account created! You can now log in.")

# Logout
if "user" in st.session_state:
    if st.button("Log Out"):
        del st.session_state["user"]
        st.experimental_rerun()
