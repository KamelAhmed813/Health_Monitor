from __future__ import annotations

from domain.entities.models import User
from domain.ports.interfaces import UserRepository


def auth_register(*, email: str, password_hash: str, user_repo: UserRepository) -> User:
    """
    Register a new user.

    This is a skeleton implementation; wire validation/business rules later.
    """

    raise NotImplementedError("auth_register use case not implemented yet")

