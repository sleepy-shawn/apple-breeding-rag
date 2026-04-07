"""
引文挖掘脚本 — 以现有种子论文为起点，通过 Semantic Scholar API 找到：
  1. 种子论文引用了哪些论文（上游经典文献）
  2. 哪些论文引用了种子论文（最新跟进研究）

输出：按优先级排序的下载清单（含DOI / PMC / 标题 / 摘要关键词）

用法：
    python3 scripts/mine_citations.py
    python3 scripts/mine_citations.py --seeds-only firmness color acidity
    python3 scripts/mine_citations.py --max-per-seed 50 --min-year 2019
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests

# ──────────────────────────────────────────────
# 种子论文 DOI 表（来自 backend/data/papers/）
# 格式：{ paper_id: (doi, trait, title_hint) }
# ──────────────────────────────────────────────
SEED_DOIS: dict[str, tuple[str, str, str]] = {
    "001": ("10.1093/plcell/koaf007",         "firmness",  "MdNAC18 InDel apple ripening"),
    "006": ("10.1038/s41467-024-54428-5",      "general",   "Fuji apple genome sequencing"),
    "008": ("10.1038/s41467-021-24301-7",      "general",   "Apple genome re-sequencing fruit enlargement"),
    "011": ("10.1111/tpj.13957",               "acidity",   "MdSAUR37 MdPP2CH MdALMTII acidity"),
    "013": ("10.1093/hr/uhae284",              "firmness",  "MdNAC5 fruit firmness ripening"),
    "014": ("10.1371/journal.pgen.1007993",    "color",     "GWAS apple polyphenols"),
    "015": ("10.1073/pnas.2022788118",         "nutrition", "GDP-L-galactose vitamin C apple"),
    "016": ("10.1007/s00122-024-04743-8",      "firmness",  "MdEXP-A1 expansin flesh firmness"),
    "022": ("10.1093/plcell/koae059",          "firmness",  "MdNAC18 harvest date ethylene"),
    "024": ("10.1093/plcell/koae106",          "firmness",  "MdNAC18.1 promoter maturity"),
    "025": ("10.1111/tpj.16100",               "sugar",     "MdMYB109 MdHXK1 sugar content"),
    "028": ("10.1186/1471-2229-14-74",         "color",     "QTL polyphenol apple"),
    "029": ("10.1094/PHYTO-02-20-0051-R",      "disease",   "Fire blight QTL Honeycrisp"),
    "030": ("10.1111/tpj.16314",               "firmness",  "MdERF3 MdERF118 firmness crispness QTL"),
    "032": ("10.1007/s00122-019-03421-5",      "general",   "GWAS apple quality scab resistance"),
    "033": ("10.1371/journal.pgen.1008604",    "disease",   "GWAS fire blight resistance apple"),
    "034": ("10.1038/s41477-021-00940-w",      "general",   "Genomic architecture complex traits apple"),
    "035": ("10.1007/s00122-020-03614-7",      "general",   "Genome to phenome apple historical data"),
    "036": ("10.1186/s12870-021-03023-6",      "general",   "Dense SNP map QTL fruit quality"),
    "038": ("10.3389/fpls.2022.833119",        "disease",   "Minor QTL fire blight apple"),
    "039": ("10.1007/s11032-024-01509-9",      "firmness",  "KASP markers apple crispness"),
    "040": ("10.3390/plants12091874",          "disease",   "Fire blight GWAS Asturian apple"),
}

# 关键词过滤 — 必须包含至少一个苹果相关词
APPLE_KEYWORDS = {
    "apple", "malus", "malus domestica", "rosaceae", "fruit quality",
    "苹果", "果实", "品质", "育种",
}

# 过滤掉明显不相关领域
NEGATIVE_KEYWORDS = {
    "cardiac", "aortic", "neural", "cancer", "tumor", "wheat", "rice",
    "maize", "soybean", "tobacco", "tomato postharvest storage coating",
}

# 高价值性状关键词（用于评分排序）
PRIORITY_TRAITS = {
    "firmness": ["firmness", "crispness", "texture", "softening", "nac", "erf", "expansin"],
    "color":    ["anthocyanin", "myb", "color", "colour", "pigment", "skin"],
    "acidity":  ["malic acid", "acidity", "almt", "malate", "titratable"],
    "sugar":    ["sugar", "sucrose", "sorbitol", "soluble solids", "brix"],
    "harvest":  ["harvest", "ripening", "maturity", "ethylene"],
    "general":  ["gwas", "qtl", "snp", "marker", "breeding", "genetic map"],
}

REQUEST_TIMEOUT = 20
SLEEP_SEC = 0.4


# ──────────────────────────────────────────────
# Semantic Scholar helpers
# ──────────────────────────────────────────────

def ss_get(url: str, params: dict | None = None, retries: int = 3) -> dict | None:
    headers = {"Accept": "application/json"}
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
            if r.status_code == 429:
                wait = 10 * attempt
                print(f"    [rate limit] 等待 {wait}s ...")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
        except requests.RequestException as e:
            print(f"    [请求失败 attempt {attempt}] {e}")
        time.sleep(1.5 * attempt)
    return None


def lookup_paper(doi: str) -> dict | None:
    """Look up a paper by DOI, return Semantic Scholar paper object."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{quote(doi, safe='')}"
    return ss_get(url, params={"fields": "paperId,title,year,abstract,references,citations,externalIds"})


