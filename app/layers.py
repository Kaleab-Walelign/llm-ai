"""Cell 4 — Layer legends and classification."""
STANDARD_CLASSES = {
    1: ('Very Low',  '#8B0000'),
    2: ('Low',       '#FF4500'),
    3: ('Moderate',  '#FFD700'),
    4: ('High',      '#7CFC00'),
    5: ('Very High', '#006400'),
}

def classify_standard(mean_val):
    if mean_val is None: return None, 'No data', ''
    score = max(1, min(5, round(mean_val)))
    label, color = STANDARD_CLASSES[score]
    return score, label, color

LAYER_CLASSIFY = {}
LAYER_DESCRIBE = {}

LAYER_DESCRIBE['rangeland']     = {1:'Very low rangeland health',2:'Low rangeland health',
    3:'Moderate rangeland health',4:'High rangeland health',5:'Very high rangeland health'}
LAYER_CLASSIFY['rangeland']     = classify_standard

LAYER_DESCRIBE['biomass']       = {1:'Very Low Biomass < 180 kg/ha',2:'Low Biomass 180–800 kg/ha',
    3:'Moderate Biomass 800–1400 kg/ha',4:'High Biomass 1400–2000 kg/ha',5:'Very High Biomass > 2000 kg/ha'}
LAYER_CLASSIFY['biomass']       = classify_standard

LAYER_DESCRIBE['ndvi']          = {1:'NDVI < 0.08 — bare/degraded',2:'NDVI 0.08–0.25 — sparse',
    3:'NDVI 0.25–0.35 — moderate',4:'NDVI 0.35–0.48 — good',5:'NDVI > 0.48 — dense'}
LAYER_CLASSIFY['ndvi']          = classify_standard

LAYER_DESCRIBE['rainfall']      = {1:'< 226 mm',2:'226–295 mm',3:'295–363 mm',
    4:'363–510 mm',5:'> 510 mm'}
LAYER_CLASSIFY['rainfall']      = classify_standard

LAYER_DESCRIBE['climate']       = {1:'Very unfavourable',2:'Unfavourable',3:'Moderate',
    4:'Favourable',5:'Very favourable'}
LAYER_CLASSIFY['climate']       = classify_standard

LAYER_DESCRIBE['vegetation']    = {1:'Very low cover',2:'Low cover',3:'Moderate cover',
    4:'High cover',5:'Very high cover'}
LAYER_CLASSIFY['vegetation']    = classify_standard

LAYER_DESCRIBE['soil']          = {1:'Very low quality',2:'Low quality',3:'Moderate quality',
    4:'High quality',5:'Very high quality'}
LAYER_CLASSIFY['soil']          = classify_standard

LAYER_DESCRIBE['soil_bulk']     = {1:'> 1.7 g/cm³ — high compaction',2:'1.5–1.7 g/cm³',
    3:'1.3–1.5 g/cm³',4:'1.1–1.3 g/cm³',5:'< 1.1 g/cm³ — optimal'}
LAYER_CLASSIFY['soil_bulk']     = classify_standard

LAYER_DESCRIBE['soil_moisture'] = {1:'< 20%',2:'20–40%',3:'40–60%',4:'60–80%',5:'> 80%'}
LAYER_CLASSIFY['soil_moisture'] = classify_standard

LAYER_DESCRIBE['soil_ph']       = {1:'pH < 5 or > 9',2:'pH 5.0–5.5 / 8.5–9.0',
    3:'pH 5.5–6.0 / 8.0–8.5',4:'pH 6.0–6.5 / 7.5–8.0',5:'pH 6.5–7.5 — optimal'}
LAYER_CLASSIFY['soil_ph']       = classify_standard

LAYER_DESCRIBE['soil_carbon']   = {1:'SOM < 0.2% — degraded',2:'SOM 0.2–0.6%',
    3:'SOM 0.6–1.2%',4:'SOM 1.2–2.0%',5:'SOM > 2.0% — excellent'}
LAYER_CLASSIFY['soil_carbon']   = classify_standard

LAYER_DESCRIBE['temperature']   = {1:'> 40°C — severe heat stress',2:'35–40°C — hot',
    3:'30–35°C — warm',4:'25–30°C — comfortable',5:'< 25°C — optimal'}
LAYER_CLASSIFY['temperature']   = classify_standard

LAYER_DESCRIBE['water']         = {1:'> 8 km from water',2:'5–8 km',3:'3–5 km',
    4:'1–3 km',5:'< 1 km — excellent access'}
LAYER_CLASSIFY['water']         = classify_standard

LAYER_DESCRIBE['livestock']     = {1:'> 35 TLU/km² — overgrazing',2:'20–35 TLU/km²',
    3:'10–20 TLU/km²',4:'5–10 TLU/km²',5:'< 5 TLU/km² — optimal'}
LAYER_CLASSIFY['livestock']     = classify_standard

LAYER_DESCRIBE['lulc']          = {1:'Bare / severely degraded',2:'Shrubland',
    3:'Grassland',4:'Woodland / Bushland',5:'Dense forest / good cover'}
LAYER_CLASSIFY['lulc']          = classify_standard

def classify_encroachment(mean_val):
    if mean_val is None: return None, 'No data', ''
    v = float(mean_val)
    if v < 0.10: return 0, 'None',     '#008001'
    if v < 0.25: return 1, 'Low',      '#ADFF2F'
    if v < 0.45: return 2, 'Moderate', '#FFFF00'
    if v < 0.65: return 3, 'High',     '#FFA500'
    if v < 0.85: return 4, 'Severe',   '#FF0000'
    return 5, 'Maximum', '#800100'

LAYER_DESCRIBE['encroachment']  = {0:'No encroachment',1:'Low (~0.2)',2:'Moderate (~0.4)',
    3:'High (~0.6)',4:'Severe (~0.8)',5:'Maximum (1.0)'}
LAYER_CLASSIFY['encroachment']  = classify_encroachment

LAYER_DESCRIBE['slope']         = {1:'> 15% — very steep',2:'10–15% — steep',
    3:'5–10% — moderate',4:'2–5% — gentle',5:'0–2% — flat, best for rangeland'}
LAYER_CLASSIFY['slope']         = classify_standard

print(f'✅ {len(LAYER_CLASSIFY)} layer classifiers ready (shared across all regions)')

