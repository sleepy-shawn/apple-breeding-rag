"""
自动检索苹果育种相关论文。

默认输出到统一 pipeline workspace，可通过 --config 覆盖。
"""

from __future__ import annotations

import argparse
import json
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout

SLEEP_SEC = 0.35
REQUEST_TIMEOUT = 20
PDF_TIMEOUT = 45
MAX_RETRIES = 3
USER_AGENT = "apple-breeding-rag-fetcher/1.0 (research automation)"

GENE_KEYWORDS = [
    "qtl",
    "gene",
    "locus",
    "marker",
    "myb",
    "nac",
    "erf",
    "gwas",
    "snp",
    "allele",
    "transcription factor",
    "candidate gene",
    "genetic map",
    "linkage map",
]

BREEDING_KEYWORDS = [
    "breeding",
    "qtl",
    "gwas",
    "marker",
    "locus",
    "candidate gene",
    "linkage map",
    "genetic map",
    "association mapping",
]

NEGATIVE_KEYWORDS = [
    "postharvest",
    "storage",
    "fresh-cut",
    "juice",
    "processing",
    "edible coating",
    "preservation",
]


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    timeout: int,
    allow_redirects: bool = True,
    **kwargs: Any,
) -> requests.Response | None:
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.request(
                method,
                url,
                timeout=timeout,
                allow_redirects=allow_redirects,
                **kwargs,
            )
            if response.status_code < 500:
                return response
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(min(2.0, 0.4 * attempt))
    if last_error:
        print(f"  [请求失败] {url}: {last_error}")
    return None


def normalize_title(title: str) -> str:
    text = re.sub(r"<[^>]+>", " ", title)
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("×", "x")
    return text


def pubmed_search(session: requests.Session, query: str, max_results: int, min_year: int) -> list[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    response = request_with_retry(
        session,
        "GET",
        url,
        timeout=REQUEST_TIMEOUT,
        params={
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance",
            "mindate": str(min_year),
            "datetype": "pdat",
        },
    )
    if response is None:
        return []
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])


def extract_article_ids(root: ET.Element) -> dict[str, str]:
    article_ids: dict[str, str] = {}
    for node in root.findall(".//ArticleId"):
        id_type = (node.attrib.get("IdType") or "").lower()
        value = (node.text or "").strip()
        if id_type and value:
            article_ids[id_type] = value
    return article_ids


def pubmed_fetch_meta(session: requests.Session, pmid: str) -> dict[str, Any]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    response = request_with_retry(
        session,
        "GET",
        url,
        timeout=REQUEST_TIMEOUT,
        params={"db": "pubmed", "id": pmid, "retmode": "xml"},
    )
    if response is None:
        return {}
    response.raise_for_status()

    root = ET.fromstring(response.text)
    article = root.find(".//Article")
    if article is None:
        return {}

    title = normalize_title(article.findtext(".//ArticleTitle") or "")
    abstract_parts = article.findall(".//AbstractText")
    abstract = " ".join(" ".join(part.itertext()).strip() for part in abstract_parts).strip()
    article_ids = extract_article_ids(root)

    year = 0
    for candidate in [
        root.findtext(".//PubDate/Year"),
        root.findtext(".//ArticleDate/Year"),
        root.findtext(".//PubMedPubDate[@PubStatus='pubmed']/Year"),
    ]:
        if candidate and candidate.isdigit():
            year = int(candidate)
            break

    journal = normalize_title(root.findtext(".//Journal/Title") or "")
    authors = []
    for author in root.findall(".//Author"):
        last = (author.findtext("LastName") or "").strip()
        fore = (author.findtext("ForeName") or "").strip()
        name = " ".join(part for part in [fore, last] if part).strip()
        if name:
            authors.append(name)

    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
        "year": year,
        "doi": article_ids.get("doi", ""),
        "pmcid": article_ids.get("pmc", ""),
        "journal": journal,
        "authors": authors[:8],
    }


def semantic_scholar_pdf(session: requests.Session, title: str) -> str | None:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    response = request_with_retry(
        session,
        "GET",
        url,
        timeout=REQUEST_TIMEOUT,
        params={
            "query": title,
            "fields": "title,openAccessPdf,externalIds,year",
            "limit": 3,
        },
    )
    if response is None or response.status_code != 200:
        return None
    data = response.json().get("data", [])
    normalized = normalize_title(title).lower()
    for item in data:
        item_title = normalize_title(item.get("title") or "").lower()
        if item_title and normalized and item_title[:80] != normalized[:80]:
            continue
        pdf_info = item.get("openAccessPdf") or {}
        pdf_url = pdf_info.get("url")
        if pdf_url:
            return pdf_url
    for item in data:
        pdf_info = item.get("openAccessPdf") or {}
        pdf_url = pdf_info.get("url")
        if pdf_url:
            return pdf_url
    return None


