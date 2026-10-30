from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


@pytest.fixture(autouse=True)
def configure_test_secret(monkeypatch):
    monkeypatch.setattr(
        settings,
        "jwt_secret_key",
        "chave-de-teste-jwt-com-mais-de-32-bytes"
    )


def test_hash_password():
    hashed = hash_password("Senha123!")

    assert hashed.startswith("$argon2")
    assert hashed != "Senha123!"


def test_verify_password():
    hashed = hash_password("Senha123!")

    assert verify_password("Senha123!", hashed)
    assert not verify_password("senha-errada", hashed)


def test_create_and_decode_token():
    token = create_access_token("admin-teste")
    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "admin-teste"


def test_invalid_token():
    assert decode_access_token("token-invalido") is None


def test_expired_token():
    now = datetime.now(timezone.utc)

    payload = {
        "sub": "admin-teste",
        "iat": now - timedelta(hours=2),
        "exp": now - timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    assert decode_access_token(token) is None