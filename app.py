import streamlit as st
import bcrypt
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

# Password Hashing & Verification
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/100", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Profile", "Upload Media", "Circles", "Business", "Settings", "Log In", "Sign Up"])

# --- Log In Page ---
if page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        users = load_data(USER_DB)
        if username in users and verify_password(password, users[username]["password"]):
            st.success(f"Welcome back, {username}!")
            st.session_state["user"] = username  # Store session
            st.session_state["account_type"] = users[username]["account_type"]
            st.experimental_rerun()
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

# --- Business Owner Page ---
elif page == "Business":
    if "user" in st.session_state and st.session_state.get("account_type") == "Business":
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
    else:
        st.warning("You need to be a business user to access this page.")

# Footer Navigation
st.markdown("---")
st.markdown("🏠 Home | 👥 Circles | 📍 Explore | 📸 Upload Media | 👤 Profile", unsafe_allow_html=True)
