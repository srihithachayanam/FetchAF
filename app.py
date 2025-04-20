import streamlit as st
import hashlib

# Initialize session state for user data and login status
if 'users' not in st.session_state:
    st.session_state.users = {}  # Store username: hashed_password
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Hide Streamlit's default sidebar for login/signup and welcome pages
st.set_page_config(page_title="FetchAF", layout="wide")
st.markdown(
    """
    <style>
    /* Hide default sidebar */
    [data-testid="stSidebar"] {display: none;}
    
    /* Modern minimalist color palette */
    :root {
        --primary-green: #2ecc71;
        --dark-green: #27ae60;
        --light-green: rgba(46, 204, 113, 0.1);
        --accent-green: #46cb8c;
        --bg-dark: #1e1e2e;
        --bg-card: #2a2a3a;
        --text-white: #f8f9fa;
        --text-light: #bdc3c7;
        --text-accent: #ecf0f1;
        --shadow: rgba(0, 0, 0, 0.2);
    }
    
    /* Dark background */
    .main .block-container {
        background: var(--bg-dark);
        color: var(--text-white);
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Modern typography with white text */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: var(--primary-green);
    }
    
    h2, h3 {
        font-weight: 600;
        color: var(--primary-green);
    }
    
    p, li {
        font-weight: 400;
        color: var(--text-white);
        line-height: 1.6;
    }
    
    /* Clean buttons */
    button, .stButton>button {
        background-color: var(--primary-green) !important;
        color: var(--bg-dark) !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px var(--shadow) !important;
    }
    
    button:hover, .stButton>button:hover {
        background-color: var(--dark-green) !important;
        box-shadow: 0 4px 10px rgba(46, 204, 113, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Minimal input fields */
    input[type="text"], input[type="password"], .stTextInput>div>div>input {
        border: 1px solid #4a4a5a !important;
        border-radius: 8px !important;
        padding: 0.8rem 1rem !important;
        background-color: #2a2a3a !important;
        color: var(--text-white) !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    input[type="text"]:focus, input[type="password"]:focus, .stTextInput>div>div>input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.15) !important;
    }
    
    /* Modern tab interface */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #4a4a5a;
        padding-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        color: var(--text-light) !important;
        font-weight: 500;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-green) !important;
        border-bottom: 2px solid var(--primary-green) !important;
        background-color: transparent !important;
    }
    
    /* Status messages */
    .element-container div[data-testid="stImage"] {
        background-color: transparent;
        padding: 0;
        border-radius: 8px;
        color: var(--text-white);
    }
    
    /* Clean cards */
    .card {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #3a3a4a;
        box-shadow: 0 4px 20px var(--shadow);
        transition: transform 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow);
    }
    
    /* Feature list styling */
    .feature-list {
        padding-left: 0;
    }
    
    .feature-list li {
        margin-bottom: 12px;
        list-style-type: none;
        position: relative;
        padding-left: 28px;
        color: var(--text-white);
    }
    
    .feature-list li:before {
        content: "✓";
        color: var(--primary-green);
        font-weight: bold;
        position: absolute;
        left: 0;
        font-size: 16px;
    }
    
    /* Links styling */
    a {
        color: var(--primary-green);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: var(--accent-green);
    }
    
    /* Modern footer */
    .app-footer {
        text-align: center;
        margin-top: 3rem;
        color: var(--text-light);
        font-size: 0.85rem;
        padding-top: 1.5rem;
        border-top: 1px solid #3a3a4a;
    }
    
    /* Logo styling */
    .logo {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-green);
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .logo-accent {
        color: var(--text-white);
    }
    
    /* Two-column layout */
    .flex-container {
        display: flex;
        gap: 2rem;
        align-items: center;
        margin: 2rem 0;
    }
    
    .flex-item {
        flex: 1;
    }
    
    @media (max-width: 768px) {
        .flex-container {
            flex-direction: column;
        }
    }
    
    /* Streamlit native elements */
    label {
        color: var(--text-white) !important;
    }
    
    .stAlert > div {
        color: var(--bg-dark) !important;
    }
    
    /* Code blocks */
    code {
        color: var(--primary-green) !important;
        background-color: #32324a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to navigate to main.py
def navigate_to_main():
    try:
        st.switch_page("pages/main.py")
    except Exception as e:
        st.error(f"Navigation error: {str(e)}")

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to display signup form
def signup():
    st.subheader("Create a New Account")
    new_username = st.text_input("Username", key="new_username")
    new_password = st.text_input("Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    if st.button("Sign Up", key="signup_button"):
        if new_username and new_password and confirm_password:
            if new_username in st.session_state.users:
                st.error("Username already exists!")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                st.session_state.users[new_username] = hash_password(new_password)
                st.success("Account created successfully! Please log in.")
        else:
            st.error("Please fill in all fields!")

# Function to display login form
def login():
    st.subheader("Login to Your Account")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login", key="login_button"):
        if username in st.session_state.users:
            hashed_password = hash_password(password)
            if st.session_state.users[username] == hashed_password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Incorrect password!")
        else:
            st.error("Username not found!")

# Function to display welcome page
def welcome_page():
    # Centered layout
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        # Header with modern design
        st.markdown('<div class="logo">Fetch<span class="logo-accent">AF</span></div>', unsafe_allow_html=True)
        st.title(f"Welcome, {st.session_state.current_user}")
        
        # Introduction card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### SQL from Plain English")
        st.markdown("Query your PostgreSQL database using natural language - eliminate the need to write complex SQL queries.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Features card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Why FetchAF?")
        st.markdown('<ul class="feature-list">', unsafe_allow_html=True)
        st.markdown("""
        <li>Ask questions in plain English, get SQL queries instantly</li>
        <li>Skip the technical barriers and focus on insights</li>
        <li>Explore your database structure with an intuitive interface</li>
        <li>Deploy anywhere with Docker in minutes</li>
        """, unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Start card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Quick Start")
        st.code("docker-compose up -d", language="bash")
        st.markdown("Connect to http://localhost:8501")
        
        # Action button - fixed to use the navigate_to_main function directly
        if st.button("Explore Now", key="explore_button"):
            navigate_to_main()
        st.markdown('</div>', unsafe_allow_html=True)

        # Links and footer
        st.markdown("""
        <div class="app-footer">
            <p><a href="#">Documentation</a> · <a href="#">GitHub</a> · <a href="#">Support</a></p>
            <p>Powered by Cohere AI & Streamlit</p>
            <button style="background: transparent !important; color: var(--text-light) !important; box-shadow: none !important; font-size: 0.8rem !important; padding: 0 !important;" onclick="handleLogout()">Logout</button>
        </div>
        <script>
        function handleLogout() {
            document.getElementById('logout_button').click();
        }
        </script>
        """, unsafe_allow_html=True)
        
        # Hidden logout button
        if st.button("Logout", key="logout_button", type="primary"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

# Function to display login/signup page
def login_signup_page():
    # Centered layout
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        # Modern header
        st.markdown('<div class="logo">Fetch<span class="logo-accent">AF</span></div>', unsafe_allow_html=True)
        
        # Introduction 
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Transform Database Queries")
        st.markdown("Use natural language to query your PostgreSQL database without writing a single line of SQL.")
        
        st.markdown("#### How It Works")
        st.markdown("""
        1. Connect to your PostgreSQL database
        2. Ask questions in plain English
        3. Get instant results with generated SQL
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auth card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login()
        with tab2:
            signup()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="app-footer">
            <p>Powered by Cohere AI & Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_signup_page()
    else:
        welcome_page()

if __name__ == "__main__":
    main()