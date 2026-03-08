# Apple Breeding RAG

面向苹果育种场景的 RAG 系统（论文 PDF + 基因表格），支持证据引用问答与本地 Web 演示。

## 当前已实现

- 后端：FastAPI + Qdrant（向量检索）
- 前端：Next.js 单页问答界面
- 数据源：
  - `backend/data/papers/` 下论文 PDF
  - `backend/data/genes/` 下基因/位点 CSV
- 自动导入：后端启动后会自动检查并导入（可关闭）
  - `papers` 集合
  - `genes` 集合
  - `genes_firmness` 集合（硬度专项）
- 查询路由：`auto | papers | genes | hybrid`
- 硬度问题增强：
  - 优先检索 `genes_firmness`
  - 对病害类噪声证据降权/过滤
- 生成回答：默认要求输出 Level A / Level B，并给引用编号

## 项目结构

- `backend/`：API、检索、入库逻辑
- `frontend/`：Web 页面
- `scripts/`：数据整理与转换脚本
- `document.md`：评测问题与结果记录

## 配置

```bash
cd /Users/shuaige/code/apple-breeding-rag
cp backend/.env.example backend/.env
```

主要环境变量（`backend/.env`）：

- `LLM_API_KEY`：大模型 API Key
- `LLM_BASE_URL`：兼容 OpenAI 的地址（如 DeepSeek / Qwen 网关）
- `LLM_MODEL`：模型名（如 `deepseek-chat`）
- `AUTO_INGEST_ON_STARTUP=true|false`
- `AUTO_INGEST_GENES_FILENAME=genes.csv`
- `AUTO_INGEST_GENES_FIRMNESS_FILENAME=genes_firmness.csv`

备注：未配置 `LLM_API_KEY` 时，系统会返回检索摘要而非完整生成答案。

## 启动

```bash
docker compose up -d --build
```

服务地址：

- Web: [http://localhost:3000](http://localhost:3000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 手动导入接口（可选）

```bash
curl -X POST http://localhost:8000/api/ingest/papers
curl -X POST "http://localhost:8000/api/ingest/genes?filename=genes.csv"
curl -X POST "http://localhost:8000/api/ingest/genes_firmness?filename=genes_firmness.csv"
```

## 问答接口

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "哪些基因或位点与苹果果肉硬度保持相关？",
    "route": "auto",
    "top_k": 6
  }'
```

## 数据处理脚本（当前版本）

位于 `scripts/`：

- `convert_gene_candidates_to_csv.py`：原始候选文件批量转 CSV
- `build_structured_genes.py`：从扁平行文本提取结构化字段
- `build_trait_subsets.py`：按 trait 拆分为 `genes_*.csv`
- `build_firmness_genes_subset.py`：构建硬度专项 `genes_firmness.csv`
- `scan_papers_coverage.py`：扫描论文/基因覆盖情况
- `reorganize_rag_data.py`：整理原始数据目录

## 当前限制

- 证据质量强依赖原始 PDF 抽取与补充表规范度
- 非硬度 trait（酸度/糖度/颜色）召回仍需继续精修
- 目前以首轮可用为目标，评测指标（准确率/可追溯率）仍在迭代

## 建议工作流

1. 先整理/转换基因数据（`scripts/`）
2. 生成 `genes_firmness.csv` 并导入 `genes_firmness`
3. 跑 20 题评测并记录到 `document.md`
4. 根据错例继续优化 trait 分类与检索重排
