import streamlit as st
from streamlit.components.v1 import html

class DictationButton:
    def __init__(self):
        if 'dictated_text' not in st.session_state:
            st.session_state.dictated_text = ""

    def render(self):
        st.markdown("### Dictation (Speech-to-Text)")

        # Display the dictated text area
        dictated_text = st.text_area("Dictated Text:", value=st.session_state.dictated_text, height=150)

        # JS code for microphone button and Chrome Web Speech API integration
        js_code = """
        <script>
        const textarea = window.parent.document.querySelector('textarea[aria-label="Dictated Text:"]');
        let recognizing = false;
        let recognition;

        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support speech recognition. Please use Chrome for this feature.");
        } else {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                recognizing = true;
                console.log("Speech recognition started");
            };

            recognition.onerror = (event) => {
                console.error("Speech recognition error:", event);
            };

            recognition.onend = () => {
                recognizing = false;
                console.log("Speech recognition stopped");
            };

            recognition.onresult = (event) => {
                let interimTranscript = "";
                let finalTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                textarea.value = textarea.value + finalTranscript + interimTranscript;
                textarea.dispatchEvent(new Event('input'));
            };
        }

        function toggleRecognition() {
            if (recognizing) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }
        </script>

        <button onclick="toggleRecognition()" style="font-size: 24px; background-color: #4CAF50; color: white; 
            border:none; padding: 12px 20px; border-radius: 50%; cursor: pointer;" title="Click to start/stop dictation">
            🎤
        </button>
        """

        # Render the microphone button and JS
        html(js_code, height=100)

        # Update session state if text area content changes
        if dictated_text != st.session_state.dictated_text:
            st.session_state.dictated_text = dictated_text


# To use this component inside your Streamlit app,
# instantiate and call render() method:
if __name__ == "__main__":
    dictation_button = DictationButton()
    dictation_button.render()
