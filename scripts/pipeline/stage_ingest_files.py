#!/usr/bin/env python3
"""Stage ingest files into backend/data from ingest_manifest.csv.

- Copy PDF files to backend/data/papers
- Copy gene candidate files to backend/data/genes/raw_candidates
- Write a manifest of copied files for traceability

Usage:
  python scripts/pipeline/stage_ingest_files.py \
    --manifest "/Users/shuaige/code/rag原数据/ingest_manifest.csv" \
    --papers-out "/Users/shuaige/code/apple-breeding-rag/backend/data/papers" \
    --genes-out "/Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates" \
    --report "/Users/shuaige/code/apple-breeding-rag/backend/data/staged_manifest.csv"
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout


def split_paths(value: str) -> list[Path]:
    if not value:
        return []
    parts = [p.strip() for p in value.split("|") if p.strip()]
    return [Path(p) for p in parts]


def safe_name(seq: str, slug: str, src: Path, idx: int) -> str:
    suffix = "".join(src.suffixes) if src.suffixes else ""
    stem = src.name
    if suffix:
        stem = src.name[: -len(suffix)]
    return f"{seq}_{slug}_{idx:03d}_{stem}{suffix}"


def copy_unique(src: Path, dst_dir: Path, preferred_name: str) -> Path:
    dst = dst_dir / preferred_name
    if not dst.exists():
        shutil.copy2(src, dst)
        return dst

    i = 2
    while True:
        alt = dst_dir / f"{dst.stem}_{i}{dst.suffix}"
        if not alt.exists():
            shutil.copy2(src, alt)
            return alt
        i += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage files from ingest manifest")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    parser.add_argument("--manifest")
    parser.add_argument("--papers-out")
    parser.add_argument("--genes-out")
    parser.add_argument("--report")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    manifest_path = Path(args.manifest).resolve() if args.manifest else layout.ingest_manifest_file
    papers_out = Path(args.papers_out).resolve() if args.papers_out else layout.backend_papers_dir
    genes_out = Path(args.genes_out).resolve() if args.genes_out else layout.backend_genes_raw_dir
    report = Path(args.report).resolve() if args.report else layout.staged_manifest_file

    papers_out.mkdir(parents=True, exist_ok=True)
    genes_out.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows: list[list[str]] = []
    copied_papers = 0
    copied_genes = 0

    for row in rows:
        seq = (row.get("seq") or "").strip() or "000"
        slug = (row.get("paper_slug") or "paper").strip().replace(" ", "_")

        pdf_files = split_paths((row.get("paper_pdf_files") or "").strip())
        gene_files = split_paths((row.get("gene_candidate_files") or "").strip())

        for i, src in enumerate(pdf_files, start=1):
            if not src.exists() or not src.is_file():
                out_rows.append([seq, slug, "paper", str(src), "", "missing_source"])
                continue
            name = safe_name(seq, slug, src, i)
            dst = copy_unique(src, papers_out, name)
            copied_papers += 1
            out_rows.append([seq, slug, "paper", str(src), str(dst), "copied"])

        for i, src in enumerate(gene_files, start=1):
            if not src.exists() or not src.is_file():
                out_rows.append([seq, slug, "gene", str(src), "", "missing_source"])
                continue
            name = safe_name(seq, slug, src, i)
            dst = copy_unique(src, genes_out, name)
            copied_genes += 1
            out_rows.append([seq, slug, "gene", str(src), str(dst), "copied"])

    with report.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seq", "paper_slug", "kind", "source_path", "staged_path", "status"])
        w.writerows(out_rows)

    print(f"copied_paper_files={copied_papers}")
    print(f"copied_gene_files={copied_genes}")
    print(f"report={report}")


if __name__ == "__main__":
    main()
