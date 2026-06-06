"""Cell 8 — Topic, region, and layer detection."""
from app.layers import LAYER_CLASSIFY
from app.regions import REGION_REGISTRY

ALL_LAYER_KEYS = list(LAYER_CLASSIFY.keys())

TOPIC_TO_LAYERS = {
    'rangeland':    ['rangeland','vegetation','soil','water','climate','livestock'],
    'health':       ['rangeland','vegetation','soil','water','climate','livestock'],
    'condition':    ['rangeland','vegetation','soil','water','climate','livestock'],
    'ndvi':         ['ndvi'],
    'vegetation':   ['ndvi','biomass','vegetation'],
    'biomass':      ['biomass'],
    'rainfall':     ['rainfall'],
    'rain':         ['rainfall'],
    'drought':      ['rainfall','ndvi','climate'],
    'climate':      ['climate','rainfall','temperature'],
    'soil':         ['soil','soil_bulk','soil_moisture','soil_ph','soil_carbon'],
    'soil health':  ['soil'],
    'bulk density': ['soil_bulk'],
    'moisture':     ['soil_moisture'],
    'ph':           ['soil_ph'],
    'organic':      ['soil_carbon'],
    'carbon':       ['soil_carbon'],
    'temperature':  ['temperature'],
    'heat':         ['temperature'],
    'water':        ['water'],
    'livestock':    ['livestock'],
    'grazing':      ['livestock','rangeland'],
    'encroachment': ['encroachment'],
    'bush':         ['encroachment'],
    'prosopis':     ['encroachment'],
    'slope':        ['slope'],
    'terrain':      ['slope'],
    'lulc':         ['lulc'],
    'land use':     ['lulc'],
    'land cover':   ['lulc'],
    'vci':          ['vci'],
    'vegetation condition': ['vci'],
    'spei':         ['spei'],
    'drought index': ['spei'],
    'summary':      ['rangeland','vegetation','soil','climate','livestock','water'],
    'pastoralist':  ['rangeland','vegetation','soil','climate','livestock','water'],
}

def detect_layers(question, region_key=None):
    from app.data_catalog import list_available_indicators

    available = set(list_available_indicators())
    q = question.lower()
    found = set()
    for topic in sorted(TOPIC_TO_LAYERS, key=len, reverse=True):
        if topic in q:
            for lk in TOPIC_TO_LAYERS[topic]:
                if lk not in available:
                    continue
                if region_key:
                    if lk in REGION_REGISTRY[region_key]['layers']:
                        found.add(lk)
                else:
                    found.add(lk)
    return list(found) if found else ['rangeland', 'climate', 'vegetation']

def detect_admin_level(text):
    t = text.lower()
    if any(w in t for w in ['zone','zonal']): return 'zone'
    if any(w in t for w in ['region','regional','overall','entire','whole']): return 'region'
    return 'woreda'

# Quick test
tq = 'What is the soil and water condition in Dire Dawa?'
#print(f'Q: "{tq}"')
#print(f'Region: {detect_region(tq)}')
#print(f'Layers: {detect_layers(tq)}')
