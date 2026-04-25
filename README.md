# 苹果品质育种知识问答系统

**Apple Breeding RAG — Retrieval-Augmented Generation for Apple Fruit Quality Traits**

面向苹果品质育种场景的检索增强问答系统。系统将学术文献、结构化基因数据与 QTL/GWAS 数据库统一接入向量检索引擎，针对苹果果实品质相关问题自动检索证据并生成带引用、按证据强度分层的结构化回答。

---

## 项目简介

苹果基因组与果实品质性状研究文献分散、基因数据异构，人工检索效率低、难以跨文献交叉比对。本系统将 **50 组共 70 个 PDF 文献**（含主论文 54 + 补充材料 16）和 **18 个基因/QTL/GWAS 数据集**统一向量化，构建多层级专题知识库，并通过检索增强生成（RAG）技术，根据问题类型自动路由到最相关的数据源，输出带文献引用与 Level A/B 证据分层的回答。

覆盖 5 个苹果果实品质性状：

| 性状 | 关键词示例 |
|------|-----------|
| 果实硬度（Firmness） | 细胞壁降解、果胶酶、质地 |
| 果皮颜色（Color） | 花青素、MYB 转录因子、光照响应 |
| 果实酸度（Acidity） | 苹果酸、液泡 pH、Ma1/MdALMT9 |
| 采收期（Harvest Date） | 乙烯合成、成熟指数、采前落果 |
| 糖度（Sugar Content） | 可溶性固形物、Brix、蔗糖转运 |

---

## 系统架构

```
用户提问
   │
   ▼
前端 Web UI (Next.js)
   │  HTTP / JSON
   ▼
FastAPI 后端
   ├─ 路由判断（trait 关键词 + 启发式）
   │     ├─ papers   → Qdrant: papers collection（2934 向量点）
   │     ├─ genes    → Qdrant: 18 个基因/QTL/GWAS collection（按性状分层）
   │     └─ hybrid   → 论文 + 基因双路检索，去重后多维 rerank
   │
   ├─ fastembed 语义编码（all-MiniLM-L6-v2，384 维）
   │
   └─ LLM 生成（DeepSeek / 任意 OpenAI 兼容接口）
         │
         ▼
   结构化回答（Level A 直接遗传证据 / Level B 功能支持证据 + 引用）
```

任意一次查询最多触达 **7 个 collection**（5 个 trait 优先 + 1 个通用 genes + 1 个 papers）；18 / 19 是知识库总切片数。

---

## 知识库数据概况

| 数据类型 | 来源 | 规模 |
|---------|------|------|
| 学术论文 PDF | 自动抓取（PubMed + Semantic Scholar）+ 人工筛选 | 50 组正式条目，70 个 PDF（主论文 54 + 补充材料 16），共 2934 个向量点 |
| 性状特异性基因数据 | 已发表文献人工 curated | 5 份 CSV（硬度/颜色/酸度/采收期/糖度各一） |
| GDR 原始 QTL/GWAS | Genome Database for Rosaceae | 含候选基因、染色体坐标、参考基因组 |
| GDR 精选层 | 在 GDR 基础上人工清洗 | 解析候选基因字段、统一 display_title |
| 通用兜底层 | genes.csv 全性状基线 | 42 MB CSV，覆盖五类性状 |

Qdrant 共维护 **19 个向量集合**（1 个 `papers` + 18 个基因 collection），按"性状 × 数据源 × 质量层级"分层组织。

---

## 评测结果

基于 **28 题固定测试集**（按硬度 5 / 颜色 5 / 酸度 5 / 采收期 4 / 糖度 4 / 通用方法 5 分组），LLM-as-Judge 自动评分，对比四种配置：

| 配置 | 基因召回 | 引用率 | 证据分层率 | 综合得分 |
|------|:-------:|:------:|:--------:|:------:|
| A0 No-RAG（纯 LLM） | 58% | 0% | 0% | 4.50 / 10 |
| A1 Papers-only | 59% | 100% | 39% | 4.96 / 10 |
| A2 Genes-only | 83% | 100% | 86% | 7.00 / 10 |
| **A3 Hybrid（完整系统）** | **81%** | **100%** | **86%** | **7.07 / 10** |

A3 完整系统分性状得分（由高到低）：颜色 8.2、硬度 7.6、采收期 7.5、酸度 7.0、糖度 6.25、通用方法 5.8。

> 通用类得分偏低主要是结构性原因——该类题目不考查特定候选基因，基因命中维度（4 分）天然失分。

详细结果见 [`workspace/default/evaluation/ablation/`](workspace/default/evaluation/ablation/)。

---

## 快速启动

### 前置条件

- Docker 与 Docker Compose
- DeepSeek API Key（或其他兼容 OpenAI 协议的 LLM 服务凭据）

### 启动步骤

