"""Infraestrutura isolada do Sprint 3: SQLite em memoria e Gutendex bloqueado por mock."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["MIGRATIONS_DATABASE_URL"] = ""
os.environ["JWT_SECRET_KEY"] = "sprint3-test-only-secret-not-for-production"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from app.db.base import Base
from app.db.database import get_db
from app.models.admin import Admin
from app.models.news import Noticia
from app.core.security import create_access_token

BOOK = {"id": 84, "title": "Frankenstein", "authors": [{"name": "Mary Shelley"}],
        "formats": {"image/jpeg": "https://example.invalid/cover.jpg",
                    "application/epub+zip": "https://example.invalid/book.epub"}}

@pytest.fixture
def upstream(monkeypatch):
    state = {"status": 200, "json": BOOK, "requests": []}
    original = httpx.AsyncClient
    def handle(request):
        state["requests"].append(request)
        if "error" in state:
            raise state["error"]("simulated", request=request)
        if "content" in state:
            return httpx.Response(state["status"], content=state["content"])
        return httpx.Response(state["status"], json=state["json"])
    def factory(*args, **kwargs):
        return original(*args, **kwargs, transport=httpx.MockTransport(handle))
    monkeypatch.setattr(httpx, "AsyncClient", factory)
    return state

@pytest.fixture
def api(upstream):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    sessions = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    with sessions() as db:
        db.add(Admin(id=1, usuario="sprint-admin", senha_hash="not-used-by-these-tests"))
        db.commit()
    def database():
        with sessions() as db:
            yield db
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = database
    try:
        with TestClient(app) as client:
            yield client, {"Authorization": "Bearer " + create_access_token("1")}, sessions
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()

def seed_news(sessions, **values):
    payload = {"titulo": "Noticia", "conteudo": "Conteudo", "publicada": False, "destaque": False, "ordem": 0, **values}
    with sessions() as db:
        row = Noticia(**payload)
        db.add(row)
        db.commit()
        return row.id
