"""Gemini explanation layer — receives compact analytics JSON."""

from __future__ import annotations

import json
import logging
import threading
import uuid
from typing import Any

from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

from app.analytics import build_compact_json, run_query
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.intent import parse_intent

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are the ATI NRMS Expert — professional rangeland monitoring
assistant for Ethiopia's National Rangeland Monitoring System.

You receive compact JSON analytics (woreda, indicators, scores, labels, time periods).
Never invent values — use only the numbers in the JSON.

Structure your answer:
1) Brief summary for the woreda and time period
2) Key findings per indicator (score, label, what it means)
3) Practical recommendations for pastoralists and policymakers
4) Flag URGENT when any indicator is Very Low or Low

Be concise, professional, and grounded in the provided data."""


def _create_model() -> genai.GenerativeModel:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_INSTRUCTION,
    )


def explain_with_gemini(question: str, compact: dict[str, Any]) -> str:
    model = _create_model()
    payload = json.dumps(compact, indent=2)
    prompt = (
        f"User question: {question}\n\n"
        f"Analytics data (JSON):\n{payload}\n\n"
        "Provide a clear expert explanation based on this data."
    )
    response = model.generate_content(prompt)
    return response.text or ""


class ChatManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, list[dict[str, str]]] = {}

    def new_session(self) -> str:
        sid = str(uuid.uuid4())
        with self._lock:
            self._sessions[sid] = []
        return sid

    def reset(self, session_id: str) -> None:
        with self._lock:
            self._sessions[session_id] = []

    def ask(self, question: str, session_id: str | None = None) -> dict[str, Any]:
        sid = session_id or str(uuid.uuid4())
        try:
            intent = parse_intent(question)
            result = run_query(intent)
            compact = build_compact_json(intent, result)

            if not GEMINI_API_KEY:
                return {
                    "session_id": sid,
                    "reply": json.dumps(compact, indent=2),
                    "data": compact,
                    "error": "GEMINI_API_KEY not set — returning raw analytics only.",
                }

            reply = explain_with_gemini(question, compact)
            with self._lock:
                if sid not in self._sessions:
                    self._sessions[sid] = []
                self._sessions[sid].append({"q": question, "a": reply})

            return {
                "session_id": sid,
                "reply": reply,
                "data": compact,
                "error": None,
            }
        except ValueError as exc:
            return {"session_id": sid, "reply": None, "error": str(exc), "data": None}
        except Exception as exc:
            msg = str(exc)
            if "429" in msg:
                msg = "Rate limit exceeded. Wait about 60 seconds and try again."
            logger.exception("Chat pipeline failed")
            return {"session_id": sid, "reply": None, "error": msg, "data": None}


_manager: ChatManager | None = None


def get_chat_manager() -> ChatManager:
    global _manager
    if _manager is None:
        _manager = ChatManager()
    return _manager
