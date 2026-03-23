from __future__ import annotations

from datetime import date

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
    parsed_date = date.fromisoformat(meal_date)
    meal = meal_repo.add_meal(
        user_id=user_id,
        meal_type=meal_type,
        meal_date=parsed_date,
        notes=notes,
    )
    for item in items:
        meal_repo.add_meal_item(
            meal_id=meal.id,
            name=str(item["name"]),
            quantity=str(item["quantity"]),
            calories=int(item["calories"]) if item.get("calories") is not None else None,
        )
    return meal

