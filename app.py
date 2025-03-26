import streamlit as st

st.title("Atmosphere")
st.subheader("Share your world, where you are")

st.text_input("Username", placeholder="Enter your username")
st.text_input("Password", type="password", placeholder="Enter your password")

if st.button("Log In"):
    st.success("Logged in successfully!")

