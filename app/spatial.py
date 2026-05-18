"""Cell 6 — Core spatial analysis."""
import json
import logging
import os
import tempfile

from rasterstats import zonal_stats

from app.geoserver import fetch_wfs, get_bbox, get_raster_path
from app.layers import LAYER_CLASSIFY, LAYER_DESCRIBE
from app.regions import REGION_REGISTRY

logger = logging.getLogger(__name__)

def run_spatial_analysis(area_name, layer_keys, region_key, admin_level='woreda',
                         visualize=False):
    """
    Identical logic to the working Afar notebook — now region-aware.
    region_key  : key into REGION_REGISTRY ('afar','diredawa','somali', ...)
    admin_level : 'woreda' | 'zone' | 'region'
    """
    reg = REGION_REGISTRY[region_key]

    # ── Planned region guard ──────────────────────────────────────────────────
    if reg['status'] != 'active':
        active_list = ', '.join(
            v['display_name'] for v in REGION_REGISTRY.values() if v['status']=='active'
        )
        return {
            'error': (
                f"{reg['display_name']} data is not yet available on NRMS GeoServer. "
                f"It is planned for future monitoring. "
                f"Currently active regions: {active_list}."
            )
        }

    wfs_layer    = reg['wfs']
    filter_field = reg['adm_fields'][admin_level]
    layers_map   = reg['layers']
    local_tifs   = reg.get('local_tifs', {})

    logger.info('=== [{reg["display_name"]}] {area_name} ({admin_level}) ===')

    geojson  = fetch_wfs(area_name, wfs_layer, filter_field)
    features = geojson.get('features', [])
    if not features:
        return {'error': f'No features found for "{area_name}" in {reg["display_name"]}. '
                         f'Check spelling or try a different admin level.'}
    logger.info('  → {len(features)} feature(s) found')

    bbox = get_bbox(geojson)
    logger.info('  → BBox: {tuple(round(b,4) for b in bbox)}')

    if visualize:
        logger.debug('visualize=True ignored in API mode')

    tmp_gj = tempfile.NamedTemporaryFile(suffix='.geojson', delete=False, mode='w')
    json.dump(geojson, tmp_gj); tmp_gj.close()
    geojson_path = tmp_gj.name

    result = {
        'area': area_name, 'region': region_key,
        'region_display': reg['display_name'],
        'admin_level': admin_level,
        'feature_count': len(features), 'bbox': bbox, 'layers': {},
    }
    temp_rasters = []

    for layer_key in layer_keys:
        geoserver_layer = layers_map.get(layer_key)
        if not geoserver_layer:
            result['layers'][layer_key] = {
                'error': f'Layer "{layer_key}" not configured for {reg["display_name"]}'
            }
            continue
        try:
            raster_path, is_temp = get_raster_path(layer_key, geoserver_layer, local_tifs, bbox)
            if is_temp: temp_rasters.append(raster_path)

            stats = zonal_stats(geojson_path, raster_path,
                                stats=['min','max','mean','count'], all_touched=True)
            valid = [s for s in stats if s.get('mean') is not None]
            if not valid:
                result['layers'][layer_key] = {'error': 'No valid pixels found'}; continue

            total_pixels = sum(s['count'] for s in valid)
            agg_mean = sum(s['mean']*s['count'] for s in valid) / total_pixels
            agg_min  = min(s['min'] for s in valid if s['min'] is not None)
            agg_max  = max(s['max'] for s in valid if s['max'] is not None)

            score, label, color = LAYER_CLASSIFY[layer_key](agg_mean)
            desc = LAYER_DESCRIBE.get(layer_key, {}).get(score, '')

            result['layers'][layer_key] = {
                'mean': round(agg_mean,3), 'min': agg_min, 'max': agg_max,
                'pixel_count': total_pixels,
                'score': score, 'label': label, 'color': color, 'description': desc,
            }
            logger.info('  [%s] {agg_mean:.3f} → {label}')

        except Exception as e:
            result['layers'][layer_key] = {'error': str(e)}
            logger.info('  [%s] ERROR: {e}')

    os.unlink(geojson_path)
    for p in temp_rasters:
        try: os.unlink(p)
        except: pass

    logger.info('Done — {len(result["layers"])} layers processed')
    return result

print('✅ run_spatial_analysis() ready')
