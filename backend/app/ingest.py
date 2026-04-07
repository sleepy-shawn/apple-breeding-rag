from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

import pandas as pd
from pypdf import PdfReader

GENE_ID_RE = re.compile(r"\b(?:MD\d{2}G\d+|Md[A-Za-z][A-Za-z0-9]+|Ma\d+|LAR1)\b")
ASSOCIATED_GENE_RE = re.compile(r"Associated gene:\s*([A-Za-z0-9_,; \-]+?)(?:\.| GWAS marker:| Published symbol:| P-value:)")
REFERENCE_GENOME_RE = re.compile(
    r"Reference genome:\s*(.*?)(?:\. Colocalizing marker:|\. Population/|\. Dataset:|\. Citation:|$)"
)


def infer_coordinate_metadata(row: dict[str, str]) -> dict[str, str]:
    """Attach conservative coordinate provenance without attempting liftover."""
    evidence = (row.get("evidence_text") or "").strip()
    source_file = (row.get("source_file") or "").strip()
    chr_value = (row.get("chr") or "").strip()
    pos_value = (row.get("pos") or "").strip()
    reference = (row.get("reference_genome") or "").strip()
    coordinate_system = (row.get("coordinate_system") or "").strip()

    if not reference:
        match = REFERENCE_GENOME_RE.search(evidence)
        if match:
            reference = " ".join(match.group(1).split())

    has_coordinate = bool(chr_value or pos_value)
    if not coordinate_system and has_coordinate:
        coordinate_system = "source-reported chr/pos"

    if reference:
        confidence = "source_reported"
        note = f"Coordinates are source-reported against {reference}; do not compare with other genome builds without liftover."
    elif has_coordinate:
        confidence = "unverified"
        if "gdr" in source_file.lower():
            note = "Coordinate reference was not parsed from this row; treat chr/pos as GDR source-reported raw coordinates and do not merge across studies without checking the source genome build."
        else:
            note = "Coordinate reference is not confirmed; treat chr/pos as raw source coordinates and do not merge across studies without checking the source genome build."
    else:
        confidence = "not_available"
        note = "No chr/pos coordinate was provided for this record."

    result = {
        "coordinate_confidence": confidence,
        "coordinate_note": note,
    }
    if reference:
        result["reference_genome"] = reference
    elif has_coordinate:
        result["reference_genome"] = "unknown"
    if coordinate_system:
        result["coordinate_system"] = coordinate_system
    return result


def extract_candidate_gene(row: dict[str, str]) -> str:
    gene_value = (row.get("gene") or "").strip()
    evidence = (row.get("evidence_text") or "").strip()

    direct_match = GENE_ID_RE.search(gene_value)
    if direct_match:
        return direct_match.group(0)

    assoc_match = ASSOCIATED_GENE_RE.search(evidence)
    if assoc_match:
        genes = []
        seen: set[str] = set()
        for match in GENE_ID_RE.finditer(assoc_match.group(1)):
            gene = match.group(0)
            lowered = gene.lower()
            if lowered not in seen:
                genes.append(gene)
                seen.add(lowered)
        if genes:
            return ", ".join(genes)

    evidence_hits = []
    seen_hits: set[str] = set()
    for match in GENE_ID_RE.finditer(evidence):
        gene = match.group(0)
        lowered = gene.lower()
        if lowered not in seen_hits:
            evidence_hits.append(gene)
            seen_hits.add(lowered)
        if len(evidence_hits) >= 3:
            break
    return ", ".join(evidence_hits)


def enrich_gene_row(row: dict[str, str]) -> dict[str, str]:
    enriched = {k.lstrip("\ufeff") if isinstance(k, str) else k: str(v) for k, v in row.items() if k is not None}
    extra_values = row.get(None)
    if extra_values and isinstance(extra_values, list):
        # Some small manually curated CSV rows contain one extra empty column
        # before chr, shifting chr/pos/pvalue/variety/evidence_text to the right.
        if enriched.get("chr") == "" and enriched.get("pos", "").lower().startswith(("chr", "lg")):
            enriched["chr"] = enriched.get("pos", "")
            enriched["pos"] = enriched.get("pvalue", "")
            enriched["pvalue"] = enriched.get("variety", "")
            enriched["variety"] = enriched.get("evidence_text", "")
            enriched["evidence_text"] = " ".join(str(value) for value in extra_values if value)
        elif not enriched.get("evidence_text"):
            enriched["evidence_text"] = " ".join(str(value) for value in extra_values if value)
    candidate_gene = extract_candidate_gene(enriched)
    published_symbol = enriched.get("gene", "").strip()
    trait = enriched.get("trait", "").strip()

    if candidate_gene:
        enriched["candidate_gene"] = candidate_gene
    if published_symbol:
        enriched["published_symbol"] = published_symbol

    if candidate_gene and published_symbol and candidate_gene.lower() != published_symbol.lower():
        enriched["display_title"] = f"{candidate_gene} ({published_symbol})"
    elif candidate_gene:
        enriched["display_title"] = candidate_gene
    elif published_symbol:
        enriched["display_title"] = published_symbol
    elif trait:
        enriched["display_title"] = f"{trait} locus"

    enriched.update(infer_coordinate_metadata(enriched))
    return enriched


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunks.append(cleaned[start:end])
        start += step
    return chunks


def load_pdf_chunks(pdf_dir: Path, pdf_paths: Iterable[Path] | None = None) -> list[dict]:
    items: list[dict] = []
    selected_paths = list(pdf_paths) if pdf_paths is not None else sorted(pdf_dir.glob("*.pdf"))
    for pdf_path in selected_paths:
        reader = PdfReader(str(pdf_path))
        title = pdf_path.stem
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            for chunk_idx, chunk in enumerate(chunk_text(text)):
                items.append(
                    {
                        "text": chunk,
                        "metadata": {
                            "source_type": "paper",
                            "title": title,
                            "page": page_idx + 1,
                            "chunk": chunk_idx,
                            "filename": pdf_path.name,
                        },
                    }
                )
    return items


def load_gene_rows(gene_file: Path) -> list[dict]:
    if gene_file.suffix.lower() not in {".csv"}:
        df = pd.read_csv(gene_file, sep="\t")
        rows = df.fillna("").to_dict(orient="records")
    else:
        with gene_file.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            try:
                header = next(reader)
            except StopIteration:
                return []

            rows: list[dict[str, str]] = []
            for line_no, row in enumerate(reader, start=2):
                if not row:
                    continue

                # Some manually curated CSV rows contain one extra blank cell
                # before the chromosome column. Drop that padding so the row
                # can still be ingested instead of failing the whole dataset.
                if len(row) == len(header) + 1 and len(header) >= 7 and row[6] == "":
                    row = row[:6] + row[7:]

                if len(row) != len(header):
                    raise ValueError(
                        f"Could not parse {gene_file.name} line {line_no}: "
                        f"expected {len(header)} fields, got {len(row)}"
                    )

                rows.append({key: value for key, value in zip(header, row)})

    items: list[dict] = []
    metadata_only_fields = {
        "reference_genome",
        "coordinate_system",
        "coordinate_confidence",
        "coordinate_note",
    }
    for idx, row in enumerate(rows):
        row_dict = enrich_gene_row(row)
        text = "; ".join([f"{k}: {v}" for k, v in row_dict.items() if v and k not in metadata_only_fields])
        if not text:
            continue
        items.append(
            {
                "text": text,
                "metadata": {
                    "source_type": "gene",
                    "record_id": str(idx),
                    **row_dict,
                },
            }
        )
    return items
