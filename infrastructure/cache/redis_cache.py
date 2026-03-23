from __future__ import annotations

import json
from typing import Any

import redis


class RedisCacheService:
    def __init__(self, *, redis_url: str):
        self._client = redis.from_url(redis_url, decode_responses=True)

    def get(self, key: str) -> Any | None:
        raw = self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        raw = json.dumps(value)
        self._client.set(key, raw, ex=ttl_seconds)

