from typing import Dict, Any, List, Optional
from services.api_client import APIClient

class QuizService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create new instance
        self.api_client = api_client or APIClient()

    def get_questions(self) -> List[Dict[str, Any]]:
        """
        Fetch quiz questions from backend.

        Returns:
            List[Dict[str, Any]]: List of quiz question objects.
        """
        try:
            response = self.api_client.get("quiz/questions")
            # Expect response format example: {"questions": [...]} 
            questions = response.get("questions", [])
            return questions
        except Exception as e:
            raise RuntimeError(f"Error fetching quiz questions: {e}")

    def submit_answer(self, question_id: int, selected_option: int) -> Dict[str, Any]:
        """
        Submit user answer for a quiz question.

        Args:
            question_id (int): ID of the question being answered.
            selected_option (int): Index or identifier of selected option.

        Returns:
            Dict[str, Any]: API response, e.g., correctness, explanation, updated score.
        """
        try:
            payload = {"question_id": question_id, "selected_option": selected_option}
            response = self.api_client.post("quiz/answer", payload)
            return response
        except Exception as e:
            raise RuntimeError(f"Error submitting quiz answer: {e}")

# Standalone usage example:
if __name__ == "__main__":
    service = QuizService()
    try:
        questions = service.get_questions()
        print("Received questions:", questions)

        if questions:
            first_q = questions[0]
            resp = service.submit_answer(first_q.get("id", 0), 1)  # submits option index 1
            print("Submit answer response:", resp)

    except Exception as err:
        print("Error:", err)
