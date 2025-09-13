# backend/models/tts.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic models for API validation

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to convert to speech")

class TTSResponse(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio data (MP3 or WAV)")

# Optional SQLAlchemy ORM for logging TTS conversion requests

from sqlalchemy import Column, Integer, Text, DateTime
from database import Base  # Import declarative base

class TextToSpeechLog(Base):
    __tablename__ = "tts_logs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    audio_base64 = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, text: str, audio_base64: str, created_at=None):
        self.text = text
        self.audio_base64 = audio_base64
        self.created_at = created_at
