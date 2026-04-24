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
PAPER_QUERY_HINTS = {"论文", "文章", "paper", "article", "study"}
TITLE_MATCH_STOPWORDS = {
    "the", "and", "of", "in", "on", "for", "with", "from", "into", "using",
    "analysis", "study", "paper", "article", "reveals", "reveal", "published",
    "nature", "genetics", "authors", "author", "how", "what", "which",
    "作者", "论文", "文章", "发表", "问题", "这篇", "中", "如何", "什么",
}


def _normalize_match_text(text: str) -> str:
    cleaned = re.sub(r"\.pdf$", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"^\d+[_\-\s]+", "", cleaned)
    cleaned = re.sub(r"_\d{3}_", " ", cleaned)
    cleaned = cleaned.replace("_", " ")
    cleaned = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", cleaned.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _match_tokens(text: str) -> list[str]:
    return [
        token
        for token in _normalize_match_text(text).split()
        if len(token) > 2 and token not in TITLE_MATCH_STOPWORDS
    ]


def _looks_like_paper_query(question: str) -> bool:
    lowered = question.lower()
    english_tokens = re.findall(r"[A-Za-z][A-Za-z\-]+", question)
    return any(hint in lowered for hint in PAPER_QUERY_HINTS) and len(english_tokens) >= 5


def _title_match_strength(question: str, title: str | None) -> float:
    if not title:
        return 0.0
    q_norm = _normalize_match_text(question)
    t_norm = _normalize_match_text(title)
    if not q_norm or not t_norm:
        return 0.0
    if t_norm in q_norm:
        return 1.0

    q_tokens = set(_match_tokens(question))
    t_tokens = set(_match_tokens(title))
    if not q_tokens or not t_tokens:
        return 0.0

    overlap = len(q_tokens & t_tokens)
    if overlap == 0:
        return 0.0
    return overlap / max(1, len(t_tokens))


def _paper_query_terms(question: str) -> list[str]:
    lowered = question.lower()
    terms: list[str] = []
    candidates = [
        ("PAV", ["presence-absence variation", "pav"]),
        ("pan-genome graph", ["pan-genome graph"]),
        ("structural variations", ["structural variation", "structural variations", "sv"]),
        ("selective sweep", ["selective sweep"]),
        ("MdMYB5", ["mdmyb5"]),
        ("domestication", ["domestication", "驯化"]),
    ]
    for label, needles in candidates:
        if any(needle in lowered for needle in needles):
            terms.append(label)
    return terms


def _paper_focus_summary(sources: list["RetrievedItem"]) -> list[str]:
    text = " ".join(src.chunk_text for src in sources).lower()
    bullets: list[str] = []
    if "pan-genome graph" in text or "genome graph" in text:
        bullets.append("作者构建了 pan-Malus genome graph，用图泛基因组而不是单一线性参考来表征苹果属的遗传多样性。")
    if "117,246 svs" in text or "117246 svs" in text:
        bullets.append("基于图泛基因组分析，研究识别出了 117,246 个结构变异（SVs），并指出随着纳入更多基因组，SV 总数逐渐趋于平台，说明大多数结构变异已被捕获。")
    if "selective sweep" in text:
        bullets.append("论文强调这种图泛基因组框架相比单一参考基因组，更适合捕获与重要农艺性状相关的 selective sweeps。")
    if "mdmyb5" in text:
        bullets.append("关于 MdMYB5，当前命中的片段支持这样一个解释：驯化过程中可能选择了较低的 MdMYB5 表达，从而影响与果实风味相关的次生代谢物。")
    if "hybridization" in text or "polyploidy" in text or "wgd" in text:
        bullets.append("论文还把苹果属的演化多样性与杂交、多倍化以及全基因组复制相关的基因组事件联系起来。")
    return bullets[:4]


