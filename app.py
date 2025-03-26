import streamlit as st

# Set page title
st.set_page_config(page_title="Atmosphere", page_icon="📍")

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

# Function to switch pages
def switch_page(page_name):
    st.session_state.page = page_name

# Login Page
if st.session_state.page == "login":
    st.title("Atmosphere")
    st.subheader("Share your world, where you are")

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Log In"):
        # Here, you can add authentication logic
        st.success("Logged in successfully!")

    st.markdown("---")
    st.button("Create an Account", on_click=lambda: switch_page("register"))

# Registration Page
elif st.session_state.page == "register":
    st.title("Register for Atmosphere")
    
    new_username = st.text_input("Choose a Username", placeholder="Enter a username")
    new_email = st.text_input("Email", placeholder="Enter your email")
    new_password = st.text_input("Choose a Password", type="password", placeholder="Enter a strong password")

    if st.button("Register"):
        # Here, you can add user registration logic (save to database)
        st.success("Account created successfully! You can now log in.")
        switch_page("login")

    st.markdown("---")
    st.button("Back to Login", on_click=lambda: switch_page("login"))
