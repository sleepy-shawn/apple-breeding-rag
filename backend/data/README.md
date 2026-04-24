# Backend Data Directory

`backend/data/` 是后端运行时的数据入口。FastAPI 服务和 ingest 流程会从这里读取论文 PDF 与结构化基因表，并将它们写入 Qdrant collections。

## 目录结构

- `papers/`
  - 已准备入库的主论文 PDF 与补充材料。
  - 文件通常由 `scripts/pipeline/stage_ingest_files.py` 复制进来，或由前端上传后直接写入。

- `genes/`
  - 结构化基因/QTL/GWAS 数据。
  - 只保留当前运行所需的最终版 CSV。
  - 详细说明见 `genes/README.md`。

## 数据来源

本目录下的数据通常来自三条路径：

1. 由 `scripts/pipeline/init_pipeline_workspace.py` 初始化出的 workspace 工作区中，人工确认后的论文库经 manifest 和 staging 后进入本目录。
2. `scripts/data_prep/` 生成的结构化基因/GDR/curated CSV。
3. Web 前端上传或 API ingest 接口触发的运行时写入。

## Git 跟踪原则

- 大体积 PDF、临时中间文件和频繁变化的运行数据通常不建议全部纳入版本控制。
- 小体积、可复现实验必需、适合演示或论文说明的 CSV 可以保留在仓库中。
- 如果新增了关键 curated layer，建议同步更新根 README 和评测说明，避免数据口径不一致。

## 使用建议

- 不要把原始下载池直接全部放入 `backend/data/`；优先经过 `workspace/default/` 的整理与筛选流程。
- 若要重建 collection，先确认 `backend/app/settings.py` 中默认文件名与这里的实际文件一致。
- 若要引入新的 trait-specific 数据，建议遵循现有命名方式：
  - `genes_<trait>.csv`
  - `genes_<trait>_curated.csv`
  - `genes_gdr_<trait>.csv`
  - `genes_gdr_curated_<trait>.csv`

## 说明

`backend/data/` 更像“运行时数据入口”而不是原始资料仓库。当前仓库中只保留准备参与在线检索和向量化的数据。
