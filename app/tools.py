"""Report helpers — use local analytics pipeline."""

from __future__ import annotations

from app.analytics import run_query
from app.context import build_ai_context
from app.data_catalog import list_available_indicators
from app.detection import detect_layers
from app.intent import QueryIntent
from app.regions import REGION_REGISTRY, detect_region
from app.timeseries import parse_time_from_text


def get_woreda_report(
    woreda_name: str,
    layers: str = "summary",
    region: str = "auto",
) -> dict:
    rk = region if region in REGION_REGISTRY else detect_region(woreda_name + " " + layers)
    lkeys = detect_layers(layers, rk)
    explicit = [l.strip() for l in layers.split(",") if l.strip()]
    if explicit:
        available = set(list_available_indicators())
        lkeys = [l for l in explicit if l in available] or lkeys
    if not lkeys:
        lkeys = ["rangeland", "climate", "vegetation"]

    intent = QueryIntent(
        woreda=woreda_name,
        indicators=lkeys,
        time_hint=parse_time_from_text(layers),
        raw_question=layers,
    )
    result = run_query(intent)
    if "error" not in result:
        result["ai_context"] = build_ai_context({
            "area": woreda_name,
            "layers": result.get("layers", {}),
        })
    return result


def get_zone_report(zone_name: str, layers: str = "summary", region: str = "auto") -> dict:
    return {
        "error": "Zone-level reports require GeoServer WFS. Use woreda-level queries with local data.",
    }


def get_region_report(region_name: str = "Afar", layers: str = "summary") -> dict:
    return {
        "error": "Region-level reports require GeoServer WFS. Use woreda-level queries with local data.",
    }


def compare_woredas(woreda_names: str, layer: str = "rangeland", region: str = "auto") -> dict:
    names = [n.strip() for n in woreda_names.split(",") if n.strip()]
    lk = layer.strip() or "rangeland"
    comp = {"layer": lk, "woredas": {}}
    for name in names:
        intent = QueryIntent(woreda=name, indicators=[lk], raw_question=woreda_names)
        r = run_query(intent)
        comp["woredas"][name] = r["layers"].get(lk, r.get("error", "No data"))
    lines = [f"COMPARISON — {lk.upper()}", ""]
    for name, d in sorted(
        comp["woredas"].items(),
        key=lambda x: x[1].get("mean", 0) if isinstance(x[1], dict) else 0,
    ):
        if isinstance(d, dict) and "mean" in d:
            lines.append(f"  {name}: {d['mean']} → {d['label']} — {d.get('description', '')}")
        else:
            lines.append(f"  {name}: {d}")
    comp["ai_context"] = "\n".join(lines)
    return comp
