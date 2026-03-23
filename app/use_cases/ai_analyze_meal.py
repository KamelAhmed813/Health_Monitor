from __future__ import annotations

from domain.ports.interfaces import AIService


def ai_analyze_meal(*, user_id: int, meal_payload: dict, ai_service: AIService) -> str:
    """
    Analyze a meal (nutrition + suggestions).
    """

    raise NotImplementedError("ai_analyze_meal use case not implemented yet")

