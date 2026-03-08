from __future__ import annotations

import logging
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ingest import load_gene_rows, load_pdf_chunks
from app.rag import RagService
from app.schemas import ChatRequest, ChatResponse, IngestResponse, SourceItem
from app.settings import get_settings

settings = get_settings()
rag = RagService(settings)
logger = logging.getLogger(__name__)
bootstrap_lock = threading.Lock()

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


def ingest_papers_impl() -> IngestResponse:
    base = Path("data/papers")
    if not base.exists():
        raise HTTPException(status_code=404, detail="data/papers not found")
    items = load_pdf_chunks(base)
    inserted = rag.add_documents(settings.qdrant_papers_collection, items)
    return IngestResponse(inserted=inserted, collection=settings.qdrant_papers_collection)


def ingest_genes_impl(filename: str = "genes.csv", collection: str | None = None) -> IngestResponse:
    file_path = Path("data/genes") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    items = load_gene_rows(file_path)
    target_collection = collection or settings.qdrant_genes_collection
    inserted = rag.add_documents(target_collection, items)
    return IngestResponse(inserted=inserted, collection=target_collection)


@app.post(f"{settings.api_prefix}/ingest/papers", response_model=IngestResponse)
def ingest_papers() -> IngestResponse:
    return ingest_papers_impl()


@app.post(f"{settings.api_prefix}/ingest/genes", response_model=IngestResponse)
def ingest_genes(filename: str = "genes.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename)


@app.post(f"{settings.api_prefix}/ingest/genes_firmness", response_model=IngestResponse)
def ingest_genes_firmness(filename: str = "genes_firmness.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection=settings.qdrant_genes_firmness_collection)


def _auto_ingest_worker() -> None:
    try:
        if not rag.collection_exists(settings.qdrant_papers_collection):
            try:
                result = ingest_papers_impl()
                print(f"[auto-ingest] papers inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] papers failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip papers (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_collection):
            try:
                result = ingest_genes_impl(filename=settings.auto_ingest_genes_filename)
                print(f"[auto-ingest] genes inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_firmness_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_firmness_filename,
                    collection=settings.qdrant_genes_firmness_collection,
                )
                print(f"[auto-ingest] genes_firmness inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_firmness failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_firmness (collection exists)", flush=True)
    except Exception:
        logger.exception("auto-ingest failed")


def ensure_bootstrap_ingested() -> None:
    if rag.collection_exists(settings.qdrant_papers_collection) and rag.collection_exists(
        settings.qdrant_genes_collection
    ):
        return

    with bootstrap_lock:
        if not rag.collection_exists(settings.qdrant_papers_collection):
            try:
                result = ingest_papers_impl()
                print(f"[bootstrap-chat] papers inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[bootstrap-chat] papers failed: {exc}", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_collection):
            try:
                result = ingest_genes_impl(filename=settings.auto_ingest_genes_filename)
                print(f"[bootstrap-chat] genes inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[bootstrap-chat] genes failed: {exc}", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_firmness_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_firmness_filename,
                    collection=settings.qdrant_genes_firmness_collection,
                )
                print(f"[bootstrap-chat] genes_firmness inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[bootstrap-chat] genes_firmness failed: {exc}", flush=True)


@app.on_event("startup")
def on_startup() -> None:
    if not settings.auto_ingest_on_startup:
        logger.info("auto-ingest disabled")
        return
    threading.Thread(target=_auto_ingest_worker, daemon=True).start()


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    if settings.auto_ingest_on_startup:
        ensure_bootstrap_ingested()

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
