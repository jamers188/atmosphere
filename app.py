import streamlit as st

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Profile", "Circles", "Business", "Analytics"])

if page == "Home":
    from pages import home
elif page == "Profile":
    from pages import profile
elif page == "Circles":
    from pages import circles
elif page == "Business":
    from pages import business
elif page == "Analytics":
    from pages import analytics
