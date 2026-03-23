from __future__ import annotations

from datetime import date as date_type

from fastapi import APIRouter, Depends

from app.use_cases.ai_analyze_meal import ai_analyze_meal
from app.use_cases.ai_plan_meals_next_day import ai_plan_meals_next_day
from app.use_cases.ai_workout_feedback import ai_workout_feedback
from presentation.dependencies import get_ai_service, get_current_user_id
from presentation.schemas.ai import (
    AiAnalyzeMealRequest,
    AiAnalyzeMealResponse,
    AiPlanMealsNextDayRequest,
    AiPlanMealsNextDayResponse,
    AiWorkoutFeedbackRequest,
    AiWorkoutFeedbackResponse,
)


router = APIRouter()


@router.post("/analyze-meal", response_model=AiAnalyzeMealResponse)
def analyze_meal(
    request: AiAnalyzeMealRequest,
    user_id: int = Depends(get_current_user_id),
):
    ai_service = get_ai_service()
    analysis = ai_analyze_meal(user_id=user_id, meal_payload=request.meal_payload, ai_service=ai_service)
    return AiAnalyzeMealResponse(analysis=analysis)


@router.post("/workout-feedback", response_model=AiWorkoutFeedbackResponse)
def workout_feedback(
    request: AiWorkoutFeedbackRequest,
    user_id: int = Depends(get_current_user_id),
):
    ai_service = get_ai_service()
    feedback = ai_workout_feedback(user_id=user_id, workout_payload=request.workout_payload, ai_service=ai_service)
    return AiWorkoutFeedbackResponse(feedback=feedback)


@router.post("/plan-next-day", response_model=AiPlanMealsNextDayResponse)
def plan_next_day(
    request: AiPlanMealsNextDayRequest,
    user_id: int = Depends(get_current_user_id),
):
    ai_service = get_ai_service()
    # request.day_payload is left flexible; next-day planning will use it later.
    day = date_type.fromisoformat(request.day_payload.get("day")) if isinstance(request.day_payload, dict) else None
    plan = ai_plan_meals_next_day(user_id=user_id, day=day, ai_service=ai_service)  # type: ignore[arg-type]
    return AiPlanMealsNextDayResponse(plan=plan)

