"""Resolve GeoTIFF paths from indicator + time intent."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path

from app.data_catalog import YEARLY_INDICATORS, indicator_dir

logger = logging.getLogger(__name__)

_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}


def list_tif_files(indicator: str) -> list[str]:
    d = indicator_dir(indicator)
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob("*.tif"))


def latest_time_key(indicator: str) -> str | None:
    files = list_tif_files(indicator)
    return files[-1] if files else None


def _decadal_keys_for_month(year: int, month: int) -> list[str]:
    return [f"{year}{month:02d}{day:02d}" for day in (1, 11, 21)]


def parse_time_from_text(text: str) -> dict | None:
    """Extract year/month/day hints from natural language."""
    t = text.lower()
    if any(w in t for w in ("latest", "current", "recent", "now", "today")):
        return {"mode": "latest"}

    m = re.search(r"\b(20\d{2})(\d{2})(\d{2})\b", t)
    if m:
        return {"mode": "exact", "key": m.group(0)}

    m = re.search(r"\b(20\d{2})\b", t)
    year = int(m.group(1)) if m else None

    month = None
    for name, num in _MONTHS.items():
        if re.search(rf"\b{re.escape(name)}\b", t):
            month = num
            break

    if year and month:
        return {"mode": "month", "year": year, "month": month}
    if year:
        return {"mode": "year", "year": year}
    return None


def resolve_time_key(indicator: str, time_hint: dict | None = None) -> str:
    files = list_tif_files(indicator)
    if not files:
        raise FileNotFoundError(f"No GeoTIFF files for indicator '{indicator}'")

    yearly = indicator in YEARLY_INDICATORS
    hint = time_hint or {"mode": "latest"}

    if hint.get("mode") == "latest":
        return files[-1]

    if hint.get("mode") == "exact":
        key = hint["key"]
        if key in files:
            return key
        if yearly and len(key) >= 4:
            year_key = key[:4]
            if year_key in files:
                return year_key
        raise FileNotFoundError(f"No file matching '{key}' for {indicator}")

    if hint.get("mode") == "year":
        year = str(hint["year"])
        if yearly:
            if year in files:
                return year
            matches = [f for f in files if f.startswith(year)]
            if matches:
                return matches[-1]
        else:
            matches = [f for f in files if f.startswith(year)]
            if matches:
                return matches[-1]
        raise FileNotFoundError(f"No data for year {year} ({indicator})")

    if hint.get("mode") == "month":
        year, month = hint["year"], hint["month"]
        if yearly:
            year_key = str(year)
            if year_key in files:
                return year_key
            raise FileNotFoundError(f"No yearly file for {year} ({indicator})")
        candidates = _decadal_keys_for_month(year, month)
        for key in reversed(candidates):
            if key in files:
                return key
        prefix = f"{year}{month:02d}"
        matches = [f for f in files if f.startswith(prefix)]
        if matches:
            return matches[-1]
        raise FileNotFoundError(f"No data for {year}-{month:02d} ({indicator})")

    return files[-1]


def resolve_raster_path(indicator: str, time_hint: dict | None = None) -> tuple[str, str]:
    """Return (absolute_path, time_key)."""
    time_key = resolve_time_key(indicator, time_hint)
    path = indicator_dir(indicator) / f"{time_key}.tif"
    if not path.is_file():
        raise FileNotFoundError(f"Raster not found: {path}")
    logger.info("[%s] time=%s path=%s", indicator, time_key, path)
    return str(path), time_key


def format_time_label(time_key: str, indicator: str) -> str:
    if indicator in YEARLY_INDICATORS and len(time_key) == 4:
        return time_key
    if len(time_key) == 8:
        try:
            return datetime.strptime(time_key, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return time_key
