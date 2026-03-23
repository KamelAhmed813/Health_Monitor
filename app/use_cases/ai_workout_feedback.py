from __future__ import annotations

from datetime import datetime

from domain.entities.models import Workout
from domain.ports.interfaces import AIService


def ai_workout_feedback(*, user_id: int, workout_payload: dict, ai_service: AIService) -> str:
    """
    Provide AI feedback after a workout.
    """

    workout = Workout(
        id=int(workout_payload.get("id", 0)),
        user_id=user_id,
        workout_type=str(workout_payload.get("workout_type", "workout")),
        duration_minutes=int(workout_payload.get("duration_minutes", 0)),
        calories_burned=int(workout_payload["calories_burned"]) if workout_payload.get("calories_burned") is not None else None,
        created_at=datetime.utcnow(),
    )
    return ai_service.workout_feedback(workout=workout, user_id=user_id)

