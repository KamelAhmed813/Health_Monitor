from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    # Keep dashboard flexible for now; production should define a strong typed schema.
    data: Any