def parse_pdf_links_from_html(html: str) -> list[str]:
    patterns = [
        r'citation_pdf_url"\s+content="([^"]+)"',
        r'citation_pdf_url" content="([^"]+)"',
        r"citation_pdf_url' content='([^']+)'",
        r'href="([^"]+\.pdf(?:\?[^"]*)?)"',
        r"href='([^']+\.pdf(?:\?[^']*)?)'",
        r'"pdfUrl":"([^"]+)"',
    ]
    links: list[str] = []
    for pattern in patterns:
        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            links.append(match.replace("\\u002F", "/").replace("\\/", "/"))
    return links


def doi_pdf_candidates(session: requests.Session, doi: str) -> list[str]:
    if not doi:
        return []
    doi_url = f"https://doi.org/{quote(doi, safe='/')}"
    response = request_with_retry(session, "GET", doi_url, timeout=REQUEST_TIMEOUT)
    if response is None or response.status_code >= 400:
        return []

    candidates: list[str] = []
    content_type = response.headers.get("Content-Type", "").lower()
    final_url = response.url
    if "pdf" in content_type or final_url.lower().endswith(".pdf"):
        candidates.append(final_url)

    text = response.text
    for link in parse_pdf_links_from_html(text):
        if link.startswith("//"):
            candidates.append(f"https:{link}")
        elif link.startswith("http://") or link.startswith("https://"):
            candidates.append(link)
        elif link.startswith("/"):
            from requests.compat import urljoin

            candidates.append(urljoin(final_url, link))
    return list(dict.fromkeys(candidates))


def pmc_pdf_candidates(pmcid: str) -> list[str]:
    if not pmcid:
        return []
    cleaned = pmcid if pmcid.upper().startswith("PMC") else f"PMC{pmcid}"
    return [
        f"https://pmc.ncbi.nlm.nih.gov/articles/{cleaned}/pdf/",
        f"https://pmc.ncbi.nlm.nih.gov/articles/{cleaned}/pdf/{cleaned}.pdf",
    ]


def download_pdf(session: requests.Session, url: str, save_path: Path) -> bool:
    response = request_with_retry(session, "GET", url, timeout=PDF_TIMEOUT, stream=True)
    if response is None or response.status_code != 200:
        return False

    content_type = response.headers.get("Content-Type", "").lower()
    chunks: list[bytes] = []
    try:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                chunks.append(chunk)
    finally:
        response.close()

    content = b"".join(chunks)
    if not content:
        return False
    if b"%PDF" not in content[:1024] and "pdf" not in content_type:
        return False

    save_path.write_bytes(content)
    return True


def build_pdf_candidates(session: requests.Session, meta: dict[str, Any]) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for url in pmc_pdf_candidates(meta.get("pmcid", "")):
        candidates.append(("pmc", url))
    for url in doi_pdf_candidates(session, meta.get("doi", "")):
        candidates.append(("doi", url))
    semantic_pdf = semantic_scholar_pdf(session, meta.get("title", ""))
    if semantic_pdf:
        candidates.append(("semantic_scholar", semantic_pdf))

    unique: list[tuple[str, str]] = []
    seen: set[str] = set()
    for source, url in candidates:
        if url and url not in seen:
            seen.add(url)
            unique.append((source, url))
    return unique


def should_keep(meta: dict[str, Any], min_year: int) -> bool:
    abstract = (meta.get("abstract") or "").lower()
    title = (meta.get("title") or "").lower()
    year = meta.get("year", 0)
    combined = f"{title} {abstract}"

    has_gene_signal = any(keyword in combined for keyword in GENE_KEYWORDS)
    has_breeding_signal = any(keyword in combined for keyword in BREEDING_KEYWORDS)
    title_gene_signal = any(keyword in title for keyword in GENE_KEYWORDS)
    title_breeding_signal = any(keyword in title for keyword in BREEDING_KEYWORDS)
    too_postharvest = any(keyword in combined for keyword in NEGATIVE_KEYWORDS)

    score = 0
    if has_gene_signal:
        score += 2
    if has_breeding_signal:
        score += 2
    if title_gene_signal:
        score += 1
    if title_breeding_signal:
        score += 1
    if "apple" in combined or "malus" in combined:
        score += 1
    if too_postharvest:
        score -= 3

    return bool(year >= min_year and score >= 3 and not too_postharvest)


