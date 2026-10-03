from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class AnalysisResult(Base):
    """Analysis result model storing AI feedback, security flaws, and code metrics."""

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)  # Removed index=True
    snippet_id = Column(Integer, ForeignKey("code_snippets.id", ondelete="CASCADE"), nullable=False)
    quality_score = Column(Float, nullable=False)  # 0.0 to 10.0
    security_score = Column(Float, nullable=False)  # 0.0 to 10.0
    summary = Column(Text, nullable=False)
    suggestions = Column(Text, nullable=True)
    detected_bugs = Column(Text, nullable=True)  # JSON-formatted or bulleted findings
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    snippet = relationship("CodeSnippet", back_populates="analysis_results")