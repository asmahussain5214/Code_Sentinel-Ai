from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    """User account model for authentication and access control."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Removed index=True (Primary keys are indexed automatically)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="developer", nullable=False)  # 'admin', 'reviewer', 'developer'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    snippets = relationship("CodeSnippet", back_populates="owner", cascade="all, delete-orphan")