def get_references(paper_id: str, limit: int = 100) -> list[dict]:
    """Get papers this paper references (upstream)."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"
    data = ss_get(url, params={
        "fields": "paperId,title,year,abstract,externalIds,openAccessPdf",
        "limit": limit,
    })
    if not data or not isinstance(data, dict):
        return []
    return [item.get("citedPaper") or {} for item in data.get("data") or []]


def get_citations(paper_id: str, limit: int = 100) -> list[dict]:
    """Get papers that cite this paper (downstream)."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    data = ss_get(url, params={
        "fields": "paperId,title,year,abstract,externalIds,openAccessPdf",
        "limit": limit,
    })
    if not data or not isinstance(data, dict):
        return []
    return [item.get("citingPaper") or {} for item in data.get("data") or []]


# ──────────────────────────────────────────────
# Scoring & filtering
# ──────────────────────────────────────────────

def is_relevant(paper: dict, min_year: int) -> bool:
    title = (paper.get("title") or "").lower()
    abstract = (paper.get("abstract") or "").lower()
    year = paper.get("year") or 0
    combined = title + " " + abstract

    if year and year < min_year:
        return False
    if not paper.get("title"):
        return False
    if any(neg in combined for neg in NEGATIVE_KEYWORDS):
        return False
    if not any(kw in combined for kw in APPLE_KEYWORDS):
        return False
    return True


def score_paper(paper: dict, direction: str) -> float:
    """Higher = more relevant. direction = 'reference' or 'citation'."""
    title = (paper.get("title") or "").lower()
    abstract = (paper.get("abstract") or "").lower()
    combined = title + " " + abstract

    score = 0.0
    # Trait-specific keywords
    for trait, keywords in PRIORITY_TRAITS.items():
        hits = sum(1 for k in keywords if k in combined)
        score += hits * (2.0 if trait in ("firmness", "color", "acidity") else 1.0)

    # GWAS / QTL is always high value
    if "gwas" in combined or "qtl" in combined:
        score += 3.0
    if "candidate gene" in combined or "causal variant" in combined:
        score += 2.0

    # Recent papers worth more
    year = paper.get("year") or 0
    if year >= 2023:
        score += 2.0
    elif year >= 2021:
        score += 1.0

    # Citations upstream means it's a classic
    if direction == "reference":
        score += 1.0

    # Open access PDF available
    if paper.get("openAccessPdf"):
        score += 1.5

    return score


# ──────────────────────────────────────────────
# DOI / download link extraction
# ──────────────────────────────────────────────

