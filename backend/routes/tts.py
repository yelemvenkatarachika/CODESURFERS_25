# backend/routes/tts.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
import base64

from models.tts import TTSRequest, TTSResponse
from services.tts_service import synthesize_speech  # Your TTS business logic
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tts",
    tags=["tts"],
    responses={400: {"description": "Bad Request"}},
)

@router.post("/", response_model=TTSResponse)
def text_to_speech_endpoint(request: TTSRequest, db: Session = Depends(get_db)):
    """
    Accepts input text and returns base64 encoded audio data.
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    try:
        audio_bytes = synthesize_speech(text)

        # Encode audio bytes as base64 string
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Optional: log TTS request/response to DB here

        return TTSResponse(audio_base64=audio_base64)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech processing error: {e}")
