"""Maps indicator keys to rangeland_data directory layout."""

from __future__ import annotations

from pathlib import Path

from app.config import DATA_DIR

# Directory names match the host layout under NRMS_DATA_DIR (e.g. ~/Documents/rangeland_data).
INDICATOR_DIRS: dict[str, str] = {
    "biomass": "biomass_weighted_timeseries",
    "lulc": "lulc_timeseries",
    "rangeland": "rangelandhealth_weighted_timeseries",
    "soil_moisture": "soilmosture_timeseries",
    "soil": "soil_weigted_timeseries",
    "vci": "vci_timeseries",
    "climate": "climate_weighted_timeseries",
    "ndvi": "ndvi_timeseries",
    "slope": "slope_weighted_timeseries",
    "soil_carbon": "soilorganiccarbon_weighted_timeseries",
    "spei": "spei_timeseries",
    "vegetation": "vegetation_weighted_timeseries",
    "livestock": "livestock_weighted_timeseries",
    "rainfall": "rainfall_timeseries",
    "soil_bulk": "soilbd_weighted_timeseries",
    "soil_ph": "soilph_weighted_timeseries",
    "temperature": "temprature_timeseries",
    "water": "water_weighted_timeseries",
}

# Yearly snapshots (e.g. 2025.tif) vs decadal composites (e.g. 20250101.tif).
YEARLY_INDICATORS = frozenset({
    "rangeland", "biomass", "climate", "vegetation", "soil",
    "soil_bulk", "soil_ph", "soil_carbon", "water", "livestock", "slope",
})

WOREDA_SHP_DIR = "woreda_shp_file"
WOREDA_SHP_NAME = "woreda.shp"


def indicator_dir(indicator: str) -> Path:
    dirname = INDICATOR_DIRS.get(indicator)
    if not dirname:
        raise ValueError(f"Unknown indicator: {indicator}")
    return DATA_DIR / dirname


def woreda_shp_path() -> Path:
    return DATA_DIR / WOREDA_SHP_DIR / WOREDA_SHP_NAME


def list_available_indicators() -> list[str]:
    return sorted(INDICATOR_DIRS.keys())
