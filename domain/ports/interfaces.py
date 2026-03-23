from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol, runtime_checkable

from domain.entities.models import DailyTarget, Meal, MealItem, User, WaterLog, Workout


@runtime_checkable
class UserRepository(Protocol):
    def get_by_email(self, email: str) -> User | None: ...

    def get_by_id(self, user_id: int) -> User | None: ...

    def create(self, email: str, password_hash: str) -> User: ...


@runtime_checkable
class WorkoutRepository(Protocol):
    def add_workout(
        self,
        *,
        user_id: int,
        workout_type: str,
        duration_minutes: int,
        calories_burned: int | None,
    ) -> Workout: ...

    def list_workouts_today(self, *, user_id: int, day: date) -> list[Workout]: ...


@runtime_checkable
class MealRepository(Protocol):
    def add_meal(
        self,
        *,
        user_id: int,
        meal_type: str,
        meal_date: date,
        notes: str | None,
    ) -> Meal: ...

    def add_meal_item(
        self,
        *,
        meal_id: int,
        name: str,
        quantity: str,
        calories: int | None,
    ) -> MealItem: ...

    def list_meals_today(self, *, user_id: int, day: date) -> list[Meal]: ...


@runtime_checkable
class WaterRepository(Protocol):
    def log_water(self, *, user_id: int, log_date: date, amount_ml: int) -> WaterLog: ...

    def get_total_water_today(self, *, user_id: int, day: date) -> int: ...


@runtime_checkable
class TargetRepository(Protocol):
    def get_or_create_targets_today(
        self,
        *,
        user_id: int,
        day: date,
    ) -> DailyTarget: ...

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
    ) -> DailyTarget: ...


@runtime_checkable
class CacheService(Protocol):
    def get(self, key: str) -> Any | None: ...

    def set(self, key: str, value: Any, ttl_seconds: int) -> None: ...

    def delete(self, *keys: str) -> int: ...


@dataclass(frozen=True)
class AiMealContext:
    user_id: int
    meal: Meal
    meals_today: list[Meal]
    water_today_ml: int
    targets_today: DailyTarget | None


@runtime_checkable
class AIService(Protocol):
    def analyze_meal(self, *, context: AiMealContext) -> str: ...

    def workout_feedback(self, *, workout: Workout, user_id: int) -> str: ...

    def plan_meals_next_day(self, *, user_id: int, day: date) -> list[dict[str, Any]]: ...

