import os

from app.models.base import Base  # Keep this, do NOT redefine Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database URL from env or default SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    """
    Provides a database session and closes it after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
