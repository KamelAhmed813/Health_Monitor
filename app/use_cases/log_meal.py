from __future__ import annotations

from domain.entities.models import Meal, MealItem
from domain.ports.interfaces import MealRepository


def log_meal(
    *,
    user_id: int,
    meal_type: str,
    meal_date: str,  # ISO date string (YYYY-MM-DD) for request DTO simplicity
    notes: str | None,
    items: list[dict],  # [{name, quantity, calories?}, ...]
    meal_repo: MealRepository,
) -> Meal:
    raise NotImplementedError("log_meal use case not implemented yet")

