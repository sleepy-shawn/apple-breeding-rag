from __future__ import annotations

import logging
import threading
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.ingest import load_gene_rows, load_pdf_chunks
from app.rag import RagService
from app.schemas import ChatRequest, ChatResponse, IngestResponse, SourceItem
from app.settings import COLLECTION_REGISTRY, DEFAULT_INGEST_FILENAMES, get_settings

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


def ingest_papers_impl(replace: bool = False, pdf_paths: list[Path] | None = None) -> IngestResponse:
    base = Path("data/papers")
    if not base.exists():
        raise HTTPException(status_code=404, detail="data/papers not found")
    items = load_pdf_chunks(base, pdf_paths=pdf_paths)
    collection = settings.collection_name("papers")
    inserted = (
        rag.replace_documents(collection, items)
        if replace
        else rag.add_documents(collection, items)
    )
    return IngestResponse(inserted=inserted, collection=collection)


def ingest_genes_impl(filename: str = "genes.csv", collection_key: str = "genes", replace: bool = False) -> IngestResponse:
    file_path = Path("data/genes") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    if collection_key not in COLLECTION_REGISTRY:
        allowed = ", ".join(k for k in COLLECTION_REGISTRY if k != "papers")
        raise HTTPException(status_code=400, detail=f"collection must be one of: {allowed}")
    target_collection = settings.collection_name(collection_key)
    items = load_gene_rows(file_path)
    inserted = rag.replace_documents(target_collection, items) if replace else rag.add_documents(target_collection, items)
    return IngestResponse(inserted=inserted, collection=target_collection)


@app.post(f"{settings.api_prefix}/ingest/papers", response_model=IngestResponse)
def ingest_papers() -> IngestResponse:
    return ingest_papers_impl(replace=True)


@app.post(f"{settings.api_prefix}/ingest/papers/add", response_model=IngestResponse)
def ingest_papers_add(filenames: list[str]) -> IngestResponse:
    base = Path("data/papers")
    pdf_paths = [base / f for f in filenames if (base / f).exists()]
    return ingest_papers_impl(replace=False, pdf_paths=pdf_paths)


@app.post(f"{settings.api_prefix}/ingest/{{collection_key}}", response_model=IngestResponse)
def ingest_genes(collection_key: str, filename: str | None = None) -> IngestResponse:
    if collection_key not in COLLECTION_REGISTRY or collection_key == "papers":
        allowed = ", ".join(k for k in COLLECTION_REGISTRY if k != "papers")
        raise HTTPException(status_code=400, detail=f"collection_key must be one of: {allowed}")
    if filename is None:
        filename = settings.ingest_filename(collection_key)
    return ingest_genes_impl(filename=filename, collection_key=collection_key, replace=True)


@app.post(f"{settings.api_prefix}/upload/papers")
async def upload_papers(files: list[UploadFile] = File(...), ingest: bool = True) -> dict:
    papers_dir = Path("data/papers")
    papers_dir.mkdir(parents=True, exist_ok=True)

    saved: list[str] = []
    saved_paths: list[Path] = []
    for f in files:
        name = Path(f.filename or "").name
        if not name:
            continue
        if not name.lower().endswith(".pdf"):
            continue
        target = papers_dir / name
        content = await f.read()
        target.write_bytes(content)
        saved.append(name)
        saved_paths.append(target)

    if not saved:
        raise HTTPException(status_code=400, detail="No valid PDF file uploaded")

    inserted = 0
    collection = settings.collection_name("papers")
    if ingest:
        result = ingest_papers_impl(pdf_paths=saved_paths)
        inserted = result.inserted
        collection = result.collection

    return {
        "saved_files": saved,
        "saved_count": len(saved),
        "ingested": ingest,
        "inserted": inserted,
        "collection": collection,
    }


@app.post(f"{settings.api_prefix}/upload/genes")
async def upload_genes(file: UploadFile = File(...), ingest: bool = True, collection_key: str = "genes") -> dict:
    name = Path(file.filename or "").name
    if not name:
        raise HTTPException(status_code=400, detail="Filename is required")
    if not (name.lower().endswith(".csv") or name.lower().endswith(".tsv")):
        raise HTTPException(status_code=400, detail="Only CSV/TSV files are supported")

    genes_dir = Path("data/genes")
    genes_dir.mkdir(parents=True, exist_ok=True)
    target = genes_dir / name
    target.write_bytes(await file.read())

    inserted = 0
    target_collection = settings.collection_name(collection_key)
    if ingest:
        result = ingest_genes_impl(filename=name, collection_key=collection_key, replace=True)
        inserted = result.inserted
        target_collection = result.collection

    return {
        "saved_file": name,
        "ingested": ingest,
        "inserted": inserted,
        "collection": target_collection,
    }


def _auto_ingest_worker() -> None:
    try:
        if not rag.collection_exists(settings.collection_name("papers")):
            try:
                result = ingest_papers_impl()
                print(f"[auto-ingest] papers inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] papers failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip papers (collection exists)", flush=True)

        for key, filename in DEFAULT_INGEST_FILENAMES.items():
            col_name = settings.collection_name(key)
            if not rag.collection_exists(col_name):
                try:
                    result = ingest_genes_impl(filename=filename, collection_key=key)
                    print(f"[auto-ingest] {key} inserted={result.inserted}", flush=True)
                except Exception as exc:
                    print(f"[auto-ingest] {key} failed: {exc}", flush=True)
            else:
                print(f"[auto-ingest] skip {key} (collection exists)", flush=True)
    except Exception:
        logger.exception("auto-ingest failed")


def ensure_bootstrap_ingested() -> None:
    papers_col = settings.collection_name("papers")
    genes_col = settings.collection_name("genes")
    if rag.collection_exists(papers_col) and rag.collection_exists(genes_col):
        return

    with bootstrap_lock:
        if not rag.collection_exists(papers_col):
            try:
                result = ingest_papers_impl()
                print(f"[bootstrap-chat] papers inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[bootstrap-chat] papers failed: {exc}", flush=True)

        for key in ("genes", "genes_firmness"):
            col_name = settings.collection_name(key)
            if not rag.collection_exists(col_name):
                try:
                    result = ingest_genes_impl(
                        filename=settings.ingest_filename(key),
                        collection_key=key,
                    )
                    print(f"[bootstrap-chat] {key} inserted={result.inserted}", flush=True)
                except Exception as exc:
                    print(f"[bootstrap-chat] {key} failed: {exc}", flush=True)


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

    answer = rag.generate(
        body.question,
        sources,
        llm_api_key=body.llm_api_key,
        llm_base_url=body.llm_base_url,
        llm_model=body.llm_model,
    )
    response_sources = [
        SourceItem(
            source_type=s.source_type,
            source_id=s.source_id,
            score=s.score,
            title=s.title,
            chunk_text=s.chunk_text,
            page=s.page,
            trait=s.trait,
            reference_genome=s.reference_genome,
            coordinate_note=s.coordinate_note,
        )
        for s in sources
    ]
    return ChatResponse(answer=answer, route_used=route, sources=response_sources)
