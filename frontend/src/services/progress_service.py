from typing import Dict, Any, Optional
from services.api_client import APIClient

class ProgressService:
    def __init__(self, api_client: APIClient = None):
        # Use existing APIClient or create new instance with default base_url
        self.api_client = api_client or APIClient()

    def get_progress(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch user learning progress data from backend API.

        Args:
            user_id (Optional[int]): Optional user ID to fetch progress for.

        Returns:
            Dict[str, Any]: Dictionary containing progress data such as quiz scores,
                            lesson completions, milestones, etc.
        """
        try:
            progress = self.api_client.get_progress(user_id=user_id)
            return progress
        except Exception as e:
            # Log or handle errors as appropriate in production
            raise RuntimeError(f"Progress service error: {e}")

    def update_progress(self, user_id: int, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update or submit user progress data to backend API.

        Args:
            user_id (int): User identifier.
            progress_data (Dict[str, Any]): Progress details to update/submit.

        Returns:
            Dict[str, Any]: Backend API response data.
        """
        try:
            data = {"user_id": user_id, "progress": progress_data}
            response = self.api_client.post("progress/update", data)
            return response
        except Exception as e:
            raise RuntimeError(f"Progress update error: {e}")

# Usage example for standalone testing
if __name__ == "__main__":
    service = ProgressService()
    try:
        user_id_test = 123
        user_progress = service.get_progress(user_id=user_id_test)
        print(f"Progress for user {user_id_test}: {user_progress}")

        # Example update payload
        update_payload = {"quiz_score": 85, "lessons_completed": 4}
        update_resp = service.update_progress(user_id=user_id_test, progress_data=update_payload)
        print(f"Update response: {update_resp}")

    except Exception as err:
        print("Error:", err)
