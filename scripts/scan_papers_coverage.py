#!/usr/bin/env python3
"""Scan papers folder coverage and output CSV summary.

Usage:
  python scripts/scan_papers_coverage.py \
    --papers-root "/Users/shuaige/code/rag原数据/papers" \
    --output "/Users/shuaige/code/rag原数据/coverage_report.csv"
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

PDF_EXT = {".pdf"}
TABLE_EXT = {".xls", ".xlsx", ".csv", ".tsv"}
SEQ_EXT = {".fasta", ".fa", ".fna", ".fastq", ".fq", ".vcf", ".vcf.gz", ".gff", ".gff3", ".bed", ".bam", ".sam", ".nex"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz"}


def suffixes_str(path: Path) -> str:
    if path.name.endswith(".vcf.gz"):
        return ".vcf.gz"
    return path.suffix.lower()


def list_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store"]


def count_by_ext(paths: list[Path], allowed: set[str]) -> int:
    c = 0
    for p in paths:
        if suffixes_str(p) in allowed:
            c += 1
    return c


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan paper coverage")
    parser.add_argument("--papers-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    papers_root = Path(args.papers_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows: list[list[str]] = []
    for paper_dir in sorted(p for p in papers_root.iterdir() if p.is_dir()):
        m = re.match(r"^(\d{3})_(.+)$", paper_dir.name)
        seq = m.group(1) if m else ""
        slug = m.group(2) if m else paper_dir.name

        raw_dir = paper_dir / "raw"
        processed_dir = paper_dir / "processed"

        raw_files = list_files(raw_dir) if raw_dir.exists() else []
        processed_files = list_files(processed_dir) if processed_dir.exists() else []

        raw_pdf = count_by_ext(raw_files, PDF_EXT)
        raw_table = count_by_ext(raw_files, TABLE_EXT)
        raw_seq = count_by_ext(raw_files, SEQ_EXT)
        raw_archive = count_by_ext(raw_files, ARCHIVE_EXT)
        processed_table = count_by_ext(processed_files, TABLE_EXT)
        processed_seq = count_by_ext(processed_files, SEQ_EXT)

        has_pdf = raw_pdf > 0
        has_supp = (raw_table + raw_archive + raw_seq) > 0
        has_gene_like = (raw_table + raw_seq + processed_table + processed_seq) > 0

        missing = []
        if not has_pdf:
            missing.append("pdf")
        if not has_supp:
            missing.append("supplement")
        if not has_gene_like:
            missing.append("gene_or_variant_data")

        rows.append(
            [
                seq,
                slug,
                str(raw_pdf),
                str(raw_table),
                str(raw_seq),
                str(raw_archive),
                str(processed_table),
                str(processed_seq),
                "yes" if has_pdf else "no",
                "yes" if has_supp else "no",
                "yes" if has_gene_like else "no",
                ";".join(missing),
            ]
        )

    with output.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "seq",
                "paper_slug",
                "raw_pdf_count",
                "raw_table_count",
                "raw_sequence_count",
                "raw_archive_count",
                "processed_table_count",
                "processed_sequence_count",
                "has_pdf",
                "has_supplement",
                "has_gene_or_variant_data",
                "missing",
            ]
        )
        w.writerows(rows)

    total = len(rows)
    missing_pdf = sum(1 for r in rows if r[8] == "no")
    missing_supp = sum(1 for r in rows if r[9] == "no")
    missing_gene = sum(1 for r in rows if r[10] == "no")

    print(f"total_papers={total}")
    print(f"missing_pdf={missing_pdf}")
    print(f"missing_supplement={missing_supp}")
    print(f"missing_gene_or_variant_data={missing_gene}")
    print(f"report={output}")


if __name__ == "__main__":
    main()
