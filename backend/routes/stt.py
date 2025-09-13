# backend/routes/stt.py

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import aiofiles
import os

from models.stt import STTResponse
from services.stt_service import transcribe_audio  # Your business logic to transcribe audio
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/stt",
    tags=["stt"],
    responses={400: {"description": "Bad request"}, 500: {"description": "Internal Server Error"}},
)

@router.post("/", response_model=STTResponse)
async def speech_to_text(
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Accept an audio file upload and return the recognized text transcript.
    """
    # Validate audio file content type (optional)
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid audio file.")

    # Save uploaded file to a temporary location
    temp_file_path = f"/tmp/{audio_file.filename}"
    try:
        async with aiofiles.open(temp_file_path, "wb") as out_file:
            content = await audio_file.read()
            await out_file.write(content)

        # Call your speech-to-text service
        transcript = transcribe_audio(temp_file_path)

        # Optionally, log transcript in DB here

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text processing error: {e}")
    finally:
        # Cleanup the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return STTResponse(transcript=transcript)
