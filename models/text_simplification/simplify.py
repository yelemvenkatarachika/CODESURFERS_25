# models/text_simplification/simplify.py

from pydantic import BaseModel, Field

class SimplifyRequest(BaseModel):
    text: str = Field(..., description="Original text to simplify")

class SimplifyResponse(BaseModel):
    simplified_text: str = Field(..., description="Simplified output text")
