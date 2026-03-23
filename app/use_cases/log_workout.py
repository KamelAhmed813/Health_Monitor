from __future__ import annotations

from domain.entities.models import Workout
from domain.ports.interfaces import WorkoutRepository


def log_workout(
    *,
    user_id: int,
    workout_type: str,
    duration_minutes: int,
    calories_burned: int | None,
    workout_repo: WorkoutRepository,
) -> Workout:
    return workout_repo.add_workout(
        user_id=user_id,
        workout_type=workout_type,
        duration_minutes=duration_minutes,
        calories_burned=calories_burned,
    )

