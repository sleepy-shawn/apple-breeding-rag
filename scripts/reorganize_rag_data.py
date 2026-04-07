#!/usr/bin/env python3
"""Reorganize rag原数据 by moving files from ALL/* into papers/*/raw.

Rules:
- Preferred mapping: ALL child folder name == 原始数据文件名 in checklist.
- Fallback mapping: leading number in ALL folder name maps to seq in papers.
- Unmapped folders go to papers_unmapped/<folder>/raw.

Usage:
  python scripts/reorganize_rag_data.py \
    --root "/Users/shuaige/code/rag原数据" \
    --checklist "/Users/shuaige/code/rag原数据/download_checklist.tsv"
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout


def detect_delimiter(path: Path) -> str:
    return "\t" if path.suffix.lower() == ".tsv" else ","


def load_checklist(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=detect_delimiter(path)))


def load_paper_dirs(papers_root: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for d in papers_root.iterdir():
        if not d.is_dir():
            continue
        m = re.match(r"^(\d{3})_", d.name)
        if m:
            out[m.group(1)] = d
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def main() -> None:
    p = argparse.ArgumentParser(description="Move ALL data into papers/*/raw")
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    p.add_argument("--root")
    p.add_argument("--checklist")
    p.add_argument("--copy", action="store_true", help="Copy instead of move")
    args = p.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    root = Path(args.root).resolve() if args.root else layout.workspace_root
    checklist_path = Path(args.checklist).resolve() if args.checklist else layout.checklist_file
    legacy_all_root = root / "ALL"
    modern_all_root = root / "source" / "ALL"
    all_root = legacy_all_root if legacy_all_root.exists() else modern_all_root
    papers_root = layout.papers_root if not (root / "papers").exists() else root / "papers"
    unmapped_root = root / "source" / "papers_unmapped"

    if not all_root.exists():
        raise FileNotFoundError(f"Missing folder: {all_root}")
    if not papers_root.exists():
        raise FileNotFoundError(f"Missing folder: {papers_root}")

    rows = load_checklist(checklist_path)
    by_raw_name: dict[str, str] = {}
    for row in rows:
        seq = (row.get("序号") or "").strip()
        raw_name = (row.get("原始数据文件名") or "").strip()
        if not seq:
            continue
        seq3 = seq.zfill(3)
        if raw_name:
            by_raw_name[norm(raw_name)] = seq3

    paper_dirs = load_paper_dirs(papers_root)

    moved_files = 0
    mapped_folders = 0
    unmapped_folders = 0

    for src_dir in sorted(all_root.iterdir()):
        if not src_dir.is_dir():
            continue

        seq3 = by_raw_name.get(norm(src_dir.name), "")
        if not seq3:
            m = re.match(r"^(\d+)", src_dir.name)
            if m:
                seq3_candidate = m.group(1).zfill(3)
                if seq3_candidate in paper_dirs:
                    seq3 = seq3_candidate

        if seq3 and seq3 in paper_dirs:
            dst_raw = paper_dirs[seq3] / "raw"
            mapped_folders += 1
        else:
            dst_raw = unmapped_root / src_dir.name / "raw"
            unmapped_folders += 1

        dst_raw.mkdir(parents=True, exist_ok=True)

        for item in sorted(src_dir.iterdir()):
            if item.name == ".DS_Store":
                continue
            dst = dst_raw / item.name
            # Avoid overwrite: append numeric suffix
            if dst.exists():
                stem = dst.stem
                suffix = dst.suffix
                i = 2
                while True:
                    alt = dst_raw / f"{stem}_{i}{suffix}"
                    if not alt.exists():
                        dst = alt
                        break
                    i += 1

            if args.copy:
                if item.is_dir():
                    shutil.copytree(item, dst)
                else:
                    shutil.copy2(item, dst)
            else:
                shutil.move(str(item), str(dst))
            moved_files += 1

        # Clean emptied source directory when move mode
        if not args.copy:
            try:
                src_dir.rmdir()
            except OSError:
                pass

    print(f"mapped_folders={mapped_folders}")
    print(f"unmapped_folders={unmapped_folders}")
    print(f"transferred_items={moved_files}")
    print(f"unmapped_root={unmapped_root}")


if __name__ == "__main__":
    main()
