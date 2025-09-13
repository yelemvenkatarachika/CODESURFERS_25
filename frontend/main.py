# main.py
import streamlit as st
import sys
import os

# Add the src directory to sys.path to import components and app module
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the main app module (app.py) from src folder
import app

if __name__ == "__main__":
    try:
        # Call the main rendering function or class in app.py
        # Assuming app.py executes main UI logic at import or includes a main() function you can call
        pass  # app.py should execute on import, nothing else is needed here

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
