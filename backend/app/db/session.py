from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Construct Oracle SQLAlchemy connection string using python-oracledb driver
# Format: oracle+oracledb://user:password@host:port/?service_name=service
DATABASE_URL = (
    f"oracle+oracledb://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/?service_name={settings.DB_SERVICE_NAME}"
)

# Create SQLAlchemy Database Engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Logs generated SQL queries when DEBUG=True
    pool_pre_ping=True,   # Verifies database connection before executing queries
)

# Create SessionLocal class factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base Class for ORM models
Base = declarative_base()


def get_db() -> Generator:
    """FastAPI Dependency providing a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()