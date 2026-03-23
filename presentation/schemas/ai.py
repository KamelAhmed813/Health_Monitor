from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AiAnalyzeMealRequest(BaseModel):
    meal_payload: dict[str, Any]


class AiAnalyzeMealResponse(BaseModel):
    analysis: str


class AiWorkoutFeedbackRequest(BaseModel):
    workout_payload: dict[str, Any]


class AiWorkoutFeedbackResponse(BaseModel):
    feedback: str


class AiPlanMealsNextDayRequest(BaseModel):
    day_payload: dict[str, Any]


class AiPlanMealsNextDayResponse(BaseModel):
    plan: list[dict[str, Any]]

