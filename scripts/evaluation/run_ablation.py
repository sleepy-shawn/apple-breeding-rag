from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from run_evaluation import score_answer


CONFIGS: list[dict[str, Any]] = [
    {
        "config_id": "A0",
        "config_name": "No-RAG",
        "mode": "no_rag",
        "route": "",
    },
    {
        "config_id": "A1",
        "config_name": "Papers-only",
        "mode": "rag",
        "route": "papers",
    },
    {
        "config_id": "A2",
        "config_name": "Genes-only",
        "mode": "rag",
        "route": "genes",
    },
    {
        "config_id": "A3",
        "config_name": "Hybrid（完整系统）",
        "mode": "rag",
        "route": "hybrid",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ablation study for apple breeding RAG evaluation")
    parser.add_argument(
        "--test-file",
        default="workspace/default/evaluation/test_questions.jsonl",
        help="Path to JSONL test file",
    )
    parser.add_argument("--api-url", default="http://localhost:8000/api/chat", help="RAG API endpoint")
    parser.add_argument(
        "--output",
        default="workspace/default/evaluation/ablation",
        help="Output directory for ablation results",
    )
    parser.add_argument("--top-k", type=int, default=6, help="Top-k retrieval for RAG configs")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for smoke testing")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep between calls in seconds")
    parser.add_argument(
        "--env-file",
        default="backend/.env",
        help="Path to .env file containing LLM_API_KEY / LLM_BASE_URL / LLM_MODEL",
    )
    parser.add_argument("--model", default="", help="Optional model override for A0 / backend generation")
    parser.add_argument(
        "--configs",
        default="A0,A1,A2,A3",
        help="Comma-separated config ids to run, e.g. A1,A2,A3",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def resolve_llm_config(env_file: Path, model_override: str) -> dict[str, str]:
    env = load_env_file(env_file)
    api_key = os.getenv("LLM_API_KEY", env.get("LLM_API_KEY", ""))
    base_url = os.getenv("LLM_BASE_URL", env.get("LLM_BASE_URL", "https://api.deepseek.com"))
    model = model_override or os.getenv("LLM_MODEL", env.get("LLM_MODEL", "deepseek-chat"))

    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
    }


def load_questions(path: Path, limit: int = 0) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Test file not found: {path}")

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if limit > 0:
        return rows[:limit]
    return rows


def query_rag(
    api_url: str,
    question: str,
    route: str,
    top_k: int,
    llm_config: dict[str, str],
) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = {
            "question": question,
            "route": route,
            "top_k": top_k,
        }
        if llm_config.get("api_key"):
            payload.update(
                {
                    "llm_api_key": llm_config["api_key"],
                    "llm_base_url": llm_config["base_url"],
                    "llm_model": llm_config["model"],
                }
            )
        response = requests.post(
            api_url,
            json=payload,
            timeout=90,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {
            "answer": "",
            "route_used": route,
            "sources": [],
            "error": str(exc),
        }


def create_openai_client(llm_config: dict[str, str]) -> Any:
    if OpenAI is None:
        return None
    return OpenAI(
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"],
        timeout=90.0,
    )


def llm_chat_completion(
    llm_config: dict[str, str],
    messages: list[dict[str, str]],
    temperature: float,
    client: Any = None,
) -> str:
    if client is not None:
        response = client.chat.completions.create(
            model=llm_config["model"],
            temperature=temperature,
            messages=messages,
        )
        return response.choices[0].message.content or ""

    response = requests.post(
        f"{llm_config['base_url'].rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {llm_config['api_key']}",
            "Content-Type": "application/json",
        },
        json={
            "model": llm_config["model"],
            "temperature": temperature,
            "messages": messages,
        },
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def query_no_rag(client: Any, question: str, llm_config: dict[str, str]) -> dict[str, Any]:
    prompt = f"你是苹果遗传育种助手。请直接根据你的知识回答以下问题，不要使用任何外部工具。\n问题：{question}"
    try:
        if not llm_config.get("api_key"):
            raise RuntimeError("LLM_API_KEY is required for A0 No-RAG mode")
        answer = llm_chat_completion(
            llm_config=llm_config,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            client=client,
        )
        return {
            "answer": answer,
            "route_used": "no_rag",
            "sources": [],
            "error": "",
        }
    except Exception as exc:
        return {
            "answer": "",
            "route_used": "no_rag",
            "sources": [],
            "error": str(exc),
        }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")


def source_titles(response: dict[str, Any]) -> str:
    titles = []
    for source in response.get("sources") or []:
        title = source.get("title") or source.get("source_type") or source.get("source_id") or ""
        if title:
            titles.append(str(title))
    return " | ".join(titles)


def build_row(
    config: dict[str, Any],
    question: dict[str, Any],
    response: dict[str, Any],
    scores: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    return {
        "config_id": config["config_id"],
        "config_name": config["config_name"],
        "id": question["id"],
        "trait": question["trait"],
        "question": question["question"],
        "expected_genes": json.dumps(question.get("expected_genes", []), ensure_ascii=False),
        "expected_mechanism": question.get("expected_mechanism", ""),
        "evidence_type": question.get("evidence_type", ""),
        "route": config.get("route", ""),
        "route_used": response.get("route_used", ""),
        "top_k": top_k,
        "answer": response.get("answer", ""),
        "source_count": scores.get("source_count", 0),
        "source_titles": source_titles(response),
        "gene_score": scores["gene_score"],
        "citation_score": scores["citation_score"],
        "level_score": scores["level_score"],
        "mechanism_score_manual": "",
        "mechanism_score_auto": "",
        "judge_reason": "",
        "auto_total": scores["auto_total"],
        "full_total": "",
        "gene_hit_count": scores["gene_hit_count"],
        "gene_expected_count": scores["gene_expected_count"],
        "gene_hit_ratio": scores["gene_hit_ratio"],
        "has_error": int(bool(response.get("error"))),
        "error": response.get("error", ""),
    }


def write_results_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "config_id",
        "config_name",
        "id",
        "trait",
        "question",
        "expected_genes",
        "expected_mechanism",
        "evidence_type",
        "route",
        "route_used",
        "top_k",
        "answer",
        "source_count",
        "source_titles",
        "gene_score",
        "citation_score",
        "level_score",
        "mechanism_score_manual",
        "mechanism_score_auto",
        "judge_reason",
        "auto_total",
        "full_total",
        "gene_hit_count",
        "gene_expected_count",
        "gene_hit_ratio",
        "has_error",
        "error",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_manifest(args: argparse.Namespace, question_count: int, llm_config: dict[str, str]) -> dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "api_url": args.api_url,
        "test_file": args.test_file,
        "question_count": question_count,
        "top_k": args.top_k,
        "sleep": args.sleep,
        "llm_base_url": llm_config["base_url"],
        "llm_model": llm_config["model"],
        "configs": [config for config in CONFIGS if config["config_id"] in parse_config_ids(args.configs)],
    }


def parse_config_ids(raw: str) -> list[str]:
    config_ids = [part.strip() for part in raw.split(",") if part.strip()]
    valid = {config["config_id"] for config in CONFIGS}
    unknown = [config_id for config_id in config_ids if config_id not in valid]
    if unknown:
        raise SystemExit(f"Unknown config id(s): {', '.join(unknown)}")
    if not config_ids:
        raise SystemExit("At least one config id is required")
    return config_ids


def print_summary(rows: list[dict[str, Any]], selected_configs: list[dict[str, Any]]) -> None:
    print("\nAblation run summary (mechanism score pending LLM judge)")
    print(f"{'Config':<18} {'Avg Auto Total':<15} {'Errors':<8}")
    print("-" * 48)

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["config_id"]), []).append(row)

    for config in selected_configs:
        config_rows = grouped.get(config["config_id"], [])
        if not config_rows:
            continue
        avg_auto_total = sum(float(row["auto_total"]) for row in config_rows) / max(1, len(config_rows))
        error_count = sum(int(row["has_error"]) for row in config_rows)
        print(f"{config['config_name']:<18} {avg_auto_total:<15.2f} {error_count:<8}")


