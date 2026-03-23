from __future__ import annotations

from datetime import date, timedelta

from domain.ports.interfaces import AIService


def ai_plan_meals_next_day(*, user_id: int, day: date, ai_service: AIService) -> list[dict]:
    """
    Plan meals for the next day using AI and the user's historical data.
    """

    target_day = day + timedelta(days=1)
    return ai_service.plan_meals_next_day(user_id=user_id, day=target_day)

