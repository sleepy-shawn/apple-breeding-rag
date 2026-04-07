from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

REFERENCE_GENOME_RE = re.compile(
    r"Reference genome:\s*(.*?)(?:\. Colocalizing marker:|\. Population/|\. Dataset:|\. Citation:|$)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit QTL/GWAS coordinate reference-system metadata.")
    parser.add_argument("--genes-dir", type=Path, default=Path("backend/data/genes"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workspace/default/reports/qtl_reference_system_audit.md"),
    )
    return parser.parse_args()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], [{k: v for k, v in row.items() if k is not None} for row in reader]


def infer_reference(row: dict[str, str]) -> str:
    for key in ("reference_genome", "genome_build", "coordinate_system"):
        value = (row.get(key) or "").strip()
        if value:
            return value
    evidence = (row.get("evidence_text") or "").strip()
    match = REFERENCE_GENOME_RE.search(evidence)
    if match:
        return " ".join(match.group(1).split())
    return ""


def has_coordinate(row: dict[str, str]) -> bool:
    return bool((row.get("chr") or "").strip() or (row.get("pos") or "").strip())


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    rows_by_file: list[dict[str, object]] = []
    references: Counter[str] = Counter()
    source_refs: dict[str, Counter[str]] = defaultdict(Counter)
    total_rows = 0
    total_coordinate_rows = 0
    total_reference_rows = 0

    for path in sorted(args.genes_dir.glob("*.csv")):
        fields, rows = read_rows(path)
        if not rows:
            rows_by_file.append(
                {
                    "file": path.name,
                    "rows": 0,
                    "coordinate_rows": 0,
                    "reference_rows": 0,
                    "fields": fields,
                    "top_references": [],
                }
            )
            continue

        file_refs: Counter[str] = Counter()
        coordinate_rows = 0
        reference_rows = 0
        for row in rows:
            total_rows += 1
            source = (row.get("source_file") or "unknown").strip() or "unknown"
            if has_coordinate(row):
                coordinate_rows += 1
                total_coordinate_rows += 1
            reference = infer_reference(row)
            if reference:
                reference_rows += 1
                total_reference_rows += 1
                file_refs[reference] += 1
                references[reference] += 1
                source_refs[source][reference] += 1

        rows_by_file.append(
            {
                "file": path.name,
                "rows": len(rows),
                "coordinate_rows": coordinate_rows,
                "reference_rows": reference_rows,
                "fields": fields,
                "top_references": file_refs.most_common(3),
            }
        )

    lines = [
        "# QTL/GWAS Reference-System Audit",
        "",
        "This report checks whether gene/QTL/GWAS CSV files carry enough reference-genome metadata for safe coordinate interpretation.",
        "",
        "## Summary",
        "",
        f"- Total CSV rows: `{total_rows}`",
        f"- Rows with chr/pos coordinates: `{total_coordinate_rows}`",
        f"- Rows with parsed reference-genome metadata: `{total_reference_rows}`",
        "",
        "Interpretation: coordinates should be treated as source-reported raw coordinates unless `reference_genome` is explicitly available. Do not merge or compare positions across studies without liftover and source-build validation.",
        "",
        "## Top Parsed Reference Genomes",
        "",
    ]

    if references:
        for ref, count in references.most_common(12):
            lines.append(f"- `{ref}`: {count}")
    else:
        lines.append("- No explicit reference-genome metadata parsed.")

    lines += [
        "",
        "## File-Level Coverage",
        "",
        "| File | Rows | chr/pos rows | parsed reference rows | top references |",
        "|------|------|--------------|-----------------------|----------------|",
    ]
    for item in rows_by_file:
        top_refs = "; ".join(f"{ref} ({count})" for ref, count in item["top_references"]) or "-"
        lines.append(
            f"| `{item['file']}` | {item['rows']} | {item['coordinate_rows']} | {item['reference_rows']} | {top_refs} |"
        )

    lines += [
        "",
        "## Recommended Thesis Wording",
        "",
        "The system preserves source-reported chromosome and position fields from QTL/GWAS resources, but does not perform cross-study coordinate liftover. When reference genome information is absent or inconsistent, chromosome positions are used only as provenance metadata rather than as direct evidence for physical colocalization.",
        "",
    ]

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
