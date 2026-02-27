from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ingest import load_gene_rows, load_pdf_chunks
from app.rag import RagService
from app.schemas import ChatRequest, ChatResponse, IngestResponse, SourceItem
from app.settings import get_settings

settings = get_settings()
rag = RagService(settings)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post(f"{settings.api_prefix}/ingest/papers", response_model=IngestResponse)
def ingest_papers() -> IngestResponse:
    base = Path("data/papers")
    if not base.exists():
        raise HTTPException(status_code=404, detail="data/papers not found")
    items = load_pdf_chunks(base)
    inserted = rag.add_documents(settings.qdrant_papers_collection, items)
    return IngestResponse(inserted=inserted, collection=settings.qdrant_papers_collection)


@app.post(f"{settings.api_prefix}/ingest/genes", response_model=IngestResponse)
def ingest_genes(filename: str = "genes.csv") -> IngestResponse:
    file_path = Path("data/genes") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    items = load_gene_rows(file_path)
    inserted = rag.add_documents(settings.qdrant_genes_collection, items)
    return IngestResponse(inserted=inserted, collection=settings.qdrant_genes_collection)


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    route = rag.route(body.question, body.route)
    sources = rag.retrieve(body.question, route=route, top_k=body.top_k)
    if not sources:
        return ChatResponse(answer="未检索到相关材料。", route_used=route, sources=[])

    answer = rag.generate(body.question, sources)
    response_sources = [
        SourceItem(
            source_type=s.source_type,
            source_id=s.source_id,
            score=s.score,
            title=s.title,
            chunk_text=s.chunk_text,
            page=s.page,
        )
        for s in sources
    ]
    return ChatResponse(answer=answer, route_used=route, sources=response_sources)
