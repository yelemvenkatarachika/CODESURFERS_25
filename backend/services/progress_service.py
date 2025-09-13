# backend/services/progress_service.py

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.progress import UserProgress, ProgressData, ProgressRequest, ProgressResponse

class ProgressService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_progress(self, user_id: int) -> ProgressResponse:
        """
        Retrieve progress data for a user, or return empty data if none exists.
        """
        record = self.db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if not record:
            # Return empty progress data object if not found
            progress_data = ProgressData(
                quiz_score=None,
                lessons_completed=None,
                milestones=[],
                updated_at=None,
            )
            return ProgressResponse(user_id=user_id, progress=progress_data)

        progress_data = ProgressData(
            quiz_score=record.quiz_score,
            lessons_completed=record.lessons_completed,
            milestones=record.milestones or [],
            updated_at=record.updated_at,
        )
        return ProgressResponse(user_id=user_id, progress=progress_data)

    def update_progress(self, progress_request: ProgressRequest) -> ProgressResponse:
        """
        Create or update a user's progress record.
        """
        user_id = progress_request.user_id
        progress = progress_request.progress

        record = self.db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

        if not record:
            record = UserProgress(
                user_id=user_id,
                quiz_score=progress.quiz_score,
                lessons_completed=progress.lessons_completed,
                milestones=progress.milestones,
                updated_at=progress.updated_at or datetime.utcnow(),
            )
            self.db.add(record)
        else:
            # Update fields only if new values are provided
            if progress.quiz_score is not None:
                record.quiz_score = progress.quiz_score
            if progress.lessons_completed is not None:
                record.lessons_completed = progress.lessons_completed
            if progress.milestones:
                record.milestones = progress.milestones
            record.updated_at = progress.updated_at or datetime.utcnow()

        self.db.commit()
        self.db.refresh(record)

        updated_progress = ProgressData(
            quiz_score=record.quiz_score,
            lessons_completed=record.lessons_completed,
            milestones=record.milestones or [],
            updated_at=record.updated_at,
        )

        return ProgressResponse(user_id=user_id, progress=updated_progress)
