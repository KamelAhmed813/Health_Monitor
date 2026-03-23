from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from domain.entities.models import User
from domain.ports.interfaces import CacheService, UserRepository
from infrastructure.db.models import UserModel


class UserRepositoryImpl(UserRepository):
    _TTL_SECONDS = 1800

    def __init__(self, session: Session, cache: CacheService):
        self._session = session
        self._cache = cache

    def get_by_email(self, email: str) -> User | None:
        email_key = self._email_key(email)
        cached = self._cache.get(email_key)
        if isinstance(cached, dict):
            return User(
                id=int(cached["id"]),
                email=str(cached["email"]),
                password_hash=str(cached["password_hash"]),
                created_at=datetime.fromisoformat(str(cached["created_at"])),
            )

        row = self._session.query(UserModel).filter(UserModel.email == email.lower()).first()
        if row is None:
            return None
        user = self._to_domain(row)
        self._write_through(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        id_key = self._id_key(user_id)
        cached = self._cache.get(id_key)
        if isinstance(cached, dict):
            return User(
                id=int(cached["id"]),
                email=str(cached["email"]),
                password_hash=str(cached["password_hash"]),
                created_at=datetime.fromisoformat(str(cached["created_at"])),
            )

        row = self._session.query(UserModel).filter(UserModel.id == user_id).first()
        if row is None:
            return None
        user = self._to_domain(row)
        self._write_through(user)
        return user

    def create(self, email: str, password_hash: str) -> User:
        email_normalized = email.lower()
        row = UserModel(email=email_normalized, password_hash=password_hash)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        user = self._to_domain(row)
        self._write_through(user)
        return user

    @staticmethod
    def _to_domain(row: UserModel) -> User:
        return User(id=row.id, email=row.email, password_hash=row.password_hash, created_at=row.created_at)

    @staticmethod
    def _to_cache_payload(user: User) -> dict[str, str | int]:
        return {
            "id": user.id,
            "email": user.email,
            "password_hash": user.password_hash,
            "created_at": user.created_at.isoformat(),
        }

    def _write_through(self, user: User) -> None:
        payload = self._to_cache_payload(user)
        self._cache.set(self._id_key(user.id), payload, ttl_seconds=self._TTL_SECONDS)
        self._cache.set(self._email_key(user.email), payload, ttl_seconds=self._TTL_SECONDS)

    @staticmethod
    def _id_key(user_id: int) -> str:
        return f"cache:user:{user_id}"

    @staticmethod
    def _email_key(email: str) -> str:
        return f"cache:user_email:{email.lower()}"

