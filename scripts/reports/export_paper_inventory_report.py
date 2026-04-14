from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path("/Users/shuaige/code/apple-breeding-rag")
BACKEND_PAPERS = ROOT / "backend/data/papers"
SOURCE_PAPERS = ROOT / "workspace/default/source/papers"
REPORTS = ROOT / "workspace/default/reports"


SUPPLEMENT_KEYWORDS = [
    "supplement",
    "supplementary",
    "additional file",
    "figure s",
    "reporting summary",
    "同行评审",
    "补充",
    "附加",
    "esm",
    "s1.pdf",
    "s2.pdf",
    "s3.pdf",
    "s4.pdf",
    "s5.pdf",
    "s6.pdf",
]


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "", text)
    return text


def is_supplement_file(name: str) -> bool:
    lower = name.lower()
    return any(keyword in lower for keyword in SUPPLEMENT_KEYWORDS)


def extract_backend_inventory() -> list[dict[str, str]]:
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(BACKEND_PAPERS.glob("*.pdf")):
        group_id = path.name.split("_", 1)[0]
        groups[group_id].append(path)

    rows: list[dict[str, str]] = []
    for group_id, files in sorted(groups.items()):
        main_files = [path for path in files if not is_supplement_file(path.name)]
        supplement_files = [path for path in files if is_supplement_file(path.name)]
        primary = main_files[0] if main_files else files[0]
        rows.append(
            {
                "group_id": group_id,
                "main_title_guess": primary.stem,
                "main_file_count": str(len(main_files)),
                "supplement_file_count": str(len(supplement_files)),
                "total_file_count": str(len(files)),
                "primary_file": primary.name,
                "main_files": " | ".join(path.name for path in main_files) if main_files else "",
                "supplement_files": " | ".join(path.name for path in supplement_files),
            }
        )
    return rows


