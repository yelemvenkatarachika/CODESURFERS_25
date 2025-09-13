# backend/services/quiz_service.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from models.quiz import (
    QuizQuestionORM,
    QuizOptionORM,
    UserQuizAnswerORM,
    QuizAnswerRequest,
    QuizAnswerResponse,
    QuizQuestion,
    QuizOption,
)

class QuizService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_questions(self) -> List[QuizQuestion]:
        """
        Fetch all quiz questions along with their options (without exposing correct answers).
        """
        questions = self.db.query(QuizQuestionORM).all()
        results = []
        for question in questions:
            options = [
                QuizOption(id=option.id, text=option.text)
                for option in question.options
            ]
            results.append(
                QuizQuestion(
                    id=question.id,
                    question=question.question,
                    options=options,
                    correct_option_id=0,  # Do not expose answer in API
                )
            )
        return results

    def evaluate_answer(self, user_id: int, answer_request: QuizAnswerRequest) -> QuizAnswerResponse:
        """
        Evaluate if the submitted answer is correct, save the response, and return results.
        """
        question = self.db.query(QuizQuestionORM).filter(QuizQuestionORM.id == answer_request.question_id).first()
        if not question:
            raise ValueError("Quiz question not found")

        selected_option = (
            self.db.query(QuizOptionORM)
            .filter(
                QuizOptionORM.id == answer_request.selected_option_id,
                QuizOptionORM.question_id == answer_request.question_id,
            )
            .first()
        )
        if not selected_option:
            raise ValueError("Selected option not found for this question")

        is_correct = selected_option.is_correct == 1

        # Record the user's answer
        user_answer = UserQuizAnswerORM(
            user_id=user_id,
            question_id=answer_request.question_id,
            selected_option_id=answer_request.selected_option_id,
            correct=1 if is_correct else 0,
            answered_at=datetime.utcnow(),
        )
        self.db.add(user_answer)
        self.db.commit()

        explanation = "Correct answer!" if is_correct else "Incorrect, please review the material."

        return QuizAnswerResponse(
            question_id=answer_request.question_id,
            correct=is_correct,
            explanation=explanation,
            updated_score=None,  # Implement scoring logic if needed
        )
