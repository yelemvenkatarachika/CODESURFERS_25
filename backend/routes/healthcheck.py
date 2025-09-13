# backend/routes/healthcheck.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    responses={200: {"description": "Service is healthy"}},
)

@router.get("/", summary="Health check endpoint")
def health_check():
    """
    Returns simple status message to indicate API is running and healthy.
    """
    return {"status": "healthy", "message": "API is running smoothly"}
