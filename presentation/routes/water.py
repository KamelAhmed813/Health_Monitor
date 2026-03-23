from __future__ import annotations

from fastapi import APIRouter, Depends

from app.use_cases.log_water import log_water
from presentation.dependencies import get_current_user_id, get_water_repo
from presentation.schemas.water import LogWaterRequest


router = APIRouter()


@router.post("", summary="Log water intake")
def create_water_log(
    request: LogWaterRequest,
    user_id: int = Depends(get_current_user_id),
):
    water_repo = get_water_repo()
    water_log = log_water(
        user_id=user_id,
        log_date=request.log_date,
        amount_ml=request.amount_ml,
        water_repo=water_repo,
    )
    return {"water_log_id": getattr(water_log, "id", None)}