```bash
git clone <repo-url>
cd apple-breeding-rag

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM_API_KEY 和 LLM_BASE_URL

# 启动所有服务（Qdrant + Backend + Frontend）
docker compose up -d --build
```

首次启动时，后端会自动将 `backend/data/` 下的 PDF 与 CSV 文件入库到 Qdrant，**无需手动操作**。后续启动会复用已有 collection，跳过重建。

### 访问入口

| 服务 | 地址 |
|------|------|
| Web 问答界面 | http://localhost:3000 |
| API 文档（Swagger） | http://localhost:8000/docs |
| Qdrant 控制台 | http://localhost:6333/dashboard |

---

## 使用方式

### Web 界面

1. 打开 [http://localhost:3000](http://localhost:3000)
2. 点击右上角 "Model settings"，填入 LLM API Key 和 Base URL（默认指向 DeepSeek）
3. 在输入框提问，例如：
   - "苹果果实硬度相关的 QTL 位点有哪些？"
   - "MdMYB1 在苹果花青素合成中的调控机制是什么？"
   - "Ma1/MdALMT9 与苹果酸度的关系如何？"
4. 系统自动检索并返回带引用编号的回答；右侧 "Sources and evidence" 卡片显示来源文献/基因条目，与正文 [n] 编号一一对应

### API 调用

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "苹果果实硬度相关基因有哪些？",
    "route": "hybrid",
    "top_k": 6,
    "llm_api_key": "your-api-key"
  }'
```

返回示例：

```json
{
  "answer": "苹果果实硬度受多个基因调控... [1][2]",
  "route_used": "hybrid",
  "sources": [
    {"title": "...", "type": "paper", "score": 0.85},
    {"title": "MdNAC18 (NAC18.1)", "type": "gene", "score": 0.79}
  ]
}
```

可用的 `route` 取值：`auto` / `papers` / `genes` / `hybrid`，默认 `auto`。

---

## 项目结构

```
apple-breeding-rag/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI 服务入口
│   │   ├── rag.py        # 路由、检索、rerank、生成
│   │   ├── ingest.py     # PDF/CSV 向量化入库
│   │   └── settings.py   # 配置（19 个 collection 名称等）
│   ├── data/
│   │   ├── papers/       # 70 个 PDF
│   │   └── genes/        # 18 个 CSV（运行核心）
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   └── app/
│       └── page.js       # 三栏式问答界面（React）
├── scripts/
│   ├── pipeline/         # 论文采集与入库流水线
│   ├── data_prep/        # 基因数据清洗与转换
│   └── evaluation/       # 评测与消融实验脚本
├── workspace/default/
│   └── evaluation/ablation/   # 论文引用的最终评测结果
├── thesis/                    # 毕业论文（终极版.docx）
├── docker-compose.yml         # 三服务编排
├── CURRENT_STATUS.md          # 项目当前状态快照
└── README.md
```

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | Python / FastAPI / Uvicorn |
| 向量数据库 | Qdrant v1.15.4 |
| 语义编码 | fastembed（sentence-transformers/all-MiniLM-L6-v2） |
| LLM 接口 | DeepSeek（兼容 OpenAI SDK，可替换） |
| 前端 | Next.js 14 / React 18 |
| 容器化 | Docker Compose |

---

## 环境变量

编辑 `backend/.env`（参考 `backend/.env.example`）：

```env
QDRANT_URL=http://qdrant:6333
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.deepseek.com    # 可替换为其他 OpenAI 兼容地址
LLM_MODEL=deepseek-chat
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
AUTO_INGEST=true                          # 启动时自动入库
```

---

## 设计要点

- **trait-specific collection 分层检索**：按"人工精选 → GDR curated → GDR 原始"三级优先级召回，可在覆盖率与精准度之间灵活权衡
- **多维 rerank**：在余弦相似度基础上叠加 11 项启发式调整（性状关键词、基因命名、性状错配硬扣等），并在严格关键词层做 strong/weak/fallback 三级硬过滤
- **Level A / B 证据分层**：基于 GWAS、QTL、p-value、DEG 等关键词自动判定，回答中以学术综述风格嵌入证据强度信息
- **坐标参考系保护机制**：保留各研究 source-reported 的 chr/pos，**不做跨参考基因组 liftover**，通过 `coordinate_confidence` 元数据与回答层提示防止跨研究合并误导

---

## 文档与论文

- 项目状态快照：[`CURRENT_STATUS.md`](CURRENT_STATUS.md)
- 毕业论文（终极版）：[`thesis/葛帅论文终极版.docx`](thesis/葛帅论文终极版.docx)
- 评测结果：[`workspace/default/evaluation/ablation/`](workspace/default/evaluation/ablation/)

---

## 引用

```
葛帅. 基于 RAG 方法的苹果育种专业知识问答系统及 Web 实现[D].
杨凌: 西北农林科技大学, 2026.
```
