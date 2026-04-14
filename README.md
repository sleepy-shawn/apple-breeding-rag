# Apple Breeding RAG

面向苹果品质育种场景的检索增强问答系统。项目将论文 PDF、基因/QTL/GWAS 结构化表格、GDR 数据和人工整理的核心证据统一接入 FastAPI + Qdrant 后端，为苹果果实硬度、果皮颜色、酸度、采收期和糖度相关问题提供带引用的回答、数据入库能力和可复现实验评测。

## 项目概览

- 后端：FastAPI + Qdrant，支持论文库、通用基因库、trait-specific gene collections、GDR layer 与 curated/golden layer。
- 前端：Next.js 单页界面，支持聊天、PDF 上传、基因表上传和浏览器本地 LLM Key 配置。
- 数据流程：形成了 `fetch -> curate -> manifest -> stage -> ingest -> evaluate` 的半自动 pipeline。
- 文献抓取：支持候选抓取、PDF 尝试下载、metadata 持久化和 `core/candidate/reject` 分层。
- 结构化数据：已接入 trait-specific gene tables、GDR 原始表、GDR curated layer 以及少量人工确认的核心基因层。
- 评测：已形成固定题集、run manifest、summary、manual review 和 baseline 对比框架。

当前最佳自动评测结果：

- Run：`baseline_firmness_texture_curated`
- 路径：`workspace/default/evaluation/runs/baseline_firmness_texture_curated/summary.md`
- Overall：`8.25/10`
- Firmness：`8.6/10`
- Color：`8.0/10`
- Acidity：`8.2/10`
- Harvest：`8.5/10`
- Sugar：`9.0/10`
- Retrieval hit rate：`1.0`
- Citation rate：`1.0`
- Level distinction rate：`1.0`

说明：`firmness / harvest / sugar` 的提升部分来自人工确认的核心知识层，当前适合作为系统能力验证与毕业设计展示版本；如果要作为更严格的科研知识库，仍建议老师继续确认核心基因、来源论文和证据强度。

## 顶层目录

```text
apple-breeding-rag/
  backend/                 FastAPI API、RAG 检索、ingest 和运行配置
  frontend/                Next.js Web 前端
  scripts/                 pipeline、数据清洗、评测、报告和论文辅助脚本
  docs/                    论文写作材料、研究笔记、老师审阅资料与架构图
  archive/                 模板、学校材料、历史交付物和不直接参与运行的资料
  config/pipeline.toml     pipeline 统一路径配置
  workspace/default/       抓取、评测、报告和中间状态工作区
```

配套说明文档：

- `docs/README.md`：文档与论文材料说明
- `scripts/README.md`：脚本分层与常用入口
- `archive/README.md`：毕业设计归档资料说明
- `backend/data/README.md`：运行时数据目录说明
- `workspace/README.md`：自动化工作区说明

## 系统结构

核心后端模块：

- `backend/app/main.py`：API 路由、上传接口、ingest endpoint 和启动时自动入库。
- `backend/app/rag.py`：trait 识别、collection 路由、rerank、引用组织和无 LLM fallback。
- `backend/app/ingest.py`：PDF/CSV 入库、字段清洗、GDR/golden layer 文本构造。
- `backend/app/settings.py`：Qdrant collection、自动 ingest 文件名和服务配置。
- `backend/app/schemas.py`：聊天请求、引用 source item 和上传响应 schema。

核心数据区：

- `backend/data/papers/`：已入库的主论文 PDF 与补充材料。
- `backend/data/genes/`：通用基因表、trait-specific gene tables、GDR/GWAS/QTL 数据和 curated layer。
- `workspace/default/source/`：自动抓取得到的原始论文、JSON metadata 和候选池。
- `workspace/default/library/`：人工确认后的标准论文库。
- `workspace/default/manifests/`：checklist、ingest manifest 和中间控制表。
- `workspace/default/evaluation/`：固定题集和多轮 baseline 运行结果。
- `workspace/default/reports/`：论文库存、抓取分层、老师审阅表和 thesis bundle。

当前主要 collections：

- `papers`
- `genes`
- `genes_firmness`
- `genes_color`
- `genes_acidity`
- `genes_harvest`
- `genes_sugar`
- `genes_gdr`
- `genes_gdr_firmness`
- `genes_gdr_color`
- `genes_gdr_acidity`
- `genes_gdr_harvest`
- `genes_gdr_sugar`
- `genes_gdr_curated`
- `genes_gdr_curated_firmness`
- `genes_gdr_curated_color`
- `genes_gdr_curated_acidity`
- `genes_gdr_curated_harvest`
- `genes_gdr_curated_sugar`

## 快速开始

准备环境文件：

```bash
cd /Users/shuaige/code/apple-breeding-rag
cp backend/.env.example backend/.env
```

常用环境变量：

