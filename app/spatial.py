"""Core spatial analytics over local shapefile + timeseries GeoTIFFs."""

from __future__ import annotations

import logging
import os

from rasterstats import zonal_stats

from app.boundaries import fetch_woreda_geojson, geojson_to_tempfile
from app.layers import LAYER_CLASSIFY, LAYER_DESCRIBE
from app.timeseries import format_time_label, resolve_raster_path

logger = logging.getLogger(__name__)


def run_indicator_analysis(
    woreda_name: str,
    indicator: str,
    time_hint: dict | None = None,
) -> dict:
    """Zonal stats for one woreda + indicator + time period."""
    geojson = fetch_woreda_geojson(woreda_name)
    features = geojson.get("features", [])
    if not features:
        return {
            "error": f'No woreda boundary found for "{woreda_name}". Check spelling.',
        }

    try:
        raster_path, time_key = resolve_raster_path(indicator, time_hint)
    except FileNotFoundError as exc:
        return {"error": str(exc)}

    geojson_path = geojson_to_tempfile(geojson)
    try:
        stats = zonal_stats(
            geojson_path,
            raster_path,
            stats=["min", "max", "mean", "count"],
            all_touched=True,
        )
        valid = [s for s in stats if s.get("mean") is not None]
        if not valid:
            return {"error": "No valid pixels found in raster for this woreda."}

        total_pixels = sum(s["count"] for s in valid)
        agg_mean = sum(s["mean"] * s["count"] for s in valid) / total_pixels
        agg_min = min(s["min"] for s in valid if s["min"] is not None)
        agg_max = max(s["max"] for s in valid if s["max"] is not None)

        classify = LAYER_CLASSIFY.get(indicator)
        if not classify:
            return {"error": f"No classifier for indicator '{indicator}'."}

        score, label, color = classify(agg_mean)
        desc = LAYER_DESCRIBE.get(indicator, {}).get(score, "")

        logger.info("[%s] %s time=%s mean=%.3f → %s", woreda_name, indicator, time_key, agg_mean, label)

        return {
            "woreda": woreda_name,
            "indicator": indicator,
            "time_key": time_key,
            "time_label": format_time_label(time_key, indicator),
            "mean": round(agg_mean, 3),
            "min": agg_min,
            "max": agg_max,
            "pixel_count": total_pixels,
            "score": score,
            "label": label,
            "color": color,
            "description": desc,
            "feature_count": len(features),
        }
    except Exception as exc:
        logger.exception("Spatial analysis failed")
        return {"error": str(exc)}
    finally:
        try:
            os.unlink(geojson_path)
        except OSError:
            pass


def run_spatial_analysis(
    area_name: str,
    layer_keys: list[str],
    region_key: str | None = None,
    admin_level: str = "woreda",
    time_hint: dict | None = None,
    **_kwargs,
) -> dict:
    """Backward-compatible multi-layer report (woreda-level, local data)."""
    if admin_level != "woreda":
        return {
            "error": (
                f"Admin level '{admin_level}' is not supported with local shapefile data. "
                "Use woreda-level queries."
            ),
        }

    result = {
        "area": area_name,
        "admin_level": admin_level,
        "layers": {},
    }
    for layer_key in layer_keys:
        layer_result = run_indicator_analysis(area_name, layer_key, time_hint)
        if "error" in layer_result:
            result["layers"][layer_key] = {"error": layer_result["error"]}
        else:
            result["layers"][layer_key] = {
                k: layer_result[k]
                for k in (
                    "mean", "min", "max", "pixel_count", "score",
                    "label", "color", "description", "time_key", "time_label",
                )
                if k in layer_result
            }
    return result
