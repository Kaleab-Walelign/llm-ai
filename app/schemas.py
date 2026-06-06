"""API request/response models."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str | None = None
    error: str | None = None
    data: dict | None = None


class AnalyzeRequest(BaseModel):
    area_name: str
    region: str = "auto"
    layers: str = "summary"
    admin_level: str | None = None
