from __future__ import annotations

from pydantic import BaseModel, Field


class LogWaterRequest(BaseModel):
    log_date: str = Field(description="YYYY-MM-DD")
    amount_ml: int = Field(gt=0)

