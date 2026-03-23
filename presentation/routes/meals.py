from __future__ import annotations

from fastapi import APIRouter, Depends

from app.use_cases.log_meal import log_meal
from presentation.dependencies import get_current_user_id, get_meal_repo
from presentation.schemas.meals import LogMealRequest


router = APIRouter()


@router.post("", summary="Log a meal")
def create_meal(
    request: LogMealRequest,
    user_id: int = Depends(get_current_user_id),
):
    meal_repo = get_meal_repo()
    meal = log_meal(
        user_id=user_id,
        meal_type=request.meal_type,
        meal_date=request.meal_date,
        notes=request.notes,
        items=[item.model_dump() for item in request.items],
        meal_repo=meal_repo,
    )

    # Skeleton response: return minimal info; expand as schemas solidify.
    return {"meal_id": getattr(meal, "id", None)}

