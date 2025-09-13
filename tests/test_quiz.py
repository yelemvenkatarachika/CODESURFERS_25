import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db
from backend.services.quiz_service import QuizService
from models.quiz import QuizAnswerRequest, QuizQuestionORM, QuizOptionORM


# Test SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_quiz.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override for test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    with TestingSessionLocal() as db:
        yield db


def test_get_all_quiz_questions(test_client):
    response = test_client.get("/quiz/questions")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    for q in questions:
        assert "id" in q
        assert "question" in q
        assert "options" in q
        # Correct answers should not be exposed
        assert q.get("correct_option_id", 0) == 0


def test_evaluate_correct_answer(test_client, db_session):
    quiz_service = QuizService(db_session)
    # Add a question with options
    question = QuizQuestionORM(question="What is 2+2?")
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    option_correct = QuizOptionORM(question_id=question.id, text="4", is_correct=True)
    option_wrong = QuizOptionORM(question_id=question.id, text="3", is_correct=False)
    db_session.add_all([option_correct, option_wrong])
    db_session.commit()

    # Use test client POST to evaluate correct answer
    payload = {
        "question_id": question.id,
        "selected_option_id": option_correct.id
    }
    response = test_client.post("/quiz/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is True
    assert "Correct" in data["explanation"]


def test_evaluate_incorrect_answer(test_client, db_session):
    question = db_session.query(QuizQuestionORM).first()
    wrong_option = db_session.query(QuizOptionORM).filter_by(question_id=question.id, is_correct=False).first()

    payload = {
        "question_id": question.id,
        "selected_option_id": wrong_option.id
    }
    response = test_client.post("/quiz/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is False
    assert "Incorrect" in data["explanation"]


def test_quiz_service_direct(db_session):
    service = QuizService(db_session)
    questions = service.get_all_questions()
    assert isinstance(questions, list)

    if questions:
        first_question = questions[0]
        # Simulate answering with invalid option id 0
        with pytest.raises(ValueError):
            service.evaluate_answer(
                user_id=1, 
                answer_request=QuizAnswerRequest(
                    question_id=first_question.id,
                    selected_option_id=0
                )
            )
