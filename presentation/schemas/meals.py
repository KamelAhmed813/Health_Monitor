from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class MealItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    quantity: str = Field(min_length=1, max_length=100)
    calories: Optional[int] = Field(default=None, ge=0)


class LogMealRequest(BaseModel):
    meal_type: str = Field(min_length=1, max_length=50)
    meal_date: str = Field(description="YYYY-MM-DD")
    notes: Optional[str] = Field(default=None, max_length=1000)
    items: list[MealItemRequest]

