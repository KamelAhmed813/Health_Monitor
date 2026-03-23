from __future__ import annotations

from datetime import date
from datetime import datetime

from sqlalchemy.orm import Session

from domain.entities.models import Workout
from domain.ports.interfaces import CacheService, WorkoutRepository
from infrastructure.db.models import WorkoutModel


class WorkoutRepositoryImpl(WorkoutRepository):
    _TTL_SECONDS = 600

    def __init__(self, session: Session, cache: CacheService):
        self._session = session
        self._cache = cache

    def add_workout(
        self,
        *,
        user_id: int,
        workout_type: str,
        duration_minutes: int,
        calories_burned: int | None,
    ) -> Workout:
        row = WorkoutModel(
            user_id=user_id,
            workout_type=workout_type,
            duration_minutes=duration_minutes,
            calories_burned=calories_burned,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        workout = self._to_domain(row)
        day = workout.created_at.date()
        self._cache.delete(self._list_key(user_id, day), self._dashboard_key(user_id, day))
        return workout

    def list_workouts_today(self, *, user_id: int, day: date) -> list[Workout]:
        key = self._list_key(user_id, day)
        cached = self._cache.get(key)
        if isinstance(cached, list):
            return [self._from_cache_item(item) for item in cached if isinstance(item, dict)]

        start_dt = datetime.combine(day, datetime.min.time())
        end_dt = datetime.combine(day, datetime.max.time())
        rows = (
            self._session.query(WorkoutModel)
            .filter(WorkoutModel.user_id == user_id)
            .filter(WorkoutModel.created_at >= start_dt)
            .filter(WorkoutModel.created_at <= end_dt)
            .order_by(WorkoutModel.created_at.desc())
            .all()
        )
        workouts = [self._to_domain(row) for row in rows]
        self._cache.set(key, [self._to_cache_item(item) for item in workouts], ttl_seconds=self._TTL_SECONDS)
        return workouts

    @staticmethod
    def _to_domain(row: WorkoutModel) -> Workout:
        return Workout(
            id=row.id,
            user_id=row.user_id,
            workout_type=row.workout_type,
            duration_minutes=row.duration_minutes,
            calories_burned=row.calories_burned,
            created_at=row.created_at,
        )

    @staticmethod
    def _to_cache_item(workout: Workout) -> dict[str, int | str | None]:
        return {
            "id": workout.id,
            "user_id": workout.user_id,
            "workout_type": workout.workout_type,
            "duration_minutes": workout.duration_minutes,
            "calories_burned": workout.calories_burned,
            "created_at": workout.created_at.isoformat(),
        }

    @staticmethod
    def _from_cache_item(item: dict) -> Workout:
        return Workout(
            id=int(item["id"]),
            user_id=int(item["user_id"]),
            workout_type=str(item["workout_type"]),
            duration_minutes=int(item["duration_minutes"]),
            calories_burned=int(item["calories_burned"]) if item.get("calories_burned") is not None else None,
            created_at=datetime.fromisoformat(str(item["created_at"])),
        )

    @staticmethod
    def _list_key(user_id: int, day: date) -> str:
        return f"cache:workouts:{user_id}:{day.isoformat()}"

    @staticmethod
    def _dashboard_key(user_id: int, day: date) -> str:
        return f"cache:dashboard:{user_id}:{day.isoformat()}"

