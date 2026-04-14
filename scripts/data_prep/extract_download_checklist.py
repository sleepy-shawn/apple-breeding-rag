#!/usr/bin/env python3
"""Extract a download checklist CSV from an xlsx file.

Usage:
  python scripts/data_prep/extract_download_checklist.py \
    --input "/path/to/副本变异位点统计.xlsx" \
    --output "/path/to/download_checklist.csv"
"""

from __future__ import annotations

import argparse
import csv
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_to_index(cell_ref: str) -> int:
    letters = ""
    for ch in cell_ref:
        if "A" <= ch <= "Z":
            letters += ch
        else:
            break
    index = 0
    for ch in letters:
        index = index * 26 + (ord(ch) - ord("A") + 1)
    return index - 1


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    name = "xl/sharedStrings.xml"
    if name not in zf.namelist():
        return []

    root = ET.fromstring(zf.read(name))
    strings: list[str] = []
    for si in root.findall("a:si", NS):
        text_parts = [node.text or "" for node in si.findall(".//a:t", NS)]
        strings.append("".join(text_parts))
    return strings


def read_sheet_rows(zf: zipfile.ZipFile, sheet_name: str = "xl/worksheets/sheet1.xml") -> list[list[str]]:
    if sheet_name not in zf.namelist():
        raise FileNotFoundError(f"Sheet not found: {sheet_name}")

    shared = load_shared_strings(zf)
    root = ET.fromstring(zf.read(sheet_name))
    rows_out: list[list[str]] = []

    for row in root.findall(".//a:sheetData/a:row", NS):
        row_map: dict[int, str] = {}
        max_col = 0
        for cell in row.findall("a:c", NS):
            ref = cell.get("r", "A1")
            col_idx = col_to_index(ref)
            max_col = max(max_col, col_idx)

            t = cell.get("t")
            value = ""

            v_node = cell.find("a:v", NS)
            is_node = cell.find("a:is", NS)

            if t == "s" and v_node is not None and shared:
                value = shared[int(v_node.text or "0")]
            elif t == "inlineStr" and is_node is not None:
                text_parts = [node.text or "" for node in is_node.findall(".//a:t", NS)]
                value = "".join(text_parts)
            elif v_node is not None and v_node.text is not None:
                value = v_node.text

            row_map[col_idx] = value.strip()

        row_values = [""] * (max_col + 1)
        for idx, val in row_map.items():
            row_values[idx] = val
        rows_out.append(row_values)

    return rows_out


def normalize_header(name: str) -> str:
    return re.sub(r"\s+", "", name or "")


def extract_pmid(url: str) -> str:
    if not url:
        return ""
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
    return m.group(1) if m else ""


def first_nonempty(row: list[str], idx: int) -> str:
    return row[idx].strip() if idx < len(row) else ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract paper download checklist from xlsx")
    parser.add_argument("--input", required=True, help="Input .xlsx path")
    parser.add_argument("--output", required=True, help="Output .csv path")
    parser.add_argument("--sheet", default="xl/worksheets/sheet1.xml", help="Sheet xml path in xlsx zip")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(in_path) as zf:
        rows = read_sheet_rows(zf, sheet_name=args.sheet)

    if not rows:
        raise ValueError("No rows found in workbook")

    header = rows[0]
    header_map = {normalize_header(col): i for i, col in enumerate(header)}

    idx_seq = header_map.get("文献序号", 0)
    idx_raw = header_map.get("原始数据文件名", 1)
    idx_title = header_map.get("文献题目", 2)
    idx_link = header_map.get("文献链接", 3)
    idx_ref = header_map.get("参考基因组", 4)

    out_header = [
        "序号",
        "文献题目",
        "文献链接",
        "PMID",
        "原始数据文件名",
        "参考基因组",
        "PDF是否完成",
        "Supplement是否完成",
        "数据来源链接",
        "备注",
    ]

    records: list[list[str]] = []
    for row in rows[1:]:
        seq = first_nonempty(row, idx_seq)
        title = first_nonempty(row, idx_title)
        link = first_nonempty(row, idx_link)

        if not (seq or title or link):
            continue

        records.append(
            [
                seq,
                title,
                link,
                extract_pmid(link),
                first_nonempty(row, idx_raw),
                first_nonempty(row, idx_ref),
                "",
                "",
                "",
                "",
            ]
        )

    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(out_header)
        writer.writerows(records)

    print(f"Wrote {len(records)} rows -> {out_path}")


if __name__ == "__main__":
    main()
