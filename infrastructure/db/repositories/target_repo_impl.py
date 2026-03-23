from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import DailyTarget
from domain.ports.interfaces import TargetRepository
from infrastructure.db.models import DailyTargetModel


class TargetRepositoryImpl(TargetRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_or_create_targets_today(
        self,
        *,
        user_id: int,
        day: date,
    ) -> DailyTarget:
        raise NotImplementedError("TargetRepositoryImpl.get_or_create_targets_today not implemented yet")

    def update_targets(
        self,
        *,
        user_id: int,
        day: date,
        calories_target: int,
        water_target_ml: int,
        protein_target_g: int,
        carbs_target_g: int,
        fat_target_g: int,
    ) -> DailyTarget:
        raise NotImplementedError("TargetRepositoryImpl.update_targets not implemented yet")

