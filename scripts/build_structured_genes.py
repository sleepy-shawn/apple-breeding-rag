#!/usr/bin/env python3
"""Build structured genes table from flattened genes.csv rows.

Input columns expected:
- source_file, sheet, row_index, row_text

Output columns:
- source_file, sheet, row_index, trait, gene, snp, chr, pos, pvalue, score_raw, variety, evidence_text
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

TRAIT_RULES = {
    "firmness": ["firmness", "crispness", "hardness", "texture", "脆度", "硬度", "软化", "flesh crisp"],
    "acidity": ["fruit acidity", "titratable acidity", "malic acid", "苹果酸", "酸度", "有机酸"],
    "sugar": ["sugar", "soluble solids", "brix", "sucrose", "fructose", "glucose", "糖度", "可溶性固形物"],
    "color": ["skin color", "anthocyanin", "myb10", "果皮颜色", "花青素", "着色"],
    "harvest": ["harvest date", "ripening", "maturity", "成熟期", "采收期", "成熟"],
}

NEGATIVE_HINTS = ["fire blight", "anthracnose", "scab", "褐斑病", "炭疽", "病害"]

SNP_RE = re.compile(r"\bSNP[-_ ]?\d[\d,_.-]*\b", re.IGNORECASE)
GENE_RE_1 = re.compile(r"\bgene:([A-Za-z0-9_.-]+)", re.IGNORECASE)
GENE_RE_2 = re.compile(r"\b(Md[A-Za-z0-9_.-]{2,})\b")
CHR_POS_RE = re.compile(r"\b(Chr\s*\d+)\s*[:]\s*(\d+)\b", re.IGNORECASE)
PVAL_RE = re.compile(r"\b(\d+(?:\.\d+)?E[-+]?\d+)\b", re.IGNORECASE)
HEADER_HINTS = ["table s", "supplementary table", "name;", "traits", "marker combination"]
METHOD_HINTS = ["list of primer sequences", "primer", "electrophoresis", "pcr reaction", "experimental procedure"]


def detect_trait(text: str) -> str:
    t = text.lower()
    if any(x in t for x in NEGATIVE_HINTS):
        return ""
    for trait, keys in TRAIT_RULES.items():
        if any(k in t for k in keys):
            return trait
    return ""


def is_header_or_method_row(text: str, row_index: str) -> bool:
    t = text.lower()
    if any(k in t for k in METHOD_HINTS):
        return True
    if row_index.strip() == "1" and any(k in t for k in HEADER_HINTS):
        return True
    return False


def extract_first(regex: re.Pattern[str], text: str) -> str:
    m = regex.search(text)
    if not m:
        return ""
    return (m.group(1) if m.groups() else m.group(0)).strip()


def extract_chr_pos(text: str) -> tuple[str, str]:
    m = CHR_POS_RE.search(text)
    if m:
        return m.group(1).replace(" ", ""), m.group(2)

    # common flattened format: col_3: Chr03; col_4: 30696840
    m_chr = re.search(r"col_3:\s*(Chr\d+)", text, flags=re.IGNORECASE)
    m_pos = re.search(r"col_4:\s*(\d{4,})", text, flags=re.IGNORECASE)
    if m_chr or m_pos:
        return (m_chr.group(1) if m_chr else "", m_pos.group(1) if m_pos else "")

    return "", ""


def extract_pvalue(text: str) -> str:
    low = text.lower()
    # Only treat as p-value when clear statistical context exists.
    stat_context = any(k in low for k in ["gwas", "p-value", "p value", "significance", "association analysis"])
    if not stat_context:
        return ""
    m = PVAL_RE.search(text)
    if m:
        return m.group(1)
    # fallback: col_5 is often p-value in GWAS-like table
    m2 = re.search(r"col_5:\s*([0-9.]+(?:E[-+]?\d+)?)", text, flags=re.IGNORECASE)
    if m2 and ("e-" in m2.group(1).lower() or "e+" in m2.group(1).lower()):
        return m2.group(1)
    return ""


def extract_score_raw(text: str) -> str:
    # For DEG / expression-like rows, keep col_5 as a generic score.
    m = re.search(r"col_5:\s*([0-9.]+(?:E[-+]?\d+)?)", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""


def extract_variety(text: str) -> str:
    # pattern: KASP genotyping in SNP-2,002: Honeycrisp;
    m = re.search(r"KASP\s+genotyping\s+in\s+SNP[-_ ]?\d[\d,_.-]*:\s*([^;]+)", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


def normalize_snp(text: str) -> str:
    m = SNP_RE.search(text)
    if not m:
        return ""
    return m.group(0).replace(" ", "").upper()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build structured genes CSV")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows_out = []
    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (row.get("row_text") or "").strip()
            if not text:
                continue
            if is_header_or_method_row(text, str(row.get("row_index", ""))):
                continue

            trait = detect_trait(text)
            if not trait:
                continue

            gene = extract_first(GENE_RE_1, text) or extract_first(GENE_RE_2, text)
            snp = normalize_snp(text)
            chr_, pos = extract_chr_pos(text)
            pvalue = extract_pvalue(text)
            score_raw = extract_score_raw(text)
            variety = extract_variety(text)

            if not (gene or snp or (chr_ and pos)):
                continue

            rows_out.append(
                {
                    "source_file": row.get("source_file", ""),
                    "sheet": row.get("sheet", ""),
                    "row_index": row.get("row_index", ""),
                    "trait": trait,
                    "gene": gene,
                    "snp": snp,
                    "chr": chr_,
                    "pos": pos,
                    "pvalue": pvalue,
                    "score_raw": score_raw,
                    "variety": variety,
                    "evidence_text": text,
                }
            )

    # dedupe
    dedup = {}
    for r in rows_out:
        key = (r["source_file"], r["sheet"], r["row_index"], r["gene"], r["snp"], r["chr"], r["pos"], r["trait"])
        dedup[key] = r
    final_rows = list(dedup.values())

    headers = [
        "source_file",
        "sheet",
        "row_index",
        "trait",
        "gene",
        "snp",
        "chr",
        "pos",
        "pvalue",
        "score_raw",
        "variety",
        "evidence_text",
    ]

    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"input={in_path}")
    print(f"output={out_path}")
    print(f"rows={len(final_rows)}")


if __name__ == "__main__":
    main()
