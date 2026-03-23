from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from domain.entities.models import Workout
from domain.ports.interfaces import WorkoutRepository
from infrastructure.db.models import WorkoutModel


class WorkoutRepositoryImpl(WorkoutRepository):
    def __init__(self, session: Session):
        self._session = session

    def add_workout(
        self,
        *,
        user_id: int,
        workout_type: str,
        duration_minutes: int,
        calories_burned: int | None,
    ) -> Workout:
        raise NotImplementedError("WorkoutRepositoryImpl.add_workout not implemented yet")

    def list_workouts_today(self, *, user_id: int, day: date) -> list[Workout]:
        raise NotImplementedError("WorkoutRepositoryImpl.list_workouts_today not implemented yet")