- `LLM_API_KEY`：大模型 API Key。未配置时，系统返回检索摘要而非完整生成答案。
- `LLM_BASE_URL`：兼容 OpenAI 的推理服务地址。
- `LLM_MODEL`：聊天模型名称。
- `AUTO_INGEST_ON_STARTUP=true|false`：后端启动时是否自动执行 ingest。
- `AUTO_INGEST_GENES_FILENAME=genes.csv`：通用基因表默认文件名。

初始化工作区并启动服务：

```bash
python3 scripts/pipeline/init_pipeline_workspace.py
docker compose up -d --build
```

服务地址：

- Web：[http://localhost:3000](http://localhost:3000)
- API Docs：[http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant Dashboard：[http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 常用接口

手动触发 ingest：

```bash
curl -X POST http://localhost:8000/api/ingest/papers
curl -X POST "http://localhost:8000/api/ingest/genes?filename=genes.csv"
curl -X POST http://localhost:8000/api/ingest/genes_firmness
curl -X POST http://localhost:8000/api/ingest/genes_color
curl -X POST http://localhost:8000/api/ingest/genes_acidity
curl -X POST http://localhost:8000/api/ingest/genes_harvest
curl -X POST http://localhost:8000/api/ingest/genes_sugar
curl -X POST http://localhost:8000/api/ingest/genes_gdr
curl -X POST http://localhost:8000/api/ingest/genes_gdr_curated
```

聊天接口示例：

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "Ma1基因位点对苹果果实酸度有何影响？",
    "route": "auto",
    "top_k": 6
  }'
```

## 典型工作流

1. 初始化工作区：`python3 scripts/pipeline/init_pipeline_workspace.py`
2. 抓取候选论文：`python3 scripts/pipeline/fetch_papers.py`
3. 对候选论文分层：`python3 scripts/pipeline/rank_fetched_papers.py`
4. 将老师确认的核心论文或补充材料整理到 `workspace/default/library/papers/`
5. 生成 ingest manifest：`python3 scripts/pipeline/build_ingest_manifest.py`
6. staging 到运行数据区：`python3 scripts/pipeline/stage_ingest_files.py`
7. 重建服务或手动 ingest 指定 collection
8. 运行评测：`python3 scripts/evaluation/run_evaluation.py`
9. 导出老师审阅表或论文库存报告

## 常用脚本入口

文献 pipeline：

- `scripts/pipeline/fetch_papers.py`
- `scripts/pipeline/rank_fetched_papers.py`
- `scripts/pipeline/mine_citations.py`
- `scripts/pipeline/setup_paper_folders.py`
- `scripts/pipeline/build_ingest_manifest.py`
- `scripts/pipeline/stage_ingest_files.py`
- `scripts/pipeline/scan_papers_coverage.py`

结构化数据处理：

- `scripts/data_prep/convert_gene_candidates_to_csv.py`
- `scripts/data_prep/build_structured_genes.py`
- `scripts/data_prep/build_trait_subsets.py`
- `scripts/data_prep/build_firmness_genes_subset.py`
- `scripts/data_prep/convert_gdr_to_genes.py`
- `scripts/data_prep/build_gdr_curated_layer.py`

评测与汇报：

- `scripts/evaluation/run_evaluation.py`
- `scripts/evaluation/audit_qtl_reference_systems.py`
- `scripts/reports/export_backend_papers_review_sheet.py`
- `scripts/reports/export_paper_inventory_report.py`

论文辅助：

- `scripts/thesis/generate_thesis_word_draft.py`

## 自动评测

推荐把每轮重要改动都固化成一个 baseline：

```bash
python3 scripts/evaluation/run_evaluation.py \
  --api-url http://localhost:8000/api/chat \
  --test-file workspace/default/evaluation/test_questions.jsonl \
  --output-dir workspace/default/evaluation/runs/baseline_firmness_texture_curated \
  --run-name baseline_firmness_texture_curated \
  --notes "Added curated firmness texture/Honeycrisp gene layer for weak F004 question."
```

每次评测会输出：

- `results.jsonl`
- `results.csv`
- `manual_review.csv`
- `summary.json`
- `summary.md`
- `run_manifest.json`

## 当前限制

- `firmness / harvest / sugar` 仍部分依赖人工 curated/golden layer，更适合作为毕业设计展示版本而非完全自动化科研知识库。
- GDR 原始表中仍包含 marker 名、trait label 和跨研究异构字段，curated layer 已提升可解释性，但仍需要更严格的人工清洗。
- QTL/GWAS 坐标参考系并不完全一致；系统当前只保留来源中的 `chr/pos` 与 `reference_genome`，不做 liftover，也不直接跨研究合并坐标。
- 当前自动评分仍带有规则化成分，不能替代老师人工审阅，建议结合 `manual_review.csv` 使用。

## 下一步建议

1. 继续请老师确认核心文献、golden gene layer 和关键表述。
2. 为人工 curated 层补齐 DOI、PMID、supplement 表编号和证据强度说明。
3. 如果后续需要做坐标级共定位分析，再单独引入参考基因组版本管理与 liftover 方案。
