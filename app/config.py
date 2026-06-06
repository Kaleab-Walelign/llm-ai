"""Cells 1–2: configuration and paths."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(os.getenv("NRMS_DATA_DIR", "/home/kaleabwalelign/Documents/rangeland_data"))
GEOSERVER_BASE = os.getenv("GEOSERVER_URL", "https://nrms.ati.gov.et/geoserver").rstrip("/")
WFS_URL = f"{GEOSERVER_BASE}/geonode/ows"
WCS_URL = f"{GEOSERVER_BASE}/geonode/wcs"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nrms:nrms@localhost:5432/nrms",
)
WOREDA_NAME_FIELD = os.getenv("WOREDA_NAME_FIELD", "")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]


def resolve_tif_path(filename: str | None) -> str | None:
    if not filename:
        return None
    p = Path(filename)
    if p.is_absolute() and p.exists():
        return str(p)
    candidate = DATA_DIR / filename
    if candidate.exists():
        return str(candidate)
    if p.exists():
        return str(p)
    return str(candidate)
