"""Cell 3 — Region registry (8 regions + aliases)."""
from app.config import resolve_tif_path

REGION_REGISTRY = {

    # ══════════════════════════════════════════════════════════════════════════
    # AFAR  ✅ active
    # ══════════════════════════════════════════════════════════════════════════
    'afar': {
        'display_name': 'Afar',
        'status': 'active',
        'wfs': 'geonode:afar_wereda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:afar_rangeland',
            'biomass':       'geonode:afar_abg',
            'ndvi':          'geonode:afar_ndvi',
            'rainfall':      'geonode:afar_rainfall',
            'climate':       'geonode:afar_climate_weighted',
            'vegetation':    'geonode:afar_vegetation_weighted',
            'soil':          'geonode:afar_soil_weighted',
            'soil_bulk':     'geonode:afar_soil_bd',
            'soil_moisture': 'geonode:afar_soil_moisture',
            'soil_ph':       'geonode:afar_soil_ph',
            'soil_carbon':   'geonode:afar_som',
            'temperature':   'geonode:afar_temprature',
            'water':         'geonode:afar_water_weighted',
            'livestock':     'geonode:afar_livestock_weighted',
            'encroachment':  'geonode:afar_encroachment',
            'slope':         'geonode:afar_slope',
        },
        'local_tifs': {
            'rangeland':  '/opt/data/geoserver_data/afar/rangeland_health/rangeland_health_afar.tif',
            'climate':    '/opt/data/geoserver_data/afar/climate/climate_weighted/Climate.tif',
            'water':      '/opt/data/geoserver_data/afar/water/water_weighted/water.tif',
            'livestock':   '/opt/data/geoserver_data/afar/livestock/livestock_weighted/livestock.tif',
            'vegetation':  '/opt/data/geoserver_data/afar/vegetation/vegetation_weighted/Vegetation.tif',
            'soil':        '/opt/data/geoserver_data/afar/soil/soil_weighted/Soil.tif',
        },
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DIRE DAWA  ✅ active
    # ══════════════════════════════════════════════════════════════════════════
    'diredawa': {
        'display_name': 'Dire Dawa',
        'status': 'active',
        'wfs': 'geonode:diredawa_woreda',      # ← confirm exact WFS name
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:dire_rangeland',
            'biomass':       'geonode:dire_agb',
            'ndvi':          'geonode:dire_ndvi',
            'rainfall':      'geonode:dire_rainfall',
            'climate':       'geonode:dire_climate',
            'vegetation':    'geonode:dire_vegetation_weighted',
            'soil':          'geonode:dire_soil_weighted',
            'soil_bulk':     'geonode:dire_soilbd',
            'soil_moisture': 'geonode:dire_soil_moisture',
            'soil_ph':       'geonode:dire_soil_ph',
            'soil_carbon':   'geonode:dire_som',
            'temperature':   'geonode:dire_temprature',
            'water':         'geonode:dire_water',
            'livestock':     'geonode:dire_livestock',
            'encroachment':  'geonode:dire_encroachment',
            'slope':         'geonode:dire_slope',
            'lulc':          'geonode:dire_lulc',
        },
        'local_tifs': {
            'rangeland':  '/opt/data/geoserver_data/diredawa/rangeland/rangeland.tif',
            'soil':  '/opt/data/geoserver_data/diredawa/soil/soil_weighted/Soil.tif',
            'vegetation':  '/opt/data/geoserver_data/diredawa/vegetation/weighted/Vegetation.tif',
            'water':  '/opt/data/geoserver_data/diredawa/water/Water_rec.tif',
            'climate':  '/opt/data/geoserver_data/climate/climate_weighted/Climate_Condition.tif',
            'livestock':  '/opt/data/geoserver_data/livestock/Livestock.tif',
        },
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SOMALI  🔜 planned — update layer names when data is on GeoServer
    # ══════════════════════════════════════════════════════════════════════════
    'somali': {
        'display_name': 'Somali',
        'status': 'planned',
        'wfs': 'geonode:somali_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:somali_rangeland',
            'biomass':       'geonode:somali_agb',
            'ndvi':          'geonode:somali_ndvi',
            'rainfall':      'geonode:somali_rainfall',
            'climate':       'geonode:somali_climate_weighted',
            'vegetation':    'geonode:somali_vegetation_weighted',
            'soil':          'geonode:somali_soil_weighted',
            'soil_bulk':     'geonode:somali_soil_bd',
            'soil_moisture': 'geonode:somali_soil_moisture',
            'soil_ph':       'geonode:somali_soil_ph',
            'soil_carbon':   'geonode:somali_som',
            'temperature':   'geonode:somali_temprature',
            'water':         'geonode:somali_water_weighted',
            'livestock':     'geonode:somali_livestock_weighted',
            'encroachment':  'geonode:somali_encroachment',
            'slope':         'geonode:somali_slope',
        },
        'local_tifs': {},
    },

    # ══════════════════════════════════════════════════════════════════════════
    # OROMIA  🔜 planned
    # ══════════════════════════════════════════════════════════════════════════
    'oromia': {
        'display_name': 'Oromia',
        'status': 'planned',
        'wfs': 'geonode:oromia_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:oromia_rangeland',
            'biomass':       'geonode:oromia_agb',
            'ndvi':          'geonode:oromia_ndvi',
            'rainfall':      'geonode:oromia_rainfall',
            'climate':       'geonode:oromia_climate_weighted',
            'vegetation':    'geonode:oromia_vegetation_weighted',
            'soil':          'geonode:oromia_soil_weighted',
            'soil_bulk':     'geonode:oromia_soil_bd',
            'soil_moisture': 'geonode:oromia_soil_moisture',
            'soil_ph':       'geonode:oromia_soil_ph',
            'soil_carbon':   'geonode:oromia_som',
            'temperature':   'geonode:oromia_temprature',
            'water':         'geonode:oromia_water_weighted',
            'livestock':     'geonode:oromia_livestock_weighted',
            'encroachment':  'geonode:oromia_encroachment',
            'slope':         'geonode:oromia_slope',
            'lulc':          'geonode:oromia_lulc',
        },
        'local_tifs': {},
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SOUTH ETHIOPIA  🔜 planned
    # ══════════════════════════════════════════════════════════════════════════
    'south': {
        'display_name': 'South Ethiopia',
        'status': 'planned',
        'wfs': 'geonode:south_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:south_rangeland',
            'biomass':       'geonode:south_agb',
            'ndvi':          'geonode:south_ndvi',
            'rainfall':      'geonode:south_rainfall',
            'climate':       'geonode:south_climate_weighted',
            'vegetation':    'geonode:south_vegetation_weighted',
            'soil':          'geonode:south_soil_weighted',
            'soil_bulk':     'geonode:south_soil_bd',
            'soil_moisture': 'geonode:south_soil_moisture',
            'soil_ph':       'geonode:south_soil_ph',
            'soil_carbon':   'geonode:south_som',
            'temperature':   'geonode:south_temprature',
            'water':         'geonode:south_water_weighted',
            'livestock':     'geonode:south_livestock_weighted',
            'encroachment':  'geonode:south_encroachment',
            'slope':         'geonode:south_slope',
        },
        'local_tifs': {},
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SOUTH WEST ETHIOPIA  🔜 planned
    # ══════════════════════════════════════════════════════════════════════════
    'southwest': {
        'display_name': 'South West Ethiopia',
        'status': 'planned',
        'wfs': 'geonode:southwest_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:southwest_rangeland',
            'biomass':       'geonode:southwest_agb',
            'ndvi':          'geonode:southwest_ndvi',
            'rainfall':      'geonode:southwest_rainfall',
            'climate':       'geonode:southwest_climate_weighted',
            'vegetation':    'geonode:southwest_vegetation_weighted',
            'soil':          'geonode:southwest_soil_weighted',
            'soil_bulk':     'geonode:southwest_soil_bd',
            'soil_moisture': 'geonode:southwest_soil_moisture',
            'soil_ph':       'geonode:southwest_soil_ph',
            'soil_carbon':   'geonode:southwest_som',
            'temperature':   'geonode:southwest_temprature',
            'water':         'geonode:southwest_water_weighted',
            'livestock':     'geonode:southwest_livestock_weighted',
            'encroachment':  'geonode:southwest_encroachment',
            'slope':         'geonode:southwest_slope',
        },
        'local_tifs': {},
    },

    # ══════════════════════════════════════════════════════════════════════════
    # GAMBELLA  🔜 planned
    # ══════════════════════════════════════════════════════════════════════════
    'gambella': {
        'display_name': 'Gambella',
        'status': 'planned',
        'wfs': 'geonode:gambella_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:gambella_rangeland',
            'biomass':       'geonode:gambella_agb',
            'ndvi':          'geonode:gambella_ndvi',
            'rainfall':      'geonode:gambella_rainfall',
            'climate':       'geonode:gambella_climate_weighted',
            'vegetation':    'geonode:gambella_vegetation_weighted',
            'soil':          'geonode:gambella_soil_weighted',
            'soil_bulk':     'geonode:gambella_soil_bd',
            'soil_moisture': 'geonode:gambella_soil_moisture',
            'soil_ph':       'geonode:gambella_soil_ph',
            'soil_carbon':   'geonode:gambella_som',
            'temperature':   'geonode:gambella_temprature',
            'water':         'geonode:gambella_water_weighted',
            'livestock':     'geonode:gambella_livestock_weighted',
            'encroachment':  'geonode:gambella_encroachment',
            'slope':         'geonode:gambella_slope',
        },
        'local_tifs': {},
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BENSHANGUL-GUMUZ  🔜 planned
    # ══════════════════════════════════════════════════════════════════════════
    'benshangul': {
        'display_name': 'Benshangul-Gumuz',
        'status': 'planned',
        'wfs': 'geonode:benshangul_woreda',
        'adm_fields': {'woreda': 'adm3_en', 'zone': 'adm2_en', 'region': 'adm1_en'},
        'layers': {
            'rangeland':     'geonode:benshangul_rangeland',
            'biomass':       'geonode:benshangul_agb',
            'ndvi':          'geonode:benshangul_ndvi',
            'rainfall':      'geonode:benshangul_rainfall',
            'climate':       'geonode:benshangul_climate_weighted',
            'vegetation':    'geonode:benshangul_vegetation_weighted',
            'soil':          'geonode:benshangul_soil_weighted',
            'soil_bulk':     'geonode:benshangul_soil_bd',
            'soil_moisture': 'geonode:benshangul_soil_moisture',
            'soil_ph':       'geonode:benshangul_soil_ph',
            'soil_carbon':   'geonode:benshangul_som',
            'temperature':   'geonode:benshangul_temprature',
            'water':         'geonode:benshangul_water_weighted',
            'livestock':     'geonode:benshangul_livestock_weighted',
            'encroachment':  'geonode:benshangul_encroachment',
            'slope':         'geonode:benshangul_slope',
        },
        'local_tifs': {},
    },
}

