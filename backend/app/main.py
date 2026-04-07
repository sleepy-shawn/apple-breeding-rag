from __future__ import annotations

import logging
import threading
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
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


def resolve_gene_collection(collection: str | None) -> str:
    mapping = {
        None: settings.qdrant_genes_collection,
        "genes": settings.qdrant_genes_collection,
        "genes_firmness": settings.qdrant_genes_firmness_collection,
        "genes_color": settings.qdrant_genes_color_collection,
        "genes_acidity": settings.qdrant_genes_acidity_collection,
        "genes_harvest": settings.qdrant_genes_harvest_collection,
        "genes_sugar": settings.qdrant_genes_sugar_collection,
        "genes_gdr": settings.qdrant_genes_gdr_collection,
        "genes_gdr_curated": settings.qdrant_genes_gdr_curated_collection,
        "genes_gdr_firmness": settings.qdrant_genes_gdr_firmness_collection,
        "genes_gdr_color": settings.qdrant_genes_gdr_color_collection,
        "genes_gdr_acidity": settings.qdrant_genes_gdr_acidity_collection,
        "genes_gdr_harvest": settings.qdrant_genes_gdr_harvest_collection,
        "genes_gdr_sugar": settings.qdrant_genes_gdr_sugar_collection,
        "genes_gdr_curated_firmness": settings.qdrant_genes_gdr_curated_firmness_collection,
        "genes_gdr_curated_color": settings.qdrant_genes_gdr_curated_color_collection,
        "genes_gdr_curated_acidity": settings.qdrant_genes_gdr_curated_acidity_collection,
        "genes_gdr_curated_harvest": settings.qdrant_genes_gdr_curated_harvest_collection,
        "genes_gdr_curated_sugar": settings.qdrant_genes_gdr_curated_sugar_collection,
    }
    if collection not in mapping:
        allowed = ", ".join(k for k in mapping.keys() if k)
        raise HTTPException(status_code=400, detail=f"collection must be one of: {allowed}")
    return mapping[collection]


def ingest_papers_impl(replace: bool = False, pdf_paths: list[Path] | None = None) -> IngestResponse:
    base = Path("data/papers")
    if not base.exists():
        raise HTTPException(status_code=404, detail="data/papers not found")
    items = load_pdf_chunks(base, pdf_paths=pdf_paths)
    inserted = (
        rag.replace_documents(settings.qdrant_papers_collection, items)
        if replace
        else rag.add_documents(settings.qdrant_papers_collection, items)
    )
    return IngestResponse(inserted=inserted, collection=settings.qdrant_papers_collection)


def ingest_genes_impl(filename: str = "genes.csv", collection: str | None = None, replace: bool = False) -> IngestResponse:
    file_path = Path("data/genes") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"{file_path} not found")
    items = load_gene_rows(file_path)
    target_collection = resolve_gene_collection(collection)
    inserted = rag.replace_documents(target_collection, items) if replace else rag.add_documents(target_collection, items)
    return IngestResponse(inserted=inserted, collection=target_collection)


