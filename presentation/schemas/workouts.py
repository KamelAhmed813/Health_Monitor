from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class LogWorkoutRequest(BaseModel):
    workout_type: str = Field(min_length=1, max_length=100)
    duration_minutes: int = Field(gt=0)
    calories_burned: Optional[int] = Field(default=None, ge=0)


class WorkoutResponse(BaseModel):
    id: int
    workout_type: str
    duration_minutes: int
    calories_burned: Optional[int]