REGION_ALIASES = {
    # Afar
    'afar': 'afar',
    'afar region': 'afar',
    'afar state': 'afar',

    'afar dubti': 'dubti',
    'afar elidar': 'elidar',
    'afar asayita': 'asayita',
    'afar afambo': 'afambo',
    'afar mile': 'mile',
    'afar chifra': 'chifra',
    'afar dubti town': 'dubti town',
    'afar kori': 'kori',
    'afar adar': 'adar',
    'afar gerani': 'gerani',
    'afar asayita town': 'asayita town',
    'afar samera logiya town': 'samera logiya town',
    'afar erebti': 'erebti',
    'afar kunneba': 'kunneba',
    'afar abaala': 'abaala',
    'afar megale': 'megale',
    'afar berahile': 'berahile',
    'afar dalol': 'dalol',
    'afar afdera': 'afdera',
    'afar bidu': 'bidu',
    'afar abaala town': 'abaala town',
    'afar amibara': 'amibara',
    'afar awash': 'awash',
    'afar gewane': 'gewane',
    'afar dulecha': 'dulecha',
    'afar gelalu': 'gelalu',
    'afar arguba': 'arguba',
    'afar hanruka': 'hanruka',
    'afar awash town': 'awash town',
    'afar awra': 'awra',
    'afar awra (af)': 'awra',
    'afar euwa': 'euwa',
    'afar teru': 'teru',
    'afar yalo': 'yalo',
    'afar gulina': 'gulina',
    'afar telalek': 'telalek',
    'afar samurobi': 'samurobi',
    'afar dawe': 'dawe',
    'afar dalefage': 'dalefage',
    'afar hadelela': 'hadelela',
        'afar awsi': 'awsi',
    'afar awsi zone 1': 'awsi',
    'afar awsi /zone 1': 'awsi',
    'afar awsi zone1': 'awsi',
    'afar awsi / zone 1': 'awsi',

    'afar kilbati': 'kilbati',
    'afar kilbati zone 2': 'kilbati',
    'afar kilbati /zone2': 'kilbati',
    'afar kilbati zone2': 'kilbati',
    'afar kilbati / zone 2': 'kilbati',

    'afar gabi': 'gabi',
    'afar gabi zone 3': 'gabi',
    'afar gabi /zone 3': 'gabi',
    'afar gabi zone3': 'gabi',
    'afar gabi / zone 3': 'gabi',

    'afar fanti': 'fanti',
    'afar fanti zone 4': 'fanti',
    'afar fanti /zone 4': 'fanti',
    'afar fanti zone4': 'fanti',
    'afar fanti / zone 4': 'fanti',

    'afar hari': 'hari',
    'afar hari zone 5': 'hari',
    'afar hari /zone 5': 'hari',
    'afar hari zone5': 'hari',
    'afar hari / zone 5': 'hari',
    # Dire Dawa (avoid duplicate dict keys — last duplicate wins in Python)
    'dire dawa': 'diredawa', 'diredawa': 'diredawa', 'dire dawa city': 'diredawa', 'dire': 'diredawa','dire dawa': 'diredawa',
    'diredawa': 'diredawa',
    'dire dawa city': 'diredawa',
    'dire': 'diredawa',

    'diredawa adada': 'adada',
    'diredawa awale': 'awale',
    'diredawa ayale gumgum': 'ayale gumgum',
    'diredawa beke halo': 'beke halo',
    'diredawa belewa': 'belewa',
    'diredawa bishan behe': 'bishan behe',
    'diredawa biyoa wale': 'biyoa wale',
    'diredawa chire mite': 'chire mite',
    'diredawa dajuma': 'dajuma',
    'diredawa dibeley': 'dibeley',
    'diredawa elhamer': 'elhamer',
    'diredawa felema': 'felema',
    'diredawa gedenser': 'gedenser',
    'diredawa genderge': 'genderge',
    'diredawa gerbo aneno': 'gerbo aneno',
    'diredawa gole aden': 'gole aden',
    'diredawa halobusa': 'halobusa',
    'diredawa harlabe lina': 'harlabe lina',
    'diredawa hula hulul aseliso': 'hula hulul aseliso',
    'diredawa hulel mojo': 'hulel mojo',
    'diredawa jeldesa': 'jeldesa',
    'diredawa koriso': 'koriso',
    'diredawa kortu kalicha': 'kortu kalicha',
    'diredawa kulau': 'kulau',
    'diredawa lege aneni': 'lege aneni',
    'diredawa lege dini': 'lege dini',
    'diredawa legeade mirga': 'legeade mirga',
    'diredawa legehare legedel': 'legehare legedel',
    'diredawa legeode gunufeta': 'legeode gunufeta',
    'diredawa melka kero': 'melka kero',
    'diredawa mudi aneno': 'mudi aneno',
    'diredawa wahil': 'wahil',
    'diredawa dire dawa': 'diredawa',
    # Somali
    'somali':'somali', 'jijiga':'somali', 'jigjiga':'somali',
    'kebri dahar':'somali', 'gode':'somali', 'warder':'somali',
    'degehabur':'somali', 'shinile':'somali', 'afder':'somali',
    # Oromia
    'oromia':'oromia', 'borena':'oromia', 'borana':'oromia',
    'guji':'oromia', 'bale':'oromia', 'west hararghe':'oromia',
    'east hararghe':'oromia', 'arsi':'oromia',
    # South Ethiopia
    'south ethiopia':'south', 'south':'south', 'snnpr':'south',
    'snnp':'south', 'southern ethiopia':'south', 'konso':'south',
    'derashe':'south', 'burji':'south',
    # South West Ethiopia
    'south west ethiopia':'southwest', 'southwest':'southwest',
    'south west':'southwest', 'bench sheko':'southwest',
    'dawro':'southwest', 'keffa':'southwest',
    # Gambella
    'gambella':'gambella', 'gambela':'gambella',
    'agnewak':'gambella', 'nuer':'gambella',
    # Benshangul-Gumuz
    'benshangul':'benshangul', 'benshangul gumuz':'benshangul',
    'benishangul':'benshangul', 'benigshangul':'benshangul',
    'assosa':'benshangul', 'metekel':'benshangul',
}

def detect_region(text: str) -> str:
    t = text.lower()
    for alias, rkey in sorted(REGION_ALIASES.items(), key=lambda x: -len(x[0])):
        if alias in t:
            return rkey
    return "afar"

def _init_regions() -> None:
    for reg in REGION_REGISTRY.values():
        reg["local_tifs"] = {
            k: resolve_tif_path(v) or v
            for k, v in reg.get("local_tifs", {}).items()
        }

_init_regions()
ACTIVE_REGIONS = [v["display_name"] for v in REGION_REGISTRY.values() if v["status"] == "active"]
PLANNED_REGIONS = [v["display_name"] for v in REGION_REGISTRY.values() if v["status"] == "planned"]