def save_trait_metadata(trait_dir: Path, pmid: str, meta: dict[str, Any]) -> None:
    meta_dir = trait_dir / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    (meta_dir / f"{pmid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch apple breeding papers into pipeline workspace")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    parser.add_argument("--output-dir", help="Override papers output directory")
    parser.add_argument("--meta-file", help="Override fetch state JSON path")
    parser.add_argument("--max-per-trait", type=int, help="Override max results per trait")
    parser.add_argument("--min-year", type=int, help="Override minimum publication year")
    parser.add_argument("--force-pdf-retry", action="store_true", help="Retry PDF discovery for kept records without pdf")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else layout.source_papers_dir
    meta_file = Path(args.meta_file).resolve() if args.meta_file else layout.fetch_state_file
    max_per_trait = args.max_per_trait or layout.max_per_trait
    min_year = args.min_year or layout.min_year
    trait_queries = layout.trait_queries

    output_dir.mkdir(parents=True, exist_ok=True)
    meta_file.parent.mkdir(parents=True, exist_ok=True)

    if meta_file.exists():
        done: dict[str, Any] = json.loads(meta_file.read_text(encoding="utf-8"))
    else:
        done = {}

    session = create_session()

    for trait, query in trait_queries.items():
        trait_dir = output_dir / trait
        trait_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'=' * 50}")
        print(f"性状: {trait}")
        print(f"查询: {query}")

        pmids = pubmed_search(session, query, max_per_trait, min_year)
        print(f"找到 {len(pmids)} 篇候选")

        added = 0
        pdf_added = 0
        for pmid in pmids:
            existing = done.get(pmid)
            if existing and not args.force_pdf_retry:
                print(f"  [跳过] PMID {pmid} 已处理")
                continue

            time.sleep(SLEEP_SEC)
            meta = pubmed_fetch_meta(session, pmid)
            if not meta:
                done[pmid] = {"trait": trait, "kept": False, "error": "pubmed_fetch_failed"}
                continue
            if not should_keep(meta, min_year):
                done[pmid] = {
                    "trait": trait,
                    "kept": False,
                    "title": meta["title"],
                    "year": meta["year"],
                    "reason": "filtered_out",
                }
                continue

            pdf_saved = False
            pdf_source = ""
            pdf_candidates = build_pdf_candidates(session, meta)
            for source, candidate_url in pdf_candidates:
                save_path = trait_dir / f"{pmid}.pdf"
                if download_pdf(session, candidate_url, save_path):
                    pdf_saved = True
                    pdf_source = source
                    pdf_added += 1
                    print(f"  [PDF] PMID {pmid} <- {source}: {meta['title'][:72]}")
                    break

            if not pdf_saved:
                print(f"  [摘要] PMID {pmid}: 未找到可下载 PDF，保留元数据")

            record = {
                "trait": trait,
                "title": meta["title"],
                "abstract": meta["abstract"],
                "year": meta["year"],
                "doi": meta.get("doi", ""),
                "pmcid": meta.get("pmcid", ""),
                "journal": meta.get("journal", ""),
                "authors": meta.get("authors", []),
                "pdf_saved": pdf_saved,
                "pdf_source": pdf_source,
                "pdf_candidates": [url for _, url in pdf_candidates],
                "kept": True,
            }
            done[pmid] = record
            save_trait_metadata(trait_dir, pmid, {"pmid": pmid, **record})
            added += 1

        print(f"本轮新增记录: {added} 篇")
        print(f"本轮新增PDF:  {pdf_added} 篇")
        meta_file.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")

    kept = [v for v in done.values() if v.get("kept")]
    pdfs = [v for v in kept if v.get("pdf_saved")]
    print(f"\n{'=' * 50}")
    print(f"总计保留论文: {len(kept)} 篇")
    print(f"成功下载PDF:  {len(pdfs)} 篇")
    print(f"仅有摘要:     {len(kept) - len(pdfs)} 篇")
    print(f"PDF输出目录:  {output_dir}")
    print(f"元数据保存于: {meta_file}")


if __name__ == "__main__":
    main()
