from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


CONFIG_ORDER = ["A0", "A1", "A2", "A3"]
TRAIT_ORDER = ["firmness", "color", "acidity", "harvest", "sugar", "general"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate paper-ready markdown tables from judged ablation results")
    parser.add_argument("--input", required=True, help="Judged CSV produced by llm_judge.py")
    parser.add_argument(
        "--output-dir",
        default="",
        help="Optional output directory; defaults to the input file directory",
    )
    parser.add_argument(
        "--hybrid-config",
        default="A3",
        help="Config id treated as the full system for trait detail reporting",
    )
    return parser.parse_args()


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def format_number(value: float) -> str:
    text = f"{value:.2f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def average(rows: list[dict[str, str]], field: str) -> float:
    values = [safe_float(row.get(field, "0")) for row in rows]
    return sum(values) / max(1, len(values))


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sort_key_for_config(config_id: str) -> tuple[int, str]:
    if config_id in CONFIG_ORDER:
        return (CONFIG_ORDER.index(config_id), config_id)
    return (len(CONFIG_ORDER), config_id)


def sort_key_for_trait(trait: str) -> tuple[int, str]:
    if trait in TRAIT_ORDER:
        return (TRAIT_ORDER.index(trait), trait)
    return (len(TRAIT_ORDER), trait)


def build_config_summary(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    names: dict[str, str] = {}
    for row in rows:
        config_id = row.get("config_id", "")
        grouped.setdefault(config_id, []).append(row)
        names[config_id] = row.get("config_name", config_id)

    summaries: list[dict[str, Any]] = []
    for config_id in sorted(grouped, key=sort_key_for_config):
        config_rows = grouped[config_id]
        summaries.append(
            {
                "config_id": config_id,
                "config_name": names.get(config_id, config_id),
                "question_count": len(config_rows),
                "gene_score_avg": average(config_rows, "gene_score"),
                "mechanism_score_avg": average(config_rows, "mechanism_score_auto"),
                "citation_score_avg": average(config_rows, "citation_score"),
                "level_score_avg": average(config_rows, "level_score"),
                "full_total_avg": average(config_rows, "full_total"),
                "error_count": sum(safe_int(row.get("has_error", "0")) for row in config_rows),
            }
        )
    return summaries


def build_trait_summary(rows: list[dict[str, str]], hybrid_config: str) -> list[dict[str, Any]]:
    hybrid_rows = [row for row in rows if row.get("config_id") == hybrid_config]
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in hybrid_rows:
        grouped.setdefault(row.get("trait", "unknown"), []).append(row)

    summaries: list[dict[str, Any]] = []
    for trait in sorted(grouped, key=sort_key_for_trait):
        trait_rows = grouped[trait]
        rows_with_genes = [row for row in trait_rows if safe_int(row.get("gene_expected_count", "0")) > 0]
        gene_recall = None
        if rows_with_genes:
            gene_recall = sum(safe_float(row.get("gene_hit_ratio", "0")) for row in rows_with_genes) / len(rows_with_genes)

        summaries.append(
            {
                "trait": trait,
                "question_count": len(trait_rows),
                "avg_total": average(trait_rows, "full_total"),
                "gene_recall_rate": gene_recall,
            }
        )
    return summaries


def bold_if_best(label: str, value: float, best_value: float) -> str:
    formatted = format_number(value)
    if abs(value - best_value) < 1e-9:
        return f"**{formatted}**"
    return formatted


def build_ablation_table(config_summaries: list[dict[str, Any]], question_count: int) -> str:
    if not config_summaries:
        return ""

    best_gene = max(item["gene_score_avg"] for item in config_summaries)
    best_mechanism = max(item["mechanism_score_avg"] for item in config_summaries)
    best_citation = max(item["citation_score_avg"] for item in config_summaries)
    best_level = max(item["level_score_avg"] for item in config_summaries)
    best_total = max(item["full_total_avg"] for item in config_summaries)

    lines = [
        f"## 消融实验结果（{question_count}题，满分10分）",
        "",
        "| 配置 | 基因召回(4) | 机制准确(3) | 引用质量(2) | 证据分级(1) | **总分(10)** |",
        "|------|------------|------------|------------|------------|-------------|",
    ]

    for item in config_summaries:
        name = item["config_name"]
        if item["config_id"] == "A3":
            name = f"**{name}**"
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    bold_if_best("gene", item["gene_score_avg"], best_gene),
                    bold_if_best("mechanism", item["mechanism_score_avg"], best_mechanism),
                    bold_if_best("citation", item["citation_score_avg"], best_citation),
                    bold_if_best("level", item["level_score_avg"], best_level),
                    f"**{format_number(item['full_total_avg'])}**" if abs(item["full_total_avg"] - best_total) < 1e-9 else format_number(item["full_total_avg"]),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def build_trait_table(trait_summaries: list[dict[str, Any]], hybrid_name: str) -> str:
    lines = [
        f"## 各性状表现（{hybrid_name}配置，满分10分）",
        "",
        "| 性状 | 题数 | 总分均值 | 基因召回率 |",
        "|------|------|---------|-----------|",
    ]

    for item in trait_summaries:
        gene_recall = item["gene_recall_rate"]
        gene_text = "—" if gene_recall is None else f"{round(gene_recall * 100):.0f}%"
        trait_label = item["trait"].capitalize()
        lines.append(
            f"| {trait_label} | {item['question_count']} | {format_number(item['avg_total'])} | {gene_text} |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    rows = load_rows(input_path)
    if not rows:
        raise SystemExit("Input CSV is empty")

    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    config_summaries = build_config_summary(rows)
    trait_summaries = build_trait_summary(rows, hybrid_config=args.hybrid_config)
    question_count = len({row.get("id", "") for row in rows if row.get("id")})

    hybrid_name = args.hybrid_config
    for item in config_summaries:
        if item["config_id"] == args.hybrid_config:
            hybrid_name = item["config_name"]
            break

    summary_payload = {
        "question_count": question_count,
        "config_summaries": config_summaries,
        "trait_summaries": trait_summaries,
        "input_file": str(input_path),
    }

    summary_json = output_dir / "ablation_summary.json"
    ablation_md = output_dir / "ablation_table.md"
    trait_md = output_dir / "trait_detail_table.md"

    summary_json.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    ablation_md.write_text(build_ablation_table(config_summaries, question_count), encoding="utf-8")
    trait_md.write_text(build_trait_table(trait_summaries, hybrid_name), encoding="utf-8")

    print(f"Saved summary JSON to: {summary_json}")
    print(f"Saved Markdown table to: {ablation_md}")
    print(f"Saved trait detail table to: {trait_md}")


if __name__ == "__main__":
    main()
