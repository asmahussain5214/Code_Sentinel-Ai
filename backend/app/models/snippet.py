from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class CodeSnippet(Base):
    """Code snippet model storing user code submissions for AI review."""

    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True)  # Removed index=True
    title = Column(String(150), nullable=False)
    language = Column(String(50), nullable=False)  # e.g., 'python', 'javascript', 'sql', 'java'
    code_content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="snippets")
    analysis_results = relationship("AnalysisResult", back_populates="snippet", cascade="all, delete-orphan")