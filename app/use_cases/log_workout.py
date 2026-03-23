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
    raise NotImplementedError("log_workout use case not implemented yet")

