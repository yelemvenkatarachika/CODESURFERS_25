from typing import Dict, Any
from services.api_client import APIClient

class TTSService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create new instance with default backend URL
        self.api_client = api_client or APIClient()

    def text_to_speech(self, text: str) -> bytes:
        """
        Send text to backend Text-to-Speech API and receive audio binary data.

        Args:
            text (str): Input text to convert to speech.

        Returns:
            bytes: Audio data in binary form (e.g., WAV or MP3).
        """
        try:
            response: Dict[str, Any] = self.api_client.text_to_speech(text)
            audio_base64 = response.get("audio_base64", "")
            if not audio_base64:
                raise ValueError("Empty audio data received from TTS API")
            import base64
            audio_bytes = base64.b64decode(audio_base64)
            return audio_bytes
        except Exception as e:
            # Log or handle exceptions properly in production
            raise RuntimeError(f"TTS service error: {e}")

# Standalone usage example, assuming TTS API returns base64-encoded audio
if __name__ == "__main__":
    tts_service = TTSService()
    try:
        sample_text = "Hello! This is a Text-to-Speech test."
        audio_data = tts_service.text_to_speech(sample_text)
        with open("output_audio.mp3", "wb") as f:
            f.write(audio_data)
        print("Audio file saved as output_audio.mp3")
    except Exception as err:
        print("Error:", err)
