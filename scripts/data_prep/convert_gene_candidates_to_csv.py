#!/usr/bin/env python3
"""Convert staged gene candidate files into one ingest-ready CSV.

Supported input types (stdlib only):
- .csv, .tsv
- .xlsx
- .zip (recursively scans supported files inside)

Notes:
- .xls is reported as unsupported (convert to .xlsx/.csv first)
"""

from __future__ import annotations

import argparse
import csv
import re
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Iterable

NS_MAIN = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
NS_REL = {"r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

SUPPORTED_FLAT = {".csv", ".tsv", ".xlsx"}


def clean_value(v: object) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() in {"nan", "none"}:
        return ""
    return s


def build_row_text(row: dict[str, str]) -> str:
    parts = []
    for k, v in row.items():
        v = clean_value(v)
        if not v:
            continue
        if k.startswith("_"):
            continue
        parts.append(f"{k}: {v}")
    return "; ".join(parts)


def iter_supported_files(root: Path) -> Iterable[Path]:
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.name == ".DS_Store":
            continue
        suffix = p.suffix.lower()
        if suffix in SUPPORTED_FLAT or suffix in {".zip", ".xls"}:
            yield p


def col_to_index(cell_ref: str) -> int:
    m = re.match(r"([A-Z]+)", cell_ref)
    if not m:
        return 0
    letters = m.group(1)
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def parse_xlsx(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    with zipfile.ZipFile(path) as zf:
        # shared strings
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS_MAIN):
                texts = [t.text or "" for t in si.findall(".//a:t", NS_MAIN)]
                shared.append("".join(texts))

        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map: dict[str, str] = {}
        for rel in rels.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
            rid = rel.attrib.get("Id", "")
            target = rel.attrib.get("Target", "")
            if rid and target:
                rel_map[rid] = target

        results: list[tuple[str, list[dict[str, str]]]] = []
        for sheet in workbook.findall("a:sheets/a:sheet", NS_MAIN):
            name = sheet.attrib.get("name", "sheet")
            rid = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id", "")
            target = rel_map.get(rid, "")
            if not target:
                continue
            if not target.startswith("worksheets/"):
                target = f"worksheets/{target.split('/')[-1]}"
            sheet_path = f"xl/{target}"
            if sheet_path not in zf.namelist():
                continue

            root = ET.fromstring(zf.read(sheet_path))
            row_values: list[list[str]] = []
            for row in root.findall(".//a:sheetData/a:row", NS_MAIN):
                row_map: dict[int, str] = {}
                max_col = -1
                for cell in row.findall("a:c", NS_MAIN):
                    ref = cell.attrib.get("r", "A1")
                    col_idx = col_to_index(ref)
                    max_col = max(max_col, col_idx)
                    ctype = cell.attrib.get("t", "")

                    val = ""
                    v_node = cell.find("a:v", NS_MAIN)
                    is_node = cell.find("a:is", NS_MAIN)

                    if ctype == "s" and v_node is not None and v_node.text is not None:
                        si = int(v_node.text)
                        val = shared[si] if 0 <= si < len(shared) else ""
                    elif ctype == "inlineStr" and is_node is not None:
                        texts = [t.text or "" for t in is_node.findall(".//a:t", NS_MAIN)]
                        val = "".join(texts)
                    elif v_node is not None and v_node.text is not None:
                        val = v_node.text

                    row_map[col_idx] = clean_value(val)

                if max_col < 0:
                    continue
                full = [""] * (max_col + 1)
                for i, v in row_map.items():
                    full[i] = v
                row_values.append(full)

            if not row_values:
                results.append((name, []))
                continue

            # First row = header
            header = [clean_value(h) for h in row_values[0]]
            header = [h if h else f"col_{i+1}" for i, h in enumerate(header)]

            records: list[dict[str, str]] = []
            for values in row_values[1:]:
                if len(values) < len(header):
                    values = values + [""] * (len(header) - len(values))
                rec = {header[i]: clean_value(values[i]) for i in range(len(header))}
                records.append(rec)
            results.append((name, records))

        return results


def parse_csv_like(path: Path, delimiter: str) -> list[tuple[str, list[dict[str, str]]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = []
        for rec in reader:
            cleaned = {str(k): clean_value(v) for k, v in (rec or {}).items()}
            rows.append(cleaned)
        return [(path.suffix.lower().lstrip("."), rows)]


def parse_xls(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    import xlrd  # type: ignore

    book = xlrd.open_workbook(path.as_posix(), on_demand=True)
    out: list[tuple[str, list[dict[str, str]]]] = []
    for sheet in book.sheets():
        if sheet.nrows == 0:
            out.append((sheet.name, []))
            continue

        header = [clean_value(sheet.cell_value(0, c)) for c in range(sheet.ncols)]
        header = [h if h else f"col_{i+1}" for i, h in enumerate(header)]

        rows: list[dict[str, str]] = []
        for r in range(1, sheet.nrows):
            rec = {}
            for c, col_name in enumerate(header):
                rec[col_name] = clean_value(sheet.cell_value(r, c))
            rows.append(rec)
        out.append((sheet.name, rows))
    return out


def read_table(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return parse_csv_like(path, ",")
    if suffix == ".tsv":
        return parse_csv_like(path, "\t")
    if suffix == ".xlsx":
        return parse_xlsx(path)
    if suffix == ".xls":
        return parse_xls(path)
    return []


def convert(root: Path, out_csv: Path, report_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    report_csv.parent.mkdir(parents=True, exist_ok=True)

    rows_out: list[dict[str, str]] = []
    report_rows: list[list[str]] = []

    def handle_one_file(file_path: Path, logical_source: str) -> None:
        try:
            sheets = read_table(file_path)
            if not sheets:
                report_rows.append([logical_source, "skipped", "unsupported_or_empty"])
                return

            added = 0
            for sheet_name, records in sheets:
                if not records:
                    continue
                for idx, rec in enumerate(records, start=1):
                    cleaned = {str(k): clean_value(v) for k, v in rec.items()}
                    row_text = build_row_text(cleaned)
                    if not row_text:
                        continue
                    row = {
                        "source_file": logical_source,
                        "sheet": sheet_name,
                        "row_index": str(idx),
                        "row_text": row_text,
                    }
                    rows_out.append(row)
                    added += 1

            if added == 0:
                report_rows.append([logical_source, "skipped", "no_nonempty_rows"])
            else:
                report_rows.append([logical_source, "ok", f"rows={added}"])
        except Exception as exc:
            report_rows.append([logical_source, "error", str(exc)])

    for file_path in iter_supported_files(root):
        if file_path.suffix.lower() == ".zip":
            try:
                with tempfile.TemporaryDirectory() as td:
                    with zipfile.ZipFile(file_path) as zf:
                        zf.extractall(td)
                    extracted_root = Path(td)
                    extracted_any = False
                    for inner in iter_supported_files(extracted_root):
                        if inner.suffix.lower() == ".zip":
                            continue
                        extracted_any = True
                        logical = f"{file_path}::{inner.relative_to(extracted_root)}"
                        handle_one_file(inner, logical)
                    if not extracted_any:
                        report_rows.append([str(file_path), "skipped", "zip_without_supported_files"])
            except Exception as exc:
                report_rows.append([str(file_path), "error", f"zip_error: {exc}"])
            continue

        handle_one_file(file_path, str(file_path))

    dedup = {}
    for row in rows_out:
        key = (row.get("source_file", ""), row.get("sheet", ""), row.get("row_text", ""))
        dedup[key] = row
    rows_final = list(dedup.values())

    all_headers = ["source_file", "sheet", "row_index", "row_text"]

    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=all_headers)
        w.writeheader()
        w.writerows(rows_final)

    with report_csv.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "status", "detail"])
        w.writerows(report_rows)

    ok_count = sum(1 for r in report_rows if r[1] == "ok")
    err_count = sum(1 for r in report_rows if r[1] == "error")
    skipped = sum(1 for r in report_rows if r[1] == "skipped")

    print(f"converted_rows={len(rows_final)}")
    print(f"processed_files_ok={ok_count}")
    print(f"processed_files_error={err_count}")
    print(f"processed_files_skipped={skipped}")
    print(f"genes_csv={out_csv}")
    print(f"report_csv={report_csv}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert gene candidate files to genes.csv")
    parser.add_argument("--input", required=True, help="Input root, e.g. backend/data/genes/raw_candidates")
    parser.add_argument("--output", required=True, help="Output genes.csv path")
    parser.add_argument("--report", required=True, help="Output conversion report csv path")
    args = parser.parse_args()

    convert(Path(args.input), Path(args.output), Path(args.report))


if __name__ == "__main__":
    main()
