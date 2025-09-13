from typing import Dict, Any
from services.api_client import APIClient

class STTService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create new instance with default base_url
        self.api_client = api_client or APIClient()

    def speech_to_text(self, audio_file_path: str) -> str:
        """
        Send audio file to backend Speech-to-Text API and return recognized text.

        Args:
            audio_file_path (str): Path to the audio file to be transcribed.

        Returns:
            str: Transcribed text response from the API.
        """
        try:
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
            response: Dict[str, Any] = self.api_client.speech_to_text(audio_data)
            text = response.get("transcript", "")
            if not text:
                raise ValueError("Empty transcript received from STT API")
            return text
        except Exception as e:
            # Log or handle exceptions appropriately
            raise RuntimeError(f"Speech-to-Text service error: {e}")

# Usage example for standalone testing
if __name__ == "__main__":
    stt_service = STTService()
    try:
        audio_path = "sample_audio.wav"  # Replace with actual file path
        transcription = stt_service.speech_to_text(audio_path)
        print("Transcribed Text:", transcription)
    except Exception as err:
        print("Error:", err)
