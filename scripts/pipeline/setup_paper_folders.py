#!/usr/bin/env python3
"""Create per-paper folder structure from a checklist CSV/TSV.

Example:
  python scripts/pipeline/setup_paper_folders.py \
    --input "/Users/shuaige/Documents/rag原数据/download_checklist.tsv" \
    --root "/Users/shuaige/Documents/rag原数据/papers"
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout


def slugify(text: str, limit: int = 40) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:limit] or "paper"


def detect_delimiter(path: Path) -> str:
    return "\t" if path.suffix.lower() == ".tsv" else ","


def read_rows(path: Path) -> list[dict[str, str]]:
    delimiter = detect_delimiter(path)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def pick_short_name(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    if not words:
        return "paper"
    return slugify("_".join(words[:6]))


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create paper folder scaffold from checklist")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    parser.add_argument("--input", help="Checklist CSV/TSV path")
    parser.add_argument("--root", help="Output root directory, e.g. .../papers")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    in_path = Path(args.input).resolve() if args.input else layout.checklist_file
    root = Path(args.root).resolve() if args.root else layout.papers_root
    root.mkdir(parents=True, exist_ok=True)

    rows = read_rows(in_path)
    created = 0

    for row in rows:
        seq = (row.get("序号") or "").strip()
        title = (row.get("文献题目") or "").strip()
        paper_url = (row.get("文献链接") or "").strip()
        pmid = (row.get("PMID") or "").strip()
        raw_name = (row.get("原始数据文件名") or "").strip()
        ref_genome = (row.get("参考基因组") or "").strip()

        if not seq or not title:
            continue

        folder_name = f"{seq.zfill(3)}_{pick_short_name(title)}"
        paper_dir = root / folder_name
        raw_dir = paper_dir / "raw"
        processed_dir = paper_dir / "processed"
        raw_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(exist_ok=True)

        metadata_path = paper_dir / "metadata.json"
        notes_path = paper_dir / "notes.md"

        if not metadata_path.exists():
            metadata = (
                "{\n"
                f'  "seq": "{seq.zfill(3)}",\n'
                f'  "title": {title!r},\n'
                f'  "pmid": {pmid!r},\n'
                '  "doi": "",\n'
                f'  "paper_url": {paper_url!r},\n'
                f'  "reference_genome": {ref_genome!r},\n'
                '  "data_source_url": "",\n'
                '  "status": {\n'
                '    "pdf": false,\n'
                '    "supplement": false,\n'
                '    "curated": false\n'
                '  }\n'
                '}\n'
            )
            write_text(metadata_path, metadata)

        if not notes_path.exists():
            notes = (
                f"# {title}\n\n"
                "## Summary\n"
                "- Main finding: \n"
                "- Useful supplement tables: \n"
                "- Candidate genes / loci: \n\n"
                "## Download Checklist\n"
                f"- PDF: raw/paper.pdf\n"
                f"- Original supplement filename hint: {raw_name or 'N/A'}\n"
                "- Data source URL: \n\n"
                "## Processing Notes\n"
                "- Keep original downloaded files under raw/\n"
                "- Save cleaned CSV files under processed/\n"
            )
            write_text(notes_path, notes)

        created += 1

    print(f"Prepared {created} paper folders under {root}")
    print(f"checklist={in_path}")


if __name__ == "__main__":
    main()
