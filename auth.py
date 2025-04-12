import streamlit as st
import bcrypt
import json
import os
import time
from datetime import datetime
from PIL import Image
import random
import uuid
import base64
from io import BytesIO

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Atmosphere",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for styling
def load_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #4361ee;
            --primary-light: #4895ef;
            --secondary: #3f37c9;
            --success: #4cc9f0;
            --info: #4895ef;
            --warning: #f72585;
            --danger: #e63946;
            --light: #f8f9fa;
            --dark: #212529;
        }
        
        /* Card styling */
        .card {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
            background-color: white;
        }
        
        .card-header {
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
            color: var(--dark);
        }
        
        .card-subheader {
            font-weight: 500;
            font-size: 1rem;
            color: #555;
            margin-bottom: 0.5rem;
        }
        
        /* Activity items */
        .activity-item {
            background-color: #f8f9fa;
            border-left: 4px solid var(--primary);
            padding: 10px 15px;
            border-radius: 6px;
            margin: 8px 0;
            transition: all 0.2s ease;
        }
        
        .activity-item:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .activity-name {
            font-weight: 600;
            color: var(--dark);
        }
        
        .activity-action {
            color: #444;
        }
        
        .activity-time {
            color: #777;
            font-size: 0.8rem;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border-radius: 20px;
            padding: 2px 15px;
            border: none;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--primary-light);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transform: translateY(-1px);
        }
        
        /* Secondary button */
        .secondary-btn {
            background-color: white !important;
            color: var(--primary) !important;
            border: 1px solid var(--primary) !important;
        }
        
        .secondary-btn:hover {
            background-color: var(--light) !important;
        }
        
        /* Form inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect {
            border-radius: 6px;
            border: 1px solid #ced4da;
            padding: 8px 12px;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 0.2rem rgba(67, 97, 238, 0.25);
        }
        
        /* Navigation sidebar */
        .sidebar .sidebar-content {
            background-image: linear-gradient(#4361ee, #3a0ca3);
            color: white;
        }
        
        /* Section headers */
        h1, h2, h3 {
            color: #333;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-weight: 700;
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 0.5rem;
        }
        
        h2 {
            font-weight: 600;
        }
        
        h3 {
            font-weight: 500;
        }
        
        /* Notification badge */
        .notification-badge {
            background-color: var(--warning);
            color: white;
            border-radius: 50%;
            padding: 0.2rem 0.5rem;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
        
        /* Event card */
        .event-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid var(--info);
            transition: transform 0.2s ease;
        }
        
        .event-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .event-title {
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 5px;
        }
        
        .event-details {
            color: #555;
            font-size: 0.9rem;
        }
        
        .event-date {
            color: var(--primary);
            font-weight: 500;
        }
        
        /* Circle card */
        .circle-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid var(--secondary);
            transition: transform 0.2s ease;
        }
        
        .circle-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Media gallery styling */
        .gallery-item {
            position: relative;
            margin-bottom: 15px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .gallery-item:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .gallery-item img {
            width: 100%;
            border-radius: 8px;
            display: block;
        }
        
        .gallery-caption {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px 12px;
            font-size: 0.9rem;
        }
        
        /* Metrics styling */
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #555;
            margin-top: 5px;
        }
        
        /* Login/Signup container */
        .auth-container {
            max-width: 500px;
            margin: 2rem auto;
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Welcome banner */
        .welcome-banner {
            background-image: linear-gradient(135deg, #4361ee, #3a0ca3);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .welcome-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .welcome-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        /* Fix tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            color: #555;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(67, 97, 238, 0.1);
            color: var(--primary);
        }
        
        /* Custom metrics */
        div[data-testid="stMetricValue"] > div {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.9rem;
            color: #555;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        /* Profile picture */
        .profile-pic {
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Logo */
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

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
    try:
        with open(DB_FILES[file_key], "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty structure if file doesn't exist or is corrupted
        return {} if file_key in ["users", "businesses", "circles", "notifications"] else []

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

def get_initials(name):
    """Get initials from a name"""
    if not name:
        return "U"
    words = name.split()
    initials = "".join([word[0].upper() for word in words if word])
    return initials[:2]  # Return up to 2 initials

def create_user_avatar(name, size=150):
    """Create a colorful avatar with user's initials"""
    colors = [
        "#4361ee", "#3a0ca3", "#7209b7", "#f72585", "#4cc9f0",
        "#4895ef", "#560bad", "#f15bb5", "#fee440", "#00bbf9"
    ]
    
    initials = get_initials(name)
    color_seed = sum(ord(c) for c in name) if name else 0
    bg_color = colors[color_seed % len(colors)]
    
    # Create a BytesIO object
    img_io = BytesIO()
    # Create a new image with the color
    img = Image.new('RGB', (size, size), color=bg_color)
    # Get a drawing context
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font = ImageFont.truetype("arial.ttf", size=int(size/2))
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the text
    text_width, text_height = d.textsize(initials, font=font)
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    d.text(position, initials, fill="white", font=font)
    
    # Save the image to BytesIO object
    img.save(img_io, format='PNG')
    
    # Get the BytesIO value and encode as base64
    img_data = img_io.getvalue()
    return base64.b64encode(img_data).decode()

def render_card(title, content, style=""):
    """Render a card with title and content"""
    st.markdown(f"""
    <div class="card {style}">
        <div class="card-header">{title}</div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_activity_item(user, action, time):
    """Render an activity item"""
    return f"""
    <div class="activity-item">
        <span class="activity-name">{user}</span>
        <span class="activity-action"> {action}</span>
        <div class="activity-time">{time}</div>
    </div>
    """

def render_event_card(event, interactive=True):
    """Render an event card"""
    buttons = ""
    if interactive:
        buttons = f"""
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <button class="stButton button">RSVP</button>
            <button class="stButton secondary-btn">Details</button>
        </div>
        """
    
    return f"""
    <div class="event-card">
        <div class="event-title">{event['name']}</div>
        <div class="event-details">
            <span class="event-date">📅 {event['date']}</span> • 
            📍 {event['location']} • 
            👥 {event.get('circle', '')}
        </div>
        {buttons}
    </div>
    """

def render_circle_card(circle, interactive=True):
    """Render a circle card"""
    buttons = ""
    if interactive:
        buttons = f"""
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <button class="stButton button">Join</button>
            <button class="stButton secondary-btn">View</button>
        </div>
        """
    
    return f"""
    <div class="circle-card">
        <div class="event-title">{circle['name']}</div>
        <div class="event-details">
            👥 {circle.get('members', 0)} members • 
            {circle.get('description', '')}
        </div>
        {buttons}
    </div>
    """

def render_metric_card(value, label):
    """Render a metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def render_welcome_banner(name):
    """Render welcome banner"""
    return f"""
    <div class="welcome-banner">
        <div class="welcome-title">Welcome back, {name}!</div>
        <div class="welcome-subtitle">
            Discover events, connect with communities, and share your experiences.
        </div>
    </div>
    """

# ===== INITIALIZE DATABASES =====
init_db()
load_css()

# ===== AUTHENTICATION =====
def login():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; color: #4361ee;">Welcome to Atmosphere</h1>
            <p>Login to connect with your community</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.form_submit_button("Login", use_container_width=True, 
                                 on_click=lambda: login_user(username, password))
        with col2:
            forgot_password = st.form_submit_button("Forgot Password?", use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center;">
            <p>Don't have an account?</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Create New Account", use_container_width=True):
        st.session_state["auth_page"] = "signup"
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def login_user(username, password):
    if not username or not password:
        st.error("Please enter both username and password")
        return

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

def signup():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; color: #4361ee;">Join Atmosphere</h1>
            <p>Create your account to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["General User", "Business Account"])
    
    with tab1:
        with st.form("general_signup"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
            with col2:
                username = st.text_input("Username", placeholder="Choose a username")
            
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email", placeholder="Enter your email")
            with col2:
                location = st.text_input("Your Location", placeholder="City, Country")
                
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
            interests = st.multiselect("Your Interests", 
                                     ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Fashion", "Books", "Movies"])
            
            col1, col2 = st.columns([1, 1])
            with col1:
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True, 
                                     on_click=lambda: setattr(st.session_state, "auth_page", "login"))
            
            if signup_btn:
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif password != confirm_password:
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
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business Name", placeholder="Enter your business name")
            with col2:
                category = st.selectbox("Business Category", 
                                      ["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"])
            
            col1, col2 = st.columns(2)
            with col1:
                owner_name = st.text_input("Owner/Representative Name", placeholder="Your full name")
            with col2:
                username = st.text_input("Username", placeholder="Choose a username")
                
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Business Email", placeholder="Enter business email")
            with col2:
                address = st.text_input("Business Address", placeholder="Full business address")
                
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            business_description = st.text_area("Business Description", placeholder="Tell people about your business", height=100)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                signup_btn = st.form_submit_button("Register Business", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True, 
                                     on_click=lambda: setattr(st.session_state, "auth_page", "login"))
            
            if signup_btn:
                if not all([business_name, owner_name, username, email, password, confirm_password, address]):
                    st.error("Please fill in all required fields")
                elif password != confirm_password:
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
                            "description": business_description,
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
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center;">
            <p>Already have an account?</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Login to Existing Account", use_container_width=True):
        st.session_state["auth_page"] = "login"
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== MAIN APP PAGES =====
def home_page():
    # Welcome banner
    st.markdown(render_welcome_banner(st.session_state['user']['full_name']), unsafe_allow_html=True)
    
    # User stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_card("5", "Circles Joined"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("3", "Events Attended"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("12", "Media Shared"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("28", "Connections"), unsafe_allow_html=True)
    
    # Activity feed
    st.markdown("## 📰 Your Activity Feed")
    tab1, tab2, tab3 = st.tabs(["Recent Activity", "Your Circles", "Upcoming Events"])
    
    with tab1:
        st.markdown("### Latest updates from your network")
        # Sample activity data
        activities = [
            {"user": "JaneDoe", "action": "posted a photo in NYC Photographers", "time": "2h ago", "type": "media"},
            {"user": "MikeT", "action": "created an event: Central Park Picnic", "time": "5h ago", "type": "event"},
            {"user": "CoffeeShop", "action": "offered a new promotion: 20% off for members", "time": "1d ago", "type": "promotion"},
            {"user": "Sarah", "action": "joined your Photography circle", "time": "1d ago", "type": "circle"},
            {"user": "TechGroup", "action": "posted about an upcoming hackathon", "time": "2d ago", "type": "post"}
        ]
        
        activity_html = ""
        for activity in activities:
            activity_html += render_activity_item(activity['user'], activity['action'], activity['time'])
        
        st.markdown(activity_html, unsafe_allow_html=True)
        
        if st.button("Load More Activities", use_container_width=True):
            st.info("Loading more activities...")
    
    with tab2:
        st.markdown("### Your Circle Communities")
        circles = [
            {"name": "NYC Photographers", "members": 45, "description": "Photography enthusiasts in New York", "new_posts": 3},
            {"name": "Food Lovers", "members": 120, "description": "Discovering the best food spots", "new_posts": 7},
            {"name": "Tech Enthusiasts", "members": 89, "description": "Discussing tech innovations", "new_posts": 2}
        ]
        
        for circle in circles:
            with st.expander(f"{circle['name']} • {circle['members']} members • {circle['new_posts']} new posts"):
                st.write(circle['description'])
                col1, col2 = st.columns(2)
                with col1:
                    st.button("View Circle", key=f"view_{circle['name']}", use_container_width=True)
                with col2:
                    st.button("Leave Circle", key=f"leave_{circle['name']}", use_container_width=True)
    
    with tab3:
        st.markdown("### Events You Might Like")
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "location": "Brooklyn Bridge", "circle": "NYC Photographers"},
            {"name": "Food Festival", "date": "Jun 20", "location": "Downtown", "circle": "Food Lovers"},
            {"name": "Tech Meetup", "date": "Jul 2", "location": "Innovation Center", "circle": "Tech Enthusiasts"}
        ]
        
        events_html = ""
        for event in events:
            events_html += render_event_card(event)
        
        st.markdown(events_html, unsafe_allow_html=True)
        
        if st.button("View All Events", use_container_width=True):
            st.session_state["page"] = "events"
            st.experimental_rerun()

def explore_page():
    st.markdown("## 🔍 Explore")
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search for circles, events, or locations", 
                                   placeholder="Try 'photography', 'New York', or 'food festival'")
    with col2:
        filter_type = st.selectbox("Filter By", ["All", "Circles", "Events", "Users", "Businesses"])
    
    if search_query:
        st.info(f"Searching for '{search_query}' in {filter_type.lower()}...")
    
    # Map view with modern styling
    st.markdown("## 📍 Discover Around You")
    st.markdown("""
    <div style="position: relative; border-radius: 10px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <img src="https://maps.googleapis.com/maps/api/staticmap?center=40.7128,-74.0060&zoom=12&size=1200x400&style=feature:water|color:0x4361ee&style=feature:road|color:0xffffff&style=element:labels|visibility:off&style=feature:poi|visibility:off&key=YOUR_API_KEY" style="width: 100%; border-radius: 10px;">
        <div style="position: absolute; top: 20px; left: 20px; background: rgba(255,255,255,0.9); padding: 10px 20px; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <span style="font-weight: bold; color: #4361ee;">New York City</span>
        </div>
        <div style="position: absolute; bottom: 20px; right: 20px; display: flex; gap: 10px;">
            <button style="background: white; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                <span style="font-size: 20px;">+</span>
            </button>
            <button style="background: white; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                <span style="font-size: 20px;">-</span>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 Popular Circles")
        circles = [
            {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC"},
            {"name": "Food Lovers", "members": 320, "description": "Discover and share great food spots"},
            {"name": "Tech Enthusiasts", "members": 189, "description": "Discuss the latest in technology"}
        ]
        
        circles_html = ""
        for circle in circles:
            circles_html += render_circle_card(circle)
        
        st.markdown(circles_html, unsafe_allow_html=True)
        
        if st.button("Discover More Circles", key="more_circles", use_container_width=True):
            st.session_state["page"] = "circles"
            st.experimental_rerun()
    
    with col2:
        st.markdown("### 📅 Trending Events")
        events = [
            {"name": "Central Park Picnic", "date": "Jun 15", "location": "Central Park", "circle": "NYC Photographers"},
            {"name": "Food Festival", "date": "Jun 20", "location": "Downtown", "circle": "Food Lovers"},
            {"name": "Tech Conference", "date": "Jul 2", "location": "Innovation Center", "circle": "Tech Enthusiasts"}
        ]
        
        events_html = ""
        for event in events:
            events_html += render_event_card(event)
        
        st.markdown(events_html, unsafe_allow_html=True)
        
        if st.button("See All Events", key="more_events", use_container_width=True):
            st.session_state["page"] = "events"
            st.experimental_rerun()
    
    # Trending hashtags
    st.markdown("### 🔥 Trending Hashtags")
    cols = st.columns(5)
    hashtags = ["#Photography", "#FoodFestNYC", "#TechTalks", "#SummerVibes", "#CentralPark"]
    for i, tag in enumerate(hashtags):
        with cols[i]:
            st.button(tag, use_container_width=True)

def media_page():
    st.markdown("## 📸 Capture & Share")
    
    tab1, tab2, tab3 = st.tabs(["Upload Media", "Your Gallery", "Discover"])
    
    with tab1:
        st.markdown("### Share Your Moments")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Camera capture with stylish container
            st.markdown("""
            <div style="border: 2px dashed #4361ee; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 20px;">
                <div style="color: #4361ee; font-size: 1.2rem; margin-bottom: 10px;">📸 Take a photo or upload</div>
            </div>
            """, unsafe_allow_html=True)
            captured_photo = st.camera_input("", label_visibility="collapsed")
            
            # Alternative upload
            uploaded_file = st.file_uploader("Or upload from your device", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        with col2:
            # Media details
            location = st.text_input("Location", "Central Park, NYC")
            
            # Circle selection
            circles = ["", "NYC Photographers", "Food Lovers", "Tech Enthusiasts", "Travel Enthusiasts"]
            selected_circle = st.selectbox("Share to Circle", circles)
            
            # Privacy
            privacy = st.radio("Privacy Setting", ["Public", "Circle Members Only", "Private"])
            
            # Tags
            tags = st.multiselect("Tags", ["Nature", "Food", "Tech", "Art", "Sports", "Travel", "Portrait", "Friends", "Family"])
            
            # Caption
            caption = st.text_area("Caption", placeholder="Write something about this moment...", height=100)
        
        # Upload button
        if st.button("Share Now", use_container_width=True, type="primary") and (captured_photo or uploaded_file):
            # Process media upload
            media_source = captured_photo if captured_photo else uploaded_file
            
            # Save media
            media_id = generate_id("med")
            filename = f"{st.session_state['user']['user_id']}_{media_id}.jpg"
            filepath = os.path.join(MEDIA_DIR, filename)
            
            image = Image.open(media_source)
            image.save(filepath)
            
            # Add to database
            media = load_db("media")
            media.append({
                "media_id": media_id,
                "user_id": st.session_state["user"]["user_id"],
                "file_path": filepath,
                "location": {"name": location},
                "caption": caption,
                "timestamp": datetime.now().isoformat(),
                "circle_id": selected_circle if selected_circle else None,
                "privacy": privacy.lower(),
                "tags": tags,
                "likes": 0,
                "reports": []
            })
            save_db("media", media)
            
            st.success("Media shared successfully!")
            
            # Check if this qualifies for any promotions
            promotions = load_db("promotions")
            for promo_id, promo in promotions.items():
                if any(tag.lower() in [t.lower() for t in tags] for tag in promo.get("tags", [])):
                    add_notification(st.session_state["user"]["user_id"], "promotion", 
                                    f"Your photo qualifies for {promo['offer']} from {promo_id}!")
    
    with tab2:
        st.markdown("### Your Media Gallery")
        # Display user's media
        media = load_db("media")
        user_media = [m for m in media if m["user_id"] == st.session_state["user"]["user_id"]]
        
        if not user_media:
            st.info("You haven't uploaded any media yet. Start sharing your moments!")
            if st.button("Upload Your First Photo", use_container_width=True):
                st.session_state["media_tab"] = "upload"
                st.experimental_rerun()
        else:
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Most Liked"])
            with col2:
                filter_circle = st.selectbox("Filter by Circle", ["All Circles", "NYC Photographers", "Food Lovers", "Tech Enthusiasts"])
            with col3:
                filter_tag = st.selectbox("Filter by Tag", ["All Tags"] + list(set([tag for media in user_media for tag in media.get("tags", [])])))
            
            # Gallery view
            st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 15px;'>", unsafe_allow_html=True)
            
            # Sort and filter user_media based on selections
            if sort_by == "Newest":
                user_media.sort(key=lambda x: x["timestamp"], reverse=True)
            elif sort_by == "Oldest":
                user_media.sort(key=lambda x: x["timestamp"])
            elif sort_by == "Most Liked":
                user_media.sort(key=lambda x: x.get("likes", 0), reverse=True)
            
            if filter_circle != "All Circles":
                user_media = [m for m in user_media if m.get("circle_id") == filter_circle]
            
            if filter_tag != "All Tags":
                user_media = [m for m in user_media if filter_tag in m.get("tags", [])]
            
            col_count = 3
            cols = st.columns(col_count)
            
            for i, item in enumerate(user_media):
                with cols[i % col_count]:
                    # Note: In a real application, you'd use a proper media display component
                    # This is simplified for the example
                    st.image(item["file_path"], use_column_width=True)
                    
                    # Caption and metadata
                    location_name = item["location"]["name"] if "location" in item and "name" in item["location"] else "Unknown location"
                    date_str = datetime.fromisoformat(item["timestamp"]).strftime('%b %d, %Y')
                    
                    st.markdown(f"""
                    <div style="padding: 5px 0;">
                        <div style="font-weight: 500;">{location_name} • {date_str}</div>
                        <div>Tags: {', '.join(item.get('tags', []))}</div>
                        <div style="display: flex; gap: 10px; margin-top: 5px;">
                            <span>❤️ {item.get('likes', 0)}</span>
                            <span>💬 {len(item.get('comments', []))}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("Edit", key=f"edit_{item['media_id']}", use_container_width=True)
                    with col2:
                        st.button("Delete", key=f"delete_{item['media_id']}", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Explore Photography")
        
        # Categories
        categories = ["All", "Nature", "Food", "People", "Travel", "Architecture", "Art", "Technology"]
        selected_category = st.selectbox("Category", categories)
        
        # Sample discover feed
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px;'>", unsafe_allow_html=True)
        
        # In a real app, these would be from the database filtered by category
        # Here we just show some placeholder images
        for i in range(9):
            st.markdown(f"""
            <div style="position: relative; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <img src="https://picsum.photos/seed/{i+1}/400/300" style="width: 100%; height: 200px; object-fit: cover;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.6); color: white; padding: 8px;">
                    <div style="font-weight: 500;">User{i+1}</div>
                    <div style="font-size: 0.8rem;">{["NYC", "Paris", "Tokyo", "London", "Sydney"][i % 5]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Load More", use_container_width=True):
            st.info("Loading more photos...")

def circles_page():
    st.markdown("## 👥 Circles")
    
    tab1, tab2, tab3 = st.tabs(["Your Circles", "Discover", "Create Circle"])
    
    with tab1:
        st.markdown("### Your Circle Communities")
        
        # Sample data - in real app would load from DB
        user_circles = [
            {
                "name": "NYC Photographers", 
                "members": 45, 
                "unread": 3, 
                "description": "For photography enthusiasts in NYC",
                "recent_posts": [
                    {"user": "JaneDoe", "content": "Great sunset shots at Brooklyn Bridge today!", "time": "2h ago"},
                    {"user": "MarkT", "content": "Anyone interested in a Central Park photowalk this Saturday?", "time": "5h ago"}
                ]
            },
            {
                "name": "Food Lovers", 
                "members": 120, 
                "unread": 7,
                "description": "Discovering and sharing great food spots",
                "recent_posts": [
                    {"user": "FoodieChef", "content": "Just tried that new Italian place downtown. Amazing pasta!", "time": "1h ago"},
                    {"user": "TasteHunter", "content": "Check out my review of the top 5 burger joints in the city", "time": "1d ago"}
                ]
            }
        ]
        
        # Display each circle with card styling
        for circle in user_circles:
            with st.expander(f"{circle['name']} • {circle['members']} members • {circle['unread']} new posts"):
                st.markdown(f"**About:** {circle['description']}")
                
                # Recent posts
                st.markdown("#### Recent Posts")
                
                for post in circle["recent_posts"]:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                        <div style="font-weight: 600;">{post['user']}</div>
                        <div>{post['content']}</div>
                        <div style="color: #777; font-size: 0.8rem; margin-top: 5px;">{post['time']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # New post form
                st.text_area("Write a post", placeholder="Share something with this circle...", key=f"post_{circle['name']}")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.button("Post", key=f"submit_post_{circle['name']}", use_container_width=True)
                with col2:
                    st.button("Add Media", key=f"add_media_{circle['name']}", use_container_width=True)
                with col3:
                    st.button("Circle Events", key=f"events_{circle['name']}", use_container_width=True)
    
    with tab2:
        st.markdown("### Discover New Circles")
        
        # Search and filters
        col1, col2 = st.columns([3, 1])
        with col1:
            search_circles = st.text_input("Search circles", placeholder="Try 'photography', 'food', 'tech'...")
        with col2:
            sort_by = st.selectbox("Sort by", ["Popular", "New", "Active"])
        
        # Sample circles
        circles = [
            {"name": "Tech Enthusiasts", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Gadgets", "Innovation"]},
            {"name": "Fitness Community", "members": 87, "description": "Share workout tips and meetups", "tags": ["Fitness", "Health", "Wellness"]},
            {"name": "Art Lovers", "members": 142, "description": "Appreciate and create art together", "tags": ["Art", "Creativity", "Museums"]},
            {"name": "Book Club", "members": 56, "description": "Discuss and recommend great reads", "tags": ["Books", "Reading", "Literature"]},
            {"name": "Travel Adventures", "members": 210, "description": "Share travel experiences and tips", "tags": ["Travel", "Adventure", "Photography"]}
        ]
        
        # Display circles in a grid layout
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;'>", unsafe_allow_html=True)
        
        for circle in circles:
            st.markdown(f"""
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 1.2rem; font-weight: 600; color: #3a0ca3; margin-bottom: 5px;">{circle['name']}</div>
                <div style="color: #555; margin-bottom: 10px;">👥 {circle['members']} members</div>
                <div style="margin-bottom: 10px;">{circle['description']}</div>
                <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                    {''.join([f'<span style="background: #f0f2f6; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem;">{tag}</span>' for tag in circle['tags']])}
                </div>
                <button style="background: #4361ee; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; width: 100%;">Join Circle</button>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Load more button
        if st.button("Discover More Circles", use_container_width=True):
            st.info("Loading more circles...")
    
    with tab3:
        st.markdown("### Create a New Circle")
        
        with st.form("create_circle"):
            # Circle details
            st.markdown("#### Basic Information")
            name = st.text_input("Circle Name", placeholder="Give your circle a catchy name")
            description = st.text_area("Description", placeholder="What's your circle about?", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                circle_type = st.radio("Privacy Type", ["Public", "Private"])
            with col2:
                location = st.text_input("Primary Location", placeholder="City, Country (optional)")
            
            # Additional settings
            st.markdown("#### Circle Settings")
            col1, col2 = st.columns(2)
            with col1:
                join_approval = st.checkbox("Require approval for new members")
            with col2:
                post_approval = st.checkbox("Require approval for posts")
            
            # Tags
            tags = st.multiselect("Tags (helps people find your circle)", 
                                ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography", "Books", "Movies", "Fashion", "Education"])
            
            # Cover image
            st.markdown("#### Circle Image")
            cover_image = st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
            
            # Submit
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Create Circle", use_container_width=True)
            with col2:
                cancel_button = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_button:
                if not name:
                    st.error("Please provide a name for your circle")
                else:
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
                        "join_approval": join_approval,
                        "post_approval": post_approval,
                        "tags": tags,
                        "created_at": datetime.now().isoformat()
                    }
                    save_db("circles", circles)
                    
                    # Save cover image if provided
                    if cover_image:
                        image_path = f"media_gallery/circle_{circle_id}_cover.jpg"
                        Image.open(cover_image).save(image_path)
                        circles[circle_id]["cover_image"] = image_path
                        save_db("circles", circles)
                    
                    st.success(f"Circle '{name}' created successfully!")
                    add_notification(st.session_state["user"]["user_id"], "circle", f"You created a new circle: {name}")

def events_page():
    st.markdown("## 📅 Events")
    
    tab1, tab2, tab3 = st.tabs(["Upcoming Events", "Your Events", "Create Event"])
    
    with tab1:
        st.markdown("### Discover Events Near You")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            date_filter = st.selectbox("When", ["Any time", "Today", "This weekend", "Next week", "Next month"])
        with col2:
            category_filter = st.selectbox("Category", ["All categories", "Photography", "Food", "Technology", "Arts", "Outdoors", "Sports"])
        with col3:
            location_filter = st.text_input("Location", "New York, NY")
        
        # Calendar view toggle
        view_type = st.radio("View", ["List", "Calendar"], horizontal=True)
        
        if view_type == "Calendar":
            # Simple calendar view
            st.markdown("""
            <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center; font-weight: 600; font-size: 1.2rem; margin-bottom: 15px;">June 2023</div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: 600; margin-bottom: 10px;">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); grid-gap: 5px;">
                    <div style="padding: 10px; text-align: center; color: #aaa;">28</div>
                    <div style="padding: 10px; text-align: center; color: #aaa;">29</div>
                    <div style="padding: 10px; text-align: center; color: #aaa;">30</div>
                    <div style="padding: 10px; text-align: center; color: #aaa;">31</div>
                    <div style="padding: 10px; text-align: center;">1</div>
                    <div style="padding: 10px; text-align: center;">2</div>
                    <div style="padding: 10px; text-align: center;">3</div>
                    
                    <div style="padding: 10px; text-align: center;">4</div>
                    <div style="padding: 10px; text-align: center;">5</div>
                    <div style="padding: 10px; text-align: center;">6</div>
                    <div style="padding: 10px; text-align: center;">7</div>
                    <div style="padding: 10px; text-align: center;">8</div>
                    <div style="padding: 10px; text-align: center;">9</div>
                    <div style="padding: 10px; text-align: center;">10</div>
                    
                    <div style="padding: 10px; text-align: center;">11</div>
                    <div style="padding: 10px; text-align: center;">12</div>
                    <div style="padding: 10px; text-align: center;">13</div>
                    <div style="padding: 10px; text-align: center;">14</div>
                    <div style="padding: 10px; text-align: center; background: #e6f7ff; border-radius: 50%; border: 2px solid #4361ee; color: #4361ee; font-weight: bold;">15</div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        16
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: #4cc9f0; border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center;">17</div>
                    
                    <div style="padding: 10px; text-align: center;">18</div>
                    <div style="padding: 10px; text-align: center;">19</div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        20
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: #f72585; border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center;">21</div>
                    <div style="padding: 10px; text-align: center;">22</div>
                    <div style="padding: 10px; text-align: center;">23</div>
                    <div style="padding: 10px; text-align: center;">24</div>
                    
                    <div style="padding: 10px; text-align: center;">25</div>
                    <div style="padding: 10px; text-align: center;">26</div>
                    <div style="padding: 10px; text-align: center;">27</div>
                    <div style="padding: 10px; text-align: center;">28</div>
                    <div style="padding: 10px; text-align: center;">29</div>
                    <div style="padding: 10px; text-align: center;">30</div>
                    <div style="padding: 10px; text-align: center; color: #aaa;">1</div>
                </div>
                <div style="margin-top: 15px;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 10px; height: 10px; background: #4361ee; border-radius: 50%; margin-right: 5px;"></div>
                        <div>Your events</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 10px; height: 10px; background: #4cc9f0; border-radius: 50%; margin-right: 5px;"></div>
                        <div>Circle events</div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background: #f72585; border-radius: 50%; margin-right: 5px;"></div>
                        <div>Popular events</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # List view
            # Sample events
            events = [
                {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "attendees": 18},
                {"name": "International Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown City Park", "circle": "Food Lovers", "attendees": 156},
                {"name": "Tech Innovation Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Tech Innovation Center", "circle": "Tech Enthusiasts", "attendees": 42},
                {"name": "Morning Yoga in the Park", "date": "Jun 18", "time": "8:00 AM", "location": "Central Park", "circle": "Fitness Community", "attendees": 25},
                {"name": "Art Gallery Opening", "date": "Jun 25", "time": "5:30 PM", "location": "Modern Art Space", "circle": "Art Lovers", "attendees": 67}
            ]
            
            for event in events:
                with st.expander(f"{event['name']} - {event['date']} at {event['time']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="margin-bottom: 15px;">
                            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 5px;">{event['name']}</div>
                            <div>📅 {event['date']} at {event['time']}</div>
                            <div>📍 {event['location']}</div>
                            <div>👥 Organized by {event['circle']}</div>
                            <div>👤 {event['attendees']} people attending</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.button("RSVP", key=f"rsvp_{event['name']}", use_container_width=True)
                        st.button("Details", key=f"details_{event['name']}", use_container_width=True)
                        st.button("Share", key=f"share_{event['name']}", use_container_width=True)
    
    with tab2:
        st.markdown("### Your Events")
        
        # Event categories
        options = st.radio("Filter", ["Attending", "Organized", "Past Events"], horizontal=True)
        
        if options == "Attending":
            # Sample user events
            user_events = [
                {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "status": "Confirmed", "role": "Attendee"},
                {"name": "Tech Book Club", "date": "Jun 22", "time": "7:00 PM", "status": "Pending", "role": "Attendee"}
            ]
            
            if not user_events:
                st.info("You're not attending any upcoming events yet. Explore events to join!")
            else:
                for event in user_events:
                    st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 5px;">{event['name']}</div>
                                <div style="color: #555;">📅 {event['date']} at {event['time']}</div>
                            </div>
                            <div style="background: {'#4cc9f0' if event['status'] == 'Confirmed' else '#f72585'}; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.8rem;">{event['status']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.button("View Details", key=f"view_{event['name']}", use_container_width=True)
                    with col2:
                        if event['status'] == 'Confirmed':
                            st.button("Cancel RSVP", key=f"cancel_{event['name']}", use_container_width=True)
                        else:
                            st.button("Confirm", key=f"confirm_{event['name']}", use_container_width=True)
                    with col3:
                        st.button("Add to Calendar", key=f"calendar_{event['name']}", use_container_width=True)
        
        elif options == "Organized":
            # Sample organized events
            organized_events = [
                {"name": "Photography Tips & Tricks", "date": "Jul 5", "time": "7:00 PM", "attendees": 12, "capacity": 25}
            ]
            
            if not organized_events:
                st.info("You haven't organized any events yet.")
                if st.button("Create Your First Event", use_container_width=True):
                    st.session_state["events_tab"] = "create"
                    st.experimental_rerun()
            else:
                for event in organized_events:
                    st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 5px;">{event['name']}</div>
                        <div style="color: #555;">📅 {event['date']} at {event['time']}</div>
                        <div style="margin-top: 10px; background: #f8f9fa; height: 10px; border-radius: 5px; overflow: hidden;">
                            <div style="background: #4361ee; height: 100%; width: {int(event['attendees']/event['capacity']*100)}%;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.9rem;">
                            <div>{event['attendees']} attending</div>
                            <div>{event['capacity']} capacity</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.button("Manage", key=f"manage_{event['name']}", use_container_width=True)
                    with col2:
                        st.button("Edit", key=f"edit_{event['name']}", use_container_width=True)
                    with col3:
                        st.button("Cancel Event", key=f"cancel_event_{event['name']}", use_container_width=True)
        
        else:  # Past Events
            # Sample past events
            past_events = [
                {"name": "City Photo Walk", "date": "May 20", "role": "Attendee"},
                {"name": "Cooking Class", "date": "May 5", "role": "Organizer"}
            ]
            
            if not past_events:
                st.info("You don't have any past events.")
            else:
                for event in past_events:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 5px;">{event['name']}</div>
                        <div style="color: #555;">
                            📅 {event['date']} • 
                            Role: {event['role']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("View", key=f"view_past_{event['name']}", use_container_width=True)
                    with col2:
                        st.button("Media", key=f"media_past_{event['name']}", use_container_width=True)
    
    with tab3:
        st.markdown("### Create New Event")
        with st.form("create_event"):
            # Basic information
            st.markdown("#### Event Details")
            name = st.text_input("Event Name", placeholder="Give your event a clear, descriptive name")
            description = st.text_area("Description", placeholder="What's your event about? Include all important details.", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date")
            with col2:
                time = st.time_input("Time")
            
            location = st.text_input("Location", placeholder="Where will this event take place?")
            
            # Additional details
            st.markdown("#### Additional Information")
            col1, col2 = st.columns(2)
            with col1:
                circle = st.selectbox("Associated Circle", ["", "NYC Photographers", "Food Lovers", "Tech Enthusiasts"])
            with col2:
                capacity = st.number_input("Capacity (0 for unlimited)", min_value=0, value=20)
            
            col1, col2 = st.columns(2)
            with col1:
                event_type = st.radio("Event Type", ["In-person", "Online", "Hybrid"])
            with col2:
                visibility = st.radio("Visibility", ["Public", "Circle Members Only", "Invite Only"])
            
            # Tags
            tags = st.multiselect("Tags (helps people find your event)", 
                                ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography"])
            
            # Cover image
            cover_image = st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
            
            # Submit
            col1, col2 = st.columns(2)
            with col1:
                submit_btn = st.form_submit_button("Create Event", use_container_width=True)
            with col2:
                cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_btn:
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
                    "event_type": event_type.lower(),
                    "visibility": visibility.lower(),
                    "tags": tags,
                    "attendees": [st.session_state["user"]["user_id"]],
                    "created_at": datetime.now().isoformat()
                }
                save_db("events", events)
                
                # Save cover image if provided
                if cover_image:
                    image_path = f"media_gallery/event_{event_id}_cover.jpg"
                    Image.open(cover_image).save(image_path)
                    events[event_id]["cover_image"] = image_path
                    save_db("events", events)
                
                st.success(f"Event '{name}' created successfully!")
                
                # Notify circle members if associated with a circle
                if circle:
                    add_notification(st.session_state["user"]["user_id"], "event", 
                                   f"New event in {circle}: {name}")

def business_page():
    if st.session_state["user"].get("account_type") != "business":
        st.warning("This page is only available for business accounts. Please sign up for a business account to access these features.")
        if st.button("Create a Business Account"):
            st.session_state["logged_in"] = False
            st.session_state["auth_page"] = "signup"
            st.experimental_rerun()
        return
    
    st.markdown("## 💼 Business Dashboard")
    
    # Business overview header
    business_info = st.session_state.get("business", {})
    business_name = business_info.get("business_name", "Your Business")
    business_category = business_info.get("category", "")
    
    st.markdown(f"""
    <div style="background-image: linear-gradient(135deg, #4361ee, #3a0ca3); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 10px;">{business_name}</div>
        <div style="font-size: 1rem; opacity: 0.9;">{business_category}</div>
        <div style="background: rgba(255,255,255,0.2); height: 1px; margin: 15px 0;"></div>
        <div style="display: flex; justify-content: space-between;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">245</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Followers</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">56</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Media Mentions</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">3</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Active Promos</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">82%</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Positive Rating</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Promotions", "Analytics", "Settings"])
    
    with tab1:
        # Quick actions row
        st.markdown("### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Create Promotion", use_container_width=True)
        with col2:
            st.button("Post Update", use_container_width=True)
        with col3:
            st.button("Create Event", use_container_width=True)
        with col4:
            st.button("Contact Followers", use_container_width=True)
        
        # Activity and engagement
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### Recent Activity")
            
            activities = [
                {"user": "JaneDoe", "action": "mentioned your business in a post", "time": "2h ago"},
                {"user": "PhotoLover", "action": "used your promotion code", "time": "5h ago"},
                {"user": "MikeT", "action": "tagged your business in a photo", "time": "1d ago"},
                {"user": "FoodieClub", "action": "added your business to their recommended list", "time": "2d ago"}
            ]
            
            activity_html = ""
            for activity in activities:
                activity_html += render_activity_item(activity['user'], activity['action'], activity['time'])
            
            st.markdown(activity_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Engagement Summary")
            
            # Engagement metrics
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-weight: 600; margin-bottom: 10px;">Last 7 Days</div>
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Profile Views</div>
                        <div style="font-weight: 600;">127</div>
                    </div>
                    <div style="background: #f0f2f6; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 75%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Media Tags</div>
                        <div style="font-weight: 600;">23</div>
                    </div>
                    <div style="background: #f0f2f6; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 40%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>New Followers</div>
                        <div style="font-weight: 600;">18</div>
                    </div>
                    <div style="background: #f0f2f6; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 30%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Promotion Claims</div>
                        <div style="font-weight: 600;">12</div>
                    </div>
                    <div style="background: #f0f2f6; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 25%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Business Circle
        st.markdown("### Your Business Circle")
        if not business_info.get("has_circle", False):
            st.info("You don't have a business circle yet. Create one to engage directly with your customers.")
            if st.button("Create Business Circle", use_container_width=True):
                st.session_state["page"] = "circles"
                st.session_state["circles_tab"] = "create"
                st.experimental_rerun()
        else:
            st.write("Your business circle has 86 members")
            st.button("Manage Circle", use_container_width=True)
        
        # Media mentions
        st.markdown("### Media Mentions")
        st.write("Recent photos and posts that mention your business")
        
        # Grid of media
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;'>", unsafe_allow_html=True)
        
        for i in range(6):
            st.markdown(f"""
            <div style="position: relative; border-radius: 8px; overflow: hidden; height: 150px;">
                <img src="https://picsum.photos/seed/{i+100}/300/200" style="width: 100%; height: 100%; object-fit: cover;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.6); color: white; padding: 8px;">
                    <div style="font-size: 0.8rem;">@user{i+1}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Manage Promotions")
        st.markdown("Create and track special offers for your followers")
        
        # Existing promotions
        st.markdown("#### Active Promotions")
        
        # Sample promotions
        promotions = [
            {"name": "Summer Special", "offer": "20% off all items", "claimed": 12, "expires": "Jul 15, 2023"},
            {"name": "Photo Contest", "offer": "Free item for best photo", "claimed": 8, "expires": "Jun 30, 2023"}
        ]
        
        if promotions:
            for promo in promotions:
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #3a0ca3;">{promo['name']}</div>
                            <div style="color: #555; margin-bottom: 10px;">{promo['offer']} • Expires: {promo['expires']}</div>
                            <div style="color: #4361ee; font-weight: 500;">{promo['claimed']} users claimed</div>
                        </div>
                        <div>
                            <button style="background: white; border: 1px solid #4361ee; color: #4361ee; padding: 5px 15px; border-radius: 20px; margin-right: 5px;">Edit</button>
                            <button style="background: white; border: 1px solid #f72585; color: #f72585; padding: 5px 15px; border-radius: 20px;">End</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You don't have any active promotions")
        
        # Create promotion form
        st.markdown("#### Create New Promotion")
        with st.form("create_promotion"):
            col1, col2 = st.columns(2)
            with col1:
                promo_name = st.text_input("Promotion Name", placeholder="Summer Special, New Customer Discount, etc.")
            with col2:
                offer_type = st.selectbox("Offer Type", ["Percentage Discount", "Fixed Amount Off", "Free Item", "Buy One Get One", "Custom"])
            
            if offer_type == "Percentage Discount":
                col1, col2 = st.columns(2)
                with col1:
                    discount_percent = st.number_input("Discount Percentage", min_value=1, max_value=100, value=20)
                with col2:
                    min_purchase = st.number_input("Minimum Purchase ($)", min_value=0.0, value=0.0, step=5.0)
                
                offer_text = f"{discount_percent}% off"
                if min_purchase > 0:
                    offer_text += f" on purchases over ${min_purchase:.2f}"
            else:
                offer_text = st.text_input("Offer Details", placeholder="Describe your offer...")
            
            requirements = st.text_input("Requirements", placeholder="Post with #YourBusiness, Tag in a photo, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
            
            tags = st.multiselect("Relevant Tags", ["Food", "Drink", "Retail", "Sale", "Summer", "Holiday", "Special"])
            
            col1, col2 = st.columns(2)
            with col1:
                submit_btn = st.form_submit_button("Launch Promotion", use_container_width=True)
            with col2:
                cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_btn:
                promo_id = generate_id("promo")
                promotions = load_db("promotions")
                promotions[promo_id] = {
                    "promo_id": promo_id,
                    "business_id": st.session_state["user"]["user_id"],
                    "name": promo_name,
                    "offer": offer_text,
                    "requirements": requirements,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "tags": tags,
                    "created_at": datetime.now().isoformat()
                }
                save_db("promotions", promotions)
                st.success("Promotion launched successfully!")
    
    with tab3:
        st.markdown("### Business Analytics")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days", "This year", "Custom range"])
        with col2:
            if date_range == "Custom range":
                start_date = st.date_input("From")
                end_date = st.date_input("To")
        
        # Key metrics
        st.markdown("#### Key Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card("1,247", "Profile Views"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_metric_card("287", "Media Tags"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_metric_card("56", "Promotion Claims"), unsafe_allow_html=True)

        with col4:
            st.markdown(render_metric_card("32", "New Followers"), unsafe_allow_html=True)
        
        # Visual charts
        st.markdown("#### Engagement Over Time")
        
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <div style="height: 250px; position: relative;">
                <!-- Simulated chart - in a real app, this would be an actual chart -->
                <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 200px; display: flex; align-items: flex-end;">
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 30%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 45%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 60%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 40%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 70%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 85%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: #4361ee; height: 65%;"></div>
                </div>
                <div style="position: absolute; bottom: -25px; left: 0; right: 0; display: flex; justify-content: space-between; padding: 0 10px;">
                    <div style="font-size: 0.8rem; color: #555;">Mon</div>
                    <div style="font-size: 0.8rem; color: #555;">Tue</div>
                    <div style="font-size: 0.8rem; color: #555;">Wed</div>
                    <div style="font-size: 0.8rem; color: #555;">Thu</div>
                    <div style="font-size: 0.8rem; color: #555;">Fri</div>
                    <div style="font-size: 0.8rem; color: #555;">Sat</div>
                    <div style="font-size: 0.8rem; color: #555;">Sun</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Demographic data
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### User Demographics")
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="margin-bottom: 15px;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Age Groups</div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">18-24</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 25%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">25%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">25-34</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 40%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">40%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">35-44</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 20%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">20%</div>
                    </div>
                    <div style="display: flex;">
                        <div style="width: 80px;">45+</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 15%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">15%</div>
                    </div>
                </div>
                
                <div>
                    <div style="font-weight: 500; margin-bottom: 5px;">Gender</div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">Female</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 58%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">58%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">Male</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 39%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">39%</div>
                    </div>
                    <div style="display: flex;">
                        <div style="width: 80px;">Other</div>
                        <div style="flex-grow: 1;">
                            <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                                <div style="background: #4361ee; height: 100%; width: 3%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">3%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Top Locations")
            st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">New York, NY</div>
                        <div>45%</div>
                    </div>
                    <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 45%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Brooklyn, NY</div>
                        <div>25%</div>
                    </div>
                    <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 25%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Queens, NY</div>
                        <div>15%</div>
                    </div>
                    <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 15%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Other</div>
                        <div>15%</div>
                    </div>
                    <div style="background: #f0f2f6; height: 15px; border-radius: 7px; overflow: hidden;">
                        <div style="background: #4361ee; height: 100%; width: 15%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export options
        st.markdown("#### Data Export")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Export as CSV", use_container_width=True)
        with col2:
            st.button("Export as PDF", use_container_width=True)
        with col3:
            st.button("Schedule Reports", use_container_width=True)
    
    with tab4:
        st.markdown("### Business Settings")
        
        # Profile settings
        st.markdown("#### Business Profile")
        with st.form("business_profile"):
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business Name", value=business_info.get("business_name", ""))
            with col2:
                category = st.selectbox("Business Category", 
                                      ["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"],
                                      index=["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"].index(business_info.get("category", "Other")))
            
            description = st.text_area("Business Description", value=business_info.get("description", ""), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_input("Primary Address", value=business_info.get("locations", [{}])[0].get("address", ""))
            with col2:
                website = st.text_input("Website", value=business_info.get("website", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Business Phone", value=business_info.get("phone", ""))
            with col2:
                email = st.text_input("Business Email", value=business_info.get("email", ""))
            
            business_hours = st.text_area("Business Hours", value=business_info.get("hours", ""), height=100, 
                                        placeholder="Monday: 9am-5pm\nTuesday: 9am-5pm\netc.")
            
            # Logo and cover image
            st.markdown("#### Business Images")
            col1, col2 = st.columns(2)
            with col1:
                logo = st.file_uploader("Business Logo", type=["png", "jpg", "jpeg"])
            with col2:
                cover = st.file_uploader("Cover Image", type=["png", "jpg", "jpeg"])
            
            st.markdown("#### Social Media Links")
            col1, col2 = st.columns(2)
            with col1:
                instagram = st.text_input("Instagram", value=business_info.get("social", {}).get("instagram", ""))
            with col2:
                facebook = st.text_input("Facebook", value=business_info.get("social", {}).get("facebook", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                twitter = st.text_input("Twitter", value=business_info.get("social", {}).get("twitter", ""))
            with col2:
                linkedin = st.text_input("LinkedIn", value=business_info.get("social", {}).get("linkedin", ""))
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Save Changes", use_container_width=True)
            with col2:
                cancel_button = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_button:
                # Update business info
                businesses = load_db("businesses")
                business_id = business_info.get("business_id")
                
                if business_id and business_id in businesses:
                    businesses[business_id].update({
                        "business_name": business_name,
                        "category": category,
                        "description": description,
                        "locations": [{"address": address}],
                        "website": website,
                        "phone": phone,
                        "email": email,
                        "hours": business_hours,
                        "social": {
                            "instagram": instagram,
                            "facebook": facebook,
                            "twitter": twitter,
                            "linkedin": linkedin
                        }
                    })
                    
                    # Save images if provided
                    if logo:
                        logo_path = f"media_gallery/business_{business_id}_logo.jpg"
                        Image.open(logo).save(logo_path)
                        businesses[business_id]["logo"] = logo_path
                    
                    if cover:
                        cover_path = f"media_gallery/business_{business_id}_cover.jpg"
                        Image.open(cover).save(cover_path)
                        businesses[business_id]["cover_image"] = cover_path
                    
                    save_db("businesses", businesses)
                    st.session_state["business"] = businesses[business_id]
                    st.success("Business profile updated successfully!")
        
        # Verification status
        st.markdown("#### Business Verification")
        if business_info.get("verified", False):
            st.success("✓ Your business is verified!")
            st.markdown("""
            Verified businesses get:
            - Higher visibility in search results
            - A verification badge on your profile
            - Access to premium analytics
            - Ability to run advanced promotions
            """)
        else:
            st.warning("⚠️ Your business is not yet verified")
            st.markdown("""
            Get verified to unlock premium features and build trust with users. 
            To complete verification, please provide the following documents:
            """)
            
            with st.form("verification_form"):
                business_license = st.file_uploader("Business License or Registration")
                id_proof = st.file_uploader("ID Proof of Owner/Representative")
                proof_of_address = st.file_uploader("Proof of Business Address")
                website = st.text_input("Business Website")
                additional_info = st.text_area("Additional Information", height=100)
                
                st.form_submit_button("Submit for Verification", use_container_width=True)

def settings_page():
    st.markdown("## ⚙️ Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Account", "Notifications", "Privacy", "Support"])
    
    with tab1:
        st.markdown("### Account Settings")
        
        # Profile picture
        col1, col2 = st.columns([1, 3])
        with col1:
            # Display user avatar
            user_name = st.session_state["user"].get("full_name", "User")
            avatar_data = create_user_avatar(user_name)
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="data:image/png;base64,{avatar_data}" class="profile-pic" style="width: 100px; height: 100px;">
                <button style="margin-top: 10px; background: transparent; border: none; color: #4361ee; font-size: 0.9rem;">Change</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.form("account_settings"):
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("Full Name", value=st.session_state["user"].get("full_name", ""))
                with col2:
                    username = st.text_input("Username", value=[k for k, v in load_db("users").items() if v["user_id"] == st.session_state["user"]["user_id"]][0] if "user_id" in st.session_state["user"] else "", disabled=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    email = st.text_input("Email", value=st.session_state["user"].get("email", ""))
                with col2:
                    location = st.text_input("Location", value=st.session_state["user"].get("location", {}).get("city", ""))
                
                interests = st.multiselect("Interests", 
                                        ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography", "Books", "Movies"],
                                        default=st.session_state["user"].get("interests", []))
                
                biography = st.text_area("Bio", height=100, value=st.session_state["user"].get("bio", ""), 
                                      placeholder="Tell others about yourself...")
                
                col1, col2 = st.columns(2)
                with col1:
                    update_btn = st.form_submit_button("Update Profile", use_container_width=True)
                with col2:
                    cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
                
                if update_btn:
                    users = load_db("users")
                    username_key = [k for k, v in users.items() if v["user_id"] == st.session_state["user"]["user_id"]][0]
                    
                    users[username_key].update({
                        "full_name": full_name,
                        "email": email,
                        "location": {"city": location},
                        "interests": interests,
                        "bio": biography
                    })
                    
                    save_db("users", users)
                    st.session_state["user"] = users[username_key]
                    st.success("Profile updated successfully!")
        
        # Password and security
        st.markdown("### Password & Security")
        with st.form("security_form"):
            current_password = st.text_input("Current Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input("New Password", type="password")
            with col2:
                confirm_password = st.text_input("Confirm New Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_btn = st.form_submit_button("Update Password", use_container_width=True)
            
            if submit_btn:
                if not current_password:
                    st.error("Please enter your current password")
                elif not new_password or not confirm_password:
                    st.error("Please enter and confirm your new password")
                elif new_password != confirm_password:
                    st.error("New passwords don't match")
                else:
                    # Verify current password and update
                    users = load_db("users")
                    username_key = [k for k, v in users.items() if v["user_id"] == st.session_state["user"]["user_id"]][0]
                    
                    if verify_password(current_password, users[username_key]["password"]):
                        users[username_key]["password"] = hash_password(new_password)
                        save_db("users", users)
                        st.success("Password updated successfully!")
                    else:
                        st.error("Current password is incorrect")
        
        # Account management
        st.markdown("### Account Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download My Data", use_container_width=True):
                st.info("Your data is being prepared for download. This may take a few minutes.")
        with col2:
            if st.button("Delete Account", use_container_width=True):
                st.warning("⚠️ This action cannot be undone. All your data will be permanently deleted.")
                confirm_delete = st.checkbox("I understand the consequences")
                if confirm_delete:
                    if st.button("Confirm Delete"):
                        st.error("Account marked for deletion. You will be logged out in 5 seconds.")
                        # In a real app, would handle account deletion process
    
    with tab2:
        st.markdown("### Notification Settings")
        
        # Email notifications
        st.markdown("#### Email Notifications")
        col1, col2 = st.columns(2)
        with col1:
            email_circle = st.checkbox("Circle updates", value=True)
            email_events = st.checkbox("Event reminders", value=True)
            email_followers = st.checkbox("New followers", value=True)
        with col2:
            email_promos = st.checkbox("Promotions and offers", value=True)
            email_mentions = st.checkbox("Media mentions", value=True)
            email_newsletter = st.checkbox("Newsletter", value=False)
        
        # Push notifications
        st.markdown("#### Push Notifications")
        col1, col2 = st.columns(2)
        with col1:
            push_circle = st.checkbox("Circle activity", value=True)
            push_events = st.checkbox("Event notifications", value=True)
            push_followers = st.checkbox("New followers", value=True)
        with col2:
            push_promos = st.checkbox("Promotion alerts", value=True)
            push_mentions = st.checkbox("Media mentions", value=True)
            push_messages = st.checkbox("Direct messages", value=True)
        
        # Notification schedule
        st.markdown("#### Notification Schedule")
        quiet_hours = st.checkbox("Enable quiet hours")
        if quiet_hours:
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.time_input("Start time", value=datetime.strptime("22:00", "%H:%M").time())
            with col2:
                end_time = st.time_input("End time", value=datetime.strptime("07:00", "%H:%M").time())
        
        if st.button("Save Notification Preferences", use_container_width=True):
            # In a real app, would save these preferences to the user's profile
            st.success("Notification preferences saved!")
    
    with tab3:
        st.markdown("### Privacy Settings")
        
        # Profile privacy
        st.markdown("#### Profile Visibility")
        profile_visibility = st.radio("Who can see my profile", ["Everyone", "Circle Members Only", "Followers Only"])
        
        # Content privacy
        st.markdown("#### Content Privacy")
        col1, col2 = st.columns(2)
        with col1:
            location_share = st.checkbox("Share my location with posts", value=True)
            media_visibility = st.radio("Media visibility", ["Public", "Circle Members", "Followers Only"])
        with col2:
            circle_visibility = st.radio("My circles visibility", ["Public", "Followers Only", "Private"])
            event_visibility = st.radio("Event attendance visibility", ["Public", "Circle Members", "Private"])
        
        # Data sharing
        st.markdown("#### Data Usage")
        col1, col2 = st.columns(2)
        with col1:
            personalization = st.checkbox("Personalize my experience based on activity", value=True)
            recommendations = st.checkbox("Show personalized recommendations", value=True)
        with col2:
            third_party = st.checkbox("Allow third-party services", value=False)
            analytics = st.checkbox("Contribute to anonymous analytics", value=True)
        
        if st.button("Save Privacy Settings", use_container_width=True):
            # In a real app, would save these preferences to the user's profile
            st.success("Privacy settings updated!")
    
    with tab4:
        st.markdown("### Help & Support")
        
        # Report issues
        st.markdown("#### Report a Problem")
        with st.form("report_issue"):
            issue_type = st.selectbox("Issue Type", 
                                    ["Bug Report", "Feature Request", "Account Issue", "Content Moderation", "Other"])
            
            issue_description = st.text_area("Describe the issue", height=150, 
                                         placeholder="Please provide details about the issue you're experiencing...")
            
            severity = st.slider("How severely does this affect your experience?", 1, 5, 3)
            
            include_logs = st.checkbox("Include app logs to help troubleshooting", value=True)
            
            file_upload = st.file_uploader("Attach screenshots or relevant files", type=["jpg", "jpeg", "png", "pdf"])
            
            submit_btn = st.form_submit_button("Submit Report", use_container_width=True)
            
            if submit_btn:
                if not issue_description:
                    st.error("Please describe the issue")
                else:
                    st.success("Your report has been submitted. Our team will review it as soon as possible.")
        
        # Report content
        st.markdown("#### Report Content")
        with st.form("report_content"):
            content_type = st.selectbox("Content Type", ["Media", "Circle", "Event", "User Profile", "Comment"])
            content_id = st.text_input("Content URL or ID", placeholder="Paste the URL or ID of the content")
            reason = st.selectbox("Reason", 
                               ["Inappropriate content", "Spam", "Misinformation", "Harassment", "Hate speech", "Other"])
            details = st.text_area("Additional Details", height=100, 
                                 placeholder="Please provide more information about the issue...")
            
            submit_btn = st.form_submit_button("Submit Report", use_container_width=True)
            
            if submit_btn:
                if not content_id:
                    st.error("Please provide the URL or ID of the content")
                else:
                    report_id = generate_id("rep")
                    reports = load_db("reports")
                    reports.append({
                        "report_id": report_id,
                        "reporter_id": st.session_state["user"]["user_id"],
                        "content_type": content_type.lower(),
                        "content_id": content_id,
                        "reason": reason,
                        "details": details,
                        "status": "pending",
                        "timestamp": datetime.now().isoformat()
                    })
                    save_db("reports", reports)
                    st.success("Report submitted. Our team will review it shortly.")
        
        # FAQ and help resources
        st.markdown("#### Frequently Asked Questions")
        with st.expander("How do I create a Circle?"):
            st.write("""
            To create a Circle:
            1. Navigate to the Circles page
            2. Click on the "Create Circle" tab
            3. Fill in the Circle details including name, description, and settings
            4. Click "Create Circle" to finalize
            
            Your new Circle will be created immediately, and you can start inviting members.
            """)
        
        with st.expander("How do promotions work?"):
            st.write("""
            Promotions allow businesses to offer special deals to Atmosphere users:
            1. Businesses create promotional offers with specific requirements
            2. Users complete the requirements (like posting photos with specific tags)
            3. Users receive the promotion in their notification feed
            4. Users can claim the promotion at the business location
            
            Requirements vary by promotion, so check the details of each offer.
            """)
        
        with st.expander("How can I change my privacy settings?"):
            st.write("""
            You can manage your privacy settings at any time:
            1. Go to Settings > Privacy
            2. Adjust your profile visibility, content privacy, and data sharing preferences
            3. Save your changes
            
            Changes to privacy settings take effect immediately.
            """)
        
        # Contact support
        st.markdown("#### Contact Support")
        st.info("Our support team is available 24/7 to help you with any issues or questions.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Email Support", use_container_width=True)
        with col2:
            st.button("Live Chat", use_container_width=True)

# ===== NOTIFICATION BELL =====
def notification_bell():
    notifications = load_db("notifications").get(st.session_state["user"]["user_id"], [])
    unread = sum(1 for n in notifications if not n.get("read", False))
    
    with st.sidebar:
        # Notification bell with badge
        if unread > 0:
            notification_button = st.button(f"🔔 Notifications ({unread})", use_container_width=True)
        else:
            notification_button = st.button("🔔 Notifications", use_container_width=True)
        
        if notification_button:
            if "show_notifications" in st.session_state and st.session_state["show_notifications"]:
                st.session_state["show_notifications"] = False
            else:
                st.session_state["show_notifications"] = True
        
        # Display notifications if toggled
        if st.session_state.get("show_notifications"):
            st.markdown("""
            <div style="background: white; padding: 10px; border-radius: 10px; margin-top: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-weight: 600;margin-bottom: 10px;">Recent Notifications</div>
            """, unsafe_allow_html=True)
            
            if not notifications:
                st.markdown("""
                <div style="padding: 10px; text-align: center; color: #777;">
                    You don't have any notifications yet
                </div>
                """, unsafe_allow_html=True)
            else:
                # Sort notifications by timestamp, newest first
                sorted_notifications = sorted(notifications, key=lambda x: x.get("timestamp", ""), reverse=True)
                
                # Display 5 most recent notifications
                for note in sorted_notifications[:5]:
                    # Format timestamp
                    timestamp = datetime.fromisoformat(note["timestamp"]) if "timestamp" in note else datetime.now()
                    time_str = timestamp.strftime('%b %d %H:%M')
                    
                    # Get notification type icon
                    type_icon = "🔔"  # Default
                    if note.get("type") == "event_reminder":
                        type_icon = "📅"
                    elif note.get("type") == "circle":
                        type_icon = "👥"
                    elif note.get("type") == "promotion":
                        type_icon = "🎁"
                    elif note.get("type") == "login":
                        type_icon = "🔐"
                    
                    # Render notification
                    st.markdown(f"""
                    <div style="background: {'#f8f9fa' if note.get('read', False) else '#e6f7ff'}; padding: 10px; border-radius: 8px; margin-bottom: 10px; cursor: pointer;">
                        <div style="display: flex; align-items: start;">
                            <div style="font-size: 1.2rem; margin-right: 10px;">{type_icon}</div>
                            <div style="flex-grow: 1;">
                                <div style="margin-bottom: 5px;">{note.get('content', '')}</div>
                                <div style="color: #777; font-size: 0.8rem;">{time_str}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Mark all as read and view all buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark all read", use_container_width=True):
                    # Mark all notifications as read
                    notifications_db = load_db("notifications")
                    if st.session_state["user"]["user_id"] in notifications_db:
                        for note in notifications_db[st.session_state["user"]["user_id"]]:
                            note["read"] = True
                        save_db("notifications", notifications_db)
                        st.experimental_rerun()
            with col2:
                if st.button("View all", use_container_width=True):
                    # View all notifications
                    st.session_state["page"] = "notifications"
                    st.experimental_rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ===== MAIN APP FLOW =====
def main():
    # Initialize session state variables if they don't exist
    if "show_notifications" not in st.session_state:
        st.session_state["show_notifications"] = False
    
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"
    
    # Sidebar navigation
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="logo-container">
            <div class="logo">🌍 Atmosphere</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if "logged_in" in st.session_state:
            # User info
            user_name = st.session_state['user']['full_name']
            avatar_data = create_user_avatar(user_name)
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <img src="data:image/png;base64,{avatar_data}" class="profile-pic" style="width: 40px; height: 40px; margin-right: 10px;">
                <div>
                    <div style="font-weight: 600; color: white;">{user_name}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">@{st.session_state['user'].get('email', '').split('@')[0]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
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
            
            # Check if page is stored in session state
            if "page" not in st.session_state:
                st.session_state["page"] = "🏠 Home"
            
            selected_page = st.radio("", list(pages.keys()), 
                                    index=list(pages.keys()).index(st.session_state["page"]) if st.session_state["page"] in pages else 0,
                                    label_visibility="collapsed")
            
            # Update page in session state
            st.session_state["page"] = selected_page
            
            # Notification bell
            notification_bell()
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        else:
            # Welcome message for non-logged in users
            st.markdown("""
            <div style="color: white; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 10px;">Welcome to Atmosphere</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Connect with your community</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Login/Signup buttons
            if st.button("Login", use_container_width=True):
                st.session_state["auth_page"] = "login"
                st.experimental_rerun()
            
            if st.button("Sign Up", use_container_width=True):
                st.session_state["auth_page"] = "signup"
                st.experimental_rerun()
    
    # Main content area
    if "logged_in" in st.session_state:
        # Call the appropriate page function
        pages[selected_page]()
    else:
        if st.session_state["auth_page"] == "login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()
                
                        
