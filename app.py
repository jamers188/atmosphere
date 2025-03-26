import streamlit as st
import bcrypt
import json
import os

# Set page configuration
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# --- USER DATABASE HANDLING ---
USER_DB = "users.json"

# Ensure user database file exists
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# --- SESSION MANAGEMENT ---
if "user" not in st.session_state:
    st.session_state["user"] = None

# --- NAVIGATION ---
st.sidebar.title("📍 Atmosphere")
page = st.sidebar.radio("Navigate", ["Home", "Search", "Your Circles", "Log In", "Sign Up"])

# --- SEARCH FUNCTIONALITY ---
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

search_data = locations + circles + events + businesses

def search_page():
    st.title("🔍 Search Locations, Circles, Events & Businesses")
    query = st.text_input("Enter a name to search:")
    
    if query:
        results = [item for item in search_data if query.lower() in item["name"].lower()]
        if results:
            st.write("### 🔎 Search Results:")
            for item in results:
                st.write(f"**{item['name']}** ({item['type']})")
        else:
            st.warning("No results found.")

# --- HOME PAGE ---
if page == "Home":
    st.title("🏡 Welcome to Atmosphere")
    st.subheader("Share your world, where you are")
    st.image("https://via.placeholder.com/800x300", use_column_width=True)  # Placeholder banner

    if st.session_state["user"]:
        st.success(f"Welcome back, {st.session_state['user']}!")
    else:
        st.info("Log in or sign up to explore Atmosphere.")

# --- LOG IN PAGE ---
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

# --- SIGN UP PAGE ---
elif page == "Sign Up":
    st.title("🆕 Create an Account")
    account_type = st.radio("Account Type", ["General User", "Business"])
    full_name = st.text_input("Full Name")
    new_username = st.text_input("Username")
    email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    signup_btn = st.button("Sign Up")

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

# --- CIRCLES PAGE ---
elif page == "Your Circles":
    st.title("👥 Your Circles")
    
    st.text_input("🔎 Search circles...")
    st.button("➕ Create a Circle")

    st.write("### My Circles")
    st.warning("You haven't joined any circles yet.")

    st.write("### Recommended Circles")
    for circle in circles[:3]:  # Show top 3 recommended circles
        st.write(f"🔹 **{circle['name']}**")

# --- SEARCH PAGE ---
elif page == "Search":
    search_page()

# --- FOOTER NAVIGATION ---
st.markdown("---")
st.markdown(
    '<p style="text-align:center;">🏠 Home | 👥 Circles | 📍 Explore | 👤 Profile</p>',
    unsafe_allow_html=True
)
