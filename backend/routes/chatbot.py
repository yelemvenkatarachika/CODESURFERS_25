# backend/routes/chatbot.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

from models.chatbot import ChatRequest, ChatResponse, ChatMessage, ChatHistory
from database import get_db  # Your DB session dependency
from sqlalchemy.orm import Session
from models.chatbot import ChatSession, ChatMessageORM

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}},
)

# Dependency function to get DB session (modify as per your app's setup)
def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat", response_model=ChatResponse)
def send_chat_message(request: ChatRequest, db: Session = Depends(get_db_session)):
    """
    Endpoint to receive a user message and return the chatbot's reply.
    """

    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Simple example chatbot logic: echo or basic processing
    # Replace or extend this with real chatbot/NLP integration
    bot_reply = f"I received your message: {user_message}"

    # Create or retrieve chat session (example: create new session for simplicity)
    session_id = str(uuid.uuid4())
    session = ChatSession(session_id=session_id, created_at=datetime.utcnow())
    db.add(session)
    db.commit()
    db.refresh(session)

    # Save messages to DB (user message)
    user_msg_entry = ChatMessageORM(
        session_id=session.id,
        sender="user",
        message=user_message,
        timestamp=datetime.utcnow(),
    )
    db.add(user_msg_entry)

    # Save bot reply
    bot_msg_entry = ChatMessageORM(
        session_id=session.id,
        sender="bot",
        message=bot_reply,
        timestamp=datetime.utcnow(),
    )
    db.add(bot_msg_entry)

    db.commit()

    return ChatResponse(reply=bot_reply)

@router.get("/history/{session_id}", response_model=ChatHistory)
def get_chat_history(session_id: str, db: Session = Depends(get_db_session)):
    """
    Fetch chat history for a given session ID
    """
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    messages_db = db.query(ChatMessageORM).filter(ChatMessageORM.session_id == session.id).order_by(ChatMessageORM.timestamp.asc()).all()

    chat_messages = [
        ChatMessage(
            sender=msg.sender,
            message=msg.message,
            timestamp=msg.timestamp
        ) for msg in messages_db
    ]

    return ChatHistory(session_id=session_id, history=chat_messages)
