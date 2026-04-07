#!/usr/bin/env python3
"""Initialize the default workspace folders for automated pipelines."""

from __future__ import annotations

import argparse
from pathlib import Path

from lib.pipeline_layout import DEFAULT_CONFIG_PATH, ensure_pipeline_dirs, load_pipeline_layout, layout_summary


README_TEXT = """# Pipeline Workspace

This directory stores automation-oriented assets and intermediate data.

Recommended flow:
1. Put raw paper fetch outputs under `source/` when they are not yet curated.
2. Normalize curated per-paper folders under `library/papers/`.
3. Save manifests under `manifests/`.
4. Save evaluation sets and run outputs under `evaluation/` and `reports/`.
5. Stage ingest-ready files into `backend/data/` via the provided scripts.
"""


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize pipeline workspace directories")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Pipeline config TOML path")
    args = parser.parse_args()

    layout = load_pipeline_layout(args.config)
    ensure_pipeline_dirs(layout)

    write_if_missing(layout.workspace_root / "README.md", README_TEXT)
    write_if_missing(layout.evaluation_dir / ".gitkeep", "")
    write_if_missing(layout.reports_dir / ".gitkeep", "")
    write_if_missing(layout.manifests_dir / ".gitkeep", "")
    write_if_missing(layout.source_papers_dir / ".gitkeep", "")
    write_if_missing(layout.papers_root / ".gitkeep", "")

    print("workspace_initialized=yes")
    print(layout_summary(layout))


if __name__ == "__main__":
    main()
