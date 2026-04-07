from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=6, ge=1, le=20)
    route: Literal["auto", "papers", "genes", "hybrid"] = "auto"
    llm_api_key: str | None = None
    llm_base_url: str | None = None
    llm_model: str | None = None


class SourceItem(BaseModel):
    source_type: str
    source_id: str
    score: float
    title: str | None = None
    chunk_text: str
    page: int | None = None
    trait: str | None = None
    reference_genome: str | None = None
    coordinate_note: str | None = None


class ChatResponse(BaseModel):
    answer: str
    route_used: str
    sources: list[SourceItem]


class IngestResponse(BaseModel):
    inserted: int
    collection: str
