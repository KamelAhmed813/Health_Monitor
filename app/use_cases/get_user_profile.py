from __future__ import annotations

from domain.ports.interfaces import UserRepository


def get_user_profile(*, user_id: int, user_repo: UserRepository) -> dict:
    """
    Return user profile view model.
    """

    raise NotImplementedError("get_user_profile use case not implemented yet")

