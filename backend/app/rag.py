from __future__ import annotations

import re
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
    "firmness", "crispness", "ripening", "texture",
    "mdnac18", "mdnac5", "mdpg", "mdacs",
    "硬度", "成熟", "软化", "脆度", "质地",
}
FIRMNESS_NEGATIVE = {"fire blight", "scab", "anthracnose", "褐斑病", "炭疽", "病害"}
FIRMNESS_STRICT = {
    "firmness", "crispness", "hardness", "texture",
    "mdnac18", "mdnac5", "mdpg", "mdacs1", "mderf3", "mderf118",
    "硬度", "脆度", "质地", "软化",
}

COLOR_HINTS = {
    "color", "colour", "anthocyanin", "pigment", "red", "blush", "skin color",
    "颜色", "花青素", "着色", "红色", "果皮颜色", "色泽",
}
COLOR_POSITIVE = {
    "anthocyanin", "color", "colour", "red", "blush", "pigment", "skin",
    "mdmyb1", "mdmyb10", "mdmyb9", "mddFR", "mdans", "mdufgt", "mdchs",
    "mdhy5", "mdcop1", "mdbhbh3", "mdbbx22",
    "花青素", "颜色", "着色", "果皮", "色素",
}
COLOR_NEGATIVE = {"fire blight", "scab", "disease", "病害", "炭疽"}
COLOR_STRICT = {
    "anthocyanin", "color", "colour", "red skin", "blush",
    "mdmyb1", "mdmyb10", "mdmyb9", "mddfr", "mdans", "mdufgt",
    "花青素", "着色", "果皮颜色",
}

ACIDITY_HINTS = {
    "acid", "acidity", "malic", "malate", "citric", "titratable",
    "酸度", "苹果酸", "有机酸", "可滴定酸", "酸含量", "ph",
}
ACIDITY_POSITIVE = {
    "malic acid", "malate", "acidity", "acid", "titratable", "citric",
    "ma1", "mdalmt", "mdvhp1", "mdvha", "mdpepc", "mdmdh", "mdsaur37",
    "苹果酸", "酸度", "有机酸", "可滴定酸",
}
ACIDITY_NEGATIVE = {"fire blight", "scab", "disease", "病害"}
ACIDITY_STRICT = {
    "malic acid", "malate", "titratable acidity", "acidity",
    "ma1", "mdalmt9", "mdalmt11", "mdvhp1", "mdpepc",
    "苹果酸", "可滴定酸", "酸度",
}

HARVEST_HINTS = {
    "harvest", "maturity", "ripening date", "maturity date", "preharvest", "drop",
    "采收", "采收期", "成熟期", "成熟时间", "落果", "成熟日期",
}
HARVEST_POSITIVE = {
    "harvest", "maturity", "ripening", "harvest date", "maturity date",
    "mdnac18", "mdacs1", "mdaco1", "mdein3",
    "采收", "成熟期", "成熟时间", "落果", "乙烯",
}
HARVEST_NEGATIVE = {"fire blight", "scab", "disease", "病害"}
HARVEST_STRICT = {
    "harvest date", "maturity date", "ripening date",
    "mdnac18", "mdacs1", "mdaco1", "mdein3",
    "采收期", "成熟期", "成熟时间",
}

SUGAR_HINTS = {
    "sugar", "sucrose", "fructose", "glucose", "soluble solids", "brix", "sweetness",
    "糖", "蔗糖", "果糖", "葡萄糖", "可溶性固形物", "甜度",
}
SUGAR_POSITIVE = {
    "sugar", "sucrose", "fructose", "glucose", "soluble solids", "sweetness",
    "mdsut", "mdinv", "mdsps", "mdhxk1",
    "糖", "蔗糖", "果糖", "葡萄糖", "甜度", "可溶性固形物",
}
SUGAR_NEGATIVE = {"fire blight", "scab", "disease", "病害"}
SUGAR_STRICT = {
    "sucrose", "soluble solids", "sweetness",
    "mdsut1", "mdsut4", "mdinv", "mdsps", "mdhxk1",
    "蔗糖", "甜度", "可溶性固形物",
}

QUESTION_GENE_HINTS = {
    "which gene", "what gene", "which genes", "what genes",
    "调控基因", "哪些基因", "哪个基因", "关键基因", "候选基因", "主要基因",
    "调控因子", "转录因子", "机制", "通路",
}
GENE_NAME_RE = re.compile(r"\b(?:md[a-z0-9+\-]+|ma1|ma\d+)\b", re.IGNORECASE)
GENERIC_LABEL_TOKENS = {
    "brix",
    "acidity",
    "malacid",
    "pickday",
    "drop",
    "skin color",
    "skin overcolour",
    "yellowcolor",
    "solublesolidscontent",
}


