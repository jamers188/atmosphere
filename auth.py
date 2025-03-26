import streamlit as st
import sqlite3
import hashlib

# Connect to SQLite database
conn = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
    return cursor.fetchone()

# Streamlit UI
st.title("Welcome to Atmosphere")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome {user[1]}! You are now logged in.")
            st.session_state["logged_in"] = True
            st.session_state["username"] = user[1]
        else:
            st.error("Invalid login credentials.")

elif choice == "Register":
    st.subheader("Create a new account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if register_user(new_username, new_email, new_password):
            st.success("Account created successfully! You can now log in.")
        else:
            st.error("Username or email already exists. Try a different one.")
