import streamlit as st
import sqlite3
import bcrypt

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Database Setup
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Initialize the database


# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Function to check login credentials
def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()  # Fetch the stored hashed password
    
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False


# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists


# Page Navigation
menu = st.sidebar.radio("Navigation", ["Login", "Register", "Dashboard"])

# Login Page
if menu == "Login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful! Redirecting...")
            st.session_state["logged_in"] = True  # Store session
            st.session_state["username"] = username
            st.experimental_rerun()  # Refresh the app
        else:
            st.error("Invalid username or password. Try again.")

# Registration Page
elif menu == "Register":
    st.title("Register")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")

    if st.button("Register"):
        if register_user(new_username, new_password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists. Choose a different one.")

# Dashboard (Only if logged in)
elif menu == "Dashboard":
    if st.session_state["logged_in"]:
        st.title(f"Welcome, {st.session_state['username']}!")

        if st.button("Logout"):
            del st.session_state["logged_in"]
            del st.session_state["username"]
            st.experimental_rerun()
    else:
        st.warning("Please log in to access the dashboard.")
