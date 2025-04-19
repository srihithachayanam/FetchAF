# import streamlit as st
# import hashlib

# # Initialize session state for user data, login status, and page navigation
# if 'users' not in st.session_state:
#     st.session_state.users = {}  # Store username: hashed_password
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None
# if 'page' not in st.session_state:
#     st.session_state.page = 'login'  # Tracks current page: 'login', 'welcome', 'main'

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to display signup form
# def signup():
#     st.subheader("Create a New Account")
#     new_username = st.text_input("New Username")
#     new_password = st.text_input("New Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")

#     if st.button("Sign Up"):
#         if new_username and new_password and confirm_password:
#             if new_username in st.session_state.users:
#                 st.error("Username already exists!")
#             elif new_password != confirm_password:
#                 st.error("Passwords do not match!")
#             else:
#                 st.session_state.users[new_username] = hash_password(new_password)
#                 st.success("Account created successfully! Please log in.")
#         else:
#             st.error("Please fill in all fields!")

# # Function to display login form
# def login():
#     st.subheader("Login to Your Account")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username in st.session_state.users:
#             hashed_password = hash_password(password)
#             if st.session_state.users[username] == hashed_password:
#                 st.session_state.logged_in = True
#                 st.session_state.current_user = username
#                 st.session_state.page = 'welcome'
#                 st.success(f"Welcome back, {username}!")
#                 st.rerun()  # Refresh to show welcome page
#             else:
#                 st.error("Incorrect password!")
#         else:
#             st.error("Username not found!")

# # Function to display welcome page
# def welcome_page():
#     st.title(f"Welcome, {st.session_state.current_user}!")
#     st.write("You have successfully logged in to your account.")

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Explore"):
#             st.session_state.page = 'main'
#             st.rerun()  # Navigate to main.py page
#     with col2:
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.current_user = None
#             st.session_state.page = 'login'
#             st.success("You have been logged out.")
#             st.rerun()  # Refresh to show login/signup page

# # Function to display login/signup page
# def login_signup_page():
#     st.title("FetchAF")
#     tab1, tab2 = st.tabs(["Login", "Signup"])
#     with tab1:
#         login()
#     with tab2:
#         signup()

# # Main app logic
# def main():
#     if not st.session_state.logged_in:
#         st.session_state.page = 'login'
#         login_signup_page()
#     else:
#         if st.session_state.page == 'welcome':
#             welcome_page()
#         elif st.session_state.page == 'main':
#             # Placeholder for main.py content; actual content will be in pages/main.py
#             st.title(f"Explore Page for {st.session_state.current_user}")
#             st.write("This is the main page content from main.py.")
#             if st.button("Back to Welcome"):
#                 st.session_state.page = 'welcome'
#                 st.rerun()

# if __name__ == "__main__":
#     main()




    
# import streamlit as st
# import hashlib

