from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from config.settings import settings
from jose import JWTError, jwt
from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return _pwd_context.verify(plain_password, password_hash)
    except Exception:
        return False


def create_access_token(*, subject: str | int, expires_in_minutes: int | None = None) -> str:
    expire_minutes = expires_in_minutes or settings.jwt_access_token_exp_minutes
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expire_minutes)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise ValueError("Invalid JWT") from e

