from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from app.settings import Settings


GENE_HINTS = {"gene", "snp", "marker", "locus", "allele", "qtl", "genotype", "位点", "基因"}
FIRMNESS_HINTS = {"firmness", "hardness", "crisp", "crispness", "texture", "硬度", "脆", "质地", "软化", "ripening"}
FIRMNESS_POSITIVE = {
    "firmness",
    "crispness",
    "ripening",
    "texture",
    "mdnac18",
    "mdnac5",
    "mdpg",
    "mdacs",
    "硬度",
    "成熟",
    "软化",
    "脆度",
    "质地",
}
FIRMNESS_NEGATIVE = {"fire blight", "scab", "anthracnose", "褐斑病", "炭疽", "病害"}
FIRMNESS_STRICT = {
    "firmness",
    "crispness",
    "hardness",
    "texture",
    "mdnac18",
    "mdnac5",
    "mdpg",
    "mdacs1",
    "mderf3",
    "mderf118",
    "硬度",
    "脆度",
    "质地",
    "软化",
}


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

    def is_firmness_query(self, question: str) -> bool:
        q = question.lower()
        return any(k in q for k in FIRMNESS_HINTS)

    def retrieve(self, question: str, route: str, top_k: int) -> list[RetrievedItem]:
        ask_firmness = self.is_firmness_query(question)
        collections: list[str]
        if route == "papers":
            collections = [self.settings.qdrant_papers_collection]
        elif route == "genes":
            if ask_firmness:
                collections = [
                    self.settings.qdrant_genes_firmness_collection,
                    self.settings.qdrant_genes_collection,
                ]
            else:
                collections = [self.settings.qdrant_genes_collection]
        else:
            if ask_firmness:
                collections = [
                    self.settings.qdrant_papers_collection,
                    self.settings.qdrant_genes_firmness_collection,
                    self.settings.qdrant_genes_collection,
                ]
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

        return self.rerank(question=question, items=merged, top_k=top_k)

    def rerank(self, question: str, items: list[RetrievedItem], top_k: int) -> list[RetrievedItem]:
        if not items:
            return []

        q = question.lower()
        ask_firmness = any(k in q for k in FIRMNESS_HINTS)

        def hit_counts(text: str) -> tuple[int, int]:
            pos_hits = sum(1 for k in FIRMNESS_POSITIVE if k in text)
            neg_hits = sum(1 for k in FIRMNESS_NEGATIVE if k in text)
            return pos_hits, neg_hits

        def adjusted_score(item: RetrievedItem) -> float:
            score = item.score
            text = f"{item.title or ''} {item.chunk_text}".lower()

            # De-prioritize noisy generated columns from flattened tables.
            if text.count("col_") >= 10:
                score -= 0.25

            if ask_firmness:
                pos_hits, neg_hits = hit_counts(text)
                score += 0.06 * pos_hits
                score -= 0.12 * neg_hits

                # Extra boost for gene records on firmness-like query.
                if item.source_type == "gene":
                    score += 0.08

            return score

        reranked = sorted(items, key=adjusted_score, reverse=True)
        if not ask_firmness:
            return reranked[:top_k]

        # Hard filter for firmness queries: avoid returning disease-only evidence.
        scored = []
        for it in reranked:
            t = f"{it.title or ''} {it.chunk_text}".lower()
            pos_hits, neg_hits = hit_counts(t)
            strict_hits = sum(1 for k in FIRMNESS_STRICT if k in t)
            scored.append((it, pos_hits, neg_hits, strict_hits))

        # Prefer strict-match evidence and reject disease-focused chunks.
        strong = [it for it, pos, neg, strict in scored if strict > 0 and neg == 0]
        weak = [it for it, pos, neg, strict in scored if strict > 0 and neg <= pos]
        if strong:
            return strong[:top_k]
        if weak:
            return weak[:top_k]

        # No evidence matching firmness intent: return empty and let API report insufficient evidence.
        return []

    def generate(self, question: str, sources: list[RetrievedItem]) -> str:
        context_lines = []
        for idx, src in enumerate(sources, start=1):
            level = "B"
            low = (src.chunk_text or "").lower()
            if any(k in low for k in ["qtl region", "deg", "gwas", "association", "p-value", "p value"]):
                level = "A"
            citation = f"[{idx}] {src.source_type}"
            if src.title:
                citation += f" | {src.title}"
            if src.page:
                citation += f" | p.{src.page}"
            context_lines.append(f"{citation} | evidence_level={level}\n{src.chunk_text}")
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
            "若证据不足要明确说明。答案必须分两段：Level A(直接证据) 与 Level B(间接证据)。"
            "答案末尾必须给出引用编号。"
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
