import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.components.TextInput import TextInput
from src.components.DictationButton import DictationButton
from src.components.TextSimplifier import TextSimplifier
from src.components.Quiz import Quiz
from src.components.ProgressDashboard import ProgressDashboard

def set_dyslexia_friendly_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Dyslexic&display=swap');
    html, body, [class*="css"] {
        font-family: 'Open Dyslexic', Arial, sans-serif !important;
        background-color: #171B22 !important;
    }
    .header-bar {
        margin: 36px auto 34px auto;
        max-width: 950px;
        height: 110px;
        background-color: #EAF3FA;
        border-radius: 24px;
        box-shadow: 0 2px 18px #23262D44;
        padding: 20px 32px 24px 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-left {
        display: flex;
        align-items: center;
    }
    .header-logo {
        width: 44px;
        margin-right: 18px;
    }
    .header-title {
        font-size: 32px;
        font-weight: 700;
        color: #31333F;
        margin-bottom: 5px;
        font-family: 'Open Dyslexic', Arial, sans-serif;
        line-height:1.22;
    }
    .header-subtitle {
        color: #4682B4;
        font-size: 15px;
        letter-spacing: 0.03em;
    }
    .header-btn-row {
        display: flex;
        gap: 18px;
    }
    .header-btn {
        font-family: 'Open Dyslexic', Arial, sans-serif !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        border-radius: 13px !important;
        line-height: 1.1 !important;
        height: 52px !important;
        min-width: 116px !important;
        cursor: pointer;
        outline: none !important;
        box-shadow: none !important;
        border-width: 2px;
        border-style: solid;
        transition: background 0.18s;
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
    }
    .login-btn {
        color: #4682B4 !important;
        border-color: #4682B4 !important;
        background: #fff !important;
    }
    .login-btn:hover {
        background: #e4eefd !important;
    }
    .signup-btn {
        color: #FFF !important;
        border-color: #4682B4 !important;
        background: #4682B4 !important;
    }
    .signup-btn:hover {
        background: #3569a9 !important;
    }
    .main-hero-card {
        background-color: #EAF3FA;
        border-radius:32px;
        margin: 40px auto 0 auto;
        max-width: 960px;
        box-shadow: 0 0px 18px #23262D23;
        padding: 54px 40px 55px 40px;
    }
    .main-title {
        text-align:center;
        font-size: 48px;
        font-weight: 800;
        color: #31333F;
        line-height: 1.12;
        margin-bottom: 10px;
    }
    .main-desc {
        text-align:center;
        font-size: 22px;
        margin: 18px auto 32px auto;
        color: #363B41;
        font-weight: 400;
        max-width: 700px;
        padding-bottom: 12px;
    }
    .features-grid {
        display: flex;
        justify-content: center;
        gap: 32px;
        flex-wrap: wrap;
        margin-top: 28px;
    }
    .feature-card {
        background: #FFF;
        border-radius: 18px;
        box-shadow: 0 2px 12px #C4D1E825;
        width: 250px;
        padding: 32px 16px 28px 16px;
        min-height: 230px;
        text-align: center;
    }
    .feature-card .icon {
        font-size: 38px;
    }
    .feature-card .feature-title {
        font-weight: 700;
        font-size: 20px;
        margin-top: 18px;
        margin-bottom: 9px;
        color: #222;
    }
    .feature-card .feature-desc {
        font-size: 15px;
        color: #222;
    }
    .link-blue{
        color:#4682B4 !important; 
        background:none !important; 
        border:none !important;
        padding:0 !important;
        font-size:14px !important;
        text-decoration: underline !important;
        margin-top: 0px !important;
    }
    .plain-text {
        font-size: 16px;
        color: #000;
        font-family: 'Open Dyslexic', Arial, sans-serif;
        display: inline-block;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)
set_dyslexia_friendly_style()

st.set_page_config(
    page_title="EduBot - Dyslexic Learner Support",
    layout="centered",
    initial_sidebar_state="auto"
)

if "page" not in st.session_state:
    st.session_state.page = 'Landing'
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ''

def render_header():
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-left">
            <img class="header-logo" src="https://cdn-icons-png.flaticon.com/512/3061/3061185.png"/>
            <div>
                <div class="header-title">DysLearner AI</div>
                <div class="header-subtitle">Empowering Dyslexic Learners</div>
            </div>
        </div>
        {""
        if not (not st.session_state.logged_in and st.session_state.page == 'Landing')
        else '''<div class="header-btn-row">
            <form action="" method="post" style="display:inline;">
                <button class="header-btn login-btn" name="login-button" type="submit" formnovalidate>Login</button>
            </form>
            <form action="" method="post" style="display:inline;">
                <button class="header-btn signup-btn" name="signup-button" type="submit" formnovalidate>Sign Up</button>
            </form>
        </div>'''
        }
    </div>
    """, unsafe_allow_html=True)
    # Handle navigation with query params (Streamlit's workaround)
    if st.session_state.page == "Landing" and not st.session_state.logged_in:
        qp = st.query_params
        if "login-button" in qp:
            st.session_state.page = "Login"
            st.query_params.clear()
            st.experimental_rerun()
        if "signup-button" in qp:
            st.session_state.page = "Signup"
            st.query_params.clear()
            st.experimental_rerun()

def landing_page():
    render_header()
    st.markdown("""
    <div class="main-hero-card">
      <div class="main-title">Learning Made Easy<br>with AI</div>
      <div class="main-desc">
        Overcome reading and writing challenges with our AI-powered tools designed specifically for dyslexic learners.<br>
        Convert text to speech, speak your thoughts, and simplify complex content.
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="icon">🔊</div>
          <div class="feature-title">Text to Speech</div>
          <div class="feature-desc">Listen to any text with natural, clear pronunciation.</div>
        </div>
        <div class="feature-card">
          <div class="icon">🎤</div>
          <div class="feature-title">Speech to Text</div>
          <div class="feature-desc">Speak your thoughts and convert them to written text.</div>
        </div>
        <div class="feature-card">
          <div class="icon">🧩</div>
          <div class="feature-title">Text Simplifier</div>
          <div class="feature-desc">Simplify complex text for easier understanding.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    render_header()
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_submit_btn"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Profile"
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Please enter both username and password.")

    # Under password: blue-colored "Forgot password?" as clickable markdown (simulate with st.button for function)
    if st.button("Forgot password?", key="forgot_password_btn"):
        st.session_state.page = "ForgotPassword"

    # "Don't have an account? Sign Up" with "Sign Up" in blue and clickable
    st.markdown("""
    <span class="plain-text">Don't have an account?</span>
    <a href="#" class="link-blue" onclick="window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:customEvent', event: {name:'goto_signup'}}, '*');">Sign Up</a>
    """, unsafe_allow_html=True)
    # For Streamlit: catch the button click
    if st.button("Back to Landing", key="back_to_landing_from_login"):
        st.session_state.page = "Landing"
    # Handle JS event fallback
    for k in st.session_state:
        if str(k).startswith("customEvent") and st.session_state[k].get("name") == "goto_signup":
            st.session_state.page = "Signup"

def signup_page():
    render_header()
    st.title("Sign Up")
    st.button("Sign up with Google", key="signup_with_google")
    new_user = st.text_input("Choose Username", key="signup_username")
    new_pass = st.text_input("Create Password", type="password", key="signup_password")
    if st.button("Sign Up", key="final_signup_btn"):
        if new_user and new_pass:
            st.session_state.logged_in = True
            st.session_state.username = new_user
            st.session_state.page = "Profile"
            st.success(f"Account created! Welcome, {new_user}!")
        else:
            st.error("Please enter username and password.")

    st.markdown("""
    <span class="plain-text">Already have an account?</span>
    <a href="#" class="link-blue" onclick="window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:customEvent', event: {name:'goto_login'}}, '*');">Login</a>
    """, unsafe_allow_html=True)
    if st.button("Back to Landing", key="signup_back_landing"):
        st.session_state.page = "Landing"
    for k in st.session_state:
        if str(k).startswith("customEvent") and st.session_state[k].get("name") == "goto_login":
            st.session_state.page = "Login"

def forgot_password_page():
    render_header()
    st.title("Forgot Password")
    email = st.text_input("Enter your email to reset password", key="forgot_email")
    if st.button("Reset Password"):
        if email:
            st.success("Password reset link sent! Check your email.")
        else:
            st.error("Please enter your email address.")
    if st.button("Back to Login"):
        st.session_state.page = "Login"
    if st.button("Back to Landing"):
        st.session_state.page = "Landing"

def profile_page():
    render_header()
    st.title(f"Welcome, {st.session_state.username}!")
    feature = st.selectbox("Select a feature to continue:", [
        "Chatbot",
        "Text Input",
        "Dictation",
        "Text Simplifier",
        "Quiz",
        "Progress Dashboard"
    ])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.session_state.page = "Landing"
        st.experimental_rerun()

    if feature == "Chatbot":
        st.info("Chatbot backend integration coming soon.")
    elif feature == "Text Input":
        text_input = TextInput()
        input_text = text_input.render()
        st.markdown("**Your input:**")
        st.write(input_text)
    elif feature == "Dictation":
        dictation_button = DictationButton()
        dictation_button.render()
    elif feature == "Text Simplifier":
        simplifier = TextSimplifier()
        simplifier.render()
    elif feature == "Quiz":
        quiz = Quiz()
        quiz.render()
    elif feature == "Progress Dashboard":
        dashboard = ProgressDashboard()
        dashboard.render()

if not st.session_state.logged_in:
    if st.session_state.page == "Landing":
        landing_page()
    elif st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Signup":
        signup_page()
    elif st.session_state.page == "ForgotPassword":
        forgot_password_page()
else:
    profile_page()

st.sidebar.markdown("---")
st.sidebar.markdown("Made with 💚 for dyslexic learners by EduBot Team.")