@app.post(f"{settings.api_prefix}/ingest/papers", response_model=IngestResponse)
def ingest_papers() -> IngestResponse:
    return ingest_papers_impl(replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes", response_model=IngestResponse)
def ingest_genes(filename: str = "genes.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_firmness", response_model=IngestResponse)
def ingest_genes_firmness(filename: str = "genes_firmness_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_firmness", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_color", response_model=IngestResponse)
def ingest_genes_color(filename: str = "genes_color_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_color", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_acidity", response_model=IngestResponse)
def ingest_genes_acidity(filename: str = "genes_acidity_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_acidity", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_harvest", response_model=IngestResponse)
def ingest_genes_harvest(filename: str = "genes_harvest_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_harvest", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_sugar", response_model=IngestResponse)
def ingest_genes_sugar(filename: str = "genes_sugar_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_sugar", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr", response_model=IngestResponse)
def ingest_genes_gdr(filename: str = "genes_gdr.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated", response_model=IngestResponse)
def ingest_genes_gdr_curated(filename: str = "genes_gdr_curated.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_firmness", response_model=IngestResponse)
def ingest_genes_gdr_firmness(filename: str = "genes_gdr_firmness.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_firmness", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_color", response_model=IngestResponse)
def ingest_genes_gdr_color(filename: str = "genes_gdr_color.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_color", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_acidity", response_model=IngestResponse)
def ingest_genes_gdr_acidity(filename: str = "genes_gdr_acidity.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_acidity", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_harvest", response_model=IngestResponse)
def ingest_genes_gdr_harvest(filename: str = "genes_gdr_harvest.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_harvest", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_sugar", response_model=IngestResponse)
def ingest_genes_gdr_sugar(filename: str = "genes_gdr_sugar.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_sugar", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated_firmness", response_model=IngestResponse)
def ingest_genes_gdr_curated_firmness(filename: str = "genes_gdr_curated_firmness.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated_firmness", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated_color", response_model=IngestResponse)
def ingest_genes_gdr_curated_color(filename: str = "genes_gdr_curated_color.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated_color", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated_acidity", response_model=IngestResponse)
def ingest_genes_gdr_curated_acidity(filename: str = "genes_gdr_curated_acidity.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated_acidity", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated_harvest", response_model=IngestResponse)
def ingest_genes_gdr_curated_harvest(filename: str = "genes_gdr_curated_harvest.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated_harvest", replace=True)


@app.post(f"{settings.api_prefix}/ingest/genes_gdr_curated_sugar", response_model=IngestResponse)
def ingest_genes_gdr_curated_sugar(filename: str = "genes_gdr_curated_sugar.csv") -> IngestResponse:
    return ingest_genes_impl(filename=filename, collection="genes_gdr_curated_sugar", replace=True)


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
    collection = settings.qdrant_papers_collection
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
async def upload_genes(file: UploadFile = File(...), ingest: bool = True, collection: str = "genes") -> dict:
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
    target_collection = resolve_gene_collection(collection)
    if ingest:
        result = ingest_genes_impl(filename=name, collection=collection, replace=True)
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
                    collection="genes_firmness",
                )
                print(f"[auto-ingest] genes_firmness inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_firmness failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_firmness (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_color_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_color_filename,
                    collection="genes_color",
                )
                print(f"[auto-ingest] genes_color inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_color failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_color (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_acidity_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_acidity_filename,
                    collection="genes_acidity",
                )
                print(f"[auto-ingest] genes_acidity inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_acidity failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_acidity (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_harvest_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_harvest_filename,
                    collection="genes_harvest",
                )
                print(f"[auto-ingest] genes_harvest inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_harvest failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_harvest (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_sugar_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_sugar_filename,
                    collection="genes_sugar",
                )
                print(f"[auto-ingest] genes_sugar inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_sugar failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_sugar (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_gdr_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_gdr_filename,
                    collection="genes_gdr",
                )
                print(f"[auto-ingest] genes_gdr inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_gdr failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_gdr (collection exists)", flush=True)

        if not rag.collection_exists(settings.qdrant_genes_gdr_curated_collection):
            try:
                result = ingest_genes_impl(
                    filename=settings.auto_ingest_genes_gdr_curated_filename,
                    collection="genes_gdr_curated",
                )
                print(f"[auto-ingest] genes_gdr_curated inserted={result.inserted}", flush=True)
            except Exception as exc:
                print(f"[auto-ingest] genes_gdr_curated failed: {exc}", flush=True)
        else:
            print("[auto-ingest] skip genes_gdr_curated (collection exists)", flush=True)

        for collection_name, filename, collection_key in [
            (settings.qdrant_genes_gdr_firmness_collection, settings.auto_ingest_genes_gdr_firmness_filename, "genes_gdr_firmness"),
            (settings.qdrant_genes_gdr_color_collection, settings.auto_ingest_genes_gdr_color_filename, "genes_gdr_color"),
            (settings.qdrant_genes_gdr_acidity_collection, settings.auto_ingest_genes_gdr_acidity_filename, "genes_gdr_acidity"),
            (settings.qdrant_genes_gdr_harvest_collection, settings.auto_ingest_genes_gdr_harvest_filename, "genes_gdr_harvest"),
            (settings.qdrant_genes_gdr_sugar_collection, settings.auto_ingest_genes_gdr_sugar_filename, "genes_gdr_sugar"),
            (settings.qdrant_genes_gdr_curated_firmness_collection, settings.auto_ingest_genes_gdr_curated_firmness_filename, "genes_gdr_curated_firmness"),
            (settings.qdrant_genes_gdr_curated_color_collection, settings.auto_ingest_genes_gdr_curated_color_filename, "genes_gdr_curated_color"),
            (settings.qdrant_genes_gdr_curated_acidity_collection, settings.auto_ingest_genes_gdr_curated_acidity_filename, "genes_gdr_curated_acidity"),
            (settings.qdrant_genes_gdr_curated_harvest_collection, settings.auto_ingest_genes_gdr_curated_harvest_filename, "genes_gdr_curated_harvest"),
            (settings.qdrant_genes_gdr_curated_sugar_collection, settings.auto_ingest_genes_gdr_curated_sugar_filename, "genes_gdr_curated_sugar"),
        ]:
            if not rag.collection_exists(collection_name):
                try:
                    result = ingest_genes_impl(filename=filename, collection=collection_key)
                    print(f"[auto-ingest] {collection_key} inserted={result.inserted}", flush=True)
                except Exception as exc:
                    print(f"[auto-ingest] {collection_key} failed: {exc}", flush=True)
            else:
                print(f"[auto-ingest] skip {collection_key} (collection exists)", flush=True)
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
                    collection="genes_firmness",
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
