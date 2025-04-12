import streamlit as st
import bcrypt
import json
import os
import time
from datetime import datetime
from PIL import Image
import random
import uuid

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Atmosphere",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== DATABASE STRUCTURES =====
DB_STRUCTURE = {
    "users": {
        "sample_user": {
            "user_id": "usr_123",
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "<hashed_password>",
            "account_type": "general",
            "verified": True,
            "joined_date": "2023-01-01",
            "interests": ["music", "tech"],
            "location": {"city": "New York", "lat": 40.7128, "lng": -74.0060}
        }
    },
    "businesses": {
        "sample_business": {
            "business_id": "biz_123",
            "owner_id": "usr_123",
            "business_name": "Cool Cafe",
            "category": "Food & Drink",
            "verified": False,
            "locations": [
                {"address": "123 Main St", "lat": 40.7128, "lng": -74.0060}
            ]
        }
    },
    "media": [
        {
            "media_id": "med_123",
            "user_id": "usr_123",
            "file_path": "media_gallery/usr_123_photo1.jpg",
            "location": {"name": "Central Park", "lat": 40.7829, "lng": -73.9654},
            "timestamp": "2023-01-01T12:00:00",
            "circle_id": "cir_123",
            "tags": ["nature", "park"],
            "reports": []
        }
    ],
    "circles": {
        "cir_123": {
            "circle_id": "cir_123",
            "name": "NYC Photographers",
            "description": "For photography enthusiasts in NYC",
            "type": "public",
            "location": {"city": "New York", "lat": 40.7128, "lng": -74.0060},
            "members": ["usr_123"],
            "events": ["evt_123"],
            "business_owned": False
        }
    },
    "events": {
        "evt_123": {
            "event_id": "evt_123",
            "circle_id": "cir_123",
            "name": "Sunset Photography Meetup",
            "description": "Let's capture the sunset together!",
            "location": {"name": "Brooklyn Bridge", "lat": 40.7061, "lng": -73.9969},
            "date": "2023-06-15",
            "time": "18:00",
            "organizer": "usr_123",
            "attendees": ["usr_123"],
            "capacity": 20,
            "tags": ["photography", "outdoors"]
        }
    },
    "promotions": {
        "promo_123": {
            "promo_id": "promo_123",
            "business_id": "biz_123",
            "offer": "20% off coffee",
            "requirements": "Post 3 photos with #CoolCafe",
            "start_date": "2023-01-01",
            "end_date": "2023-01-31",
            "claimed_by": ["usr_123"]
        }
    },
    "notifications": {
        "usr_123": [
            {
                "notification_id": "notif_123",
                "type": "event_reminder",
                "content": "Sunset Photography Meetup starts in 2 hours!",
                "timestamp": "2023-06-15T16:00:00",
                "read": False,
                "related_id": "evt_123"
            }
        ]
    },
    "reports": [
        {
            "report_id": "rep_123",
            "reporter_id": "usr_123",
            "content_id": "med_123",
            "content_type": "media",
            "reason": "Inappropriate content",
            "status": "pending",
            "timestamp": "2023-01-01T12:30:00"
        }
    ]
}

# ===== FILE PATHS =====
DB_FILES = {
    "users": "data/users.json",
    "businesses": "data/businesses.json",
    "media": "data/media.json",
    "circles": "data/circles.json",
    "events": "data/events.json",
    "promotions": "data/promotions.json",
    "notifications": "data/notifications.json",
    "reports": "data/reports.json"
}

