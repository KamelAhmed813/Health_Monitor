from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import DailyTarget
from domain.ports.interfaces import CacheService, TargetRepository
from infrastructure.db.models import DailyTargetModel


class TargetRepositoryImpl(TargetRepository):
    _TTL_SECONDS = 900
    _DEFAULT_CALORIES = 2200
    _DEFAULT_WATER_ML = 2500
    _DEFAULT_PROTEIN_G = 120
    _DEFAULT_CARBS_G = 250
    _DEFAULT_FAT_G = 70

    def __init__(self, session: Session, cache: CacheService):
        self._session = session
        self._cache = cache

    def get_or_create_targets_today(
        self,
        *,
        user_id: int,
        day: date,
    ) -> DailyTarget:
        key = self._key(user_id, day)
        cached = self._cache.get(key)
        if isinstance(cached, dict):
            return self._from_cache_item(cached)

        row = (
            self._session.query(DailyTargetModel)
            .filter(DailyTargetModel.user_id == user_id)
            .filter(DailyTargetModel.target_date == day)
            .first()
        )
        if row is None:
            row = DailyTargetModel(
                user_id=user_id,
                target_date=day,
                calories_target=self._DEFAULT_CALORIES,
                water_target_ml=self._DEFAULT_WATER_ML,
                protein_target_g=self._DEFAULT_PROTEIN_G,
                carbs_target_g=self._DEFAULT_CARBS_G,
                fat_target_g=self._DEFAULT_FAT_G,
            )
            self._session.add(row)
            self._session.commit()
            self._session.refresh(row)

        target = self._to_domain(row)
        self._cache.set(key, self._to_cache_item(target), ttl_seconds=self._TTL_SECONDS)
        return target

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
        row = (
            self._session.query(DailyTargetModel)
            .filter(DailyTargetModel.user_id == user_id)
            .filter(DailyTargetModel.target_date == day)
            .first()
        )
        if row is None:
            row = DailyTargetModel(user_id=user_id, target_date=day)
            self._session.add(row)

        row.calories_target = calories_target
        row.water_target_ml = water_target_ml
        row.protein_target_g = protein_target_g
        row.carbs_target_g = carbs_target_g
        row.fat_target_g = fat_target_g
        self._session.commit()
        self._session.refresh(row)

        target = self._to_domain(row)
        self._cache.set(self._key(user_id, day), self._to_cache_item(target), ttl_seconds=self._TTL_SECONDS)
        self._cache.delete(self._dashboard_key(user_id, day))
        return target

    @staticmethod
    def _to_domain(row: DailyTargetModel) -> DailyTarget:
        return DailyTarget(
            id=row.id,
            user_id=row.user_id,
            target_date=row.target_date,
            calories_target=row.calories_target,
            water_target_ml=row.water_target_ml,
            protein_target_g=row.protein_target_g,
            carbs_target_g=row.carbs_target_g,
            fat_target_g=row.fat_target_g,
        )

    @staticmethod
    def _to_cache_item(target: DailyTarget) -> dict[str, int | str]:
        return {
            "id": target.id,
            "user_id": target.user_id,
            "target_date": target.target_date.isoformat(),
            "calories_target": target.calories_target,
            "water_target_ml": target.water_target_ml,
            "protein_target_g": target.protein_target_g,
            "carbs_target_g": target.carbs_target_g,
            "fat_target_g": target.fat_target_g,
        }

    @staticmethod
    def _from_cache_item(item: dict) -> DailyTarget:
        return DailyTarget(
            id=int(item["id"]),
            user_id=int(item["user_id"]),
            target_date=date.fromisoformat(str(item["target_date"])),
            calories_target=int(item["calories_target"]),
            water_target_ml=int(item["water_target_ml"]),
            protein_target_g=int(item["protein_target_g"]),
            carbs_target_g=int(item["carbs_target_g"]),
            fat_target_g=int(item["fat_target_g"]),
        )

    @staticmethod
    def _key(user_id: int, day: date) -> str:
        return f"cache:targets:{user_id}:{day.isoformat()}"

    @staticmethod
    def _dashboard_key(user_id: int, day: date) -> str:
        return f"cache:dashboard:{user_id}:{day.isoformat()}"

