"""
Build a smaller, cleaner GDR layer for retrieval.

This keeps rows that expose a likely candidate gene, strong evidence,
or a trait-relevant QTL/GWAS signal, then deduplicates noisy marker-level
records into a more retrieval-friendly CSV.

Usage:
    python3 scripts/build_gdr_curated_layer.py \
        --input-dir backend/data/genes \
        --output-dir backend/data/genes
"""
from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path


TRAITS = ["firmness", "color", "acidity", "harvest", "sugar"]
GENE_ID_RE = re.compile(r"\b(?:MD\d{2}G\d+|Md[A-Za-z][A-Za-z0-9]+|Ma\d+|LAR1)\b")
ASSOCIATED_GENE_RE = re.compile(
    r"Associated gene:\s*([A-Za-z0-9_,; \-]+?)(?:\.| GWAS marker:| Published symbol:| P-value:)"
)
GENERIC_LABEL_TOKENS = {
    "brix",
    "brixg",
    "brixr",
    "acidity",
    "malacid",
    "pickday",
    "drop",
    "skin color",
    "skin overcolour",
    "fruit color",
    "fruit skin color",
    "yellowcolor",
    "greencolor",
    "solublesolidscontent",
    "sugar content",
    "harvest date",
    "ripening period",
}


def extract_candidate_genes(row: dict[str, str]) -> list[str]:
    gene_value = (row.get("gene") or "").strip()
    evidence = (row.get("evidence_text") or "").strip()
    hits: list[str] = []
    seen: set[str] = set()

    for source in [gene_value]:
        for match in GENE_ID_RE.finditer(source):
            gene = match.group(0)
            key = gene.lower()
            if key not in seen:
                seen.add(key)
                hits.append(gene)

    assoc_match = ASSOCIATED_GENE_RE.search(evidence)
    if assoc_match:
        for match in GENE_ID_RE.finditer(assoc_match.group(1)):
            gene = match.group(0)
            key = gene.lower()
            if key not in seen:
                seen.add(key)
                hits.append(gene)

    for match in GENE_ID_RE.finditer(evidence):
        gene = match.group(0)
        key = gene.lower()
        if key not in seen:
            seen.add(key)
            hits.append(gene)
        if len(hits) >= 4:
            break
    return hits


def parse_significance(value: str) -> float:
    raw = (value or "").strip()
    if not raw:
        return 0.0
    try:
        number = float(raw)
    except ValueError:
        return 0.0
    if number <= 0:
        return 0.0
    # Some source rows store p-values directly, others store -log10(P).
    if number < 1:
        return -math.log10(number)
    return number


def is_generic_label(label: str) -> bool:
    lowered = (label or "").strip().lower()
    if not lowered:
        return True
    return any(token in lowered for token in GENERIC_LABEL_TOKENS)


def build_display_title(row: dict[str, str], candidate_genes: list[str]) -> str:
    gene_label = (row.get("gene") or "").strip()
    if candidate_genes:
        joined = ", ".join(candidate_genes[:2])
        if gene_label and joined.lower() != gene_label.lower():
            return f"{joined} ({gene_label})"
        return joined
    if gene_label:
        return gene_label
    trait = (row.get("trait") or "").strip()
    return f"{trait} locus" if trait else "gdr locus"


def keep_row(row: dict[str, str], candidate_genes: list[str]) -> bool:
    evidence = (row.get("evidence_text") or "").strip()
    score = parse_significance(row.get("pvalue") or row.get("score_raw") or "")
    gene_label = (row.get("gene") or "").strip()
    has_assoc_gene = "Associated gene:" in evidence
    is_qtl = "GDR QTL:" in evidence
    strong_score = score >= 4.0

    if candidate_genes and (has_assoc_gene or strong_score or is_qtl):
        return True
    if candidate_genes and not is_generic_label(gene_label) and score >= 3.0:
        return True
    return False


def dedupe_key(row: dict[str, str], candidate_genes: list[str]) -> tuple[str, str, str, str, str]:
    return (
        (row.get("trait") or "").strip(),
        ",".join(g.lower() for g in candidate_genes[:2]),
        (row.get("chr") or "").strip(),
        (row.get("pos") or "").strip(),
        (row.get("snp") or "").strip(),
    )


def row_priority(row: dict[str, str], candidate_genes: list[str]) -> tuple[float, int, int]:
    evidence = (row.get("evidence_text") or "").strip()
    score = parse_significance(row.get("pvalue") or row.get("score_raw") or "")
    has_assoc_gene = 1 if "Associated gene:" in evidence else 0
    is_qtl = 1 if "GDR QTL:" in evidence else 0
    candidate_count = len(candidate_genes)
    return (score, has_assoc_gene + is_qtl, candidate_count)


def curate_trait_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    picked_by_key: dict[tuple[str, str, str, str, str], tuple[tuple[float, int, int], dict[str, str]]] = {}
    per_gene_limit: defaultdict[str, int] = defaultdict(int)
    kept: list[dict[str, str]] = []

    for row in rows:
        candidate_genes = extract_candidate_genes(row)
        if not keep_row(row, candidate_genes):
            continue

        enriched = dict(row)
        if candidate_genes:
            enriched["candidate_gene"] = ", ".join(candidate_genes[:3])
        enriched["display_title"] = build_display_title(row, candidate_genes)
        enriched["generic_label"] = "1" if is_generic_label(row.get("gene", "")) else "0"
        priority = row_priority(row, candidate_genes)
        key = dedupe_key(row, candidate_genes)

        existing = picked_by_key.get(key)
        if existing is None or priority > existing[0]:
            picked_by_key[key] = (priority, enriched)

    ranked = sorted(
        (item for _, item in picked_by_key.values()),
        key=lambda r: row_priority(r, extract_candidate_genes(r)),
        reverse=True,
    )

    for row in ranked:
        gene_bucket = (row.get("candidate_gene") or row.get("display_title") or "").lower()
        if gene_bucket and per_gene_limit[gene_bucket] >= 8:
            continue
        if gene_bucket:
            per_gene_limit[gene_bucket] += 1
        kept.append(row)

    return kept


def main() -> None:
    parser = argparse.ArgumentParser(description="Build curated GDR retrieval layer")
    parser.add_argument("--input-dir", default="backend/data/genes")
    parser.add_argument("--output-dir", default="backend/data/genes")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    combined_rows: list[dict[str, str]] = []
    fieldnames: list[str] | None = None

    for trait in TRAITS:
        path = input_dir / f"genes_gdr_{trait}.csv"
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if reader.fieldnames and fieldnames is None:
                fieldnames = list(reader.fieldnames)
        curated = curate_trait_rows(rows)
        combined_rows.extend(curated)

        trait_fields = list(fieldnames or [])
        for extra in ["candidate_gene", "display_title", "generic_label"]:
            if extra not in trait_fields:
                trait_fields.append(extra)
        out_path = output_dir / f"genes_gdr_curated_{trait}.csv"
        with out_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=trait_fields)
            writer.writeheader()
            writer.writerows(curated)
        print(f"{trait:<10} -> {len(curated):4d} rows -> {out_path}")

    all_fields = list(fieldnames or [])
    for extra in ["candidate_gene", "display_title", "generic_label"]:
        if extra not in all_fields:
            all_fields.append(extra)
    combined_path = output_dir / "genes_gdr_curated.csv"
    with combined_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(combined_rows)
    print(f"combined    -> {len(combined_rows):4d} rows -> {combined_path}")


if __name__ == "__main__":
    main()
