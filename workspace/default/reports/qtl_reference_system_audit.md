# QTL/GWAS Reference-System Audit

This report checks whether gene/QTL/GWAS CSV files carry enough reference-genome metadata for safe coordinate interpretation.

## Summary

- Total CSV rows: `144439`
- Rows with chr/pos coordinates: `12853`
- Rows with parsed reference-genome metadata: `10384`

Interpretation: coordinates should be treated as source-reported raw coordinates unless `reference_genome` is explicitly available. Do not merge or compare positions across studies without liftover and source-build validation.

## Top Parsed Reference Genomes

- `Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation`: 9428
- `Malus x domestica Whole Genome v1.0 Assembly & Annotation`: 762
- `Malus x domestica Whole Genome v1.0p Assembly & Annotation`: 88
- `Malus x domestica ‘Honeycrisp’ Genome v1.1.a1 Assembly & Annotation`: 52
- `Malus x domestica HFTH1 Whole Genome v1.0`: 46
- `Pyrus pyrifolia Whole Genome v1.0 Assembly & Annotation`: 8

## File-Level Coverage

| File | Rows | chr/pos rows | parsed reference rows | top references |
|------|------|--------------|-----------------------|----------------|
| `conversion_report.csv` | 48 | 0 | 0 | - |
| `genes.csv` | 129842 | 0 | 0 | - |
| `genes_acidity.csv` | 0 | 0 | 0 | - |
| `genes_acidity_curated.csv` | 15 | 15 | 0 | - |
| `genes_color.csv` | 4 | 4 | 0 | - |
| `genes_color_curated.csv` | 15 | 15 | 0 | - |
| `genes_firmness.csv` | 8 | 1 | 0 | - |
| `genes_gdr.csv` | 5691 | 5178 | 4543 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (4156); Malus x domestica Whole Genome v1.0 Assembly & Annotation (290); Malus x domestica Whole Genome v1.0p Assembly & Annotation (44) |
| `genes_gdr_acidity.csv` | 1727 | 1573 | 1647 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (1491); Malus x domestica Whole Genome v1.0 Assembly & Annotation (152); Pyrus pyrifolia Whole Genome v1.0 Assembly & Annotation (4) |
| `genes_gdr_color.csv` | 193 | 160 | 129 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (78); Malus x domestica Whole Genome v1.0p Assembly & Annotation (42); Malus x domestica Whole Genome v1.0 Assembly & Annotation (9) |
| `genes_gdr_curated.csv` | 649 | 558 | 649 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (558); Malus x domestica Whole Genome v1.0 Assembly & Annotation (91) |
| `genes_gdr_curated_acidity.csv` | 219 | 185 | 219 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (185); Malus x domestica Whole Genome v1.0 Assembly & Annotation (34) |
| `genes_gdr_curated_color.csv` | 18 | 15 | 18 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (15); Malus x domestica Whole Genome v1.0 Assembly & Annotation (3) |
| `genes_gdr_curated_firmness.csv` | 38 | 37 | 38 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (37); Malus x domestica Whole Genome v1.0 Assembly & Annotation (1) |
| `genes_gdr_curated_harvest.csv` | 335 | 290 | 335 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (290); Malus x domestica Whole Genome v1.0 Assembly & Annotation (45) |
| `genes_gdr_curated_sugar.csv` | 39 | 31 | 39 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (31); Malus x domestica Whole Genome v1.0 Assembly & Annotation (8) |
| `genes_gdr_firmness.csv` | 854 | 802 | 335 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (280); Malus x domestica ‘Honeycrisp’ Genome v1.1.a1 Assembly & Annotation (26); Malus x domestica HFTH1 Whole Genome v1.0 (23) |
| `genes_gdr_harvest.csv` | 974 | 913 | 878 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (823); Malus x domestica Whole Genome v1.0 Assembly & Annotation (55) |
| `genes_gdr_polyphenol.csv` | 1655 | 1464 | 1424 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (1376); Malus x domestica Whole Genome v1.0 Assembly & Annotation (48) |
| `genes_gdr_sugar.csv` | 288 | 266 | 130 | Malus x domestica GDDH13 v1.1 Whole Genome Assembly & Annotation (108); Malus x domestica Whole Genome v1.0 Assembly & Annotation (22) |
| `genes_harvest.csv` | 678 | 660 | 0 | - |
| `genes_harvest_curated.csv` | 5 | 3 | 0 | - |
| `genes_structured.csv` | 913 | 674 | 0 | - |
| `genes_sugar.csv` | 223 | 9 | 0 | - |
| `genes_sugar_curated.csv` | 5 | 0 | 0 | - |
| `sample_genes.csv` | 3 | 0 | 0 | - |

## Recommended Thesis Wording

The system preserves source-reported chromosome and position fields from QTL/GWAS resources, but does not perform cross-study coordinate liftover. When reference genome information is absent or inconsistent, chromosome positions are used only as provenance metadata rather than as direct evidence for physical colocalization.
