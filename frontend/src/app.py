import streamlit as st

from components.TextInput import TextInput
from components.DictationButton import DictationButton
from components.Chatbot import Chatbot
from components.TextSimplifier import TextSimplifier
from components.Quiz import Quiz
from components.ProgressDashboard import ProgressDashboard

st.set_page_config(page_title="EduBot - Dyslexic Learner Support", layout="centered", initial_sidebar_state="auto")

# Sidebar Navigation
st.sidebar.title("EduBot Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "Chatbot", "Text Input", "Dictation", "Text Simplifier", "Quiz", "Progress Dashboard"])

st.sidebar.markdown("---")
st.sidebar.markdown("Build an adaptive learning experience for dyslexic users with AI-powered tools.")

# Home Page
if app_mode == "Home":
    st.title("Welcome to EduBot")
    st.markdown("""
    EduBot is an AI-powered educational support app designed to assist dyslexic learners.
    
    Navigate using the sidebar to interact with different learning support tools:
    - Interactive Chatbot for conversational learning.
    - Dyslexia-friendly Text Input with customizable font and spacing.
    - Speech-to-text Dictation.
    - Text Simplification.
    - Interactive Quizzes.
    - Progress Dashboard to track your achievements.
    """)
    st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80")  # Placeholder image

# Chatbot Page
elif app_mode == "Chatbot":
    st.title("Educational Chatbot")
    chatbot = Chatbot()
    chatbot.render()

# Text Input Page
elif app_mode == "Text Input":
    st.title("Dyslexia-friendly Text Input")
    text_input = TextInput()
    input_text = text_input.render()
    st.markdown("**Your input:**")
    st.write(input_text)

# Dictation Page
elif app_mode == "Dictation":
    st.title("Speech-to-Text Dictation")
    dictation_button = DictationButton()
    dictation_button.render()

# Text Simplifier Page
elif app_mode == "Text Simplifier":
    st.title("Text Simplifier")
    simplifier = TextSimplifier()
    simplifier.render()

# Quiz Page
elif app_mode == "Quiz":
    st.title("Interactive Quiz")
    quiz = Quiz()
    quiz.render()

# Progress Dashboard Page
elif app_mode == "Progress Dashboard":
    st.title("Learning Progress Dashboard")
    dashboard = ProgressDashboard()
    dashboard.render()

else:
    st.error("Unknown page selected. Please select a valid option from the sidebar.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with 💚 for dyslexic learners by EduBot Team.")
