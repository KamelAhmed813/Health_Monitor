from __future__ import annotations

from domain.ports.interfaces import AIService


def ai_workout_feedback(*, user_id: int, workout_payload: dict, ai_service: AIService) -> str:
    """
    Provide AI feedback after a workout.
    """

    raise NotImplementedError("ai_workout_feedback use case not implemented yet")

