from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

import redis


class RedisCacheService:
    def __init__(
        self,
        *,
        redis_url: str,
        socket_connect_timeout: float | None = 2.0,
        socket_timeout: float | None = 2.0,
        health_check_interval: int = 30,
        max_connections: int = 20,
    ):
        self._client = redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=socket_connect_timeout,
            socket_timeout=socket_timeout,
            health_check_interval=health_check_interval,
            max_connections=max_connections,
        )

    def get(self, key: str) -> Any | None:
        raw = self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        raw = json.dumps(value, default=self._json_default)
        self._client.set(key, raw, ex=ttl_seconds)

    def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        return int(self._client.delete(*keys))

    @staticmethod
    def _json_default(value: Any) -> str:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return str(value)