# backend/models/simplify.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic models for API validation

class SimplifyRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Original text to simplify")

class SimplifyResponse(BaseModel):
    simplified_text: str = Field(..., description="Simplified version of the input text")

# Optional SQLAlchemy ORM for persistence (e.g., logs, history)

from sqlalchemy import Column, Integer, Text, DateTime
from database import Base  # Import declarative base

class TextSimplificationLog(Base):
    __tablename__ = "text_simplifications"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    simplified_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, original_text: str, simplified_text: str, created_at=None):
        self.original_text = original_text
        self.simplified_text = simplified_text
        self.created_at = created_at

