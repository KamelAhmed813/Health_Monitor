from __future__ import annotations

from domain.ports.interfaces import UserRepository

from presentation.security.jwt import create_access_token, verify_password


def auth_login(*, email: str, password: str, user_repo: UserRepository) -> str:
    """
    Authenticate user and return a JWT access token.
    """

    raise NotImplementedError("auth_login use case not implemented yet")

