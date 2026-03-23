from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class User:
    id: int
    email: str
    password_hash: str
    created_at: datetime


@dataclass(frozen=True)
class Workout:
    id: int
    user_id: int
    workout_type: str
    duration_minutes: int
    calories_burned: Optional[int]
    created_at: datetime


@dataclass(frozen=True)
class MealItem:
    id: int
    meal_id: int
    name: str
    quantity: str
    calories: Optional[int]


@dataclass(frozen=True)
class Meal:
    id: int
    user_id: int
    meal_type: str  # breakfast/lunch/dinner/snack
    meal_date: date
    notes: Optional[str]


@dataclass(frozen=True)
class WaterLog:
    id: int
    user_id: int
    log_date: date
    amount_ml: int
    created_at: datetime


@dataclass(frozen=True)
class DailyTarget:
    id: int
    user_id: int
    target_date: date
    calories_target: int
    water_target_ml: int
    protein_target_g: int
    carbs_target_g: int
    fat_target_g: int

