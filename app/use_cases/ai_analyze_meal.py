from __future__ import annotations

from datetime import date

from domain.entities.models import Meal
from domain.ports.interfaces import AIService, AiMealContext


def ai_analyze_meal(*, user_id: int, meal_payload: dict, ai_service: AIService) -> str:
    """
    Analyze a meal (nutrition + suggestions).
    """

    meal = Meal(
        id=int(meal_payload.get("meal_id", 0)),
        user_id=user_id,
        meal_type=str(meal_payload.get("meal_type", "meal")),
        meal_date=date.fromisoformat(str(meal_payload.get("meal_date", date.today().isoformat()))),
        notes=str(meal_payload.get("notes")) if meal_payload.get("notes") is not None else None,
    )
    context = AiMealContext(
        user_id=user_id,
        meal=meal,
        meals_today=[],
        water_today_ml=0,
        targets_today=None,
    )
    return ai_service.analyze_meal(context=context)