def extract_source_inventory() -> list[dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    meta_paths = sorted(SOURCE_PAPERS.glob("*/meta/*.json"))
    for meta_path in meta_paths:
        trait = meta_path.parents[1].name
        try:
            data = json.loads(meta_path.read_text())
        except Exception:
            continue
        pmid = str(data.get("pmid") or meta_path.stem)
        title = (data.get("title") or "").strip()
        abstract = (data.get("abstract") or "").strip()
        has_pdf = (meta_path.parents[1] / f"{pmid}.pdf").exists()
        doi = str(data.get("doi") or "")
        year = str(data.get("year") or "")
        key = pmid if pmid else normalize_text(title)
        if key not in records:
            records[key] = {
                "pmid": pmid,
                "trait": trait,
                "title": title,
                "doi": doi,
                "year": year,
                "has_pdf_in_source": "yes" if has_pdf else "no",
                "meta_path": str(meta_path),
                "pdf_path": str(meta_path.parents[1] / f"{pmid}.pdf") if has_pdf else "",
                "abstract_preview": abstract[:160].replace("\n", " "),
            }
        else:
            if has_pdf:
                records[key]["has_pdf_in_source"] = "yes"
                records[key]["pdf_path"] = str(meta_path.parents[1] / f"{pmid}.pdf")
    return sorted(records.values(), key=lambda row: (row["trait"], row["pmid"]))


def annotate_source_against_backend(
    source_rows: list[dict[str, str]], backend_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    backend_titles = []
    for row in backend_rows:
        label = row["main_title_guess"]
        normalized = normalize_text(label)
        backend_titles.append((label, normalized))

    annotated = []
    for row in source_rows:
        title = row["title"]
        normalized = normalize_text(title)
        matched = ""
        if normalized:
            for backend_label, backend_norm in backend_titles:
                if not backend_norm:
                    continue
                if normalized in backend_norm or backend_norm in normalized:
                    matched = backend_label
                    break
        updated = dict(row)
        updated["likely_already_in_backend"] = "yes" if matched else "no"
        updated["matched_backend_title"] = matched
        annotated.append(updated)
    return annotated


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_summary(backend_rows: list[dict[str, str]], source_rows: list[dict[str, str]]) -> str:
    backend_group_count = len(backend_rows)
    backend_main_count = sum(int(row["main_file_count"]) for row in backend_rows)
    backend_supp_count = sum(int(row["supplement_file_count"]) for row in backend_rows)
    backend_total_count = sum(int(row["total_file_count"]) for row in backend_rows)

    source_total = len(source_rows)
    source_pdf = sum(1 for row in source_rows if row["has_pdf_in_source"] == "yes")
    source_only_meta = source_total - source_pdf
    source_likely_in_backend = sum(1 for row in source_rows if row["likely_already_in_backend"] == "yes")
    source_not_in_backend = source_total - source_likely_in_backend

    top_backend = backend_rows[:10]
    top_source = [row for row in source_rows if row["likely_already_in_backend"] == "no"][:20]

    lines = [
        "# 论文库存盘点",
        "",
        "## 1. 结论",
        "",
        f"- 后端正式库当前约有 `{backend_group_count}` 组论文条目。",
        f"- `backend/data/papers` 目录下共有 `{backend_total_count}` 个 PDF 文件，其中主论文样文件约 `{backend_main_count}` 个，补充材料/附件约 `{backend_supp_count}` 个。",
        f"- `workspace/default/source/papers` 中按 PMID/标题去重后约有 `{source_total}` 条抓取记录。",
        f"- 其中 source 侧已有 PDF 的约 `{source_pdf}` 条，仅有 metadata 的约 `{source_only_meta}` 条。",
        f"- source 侧与后端主论文标题疑似重合的约 `{source_likely_in_backend}` 条，疑似尚未正式整理进后端的约 `{source_not_in_backend}` 条。",
        "",
        "## 2. 口径说明",
        "",
        "- `后端正式库已有`：指 `backend/data/papers` 中已经存在的论文分组。",
        "- `补充材料/附件`：指文件名中包含 supplementary、additional file、figure s、reporting summary、补充、附加等关键词的文件。",
        "- `workspace 新找到但未正式入库`：指 `workspace/default/source/papers/*/meta/*.json` 中的抓取记录；此列表按 PMID/标题去重，并用标题粗匹配标记是否疑似已经在后端中存在。",
        "- 由于后端文件名和 source 元数据命名方式不同，`likely_already_in_backend` 只是辅助判断，不代表严格去重结果。",
        "",
        "## 3. 后端正式库前 10 组",
        "",
    ]

    for row in top_backend:
        lines.append(
            f"- `{row['group_id']}`: 主文件 {row['main_file_count']} 个，补充/附件 {row['supplement_file_count']} 个，主标题 `{row['primary_file']}`"
        )

    lines.extend(
        [
            "",
            "## 4. source 中疑似尚未正式入库的前 20 条",
            "",
        ]
    )

    for row in top_source:
        lines.append(
            f"- trait=`{row['trait']}` pmid=`{row['pmid']}` has_pdf=`{row['has_pdf_in_source']}` title=`{row['title']}`"
        )

    lines.extend(
        [
            "",
            "## 5. 相关导出文件",
            "",
            "- `workspace/default/reports/backend_paper_inventory.csv`",
            "- `workspace/default/reports/source_paper_inventory.csv`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    backend_rows = extract_backend_inventory()
    source_rows = extract_source_inventory()
    source_rows = annotate_source_against_backend(source_rows, backend_rows)

    backend_csv = REPORTS / "backend_paper_inventory.csv"
    source_csv = REPORTS / "source_paper_inventory.csv"
    summary_md = REPORTS / "paper_inventory_summary.md"

    write_csv(
        backend_csv,
        backend_rows,
        [
            "group_id",
            "main_title_guess",
            "main_file_count",
            "supplement_file_count",
            "total_file_count",
            "primary_file",
            "main_files",
            "supplement_files",
        ],
    )
    write_csv(
        source_csv,
        source_rows,
        [
            "pmid",
            "trait",
            "title",
            "doi",
            "year",
            "has_pdf_in_source",
            "likely_already_in_backend",
            "matched_backend_title",
            "pdf_path",
            "meta_path",
            "abstract_preview",
        ],
    )
    summary_md.write_text(build_summary(backend_rows, source_rows), encoding="utf-8")

    print(summary_md)
    print(backend_csv)
    print(source_csv)


if __name__ == "__main__":
    main()
