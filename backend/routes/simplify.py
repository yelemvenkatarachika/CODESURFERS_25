# backend/routes/simplify.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict

from models.simplify import SimplifyRequest, SimplifyResponse
from services.text_simplification import simplify_text  # Your business logic service
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/simplify",
    tags=["simplify"],
    responses={400: {"description": "Bad Request"}},
)

@router.post("/", response_model=SimplifyResponse)
def simplify_text_endpoint(request: SimplifyRequest, db: Session = Depends(get_db)):
    """
    Accepts input text and returns a simplified version of it.
    """
    original_text = request.text.strip()
    if not original_text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    try:
        # Call your text simplification service logic here
        simplified = simplify_text(original_text)

        # Optional: Log simplification in DB or cache, e.g.:
        # log = TextSimplificationLog(
        #     original_text=original_text,
        #     simplified_text=simplified,
        #     created_at=datetime.utcnow(),
        # )
        # db.add(log)
        # db.commit()

        return SimplifyResponse(simplified_text=simplified)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during text simplification: {e}")
