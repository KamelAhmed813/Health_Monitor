from __future__ import annotations

from datetime import date

from domain.ports.interfaces import AIService


def ai_plan_meals_next_day(*, user_id: int, day: date, ai_service: AIService) -> list[dict]:
    """
    Plan meals for the next day using AI and the user's historical data.
    """

    raise NotImplementedError("ai_plan_meals_next_day use case not implemented yet")

