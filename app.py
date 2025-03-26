import streamlit as st
import bcrypt
import json
import os

# File to store users & circles
USER_DB = "users.json"
CIRCLE_DB = "circles.json"

# Ensure user database and circles file exist
for file in [USER_DB, CIRCLE_DB]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

# Load & Save JSON Data
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Hash & Verify Passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Streamlit App Config
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/150", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Search", "Profile", "Upload Media", "Circles", "Log In", "Sign Up"])

# --- Home Page ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("Explore locations, join circles, and engage with events!")
    st.image("https://via.placeholder.com/600x300", use_container_width=True)

# --- Search Page ---
elif page == "Search":
    st.title("🔍 Search Locations, Circles, Events & Businesses")
    search_query = st.text_input("Type a name to search:")
    
    search_data = [
        {"name": "Downtown Cafe", "type": "Location"},
        {"name": "Coffee Lovers", "type": "Circle"},
        {"name": "Live Music Night", "type": "Event"},
        {"name": "Grand Hotel", "type": "Business"},
    ]

    if search_query:
        results = [item for item in search_data if search_query.lower() in item["name"].lower()]
        if results:
            for item in results:
                st.write(f"**{item['name']}** ({item['type']})")
        else:
            st.write("❌ No results found.")

# --- Profile Page ---
elif page == "Profile":
    st.title("👤 User Profile")
    if "user" in st.session_state:
        st.write(f"Logged in as: **{st.session_state['user']}**")
        st.button("Log Out", on_click=lambda: st.session_state.pop("user", None))
    else:
        st.warning("You are not logged in.")

# --- Upload Media Page ---
elif page == "Upload Media":
    if "user" not in st.session_state:
        st.warning("You must be logged in to upload media.")
    else:
        st.title("📸 Upload Your Photo")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        location = st.text_input("Location (Where was this taken?)")
        upload_btn = st.button("Upload")

        if upload_btn and uploaded_file and location:
            st.success(f"Image uploaded successfully for **{location}**!")

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
                    st.success(f"Joined **{selected_circle}**!")
                else:
                    st.info("You are already a member.")

        # Create a Circle
        st.subheader("➕ Create a New Circle")
        new_circle = st.text_input("Circle Name")
        if st.button("Create Circle"):
            if new_circle and new_circle not in circles:
                circles[new_circle] = {"members": [st.session_state["user"]]}
                save_data(CIRCLE_DB, circles)
                st.success(f"Circle **{new_circle}** created!")
            elif new_circle in circles:
                st.error("Circle name already exists!")

# --- Log In Page ---
elif page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        users = load_data(USER_DB)
        if username in users and verify_password(password, users[username]["password"]):
            st.success(f"Welcome back, {username}!")
            st.session_state["user"] = username  # Store session
        else:
            st.error("Invalid username or password!")

# --- Sign Up Page ---
elif page == "Sign Up":
    st.title("🆕 Create an Account")
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
            users = load_data(USER_DB)
            if new_username in users:
                st.error("Username already exists!")
            else:
                users[new_username] = {
                    "full_name": full_name,
                    "email": email,
                    "password": hash_password(new_password),
                    "account_type": account_type
                }
                save_data(USER_DB, users)
                st.success("Account created! You can now log in.")

# Footer Navigation
st.markdown("---")
st.markdown("🏠 Home | 👥 Circles | 📍 Explore | 📸 Upload Media | 👤 Profile", unsafe_allow_html=True)
