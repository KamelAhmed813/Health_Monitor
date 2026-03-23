from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings


def _sqlite_url(path: str) -> str:
    # SQLAlchemy expects 3 slashes for absolute paths: sqlite:////absolute/path.db
    normalized = os.path.abspath(path)
    parent_dir = os.path.dirname(normalized)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    return "sqlite:///" + normalized.replace("\\", "/")


engine = create_engine(
    _sqlite_url(settings.sqlite_path),
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session, future=True)


def get_session() -> Session:
    # Minimal helper for repository wiring. In production, manage lifecycle via FastAPI dependencies.
    return SessionLocal()

