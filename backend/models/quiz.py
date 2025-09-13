# backend/models/quiz.py

from pydantic import BaseModel, Field, conint
from typing import List, Optional
from datetime import datetime

# Pydantic models for API validation


class QuizOption(BaseModel):
    id: int = Field(..., description="Option identifier")
    text: str = Field(..., description="Text of the option")


class QuizQuestion(BaseModel):
    id: int = Field(..., description="Question identifier")
    question: str = Field(..., description="The question text")
    options: List[QuizOption] = Field(..., description="Answer options")
    correct_option_id: int = Field(..., description="ID of the correct option")

    class Config:
        orm_mode = True


class QuizAnswerRequest(BaseModel):
    question_id: int = Field(..., description="ID of the quiz question being answered")
    selected_option_id: int = Field(..., description="ID of the option selected by the user")


class QuizAnswerResponse(BaseModel):
    question_id: int = Field(..., description="ID of the quiz question")
    correct: bool = Field(..., description="Whether the answer was correct")
    explanation: Optional[str] = Field(None, description="Optional explanation for the correct answer")
    updated_score: Optional[int] = Field(None, description="User's updated quiz score after answering")


# SQLAlchemy ORM models for persistence

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base  # Import your declarative base


class QuizQuestionORM(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    options = relationship("QuizOptionORM", back_populates="question", cascade="all, delete")


class QuizOptionORM(Base):
    __tablename__ = "quiz_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Integer, nullable=False, default=0)  # 1 for correct, 0 for incorrect

    question = relationship("QuizQuestionORM", back_populates="options")


class UserQuizAnswerORM(Base):
    __tablename__ = "user_quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("quiz_options.id"), nullable=False)
    correct = Column(Integer, nullable=False)
    answered_at = Column(DateTime, nullable=False)

