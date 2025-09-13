# backend/models/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models for API validation

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, description="Full name of the user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

    @validator('password')
    def password_rules(cls, v):
        # Add any custom password validation rules here
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class UserRead(UserBase):
    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="Is the user account active")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        orm_mode = True

# SQLAlchemy ORM models for persistence

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base  # Import your declarative base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a plaintext password against the stored hashed password
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password: str):
        """
        Hash and store the password
        """
        self.hashed_password = pwd_context.hash(plain_password)
