from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import Meal, MealItem
from domain.ports.interfaces import CacheService, MealRepository
from infrastructure.db.models import MealItemModel, MealModel


class MealRepositoryImpl(MealRepository):
    _TTL_SECONDS = 600

    def __init__(self, session: Session, cache: CacheService):
        self._session = session
        self._cache = cache

    def add_meal(
        self,
        *,
        user_id: int,
        meal_type: str,
        meal_date: date,
        notes: str | None,
    ) -> Meal:
        row = MealModel(
            user_id=user_id,
            meal_type=meal_type,
            meal_date=meal_date,
            notes=notes,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        meal = self._to_meal_domain(row)
        self._cache.delete(self._list_key(user_id, meal_date), self._dashboard_key(user_id, meal_date))
        return meal

    def add_meal_item(
        self,
        *,
        meal_id: int,
        name: str,
        quantity: str,
        calories: int | None,
    ) -> MealItem:
        row = MealItemModel(meal_id=meal_id, name=name, quantity=quantity, calories=calories)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        meal = self._session.query(MealModel).filter(MealModel.id == meal_id).first()
        if meal is not None:
            self._cache.delete(self._list_key(meal.user_id, meal.meal_date), self._dashboard_key(meal.user_id, meal.meal_date))
        return self._to_meal_item_domain(row)

    def list_meals_today(self, *, user_id: int, day: date) -> list[Meal]:
        key = self._list_key(user_id, day)
        cached = self._cache.get(key)
        if isinstance(cached, list):
            return [self._from_cache_item(item) for item in cached if isinstance(item, dict)]

        rows = (
            self._session.query(MealModel)
            .filter(MealModel.user_id == user_id)
            .filter(MealModel.meal_date == day)
            .order_by(MealModel.id.desc())
            .all()
        )
        meals = [self._to_meal_domain(row) for row in rows]
        self._cache.set(key, [self._to_cache_item(item) for item in meals], ttl_seconds=self._TTL_SECONDS)
        return meals

    @staticmethod
    def _to_meal_domain(row: MealModel) -> Meal:
        return Meal(
            id=row.id,
            user_id=row.user_id,
            meal_type=row.meal_type,
            meal_date=row.meal_date,
            notes=row.notes,
        )

    @staticmethod
    def _to_meal_item_domain(row: MealItemModel) -> MealItem:
        return MealItem(
            id=row.id,
            meal_id=row.meal_id,
            name=row.name,
            quantity=row.quantity,
            calories=row.calories,
        )

    @staticmethod
    def _to_cache_item(meal: Meal) -> dict[str, int | str | None]:
        return {
            "id": meal.id,
            "user_id": meal.user_id,
            "meal_type": meal.meal_type,
            "meal_date": meal.meal_date.isoformat(),
            "notes": meal.notes,
        }

    @staticmethod
    def _from_cache_item(item: dict) -> Meal:
        return Meal(
            id=int(item["id"]),
            user_id=int(item["user_id"]),
            meal_type=str(item["meal_type"]),
            meal_date=date.fromisoformat(str(item["meal_date"])),
            notes=str(item["notes"]) if item.get("notes") is not None else None,
        )

    @staticmethod
    def _list_key(user_id: int, day: date) -> str:
        return f"cache:meals:{user_id}:{day.isoformat()}"

    @staticmethod
    def _dashboard_key(user_id: int, day: date) -> str:
        return f"cache:dashboard:{user_id}:{day.isoformat()}"

