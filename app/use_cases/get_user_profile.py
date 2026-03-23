from __future__ import annotations

from domain.ports.interfaces import UserRepository


def get_user_profile(*, user_id: int, user_repo: UserRepository) -> dict:
    """
    Return user profile view model.
    """

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }

