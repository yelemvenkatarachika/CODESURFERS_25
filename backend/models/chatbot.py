# backend/models/chatbot.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Pydantic models for API validation

class ChatMessage(BaseModel):
    sender: str = Field(..., description="Sender of the message: 'user' or 'bot'")
    message: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default=None, description="Message timestamp")

class ChatRequest(BaseModel):
    """
    Model to receive a user message for chatbot endpoint
    """
    message: str = Field(..., min_length=1, description="User message text")

class ChatResponse(BaseModel):
    """
    Model for chatbot response containing reply text
    """
    reply: str = Field(..., description="Chatbot reply message")

class ChatHistory(BaseModel):
    """
    Model representing a list of chat messages for session history
    """
    session_id: str = Field(..., description="Unique identifier for chat session")
    history: List[ChatMessage] = Field(default_factory=list, description="List of chat messages in session")

    class Config:
        orm_mode = True

# Example SQLAlchemy ORM model for persistent chat session and messages (optional)

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Import your Base from database.py

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    messages = relationship("ChatMessageORM", back_populates="session", cascade="all, delete")

class ChatMessageORM(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'bot'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    session = relationship("ChatSession", back_populates="messages")

