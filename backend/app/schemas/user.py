from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Shared user properties."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Payload for user registration."""

    password: str = Field(..., min_length=6, max_length=100)
    role: Optional[str] = "developer"


class UserLogin(BaseModel):
    """Payload for user login."""

    username: str
    password: str


class UserResponse(UserBase):
    """User response output model (excludes password)."""

    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT Token payload context."""

    username: Optional[str] = None