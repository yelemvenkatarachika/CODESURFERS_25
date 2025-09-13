# backend/models/stt.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic models for API validation

class STTRequest(BaseModel):
    audio_filename: Optional[str] = Field(None, description="Original audio filename (optional)")
    audio_format: Optional[str] = Field(None, description="Audio format like 'wav', 'mp3' (optional)")

class STTResponse(BaseModel):
    transcript: str = Field(..., description="Recognized text transcript from the audio")

# Optional SQLAlchemy ORM for logging STT requests

from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base  # Import declarative base

class SpeechToTextLog(Base):
    __tablename__ = "stt_logs"

    id = Column(Integer, primary_key=True, index=True)
    audio_filename = Column(String, nullable=True)
    transcript = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, transcript: str, audio_filename: Optional[str] = None, created_at=None):
        self.audio_filename = audio_filename
        self.transcript = transcript
        self.created_at = created_at

