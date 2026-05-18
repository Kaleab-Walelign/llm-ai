"""Cell 9 — Gemini tool functions."""
from app.context import build_ai_context
from app.detection import detect_layers
from app.regions import REGION_REGISTRY, detect_region
from app.spatial import run_spatial_analysis

def get_woreda_report(woreda_name: str,
                      layers: str = 'summary',
                      region: str = 'auto') -> dict:
    """
    Get rangeland monitoring data for a specific woreda in any supported region.

    Args:
        woreda_name: Name of the woreda e.g. 'Dubti', 'Afambo', 'Jijiga', 'Gode'
        layers:      Comma-separated layer keys, or keywords:
                     'summary' (6 key layers), 'all', 'soil', 'vegetation',
                     'rangeland', 'climate', 'water', 'livestock', etc.
        region:      Region key ('afar','diredawa','somali','oromia','south',
                     'southwest','gambella','benshangul') or 'auto' to detect.
    """
    rk = region if region in REGION_REGISTRY else detect_region(woreda_name + ' ' + layers)
    reg = REGION_REGISTRY[rk]
    lkeys = detect_layers(layers, rk)
    explicit = [l.strip() for l in layers.split(',') if l.strip() in reg['layers']]
    if explicit: lkeys = explicit
    if not lkeys: lkeys = ['rangeland','climate','vegetation']
    result = run_spatial_analysis(woreda_name, lkeys, rk, 'woreda')
    if 'error' not in result: result['ai_context'] = build_ai_context(result)
    return result


def get_zone_report(zone_name: str,
                    layers: str = 'summary',
                    region: str = 'auto') -> dict:
    """
    Get rangeland data aggregated for an entire zone (admin level 2).

    Args:
        zone_name: Zone name e.g. 'Zone 1', 'Awsi Rasu', 'Afder', 'Borena'
        layers:    Same options as get_woreda_report
        region:    Region key or 'auto'
    """
    rk = region if region in REGION_REGISTRY else detect_region(zone_name + ' ' + layers)
    reg = REGION_REGISTRY[rk]
    lkeys = detect_layers(layers, rk)
    explicit = [l.strip() for l in layers.split(',') if l.strip() in reg['layers']]
    if explicit: lkeys = explicit
    result = run_spatial_analysis(zone_name, lkeys, rk, 'zone')
    if 'error' not in result: result['ai_context'] = build_ai_context(result)
    return result


def get_region_report(region_name: str = 'Afar',
                      layers: str = 'summary') -> dict:
    """
    Get overall rangeland data for an entire region.
    Use for: 'overall condition of Afar', 'Somali region summary', 'how is Oromia'.

    Args:
        region_name: Region name or key e.g. 'Afar', 'Dire Dawa', 'Somali', 'Oromia',
                     'South Ethiopia', 'South West Ethiopia', 'Gambella', 'Benshangul-Gumuz'
        layers:      Same options as get_woreda_report
    """
    rk = detect_region(region_name)
    reg = REGION_REGISTRY[rk]
    lkeys = detect_layers(layers, rk)
    result = run_spatial_analysis(reg['display_name'], lkeys, rk, 'region')
    if 'error' not in result: result['ai_context'] = build_ai_context(result)
    return result


def compare_woredas(woreda_names: str,
                    layer: str = 'rangeland',
                    region: str = 'auto') -> dict:
    """
    Compare multiple woredas side by side for one indicator.
    Use when user asks to compare areas e.g. 'Compare Dubti and Afambo'.

    Args:
        woreda_names: Comma-separated names e.g. 'Dubti,Afambo,Asayita'
        layer:        Indicator key e.g. 'rangeland', 'ndvi', 'rainfall', 'biomass'
        region:       Region key or 'auto'
    """
    names = [n.strip() for n in woreda_names.split(',') if n.strip()]
    rk    = region if region in REGION_REGISTRY else detect_region(woreda_names + ' ' + layer)
    reg   = REGION_REGISTRY[rk]
    lk    = layer.strip() if layer.strip() in reg['layers'] else 'rangeland'
    comp  = {'layer': lk, 'region': rk, 'woredas': {}}
    for name in names:
        r = run_spatial_analysis(name, [lk], rk, 'woreda')
        comp['woredas'][name] = r['layers'].get(lk, r.get('error','No data'))
    lines = [f'COMPARISON — {lk.upper()} | {reg["display_name"]}', '']
    for name, d in sorted(comp['woredas'].items(),
                           key=lambda x: x[1].get('mean',0) if isinstance(x[1],dict) else 0):
        if isinstance(d,dict) and 'mean' in d:
            lines.append(f'  {name}: {d["mean"]} → {d["label"]} — {d["description"]}')
        else:
            lines.append(f'  {name}: {d}')
    comp['ai_context'] = '\n'.join(lines)
    return comp
