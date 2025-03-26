import streamlit as st
import json
import os
import base64

# Page config
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Database files
USER_DB = "users.json"
POSTS_DB = "posts.json"
CIRCLE_DB = "circles.json"
PROMO_DB = "promotions.json"

# Ensure database files exist
def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(CIRCLE_DB, {})
ensure_file(PROMO_DB, [])

# Load & Save JSON Data
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/100", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Profile", "Upload Media", "Circles", "Business", "Settings"])

# --- Home Page ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("Explore locations, join circles, and engage with events!")

    # Display Upcoming Events
    st.subheader("🔥 Upcoming Events")
    event_columns = st.columns(3)
    events = [
        {"name": "Music Festival", "image": "https://via.placeholder.com/100"},
        {"name": "Tech Conference", "image": "https://via.placeholder.com/100"},
        {"name": "Food Expo", "image": "https://via.placeholder.com/100"},
    ]
    for col, event in zip(event_columns, events):
        with col:
            st.image(event["image"], width=100)
            st.write(event["name"])

# --- Explore Page ---
elif page == "Explore":
    st.title("🔍 Explore Recent Uploads")
    
    # Show Recent Posts
    posts = load_data(POSTS_DB)
    if posts:
        for post in reversed(posts):
            st.write(f"**{post['user']}** uploaded:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))

    # Show Circles
    st.subheader("👥 Join Circles")
    circles = load_data(CIRCLE_DB)
    for circle in circles:
        if st.button(f"Join {circle}"):
            st.success(f"Joined circle {circle}!")

# --- Profile Page ---
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_data(USER_DB)
        
        if username in users:
            user_data = users[username]

            # Profile Header (Instagram-Like)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <img src="https://via.placeholder.com/100" style="border-radius: 50%; width: 100px; height: 100px; margin-right: 20px;">
                    <div>
                        <h2>@{username}</h2>
                        <p>{user_data.get("email", "No email provided")}</p>
                        <p>🔹 {len(user_data.get('followers', []))} Followers  |  🔹 {len(user_data.get('following', []))} Following</p>
                        <button>Edit Profile</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # My Posts
            st.subheader("📸 My Posts")
            posts = load_data(POSTS_DB)
            user_posts = [post for post in posts if post["user"] == username]

            if user_posts:
                for post in reversed(user_posts):
                    if post.get("image"):
                        st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
                    else:
                        st.write(post.get("caption", "No caption."))

            # Saved Posts Section
            st.subheader("📌 Saved Posts")
            st.info("No saved posts yet.")
        else:
            st.error("User not found!")
    else:
        st.warning("You need to log in first.")

# --- Upload Media Page ---
elif page == "Upload Media":
    if "user" in st.session_state:
        st.title("📸 Upload Your Photo")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
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

# --- Circles Page ---
elif page == "Circles":
    st.title("👥 Your Circles")
    
    if "user" not in st.session_state:
        st.warning("Log in to join or create circles.")
    else:
        circles = load_data(CIRCLE_DB)

        # Join a Circle
        st.subheader("🔗 Join a Circle")
        if circles:
            selected_circle = st.selectbox("Select a Circle", list(circles.keys()))
            if st.button("Join Circle"):
                user = st.session_state["user"]
                if user not in circles[selected_circle]["members"]:
                    circles[selected_circle]["members"].append(user)
                    save_data(CIRCLE_DB, circles)
                    st.success(f"Joined *{selected_circle}*!")
                else:
                    st.info("You are already a member.")

        # Leave a Circle
        if circles:
            leave_circle = st.selectbox("Select a Circle to Leave", list(circles.keys()))
            if st.button("Leave Circle"):
                user = st.session_state["user"]
                if user in circles[leave_circle]["members"]:
                    circles[leave_circle]["members"].remove(user)
                    save_data(CIRCLE_DB, circles)
                    st.warning(f"Left *{leave_circle}*.")

# --- Business Owner Page ---
elif page == "Business":
    st.title("💼 Business Panel")

    st.subheader("📢 Create Promotion")
    media_count = st.number_input("Number of Media Posts", min_value=1)
    discount_offer = st.text_input("Enter Offer (e.g., '40% Off')")

    if st.button("Create Promotion"):
        if media_count and discount_offer:
            promotions = load_data(PROMO_DB)
            promotions.append({"posts": media_count, "offer": discount_offer})
            save_data(PROMO_DB, promotions)
            st.success(f"Promotion Created: Post {media_count} media to get {discount_offer}!")
        else:
            st.error("Please enter all details.")

# --- Settings Page (Logout Moved Here) ---
elif page == "Settings":
    st.title("⚙️ Settings")
    if "user" in st.session_state:
        if st.button("Log Out"):
            del st.session_state["user"]
            st.experimental_rerun()
    else:
        st.warning("You are not logged in.")

