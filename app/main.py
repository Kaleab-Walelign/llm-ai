"""
NRMS AI Assistant API — FastAPI (nrms_8regions.ipynb).

Run:  ./run.sh
Docs: http://localhost:8001/docs
Demo: http://localhost:8001/assistant
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ai import get_chat_manager
from app.config import CORS_ORIGINS, DATA_DIR, GEOSERVER_BASE, GEMINI_API_KEY
from app.detection import TOPIC_TO_LAYERS, detect_admin_level, detect_layers
from app.layers import LAYER_CLASSIFY
from app.regions import (
    ACTIVE_REGIONS,
    PLANNED_REGIONS,
    REGION_REGISTRY,
    detect_region,
)
from app.schemas import AnalyzeRequest, ChatRequest, ChatResponse
from app.spatial import run_spatial_analysis
from app.tools import (
    compare_woredas,
    get_region_report,
    get_woreda_report,
    get_zone_report,
)

STATIC = Path(__file__).resolve().parent.parent / "static"
STATIC.mkdir(exist_ok=True)

app = FastAPI(
    title="NRMS AI Assistant API",
    description="Ethiopia National Rangeland Monitoring System — 8 regions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    return obj


@app.get("/")
def root():
    return {
        "service": "NRMS AI Assistant",
        "docs": "/docs",
        "assistant": "/assistant",
        "active_regions": ACTIVE_REGIONS,
        "planned_regions": PLANNED_REGIONS,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini": bool(GEMINI_API_KEY),
        "data_dir": str(DATA_DIR),
        "geoserver": GEOSERVER_BASE,
    }


@app.get("/assistant")
def assistant_page():
    page = STATIC / "assistant.html"
    if not page.is_file():
        raise HTTPException(404, "static/assistant.html not found")
    return FileResponse(page)


@app.get("/api/regions")
def api_regions():
    return [
        {
            "key": k,
            "name": v["display_name"],
            "status": v["status"],
            "layers": list(v["layers"].keys()),
        }
        for k, v in REGION_REGISTRY.items()
    ]


@app.get("/api/layers")
def api_layers():
    return {"layer_keys": list(LAYER_CLASSIFY.keys()), "topics": TOPIC_TO_LAYERS}


@app.get("/api/detect")
def api_detect(q: str = Query(...)):
    rk = detect_region(q)
    return {
        "region_key": rk,
        "region_name": REGION_REGISTRY[rk]["display_name"],
        "layers": detect_layers(q, rk),
        "admin_level": detect_admin_level(q),
    }


@app.post("/api/chat", response_model=ChatResponse)
def api_chat(body: ChatRequest):
    out = get_chat_manager().ask(body.message.strip(), body.session_id)
    if out["error"] and not out["reply"]:
        raise HTTPException(503, out["error"])
    return ChatResponse(**out)


@app.post("/api/chat/session")
def api_new_session():
    return {"session_id": get_chat_manager().new_session()}


@app.post("/api/chat/session/{session_id}/reset")
def api_reset_session(session_id: str):
    get_chat_manager().reset(session_id)
    return {"session_id": session_id, "reset": True}


@app.get("/api/reports/woreda")
def api_woreda(woreda: str, layers: str = "summary", region: str = "auto"):
    return _json_safe(get_woreda_report(woreda, layers=layers, region=region))


@app.get("/api/reports/zone")
def api_zone(zone: str, layers: str = "summary", region: str = "auto"):
    return _json_safe(get_zone_report(zone, layers=layers, region=region))


@app.get("/api/reports/region")
def api_region(region: str = "Afar", layers: str = "summary"):
    return _json_safe(get_region_report(region, layers=layers))


@app.get("/api/reports/compare")
def api_compare(woredas: str, layer: str = "rangeland", region: str = "auto"):
    return _json_safe(compare_woredas(woredas, layer=layer, region=region))


@app.get("/api/analyze")
def api_analyze_get(
    area_name: str,
    region: str = "auto",
    layers: str = "summary",
    admin_level: str | None = None,
):
    return api_analyze_post(
        AnalyzeRequest(
            area_name=area_name,
            region=region,
            layers=layers,
            admin_level=admin_level,
        )
    )


@app.post("/api/analyze")
def api_analyze_post(body: AnalyzeRequest):
    rk = body.region if body.region in REGION_REGISTRY else detect_region(
        f"{body.area_name} {body.layers}"
    )
    admin = body.admin_level or detect_admin_level(f"{body.area_name} {body.layers}")
    lkeys = detect_layers(body.layers, rk)
    explicit = [
        x.strip()
        for x in body.layers.split(",")
        if x.strip() in REGION_REGISTRY[rk]["layers"]
    ]
    if explicit:
        lkeys = explicit
    return _json_safe(run_spatial_analysis(body.area_name, lkeys, rk, admin))
