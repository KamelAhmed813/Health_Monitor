from __future__ import annotations

from domain.entities.models import WaterLog
from domain.ports.interfaces import WaterRepository


def log_water(
    *,
    user_id: int,
    log_date: str,  # ISO date string
    amount_ml: int,
    water_repo: WaterRepository,
) -> WaterLog:
    raise NotImplementedError("log_water use case not implemented yet")