@dataclass
class RetrievedItem:
    source_type: str
    source_id: str
    score: float
    title: str | None
    chunk_text: str
    page: int | None
    trait: str | None = None


class RagService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = QdrantClient(url=settings.qdrant_url)
        self.client.set_model(settings.embedding_model)
        self.llm = self._make_llm_client(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    def _make_llm_client(self, api_key: str | None, base_url: str | None) -> OpenAI | None:
        if not api_key or not api_key.strip():
            return None
        return OpenAI(api_key=api_key.strip(), base_url=(base_url or self.settings.llm_base_url).strip())

    def add_documents(self, collection: str, items: list[dict[str, Any]]) -> int:
        if not items:
            return 0
        docs = [item["text"] for item in items]
        metadata = [item["metadata"] for item in items]
        ids = [str(uuid4()) for _ in items]
        self.client.add(collection_name=collection, documents=docs, metadata=metadata, ids=ids)
        return len(items)

    def replace_documents(self, collection: str, items: list[dict[str, Any]]) -> int:
        if self.collection_exists(collection):
            self.client.delete_collection(collection_name=collection)
        return self.add_documents(collection, items)

    def collection_exists(self, collection: str) -> bool:
        try:
            return bool(self.client.collection_exists(collection_name=collection))
        except Exception:
            return False

    def route(self, question: str, user_route: str) -> str:
        if user_route != "auto":
            return user_route
        lowered = question.lower()
        trait = self.detect_trait(question)
        if trait:
            return "hybrid"
        if any(token in lowered for token in GENE_HINTS | QUESTION_GENE_HINTS):
            return "hybrid"
        return "papers"

    def detect_trait(self, question: str) -> str | None:
        """Return the dominant trait of the query, or None if ambiguous/unknown."""
        q = question.lower()
        scores = {
            "firmness": sum(1 for k in FIRMNESS_HINTS if k in q),
            "color": sum(1 for k in COLOR_HINTS if k in q),
            "acidity": sum(1 for k in ACIDITY_HINTS if k in q),
            "harvest": sum(1 for k in HARVEST_HINTS if k in q),
            "sugar": sum(1 for k in SUGAR_HINTS if k in q),
        }
        best = max(scores, key=lambda t: scores[t])
        return best if scores[best] > 0 else None

    def is_firmness_query(self, question: str) -> bool:
        q = question.lower()
        return any(k in q for k in FIRMNESS_HINTS)

    def _trait_collections(self, trait: str | None) -> list[str]:
        """Return trait-specific curated + GDR collections to prioritize."""
        gdr = self.settings.qdrant_genes_gdr_collection
        gdr_curated = self.settings.qdrant_genes_gdr_curated_collection
        if trait == "firmness":
            return [
                self.settings.qdrant_genes_firmness_collection,
                self.settings.qdrant_genes_gdr_curated_firmness_collection,
                gdr_curated,
                self.settings.qdrant_genes_gdr_firmness_collection,
                gdr,
            ]
        if trait == "color":
            return [
                self.settings.qdrant_genes_color_collection,
                self.settings.qdrant_genes_gdr_curated_color_collection,
                gdr_curated,
                self.settings.qdrant_genes_gdr_color_collection,
                gdr,
            ]
        if trait == "acidity":
            return [
                self.settings.qdrant_genes_acidity_collection,
                self.settings.qdrant_genes_gdr_curated_acidity_collection,
                gdr_curated,
                self.settings.qdrant_genes_gdr_acidity_collection,
                gdr,
            ]
        if trait == "harvest":
            return [
                self.settings.qdrant_genes_harvest_collection,
                self.settings.qdrant_genes_gdr_curated_harvest_collection,
                gdr_curated,
                self.settings.qdrant_genes_gdr_harvest_collection,
                gdr,
            ]
        if trait == "sugar":
            return [
                self.settings.qdrant_genes_sugar_collection,
                self.settings.qdrant_genes_gdr_curated_sugar_collection,
                gdr_curated,
                self.settings.qdrant_genes_gdr_sugar_collection,
                gdr,
            ]
        return [gdr_curated, gdr]

    def retrieve(self, question: str, route: str, top_k: int) -> list[RetrievedItem]:
        trait = self.detect_trait(question)
        trait_cols = self._trait_collections(trait)
        collections: list[str]
        if route == "papers":
            collections = [self.settings.qdrant_papers_collection]
        elif route == "genes":
            collections = trait_cols + [self.settings.qdrant_genes_collection]
        else:
            collections = (
                trait_cols
                + [self.settings.qdrant_genes_collection, self.settings.qdrant_papers_collection]
            )

        merged: list[RetrievedItem] = []
        for collection in collections:
            if route == "papers":
                limit = top_k
            elif route == "genes":
                limit = max(top_k, 4) if collection in trait_cols else max(3, top_k // 2)
            else:
                if collection in trait_cols:
                    limit = max(top_k, 5)
                elif collection == self.settings.qdrant_genes_collection:
                    limit = max(4, top_k // 2 + 1)
                else:
                    limit = max(3, top_k // 2)
            try:
                results = self.client.query(
                    collection_name=collection,
                    query_text=question,
                    limit=limit,
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
                        title=(
                            payload.get("title")
                            or payload.get("display_title")
                            or payload.get("candidate_gene")
                            or payload.get("gene")
                            or payload.get("filename")
                        ),
                        chunk_text=document,
                        page=int(payload["page"]) if payload.get("page") else None,
                        trait=str(payload.get("trait")) if payload.get("trait") else None,
                    )
                )

        deduped: list[RetrievedItem] = []
        seen_keys: set[tuple[str, str, str | None]] = set()
        for item in merged:
            if item.source_type == "gene" and item.title:
                key = (item.source_type, item.title, item.trait)
            else:
                key = (item.source_type, item.source_id, item.title)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            deduped.append(item)

        return self.rerank(question=question, items=deduped, top_k=top_k)

    def rerank(self, question: str, items: list[RetrievedItem], top_k: int) -> list[RetrievedItem]:
        if not items:
            return []

        trait = self.detect_trait(question)
        q = question.lower()
        gene_mentions = {m.group(0).lower() for m in GENE_NAME_RE.finditer(q)}

        # Select keyword sets based on detected trait
        if trait == "firmness":
            pos_kw, neg_kw, strict_kw = FIRMNESS_POSITIVE, FIRMNESS_NEGATIVE, FIRMNESS_STRICT
        elif trait == "color":
            pos_kw, neg_kw, strict_kw = COLOR_POSITIVE, COLOR_NEGATIVE, COLOR_STRICT
        elif trait == "acidity":
            pos_kw, neg_kw, strict_kw = ACIDITY_POSITIVE, ACIDITY_NEGATIVE, ACIDITY_STRICT
        elif trait == "harvest":
            pos_kw, neg_kw, strict_kw = HARVEST_POSITIVE, HARVEST_NEGATIVE, HARVEST_STRICT
        elif trait == "sugar":
            pos_kw, neg_kw, strict_kw = SUGAR_POSITIVE, SUGAR_NEGATIVE, SUGAR_STRICT
        else:
            pos_kw, neg_kw, strict_kw = set(), set(), set()

        def hit_counts(text: str) -> tuple[int, int]:
            pos_hits = sum(1 for k in pos_kw if k in text)
            neg_hits = sum(1 for k in neg_kw if k in text)
            return pos_hits, neg_hits

        def adjusted_score(item: RetrievedItem) -> float:
            score = item.score
            text = f"{item.title or ''} {item.chunk_text}".lower()
            title = (item.title or "").lower().strip()

            # De-prioritize noisy generated columns from flattened tables.
            if text.count("col_") >= 10:
                score -= 0.25

            if trait:
                pos_hits, neg_hits = hit_counts(text)
                score += 0.06 * pos_hits
                score -= 0.12 * neg_hits
                if item.source_type == "gene" and item.trait and item.trait.lower() != trait:
                    score -= 0.35
                # Extra boost for gene records on trait-specific queries
                if item.source_type == "gene":
                    score += 0.16
                else:
                    score -= 0.03
                # Prefer standard gene identifiers over generic trait labels such as Brix/PickDay.
                if GENE_NAME_RE.search(text):
                    score += 0.14
                if title and any(tok in title for tok in GENERIC_LABEL_TOKENS) and not GENE_NAME_RE.search(title):
                    score -= 0.18

            if gene_mentions and any(gene in text for gene in gene_mentions):
                score += 0.22

            return score

        reranked = sorted(items, key=adjusted_score, reverse=True)
        if not trait:
            return reranked[:top_k]

        # Hard filter: prefer strict-match evidence, reject disease/off-topic chunks.
        scored = []
        for it in reranked:
            t = f"{it.title or ''} {it.chunk_text}".lower()
            pos_hits, neg_hits = hit_counts(t)
            strict_hits = sum(1 for k in strict_kw if k in t)
            scored.append((it, pos_hits, neg_hits, strict_hits))

        strong = [it for it, pos, neg, strict in scored if strict > 0 and neg == 0]
        weak = [it for it, pos, neg, strict in scored if strict > 0 and neg <= pos]
        if strong:
            return strong[:top_k]
        if weak:
            return weak[:top_k]

        # Fallback: return top results without strict filtering
        return reranked[:top_k]

    def generate(
        self,
        question: str,
        sources: list[RetrievedItem],
        llm_api_key: str | None = None,
        llm_base_url: str | None = None,
        llm_model: str | None = None,
    ) -> str:
        context_lines = []
        level_a_lines: list[str] = []
        level_b_lines: list[str] = []
        seen_gene_labels: list[str] = []
        for idx, src in enumerate(sources, start=1):
            level = "B"
            low = (src.chunk_text or "").lower()
            if any(k in low for k in ["qtl region", "deg", "gwas", "association", "p-value", "p value"]):
                level = "A"
            label = src.title or src.source_id or src.source_type
            if src.source_type == "gene" and label not in seen_gene_labels:
                seen_gene_labels.append(label)
            citation = f"[{idx}] {src.source_type}"
            if src.title:
                citation += f" | {src.title}"
            if src.page:
                citation += f" | p.{src.page}"
            snippet = src.chunk_text[:220].replace("\n", " ").strip()
            line = f"{citation} | evidence_level={level}\n{snippet}"
            context_lines.append(line)
            summary_line = f"- {label}: {snippet} [{idx}]"
            if level == "A":
                level_a_lines.append(summary_line)
            else:
                level_b_lines.append(summary_line)
        context = "\n\n".join(context_lines)

        llm = self._make_llm_client(
            api_key=llm_api_key if llm_api_key is not None else self.settings.llm_api_key,
            base_url=llm_base_url if llm_base_url is not None else self.settings.llm_base_url,
        )
        if llm is None:
            gene_summary = "、".join(seen_gene_labels[:6]) if seen_gene_labels else "未从当前证据中稳定识别出明确基因名"
            if not level_a_lines:
                level_a_lines.append("- 当前返回结果中缺少明确的 GWAS/QTL/p-value 直接证据片段。")
            if not level_b_lines:
                level_b_lines.append("- 当前返回结果中缺少功能或表达层面的支持性证据片段。")
            return (
                "未配置LLM API Key，当前返回检索结果摘要。\n\n"
                f"问题: {question}\n"
                f"候选关键基因/位点: {gene_summary}\n\n"
                "【Level A 直接证据】\n"
                + "\n".join(level_a_lines[:3])
                + "\n\n【Level B 间接证据】\n"
                + "\n".join(level_b_lines[:3])
                + "\n\n引用: "
                + "".join(f"[{i}]" for i in range(1, min(len(sources), 6) + 1))
            )

        system_prompt = (
            "你是苹果（Malus domestica）育种领域的RAG专家助手，专注于果实品质性状的遗传与分子机制研究。"
            "你精通以下性状相关的基因和通路：\n"
            "- 果肉硬度/质地：MdNAC18、MdNAC5、MdPG（多聚半乳糖醛酸酶）、MdEXP（扩展素）、MdACS/MdACO（乙烯合成）等\n"
            "- 果皮颜色/花青素：MdMYB1/MdMYB10（主调控因子）、MdDFR、MdANS、MdUFGT（花青素生物合成结构基因）、MdHY5、MdCOP1（光信号）等\n"
            "- 果实酸度：Ma1/MdALMT9（液泡苹果酸转运体）、MdVHP1（液泡焦磷酸酶）、MdPEPC（苹果酸合成）、MdMDH（苹果酸脱氢酶）等\n"
            "- 含糖量：MdSUT（蔗糖转运体）、MdINV（转化酶）等\n"
            "回答规则：\n"
            "1. 仅根据提供的证据回答；若证据不足，明确说明'证据不足'\n"
            "2. 答案分两段：【Level A 直接证据】（GWAS/QTL/p值等遗传关联证据）和【Level B 间接证据】（表达分析/功能实验等支持性证据）\n"
            "3. 基因名称使用标准命名（如MdMYB1、MdALMT9），说明染色体位置和性状关联强度\n"
            "4. 答案末尾必须列出引用编号（如[1][2][3]）\n"
            "5. 如有中文问题，用中文回答；英文问题用英文回答"
        )
        user_prompt = f"问题:\n{question}\n\n证据:\n{context}"

        completion = llm.chat.completions.create(
            model=(llm_model or self.settings.llm_model).strip(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content or ""
