import streamlit as st
import bcrypt
import json
import os
import time
from datetime import datetime
from PIL import Image

# ---- CONFIGURATION ----
st.set_page_config(page_title="Atmosphere", page_icon="🌍", layout="wide")

# ---- DATABASE FILES ----
USER_DB = "users.json"
MEDIA_DB = "media.json"
CIRCLE_DB = "circles.json"
EVENT_DB = "events.json"
PROMO_DB = "promotions.json"
REPORT_DB = "reports.json"

MEDIA_DIR = "media_gallery"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# ---- FUNCTION HELPERS ----
def ensure_file(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f)

ensure_file(USER_DB, {})
ensure_file(MEDIA_DB, [])
ensure_file(CIRCLE_DB, {})
ensure_file(EVENT_DB, [])
ensure_file(PROMO_DB, [])
ensure_file(REPORT_DB, [])

def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---- SIDEBAR NAVIGATION ----
st.sidebar.image("https://via.placeholder.com/100", width=80)
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Profile", "Upload Media", "Circles", "Business", "Settings", "Log In", "Sign Up"])

# ---- LOG IN ----
if page == "Log In":
    st.title("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        users = load_data(USER_DB)
        if username in users and verify_password(password, users[username]["password"]):
            st.success(f"Welcome back, {username}!")
            st.session_state["user"] = username
            st.session_state["account_type"] = users[username]["account_type"]
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

# ---- SIGN UP ----
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

# ---- UPLOAD MEDIA ----
elif page == "Upload Media":
    st.title("📸 Capture & Upload Media")

    if "user" in st.session_state:
        captured_photo = st.camera_input("Take a photo")

        if captured_photo:
            timestamp = int(time.time())
            filename = f"{st.session_state['user']}_{timestamp}.png"
            filepath = os.path.join(MEDIA_DIR, filename)

            image = Image.open(captured_photo)
            image.save(filepath)

            media_data = load_data(MEDIA_DB)
            media_data.append({
                "user": st.session_state["user"],
                "file": filename,
                "timestamp": datetime.now().isoformat()
            })
            save_data(MEDIA_DB, media_data)

            st.success("Photo saved! You can upload it later.")
    else:
        st.warning("Please log in to upload media.")

# ---- IN-APP GALLERY ----
    st.subheader("📂 Your Media Gallery")
    media_data = load_data(MEDIA_DB)
    user_media = [m for m in media_data if m["user"] == st.session_state.get("user")]

    if user_media:
        selected_file = st.selectbox("Select a photo to upload", [m["file"] for m in user_media])
        st.image(os.path.join(MEDIA_DIR, selected_file), caption="Preview", use_column_width=True)

        if st.button("Upload Selected Photo"):
            st.success("Photo uploaded successfully!")
    else:
        st.info("No saved photos. Capture one first!")

# ---- CIRCLES ----
elif page == "Circles":
    st.title("👥 Circles")
    circles = load_data(CIRCLE_DB)
    
    if st.session_state.get("user"):
        circle_name = st.text_input("Create a Circle")
        circle_type = st.radio("Circle Type", ["Public", "Private"])
        create_circle_btn = st.button("Create")

        if create_circle_btn:
            if circle_name in circles:
                st.error("Circle name already exists!")
            else:
                circles[circle_name] = {"type": circle_type, "members": [st.session_state["user"]]}
                save_data(CIRCLE_DB, circles)
                st.success("Circle created!")

    st.subheader("Join a Circle")
    circle_options = [c for c in circles if st.session_state["user"] not in circles[c]["members"]]
    if circle_options:
        selected_circle = st.selectbox("Select a circle to join", circle_options)
        if st.button("Join Circle"):
            circles[selected_circle]["members"].append(st.session_state["user"])
            save_data(CIRCLE_DB, circles)
            st.success(f"Joined {selected_circle}!")
    else:
        st.info("No available circles.")
# ---- EXPLORE ----
def explore():
    st.title("🔍 Explore Events")

    # Random event notifications
    event_notifications = [
        "🎶 Live Jazz Night at Central Park!",
        "📢 Tech Conference at Innovation Hub!",
        "🍕 Food Festival at Downtown Plaza!",
        "🚴‍♂️ Cycling Marathon - Sign Up Now!",
        "🎨 Art Exhibition - Free Entry This Week!"
    ]
    random_event = random.choice(event_notifications)
    st.info(f"**Event Notification:** {random_event}")

    # Search bar with common keywords
    common_keywords = ["music", "tech", "food", "sports", "art"]
    search_query = st.text_input("Search for events (e.g., music, tech, food, sports, art)").lower()

    # Event recommendations
    all_events = [
        {"name": "Music Fest", "location": "Central Park", "category": "music"},
        {"name": "Tech Meetup", "location": "Tech Hub", "category": "tech"},
        {"name": "Food Carnival", "location": "Downtown", "category": "food"},
        {"name": "Sports Championship", "location": "City Stadium", "category": "sports"},
        {"name": "Art & Craft Fair", "location": "Gallery Hall", "category": "art"}
    ]

    # Filter events based on search query
    filtered_events = [
        event for event in all_events if any(word in event["category"] for word in search_query.split())
    ] if search_query else all_events

    st.subheader("🎯 Recommended for You")
    for event in filtered_events:
        st.write(f"📍 **{event['name']}** - {event['location']} ({event['category'].capitalize()})")



# ---- REPORTING CONTENT ----
elif page == "Settings":
    st.title("🚨 Report Content")
    report_content = st.text_area("Describe the issue")
    report_btn = st.button("Submit Report")

    if report_btn:
        reports = load_data(REPORT_DB)
        reports.append({"user": st.session_state["user"], "report": report_content, "timestamp": datetime.now().isoformat()})
        save_data(REPORT_DB, reports)
        st.success("Report submitted successfully!")

# ---- BUSINESS PANEL ----
elif page == "Business":
    st.title("💼 Business Panel")

    if st.session_state.get("account_type") == "Business":
        st.subheader("📢 Create Promotion")
        media_count = st.number_input("Number of Media Posts", min_value=1)
        discount_offer = st.text_input("Enter Offer (e.g., '40% Off')")

        if st.button("Create Promotion"):
            promotions = load_data(PROMO_DB)
            promotions.append({"posts": media_count, "offer": discount_offer})
            save_data(PROMO_DB, promotions)
            st.success(f"Promotion Created!")
    else:
        st.warning("Business accounts only.")

st.markdown("---")
st.markdown("🏠 Home | 👥 Circles | 📍 Explore | 📸 Upload Media | 👤 Profile", unsafe_allow_html=True)
