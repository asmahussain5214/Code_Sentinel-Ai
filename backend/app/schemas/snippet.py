from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CodeSnippetBase(BaseModel):
    title: Optional[str] = None
    language: str = "text"
    code_content: str = Field(min_length=1)


class CodeSnippetCreate(CodeSnippetBase):
    pass


class CodeSnippetUpdate(BaseModel):
    title: Optional[str] = None
    language: Optional[str] = None
    code_content: Optional[str] = None


class CodeSnippet(CodeSnippetBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Compatibility names used by the endpoint
SnippetCreate = CodeSnippetCreate
SnippetResponse = CodeSnippet