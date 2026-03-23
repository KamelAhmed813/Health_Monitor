from __future__ import annotations

from fastapi import APIRouter, Depends

from app.use_cases.log_workout import log_workout
from domain.entities.models import Workout
from presentation.dependencies import get_current_user_id, get_workout_repo
from presentation.schemas.workouts import LogWorkoutRequest, WorkoutResponse


router = APIRouter()


@router.post("", response_model=WorkoutResponse)
def create_workout(
    request: LogWorkoutRequest,
    user_id: int = Depends(get_current_user_id),
):
    workout_repo = get_workout_repo()
    workout: Workout = log_workout(
        user_id=user_id,
        workout_type=request.workout_type,
        duration_minutes=request.duration_minutes,
        calories_burned=request.calories_burned,
        workout_repo=workout_repo,
    )

    return WorkoutResponse(
        id=workout.id,
        workout_type=workout.workout_type,
        duration_minutes=workout.duration_minutes,
        calories_burned=workout.calories_burned,
    )

