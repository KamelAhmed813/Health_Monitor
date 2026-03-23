from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import WaterLog
from domain.ports.interfaces import WaterRepository
from infrastructure.db.models import WaterLogModel


class WaterRepositoryImpl(WaterRepository):
    def __init__(self, session: Session):
        self._session = session

    def log_water(self, *, user_id: int, log_date: date, amount_ml: int) -> WaterLog:
        raise NotImplementedError("WaterRepositoryImpl.log_water not implemented yet")

    def get_total_water_today(self, *, user_id: int, day: date) -> int:
        raise NotImplementedError("WaterRepositoryImpl.get_total_water_today not implemented yet")

