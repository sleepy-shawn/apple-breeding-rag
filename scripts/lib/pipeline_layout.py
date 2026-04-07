#!/usr/bin/env python3
"""Shared project layout helpers for data pipelines."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = project_root()
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "pipeline.toml"

DEFAULT_TRAIT_QUERIES: dict[str, str] = {
    "color": '(apple OR "Malus domestica") AND (skin color OR fruit color OR anthocyanin OR pigmentation OR red flesh) AND (breeding OR QTL OR GWAS OR marker OR locus OR "candidate gene")',
    "acidity": '(apple OR "Malus domestica") AND (acidity OR malic acid OR titratable acidity) AND (breeding OR QTL OR GWAS OR marker OR locus OR "candidate gene")',
    "sugar": '(apple OR "Malus domestica") AND (sugar OR sucrose OR sorbitol OR soluble solids) AND (breeding OR QTL OR GWAS OR marker OR locus OR "candidate gene")',
    "disease": '(apple OR "Malus domestica") AND (disease resistance OR scab resistance OR powdery mildew OR Alternaria OR fire blight) AND (breeding OR QTL OR marker OR locus OR gene)',
    "maturity": '(apple OR "Malus domestica") AND (ripening OR maturity OR harvest date OR fruit development) AND (breeding OR QTL OR GWAS OR marker OR locus OR "candidate gene")',
    "firmness": '(apple OR "Malus domestica") AND (firmness OR texture OR crispness OR softening) AND (breeding OR QTL OR GWAS OR marker OR locus OR "candidate gene")',
}


@dataclass(frozen=True)
class PipelineLayout:
    project_root: Path
    workspace_root: Path
    checkpoints_dir: Path
    source_papers_dir: Path
    papers_root: Path
    manifests_dir: Path
    evaluation_dir: Path
    reports_dir: Path
    fetch_state_file: Path
    checklist_file: Path
    ingest_manifest_file: Path
    coverage_report_file: Path
    backend_papers_dir: Path
    backend_genes_raw_dir: Path
    staged_manifest_file: Path
    pipeline_config_path: Path
    min_year: int
    max_per_trait: int
    trait_queries: dict[str, str]


def _expand_path(value: str | None, default: Path) -> Path:
    if not value:
        return default
    path = Path(os.path.expanduser(value))
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def _deep_get(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _parse_toml_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        return value


def _parse_simple_toml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current: dict[str, Any] = data

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            current = data
            for part in section.split("."):
                current = current.setdefault(part, {})
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        current[key.strip()] = _parse_toml_scalar(value)
    return data


def load_pipeline_layout(config_path: str | Path | None = None) -> PipelineLayout:
    config_file = _expand_path(str(config_path), DEFAULT_CONFIG_PATH) if config_path else DEFAULT_CONFIG_PATH
    data: dict[str, Any] = {}
    if config_file.exists():
        content = config_file.read_text(encoding="utf-8")
        if tomllib is not None:
            data = tomllib.loads(content)
        else:
            data = _parse_simple_toml(content)

    workspace_root = _expand_path(
        _deep_get(data, "workspace", "root"),
        PROJECT_ROOT / "workspace" / "default",
    )
    checkpoints_dir = _expand_path(
        _deep_get(data, "workspace", "checkpoints_dir"),
        workspace_root / "state",
    )
    source_papers_dir = _expand_path(
        _deep_get(data, "workspace", "source_papers_dir"),
        workspace_root / "source" / "papers",
    )
    papers_root = _expand_path(
        _deep_get(data, "workspace", "papers_root"),
        workspace_root / "library" / "papers",
    )
    manifests_dir = _expand_path(
        _deep_get(data, "workspace", "manifests_dir"),
        workspace_root / "manifests",
    )
    evaluation_dir = _expand_path(
        _deep_get(data, "workspace", "evaluation_dir"),
        workspace_root / "evaluation",
    )
    reports_dir = _expand_path(
        _deep_get(data, "workspace", "reports_dir"),
        workspace_root / "reports",
    )

    fetch_state_file = _expand_path(
        _deep_get(data, "fetch", "state_file"),
        checkpoints_dir / "fetch" / "papers_meta.json",
    )
    checklist_file = _expand_path(
        _deep_get(data, "manifests", "checklist_file"),
        manifests_dir / "download_checklist.tsv",
    )
    ingest_manifest_file = _expand_path(
        _deep_get(data, "manifests", "ingest_manifest_file"),
        manifests_dir / "ingest_manifest.csv",
    )
    coverage_report_file = _expand_path(
        _deep_get(data, "manifests", "coverage_report_file"),
        reports_dir / "coverage_report.csv",
    )
    backend_papers_dir = _expand_path(
        _deep_get(data, "staging", "backend_papers_dir"),
        PROJECT_ROOT / "backend" / "data" / "papers",
    )
    backend_genes_raw_dir = _expand_path(
        _deep_get(data, "staging", "backend_genes_raw_dir"),
        PROJECT_ROOT / "backend" / "data" / "genes" / "raw_candidates",
    )
    staged_manifest_file = _expand_path(
        _deep_get(data, "staging", "staged_manifest_file"),
        PROJECT_ROOT / "backend" / "data" / "staged_manifest.csv",
    )

    min_year = int(_deep_get(data, "fetch", "min_year") or 2014)
    max_per_trait = int(_deep_get(data, "fetch", "max_per_trait") or 20)
    trait_queries = _deep_get(data, "fetch", "trait_queries") or DEFAULT_TRAIT_QUERIES

    return PipelineLayout(
        project_root=PROJECT_ROOT,
        workspace_root=workspace_root,
        checkpoints_dir=checkpoints_dir,
        source_papers_dir=source_papers_dir,
        papers_root=papers_root,
        manifests_dir=manifests_dir,
        evaluation_dir=evaluation_dir,
        reports_dir=reports_dir,
        fetch_state_file=fetch_state_file,
        checklist_file=checklist_file,
        ingest_manifest_file=ingest_manifest_file,
        coverage_report_file=coverage_report_file,
        backend_papers_dir=backend_papers_dir,
        backend_genes_raw_dir=backend_genes_raw_dir,
        staged_manifest_file=staged_manifest_file,
        pipeline_config_path=config_file,
        min_year=min_year,
        max_per_trait=max_per_trait,
        trait_queries=dict(trait_queries),
    )


def ensure_pipeline_dirs(layout: PipelineLayout) -> list[Path]:
    directories = [
        layout.workspace_root,
        layout.checkpoints_dir,
        layout.source_papers_dir,
        layout.papers_root,
        layout.manifests_dir,
        layout.evaluation_dir,
        layout.reports_dir,
        layout.fetch_state_file.parent,
        layout.backend_papers_dir,
        layout.backend_genes_raw_dir,
        layout.staged_manifest_file.parent,
    ]
    for path in directories:
        path.mkdir(parents=True, exist_ok=True)
    return directories


def layout_summary(layout: PipelineLayout) -> str:
    payload = {
        "project_root": str(layout.project_root),
        "workspace_root": str(layout.workspace_root),
        "papers_root": str(layout.papers_root),
        "checklist_file": str(layout.checklist_file),
        "ingest_manifest_file": str(layout.ingest_manifest_file),
        "fetch_state_file": str(layout.fetch_state_file),
        "backend_papers_dir": str(layout.backend_papers_dir),
        "backend_genes_raw_dir": str(layout.backend_genes_raw_dir),
        "staged_manifest_file": str(layout.staged_manifest_file),
        "evaluation_dir": str(layout.evaluation_dir),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
