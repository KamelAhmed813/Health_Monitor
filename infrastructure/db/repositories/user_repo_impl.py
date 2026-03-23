from __future__ import annotations

from sqlalchemy.orm import Session

from domain.entities.models import User
from domain.ports.interfaces import UserRepository
from infrastructure.db.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError("UserRepositoryImpl.get_by_email not implemented yet")

    def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError("UserRepositoryImpl.get_by_id not implemented yet")

    def create(self, email: str, password_hash: str) -> User:
        raise NotImplementedError("UserRepositoryImpl.create not implemented yet")

