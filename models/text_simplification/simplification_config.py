# models/text_simplification/simplification_config.py

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal

class SimplificationConfig(BaseModel):
    language: Optional[str] = Field(
        "en",
        description="Language code (ISO 639-1) for text simplification",
        example="en",
    )
    max_complexity_level: Optional[int] = Field(
        3,
        ge=1,
        le=5,
        description="Maximum complexity level allowed; 1=simplest, 5=most complex",
        example=3,
    )
    simplify_sentences: Optional[bool] = Field(
        True,
        description="Whether to simplify sentence structures",
    )
    replace_difficult_words: Optional[bool] = Field(
        True,
        description="Whether to replace difficult words with simpler alternatives",
    )
    style: Optional[Literal["formal", "informal", "neutral"]] = Field(
        "neutral",
        description="Style/tone for simplification output",
    )

    @validator("language")
    def language_must_be_two_letters(cls, v):
        if len(v) != 2:
            raise ValueError("Language must be a 2-letter ISO 639-1 code")
        return v.lower()
