from __future__ import annotations

from datetime import date

from domain.ports.interfaces import CacheService, MealRepository, TargetRepository, WaterRepository, WorkoutRepository


def get_dashboard_today(
    *,
    user_id: int,
    day: date,
    workout_repo: WorkoutRepository,
    meal_repo: MealRepository,
    water_repo: WaterRepository,
    target_repo: TargetRepository,
    cache: CacheService,
) -> dict:
    """
    Returns today's dashboard view model.
    """

    raise NotImplementedError("get_dashboard_today use case not implemented yet")

