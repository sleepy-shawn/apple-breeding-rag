# Apple Breeding RAG

面向苹果品质育种场景的 RAG 原型系统。项目将论文 PDF、基因/QTL/GWAS 表格和人工整理的核心基因证据接入同一个问答服务，用于回答苹果果实硬度、果皮颜色、酸度、采收期和糖度相关问题，并保留证据引用与自动化评测结果。

## 当前进展

- 后端：FastAPI + Qdrant，支持论文、通用基因表、trait-specific gene collections 和 GDR curated layer。
- 前端：Next.js 单页问答界面，支持聊天、PDF 上传、基因表上传和浏览器本地 LLM Key 配置。
- 数据 pipeline：已拆分为 `fetch -> curate -> manifest -> stage -> ingest -> eval` 的半自动流程。
- 文献抓取：支持多源 PDF 尝试、抓取状态持久化和 `core/candidate/reject` 分层报告。
- 基因/QTL/GWAS：已接入 GDR 原始表、GDR curated 表、少量人工确认的 firmness/harvest/sugar golden gene layer，并加入 QTL/GWAS 坐标参考系保护提示。
- 自动评测：已形成固定题集、run manifest、summary、CSV/manual review 的可复现实验框架。

当前最佳自动评测结果：

- Run: `baseline_firmness_texture_curated`
- 路径：`workspace/default/evaluation/runs/baseline_firmness_texture_curated/summary.md`
- Overall: `8.25/10`
- Firmness: `8.6/10`
- Color: `8.0/10`
- Acidity: `8.2/10`
- Harvest: `8.5/10`
- Sugar: `9.0/10`
- Retrieval hit rate: `1.0`
- Citation rate: `1.0`
- Level distinction rate: `1.0`

说明：firmness/harvest/sugar 的提升来自新增的人工确认核心知识层，后续仍建议由老师确认这些核心基因和表述是否适合作为毕业设计知识库的 golden layer。QTL/GWAS 坐标目前只作为来源元数据展示，不做跨参考基因组 liftover 或物理共定位合并。

## 系统结构

```text
apple-breeding-rag/
  backend/                 FastAPI API、RAG 检索、ingest 和配置
  frontend/                Next.js Web 原型
  scripts/                 抓取、整理、GDR 清洗、评测和报告脚本
  config/pipeline.toml     pipeline 统一路径配置
  workspace/default/       自动化抓取、评测、报告和中间状态工作区
```

核心后端模块：

- `backend/app/main.py`：API 路由、上传接口、ingest endpoint 和启动时自动入库。
- `backend/app/rag.py`：trait 识别、collection 路由、rerank、引用组织和无 LLM fallback。
- `backend/app/ingest.py`：PDF/CSV 入库、基因表字段清洗、GDR/golden layer 文本构造。
- `backend/app/settings.py`：Qdrant collection、自动 ingest 文件名和服务配置。
- `backend/app/schemas.py`：聊天请求、引用 source item 和上传响应 schema。

## 数据与 Collections

主要数据目录：

- `backend/data/papers/`：已进入后端的论文 PDF 与补充材料。
- `backend/data/genes/`：通用基因表、trait-specific 表、GDR 原始/curated 表和人工 golden layer。
- `workspace/default/source/`：自动抓取的原始论文和 metadata。
- `workspace/default/library/`：人工确认后的标准论文库。
- `workspace/default/reports/`：抓取分层、导师打分表、论文覆盖率和 thesis bundle。
- `workspace/default/evaluation/`：评测题集和 baseline 运行结果。

当前后端主要 collections：

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

## 运行方式

先准备环境文件：

```bash
cd /Users/shuaige/code/apple-breeding-rag
cp backend/.env.example backend/.env
```

常用环境变量：

- `LLM_API_KEY`：大模型 API Key。未配置时，系统返回检索摘要而不是完整生成答案。
- `LLM_BASE_URL`：兼容 OpenAI 的服务地址。
- `LLM_MODEL`：模型名。
- `AUTO_INGEST_ON_STARTUP=true|false`：后端启动时是否自动检查并导入数据。
- `AUTO_INGEST_GENES_FILENAME=genes.csv`：通用基因表文件。

启动服务：

