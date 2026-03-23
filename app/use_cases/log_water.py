from __future__ import annotations

from datetime import date

from domain.entities.models import WaterLog
from domain.ports.interfaces import WaterRepository


def log_water(
    *,
    user_id: int,
    log_date: str,  # ISO date string
    amount_ml: int,
    water_repo: WaterRepository,
) -> WaterLog:
    parsed_date = date.fromisoformat(log_date)
    return water_repo.log_water(user_id=user_id, log_date=parsed_date, amount_ml=amount_ml)

