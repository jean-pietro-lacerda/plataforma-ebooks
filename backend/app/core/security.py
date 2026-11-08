from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.core.config import settings


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("A senha não pode ser vazia.")

    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(hashed_password, password)

    except (VerificationError, InvalidHashError):
        return False


def get_jwt_secret_key() -> str:
    secret_key = settings.jwt_secret_key

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY não foi configurada.")

    return secret_key


def create_access_token(subject: str) -> str:
    if not subject:
        raise ValueError("O identificador do usuário é obrigatório.")

    if settings.access_token_expire_minutes <= 0:
        raise ValueError("A validade do token precisa ser positiva.")

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    }

    return jwt.encode(
        payload,
        get_jwt_secret_key(),
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            get_jwt_secret_key(),
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp"]}
        )

    except jwt.InvalidTokenError:
        return None

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject:
        return None

    return payload