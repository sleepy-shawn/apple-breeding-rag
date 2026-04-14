#!/usr/bin/env python3
"""Rank fetched papers into core/candidate/reject tiers.

Usage:
  python scripts/pipeline/rank_fetched_papers.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout

APPLE_TERMS = [
    "apple",
    "malus",
    "domestica",
    "red-fleshed apple",
    "malus x domestica",
]

BREEDING_TERMS = [
    "breeding",
    "marker",
    "marker-assisted",
    "qtl",
    "gwas",
    "locus",
    "candidate gene",
    "genetic map",
    "linkage map",
    "association mapping",
    "selection",
]

STRONG_TRAIT_TERMS: dict[str, list[str]] = {
    "color": ["anthocyanin", "pigmentation", "skin color", "fruit color", "red flesh", "myb10"],
    "acidity": ["acidity", "malic acid", "titratable acidity", "organic acid"],
    "sugar": ["sugar", "sucrose", "sorbitol", "soluble solids", "sweetness", "brix"],
    "disease": ["resistance", "fire blight", "scab", "powdery mildew", "alternaria"],
    "maturity": ["ripening", "maturity", "harvest date", "fruit development", "early ripening"],
    "firmness": ["firmness", "texture", "crispness", "softening", "cell wall"],
}

GENE_TERMS = [
    "gene",
    "allele",
    "snp",
    "transcription factor",
    "erf",
    "myb",
    "nac",
    "candidate gene",
]

REVIEW_TERMS = ["review", "research progress", "overview", "advances in", "progress of"]
GENERIC_SCOPE_TERMS = [
    "fruit crops",
    "germplasm resources",
    "outcross populations",
    "tool",
    "analysis tool",
    "breeding efficiency",
]
NON_TARGET_TERMS = [
    "citrus",
    "tomato",
    "grape",
    "peach",
    "strawberry",
    "kiwifruit",
    "kiwi",
    "pear",
    "banana",
    "rice",
    "maize",
    "wheat",
]
LOW_SIGNAL_TERMS = [
    "postharvest",
    "storage",
    "processing",
    "fresh-cut",
    "coating",
    "senescence",
]


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def count_hits(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def classify_record(pmid: str, record: dict[str, Any]) -> dict[str, Any]:
    title = (record.get("title") or "").strip()
    abstract = (record.get("abstract") or "").strip()
    text = f"{title}\n{abstract}".lower()
    trait = (record.get("trait") or "").strip().lower()

    score = 0
    reasons: list[str] = []

    if contains_any(text, APPLE_TERMS):
        score += 3
        reasons.append("apple_match")
    else:
        score -= 4
        reasons.append("apple_missing")

    if contains_any(text, BREEDING_TERMS):
        score += 3
        reasons.append("breeding_signal")

    trait_terms = STRONG_TRAIT_TERMS.get(trait, [])
    trait_hits = count_hits(text, trait_terms)
    if trait_hits >= 2:
        score += 3
        reasons.append("strong_trait_match")
    elif trait_hits == 1:
        score += 1
        reasons.append("weak_trait_match")
    else:
        score -= 2
        reasons.append("trait_weak")

    gene_hits = count_hits(text, GENE_TERMS)
    if gene_hits >= 2:
        score += 2
        reasons.append("gene_signal")
    elif gene_hits == 1:
        score += 1

    if record.get("pdf_saved"):
        score += 3
        reasons.append("pdf_saved")
    elif record.get("pmcid"):
        score += 2
        reasons.append("pmc_available")
    elif record.get("doi"):
        score += 1
        reasons.append("doi_available")

    if contains_any(title.lower(), REVIEW_TERMS):
        score -= 3
        reasons.append("review_penalty")

    if contains_any(text, GENERIC_SCOPE_TERMS):
        score -= 3
        reasons.append("generic_scope_penalty")

    if contains_any(text, NON_TARGET_TERMS):
        score -= 6
        reasons.append("non_target_crop")

    if contains_any(text, LOW_SIGNAL_TERMS):
        score -= 4
        reasons.append("low_signal_context")

    if not title:
        score -= 8
        reasons.append("missing_title_penalty")
    elif len(title) < 25:
        score -= 4
        reasons.append("short_title_penalty")
    elif title.endswith("("):
        score -= 1
        reasons.append("title_cleanup_needed")

    journal = (record.get("journal") or "").strip()
    if journal:
        reasons.append(f"journal:{journal[:40]}")

    if score >= 8:
        tier = "core"
    elif score >= 4:
        tier = "candidate"
    else:
        tier = "reject"

    return {
        "pmid": pmid,
        "trait": trait,
        "year": record.get("year", 0),
        "tier": tier,
        "score": score,
        "pdf_saved": bool(record.get("pdf_saved")),
        "pdf_source": record.get("pdf_source", ""),
        "doi": record.get("doi", ""),
        "pmcid": record.get("pmcid", ""),
        "journal": journal,
        "title": title,
        "reasons": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank fetched papers into core/candidate/reject tiers")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    parser.add_argument("--meta-file", help="Override fetched papers metadata JSON path")
    parser.add_argument("--csv-out", help="Override ranking CSV output path")
    parser.add_argument("--jsonl-out", help="Override ranking JSONL output path")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    meta_file = Path(args.meta_file).resolve() if args.meta_file else layout.fetch_state_file
    csv_out = (
        Path(args.csv_out).resolve()
        if args.csv_out
        else layout.reports_dir / "paper_fetch_ranking.csv"
    )
    jsonl_out = (
        Path(args.jsonl_out).resolve()
        if args.jsonl_out
        else layout.reports_dir / "paper_fetch_ranking.jsonl"
    )
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    jsonl_out.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(meta_file.read_text(encoding="utf-8"))
    ranked = [
        classify_record(pmid, record)
        for pmid, record in data.items()
        if record.get("kept")
    ]
    ranked.sort(key=lambda item: ({"core": 0, "candidate": 1, "reject": 2}[item["tier"]], -item["score"], -(item["year"] or 0), item["pmid"]))

    with csv_out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "tier",
                "score",
                "trait",
                "year",
                "pmid",
                "pdf_saved",
                "pdf_source",
                "doi",
                "pmcid",
                "journal",
                "title",
                "reasons",
            ]
        )
        for item in ranked:
            writer.writerow(
                [
                    item["tier"],
                    item["score"],
                    item["trait"],
                    item["year"],
                    item["pmid"],
                    "yes" if item["pdf_saved"] else "no",
                    item["pdf_source"],
                    item["doi"],
                    item["pmcid"],
                    item["journal"],
                    item["title"],
                    "|".join(item["reasons"]),
                ]
            )

    with jsonl_out.open("w", encoding="utf-8") as f:
        for item in ranked:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    priority_txt = layout.reports_dir / "paper_core_priority.txt"
    with priority_txt.open("w", encoding="utf-8") as f:
        for item in ranked:
            if item["tier"] != "core":
                continue
            pdf_flag = "PDF" if item["pdf_saved"] else "ABSTRACT"
            f.write(
                f"[{item['score']:>2}] {item['trait']:<9} {item['year']} {pdf_flag:<8} PMID {item['pmid']}  {item['title']}\n"
            )

    counts: dict[str, int] = {"core": 0, "candidate": 0, "reject": 0}
    for item in ranked:
        counts[item["tier"]] += 1

    print(f"total_ranked={len(ranked)}")
    print(f"core={counts['core']}")
    print(f"candidate={counts['candidate']}")
    print(f"reject={counts['reject']}")
    print(f"csv={csv_out}")
    print(f"jsonl={jsonl_out}")
    print(f"priority={priority_txt}")


if __name__ == "__main__":
    main()
