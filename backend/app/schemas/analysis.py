from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    """Payload for requesting an AI code analysis."""

    snippet_id: int


class AnalysisResponse(BaseModel):
    """Analysis output response model with quality scores and bug logs."""

    id: int
    snippet_id: int
    quality_score: float = Field(..., ge=0.0, le=10.0)
    security_score: float = Field(..., ge=0.0, le=10.0)
    summary: str
    suggestions: Optional[str] = None
    detected_bugs: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}