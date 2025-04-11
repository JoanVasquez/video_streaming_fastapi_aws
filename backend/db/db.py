# Import required modules 📦
from typing import Generator, Optional
from urllib.parse import quote_plus
import os
from functools import lru_cache
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

# Configuration constants with default values 🔧
DB_CONFIG = {
    "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
    "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
    "pool_pre_ping": True,
    "echo": bool(os.getenv("DB_ECHO", "False")),
}


@lru_cache()
def get_database_url() -> str:
    """
    Cache and return database URL to avoid repeated environment
    variable lookups.
    """
    required_vars = [
        "POSTGRES_DB_USER",
        "POSTGRES_DB_PASSWORD",
        "POSTGRES_DB_NAME",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ValueError(
            "Missing required environment variables: "
            f"{', '.join(missing_vars)}"
        )

    return (
        f"postgresql://{quote_plus(os.getenv('POSTGRES_DB_USER'))}:"
        f"{quote_plus(os.getenv('POSTGRES_DB_PASSWORD'))}@"
        f"{os.getenv('POSTGRES_DB_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_DB_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB_NAME')}"
    )


@lru_cache()
def create_db_engine() -> Engine:
    """Create and cache database engine instance."""
    return create_engine(
        get_database_url(),
        poolclass=QueuePool,  # Explicit queue pool for better connection
        # management
        **DB_CONFIG,
    )


# Create thread-safe session factory 🏭
SessionFactory = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=create_db_engine())
)

_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Singleton pattern for engine creation."""
    global _engine
    if _engine is None:
        _engine = create_db_engine()
    return _engine


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Optimized database session context manager.

    Yields:
        Session: SQLAlchemy database session

    Raises:
        SQLAlchemyError: If database connection fails
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f"Database error occurred: {str(e)}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        SessionFactory.remove()  # Clean up thread-local session


def dispose_engine() -> None:
    """Cleanup function to dispose of the engine and connection pool."""
    if _engine:
        _engine.dispose()
