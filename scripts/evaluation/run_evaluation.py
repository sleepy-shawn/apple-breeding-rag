"""
RAG系统标准评估脚本

用法:
    python scripts/evaluation/run_evaluation.py \
        --test-file workspace/default/evaluation/test_questions.jsonl \
        --api-url http://localhost:8000/api/chat \
        --output-dir workspace/default/evaluation/runs/baseline_current
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


def query_rag(api_url: str, question: str, route: str = "auto", top_k: int = 6) -> dict[str, Any]:
    try:
        resp = requests.post(
            api_url,
            json={"question": question, "route": route, "top_k": top_k},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"error": str(exc), "answer": "", "sources": []}


def score_answer(question_data: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    answer = (response.get("answer") or "").lower()
    sources = response.get("sources") or []

    expected_genes = question_data.get("expected_genes") or []
    if expected_genes:
        hit = sum(1 for g in expected_genes if g.lower() in answer)
        ratio = hit / len(expected_genes)
        gene_score = round(ratio * 4)
    else:
        hit = 0
        ratio = 1.0
        gene_score = 4

    citations = re.findall(r"\[\d+\]", answer)
    citation_score = 2 if len(citations) >= 2 else (1 if citations else 0)

    has_level_a = "level a" in answer or "直接证据" in answer or "level_a" in answer
    has_level_b = "level b" in answer or "间接证据" in answer or "level_b" in answer
    level_score = 1 if (has_level_a and has_level_b) else 0

    source_count = len(sources)
    route_used = response.get("route_used", "")
    api_error = response.get("error", "")

    total = gene_score + citation_score + level_score
    mechanism_score_placeholder = 2

    return {
        "gene_score": gene_score,
        "citation_score": citation_score,
        "level_score": level_score,
        "mechanism_score": mechanism_score_placeholder,
        "auto_total": total,
        "full_total": total + mechanism_score_placeholder,
        "source_count": source_count,
        "gene_hit_count": hit,
        "gene_expected_count": len(expected_genes),
        "gene_hit_ratio": round(ratio, 2),
        "route_used": route_used,
        "has_error": bool(api_error),
    }


def build_run_manifest(args: argparse.Namespace, question_count: int) -> dict[str, Any]:
    env_keys = [
        "EMBEDDING_MODEL",
        "LLM_MODEL",
        "LLM_BASE_URL",
        "AUTO_INGEST_ON_STARTUP",
    ]
    env_snapshot = {key: os.getenv(key, "") for key in env_keys}
    return {
        "run_name": args.run_name,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "api_url": args.api_url,
        "route": args.route,
        "top_k": args.top_k,
        "sleep": args.sleep,
        "test_file": args.test_file,
        "question_count": question_count,
        "notes": args.notes,
        "env": env_snapshot,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")


def write_results_csv(path: Path, results: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "trait",
                "question",
                "route_used",
                "source_count",
                "gene_score",
                "citation_score",
                "level_score",
                "mechanism_score_manual",
                "auto_total",
                "full_total",
                "teacher_score_adjusted",
                "teacher_notes",
                "error",
            ]
        )
        for item in results:
            scores = item["scores"]
            writer.writerow(
                [
                    item["id"],
                    item["trait"],
                    item["question"],
                    item.get("route_used", ""),
                    scores["source_count"],
                    scores["gene_score"],
                    scores["citation_score"],
                    scores["level_score"],
                    "",
                    scores["auto_total"],
                    scores["full_total"],
                    "",
                    "",
                    item.get("error", ""),
                ]
            )


def write_manual_review_csv(path: Path, results: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "trait",
                "question",
                "expected_genes",
                "expected_mechanism",
                "answer",
                "source_titles",
                "gene_score_auto",
                "citation_score_auto",
                "level_score_auto",
                "mechanism_score_manual",
                "teacher_overall_label",
                "teacher_notes",
            ]
        )
        for item in results:
            source_titles = " | ".join(
                str(s.get("title") or s.get("source_type") or "")
                for s in item.get("sources", [])
            )
            writer.writerow(
                [
                    item["id"],
                    item["trait"],
                    item["question"],
                    ",".join(item.get("expected_genes", [])),
                    item.get("expected_mechanism", ""),
                    item.get("answer", ""),
                    source_titles,
                    item["scores"]["gene_score"],
                    item["scores"]["citation_score"],
                    item["scores"]["level_score"],
                    "",
                    "",
                    "",
                ]
            )


def build_summary(results: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    trait_scores: dict[str, list[float]] = {}
    trait_gene_ratio: dict[str, list[float]] = {}
    route_counts: dict[str, int] = {}
    error_count = 0

    for item in results:
        trait = item["trait"]
        scores = item["scores"]
        trait_scores.setdefault(trait, []).append(scores["full_total"])
        trait_gene_ratio.setdefault(trait, []).append(scores["gene_hit_ratio"])
        route = scores.get("route_used") or item.get("route_used") or "unknown"
        route_counts[route] = route_counts.get(route, 0) + 1
        if item.get("error"):
            error_count += 1

    totals = [item["scores"]["full_total"] for item in results]
    citation_rate = sum(1 for item in results if item["scores"]["citation_score"] >= 1) / max(1, len(results))
    level_rate = sum(1 for item in results if item["scores"]["level_score"] == 1) / max(1, len(results))
    retrieval_hit_rate = sum(1 for item in results if item["scores"]["source_count"] > 0) / max(1, len(results))

    by_trait = {
        trait: {
            "avg_total": round(sum(scores) / len(scores), 2),
            "avg_gene_hit_ratio": round(sum(trait_gene_ratio[trait]) / len(trait_gene_ratio[trait]), 2),
            "count": len(scores),
        }
        for trait, scores in sorted(trait_scores.items())
    }

    return {
        "manifest": manifest,
        "overall": {
            "avg_total": round(sum(totals) / max(1, len(totals)), 2),
            "citation_rate": round(citation_rate, 2),
            "level_distinction_rate": round(level_rate, 2),
            "retrieval_hit_rate": round(retrieval_hit_rate, 2),
            "error_count": error_count,
        },
        "by_trait": by_trait,
        "route_counts": route_counts,
    }


def write_summary_markdown(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        f"# Evaluation Summary: {summary['manifest']['run_name']}",
        "",
        f"- Created at: `{summary['manifest']['created_at']}`",
        f"- API URL: `{summary['manifest']['api_url']}`",
        f"- Route: `{summary['manifest']['route']}`",
        f"- Top-k: `{summary['manifest']['top_k']}`",
        f"- Questions: `{summary['manifest']['question_count']}`",
        "",
        "## Overall",
        "",
        f"- Avg total: `{summary['overall']['avg_total']}/10`",
        f"- Retrieval hit rate: `{summary['overall']['retrieval_hit_rate']}`",
        f"- Citation rate: `{summary['overall']['citation_rate']}`",
        f"- Level distinction rate: `{summary['overall']['level_distinction_rate']}`",
        f"- Error count: `{summary['overall']['error_count']}`",
        "",
        "## By Trait",
        "",
        "| Trait | Avg Total | Avg Gene Hit Ratio | Count |",
        "|------|-----------|--------------------|-------|",
    ]
    for trait, info in summary["by_trait"].items():
        lines.append(f"| {trait} | {info['avg_total']} | {info['avg_gene_hit_ratio']} | {info['count']} |")

    lines.extend(
        [
            "",
            "## Route Counts",
            "",
        ]
    )
    for route, count in sorted(summary["route_counts"].items()):
        lines.append(f"- `{route}`: {count}")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG system on apple breeding test set")
    parser.add_argument(
        "--test-file",
        default="workspace/default/evaluation/test_questions.jsonl",
        help="Path to JSONL test file",
    )
    parser.add_argument("--api-url", default="http://localhost:8000/api/chat", help="RAG API endpoint")
    parser.add_argument(
        "--output-dir",
        default="workspace/default/evaluation/runs/baseline_current",
        help="Output directory for this evaluation run",
    )
    parser.add_argument("--run-name", default="baseline_current", help="Name of this run")
    parser.add_argument("--notes", default="", help="Optional notes recorded in run manifest")
    parser.add_argument("--route", default="auto", help="Route: auto|papers|genes|hybrid")
    parser.add_argument("--top-k", type=int, default=6, help="Top-k retrieval")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep between queries (seconds)")
    args = parser.parse_args()

    test_path = Path(args.test_file)
    if not test_path.exists():
        print(f"Test file not found: {test_path}")
        return

    questions = [json.loads(line) for line in test_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_run_manifest(args, len(questions))
    results: list[dict[str, Any]] = []

    print(f"Evaluating {len(questions)} questions against {args.api_url}\n")
    print(f"{'ID':<8} {'Trait':<12} {'Genes':<6} {'Cite':<5} {'Level':<6} {'Total':<6} Question")
    print("-" * 90)

    for q in questions:
        qid = q["id"]
        trait = q["trait"]
        question = q["question"]

        response = query_rag(args.api_url, question, route=args.route, top_k=args.top_k)
        scores = score_answer(q, response)

        result = {
            "id": qid,
            "trait": trait,
            "question": question,
            "expected_genes": q.get("expected_genes", []),
            "expected_mechanism": q.get("expected_mechanism", ""),
            "expected_evidence_type": q.get("evidence_type", ""),
            "answer": response.get("answer", ""),
            "route_used": response.get("route_used", ""),
            "error": response.get("error", ""),
            "scores": scores,
            "sources": [
                {
                    "source_type": s.get("source_type"),
                    "title": s.get("title"),
                    "score": s.get("score"),
                }
                for s in (response.get("sources") or [])
            ],
        }
        results.append(result)

        print(
            f"{qid:<8} {trait:<12} {scores['gene_score']}/4   {scores['citation_score']}/2  "
            f"{scores['level_score']}/1    {scores['full_total']}/10  {question[:50]}"
        )

        if args.sleep > 0:
            time.sleep(args.sleep)

    results_jsonl = output_dir / "results.jsonl"
    results_csv = output_dir / "results.csv"
    manual_review_csv = output_dir / "manual_review.csv"
    summary_json = output_dir / "summary.json"
    summary_md = output_dir / "summary.md"
    manifest_json = output_dir / "run_manifest.json"

    write_jsonl(results_jsonl, results)
    write_results_csv(results_csv, results)
    write_manual_review_csv(manual_review_csv, results)

    summary = build_summary(results, manifest)
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_markdown(summary_md, summary)
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 90)
    print("SUMMARY")
    print(f"  Overall average: {summary['overall']['avg_total']}/10")
    for trait, info in summary["by_trait"].items():
        print(f"  {trait:<15}: {info['avg_total']}/10 ({info['count']} questions)")
    print(f"  Retrieval hit rate: {summary['overall']['retrieval_hit_rate']}")
    print(f"  Citation rate: {summary['overall']['citation_rate']}")
    print(f"  Level distinction rate: {summary['overall']['level_distinction_rate']}")
    print(f"\nOutputs saved to: {output_dir}")
    print("Files:")
    print(f"  - {results_jsonl.name}")
    print(f"  - {results_csv.name}")
    print(f"  - {manual_review_csv.name}")
    print(f"  - {summary_json.name}")
    print(f"  - {summary_md.name}")
    print(f"  - {manifest_json.name}")
    print("NOTE: mechanism_score_manual remains blank in CSV for human review.")


if __name__ == "__main__":
    main()
