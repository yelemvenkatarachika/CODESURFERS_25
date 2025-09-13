# backend/services/chatbot_service.py

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
import uuid

from models.chatbot import ChatMessage, ChatResponse
from models.chatbot import ChatSession, ChatMessageORM

class ChatbotService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def generate_reply(self, user_message: str) -> str:
        """
        Replace this stub with real AI chatbot call or NLP logic.
        For now, echoes message with a prefix.
        """
        # TODO: integrate with AI/NLP model or API
        return f"I received your message: {user_message}"

    def create_session(self) -> ChatSession:
        """
        Creates a new chat session with unique session_id and database entry.
        """
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id=session_id, created_at=datetime.utcnow())
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def save_message(self, session_id: int, sender: str, message_text: str) -> ChatMessageORM:
        """
        Saves a single message to the database with timestamp.
        """
        msg = ChatMessageORM(
            session_id=session_id,
            sender=sender,
            message=message_text,
            timestamp=datetime.utcnow(),
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def handle_user_message(self, user_message: str) -> ChatResponse:
        """
        High-level method to process incoming user message and return response.
        Creates a new session for every interaction (can be changed for session reuse).
        Stores messages and generates bot reply.
        """
        session = self.create_session()

        # Save user message
        self.save_message(session.id, "user", user_message)

        # Generate bot reply
        bot_reply = self.generate_reply(user_message)

        # Save bot reply
        self.save_message(session.id, "bot", bot_reply)

        return ChatResponse(reply=bot_reply)
