"""
将 GDR (Genome Database for Rosaceae) 导出的 QTL/GWAS CSV 转换为本系统的基因CSV格式。

用法:
    python3 scripts/data_prep/convert_gdr_to_genes.py \
        --input /path/to/tripal_megasearch_download.csv \
        --output-dir backend/data/genes
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

# ── 性状映射 ──────────────────────────────────────────────────────────
TRAIT_MAP: dict[str, list[str]] = {
    "firmness":   ["fruit firmness", "fruit texture", "firmness after storage",
                   "loss of firmness", "fruit mealiness", "crispness", "flesh firmness"],
    "acidity":    ["malic acid", "titratable acidity", "organic acid",
                   "citric acid", "acidity"],
    "color":      ["skin color", "anthocyanin", "fruit color", "fruit colour",
                   "flesh color", "red color", "red flesh"],
    "sugar":      ["sugar content", "soluble solids", "dry matter content",
                   "sucrose", "sorbitol", "fruit sweetness", "brix"],
    "harvest":    ["harvest date", "preharvest fruit drop", "fruit ripe",
                   "ripening", "fruit drop", "maturity"],
    "polyphenol": ["phenolic", "polyphenol", "epicatechin", "procyanidin",
                   "catechin", "chlorogenic", "phloridzin", "flavonoid",
                   "prunin", "astragalin", "methyl gallate"],
}

def map_trait(trait_name: str) -> str | None:
    t = trait_name.lower()
    for cat, keywords in TRAIT_MAP.items():
        if any(k in t for k in keywords):
            return cat
    return None


# ── 染色体标准化 ──────────────────────────────────────────────────────
def parse_chr(location: str, linkage_group: str) -> tuple[str, str | None, str | None]:
    """Return (chr_label, start_bp, end_bp)."""
    if location:
        # "Chr08:9872424..9872424" or "Chr01:17050604..17050604"
        m = re.match(r"(Chr\w+):(\d+)\.\.(\d+)", location, re.IGNORECASE)
        if m:
            return m.group(1), m.group(2), m.group(3)
        # "Chr08:9872424"
        m2 = re.match(r"(Chr\w+):(\d+)", location, re.IGNORECASE)
        if m2:
            return m2.group(1), m2.group(2), None
    if linkage_group:
        lg = linkage_group.strip()
        if lg.isdigit():
            return f"LG{lg}", None, None
        return lg, None, None
    return "", None, None


# ── 证据文本构建 ──────────────────────────────────────────────────────
def build_evidence_text(row: dict, trait_cat: str) -> str:
    parts = []
    qtl_label = row.get("QTL/GWAS Label", "").strip()
    trait_name = row.get("Trait Name", "").strip()
    record_type = row.get("Type", "").strip()          # QTL or GWAS
    dataset = row.get("Dataset", "").strip()
    gene = row.get("Gene", "").strip()
    marker = row.get("GWAS Marker", "").strip()
    published_symbol = row.get("Published Symbol", "").strip()
    pvalue = row.get("P value", "").strip()
    lod = row.get("LOD", "").strip()
    r2 = row.get("R2", "").strip()
    pop = row.get("Population/GWAS panel", "").strip()
    maternal = row.get("Maternal Parent", "").strip()
    paternal = row.get("Paternal Parent", "").strip()
    location = row.get("Location", "").strip()
    citation = row.get("Citation", "").strip()
    col_marker = row.get("Colocalizing Marker", "").strip()
    genome = row.get("Genome", "").strip()

    parts.append(f"GDR {record_type}: {qtl_label}. Trait: {trait_name} (category: {trait_cat}).")

    if gene:
        parts.append(f"Associated gene: {gene}.")
    if marker:
        parts.append(f"GWAS marker: {marker}.")
    if published_symbol:
        parts.append(f"Published symbol: {published_symbol}.")
    if pvalue:
        parts.append(f"P-value: {pvalue}.")
    if lod:
        parts.append(f"LOD score: {lod}.")
    if r2:
        parts.append(f"R² (variance explained): {r2}%.")
    if location:
        parts.append(f"Genomic location: {location}.")
    if genome:
        parts.append(f"Reference genome: {genome}.")
    if col_marker:
        parts.append(f"Colocalizing marker: {col_marker}.")
    if pop:
        parts.append(f"Population/GWAS panel: {pop}.")
    if maternal or paternal:
        parents = " x ".join(p for p in [maternal, paternal] if p)
        parts.append(f"Cross: {parents}.")
    if dataset:
        parts.append(f"Dataset: {dataset}.")
    if citation:
        # Truncate very long citations
        cite = citation[:300] + "..." if len(citation) > 300 else citation
        parts.append(f"Citation: {cite}")

    return " ".join(parts)


# ── 主转换函数 ────────────────────────────────────────────────────────
def convert(input_path: Path, output_dir: Path) -> None:
    print(f"读取: {input_path}")
    rows: list[dict] = []
    with input_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"总行数: {len(rows)}")

    # Filter Malus only
    malus_rows = [r for r in rows if "Malus" in r.get("Organism", "")]
    print(f"Malus 行数: {len(malus_rows)}")

    # Map traits
    mapped: list[tuple[dict, str]] = []
    for r in malus_rows:
        trait_cat = map_trait(r.get("Trait Name", ""))
        if trait_cat:
            mapped.append((r, trait_cat))

    print(f"映射到目标性状: {len(mapped)} 行")
    by_trait = Counter(t for _, t in mapped)
    for t, c in sorted(by_trait.items()):
        print(f"  {t:<12}: {c}")

    # Build output rows
    out_rows: list[dict] = []
    for row, trait_cat in mapped:
        location = row.get("Location", "").strip()
        linkage = row.get("Linkage Group", "").strip()
        chr_label, start_bp, end_bp = parse_chr(location, linkage)

        gene_raw = row.get("Gene", "").strip()
        # Strip genome-ID prefix if present (e.g. "MD01G1067200" stays, "gene-xxx" becomes empty)
        gene_clean = gene_raw if not gene_raw.startswith("gene-") else ""

        marker = row.get("GWAS Marker", "").strip()
        pvalue = row.get("P value", "").strip()
        lod = row.get("LOD", "").strip()

        # score_raw: use p-value if available, else LOD
        score_raw = pvalue or lod or ""

        # published_symbol often contains the gene name used in literature
        pub_sym = row.get("Published Symbol", "").strip()
        gene_display = pub_sym or gene_clean or marker or ""

        # Population as variety proxy
        variety = (row.get("Maternal Parent", "") + "/" + row.get("Paternal Parent", "")).strip("/")
        if not variety.strip("/"):
            variety = row.get("Population/GWAS panel", "").strip()

        evidence = build_evidence_text(row, trait_cat)

        out_rows.append({
            "source_file": "GDR_rosaceae.org",
            "sheet": row.get("Dataset", ""),
            "row_index": row.get("#", ""),
            "trait": trait_cat,
            "gene": gene_display,
            "snp": marker,
            "chr": chr_label,
            "pos": start_bp or "",
            "pvalue": pvalue,
            "score_raw": score_raw,
            "variety": variety[:100] if variety else "",
            "evidence_text": evidence,
        })

    # Write combined file
    output_dir.mkdir(parents=True, exist_ok=True)
    combined_path = output_dir / "genes_gdr.csv"
    fieldnames = ["source_file", "sheet", "row_index", "trait", "gene", "snp",
                  "chr", "pos", "pvalue", "score_raw", "variety", "evidence_text"]
    with combined_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"\n✓ 写入: {combined_path}  ({len(out_rows)} 行)")

    # Write per-trait files
    trait_rows: dict[str, list[dict]] = {}
    for r in out_rows:
        trait_rows.setdefault(r["trait"], []).append(r)

    for trait, trows in trait_rows.items():
        tpath = output_dir / f"genes_gdr_{trait}.csv"
        with tpath.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trows)
        print(f"✓ 写入: {tpath}  ({len(trows)} 行)")

    print(f"\n完成! 共 {len(out_rows)} 条 Malus QTL/GWAS 记录")
    print("下一步: docker compose up -d --build  然后通过API触发重新建库")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GDR CSV to apple breeding gene format")
    parser.add_argument("--input", default="/Users/shuaige/Downloads/tripal_megasearch_download.csv")
    parser.add_argument("--output-dir", default="backend/data/genes")
    args = parser.parse_args()
    convert(Path(args.input), Path(args.output_dir))


if __name__ == "__main__":
    main()
