from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    title = Column(
        String(255),
        nullable=True,
    )

    code_content = Column(
        Text,
        nullable=False,
    )

    language = Column(
        String(50),
        nullable=False,
        default="text",
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    user = relationship(
        "User",
        back_populates="snippets",
    )

    analysis_results = relationship(
        "AnalysisResult",
        back_populates="snippet",
        cascade="all, delete-orphan",
    )