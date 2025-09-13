from typing import Dict, Any
from services.api_client import APIClient

class ChatbotService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create new instance with default base_url
        self.api_client = api_client or APIClient()

    def send_message(self, message: str) -> str:
        """
        Send a user message to the chatbot backend and receive the bot's response text.

        Args:
            message (str): User input message string.

        Returns:
            str: Chatbot reply message.
        """
        try:
            response: Dict[str, Any] = self.api_client.send_chat_message(message)
            # Expecting response structure: {"reply": "<bot reply>"}
            reply = response.get("reply", "")
            if not reply:
                raise ValueError("Empty reply from chatbot API")
            return reply
        except Exception as e:
            # Log or handle errors suitably in production
            raise RuntimeError(f"Chatbot service error: {e}")

# Usage example for testing standalone
if __name__ == "__main__":
    service = ChatbotService()
    try:
        user_msg = "Hello, how are you?"
        bot_reply = service.send_message(user_msg)
        print(f"User: {user_msg}")
        print(f"Bot: {bot_reply}")
    except Exception as err:
        print("Error:", err)
