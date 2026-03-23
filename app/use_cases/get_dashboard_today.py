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

    key = f"cache:dashboard:{user_id}:{day.isoformat()}"
    cached = cache.get(key)
    if isinstance(cached, dict):
        return cached

    workouts = workout_repo.list_workouts_today(user_id=user_id, day=day)
    meals = meal_repo.list_meals_today(user_id=user_id, day=day)
    water_today_ml = water_repo.get_total_water_today(user_id=user_id, day=day)
    targets = target_repo.get_or_create_targets_today(user_id=user_id, day=day)

    total_workout_minutes = sum(item.duration_minutes for item in workouts)
    total_calories_burned = sum(item.calories_burned or 0 for item in workouts)
    dashboard = {
        "date": day.isoformat(),
        "workouts_count": len(workouts),
        "meals_count": len(meals),
        "water_today_ml": water_today_ml,
        "workout_summary": {
            "total_minutes": total_workout_minutes,
            "total_calories_burned": total_calories_burned,
        },
        "targets": {
            "calories_target": targets.calories_target,
            "water_target_ml": targets.water_target_ml,
            "protein_target_g": targets.protein_target_g,
            "carbs_target_g": targets.carbs_target_g,
            "fat_target_g": targets.fat_target_g,
        },
    }
    cache.set(key, dashboard, ttl_seconds=300)
    return dashboard