@dataclass
class RetrievedItem:
    source_type: str
    source_id: str
    score: float
    title: str | None
    chunk_text: str
    page: int | None
    trait: str | None = None
    reference_genome: str | None = None
    coordinate_note: str | None = None


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
        if _looks_like_paper_query(question):
            return "papers"
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
        paper_query = _looks_like_paper_query(question)
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
                limit = max(top_k * 3, 10) if paper_query else top_k
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
                        reference_genome=(
                            str(payload.get("reference_genome"))
                            if payload.get("reference_genome")
                            else None
                        ),
                        coordinate_note=(
                            str(payload.get("coordinate_note"))
                            if payload.get("coordinate_note")
                            else None
                        ),
                    )
                )

        deduped: list[RetrievedItem] = []
        seen_keys: set[tuple[str, str, str | None]] = set()
        for item in merged:
            if item.source_type == "gene" and item.title:
                key = (item.source_type, item.title, item.trait)
            elif paper_query and item.source_type == "paper" and _title_match_strength(question, item.title) > 0.45:
                key = (item.source_type, item.source_id, str(item.page))
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
        paper_query = _looks_like_paper_query(question)
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
            title_match = _title_match_strength(question, item.title)

            # De-prioritize noisy generated columns from flattened tables.
            if text.count("col_") >= 10:
                score -= 0.25

            if paper_query:
                if item.source_type == "paper":
                    score += 0.9 * title_match
                    if title_match > 0.45:
                        score += 0.18
                else:
                    score -= 0.28

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
        if paper_query:
            matched_papers = [
                item for item in reranked
                if item.source_type == "paper" and _title_match_strength(question, item.title) > 0.45
            ]
            if matched_papers:
                return matched_papers[:top_k]
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
        paper_query = _looks_like_paper_query(question)
        matched_paper_title = None
        if paper_query and sources:
            best_paper = max(
                (src for src in sources if src.source_type == "paper"),
                key=lambda src: _title_match_strength(question, src.title),
                default=None,
            )
            if best_paper and _title_match_strength(question, best_paper.title) > 0.45:
                matched_paper_title = best_paper.title
        levels_list: list[str] = []
        for idx, src in enumerate(sources, start=1):
            level = "B"
            low = (src.chunk_text or "").lower()
            if any(k in low for k in ["qtl region", "deg", "gwas", "association", "p-value", "p value"]):
                level = "A"
            levels_list.append(level)
            label = src.title or src.source_id or src.source_type
            if src.source_type == "gene" and label not in seen_gene_labels:
                seen_gene_labels.append(label)
            citation = f"[{idx}] {src.source_type}"
            if src.title:
                citation += f" | {src.title}"
            if src.page:
                citation += f" | p.{src.page}"
            if src.reference_genome:
                citation += f" | ref={src.reference_genome}"
            snippet = src.chunk_text[:220].replace("\n", " ").strip()
            line = f"{citation}\n{snippet}"
            context_lines.append(line)
            coord_note = ""
            if src.coordinate_note and (
                src.reference_genome == "unknown" or "not confirmed" in src.coordinate_note.lower()
            ):
                coord_note = f" 坐标提示: {src.coordinate_note}"
            summary_line = f"- {label}: {snippet}{coord_note} [{idx}]"
            if level == "A":
                level_a_lines.append(summary_line)
            else:
                level_b_lines.append(summary_line)
        context = "\n\n".join(context_lines)
        if levels_list:
            level_index = "Evidence level index: " + ", ".join(
                f"[{i+1}]={lvl}" for i, lvl in enumerate(levels_list)
            )
            context = context + "\n\n" + level_index
        has_uncertain_coordinates = any(
            src.coordinate_note and (
                src.reference_genome == "unknown" or "not confirmed" in src.coordinate_note.lower()
            )
            for src in sources
        )
        paper_only = bool(sources) and all(src.source_type == "paper" for src in sources)
        paper_focus = bool(matched_paper_title) and paper_only
        paper_context = " ".join(src.chunk_text for src in sources).lower()
        asked_terms = _paper_query_terms(question)
        supported_terms = [term for term in asked_terms if term.lower() in paper_context]
        unsupported_terms = [term for term in asked_terms if term.lower() not in paper_context]

        llm = self._make_llm_client(
            api_key=llm_api_key if llm_api_key is not None else self.settings.llm_api_key,
            base_url=llm_base_url if llm_base_url is not None else self.settings.llm_base_url,
        )
        if llm is None:
            if paper_focus:
                paper_points = _paper_focus_summary(sources)
                if not paper_points:
                    paper_points = []
                    for src in sources[:3]:
                        snippet = src.chunk_text[:180].replace("\n", " ").strip()
                        page_hint = f"（p.{src.page}）" if src.page else ""
                        paper_points.append(f"- {snippet}{page_hint}")
                coverage_line = (
                    f"当前命中的片段直接支持这些概念：{', '.join(supported_terms)}。"
                    if supported_terms
                    else "当前命中的片段主要支持这篇论文的总体研究框架，而不是你问题中的全部细节术语。"
                )
                gap_line = (
                    f"但当前片段里没有直接命中：{', '.join(unsupported_terms)}。"
                    if unsupported_terms
                    else ""
                )
                return (
                    "未配置LLM API Key，当前返回论文证据摘要。\n\n"
                    + f"已命中目标论文: {matched_paper_title}\n\n"
                    + "这篇论文在当前证据中主要说明：\n"
                    + "\n".join(paper_points)
                    + "\n\n"
                    + coverage_line
                    + ("\n" + gap_line if gap_line else "")
                    + "\n\n结论：论文已经找到。当前更可靠的说法是，这篇文章重点在图泛基因组、结构变异、selective sweep 和演化/驯化信号；如果你继续追问 PAV 这种更细的术语，需要命中论文里对应的原始段落或补充材料。"
                    + "\n\n引用: "
                    + "".join(f"[{i}]" for i in range(1, min(len(sources), 6) + 1))
                )
            gene_summary = "、".join(seen_gene_labels[:6]) if seen_gene_labels else "未从当前证据中稳定识别出明确基因名"
            if not level_a_lines:
                level_a_lines.append("- 当前返回结果中缺少明确的 GWAS/QTL/p-value 直接证据片段。")
            if not level_b_lines:
                level_b_lines.append("- 当前返回结果中缺少功能或表达层面的支持性证据片段。")
            return (
                "未配置LLM API Key，当前返回检索结果摘要。\n\n"
                + f"问题: {question}\n"
                + (f"已命中目标论文: {matched_paper_title}\n" if matched_paper_title else "")
                + f"候选关键基因/位点: {gene_summary}\n\n"
                + "【Level A 直接证据】\n"
                + "\n".join(level_a_lines[:3])
                + "\n\n【Level B 间接证据】\n"
                + "\n".join(level_b_lines[:3])
                + (
                    "\n\n【坐标参考系提示】\n"
                    "部分 QTL/GWAS 记录缺少明确参考基因组；chr/pos 只能作为原始来源坐标展示，不能直接跨研究合并或比较。"
                    if has_uncertain_coordinates
                    else ""
                )
                + "\n\n引用: "
                + "".join(f"[{i}]" for i in range(1, min(len(sources), 6) + 1))
            )

        if paper_focus:
            system_prompt = (
                "你是一个科研论文问答助手。"
                "当前任务是解读一篇已经命中的具体论文，而不是做基因/QTL模板化回答。"
                "回答规则：\n"
                "1. 先明确说明论文已经命中。\n"
                "2. 用自然中文概括当前证据真正支持的结论，不要使用'Level A/Level B'模板。\n"
                "3. 如果用户问题中的某个术语没有在当前证据片段中直接出现，要明确说'论文已找到，但当前片段未直接支持该术语'。\n"
                "4. 不要提坐标系、chr/pos、QTL、GWAS，除非证据里真的出现这些内容。\n"
                "5. 优先回答论文实际讲了什么，再说明当前证据还缺什么。\n"
                "6. 结尾保留引用编号。"
            )
            user_prompt = (
                f"问题:\n{question}\n\n"
                + f"已命中目标论文：{matched_paper_title}\n"
                + (
                    f"当前片段直接支持的术语：{', '.join(supported_terms)}\n"
                    if supported_terms else ""
                )
                + (
                    f"当前片段未直接支持的术语：{', '.join(unsupported_terms)}\n"
                    if unsupported_terms else ""
                )
                + f"\n证据:\n{context}"
            )
        else:
            system_prompt = (
                "你是苹果（Malus domestica）育种领域的资深科研专家，撰写风格类似高水平综述论文："
                "语言流畅、逻辑连贯、表述自然，不使用标题块或模板化格式，而是以叙述性散文整合遗传学与分子生物学证据。"
                "你熟悉以下性状相关的基因和通路：\n"
                "- 果肉硬度/质地：MdNAC18、MdNAC5、MdPG（多聚半乳糖醛酸酶）、MdEXP（扩展素）、MdACS/MdACO（乙烯合成）等\n"
                "- 采收期/贮藏性：MdNAC83（调控细胞壁与乙烯代谢相关基因）、MdBPM2与MdRGLG3（通过泛素化调节MdNAC83稳定性）、"
                "MdHDT3（组蛋白去乙酰化抑制MdACS1、延缓成熟与软化）等\n"
                "- 果皮颜色/花青素：MdMYB1/MdMYB10（主调控因子）、MdDFR、MdANS、MdUFGT（花青素生物合成结构基因）、"
                "MdHY5、MdCOP1（光信号调控着色）、MdWRKY40（光信号下游调控花青素积累）等\n"
                "- 果实酸度：Ma1/MdALMT9（液泡苹果酸转运体）、MdVHP1（液泡焦磷酸酶）、MdPEPC（苹果酸合成）、MdMDH（苹果酸脱氢酶）等\n"
                "- 含糖量：MdSUT1/MdSUT4（蔗糖转运体）、MdINV（转化酶）、MdSPS（蔗糖磷酸合酶）、"
                "MdSWEET9b（ABA信号通路下游蔗糖转运体、促进糖积累）、MdWRKY9（激活MdSWEET9b启动子）、"
                "MdCIbHLH1（协调碳水化合物合成与分配，调控MdFBP/MdPEPCK）、ABA信号组分MdbZIP23/MdbZIP46等\n"
                "回答规则：\n"
                '1. 仅根据提供的证据作答；若证据不足，明确说明"当前证据不足以支持该结论"。\n'
                '2. 用流畅的科学论文综述风格写作，不要使用【Level A】【Level B】等标题块。'
                '将遗传关联证据（GWAS/QTL/p值）与功能实验证据的区分自然嵌入叙述之中：'
                '——对于直接遗传证据，使用"通过GWAS直接证实……"、"QTL分析表明……"、"遗传关联研究（直接证据）显示……"等表达；'
                '——对于功能或表达层面证据，使用"转录组分析进一步支持……"、"功能实验表明……"、"间接证据来自……"等表达。'
                '答案中必须至少出现一处含"直接证据"或等价短语的句子，以及一处含"间接证据"或等价短语的句子。\n'
                '3. 行文中随时插入内联引用，格式为[1]、[2]等，紧跟在支持该论点的句子或短语之后。'
                "答案全文中至少分散出现2处内联引用。末尾附一个简短参考文献列表（每条一行，格式：[编号] 来源描述），不超过6条。\n"
                "4. 基因名称使用标准命名（如MdMYB1、MdALMT9）；参考末尾的Evidence level index，"
                "对A级条目在句中说明遗传关联强度或染色体位置，对B级条目说明功能实验背景。\n"
                '5. 若证据中的chr/pos缺少明确参考基因组，在行文中自然提及"坐标来自原始文献参考系，跨研究比较需谨慎"。\n'
                '6. 如果用户问题中的术语没有在证据里直接出现，明确区分"论文已命中"与"该术语在当前证据片段中未直接出现"，并说明最接近的概念。\n'
                "7. 中文问题用中文回答；英文问题用英文回答。"
            )
            user_prompt = (
                f"问题:\n{question}\n\n"
                + (f"目标论文命中情况:\n已命中目标论文：{matched_paper_title}\n\n" if matched_paper_title else "")
                + f"证据:\n{context}"
            )

        completion = llm.chat.completions.create(
            model=(llm_model or self.settings.llm_model).strip(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.35,
        )
        return completion.choices[0].message.content or ""
