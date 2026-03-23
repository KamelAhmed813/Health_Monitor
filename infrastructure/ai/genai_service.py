from __future__ import annotations

from typing import Any

from domain.ports.interfaces import AIService, AiMealContext, WorkoutRepository


class GenAiService(AIService):
    def __init__(self, *, api_key: str):
        self._api_key = api_key

        # Intentionally not initializing SDK clients here for skeleton simplicity.
        # Production wiring should validate api_key and configure retry/timeouts.

    def analyze_meal(self, *, context: AiMealContext) -> str:
        # Placeholder output for skeleton.
        return "AI meal analysis placeholder (implement Google GenAI call later)."

    def workout_feedback(self, *, workout: Any, user_id: int) -> str:
        return "AI workout feedback placeholder (implement Google GenAI call later)."

    def plan_meals_next_day(self, *, user_id: int, day: Any) -> list[dict[str, Any]]:
        return [
            {"meal_type": "breakfast", "items": [{"name": "placeholder", "quantity": "1", "calories": None}]},
            {"meal_type": "lunch", "items": [{"name": "placeholder", "quantity": "1", "calories": None}]},
            {"meal_type": "dinner", "items": [{"name": "placeholder", "quantity": "1", "calories": None}]},
        ]

