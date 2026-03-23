from __future__ import annotations

from domain.entities.models import User
from domain.ports.interfaces import UserRepository


def auth_register(*, email: str, password_hash: str, user_repo: UserRepository) -> User:
    """
    Register a new user.

    This is a skeleton implementation; wire validation/business rules later.
    """

    existing = user_repo.get_by_email(email)
    if existing is not None:
        raise ValueError("Email already registered")
    return user_repo.create(email=email, password_hash=password_hash)

