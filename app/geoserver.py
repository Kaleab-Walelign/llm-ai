"""Cell 5 — GeoServer WFS/WCS helpers."""
import os
import tempfile
import logging
import requests
from app.config import WCS_URL, WFS_URL

logger = logging.getLogger(__name__)







def fetch_wfs(area_name, wfs_layer, filter_field):
    # Force GeoJSON coordinates in WGS84. GeoServer often defaults to the datastore's
    # native CRS (e.g. UTM). Without this, bbox is in metres while fetch_wcs uses
    # EPSG:4326 — WCS returns invalid data and zonal_stats can try to allocate PiB-scale windows.
    params = {
        'service':      'WFS',
        'version':      '1.1.0',
        'request':      'GetFeature',
        'typeName':     wfs_layer,
        'CQL_FILTER':   f"{filter_field} ILIKE '%{area_name}%'",
        'outputFormat': 'application/json',
        'maxFeatures':  500,
        'srsName':      'EPSG:4326',
    }
    resp = requests.get(WFS_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def get_bbox(geojson):
    pts = []
    def flatten(c):
        if isinstance(c[0], (int, float)): pts.append(c)
        else: [flatten(x) for x in c]
    for f in geojson.get('features', []):
        flatten(f['geometry']['coordinates'])
    if not pts: return None
    return (min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts))

def fetch_wcs_to_tempfile(layer_name, bbox):
    params = {
        'service':  'WCS',
        'version':  '1.0.0',
        'request':  'GetCoverage',
        'coverage': layer_name,
        'format':   'GeoTIFF',
        'crs':      'EPSG:4326',
        'bbox':     f'{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}',
        'width':    512,
        'height':   512,
    }
    resp = requests.get(WCS_URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.content
    # GeoServer often returns XML ServiceExceptionReport when bbox/CRS is wrong — not a TIFF.
    if len(data) < 8 or (not data.startswith(b'II') and not data.startswith(b'MM')):
        head = data[:500].decode('utf-8', errors='replace')
        raise RuntimeError(
            f'WCS did not return a GeoTIFF (check bbox is lon/lat in EPSG:4326). '
            f'Content-Type={resp.headers.get("Content-Type")!r} body start: {head!r}'
        )
    tmp = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
    tmp.write(data)
    tmp.close()
    return tmp.name

def get_raster_path(layer_key, geoserver_layer, local_tifs, bbox):
    local = local_tifs.get(layer_key)
    if local and os.path.exists(local):
        logger.info("[%s] local: %s", layer_key, local)
        return local, False
    logger.info("[%s] WCS: %s", layer_key, geoserver_layer)
    path = fetch_wcs_to_tempfile(geoserver_layer, bbox)
    return path, True