```bash
python3 scripts/init_pipeline_workspace.py
docker compose up -d --build
```

服务地址：

- Web: [http://localhost:3000](http://localhost:3000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant Dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 手动 Ingest

常用接口：

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

问答接口示例：

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "Ma1基因位点对苹果果实酸度有何影响？",
    "route": "auto",
    "top_k": 6
  }'
```

## Pipeline 脚本

论文抓取与筛选：

- `scripts/fetch_papers.py`：抓取论文候选到 `workspace/default/source/papers/`。
- `scripts/rank_fetched_papers.py`：对抓取结果打分并输出 `core/candidate/reject`。
- `scripts/mine_citations.py`：从已有论文出发挖掘引用/相似候选。

数据整理与 staging：

- `scripts/init_pipeline_workspace.py`：初始化工作区目录。
- `scripts/setup_paper_folders.py`：从 checklist 创建标准论文目录。
- `scripts/build_ingest_manifest.py`：从标准论文目录生成 ingest 清单。
- `scripts/stage_ingest_files.py`：把 ingest-ready 文件复制到 `backend/data/`。
- `scripts/scan_papers_coverage.py`：扫描论文覆盖率并输出报告。
- `scripts/reorganize_rag_data.py`：整理原始数据目录。

基因/GDR 处理：

- `scripts/convert_gene_candidates_to_csv.py`：原始候选文件批量转 CSV。
- `scripts/build_structured_genes.py`：从扁平文本提取结构化字段。
- `scripts/build_trait_subsets.py`：按 trait 拆分为 `genes_*.csv`。
- `scripts/build_firmness_genes_subset.py`：构建硬度专项基因表。
- `scripts/convert_gdr_to_genes.py`：将 GDR/QTL/GWAS 数据转换为可 ingest 的 gene 表。
- `scripts/build_gdr_curated_layer.py`：从 GDR 数据生成 curated trait-specific layer。
- `scripts/audit_qtl_reference_systems.py`：审计 QTL/GWAS 表中的 `chr/pos` 与参考基因组元数据，输出坐标参考系风险报告。

评测与汇报：

- `scripts/run_evaluation.py`：运行固定题集，输出 `results.csv/jsonl`、`summary.md/json` 和 `manual_review.csv`。
- `scripts/export_backend_papers_review_sheet.py`：导出后端已入库论文，生成给老师打分的 Excel 表。

## 自动化评测

当前推荐用固定题集评估每轮改动：

```bash
python3 scripts/run_evaluation.py \
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

## 推荐工作流

1. 初始化工作区：`python3 scripts/init_pipeline_workspace.py`
2. 抓取候选论文：`python3 scripts/fetch_papers.py`
3. 对抓取结果分层：`python3 scripts/rank_fetched_papers.py`
4. 将老师确认的核心文献或补充表整理到标准库。
5. 生成 ingest manifest 与覆盖率报告。
6. staging 到 `backend/data/`。
7. 重建后端和 Qdrant collections。
8. 运行 `scripts/run_evaluation.py`，把结果保存成一个新 baseline。

## 当前限制与下一步

- Firmness/harvest/sugar 当前依赖少量人工 golden layer，适合作为系统能力验证，但需要老师确认其科学表述和证据强度。
- GDR 数据中仍有不少 marker 或 trait label，不一定是标准基因名；curated layer 已改善可解释性，但仍需要更高质量的人工整理。
- QTL/GWAS 坐标参考系并不完全一致；系统当前保留 source-reported `chr/pos` 和 `reference_genome`，但不进行 liftover，也不把不同参考基因组下的坐标直接合并。
- Firmness 已通过 Honeycrisp/texture curated layer 明显改善，但相关证据仍建议继续用老师确认的核心论文和补充表替换成更严格的来源记录。
- 当前自动评分包含规则化成分，不能完全替代老师人工判断；`manual_review.csv` 仍建议用于毕业设计结果复核。

下一步优先级：

1. 请老师确认核心文献和 golden gene layer。
2. 针对 firmness 的 curated layer 继续补来源 DOI、PMID、supplement 表编号和原始证据强度。
3. 若后续要做坐标级共定位分析，再为每个来源补齐 reference build 与 liftover 规则；在此之前保持“只展示原始坐标，不跨研究合并”的策略。
