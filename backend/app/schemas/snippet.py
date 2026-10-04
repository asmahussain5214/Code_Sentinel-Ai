from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SnippetBase(BaseModel):
    """Shared code snippet properties."""

    title: str = Field(..., min_length=1, max_length=150)
    language: str = Field(..., min_length=1, max_length=50)
    code_content: str = Field(..., min_length=1)


class SnippetCreate(SnippetBase):
    """Payload for creating a new code snippet."""

    pass


class SnippetResponse(SnippetBase):
    """Snippet response output model with metadata."""

    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}