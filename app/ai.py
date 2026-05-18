"""Cell 12: Gemini AI with automatic function calling."""

from __future__ import annotations

import threading
import uuid
from typing import Any

from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.regions import ACTIVE_REGIONS, PLANNED_REGIONS
from app.tools import (
    compare_woredas,
    get_region_report,
    get_woreda_report,
    get_zone_report,
)

SYSTEM_INSTRUCTION = f"""You are the ATI NRMS Expert — professional rangeland monitoring
assistant for Ethiopia's National Rangeland Monitoring System.

ACTIVE REGIONS (data available now): {", ".join(ACTIVE_REGIONS)}
PLANNED REGIONS (say 'data coming soon' if asked): {", ".join(PLANNED_REGIONS)}

TOOLS — always call one BEFORE answering any data question:
  get_woreda_report  → conditions for a specific woreda
  get_zone_report    → conditions for a zone (admin level 2)
  get_region_report  → overall conditions for an entire region
  compare_woredas    → side-by-side comparison of multiple woredas

RULES:
- Never guess or invent values. Always use tool data.
- For planned regions, explain data is not yet on NRMS and name the active ones.
- Structure answers: 1) summary  2) key findings per layer  3) recommendations.
- Flag URGENT when any layer is Very Low or Low.
- Use the 'ai_context' field from tool results to ground your answer.
- Be concise and professional. Use the actual numbers from the data."""


def _create_model() -> genai.GenerativeModel:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        tools=[get_woreda_report, get_zone_report, get_region_report, compare_woredas],
        system_instruction=SYSTEM_INSTRUCTION,
    )


class ChatManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, Any] = {}
        self._model: genai.GenerativeModel | None = None

    def _model_instance(self) -> genai.GenerativeModel:
        if self._model is None:
            self._model = _create_model()
        return self._model

    def new_session(self) -> str:
        sid = str(uuid.uuid4())
        with self._lock:
            self._sessions[sid] = self._model_instance().start_chat(
                enable_automatic_function_calling=True
            )
        return sid

    def reset(self, session_id: str) -> None:
        with self._lock:
            self._sessions[session_id] = self._model_instance().start_chat(
                enable_automatic_function_calling=True
            )

    def ask(self, question: str, session_id: str | None = None) -> dict[str, Any]:
        with self._lock:
            if session_id and session_id in self._sessions:
                sid, chat = session_id, self._sessions[session_id]
            else:
                sid = session_id or str(uuid.uuid4())
                chat = self._model_instance().start_chat(
                    enable_automatic_function_calling=True
                )
                self._sessions[sid] = chat

        try:
            response = chat.send_message(question)
            return {"session_id": sid, "reply": response.text or "", "error": None}
        except Exception as exc:
            msg = str(exc)
            if "429" in msg:
                msg = "Rate limit exceeded. Wait about 60 seconds and try again."
            return {"session_id": sid, "reply": None, "error": msg}


_manager: ChatManager | None = None


def get_chat_manager() -> ChatManager:
    global _manager
    if _manager is None:
        _manager = ChatManager()
    return _manager
