"""Redis cache for computed zonal statistics."""

from __future__ import annotations

import json
import logging
from typing import Any

import redis

from app.config import REDIS_URL

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None
TTL_SECONDS = 3600 * 6  # 6 hours


def _client_instance() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)
    return _client


def cache_key(woreda: str, indicator: str, time_key: str) -> str:
    return f"stats:{woreda.lower()}:{indicator}:{time_key}"


def get_stats(woreda: str, indicator: str, time_key: str) -> dict | None:
    try:
        raw = _client_instance().get(cache_key(woreda, indicator, time_key))
        return json.loads(raw) if raw else None
    except Exception as exc:
        logger.warning("Redis get failed: %s", exc)
        return None


def set_stats(woreda: str, indicator: str, time_key: str, data: dict[str, Any]) -> None:
    try:
        _client_instance().setex(
            cache_key(woreda, indicator, time_key),
            TTL_SECONDS,
            json.dumps(data),
        )
    except Exception as exc:
        logger.warning("Redis set failed: %s", exc)


def ping() -> bool:
    try:
        return bool(_client_instance().ping())
    except Exception:
        return False
