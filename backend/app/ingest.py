from __future__ import annotations

from pathlib import Path

import pandas as pd
from pypdf import PdfReader


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


def load_pdf_chunks(pdf_dir: Path) -> list[dict]:
    items: list[dict] = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
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
    if gene_file.suffix.lower() in {".csv"}:
        df = pd.read_csv(gene_file)
    else:
        df = pd.read_csv(gene_file, sep="\t")

    items: list[dict] = []
    for idx, row in df.fillna("").iterrows():
        row_dict = {k: str(v) for k, v in row.to_dict().items()}
        text = "; ".join([f"{k}: {v}" for k, v in row_dict.items() if v])
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
