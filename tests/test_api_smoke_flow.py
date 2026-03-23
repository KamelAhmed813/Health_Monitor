from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


class InMemoryCache:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}
        self.get_hits: dict[str, int] = {}
        self.get_misses: dict[str, int] = {}
        self.set_calls: dict[str, int] = {}

    def get(self, key: str) -> Any | None:
        if key in self._store:
            self.get_hits[key] = self.get_hits.get(key, 0) + 1
            return self._store[key]
        self.get_misses[key] = self.get_misses.get(key, 0) + 1
        return None

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self._store[key] = value
        self.set_calls[key] = self.set_calls.get(key, 0) + 1

    def delete(self, *keys: str) -> int:
        deleted = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                deleted += 1
        return deleted


def test_api_smoke_register_login_workout_meal_water_dashboard_cache_miss_then_hit() -> None:
    db_path = Path("tests/.tmp-smoke.sqlite").resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    os.environ["HEALTH_SQLITE_PATH"] = str(db_path)

    from infrastructure.db.models import Base
    from infrastructure.db.session import engine
    from main import app
    from app.use_cases import auth_login as auth_login_uc
    from presentation import dependencies
    from presentation.routes import auth as auth_route

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    cache = InMemoryCache()
    dependencies.get_cache = lambda: cache  # type: ignore[assignment]
    dependencies._cache_singleton = cache  # type: ignore[attr-defined]
    auth_route.hash_password = lambda pwd: f"hashed::{pwd}"  # type: ignore[assignment]
    auth_login_uc.verify_password = lambda plain, hashed: hashed == f"hashed::{plain}"  # type: ignore[assignment]

    client = TestClient(app)

    register_response = client.post(
        "/api/auth/register",
        json={"email": "smoke@example.com", "password": "testpass123"},
    )
    assert register_response.status_code == 200
    access_token = register_response.json()["access_token"]

    login_response = client.post(
        "/api/auth/login",
        json={"email": "smoke@example.com", "password": "testpass123"},
    )
    assert login_response.status_code == 200
    login_token = login_response.json()["access_token"]
    assert isinstance(login_token, str)
    assert login_token

    invalid_login_response = client.post(
        "/api/auth/login",
        json={"email": "smoke@example.com", "password": "wrongpass"},
    )
    assert invalid_login_response.status_code == 401
    assert invalid_login_response.json()["detail"] == "Invalid email or password"

    duplicate_register_response = client.post(
        "/api/auth/register",
        json={"email": "smoke@example.com", "password": "testpass123"},
    )
    assert duplicate_register_response.status_code == 409
    assert duplicate_register_response.json()["detail"] == "Email already registered"

    headers = {"Authorization": f"Bearer {access_token}"}

    workout_response = client.post(
        "/api/workouts",
        headers=headers,
        json={"workout_type": "running", "duration_minutes": 30, "calories_burned": 220},
    )
    assert workout_response.status_code == 200
    assert workout_response.json()["workout_type"] == "running"

    meal_response = client.post(
        "/api/meals",
        headers=headers,
        json={
            "meal_type": "lunch",
            "meal_date": "2026-03-23",
            "notes": "smoke meal",
            "items": [{"name": "rice", "quantity": "1 bowl", "calories": 240}],
        },
    )
    assert meal_response.status_code == 200
    assert meal_response.json()["meal_id"] is not None

    water_response = client.post(
        "/api/water",
        headers=headers,
        json={"log_date": "2026-03-23", "amount_ml": 500},
    )
    assert water_response.status_code == 200
    assert water_response.json()["water_log_id"] is not None

    day = "2026-03-23"
    dashboard_key = f"cache:dashboard:1:{day}"

    dashboard_first = client.get(f"/api/dashboard/today?day={day}", headers=headers)
    assert dashboard_first.status_code == 200
    data_first = dashboard_first.json()["data"]
    assert data_first["workouts_count"] >= 1
    assert data_first["meals_count"] >= 1
    assert data_first["water_today_ml"] >= 500
    assert cache.get_misses.get(dashboard_key, 0) >= 1
    assert cache.set_calls.get(dashboard_key, 0) >= 1

    dashboard_second = client.get(f"/api/dashboard/today?day={day}", headers=headers)
    assert dashboard_second.status_code == 200
    data_second = dashboard_second.json()["data"]
    assert data_second == data_first
    assert cache.get_hits.get(dashboard_key, 0) >= 1

