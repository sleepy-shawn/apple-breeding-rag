# Scripts Layout

`scripts/` 按职责拆分为 pipeline、数据清洗、评测、报告和论文辅助五类，目标是让脚本入口清晰、命名稳定、维护成本可控。

## 目录结构

- `pipeline/`
  - 文献抓取、工作区初始化、标准论文目录、manifest、staging、覆盖率扫描等流水线脚本。

- `data_prep/`
  - 基因表清洗、trait 拆分、GDR 转换、curated layer 构建等结构化数据处理脚本。

- `evaluation/`
  - 自动评测、baseline 生成以及 QTL/GWAS 坐标参考系审计脚本。

- `reports/`
  - 文献库存导出、老师审阅表、盘点报表等项目管理与汇报脚本。

- `thesis/`
  - 论文写作辅助脚本，例如根据模板生成 Word 初稿。

- `lib/`
  - 多个脚本共用的基础模块，目前主要提供 pipeline 路径配置和公共辅助逻辑。

## 常用入口

工作区与 pipeline：

- `python3 scripts/pipeline/init_pipeline_workspace.py`
- `python3 scripts/pipeline/fetch_papers.py`
- `python3 scripts/pipeline/rank_fetched_papers.py`
- `python3 scripts/pipeline/build_ingest_manifest.py`
- `python3 scripts/pipeline/stage_ingest_files.py`

结构化数据：

- `python3 scripts/data_prep/convert_gene_candidates_to_csv.py`
- `python3 scripts/data_prep/build_structured_genes.py`
- `python3 scripts/data_prep/build_trait_subsets.py`
- `python3 scripts/data_prep/convert_gdr_to_genes.py`
- `python3 scripts/data_prep/build_gdr_curated_layer.py`

评测与审计：

- `python3 scripts/evaluation/run_evaluation.py`
- `python3 scripts/evaluation/audit_qtl_reference_systems.py`

报告导出：

- `python3 scripts/reports/export_backend_papers_review_sheet.py`
- `python3 scripts/reports/export_paper_inventory_report.py`

论文辅助：

- `python3 scripts/thesis/generate_thesis_word_draft.py`

## 分类原则

- 如果脚本直接参与数据流转，优先放入 `pipeline/`。
- 如果脚本的目标是把原始文本、候选表或 GDR 文件转换成结构化 CSV，放入 `data_prep/`。
- 如果脚本输出的是评测结果、风险审计或 baseline，对应放入 `evaluation/`。
- 如果脚本输出的是清单、Excel 或盘点报表，放入 `reports/`。
- 论文写作与模板处理逻辑统一放入 `thesis/`，避免与运行脚本混杂。

## 维护建议

- 新增脚本时尽量保持“单一职责 + 稳定输出路径”。
- 公共逻辑优先抽到 `lib/`，不要在多个脚本里复制路径和配置代码。
- 如果脚本路径调整过，请同步更新根 README、`workspace/default/README.md` 和相关 bundle 文档。
