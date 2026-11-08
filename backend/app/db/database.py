from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def get_database_url():
    url = settings.database_url

    if not url:
        return None

    if url.startswith("postgresql://"):
        url = url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    elif url.startswith("postgres://"):
        url = url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )

    return url


DATABASE_URL = get_database_url()

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL não foi configurada."
        )

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
