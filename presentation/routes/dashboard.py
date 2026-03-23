from __future__ import annotations

from datetime import date as date_type, datetime, timezone

from fastapi import APIRouter, Depends, Query

from app.use_cases.get_dashboard_today import get_dashboard_today
from domain.ports.interfaces import CacheService
from presentation.dependencies import (
    get_cache,
    get_current_user_id,
    get_meal_repo,
    get_target_repo,
    get_water_repo,
    get_workout_repo,
)
from presentation.schemas.dashboard import DashboardResponse


router = APIRouter()


@router.get("/today", response_model=DashboardResponse)
def dashboard_today(
    user_id: int = Depends(get_current_user_id),
    day: str | None = Query(default=None, description="YYYY-MM-DD"),
):
    if day is None:
        day_obj = datetime.now(timezone.utc).date()
    else:
        day_obj = date_type.fromisoformat(day)

    cache: CacheService = get_cache()
    return DashboardResponse(
        data=get_dashboard_today(
            user_id=user_id,
            day=day_obj,
            workout_repo=get_workout_repo(),
            meal_repo=get_meal_repo(),
            water_repo=get_water_repo(),
            target_repo=get_target_repo(),
            cache=cache,
        )
    )

