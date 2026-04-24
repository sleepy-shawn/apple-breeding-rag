from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


JUDGE_SYSTEM_PROMPT = """你是苹果遗传育种领域专家。请评估以下问答对中答案的机制准确性。
评分标准（0-3分）：
- 3分：准确描述基因功能和作用机制，与参考机制一致，无事实错误
- 2分：大体正确，有轻微不精确，但核心机制正确
- 1分：部分正确，核心机制有偏差但有合理内容
- 0分：错误、无关或未提及机制

只输出 JSON: {"score": <0-3>, "reason": "<一句话理由>"}"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Use LLM-as-judge to score mechanism accuracy")
    parser.add_argument("--input", required=True, help="Input CSV from run_evaluation or run_ablation")
    parser.add_argument("--output", required=True, help="Output CSV with mechanism_score_auto filled")
    parser.add_argument(
        "--env-file",
        default="backend/.env",
        help="Path to .env file containing LLM_API_KEY / LLM_BASE_URL / LLM_MODEL",
    )
    parser.add_argument("--model", default="", help="Optional model override")
    parser.add_argument("--sleep", type=float, default=0.8, help="Sleep between judge calls")
    parser.add_argument("--overwrite", action="store_true", help="Re-judge rows with existing mechanism_score_auto")
    parser.add_argument(
        "--test-file",
        default="workspace/default/evaluation/test_questions.jsonl",
        help="Fallback question set used to recover missing expected_mechanism/question",
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

    if not api_key:
        raise SystemExit(f"LLM_API_KEY not found in {env_file}")

    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
    }


def create_openai_client(llm_config: dict[str, str]) -> Any:
    if OpenAI is None:
        return None
    return OpenAI(
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"],
        timeout=60.0,
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
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def load_question_bank(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    bank: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        bank[row["id"]] = row
    return bank


def load_jsonl_records(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    records: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        record_id = str(row.get("id", "")).strip()
        if record_id:
            records[record_id] = row
    return records


def load_manual_review_records(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    records: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            record_id = str(row.get("id", "")).strip()
            if record_id:
                records[record_id] = row
    return records


def hydrate_row(
    row: dict[str, str],
    jsonl_records: dict[str, dict[str, Any]],
    manual_records: dict[str, dict[str, Any]],
    question_bank: dict[str, dict[str, Any]],
) -> dict[str, str]:
    record_id = str(row.get("id", "")).strip()
    jsonl = jsonl_records.get(record_id, {})
    manual = manual_records.get(record_id, {})
    question = question_bank.get(record_id, {})

    if not row.get("question"):
        row["question"] = str(jsonl.get("question") or manual.get("question") or question.get("question") or "")
    if not row.get("expected_mechanism"):
        row["expected_mechanism"] = str(
            jsonl.get("expected_mechanism") or manual.get("expected_mechanism") or question.get("expected_mechanism") or ""
        )
    if not row.get("answer"):
        row["answer"] = str(jsonl.get("answer") or manual.get("answer") or "")
    if not row.get("trait"):
        row["trait"] = str(jsonl.get("trait") or manual.get("trait") or question.get("trait") or "")

    return row


def needs_judging(row: dict[str, str], overwrite: bool) -> bool:
    manual_score = (row.get("mechanism_score_manual") or "").strip()
    auto_score = (row.get("mechanism_score_auto") or "").strip()
    if manual_score:
        return False
    if auto_score and not overwrite:
        return False
    return True


def judge_row(client: Any, llm_config: dict[str, str], row: dict[str, str]) -> dict[str, Any]:
    question = row.get("question", "").strip()
    expected_mechanism = row.get("expected_mechanism", "").strip()
    answer = row.get("answer", "").strip()

    if not question or not expected_mechanism or not answer:
        return {
            "score": 0,
            "reason": "缺少问题、参考机制或系统答案，无法完成自动判分。",
        }

    user_prompt = (
        f"问题: {question}\n"
        f"参考机制: {expected_mechanism}\n"
        f"系统答案: {answer}"
    )
    content = llm_chat_completion(
        llm_config=llm_config,
        temperature=0,
        client=client,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return parse_judge_response(content)


def parse_judge_response(content: str) -> dict[str, Any]:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {"score": 0, "reason": "判分器未返回有效 JSON。"}
        try:
            payload = json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"score": 0, "reason": "判分器返回内容无法解析。"}

    score = payload.get("score", 0)
    try:
        score_int = int(score)
    except (TypeError, ValueError):
        score_int = 0
    score_int = max(0, min(3, score_int))
    reason = str(payload.get("reason", "")).strip() or "未提供判分理由。"
    return {"score": score_int, "reason": reason}


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_missing_fields(fieldnames: list[str], extra_fields: list[str]) -> list[str]:
    result = list(fieldnames)
    for field in extra_fields:
        if field not in result:
            result.append(field)
    return result


def summarize(rows: list[dict[str, str]]) -> None:
    print("\nJudged results")
    print(f"{'ID':<8} {'Trait':<10} {'Score':<8} Reason")
    print("-" * 90)

    by_trait: dict[str, list[float]] = {}
    for row in rows:
        score = safe_int(row.get("full_total", "0"))
        trait = row.get("trait", "") or "unknown"
        by_trait.setdefault(trait, []).append(score)
        print(
            f"{row.get('id', ''):<8} {trait:<10} {score}/10    "
            f"{(row.get('judge_reason', '') or '')[:60]}"
        )

    print("\nBy trait")
    for trait in sorted(by_trait):
        values = by_trait[trait]
        avg = sum(values) / max(1, len(values))
        print(f"  {trait:<10}: {avg:.2f}/10 ({len(values)} questions)")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    question_bank = load_question_bank(Path(args.test_file))
    jsonl_records = load_jsonl_records(input_path.with_suffix(".jsonl"))
    manual_records = load_manual_review_records(input_path.with_name("manual_review.csv"))

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        raw_rows = list(reader)
        fieldnames = reader.fieldnames or []

    fieldnames = append_missing_fields(
        fieldnames,
        [
            "question",
            "expected_mechanism",
            "answer",
            "mechanism_score_auto",
            "judge_reason",
        ],
    )

    rows_needing_judge = [
        hydrate_row(dict(row), jsonl_records, manual_records, question_bank)
        for row in raw_rows
        if needs_judging(hydrate_row(dict(row), jsonl_records, manual_records, question_bank), overwrite=args.overwrite)
    ]
    llm_config: dict[str, str] | None = None
    client: Any = None
    if rows_needing_judge:
        llm_config = resolve_llm_config(Path(args.env_file), args.model)
        client = create_openai_client(llm_config)

    judged_rows: list[dict[str, str]] = []
    for row in raw_rows:
        row = hydrate_row(row, jsonl_records, manual_records, question_bank)
        if needs_judging(row, overwrite=args.overwrite):
            if llm_config is None:
                raise RuntimeError("LLM configuration was not initialized for rows requiring judging")
            result = judge_row(client, llm_config, row)
            row["mechanism_score_auto"] = str(result["score"])
            row["judge_reason"] = result["reason"]
            if args.sleep > 0:
                time.sleep(args.sleep)
        mechanism_score = safe_int(row.get("mechanism_score_auto", "0"))
        row["full_total"] = str(
            safe_int(row.get("gene_score", "0"))
            + safe_int(row.get("citation_score", "0"))
            + safe_int(row.get("level_score", "0"))
            + mechanism_score
        )
        judged_rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(judged_rows)

    summarize(judged_rows)
    print(f"\nSaved judged CSV to: {output_path}")


if __name__ == "__main__":
    main()
