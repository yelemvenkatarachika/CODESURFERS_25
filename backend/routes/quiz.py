# backend/routes/quiz.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.quiz import (
    QuizQuestion,
    QuizAnswerRequest,
    QuizAnswerResponse,
    QuizQuestionORM,
    QuizOptionORM,
    UserQuizAnswerORM,
)
from database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Not found"}},
)

@router.get("/questions", response_model=List[QuizQuestion])
def get_quiz_questions(db: Session = Depends(get_db)):
    """
    Fetch all quiz questions with their options (excluding correct option ID for security).
    """
    questions = db.query(QuizQuestionORM).all()
    results = []
    for question in questions:
        options = [
            {
                "id": option.id,
                "text": option.text,
            }
            for option in question.options
        ]
        q = QuizQuestion(
            id=question.id,
            question=question.question,
            options=[QuizOptionORM(id=opt["id"], text=opt["text"], is_correct=0) for opt in options],
            correct_option_id=0,  # Hide from clients
        )
        results.append(
            QuizQuestion(
                id=question.id,
                question=question.question,
                options=[QuizOptionORM(id=opt["id"], text=opt["text"], is_correct=0) for opt in options],
                correct_option_id=0,  # Omit correct option in frontend
            )
        )
    return results

@router.post("/answer", response_model=QuizAnswerResponse)
def submit_quiz_answer(answer_request: QuizAnswerRequest, db: Session = Depends(get_db)):
    """
    Submit an answer for a quiz question and return correctness and optional explanation.
    """
    question_id = answer_request.question_id
    selected_option_id = answer_request.selected_option_id

    question = db.query(QuizQuestionORM).filter(QuizQuestionORM.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Quiz question not found.")

    selected_option = (
        db.query(QuizOptionORM)
        .filter(QuizOptionORM.id == selected_option_id, QuizOptionORM.question_id == question_id)
        .first()
    )
    if not selected_option:
        raise HTTPException(status_code=404, detail="Selected option not found for this question.")

    # Check correctness
    is_correct = selected_option.is_correct == 1

    # Save user answer record (user_id is not passed here; integrate auth to get actual user)
    user_answer = UserQuizAnswerORM(
        user_id=0,  # To-do: replace with actual user id from auth
        question_id=question_id,
        selected_option_id=selected_option_id,
        correct=1 if is_correct else 0,
        answered_at=datetime.utcnow(),
    )
    db.add(user_answer)
    db.commit()

    # Example explanation; extend DB or logic as required
    explanation = "Correct answer!" if is_correct else "Incorrect, please review the material."

    # Return response with correctness and explanation; updated_score can be added if implemented
    response = QuizAnswerResponse(
        question_id=question_id,
        correct=is_correct,
        explanation=explanation,
        updated_score=None,
    )
    return response
