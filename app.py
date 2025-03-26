import streamlit as st
import bcrypt
import json
import os

# File to store users
USER_DB = "users.json"

# Ensure user database file exists
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

# Load users from file
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Streamlit App Config
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/150", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Search", "Profile", "Log In", "Sign Up"])

# --- Home Page ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("Explore locations, join circles, and engage with events!")

    # Main Sections

    st.image("https://via.placeholder.com/600x300", use_container_width=True)

    st.write("### Your Circles")
    st.button("Create a Circle")
    st.write("You haven't joined any circles yet.")

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
    st.write("Manage your account and settings.")

    if "user" in st.session_state:
        st.write(f"Logged in as: **{st.session_state['user']}**")
    else:
        st.warning("You are not logged in.")

# --- Log In Page ---
elif page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        users = load_users()
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

# Footer Navigation
st.markdown("---")
st.markdown("🏠 Home | 👥 Circles | 📍 Explore | 👤 Profile", unsafe_allow_html=True)
