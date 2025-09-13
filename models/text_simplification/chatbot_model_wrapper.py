# models/chatbot_model_wrapper.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'bot'")
    content: str = Field(..., description="Content of the chat message")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Chatbot reply message")

class ChatSession(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    messages: List[ChatMessage] = Field([], description="List of chat messages in the session")
