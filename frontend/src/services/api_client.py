import requests
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        # Example: add headers that might be common for all calls (e.g., auth tokens)
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _handle_response(self, response: requests.Response) -> Any:
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            # Add logging or more sophisticated error handling here
            raise RuntimeError(f"HTTP error occurred: {http_err} - {response.text}")
        except Exception as err:
            raise RuntimeError(f"Unexpected error: {err}")

    def post(self, endpoint: str, payload: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=payload or {})
        return self._handle_response(response)

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params or {})
        return self._handle_response(response)

    # Specific API call wrappers

    def send_chat_message(self, message: str) -> Dict:
        return self.post("chatbot/chat", {"message": message})

    def get_quiz_questions(self) -> Dict:
        return self.get("quiz/questions")

    def submit_quiz_answer(self, question_id: int, selected_option: int) -> Dict:
        return self.post("quiz/answer", {"question_id": question_id, "selected_option": selected_option})

    def simplify_text(self, text: str) -> Dict:
        return self.post("simplify", {"text": text})

    def get_progress(self, user_id: Optional[int] = None) -> Dict:
        params = {"user_id": user_id} if user_id else {}
        return self.get("progress", params)

    def text_to_speech(self, text: str) -> Dict:
        return self.post("tts", {"text": text})

    def speech_to_text(self, audio_data: bytes) -> Dict:
        # Assuming multipart/form-data required for audio uploads
        url = f"{self.base_url}/stt"
        files = {"file": ("audio.wav", audio_data, "audio/wav")}
        response = self.session.post(url, files=files)
        return self._handle_response(response)

# Usage example for testing standalone functionality
if __name__ == "__main__":
    api = APIClient()
    try:
        chat_resp = api.send_chat_message("Hello!")
        print("Chatbot response:", chat_resp)

        quiz_qs = api.get_quiz_questions()
        print("Quiz questions:", quiz_qs)

        simple_text_resp = api.simplify_text("This is hard to read text.")
        print("Simplified text:", simple_text_resp)

        progress = api.get_progress()
        print("User progress data:", progress)

    except Exception as e:
        print("Error during API calls:", e)
