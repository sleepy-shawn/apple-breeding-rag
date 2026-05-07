# Scripts Layout

`scripts/` 现在只保留“当前最终版本仍在使用”的主线脚本。一次性整理脚本、老师审阅导出脚本和历史阶段工具已经移入 `archive/history/scripts/`。

## 目录结构

- `pipeline/`
  - 当前仍保留的文献抓取、工作区初始化、manifest 与 staging 脚本。

- `data_prep/`
  - 当前仍保留的 gene/GDR 转换与 curated layer 构建脚本。

- `evaluation/`
  - 自动评测与 QTL/GWAS 参考系审计。

- `reports/`
  - 当前仅保留论文库存盘点导出。

- `thesis/`
  - 当前仅保留 Word 格式规范化脚本。

- `lib/`
  - 公共路径配置和脚本共享逻辑。

## 最常用入口

- `python3 scripts/pipeline/init_pipeline_workspace.py`
- `python3 scripts/pipeline/fetch_papers.py`
- `python3 scripts/pipeline/rank_fetched_papers.py`
- `python3 scripts/evaluation/run_evaluation.py`
- `python3 scripts/reports/export_paper_inventory_report.py`
- `python3 scripts/thesis/normalize_nwsuaf_thesis_format.py thesis/<your-thesis>.docx`

## 使用原则

- 直接参与数据流转的脚本放在 `pipeline/`
- 把原始表整理成结构化 CSV 的脚本放在 `data_prep/`
- baseline、审计和对比脚本放在 `evaluation/`
- 当前仍有价值的盘点输出脚本放在 `reports/`
- 当前仍在使用的论文脚本统一放在 `thesis/`
- 历史阶段工具放到 `archive/history/scripts/`
