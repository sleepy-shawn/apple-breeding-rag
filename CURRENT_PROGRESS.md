# Current Progress

更新时间：2026-04-07

## 当前系统状态

Apple Breeding RAG 已经形成一个可运行、可评测、可继续扩展的苹果品质育种 RAG 原型系统。当前系统包含论文 PDF 检索、基因/QTL/GWAS 表格检索、trait-specific 路由、证据型回答生成、前端交互和自动化 baseline 评测。

后端 Docker 已重建，当前服务健康检查通过：

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Qdrant: `http://localhost:6333/dashboard`

## 最新优化

本轮先攻克之前较弱的 `harvest` 和 `sugar` 两类问题，随后补了 QTL/GWAS 坐标参考系保护层，最后继续补强了 `firmness` 中 Honeycrisp/texture 相关弱题。

新增人工确认核心知识层：

- `backend/data/genes/genes_firmness_curated.csv`
- `backend/data/genes/genes_harvest_curated.csv`
- `backend/data/genes/genes_sugar_curated.csv`

新增或接入的 collections：

- `genes_harvest`
- `genes_sugar`

对应代码改动：

- `backend/app/settings.py`：新增 harvest/sugar collection 与自动 ingest 文件配置。
- `backend/app/main.py`：新增 harvest/sugar ingest endpoint 和 startup auto-ingest。
- `backend/app/settings.py` 与 `backend/app/main.py`：将 `genes_firmness` 默认 ingest 文件切换到 `genes_firmness_curated.csv`。
- `backend/app/ingest.py`：为基因/QTL/GWAS 记录补充 `reference_genome`、`coordinate_confidence` 和 `coordinate_note`，但这些字段不进入 embedding 正文。
- `backend/app/rag.py`：将 harvest/sugar golden collections 加入 trait-specific 检索路由，并在坐标参考系未知时提示不要跨研究合并坐标。
- `scripts/audit_qtl_reference_systems.py`：新增 QTL/GWAS 参考系审计脚本。

新增报告：

- `workspace/default/reports/qtl_reference_system_audit.md`

审计结论：

- 现有 CSV 共 `144439` 行。
- 其中 `12853` 行带 `chr/pos` 坐标。
- 其中 `10384` 行可解析出 reference-genome 信息。
- 主要参考系包括 `Malus x domestica GDDH13 v1.1`、`Malus x domestica Whole Genome v1.0`、`Honeycrisp Genome v1.1.a1`、`HFTH1 Whole Genome v1.0` 和少量 `Pyrus pyrifolia`。
- 当前系统不做 liftover，只保留原始来源坐标和 reference note。

## 最新评测结果

最新 baseline：

- Run: `baseline_harvest_sugar_golden`
- 输出目录：`workspace/default/evaluation/runs/baseline_harvest_sugar_golden/`

带 QTL/GWAS 坐标保护后的最新 baseline：

- Run: `baseline_qtl_reference_guard_v2`
- 输出目录：`workspace/default/evaluation/runs/baseline_qtl_reference_guard_v2/`

补强 Honeycrisp/texture firmness 后的当前最佳 baseline：

- Run: `baseline_firmness_texture_curated`
- 输出目录：`workspace/default/evaluation/runs/baseline_firmness_texture_curated/`

自动评测结果：

| Trait | Avg Total |
|------|-----------|
| Overall | 8.25/10 |
| Firmness | 8.6/10 |
| Color | 8.0/10 |
| Acidity | 8.2/10 |
| Harvest | 8.5/10 |
| Sugar | 9.0/10 |
| General | 7.5/10 |

其他指标：

- Retrieval hit rate: `1.0`
- Citation rate: `1.0`
- Level distinction rate: `1.0`
- Error count: `0`

与 `baseline_qtl_reference_guard_v2` 相比，主要提升来自：

- Firmness: `6.8 -> 8.6`
- Overall: `7.8 -> 8.25`

## 重要说明

Firmness/harvest/sugar 的提升来自少量人工整理的 golden gene layer。这一层适合作为系统能力验证和毕业设计原型展示，但在论文中应表述为“人工确认核心知识层”或“curated knowledge layer”，不要表述成系统自动发现的新生物学结论。

QTL/GWAS 坐标参考系目前采用最小安全策略：保留 source-reported `chr/pos` 与 `reference_genome` 元数据，但不做坐标转换，也不把不同 genome build 下的坐标直接用于物理共定位结论。论文中建议表述为“坐标作为来源元数据展示，而非跨研究统一坐标分析”。

后续最好让老师确认：

- `MdNAC18 / MdACS1 / MdACO1 / MdETR1 / MdEIN3` 是否适合作为 harvest/ripening 核心知识。
- `MdSUT1 / MdSUT4 / MdINV / MdSPS / MdHXK1` 是否适合作为 sugar/sucrose 核心知识。
- `MdNAC18 / MdNAC5 / MdPG / MdEXP-A1 / MdERF3 / MdERF118 / MdPAE10` 是否适合作为 firmness/Honeycrisp/texture 核心知识。
- 当前 evidence_text 的措辞是否足够严谨。

## 下一步建议

1. 等老师反馈后，把确认过的核心文献 supplement 表整理为更可靠的 trait-specific curated dataset。
2. 给 firmness curated layer 继续补来源 DOI、PMID、supplement 表编号和原始证据强度。
3. 如果毕业论文需要坐标级共定位分析，再单独做 reference build 统一和 liftover；当前 RAG 版本不建议强行做复杂坐标转换。
