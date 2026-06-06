"""Local woreda boundaries from shapefile."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from functools import lru_cache

import geopandas as gpd

from app.config import WOREDA_NAME_FIELD
from app.data_catalog import woreda_shp_path

logger = logging.getLogger(__name__)

_NAME_CANDIDATES = ("woreda", "WOREDA", "Woreda", "adm3_en", "ADM3_EN", "name", "NAME")


@lru_cache(maxsize=1)
def _load_gdf() -> gpd.GeoDataFrame:
    shp = woreda_shp_path()
    if not shp.is_file():
        raise FileNotFoundError(f"Woreda shapefile not found: {shp}")
    gdf = gpd.read_file(shp)
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    return gdf


def _name_field(gdf: gpd.GeoDataFrame) -> str:
    if WOREDA_NAME_FIELD and WOREDA_NAME_FIELD in gdf.columns:
        return WOREDA_NAME_FIELD
    for col in _NAME_CANDIDATES:
        if col in gdf.columns:
            return col
    raise RuntimeError(
        f"Cannot detect woreda name column. Columns: {list(gdf.columns)}. "
        f"Set WOREDA_NAME_FIELD in .env."
    )


@lru_cache(maxsize=1)
def list_woreda_names() -> tuple[str, ...]:
    gdf = _load_gdf()
    field = _name_field(gdf)
    names = sorted({str(v).strip() for v in gdf[field].dropna() if str(v).strip()})
    return tuple(names)


def fetch_woreda_geojson(woreda_name: str) -> dict:
    gdf = _load_gdf()
    field = _name_field(gdf)
    query = woreda_name.strip()
    mask = gdf[field].astype(str).str.contains(query, case=False, na=False, regex=False)
    matched = gdf[mask]
    if matched.empty:
        return {"type": "FeatureCollection", "features": []}
    return json.loads(matched.to_json())


def geojson_to_tempfile(geojson: dict) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".geojson", delete=False, mode="w")
    json.dump(geojson, tmp)
    tmp.close()
    return tmp.name


def get_bbox(geojson: dict) -> tuple[float, float, float, float] | None:
    features = geojson.get("features", [])
    if not features:
        return None
    pts: list[list[float]] = []

    def flatten(c):
        if isinstance(c[0], (int, float)):
            pts.append(c)
        else:
            for x in c:
                flatten(x)

    for f in features:
        flatten(f["geometry"]["coordinates"])
    if not pts:
        return None
    return (
        min(p[0] for p in pts), min(p[1] for p in pts),
        max(p[0] for p in pts), max(p[1] for p in pts),
    )
