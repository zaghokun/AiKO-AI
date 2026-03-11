"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from ..config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """
    Dependency for FastAPI to get database session
    
    Usage:
        @app.get("/endpoint")
        async def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager for database session
    
    Usage:
        with get_db_context() as db:
            ...
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize database - create all tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

def drop_db():
    """Drop all tables - USE WITH CAUTION!"""
    from .models import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped!")
