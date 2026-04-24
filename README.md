# Apple Breeding RAG

面向苹果品质育种场景的检索增强问答系统。项目将论文 PDF、结构化基因表、QTL/GWAS 数据和人工确认的核心知识层统一接入 FastAPI + Qdrant 后端，为苹果果实硬度、颜色、酸度、采收期和糖度相关问题提供带引用的回答、数据入库能力和可复现实验评测。

## 当前项目结构

```text
apple-breeding-rag/
  backend/                 后端 API、RAG 检索、ingest 和运行配置
  frontend/                Next.js Web 前端
  scripts/                 当前仍在使用的主线脚本
  thesis/                  当前正在维护的论文文件和 handoff
  workspace/               当前论文仍直接引用的评测结果与报告
  config/                  pipeline 配置
  CURRENT_STATUS.md        当前系统状态与论文口径说明
```

## 你现在最常用的几个位置

- `backend/`
  - FastAPI 服务、RAG 路由、Qdrant ingest 和数据配置。
- `frontend/`
  - Web 界面与上传交互。
- `scripts/`
  - 当前主线脚本入口。
- `thesis/`
  - 当前论文主文件和写作 handoff。
- `CURRENT_STATUS.md`
  - 当前系统进展、论文最终口径、已知局限。
- `workspace/default/`
  - 当前工作区，只保留论文直接引用的评测结果与精选报告。

## 当前系统状态

- 系统已经具备论文 PDF 检索、gene/QTL/GWAS 检索、trait-specific 路由、证据型回答输出和自动评测能力。
- 当前最终论文库为 `50` 组论文条目、`70` 个 PDF，其中主论文 `54` 个、补充材料 `16` 个。
- `papers` collection 当前为 `2934` 个向量点。
- 当前论文采用的最终评测口径为 `28` 题消融实验；完整系统 `A3 Hybrid` 综合得分 `7.07/10`，引用率 `100%`，证据分层率 `86%`。

详细状态见：

- `CURRENT_STATUS.md`
- `thesis/README.md`
- `workspace/README.md`

## 快速开始

```bash
cd /Users/shuaige/code/apple-breeding-rag
cp backend/.env.example backend/.env
python3 scripts/pipeline/init_pipeline_workspace.py
docker compose up -d --build
```

服务地址：

- Web：[http://localhost:3000](http://localhost:3000)
- API Docs：[http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant Dashboard：[http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 常用脚本入口

工作区与论文集处理：

- `python3 scripts/pipeline/init_pipeline_workspace.py`
- `python3 scripts/pipeline/fetch_papers.py`
- `python3 scripts/pipeline/rank_fetched_papers.py`
- `python3 scripts/pipeline/build_ingest_manifest.py`
- `python3 scripts/pipeline/stage_ingest_files.py`

结构化 gene 数据：

- `python3 scripts/data_prep/convert_gene_candidates_to_csv.py`
- `python3 scripts/data_prep/convert_gdr_to_genes.py`
- `python3 scripts/data_prep/build_gdr_curated_layer.py`

评测与审计：

- `python3 scripts/evaluation/run_evaluation.py`
- `python3 scripts/evaluation/run_ablation.py`
- `python3 scripts/evaluation/audit_qtl_reference_systems.py`

论文辅助：

- `python3 scripts/thesis/normalize_nwsuaf_thesis_format.py thesis/实验进行中-gpt修改版本.docx`

## 运行数据与工作区

- `backend/data/`
  - 后端运行时数据入口，只放准备参与在线检索和向量化的数据。
- `workspace/default/evaluation/ablation/`
  - 当前论文采用的 28 题消融实验结果、表 5-1 来源和按题型汇总。
- `workspace/default/reports/`
  - 当前仍需要直接查看的精选报告。

## 保留原则

- 正在使用的论文文件放到 `thesis/`。
- `workspace/` 只保留论文当前仍直接引用的评测结果和报告。
- 运行时代码和当前论文无关的历史产物不再保留在仓库中。

## 推荐阅读顺序

1. `CURRENT_STATUS.md`
2. `thesis/README.md`
3. `workspace/default/evaluation/ablation/run_notes.md`
4. `workspace/default/evaluation/ablation/ablation_table.md`
5. `workspace/default/evaluation/ablation/trait_detail_table.md`
