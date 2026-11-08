import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.database import get_db
from app.models.admin import Admin


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        settings,
        "jwt_secret_key",
        "chave-de-teste-com-mais-de-32-bytes"
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        admin = Admin(
            usuario="admin-teste",
            senha_hash=hash_password("SenhaTeste123!"),
        )
        db.add(admin)
        db.commit()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous_overrides)

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_login_success(client):
    response = client.post(
        "/auth/login",
        json={
            "usuario": "admin-teste",
            "senha": "SenhaTeste123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login",
        json={
            "usuario": "admin-teste",
            "senha": "senha-incorreta",
        },
    )

    assert response.status_code == 401


def test_login_unknown_admin(client):
    response = client.post(
        "/auth/login",
        json={
            "usuario": "usuario-inexistente",
            "senha": "SenhaTeste123!",
        },
    )

    assert response.status_code == 401


def test_profile_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_profile_with_valid_token(client):
    login_response = client.post(
        "/auth/login",
        json={
            "usuario": "admin-teste",
            "senha": "SenhaTeste123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["usuario"] == "admin-teste"
    assert "senha_hash" not in response.json()