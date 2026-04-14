#!/usr/bin/env python3
"""Split structured genes CSV into trait-specific subsets."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

TARGET_TRAITS = ["firmness", "acidity", "sugar", "color", "harvest"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build trait subset CSVs")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        grouped = defaultdict(list)
        for row in reader:
            trait = (row.get("trait") or "").strip().lower()
            if trait in TARGET_TRAITS:
                grouped[trait].append(row)

    for trait in TARGET_TRAITS:
        rows = grouped.get(trait, [])
        out = out_dir / f"genes_{trait}.csv"
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(rows)
        print(f"{trait}: {len(rows)} -> {out}")


if __name__ == "__main__":
    main()
