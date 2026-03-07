from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from app.settings import Settings


GENE_HINTS = {"gene", "snp", "marker", "locus", "allele", "qtl", "genotype", "位点", "基因"}


@dataclass
class RetrievedItem:
    source_type: str
    source_id: str
    score: float
    title: str | None
    chunk_text: str
    page: int | None


class RagService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = QdrantClient(url=settings.qdrant_url)
        self.client.set_model(settings.embedding_model)
        self.llm = None
        if settings.llm_api_key:
            self.llm = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

    def add_documents(self, collection: str, items: list[dict[str, Any]]) -> int:
        if not items:
            return 0
        docs = [item["text"] for item in items]
        metadata = [item["metadata"] for item in items]
        ids = [str(uuid4()) for _ in items]
        self.client.add(collection_name=collection, documents=docs, metadata=metadata, ids=ids)
        return len(items)

    def collection_exists(self, collection: str) -> bool:
        try:
            return bool(self.client.collection_exists(collection_name=collection))
        except Exception:
            return False

    def route(self, question: str, user_route: str) -> str:
        if user_route != "auto":
            return user_route
        lowered = question.lower()
        if any(token in lowered for token in GENE_HINTS):
            return "hybrid"
        return "papers"

    def retrieve(self, question: str, route: str, top_k: int) -> list[RetrievedItem]:
        collections: list[str]
        if route == "papers":
            collections = [self.settings.qdrant_papers_collection]
        elif route == "genes":
            collections = [self.settings.qdrant_genes_collection]
        else:
            collections = [self.settings.qdrant_papers_collection, self.settings.qdrant_genes_collection]

        merged: list[RetrievedItem] = []
        per_collection_limit = max(2, top_k // max(1, len(collections)))
        for collection in collections:
            try:
                results = self.client.query(
                    collection_name=collection,
                    query_text=question,
                    limit=per_collection_limit,
                )
            except UnexpectedResponse as exc:
                # Collection may not exist yet before first ingestion.
                if "doesn't exist" in str(exc) or "Not found: Collection" in str(exc):
                    continue
                raise
            for point in results:
                payload = getattr(point, "metadata", None) or getattr(point, "payload", None) or {}
                document = (
                    getattr(point, "document", None)
                    or payload.get("document")
                    or payload.get("text")
                    or ""
                )
                merged.append(
                    RetrievedItem(
                        source_type=str(payload.get("source_type", "unknown")),
                        source_id=str(payload.get("record_id") or payload.get("filename") or getattr(point, "id", "")),
                        score=float(getattr(point, "score", 0.0)),
                        title=payload.get("title"),
                        chunk_text=document,
                        page=int(payload["page"]) if payload.get("page") else None,
                    )
                )

        merged.sort(key=lambda item: item.score, reverse=True)
        return merged[:top_k]

    def generate(self, question: str, sources: list[RetrievedItem]) -> str:
        context_lines = []
        for idx, src in enumerate(sources, start=1):
            citation = f"[{idx}] {src.source_type}"
            if src.title:
                citation += f" | {src.title}"
            if src.page:
                citation += f" | p.{src.page}"
            context_lines.append(f"{citation}\n{src.chunk_text}")
        context = "\n\n".join(context_lines)

        if self.llm is None:
            return (
                "未配置LLM API Key，当前返回检索结果摘要。\n\n"
                f"问题: {question}\n"
                "可参考以下证据片段:\n"
                + "\n".join([f"[{i+1}] {s.chunk_text[:200]}" for i, s in enumerate(sources)])
            )

        system_prompt = (
            "你是苹果育种领域的RAG助手。仅根据提供证据回答；"
            "若证据不足要明确说明。答案末尾必须给出引用编号。"
        )
        user_prompt = f"问题:\n{question}\n\n证据:\n{context}"

        completion = self.llm.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content or ""
