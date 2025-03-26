import streamlit as st
import bcrypt
import json
import os
import base64

# ---- Database Files ----
USER_DB = "users.json"
POSTS_DB = "posts.json"
CIRCLE_DB = "circles.json"

# Ensure files exist
def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(POSTS_DB, [])
ensure_file(CIRCLE_DB, {})

# Load & Save JSON Data
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Password Hashing & Verification
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---- Streamlit Page Configuration ----
st.set_page_config(page_title="Atmosphere - Social Connect", page_icon="🌍", layout="wide")

# ---- Sidebar Navigation ----
st.sidebar.image("https://via.placeholder.com/100", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Profile", "Upload Media", "Circles", "Log In", "Sign Up"])

# ---- Latest Updates Sidebar ----
def show_sidebar_updates():
    st.sidebar.subheader("📢 Latest Updates")
    posts = load_data(POSTS_DB)

    if posts:
        for post in reversed(posts[-3:]):  # Show last 3 posts
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

show_sidebar_updates()

# ---- Home Page ----
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("🌍 Discover, Connect, and Share!")
    st.image("https://via.placeholder.com/600x300", use_container_width=True)

    # Upcoming Events
    st.subheader("📅 Upcoming Events")
    events = [
        {"name": "Music Fest 2025", "location": "Central Park", "date": "April 15"},
        {"name": "Tech Conference", "location": "Silicon Valley", "date": "May 10"},
        {"name": "Food Carnival", "location": "Downtown Plaza", "date": "June 1"},
    ]
    for event in events:
        st.write(f"🎉 **{event['name']}** - 📍 {event['location']} 🗓 {event['date']}")

# ---- Explore Page (Recent Uploads & Circles) ----
elif page == "Explore":
    st.title("📸 Explore Recent Uploads & Circles")
    posts = load_data(POSTS_DB)

    if posts:
        for post in reversed(posts[:5]):  # Show latest 5 posts
            st.write(f"**{post['user']}** uploaded:")
            if post.get("image"):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
            else:
                st.write(post.get("caption", "No caption."))
    else:
        st.info("No posts yet!")

    # Circles Section
    st.subheader("🔗 Explore Circles")
    circles = load_data(CIRCLE_DB)
    if circles:
        for circle in circles.keys():
            st.write(f"👉 {circle}")
    else:
        st.write("No circles yet!")

# ---- Profile Page ----
elif page == "Profile":
    if "user" in st.session_state:
        username = st.session_state["user"]
        users = load_data(USER_DB)

        if username in users:
            user_data = users[username]
            st.title(f"👤 @{username}")
            st.write(f"**Account Type:** {user_data['account_type']}")
            st.write(f"📌 **Posts:** {len([p for p in load_data(POSTS_DB) if p['user'] == username])}")
            st.write(f"👥 **Followers:** {len(user_data.get('followers', []))}")
            st.write(f"🔗 **Following:** {len(user_data.get('following', []))}")

            # Edit Profile Option
            if st.button("✏️ Edit Profile"):
                st.write("Feature coming soon...")

            # Display My Posts
            st.subheader("📸 My Posts")
            posts = [p for p in load_data(POSTS_DB) if p["user"] == username]
            for post in reversed(posts):
                st.image(base64.b64decode(post["image"]), caption=post.get("caption", ""), use_container_width=True)
    else:
        st.warning("You need to log in first.")

# ---- Upload Media Page ----
elif page == "Upload Media":
    if "user" in st.session_state:
        st.subheader("📸 Upload Your Image")
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
        st.warning("You need to log in first.")

# ---- Circles Page ----
elif page == "Circles":
    st.title("👥 Join or Create Circles")
    circles = load_data(CIRCLE_DB)

    # Join a Circle
    if circles:
        selected_circle = st.selectbox("Select a Circle to Join", list(circles.keys()))
        if st.button("Join Circle"):
            st.success(f"🎉 Joined Circle: {selected_circle}")

    # Create a Circle
    st.subheader("➕ Create a New Circle")
    new_circle = st.text_input("Circle Name")
    if st.button("Create Circle"):
        if new_circle and new_circle not in circles:
            circles[new_circle] = {"members": [st.session_state["user"]]}
            save_data(CIRCLE_DB, circles)
            st.success(f"✅ Created Circle: {new_circle}")

# ---- Login / Signup ----
elif page in ["Log In", "Sign Up"]:
    st.warning("Login & Signup features already exist in the previous code.")

# ---- Logout ----
if "user" in st.session_state:
    if st.button("🚪 Log Out"):
        del st.session_state["user"]
        st.experimental_rerun()

