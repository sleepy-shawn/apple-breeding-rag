# Apple Breeding RAG (MVP)

一个从零可跑的最小 RAG 框架，面向苹果育种场景：
- 非结构化：论文 PDF
- 结构化：基因/位点 CSV
- 输出：带证据引用的问答 API + Web 页面

## 项目结构

- `backend/`: FastAPI + Qdrant 检索 + LLM 生成
- `frontend/`: Next.js 聊天页面
- `docker-compose.yml`: 一键启动 qdrant / backend / web

## 1) 配置环境变量

```bash
cd /Users/shuaige/code/apple-breeding-rag
cp backend/.env.example backend/.env
```

然后编辑 `backend/.env`：
- `LLM_API_KEY`: 你的 key
- `LLM_BASE_URL`: DeepSeek 或 Qwen/OpenAI 兼容地址
- `LLM_MODEL`: 如 `deepseek-chat` 或你要用的模型名

> 不填 key 也能跑检索流程，但回答会退化为“检索摘要模式”。

## 2) 放数据

- 论文 PDF 放到：`backend/data/papers/`
- 基因表（CSV/TSV）放到：`backend/data/genes/`

默认示例基因文件：`backend/data/genes/genes.csv`

## 3) 启动

```bash
docker compose up --build
```

服务地址：
- Web: [http://localhost:3000](http://localhost:3000)
- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 4) 导入数据

在前端点按钮，或直接调用 API：

```bash
curl -X POST http://localhost:8000/api/ingest/papers
curl -X POST "http://localhost:8000/api/ingest/genes?filename=genes.csv"
```

## 5) 提问

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"哪些位点与果肉硬度保持相关？","route":"auto","top_k":6}'
```

## 后续增强建议

- 混合检索：BM25 + 向量
- 重排：cross-encoder reranker
- 路由增强：基于分类器而不是关键词
- 评测集：育种问答 + 准确率/可追溯率指标
- 权限与审计：多用户、数据隔离、查询日志
