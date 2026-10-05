from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisCreate(BaseModel):
    snippet_id: int


class AnalysisResponse(BaseModel):
    id: int
    snippet_id: int
    quality_score: float
    security_score: float
    summary: str
    suggestions: str
    detected_bugs: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Compatibility names
AnalysisResultCreate = AnalysisCreate
AnalysisResult = AnalysisResponse