import streamlit as st

class TextInput:
    def __init__(self, label="Enter text:", placeholder="Type here...", height=150):
        # Initialize session state storage for input text
        if 'input_text' not in st.session_state:
            st.session_state.input_text = ""

        self.label = label
        self.placeholder = placeholder
        self.height = height

    def render(self):
        st.markdown("### Text Input (Dyslexia-friendly)")

        # Custom styling for dyslexia-friendly font and spacing using st.markdown with CSS
        custom_css = """
        <style>
        .dyslexia-textarea textarea {
            font-family: 'OpenDyslexic', Arial, sans-serif;
            font-size: 22px !important;
            line-height: 1.6 !important;
            letter-spacing: 0.12em !important;
            padding: 12px !important;
            border: 2px solid #4CAF50 !important;
            border-radius: 8px !important;
            background-color: #f9f9f9 !important;
            color: #333 !important;
            resize: vertical !important;
            min-height: """ + str(self.height) + """px !important;
        }
        </style>
        """

        # Inject custom CSS for textarea
        st.markdown(custom_css, unsafe_allow_html=True)

        # Render the styled textarea input
        input_text = st.text_area(
            label=self.label,
            value=st.session_state.input_text,
            placeholder=self.placeholder,
            key="input_text",
            height=self.height,
            help="Type your text here. This input supports dyslexia-friendly fonts and spacing."
        )

        # Update session state
        if input_text != st.session_state.input_text:
            st.session_state.input_text = input_text

        return input_text


# To use this component inside your Streamlit app,
# create instance and call render():
if __name__ == "__main__":
    text_input = TextInput()
    user_text = text_input.render()
    st.write("You typed:")
    st.write(user_text)
