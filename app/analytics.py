"""Analytics pipeline: Redis → PostgreSQL → spatial engine → cache."""

from __future__ import annotations

import logging
from typing import Any

from app import cache, database
from app.intent import QueryIntent
from app.spatial import run_indicator_analysis
from app.timeseries import format_time_label

logger = logging.getLogger(__name__)


def _row_to_result(row: dict) -> dict[str, Any]:
    return {
        "woreda": row["woreda"],
        "indicator": row["indicator"],
        "time_key": row["time_key"],
        "time_label": format_time_label(row["time_key"], row["indicator"]),
        "mean": row["mean"],
        "min": row["min_val"],
        "max": row["max_val"],
        "pixel_count": row["pixel_count"],
        "score": row["score"],
        "label": row["label"],
        "description": row["description"],
        "source": row.get("source", "cache"),
    }


def get_indicator_stats(
    woreda: str,
    indicator: str,
    time_hint: dict | None = None,
) -> dict[str, Any]:
    """Resolve one indicator: Redis → Postgres → compute → store."""
    # Need time_key for cache/db lookup; compute path resolves raster first.
    from app.timeseries import resolve_time_key

    time_key = resolve_time_key(indicator, time_hint)

    cached = cache.get_stats(woreda, indicator, time_key)
    if cached:
        cached["source"] = "redis"
        return cached

    stored = database.get_stats(woreda, indicator, time_key)
    if stored:
        result = _row_to_result({**stored, "source": "postgres"})
        cache.set_stats(woreda, indicator, time_key, result)
        return result

    computed = run_indicator_analysis(woreda, indicator, time_hint)
    if "error" in computed:
        return computed

    db_row = {
        "woreda": woreda,
        "indicator": indicator,
        "time_key": computed["time_key"],
        "mean": computed["mean"],
        "min_val": computed["min"],
        "max_val": computed["max"],
        "pixel_count": computed["pixel_count"],
        "score": computed["score"],
        "label": computed["label"],
        "description": computed["description"],
    }
    database.save_stats(db_row)
    computed["source"] = "computed"
    cache.set_stats(woreda, indicator, computed["time_key"], computed)
    return computed


def run_query(intent: QueryIntent) -> dict[str, Any]:
    layers: dict[str, Any] = {}
    errors: list[str] = []

    for indicator in intent.indicators:
        result = get_indicator_stats(intent.woreda, indicator, intent.time_hint)
        if "error" in result:
            errors.append(f"{indicator}: {result['error']}")
            layers[indicator] = result
        else:
            layers[indicator] = result

    out: dict[str, Any] = {
        "woreda": intent.woreda,
        "indicators": intent.indicators,
        "layers": layers,
    }
    if errors:
        out["warnings"] = errors
    return out


def build_compact_json(intent: QueryIntent, result: dict[str, Any]) -> dict[str, Any]:
    """Minimal payload for Gemini — numbers and labels only."""
    compact_layers = {}
    for key, layer in result.get("layers", {}).items():
        if "error" in layer:
            compact_layers[key] = {"error": layer["error"]}
        else:
            compact_layers[key] = {
                "time": layer.get("time_label", layer.get("time_key")),
                "mean": layer.get("mean"),
                "score": layer.get("score"),
                "label": layer.get("label"),
                "description": layer.get("description"),
            }
    return {
        "woreda": intent.woreda,
        "question": intent.raw_question,
        "indicators": compact_layers,
    }
