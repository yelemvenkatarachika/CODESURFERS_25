# backend/routes/progress.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.progress import ProgressRequest, ProgressResponse, ProgressData, UserProgress
from database import get_db

router = APIRouter(
    prefix="/progress",
    tags=["progress"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=ProgressResponse)
def get_progress(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch the learning progress data for a given user.
    """
    progress_record = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress_record:
        # Return empty progress if none found (or consider 404)
        return ProgressResponse(
            user_id=user_id,
            progress=ProgressData(
                quiz_score=None,
                lessons_completed=None,
                milestones=[],
                updated_at=None,
            ),
        )

    progress_data = ProgressData(
        quiz_score=progress_record.quiz_score,
        lessons_completed=progress_record.lessons_completed,
        milestones=progress_record.milestones or [],
        updated_at=progress_record.updated_at,
    )
    return ProgressResponse(user_id=user_id, progress=progress_data)

@router.post("/update", response_model=ProgressResponse)
def update_progress(progress_request: ProgressRequest, db: Session = Depends(get_db)):
    """
    Create or update user progress data.
    """
    user_id = progress_request.user_id
    new_progress = progress_request.progress

    progress_record = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

    if not progress_record:
        progress_record = UserProgress(
            user_id=user_id,
            quiz_score=new_progress.quiz_score,
            lessons_completed=new_progress.lessons_completed,
            milestones=new_progress.milestones,
            updated_at=new_progress.updated_at or datetime.utcnow(),
        )
        db.add(progress_record)
    else:
        progress_record.quiz_score = new_progress.quiz_score or progress_record.quiz_score
        progress_record.lessons_completed = new_progress.lessons_completed or progress_record.lessons_completed
        progress_record.milestones = new_progress.milestones or progress_record.milestones
        progress_record.updated_at = new_progress.updated_at or datetime.utcnow()

    db.commit()
    db.refresh(progress_record)

    updated_progress = ProgressData(
        quiz_score=progress_record.quiz_score,
        lessons_completed=progress_record.lessons_completed,
        milestones=progress_record.milestones or [],
        updated_at=progress_record.updated_at,
    )
    return ProgressResponse(user_id=user_id, progress=updated_progress)
