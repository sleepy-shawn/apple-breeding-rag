#!/usr/bin/env python3
"""Build ingest manifest from papers/* structure.

Outputs one CSV with per-paper ingest readiness and candidate files.

Usage:
  python scripts/pipeline/build_ingest_manifest.py \
    --papers-root "/Users/shuaige/code/rag原数据/papers" \
    --output "/Users/shuaige/code/rag原数据/ingest_manifest.csv"
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout

PDF_EXT = {".pdf"}
TABLE_EXT = {".xls", ".xlsx", ".csv", ".tsv"}
SEQ_EXT = {".fasta", ".fa", ".fna", ".fastq", ".fq", ".vcf", ".vcf.gz", ".gff", ".gff3", ".bed", ".bam", ".sam", ".nex"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz"}


def ext_of(path: Path) -> str:
    name = path.name.lower()
    if name.endswith(".vcf.gz"):
        return ".vcf.gz"
    return path.suffix.lower()


def iter_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store"]


def looks_like_data_file(path: Path) -> bool:
    e = ext_of(path)
    if e in TABLE_EXT or e in SEQ_EXT:
        return True
    low = path.name.lower()
    keywords = ["supp", "table", "variant", "snp", "indel", "marker", "gen", "qtl", "locus"]
    return any(k in low for k in keywords)


def is_archive(path: Path) -> bool:
    return ext_of(path) in ARCHIVE_EXT


def main() -> None:
    parser = argparse.ArgumentParser(description="Build per-paper ingest manifest")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    parser.add_argument("--papers-root")
    parser.add_argument("--output")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    papers_root = Path(args.papers_root).resolve() if args.papers_root else layout.papers_root
    output = Path(args.output).resolve() if args.output else layout.ingest_manifest_file
    output.parent.mkdir(parents=True, exist_ok=True)

    rows: list[list[str]] = []

    for paper_dir in sorted(p for p in papers_root.iterdir() if p.is_dir()):
        m = re.match(r"^(\d{3})_(.+)$", paper_dir.name)
        seq = m.group(1) if m else ""
        slug = m.group(2) if m else paper_dir.name

        raw_dir = paper_dir / "raw"
        files = iter_files(raw_dir) if raw_dir.exists() else []

        pdfs = [p for p in files if ext_of(p) in PDF_EXT]
        data_candidates = [p for p in files if looks_like_data_file(p) and ext_of(p) != ".pdf"]
        archives = [p for p in files if is_archive(p)]

        pdf_ready = "yes" if pdfs else "no"
        genes_ready = "yes" if data_candidates else "no"

        note_parts = []
        if not pdfs:
            note_parts.append("missing_pdf")
        if not data_candidates:
            if archives:
                note_parts.append("only_archive_found_extract_needed")
            else:
                note_parts.append("no_gene_or_variant_candidates")

        rows.append(
            [
                seq,
                slug,
                str(paper_dir),
                "yes",  # papers ingestion always true for existing paper dirs
                pdf_ready,
                "|".join(str(p) for p in sorted(pdfs)),
                genes_ready,
                "|".join(str(p) for p in sorted(data_candidates)),
                str(len(archives)),
                "|".join(str(p) for p in sorted(archives)),
                ";".join(note_parts),
            ]
        )

    with output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "seq",
                "paper_slug",
                "paper_dir",
                "ingest_papers_enabled",
                "paper_pdf_ready",
                "paper_pdf_files",
                "ingest_genes_enabled",
                "gene_candidate_files",
                "archive_count",
                "archive_files",
                "notes",
            ]
        )
        writer.writerows(rows)

    total = len(rows)
    genes_yes = sum(1 for r in rows if r[6] == "yes")
    pdf_yes = sum(1 for r in rows if r[4] == "yes")
    archives_only = sum(1 for r in rows if "only_archive_found_extract_needed" in r[10])

    print(f"total_papers={total}")
    print(f"paper_pdf_ready={pdf_yes}")
    print(f"ingest_genes_enabled={genes_yes}")
    print(f"archives_only={archives_only}")
    print(f"manifest={output}")


if __name__ == "__main__":
    main()
