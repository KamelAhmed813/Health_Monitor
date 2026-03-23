from __future__ import annotations

from app.errors import UnauthorizedError
from domain.ports.interfaces import UserRepository

from presentation.security.jwt import create_access_token, verify_password


def auth_login(*, email: str, password: str, user_repo: UserRepository) -> str:
    """
    Authenticate user and return a JWT access token.
    """

    user = user_repo.get_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    return create_access_token(subject=user.id)