def main() -> None:
    args = parse_args()
    questions = load_questions(Path(args.test_file), limit=args.limit)
    llm_config = resolve_llm_config(Path(args.env_file), args.model)
    client = create_openai_client(llm_config)
    selected_config_ids = parse_config_ids(args.configs)
    selected_configs = [config for config in CONFIGS if config["config_id"] in selected_config_ids]

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    jsonl_rows: list[dict[str, Any]] = []

    print(f"Running ablation on {len(questions)} questions")
    if any(config["config_id"] == "A0" for config in selected_configs) and not llm_config.get("api_key"):
        print("Warning: A0 No-RAG selected but no LLM_API_KEY was found; A0 rows will be recorded as errors.")

    for config in selected_configs:
        print(f"\n[{config['config_id']}] {config['config_name']}")
        for question in questions:
            if config["mode"] == "no_rag":
                response = query_no_rag(client, question["question"], llm_config)
            else:
                response = query_rag(
                    api_url=args.api_url,
                    question=question["question"],
                    route=str(config["route"]),
                    top_k=args.top_k,
                    llm_config=llm_config,
                )

            scores = score_answer(question, response)
            row = build_row(config, question, response, scores, top_k=args.top_k)
            all_rows.append(row)

            jsonl_rows.append(
                {
                    **row,
                    "sources": response.get("sources", []),
                }
            )
            print(
                f"  {question['id']:<5} {question['trait']:<9} "
                f"gene={scores['gene_score']}/4 cite={scores['citation_score']}/2 "
                f"level={scores['level_score']}/1 err={row['has_error']}"
            )
            if args.sleep > 0:
                time.sleep(args.sleep)

    results_csv = output_dir / "ablation_results.csv"
    results_jsonl = output_dir / "ablation_results.jsonl"
    manifest_json = output_dir / "ablation_manifest.json"

    write_results_csv(results_csv, all_rows)
    write_jsonl(results_jsonl, jsonl_rows)
    manifest_json.write_text(
        json.dumps(build_manifest(args, len(questions), llm_config), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print_summary(all_rows, selected_configs)
    print(f"\nSaved results to: {results_csv}")
    print(f"Saved JSONL to: {results_jsonl}")
    print(f"Saved manifest to: {manifest_json}")


if __name__ == "__main__":
    main()
