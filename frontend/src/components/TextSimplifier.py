import streamlit as st
import requests

class TextSimplifier:
    def __init__(self, api_url: str = "http://localhost:8000/api/simplify"):
        # Base URL for backend text simplification endpoint
        self.api_url = api_url
        
        if 'original_text' not in st.session_state:
            st.session_state.original_text = ""
        if 'simplified_text' not in st.session_state:
            st.session_state.simplified_text = ""
        if 'show_simplified' not in st.session_state:
            st.session_state.show_simplified = True
        
    def simplify_text(self, text: str) -> str:
        try:
            response = requests.post(self.api_url, json={"text": text}, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("simplified_text", "")
        except Exception as e:
            st.error(f"Error simplifying text: {e}")
            return ""
    
    def render(self):
        st.markdown("## Text Simplifier")

        st.text_area("Enter text to simplify:", value=st.session_state.original_text, key="original_text", height=150)

        if st.button("Simplify Text"):
            if st.session_state.original_text.strip():
                with st.spinner("Simplifying..."):
                    simplified = self.simplify_text(st.session_state.original_text.strip())
                    if simplified:
                        st.session_state.simplified_text = simplified
                        st.session_state.show_simplified = True
                    else:
                        st.warning("No simplified text returned.")
            else:
                st.warning("Please enter text to simplify.")

        # Toggle between original and simplified text
        if st.session_state.simplified_text:
            toggle_label = "Show Original Text" if st.session_state.show_simplified else "Show Simplified Text"
            if st.button(toggle_label):
                st.session_state.show_simplified = not st.session_state.show_simplified

            # Display text with subtle highlight for keywords or simplified parts
            if st.session_state.show_simplified:
                st.markdown(
                    f"<div style='background-color: #e0f7fa; padding: 15px; border-radius: 8px;'>{st.session_state.simplified_text}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color:#fff3e0; padding: 15px; border-radius: 8px;'>{st.session_state.original_text}</div>",
                    unsafe_allow_html=True
                )

# Usage example if run standalone
if __name__ == "__main__":
    simplifier = TextSimplifier()
    simplifier.render()
