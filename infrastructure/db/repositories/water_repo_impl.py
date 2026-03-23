from __future__ import annotations

from datetime import date
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from domain.entities.models import WaterLog
from domain.ports.interfaces import CacheService, WaterRepository
from infrastructure.db.models import WaterLogModel


class WaterRepositoryImpl(WaterRepository):
    _TTL_SECONDS = 600

    def __init__(self, session: Session, cache: CacheService):
        self._session = session
        self._cache = cache

    def log_water(self, *, user_id: int, log_date: date, amount_ml: int) -> WaterLog:
        row = WaterLogModel(user_id=user_id, log_date=log_date, amount_ml=amount_ml)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        water_log = self._to_domain(row)
        self._cache.delete(self._total_key(user_id, log_date), self._dashboard_key(user_id, log_date))
        return water_log

    def get_total_water_today(self, *, user_id: int, day: date) -> int:
        key = self._total_key(user_id, day)
        cached = self._cache.get(key)
        if isinstance(cached, int):
            return cached
        if isinstance(cached, str) and cached.isdigit():
            return int(cached)

        total = (
            self._session.query(func.coalesce(func.sum(WaterLogModel.amount_ml), 0))
            .filter(WaterLogModel.user_id == user_id)
            .filter(WaterLogModel.log_date == day)
            .scalar()
        )
        total_int = int(total or 0)
        self._cache.set(key, total_int, ttl_seconds=self._TTL_SECONDS)
        return total_int

    @staticmethod
    def _to_domain(row: WaterLogModel) -> WaterLog:
        return WaterLog(
            id=row.id,
            user_id=row.user_id,
            log_date=row.log_date,
            amount_ml=row.amount_ml,
            created_at=row.created_at,
        )

    @staticmethod
    def _total_key(user_id: int, day: date) -> str:
        return f"cache:water_total:{user_id}:{day.isoformat()}"

    @staticmethod
    def _dashboard_key(user_id: int, day: date) -> str:
        return f"cache:dashboard:{user_id}:{day.isoformat()}"

