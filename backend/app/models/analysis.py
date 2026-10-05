from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    snippet_id = Column(
        Integer,
        ForeignKey("code_snippets.id"),
        nullable=False,
    )

    quality_score = Column(
        Float,
        nullable=False,
        default=0,
    )

    security_score = Column(
        Float,
        nullable=False,
        default=0,
    )

    summary = Column(
        Text,
        nullable=False,
        default="",
    )

    suggestions = Column(
        Text,
        nullable=False,
        default="",
    )

    detected_bugs = Column(
        Text,
        nullable=False,
        default="",
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    snippet = relationship(
        "CodeSnippet",
        back_populates="analysis_results",
    )