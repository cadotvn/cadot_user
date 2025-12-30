"""
Database session configuration.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    """
    Get database session.
    
    Yields:
        SessionLocal: Database session
        
    Note:
        This function is a dependency for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
