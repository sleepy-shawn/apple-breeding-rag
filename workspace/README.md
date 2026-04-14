# Workspace Layout

`workspace/` 是项目的自动化工作区，用于承载抓取结果、标准论文库、评测数据、报告输出和流水线状态。与 `backend/data/` 相比，这里更适合保存“尚在整理过程中的资料”和“可重复执行 pipeline 的中间产物”。

## 当前工作区

默认工作区为 `workspace/default/`，包含以下核心区域：

- `source/`
  - 原始抓取结果、外部下载文件和论文 metadata。

- `library/papers/`
  - 人工确认后的标准论文库，适合作为后续 manifest 和 ingest 的输入。

- `manifests/`
  - checklist、ingest manifest 和其他控制表。

- `evaluation/`
  - 固定题集、baseline 运行目录、评测结果与人工 review 文件。

- `reports/`
  - 文献库存、抓取分层、老师审阅表、论文打包文件和其他汇总报告。

- `state/`
  - pipeline 断点状态、抓取进度、累积 metadata 等增量记录。

## 使用原则

- 原始资料先进入 `workspace/default/source/`，不要直接写入 `backend/data/`。
- 人工确认后的论文优先整理到 `workspace/default/library/papers/`。
- 报告和评测结果统一沉淀到 `workspace/default/reports/` 与 `workspace/default/evaluation/`，便于对比与复现。
- 需要参与线上检索的数据，再通过 staging 流程进入 `backend/data/`。

## 配套文档

- `workspace/default/README.md`
  - 默认工作区的具体说明和推荐工作流。
