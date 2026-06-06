"""Parse user questions into woreda + indicator(s) + time."""

from __future__ import annotations

from dataclasses import dataclass

from app.boundaries import list_woreda_names
from app.data_catalog import list_available_indicators
from app.detection import detect_layers
from app.timeseries import parse_time_from_text


@dataclass
class QueryIntent:
    woreda: str
    indicators: list[str]
    time_hint: dict | None = None
    raw_question: str = ""


def detect_woreda(text: str) -> str | None:
    try:
        names = list_woreda_names()
    except FileNotFoundError:
        return None
    t = text.lower()
    for name in sorted(names, key=len, reverse=True):
        if name.lower() in t:
            return name
    return None


def parse_intent(question: str) -> QueryIntent:
    q = question.strip()
    woreda = detect_woreda(q)
    if not woreda:
        raise ValueError(
            "Could not identify a woreda in your question. "
            "Please include a woreda name, e.g. 'Dubti' or 'Awale'."
        )

    indicators = detect_layers(q)
    available = set(list_available_indicators())
    indicators = [i for i in indicators if i in available]
    if not indicators:
        indicators = ["rangeland"]

    time_hint = parse_time_from_text(q)
    return QueryIntent(
        woreda=woreda,
        indicators=indicators,
        time_hint=time_hint,
        raw_question=q,
    )