def extract_links(paper: dict) -> dict[str, str]:
    links: dict[str, str] = {}
    ext = paper.get("externalIds") or {}

    doi = ext.get("DOI") or ext.get("doi") or ""
    if doi:
        links["doi"] = f"https://doi.org/{doi}"
        links["doi_raw"] = doi

    pmid = ext.get("PubMed") or ext.get("PMID") or ""
    if pmid:
        links["pubmed"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    pmcid = ext.get("PubMedCentral") or ""
    if pmcid:
        pmc = pmcid if pmcid.upper().startswith("PMC") else f"PMC{pmcid}"
        links["pmc"] = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/"
        links["pmc_pdf"] = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/pdf/"

    oa_pdf = (paper.get("openAccessPdf") or {}).get("url") or ""
    if oa_pdf:
        links["open_pdf"] = oa_pdf

    return links


# ──────────────────────────────────────────────
# Main logic
# ──────────────────────────────────────────────

def mine_seed(
    paper_id: str,
    doi: str,
    trait: str,
    title_hint: str,
    max_per_seed: int,
    min_year: int,
    direction: str,  # "both" | "references" | "citations"
) -> list[dict]:
    """Return list of candidate papers found from one seed."""
    print(f"\n{'─'*60}")
    print(f"种子 {paper_id} [{trait}]: {title_hint}")
    print(f"  DOI: {doi}")

    seed_data = lookup_paper(doi)
    if not seed_data:
        print(f"  [!] Semantic Scholar 未找到该 DOI，跳过")
        return []

    ss_id = seed_data.get("paperId", "")
    print(f"  SS paperId: {ss_id}")

    candidates: list[dict] = []

    if direction in ("both", "references"):
        refs = get_references(ss_id, limit=max_per_seed)
        print(f"  引用了: {len(refs)} 篇")
        time.sleep(SLEEP_SEC)
        for p in refs:
            if p and is_relevant(p, min_year):
                p["_direction"] = "reference"
                p["_seed"] = paper_id
                p["_seed_trait"] = trait
                candidates.append(p)

    if direction in ("both", "citations"):
        cites = get_citations(ss_id, limit=max_per_seed)
        print(f"  被引用了: {len(cites)} 篇")
        time.sleep(SLEEP_SEC)
        for p in cites:
            if p and is_relevant(p, min_year):
                p["_direction"] = "citation"
                p["_seed"] = paper_id
                p["_seed_trait"] = trait
                candidates.append(p)

    for p in candidates:
        p["_score"] = score_paper(p, p["_direction"])

    print(f"  过滤后苹果相关: {len(candidates)} 篇")
    return candidates


def deduplicate(papers: list[dict]) -> list[dict]:
    """Deduplicate by DOI or SS paperId, keeping highest score."""
    seen: dict[str, dict] = {}
    for p in papers:
        ext = p.get("externalIds") or {}
        doi = (ext.get("DOI") or ext.get("doi") or "").lower()
        pid = p.get("paperId") or ""
        key = doi or pid
        if not key:
            continue
        if key not in seen or p.get("_score", 0) > seen[key].get("_score", 0):
            seen[key] = p
    return sorted(seen.values(), key=lambda x: x.get("_score", 0), reverse=True)


def format_report(papers: list[dict], existing_dois: set[str]) -> str:
    lines = ["# 苹果育种文献挖掘报告", ""]
    lines.append(f"共发现候选论文: **{len(papers)}** 篇（已去重，按相关性排序）")
    lines.append(f"其中可直接下载PDF: {sum(1 for p in papers if p.get('_links', {}).get('open_pdf') or p.get('_links', {}).get('pmc_pdf'))} 篇")
    lines.append("")

    # Group by trait / category
    high = [p for p in papers if p.get("_score", 0) >= 6]
    mid  = [p for p in papers if 3 <= p.get("_score", 0) < 6]
    low  = [p for p in papers if p.get("_score", 0) < 3]

    for group_name, group in [("🔴 高优先级（score≥6）", high), ("🟡 中优先级（score 3-5）", mid), ("⚪ 低优先级（score<3）", low)]:
        if not group:
            continue
        lines.append(f"\n## {group_name}  ({len(group)} 篇)\n")
        for p in group:
            title = p.get("title") or "(无标题)"
            year = p.get("year") or "?"
            links = p.get("_links") or {}
            direction = p.get("_direction") or ""
            seed = p.get("_seed") or ""
            seed_trait = p.get("_seed_trait") or ""
            score = p.get("_score", 0)
            ext = p.get("externalIds") or {}
            doi_raw = links.get("doi_raw") or ext.get("DOI") or ext.get("doi") or ""

            already = "✅ 已有" if doi_raw.lower() in existing_dois else ""
            direction_cn = "↑上游引用" if direction == "reference" else "↓被引"

            lines.append(f"### {title} ({year}) {already}")
            lines.append(f"- **Score**: {score:.1f}  |  **方向**: {direction_cn}  |  **来源种子**: {seed} [{seed_trait}]")
            if doi_raw:
                lines.append(f"- **DOI**: `{doi_raw}`  →  {links.get('doi','')}")
            if links.get("pmc_pdf"):
                lines.append(f"- **PMC PDF**: {links['pmc_pdf']}")
            if links.get("open_pdf"):
                lines.append(f"- **Open PDF**: {links['open_pdf']}")
            if links.get("pubmed"):
                lines.append(f"- **PubMed**: {links['pubmed']}")
            abstract = (p.get("abstract") or "")[:200]
            if abstract:
                lines.append(f"- **摘要**: {abstract}...")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mine citations from seed apple breeding papers")
    parser.add_argument("--seeds-only", nargs="*", help="只处理指定性状的种子, e.g. firmness color acidity")
    parser.add_argument("--max-per-seed", type=int, default=80, help="每篇种子最多抓取的引文数 (default: 80)")
    parser.add_argument("--min-year", type=int, default=2018, help="最早发表年份过滤 (default: 2018)")
    parser.add_argument("--direction", choices=["both", "references", "citations"], default="both",
                        help="抓取方向: both/references/citations (default: both)")
    parser.add_argument("--output-dir", default="workspace/default/reports", help="报告输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Seeds to process
    seeds = SEED_DOIS
    if args.seeds_only:
        seeds = {k: v for k, v in SEED_DOIS.items() if v[1] in args.seeds_only}
        print(f"只处理性状: {args.seeds_only} → {len(seeds)} 篇种子")

    # Load existing DOIs to mark duplicates
    existing_dois: set[str] = set()
    meta_file = Path("workspace/default/state/fetch/papers_meta.json")
    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        for v in meta.values():
            d = (v.get("doi") or "").lower()
            if d:
                existing_dois.add(d)
    for doi, *_ in SEED_DOIS.values():
        existing_dois.add(doi.lower())

    print(f"\n{'='*60}")
    print(f"开始引文挖掘")
    print(f"种子论文: {len(seeds)} 篇")
    print(f"抓取方向: {args.direction}")
    print(f"最早年份: {args.min_year}")
    print(f"每种子上限: {args.max_per_seed}")
    print(f"{'='*60}")

    all_candidates: list[dict] = []
    for paper_id, (doi, trait, title_hint) in seeds.items():
        if args.seeds_only and trait not in args.seeds_only:
            continue
        batch = mine_seed(
            paper_id=paper_id,
            doi=doi,
            trait=trait,
            title_hint=title_hint,
            max_per_seed=args.max_per_seed,
            min_year=args.min_year,
            direction=args.direction,
        )
        all_candidates.extend(batch)
        time.sleep(SLEEP_SEC)

    # Deduplicate and enrich with links
    deduped = deduplicate(all_candidates)
    for p in deduped:
        p["_links"] = extract_links(p)

    # Filter out papers we already have
    new_papers = [p for p in deduped if (p.get("_links", {}).get("doi_raw") or "").lower() not in existing_dois]
    already_have = [p for p in deduped if (p.get("_links", {}).get("doi_raw") or "").lower() in existing_dois]

    print(f"\n{'='*60}")
    print(f"去重后候选总数: {len(deduped)}")
    print(f"  已有论文（跳过）: {len(already_have)}")
    print(f"  新论文候选: {len(new_papers)}")
    high = sum(1 for p in new_papers if p.get("_score", 0) >= 6)
    mid  = sum(1 for p in new_papers if 3 <= p.get("_score", 0) < 6)
    print(f"  高优先级 (score≥6): {high}")
    print(f"  中优先级 (score 3-5): {mid}")

    # Save JSON
    json_path = output_dir / "citation_mining_results.json"
    json_path.write_text(
        json.dumps(
            [{"title": p.get("title"), "year": p.get("year"),
              "score": p.get("_score"), "links": p.get("_links", {}),
              "abstract": (p.get("abstract") or "")[:300],
              "direction": p.get("_direction"), "seed": p.get("_seed"),
              "seed_trait": p.get("_seed_trait")}
             for p in new_papers],
            ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Save Markdown report
    report_md = format_report(new_papers, existing_dois)
    report_path = output_dir / "citation_mining_report.md"
    report_path.write_text(report_md, encoding="utf-8")

    # Save a simple download checklist (tab-separated, easy to read)
    checklist_path = output_dir / "download_checklist.tsv"
    with checklist_path.open("w", encoding="utf-8") as f:
        f.write("priority\ttitle\tyear\tdoi\tpmc_pdf\topen_pdf\tscore\tseed_trait\tdirection\n")
        for i, p in enumerate(new_papers, 1):
            links = p.get("_links") or {}
            f.write("\t".join([
                str(i),
                (p.get("title") or "").replace("\t", " "),
                str(p.get("year") or ""),
                links.get("doi_raw", ""),
                links.get("pmc_pdf", ""),
                links.get("open_pdf", ""),
                f"{p.get('_score', 0):.1f}",
                p.get("_seed_trait") or "",
                p.get("_direction") or "",
            ]) + "\n")

    print(f"\n输出文件：")
    print(f"  Markdown报告: {report_path}")
    print(f"  JSON结果:     {json_path}")
    print(f"  下载清单:     {checklist_path}")
    print("\n接下来：打开 download_checklist.tsv，按优先级下载PDF，放入 backend/data/papers/")


if __name__ == "__main__":
    main()
