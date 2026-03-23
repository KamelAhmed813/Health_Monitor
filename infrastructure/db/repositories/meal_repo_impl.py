from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import Meal, MealItem
from domain.ports.interfaces import MealRepository
from infrastructure.db.models import MealItemModel, MealModel


class MealRepositoryImpl(MealRepository):
    def __init__(self, session: Session):
        self._session = session

    def add_meal(
        self,
        *,
        user_id: int,
        meal_type: str,
        meal_date: date,
        notes: str | None,
    ) -> Meal:
        raise NotImplementedError("MealRepositoryImpl.add_meal not implemented yet")

    def add_meal_item(
        self,
        *,
        meal_id: int,
        name: str,
        quantity: str,
        calories: int | None,
    ) -> MealItem:
        raise NotImplementedError("MealRepositoryImpl.add_meal_item not implemented yet")

    def list_meals_today(self, *, user_id: int, day: date) -> list[Meal]:
        raise NotImplementedError("MealRepositoryImpl.list_meals_today not implemented yet")