MEDIA_DIR = "media_gallery"
os.makedirs("data", exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# ===== HELPER FUNCTIONS =====
def init_db():
    """Initialize database files with empty structures"""
    for file, structure in DB_FILES.items():
        if not os.path.exists(structure):
            with open(structure, "w") as f:
                json.dump({} if file in ["users", "businesses", "circles", "notifications"] else [], f)

def load_db(file_key):
    """Load database file"""
    with open(DB_FILES[file_key], "r") as f:
        return json.load(f)

def save_db(file_key, data):
    """Save database file"""
    with open(DB_FILES[file_key], "w") as f:
        json.dump(data, f, indent=2)

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def add_notification(user_id, notification_type, content, related_id=None):
    """Add notification to user's feed"""
    notifications = load_db("notifications")
    if user_id not in notifications:
        notifications[user_id] = []
    
    notifications[user_id].append({
        "notification_id": generate_id("notif"),
        "type": notification_type,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "read": False,
        "related_id": related_id
    })
    save_db("notifications", notifications)

# ===== INITIALIZE DATABASES =====
init_db()

# ===== AUTHENTICATION =====
def login():
    st.title("🔑 Login to Atmosphere")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                users = load_db("users")
                if username in users and verify_password(password, users[username]["password"]):
                    st.session_state["user"] = users[username]
                    st.session_state["logged_in"] = True
                    add_notification(users[username]["user_id"], "login", "Welcome back to Atmosphere!")
                    st.success("Login successful!")
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")

    with col2:
        st.image("https://via.placeholder.com/500x300?text=Atmosphere+Community", use_column_width=True)
        st.markdown("""
        **New to Atmosphere?**
        - Connect with like-minded people
        - Share your experiences
        - Discover local events
        - Grow your business
        """)

def signup():
    st.title("🆕 Join Atmosphere")
    tab1, tab2 = st.tabs(["General User", "Business Account"])
    
    with tab1:
        with st.form("general_signup"):
            st.subheader("General User Account")
            full_name = st.text_input("Full Name")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            location = st.text_input("Your Location (City)")
            interests = st.multiselect("Your Interests", ["Art", "Music", "Sports", "Food", "Tech", "Nature"])
            
            signup_btn = st.form_submit_button("Create Account")
            
            if signup_btn:
                if password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    users = load_db("users")
                    if username in users:
                        st.error("Username already exists!")
                    else:
                        user_id = generate_id("usr")
                        users[username] = {
                            "user_id": user_id,
                            "full_name": full_name,
                            "email": email,
                            "password": hash_password(password),
                            "account_type": "general",
                            "verified": False,
                            "joined_date": datetime.now().isoformat(),
                            "interests": interests,
                            "location": {"city": location}
                        }
                        save_db("users", users)
                        st.session_state["user"] = users[username]
                        st.session_state["logged_in"] = True
                        st.success("Account created successfully!")
                        time.sleep(1)
                        st.experimental_rerun()

    with tab2:
        with st.form("business_signup"):
            st.subheader("Business Account")
            business_name = st.text_input("Business Name")
            owner_name = st.text_input("Owner/Representative Name")
            username = st.text_input("Username")
            email = st.text_input("Business Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            category = st.selectbox("Business Category", ["Food & Drink", "Retail", "Services", "Entertainment", "Other"])
            address = st.text_input("Business Address")
            
            signup_btn = st.form_submit_button("Register Business")
            
            if signup_btn:
                if password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    users = load_db("users")
                    businesses = load_db("businesses")
                    
                    if username in users:
                        st.error("Username already exists!")
                    else:
                        # Create user account
                        user_id = generate_id("usr")
                        users[username] = {
                            "user_id": user_id,
                            "full_name": owner_name,
                            "email": email,
                            "password": hash_password(password),
                            "account_type": "business",
                            "verified": False,
                            "joined_date": datetime.now().isoformat()
                        }
                        
                        # Create business profile
                        business_id = generate_id("biz")
                        businesses[business_name] = {
                            "business_id": business_id,
                            "owner_id": user_id,
                            "business_name": business_name,
                            "category": category,
                            "verified": False,
                            "locations": [{"address": address}]
                        }
                        
                        save_db("users", users)
                        save_db("businesses", businesses)
                        st.session_state["user"] = users[username]
                        st.session_state["business"] = businesses[business_name]
                        st.session_state["logged_in"] = True
                        st.success("Business account created! Verification pending.")
                        time.sleep(1)
                        st.experimental_rerun()

# ===== MAIN APP PAGES =====
def home_page():
    st.title(f"🌍 Welcome to Atmosphere, {st.session_state['user']['full_name']}")
    
    # User stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Circles Joined", "5")
    with col2:
        st.metric("Events Attended", "3")
    with col3:
        st.metric("Media Shared", "12")
    
    # Activity feed
    st.subheader("📰 Your Activity Feed")
    tab1, tab2, tab3 = st.tabs(["Recent Activity", "Your Circles", "Upcoming Events"])
    
    with tab1:
        st.write("Recent posts from your circles")
        # Sample activity data
        activities = [
            {"user": "JaneDoe", "action": "posted a photo in NYC Photographers", "time": "2h ago"},
            {"user": "MikeT", "action": "created an event: Central Park Picnic", "time": "5h ago"},
            {"user": "CoffeeShop", "action": "offered 20% off for photos", "time": "1d ago"}
        ]
        for activity in activities:
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                <strong>{activity['user']}</strong> {activity['action']}
                <div style="color:gray;font-size:0.8em;">{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        circles = [
            {"name": "NYC Photographers", "members": 45, "new_posts": 3},
            {"name": "Food Lovers", "members": 120, "new_posts": 7},
            {"name": "Tech Enthusiasts", "members": 89, "new_posts": 2}
        ]
        for circle in circles:
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                <strong>{circle['name']}</strong>
                <div>👥 {circle['members']} members | ✉️ {circle['new_posts']} new posts</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "location": "Brooklyn Bridge"},
            {"name": "Food Festival", "date": "Jun 20", "location": "Downtown"},
            {"name": "Tech Meetup", "date": "Jul 2", "location": "Innovation Center"}
        ]
        for event in events:
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                <strong>{event['name']}</strong>
                <div>📅 {event['date']} | 📍 {event['location']}</div>
            </div>
            """, unsafe_allow_html=True)

def explore_page():
    st.title("🔍 Explore")
    
    # Search functionality
    search_col, filter_col = st.columns([3, 1])
    with search_col:
        search_query = st.text_input("Search for circles, events, or locations")
    with filter_col:
        filter_type = st.selectbox("Filter", ["All", "Circles", "Events", "Locations"])
    
    # Map view
    st.subheader("📍 Nearby Locations")
    # In a real app, this would be a map component
    st.image("https://maps.googleapis.com/maps/api/staticmap?center=40.7128,-74.0060&zoom=12&size=800x300&key=YOUR_API_KEY", 
             caption="Map of nearby locations with Atmosphere activity")
    
    # Popular circles
    st.subheader("👥 Popular Circles")
    circles = [
        {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC"},
        {"name": "Food Lovers", "members": 320, "description": "Discover and share great food spots"},
        {"name": "Tech Enthusiasts", "members": 189, "description": "Discuss the latest in technology"}
    ]
    for circle in circles:
        with st.expander(f"{circle['name']} ({circle['members']} members)"):
            st.write(circle['description'])
            if st.button("Join Circle", key=f"join_{circle['name']}"):
                st.success(f"You've joined {circle['name']}!")
    
    # Upcoming events
    st.subheader("📅 Upcoming Events")
    events = [
        {"name": "Central Park Picnic", "date": "Jun 15", "circle": "NYC Photographers"},
        {"name": "Food Festival", "date": "Jun 20", "circle": "Food Lovers"},
        {"name": "Tech Conference", "date": "Jul 2", "circle": "Tech Enthusiasts"}
    ]
    for event in events:
        st.markdown(f"""
        <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
            <strong>{event['name']}</strong>
            <div>📅 {event['date']} | 👥 {event['circle']}</div>
        </div>
        """, unsafe_allow_html=True)

def media_page():
    st.title("📸 Capture & Share")
    
    tab1, tab2 = st.tabs(["Upload Media", "Your Gallery"])
    
    with tab1:
        st.subheader("Upload New Media")
        captured_photo = st.camera_input("Take a photo")
        location = st.text_input("Location", "Central Park, NYC")
        circles = ["NYC Photographers", "Food Lovers", "Tech Enthusiasts"]
        selected_circle = st.selectbox("Share to Circle (optional)", [""] + circles)
        tags = st.multiselect("Tags", ["Nature", "Food", "Tech", "Art", "Sports"])
        
        if st.button("Upload Media") and captured_photo:
            media_id = generate_id("med")
            filename = f"{st.session_state['user']['user_id']}_{media_id}.jpg"
            filepath = os.path.join(MEDIA_DIR, filename)
            
            image = Image.open(captured_photo)
            image.save(filepath)
            
            media = load_db("media")
            media.append({
                "media_id": media_id,
                "user_id": st.session_state["user"]["user_id"],
                "file_path": filepath,
                "location": {"name": location},
                "timestamp": datetime.now().isoformat(),
                "circle_id": selected_circle if selected_circle else None,
                "tags": tags,
                "reports": []
            })
            save_db("media", media)
            st.success("Media uploaded successfully!")
    
    with tab2:
        st.subheader("Your Media Gallery")
        media = load_db("media")
        user_media = [m for m in media if m["user_id"] == st.session_state["user"]["user_id"]]
        
        if not user_media:
            st.info("You haven't uploaded any media yet.")
        else:
            cols = st.columns(3)
            for i, item in enumerate(user_media):
                with cols[i % 3]:
                    st.image(item["file_path"], use_container_width=True)  # Updated here
                    st.caption(f"{item['location']['name']} • {datetime.fromisoformat(item['timestamp']).strftime('%b %d, %Y')}")
                    st.write(f"Tags: {', '.join(item['tags'])}")

def circles_page():
    st.title("👥 Circles")
    
    tab1, tab2, tab3 = st.tabs(["Your Circles", "Discover", "Create Circle"])
    
    with tab1:
        st.subheader("Your Circles")
        # Sample data - in real app would load from DB
        user_circles = [
            {"name": "NYC Photographers", "members": 45, "unread": 3},
            {"name": "Food Lovers", "members": 120, "unread": 7}
        ]
        
        for circle in user_circles:
            with st.expander(f"{circle['name']} ({circle['members']} members) - {circle['unread']} new posts"):
                # Circle chat/feed would go here
                st.write("Recent posts from this circle...")
                if st.button("View Circle", key=f"view_{circle['name']}"):
                    st.session_state["current_circle"] = circle['name']
                    st.experimental_rerun()
    
    with tab2:
        st.subheader("Discover New Circles")
        # Sample circles
        circles = [
            {"name": "Tech Enthusiasts", "members": 189, "description": "Discuss the latest in technology"},
            {"name": "Fitness Community", "members": 87, "description": "Share workout tips and meetups"},
            {"name": "Art Lovers", "members": 142, "description": "Appreciate and create art together"}
        ]
        
        for circle in circles:
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                <strong>{circle['name']}</strong> ({circle['members']} members)
                <div>{circle['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Join", key=f"join_{circle['name']}"):
                st.success(f"You've joined {circle['name']}!")
    
    with tab3:
        st.subheader("Create a New Circle")
        with st.form("create_circle"):
            name = st.text_input("Circle Name")
            description = st.text_area("Description")
            circle_type = st.radio("Type", ["Public", "Private"])
            location = st.text_input("Primary Location (optional)")
            tags = st.multiselect("Tags", ["Art", "Music", "Sports", "Food", "Tech", "Nature"])
            
            if st.form_submit_button("Create Circle"):
                if name:
                    circle_id = generate_id("cir")
                    circles = load_db("circles")
                    circles[circle_id] = {
                        "circle_id": circle_id,
                        "name": name,
                        "description": description,
                        "type": circle_type.lower(),
                        "creator": st.session_state["user"]["user_id"],
                        "members": [st.session_state["user"]["user_id"]],
                        "location": {"name": location} if location else None,
                        "tags": tags,
                        "created_at": datetime.now().isoformat()
                    }
                    save_db("circles", circles)
                    st.success(f"Circle '{name}' created successfully!")
                    add_notification(st.session_state["user"]["user_id"], "circle", f"You created a new circle: {name}")

def events_page():
    st.title("📅 Events")
    
    tab1, tab2, tab3 = st.tabs(["Upcoming Events", "Your Events", "Create Event"])
    
    with tab1:
        st.subheader("Upcoming Events Near You")
        # Sample events
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "location": "Brooklyn Bridge", "circle": "NYC Photographers"},
            {"name": "Food Festival", "date": "Jun 20", "location": "Downtown", "circle": "Food Lovers"},
            {"name": "Tech Meetup", "date": "Jul 2", "location": "Innovation Center", "circle": "Tech Enthusiasts"}
        ]
        
        for event in events:
            with st.expander(f"{event['name']} - {event['date']}"):
                st.write(f"📍 {event['location']}")
                st.write(f"👥 {event['circle']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("RSVP", key=f"rsvp_{event['name']}"):
                        st.success(f"You're attending {event['name']}!")
                with col2:
                    if st.button("View Details", key=f"details_{event['name']}"):
                        st.session_state["view_event"] = event['name']
    
    with tab2:
        st.subheader("Events You're Attending")
        # Sample user events
        user_events = [
            {"name": "Sunset Photography", "date": "Jun 15", "status": "Confirmed"},
            {"name": "Food Tasting", "date": "Jun 18", "status": "Pending"}
        ]
        
        for event in user_events:
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                <strong>{event['name']}</strong>
                <div>📅 {event['date']} | 🏷️ {event['status']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Create New Event")
        with st.form("create_event"):
            name = st.text_input("Event Name")
            description = st.text_area("Description")
            date = st.date_input("Date")
            time = st.time_input("Time")
            location = st.text_input("Location")
            circle = st.selectbox("Associated Circle (optional)", ["", "NYC Photographers", "Food Lovers"])
            capacity = st.number_input("Capacity (0 for unlimited)", min_value=0)
            
            if st.form_submit_button("Create Event"):
                event_id = generate_id("evt")
                events = load_db("events")
                events[event_id] = {
                    "event_id": event_id,
                    "name": name,
                    "description": description,
                    "date": date.isoformat(),
                    "time": str(time),
                    "location": {"name": location},
                    "organizer": st.session_state["user"]["user_id"],
                    "circle_id": circle if circle else None,
                    "capacity": capacity,
                    "attendees": [st.session_state["user"]["user_id"]],
                    "created_at": datetime.now().isoformat()
                }
                save_db("events", events)
                st.success(f"Event '{name}' created successfully!")
                
                # Notify circle members if associated with a circle
                if circle:
                    add_notification(st.session_state["user"]["user_id"], "event", 
                                   f"New event in {circle}: {name}")

def business_page():
    if st.session_state["user"]["account_type"] != "business":
        st.warning("This page is only available for business accounts")
        return
    
    st.title("💼 Business Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Promotions", "Statistics", "Verification"])
    
    with tab1:
        st.subheader("Business Overview")
        # Sample business data
        st.metric("Circle Members", "245")
        st.metric("Media Mentions", "56")
        st.metric("Active Promotions", "3")
        
        st.subheader("Recent Activity")
        st.write("Posts mentioning your business")
        # Would show media that tags the business
    
    with tab2:
        st.subheader("Create Promotion")
        with st.form("create_promotion"):
            offer = st.text_input("Offer (e.g., '20% off')")
            description = st.text_area("Promotion Details")
            requirements = st.text_input("Requirements (e.g., 'Post 3 photos with #OurBusiness')")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            tags = st.multiselect("Relevant Tags", ["Food", "Drink", "Retail", "Service"])
            
            if st.form_submit_button("Launch Promotion"):
                promo_id = generate_id("promo")
                promotions = load_db("promotions")
                promotions[promo_id] = {
                    "promo_id": promo_id,
                    "business_id": st.session_state["user"]["user_id"],
                    "offer": offer,
                    "description": description,
                    "requirements": requirements,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "tags": tags,
                    "created_at": datetime.now().isoformat()
                }
                save_db("promotions", promotions)
                st.success("Promotion launched successfully!")
        
        st.subheader("Active Promotions")
        # Show existing promotions
    
    with tab3:
        st.subheader("Business Statistics")
        # Charts and graphs would go here
        st.write("Engagement metrics over time")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("New Members (7d)", "24")
            st.metric("Media Mentions (7d)", "12")
        with col2:
            st.metric("Promotion Claims", "8")
            st.metric("Event Attendees", "15")
    
    with tab4:
        st.subheader("Business Verification")
        if st.session_state.get("business", {}).get("verified", False):
            st.success("Your business is verified!")
        else:
            st.warning("Your business is not yet verified")
            st.write("To get verified, please provide:")
            with st.form("verification_form"):
                business_license = st.file_uploader("Business License")
                website = st.text_input("Business Website")
                additional_info = st.text_area("Additional Information")
                
                if st.form_submit_button("Submit for Verification"):
                    st.success("Verification submitted! We'll review your information within 3 business days.")

def settings_page():
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Account", "Notifications", "Report Content"])
    
    with tab1:
        st.subheader("Account Settings")
        with st.form("account_settings"):
            full_name = st.text_input("Full Name", value=st.session_state["user"].get("full_name", ""))
            email = st.text_input("Email", value=st.session_state["user"].get("email", ""))
            location = st.text_input("Location", value=st.session_state["user"].get("location", {}).get("city", ""))
            interests = st.multiselect("Interests", 
                                     ["Art", "Music", "Sports", "Food", "Tech", "Nature"],
                                     default=st.session_state["user"].get("interests", []))
            
            if st.form_submit_button("Update Profile"):
                users = load_db("users")
                username = [k for k, v in users.items() if v["user_id"] == st.session_state["user"]["user_id"]][0]
                users[username].update({
                    "full_name": full_name,
                    "email": email,
                    "location": {"city": location},
                    "interests": interests
                })
                save_db("users", users)
                st.session_state["user"] = users[username]
                st.success("Profile updated successfully!")
    
    with tab2:
        st.subheader("Notification Settings")
        st.checkbox("Event reminders", value=True)
        st.checkbox("Circle updates", value=True)
        st.checkbox("Promotions", value=True)
        st.checkbox("New followers", value=True)
        if st.button("Save Notification Preferences"):
            st.success("Notification preferences saved!")
    
    with tab3:
        st.subheader("Report Content")
        with st.form("report_form"):
            content_type = st.selectbox("Content Type", ["Media", "Circle", "Event", "User"])
            content_id = st.text_input("Content ID/URL")
            reason = st.selectbox("Reason", 
                                 ["Inappropriate content", "Spam", "Misinformation", "Harassment", "Other"])
            details = st.text_area("Additional Details")
            
            if st.form_submit_button("Submit Report"):
                report_id = generate_id("rep")
                reports = load_db("reports")
                reports.append({
                    "report_id": report_id,
                    "reporter_id": st.session_state["user"]["user_id"],
                    "content_type": content_type,
                    "content_id": content_id,
                    "reason": reason,
                    "details": details,
                    "status": "pending",
                    "timestamp": datetime.now().isoformat()
                })
                save_db("reports", reports)
                st.success("Report submitted. Our team will review it shortly.")

# ===== NOTIFICATION BELL =====
def notification_bell():
    notifications = load_db("notifications").get(st.session_state["user"]["user_id"], [])
    unread = sum(1 for n in notifications if not n["read"])
    
    with st.sidebar:
        if unread > 0:
            st.button(f"🔔 ({unread})", help="Notifications")
        else:
            st.button("🔔", help="Notifications")
        
        if st.session_state.get("show_notifications"):
            st.session_state["show_notifications"] = False
        else:
            st.session_state["show_notifications"] = True

# ===== MAIN APP FLOW =====
def main():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Atmosphere", width=150)
        st.markdown("---")
        
        if "logged_in" in st.session_state:
            # User info
            st.markdown(f"### Hi, {st.session_state['user']['full_name']}")
            st.markdown(f"*@{st.session_state['user'].get('email', '')}*")
            st.markdown("---")
            
            # Navigation
            pages = {
                "🏠 Home": home_page,
                "🔍 Explore": explore_page,
                "📸 Media": media_page,
                "👥 Circles": circles_page,
                "📅 Events": events_page,
                "💼 Business": business_page,
                "⚙️ Settings": settings_page
            }
            
            selected_page = st.radio("Navigation", list(pages.keys()))
            
            # Notification bell
            notification_bell()
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                del st.session_state["logged_in"]
                del st.session_state["user"]
                st.experimental_rerun()
            
            # Display notifications if toggled
            if st.session_state.get("show_notifications"):
                notifications = load_db("notifications").get(st.session_state["user"]["user_id"], [])
                if notifications:
                    st.subheader("Notifications")
                    for note in notifications[-5:][::-1]:  # Show 5 most recent
                        st.markdown(f"""
                        <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                            {note['content']}
                            <div style="color:gray;font-size:0.8em;">
                                {datetime.fromisoformat(note['timestamp']).strftime('%b %d %H:%M')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No new notifications")
        else:
            st.info("Please login to access the app")
    
    # Main content area
    if "logged_in" in st.session_state:
        pages[selected_page]()
    else:
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        with login_tab:
            login()
        with signup_tab:
            signup()

if __name__ == "__main__":
    main()
