# backend/models/progress.py

from pydantic import BaseModel, Field, conint
from typing import Optional, List
from datetime import datetime

# Pydantic models for API validation

class ProgressData(BaseModel):
    quiz_score: Optional[conint(ge=0, le=100)] = Field(None, description="Latest quiz score as a percentage")
    lessons_completed: Optional[conint(ge=0)] = Field(None, description="Number of lessons completed")
    milestones: Optional[List[str]] = Field(default_factory=list, description="Milestones achieved by user")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when progress was last updated")

class ProgressRequest(BaseModel):
    user_id: int = Field(..., description="User identifier")
    progress: ProgressData = Field(..., description="Progress data payload")

class ProgressResponse(BaseModel):
    user_id: int = Field(..., description="User identifier")
    progress: ProgressData = Field(..., description="Current progress data")

class ProgressSummary(BaseModel):
    average_score: Optional[float] = Field(None, description="Average quiz score over time")
    total_lessons_completed: Optional[int] = Field(None, description="Total lessons completed")
    milestones: List[str] = Field(default_factory=list, description="Milestones achieved")

# Optional SQLAlchemy ORM models for persistence

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base  # Import your declarative base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    quiz_score = Column(Float, nullable=True)
    lessons_completed = Column(Integer, nullable=True)
    milestones = Column(JSON, default=[])
    updated_at = Column(DateTime, nullable=True)

    def update_progress(self, new_progress: dict):
        if "quiz_score" in new_progress and new_progress["quiz_score"] is not None:
            self.quiz_score = new_progress["quiz_score"]
        if "lessons_completed" in new_progress and new_progress["lessons_completed"] is not None:
            self.lessons_completed = new_progress["lessons_completed"]
        if "milestones" in new_progress and new_progress["milestones"]:
            self.milestones = new_progress["milestones"]
        self.updated_at = new_progress.get("updated_at", self.updated_at)

