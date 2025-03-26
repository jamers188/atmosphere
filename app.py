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

# App UI
st.set_page_config(page_title="atmosphere", page_icon="🌍", layout="centered")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Log In", "Sign Up", "Your Circles"])

# **Log In Page**
if page == "Log In":
    st.image("https://via.placeholder.com/150", width=80)  # Placeholder for logo
    st.title("Atmosphere")
    st.subheader("Share your world, where you are")

    st.write("### Log In")
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

# **Sign Up Page**
elif page == "Sign Up":
    st.write("### Create an Account")
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

# **Circles Page**
elif page == "Your Circles":
    st.write("### Your Circles")
    st.text_input("Search circles...")
    st.button("Create a Circle")

    st.write("#### My Circles")
    st.info("You haven't joined any circles yet.")

    st.write("#### Recommended For You")
locations = [
    {"name": "Downtown Cafe", "type": "Location"},
    {"name": "Sunset Beach", "type": "Location"},
    {"name": "Green Park", "type": "Location"},
    {"name": "Mountain View Resort", "type": "Location"},
    {"name": "City Library", "type": "Location"},
]

circles = [
    {"name": "Coffee Lovers", "type": "Circle"},
    {"name": "Biking Club", "type": "Circle"},
    {"name": "Grand Hotel Guests", "type": "Circle"},
    {"name": "Photography Enthusiasts", "type": "Circle"},
    {"name": "Local Foodies", "type": "Circle"},
]

events = [
    {"name": "Live Music Night", "type": "Event"},
    {"name": "Bike Marathon", "type": "Event"},
    {"name": "Food Festival", "type": "Event"},
    {"name": "Tech Meetup", "type": "Event"},
    {"name": "Yoga in the Park", "type": "Event"},
]

businesses = [
    {"name": "Grand Hotel", "type": "Business"},
    {"name": "Green Park Café", "type": "Business"},
    {"name": "City Gym", "type": "Business"},
    {"name": "Tech Hub Co-working", "type": "Business"},
    {"name": "Sunset Spa", "type": "Business"},
]

# Combine all searchable items
search_data = locations + circles + events + businesses

# Search Page
def search_page():
    st.title("🔍 Search Locations, Circles, Events & Businesses")
    
    # Search input
    query = st.text_input("Type a name to search:")

    if query:
        results = [item for item in search_data if query.lower() in item["name"].lower()]
        
        if results:
            st.write("### 🔎 Search Results:")
            for item in results:
                st.write(f"**{item['name']}** ({item['type']})")
        else:
            st.write("❌ No results found.")

# Sidebar Navigation
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Search", "Profile"])

if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.write("Explore locations, join circles, and engage with events!")
elif page == "Search":
    search_page()
elif page == "Profile":
    st.title("👤 User Profile")
    st.write("Manage your account and settings.")
    st.warning("No circles found for this filter.")

    st.markdown("---")
    st.markdown("🏠 Home | 👥 Groups | 📍 Explore | 👤 Profile", unsafe_allow_html=True)

