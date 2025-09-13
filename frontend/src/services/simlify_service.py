from typing import Dict, Any
from services.api_client import APIClient

class SimplifyService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create a new instance with default base_url
        self.api_client = api_client or APIClient()

    def simplify_text(self, text: str) -> str:
        """
        Send text to the backend simplification API and return simplified text.

        Args:
            text (str): Original text input to simplify.

        Returns:
            str: Simplified text returned by the API.
        """
        try:
            response: Dict[str, Any] = self.api_client.simplify_text(text)
            simplified_text = response.get("simplified_text", "")
            if not simplified_text:
                raise ValueError("Empty simplified text received from API")
            return simplified_text
        except Exception as e:
            # Log or handle exceptions appropriately in production
            raise RuntimeError(f"Text simplification service error: {e}")

# Standalone testing example
if __name__ == "__main__":
    service = SimplifyService()
    try:
        original = "This is a complex sentence that can be difficult to understand."
        simplified = service.simplify_text(original)
        print("Original:", original)
        print("Simplified:", simplified)
    except Exception as err:
        print("Error:", err)
