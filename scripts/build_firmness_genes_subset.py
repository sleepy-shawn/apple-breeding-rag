#!/usr/bin/env python3
"""Build firmness-focused subset from genes.csv.

Input expected columns: source_file,sheet,row_index,row_text
Output keeps same columns + trait_guess.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

FIRMNESS_KEYS = {
    "firmness",
    "hardness",
    "crispness",
    "crisp",
    "texture",
    "ripening",
    "mdnac18",
    "mdnac5",
    "mdpg",
    "mdacs",
    "mderf3",
    "mderf118",
    "硬度",
    "脆度",
    "质地",
    "软化",
    "成熟",
}

NEGATIVE_KEYS = {
    "fire blight",
    "scab",
    "anthracnose",
    "褐斑病",
    "炭疽",
    "病害",
}

HEADER_HINTS = {
    "table s",
    "supplementary table",
    "the key snp information",
    "trait:",
    "traits",
}

DATA_HINTS = {
    "snp-",
    "snp_",
    "chr",
    "locus",
    "position",
    "marker",
    "genotype",
}

PRIMER_KEYS = {
    "primer",
    "primer sequences",
    "list of primer sequences",
    "-marker f",
    "-marker r",
    " marker f",
    " marker r",
}


def is_header_like(text: str) -> bool:
    lowered = text.lower().strip()
    if any(h in lowered for h in HEADER_HINTS):
        # Header rows usually have no concrete numeric marker values.
        if not re.search(r"\d{2,}", lowered):
            return True
    # Common flattened-table header artifacts.
    if lowered.count("col_") >= 8 and not re.search(r"snp[-_]?\d+", lowered):
        return True
    return False


def has_data_signal(text: str) -> bool:
    lowered = text.lower()
    hint = any(h in lowered for h in DATA_HINTS)
    has_number = bool(re.search(r"\d", lowered))
    has_snp_id = bool(re.search(r"snp[-_]?\d+", lowered))
    has_chr_pos = bool(re.search(r"chr\s*\d+|chr\d+", lowered))
    return (hint and has_number) or has_snp_id or has_chr_pos


def is_primer_like(text: str) -> bool:
    lowered = text.lower()
    return any(k in lowered for k in PRIMER_KEYS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build firmness gene subset CSV")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    kept = []
    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (row.get("row_text") or "").lower()
            if not text:
                continue
            pos = any(k in text for k in FIRMNESS_KEYS)
            neg = any(k in text for k in NEGATIVE_KEYS)
            header_like = is_header_like(text)
            data_like = has_data_signal(text)
            primer_like = is_primer_like(text)
            if pos and not neg and data_like and not header_like and not primer_like:
                row["trait_guess"] = "firmness_like"
                row["record_type"] = "data"
                kept.append(row)

    # dedup by source+sheet+row_index+row_text
    dedup = {}
    for r in kept:
        key = (r.get("source_file", ""), r.get("sheet", ""), r.get("row_index", ""), r.get("row_text", ""))
        dedup[key] = r
    rows = list(dedup.values())

    headers = ["source_file", "sheet", "row_index", "row_text", "trait_guess", "record_type"]
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"input={in_path}")
    print(f"output={out_path}")
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
