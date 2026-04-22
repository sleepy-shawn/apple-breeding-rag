# Apple Breeding RAG

面向苹果品质育种场景的检索增强问答系统。项目将论文 PDF、结构化基因表、QTL/GWAS 数据和人工确认的核心知识层统一接入 FastAPI + Qdrant 后端，为苹果果实硬度、颜色、酸度、采收期和糖度相关问题提供带引用的回答、数据入库能力和可复现实验评测。

## 当前项目结构

```text
apple-breeding-rag/
  backend/                 后端 API、RAG 检索、ingest 和运行配置
  frontend/                Next.js Web 前端
  scripts/                 当前仍在使用的主线脚本
  thesis/                  当前正在维护的论文文件和 Claude 交接说明
  archive/                 学校材料和历史归档
  workspace/               当前最终 baseline 与精选报告
  config/                  pipeline 配置
  CURRENT_STATUS.md        当前系统状态与下一步建议
```

## 你现在最常用的几个位置

- `backend/`
  - FastAPI 服务、RAG 路由、Qdrant ingest 和数据配置。
- `frontend/`
  - Web 界面与上传交互。
- `scripts/`
  - 当前主线脚本入口。
- `thesis/`
  - 当前论文主文件和 Claude 交接说明。
- `CURRENT_STATUS.md`
  - 当前系统进展、最佳 baseline、已知局限和下一步优先级。
- `workspace/default/`
  - 当前工作区，只保留最终 baseline 与精选报告。

## 当前系统状态

- 系统已经具备论文 PDF 检索、gene/QTL/GWAS 检索、trait-specific 路由、证据型回答输出和自动评测能力。
- 当前最终论文库为 `50` 组论文条目、`70` 个 PDF，其中主论文 `54` 个、补充材料 `16` 个。
- 2026-04-22 新增 final papers 已完成 ingest，`papers` collection 当前为 `2934` 个向量点。
- 当前最终版 baseline 为 `baseline_final_paper_set`，Overall 为 `8.2/10`。
- `baseline_firmness_texture_curated` 仍可作为历史对照，但不建议再当作最终论文版本结果直接引用。
- 候选抓取池、旧 baseline 和导师审阅表已移出当前工作区，不再作为活跃文件保留。

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
- `python3 scripts/evaluation/audit_qtl_reference_systems.py`

论文辅助：

- `python3 scripts/thesis/normalize_nwsuaf_thesis_format.py thesis/葛帅毕业论文_格式修订版.docx`

## 运行数据与工作区

- `backend/data/`
  - 后端运行时数据入口，只放准备参与在线检索和向量化的数据。
- `workspace/default/evaluation/runs/baseline_final_paper_set/`
  - 当前冻结的最终论文版 baseline。
- `workspace/default/reports/`
  - 当前仍需要直接查看的精选报告。

## 归档原则

- 正在使用的论文文件放到 `thesis/`。
- 学校要求、模板和过程性材料统一放到 `archive/school-materials/`。
- 历史 baseline、旧报告、中期材料和旧版本论文统一放到 `archive/history/`。
- 历史性的一次性脚本统一放到 `archive/history/scripts/`。
- `workspace/` 只保留最终 baseline 和当前仍直接引用的报告。

## 推荐阅读顺序

1. `CURRENT_STATUS.md`
2. `thesis/README.md`
3. `scripts/README.md`
4. `workspace/README.md`
5. `archive/README.md`