# # Initialize session state for user data and login status
# if 'users' not in st.session_state:
#     st.session_state.users = {}  # Store username: hashed_password
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# # Hide Streamlit's default sidebar for login/signup and welcome pages
# st.set_page_config(page_title="FetchAF", layout="wide")
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] {display: none;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to display signup form
# def signup():
#     st.subheader("Create a New Account")
#     new_username = st.text_input("New Username")
#     new_password = st.text_input("New Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")

#     if st.button("Sign Up"):
#         if new_username and new_password and confirm_password:
#             if new_username in st.session_state.users:
#                 st.error("Username already exists!")
#             elif new_password != confirm_password:
#                 st.error("Passwords do not match!")
#             else:
#                 st.session_state.users[new_username] = hash_password(new_password)
#                 st.success("Account created successfully! Please log in.")
#         else:
#             st.error("Please fill in all fields!")

# # Function to display login form
# def login():
#     st.subheader("Login to Your Account")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username in st.session_state.users:
#             hashed_password = hash_password(password)
#             if st.session_state.users[username] == hashed_password:
#                 st.session_state.logged_in = True
#                 st.session_state.current_user = username
#                 st.success(f"Welcome back, {username}!")
#                 st.rerun()  # Refresh to show welcome page
#             else:
#                 st.error("Incorrect password!")
#         else:
#             st.error("Username not found!")

# # Function to display welcome page
# def welcome_page():
#     st.title(f"Welcome, {st.session_state.current_user}!")
#     st.write("You have successfully logged in to your account.")

#     # Add FetchAF information
#     st.markdown("""
#     ### FetchAF: SQL from Plain English
#     Query PostgreSQL databases using natural language

#     #### Why FetchAF?
#     - **Simple**: Ask questions in English, get SQL queries instantly
#     - **Fast**: Skip the technical barriers to your data
#     - **Interactive**: Explore your database structure with ease
#     - **Portable**: Deploy anywhere with Docker

#     #### Quick Start
#     - `docker-compose up -d`
#     - Connect to http://localhost:8501

#     #### How It Works
#     - Connect your PostgreSQL database
#     - Type your question
#     - Get results instantly

#     [Get Started](#) | [Documentation](#)

#     **Powered by Cohere AI & Streamlit | [GitHub Repository](#)**
#     """)

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Explore"):
#             st.write("Debug: Explore button clicked, navigating to main.py")
#             try:
#                 st.switch_page("pages/main.py")  # Navigate to main.py
#             except Exception as e:
#                 st.error(f"Navigation error: {str(e)}")
#     with col2:
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.current_user = None
#             st.success("You have been logged out.")
#             st.rerun()  # Refresh to show login/signup page

# # Function to display login/signup page
# def login_signup_page():
#     st.title("FetchAF")
#     tab1, tab2 = st.tabs(["Login", "Signup"])
#     with tab1:
#         login()
#     with tab2:
#         signup()

# # Main app logic
# def main():
#     if not st.session_state.logged_in:
#         login_signup_page()
#     else:
#         welcome_page()

# if __name__ == "__main__":
#     main()    


# import streamlit as st
# import hashlib

# # Initialize session state for user data and login status
# if 'users' not in st.session_state:
#     st.session_state.users = {}  # Store username: hashed_password
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# # Hide Streamlit's default sidebar for login/signup and welcome pages
# st.set_page_config(page_title="FetchAF", layout="wide")
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] {display: none;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to display signup form
# def signup():
#     st.subheader("Create a New Account")
#     new_username = st.text_input("New Username")
#     new_password = st.text_input("New Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")

#     if st.button("Sign Up"):
#         if new_username and new_password and confirm_password:
#             if new_username in st.session_state.users:
#                 st.error("Username already exists!")
#             elif new_password != confirm_password:
#                 st.error("Passwords do not match!")
#             else:
#                 st.session_state.users[new_username] = hash_password(new_password)
#                 st.success("Account created successfully! Please log in.")
#         else:
#             st.error("Please fill in all fields!")

# # Function to display login form
# def login():
#     st.subheader("Login to Your Account")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username in st.session_state.users:
#             hashed_password = hash_password(password)
#             if st.session_state.users[username] == hashed_password:
#                 st.session_state.logged_in = True
#                 st.session_state.current_user = username
#                 st.success(f"Welcome back, {username}!")
#                 st.rerun()  # Refresh to show welcome page
#             else:
#                 st.error("Incorrect password!")
#         else:
#             st.error("Username not found!")

# # Function to display welcome page
# def welcome_page():
#     st.title(f"Welcome, {st.session_state.current_user}!")
#     st.write("You have successfully logged in to your account.")

#     # Add FetchAF information
#     st.markdown("""
#     ### FetchAF: SQL from Plain English
#     Query PostgreSQL databases using natural language

#     #### Why FetchAF?
#     - **Simple**: Ask questions in English, get SQL queries instantly
#     - **Fast**: Skip the technical barriers to your data
#     - **Interactive**: Explore your database structure with ease
#     - **Portable**: Deploy anywhere with Docker

#     #### Quick Start
#     - `docker-compose up -d`
#     - Connect to http://localhost:8501

#     #### How It Works
#     - Connect your PostgreSQL database
#     - Type your question
#     - Get results instantly

#     [Get Started](#) | [Documentation](#)

#     **Powered by Cohere AI & Streamlit | [GitHub Repository](#)**
#     """)

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Explore"):
#             st.write("Debug: Explore button clicked, navigating to main.py")
#             try:
#                 st.switch_page("pages/main.py")  # Navigate to main.py
#             except Exception as e:
#                 st.error(f"Navigation error: {str(e)}")
#     with col2:
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.current_user = None
#             st.success("You have been logged out.")
#             st.rerun()  # Refresh to show login/signup page

# # Function to display login/signup page
# def login_signup_page():
#     st.title("FetchAF")
#     tab1, tab2 = st.tabs(["Login", "Signup"])
#     with tab1:
#         login()
#     with tab2:
#         signup()

# # Main app logic
# def main():
#     if not st.session_state.logged_in:
#         login_signup_page()
#     else:
#         welcome_page()

# if __name__ == "__main__":
#     main()

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
    [data-testid="stSidebar"] {display: none;}
    .main .block-container {
        background: linear-gradient(135deg, #4b0082, #1a1a3d);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #ffffff;
        padding: 2rem;
    }
    .hero {
        background: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        backdrop-filter: blur(5px);
    }
    .hero h1 {
        font-size: 3em;
        color: #e6e6fa;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    .hero p {
        font-size: 1.2em;
        color: #d3d3d3;
        margin-bottom: 1.5rem;
    }
    .section {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        max-width: 700px;
        text-align: left;
        margin: 1rem 0;
        backdrop-filter: blur(3px);
    }
    .section h4 {
        color: #9370db;
        margin-bottom: 1rem;
    }
    .section ul {
        list-style-type: none;
        padding-left: 0;
    }
    .section ul li {
        margin-bottom: 0.5rem;
        color: #e0e0e0;
    }
    .section ul li:before {
        content: "•";
        color: #9370db;
        font-weight: bold;
        display: inline-block;
        width: 1em;
        margin-left: -1em;
    }
    .cta-button {
        display: inline-block;
        padding: 0.75rem 2rem;
        background-color: #9370db;
        color: white;
        text-decoration: none;
        border-radius: 25px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .cta-button:hover {
        background-color: #7b68ee;
    }
    .links {
        text-align: center;
        margin-top: 1rem;
    }
    .links a {
        color: #00d4ff;
        margin: 0 1rem;
        text-decoration: none;
        font-weight: bold;
    }
    .links a:hover {
        text-decoration: underline;
    }
    .powered-by {
        text-align: center;
        color: #d3d3d3;
        font-size: 0.9em;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to display signup form
def signup():
    st.subheader("Create a New Account")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
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
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
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
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title(f"Welcome, {st.session_state.current_user}!")
    st.write(f"You have successfully logged in to your account.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("### FetchAF: SQL from Plain English")
    st.write("Query PostgreSQL databases using natural language")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h4>Why FetchAF?</h4>', unsafe_allow_html=True)
    st.markdown("""
    <ul>
        <li>Simple: Ask questions in English, get SQL queries instantly</li>
        <li>Fast: Skip the technical barriers to your data</li>
        <li>Interactive: Explore your database structure with ease</li>
        <li>Portable: Deploy anywhere with Docker</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h4>Quick Start</h4>', unsafe_allow_html=True)
    st.markdown("""
    <ul>
        <li><span style="color: #32cd32">docker-compose up -d</span></li>
        <li>Connect to http://localhost:8501</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h4>How It Works</h4>', unsafe_allow_html=True)
    st.markdown("""
    <ul>
        <li>Connect your PostgreSQL database</li>
        <li>Type your question</li>
        <li>Get results instantly</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="links">', unsafe_allow_html=True)
    st.markdown('[Get Started](#) | [Documentation](#) | [GitHub Repository](#)', unsafe_allow_html=True)
    st.markdown('<div class="powered-by">Powered by Cohere AI & Streamlit</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Explore", key="explore_button"):
            st.write("Debug: Explore button clicked, navigating to main.py")
            try:
                st.switch_page("pages/main.py")
            except Exception as e:
                st.error(f"Navigation error: {str(e)}")
    with col2:
        if st.button("Logout", key="logout_button"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("You have been logged out.")
            st.rerun()

# Function to display login/signup page
def login_signup_page():
    st.title("My Streamlit App")
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        login()
    with tab2:
        signup()

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_signup_page()
    else:
        welcome_page()

if __name__ == "__main__":
    main()