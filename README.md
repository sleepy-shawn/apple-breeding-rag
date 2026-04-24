# 苹果品质育种知识问答系统

**Apple Breeding RAG — Retrieval-Augmented Generation for Apple Fruit Quality Traits**

面向苹果品质育种场景的多模态检索增强问答系统。系统将学术文献、结构化基因数据和 QTL/GWAS 数据库统一接入向量检索引擎，针对苹果果实品质相关问题自动检索证据并生成带引用的结构化回答。

---

## 项目简介

苹果基因组与果实品质性状研究文献分散、基因数据异构，人工检索效率低、难以交叉比对。本系统将 **70 篇 PDF 文献**和 **18 个基因/QTL/GWAS 数据集**统一向量化，构建多层级知识库，并通过检索增强生成（RAG）技术，根据问题类型自动路由到最相关的数据源，输出带文献引用和证据分层的回答。

覆盖 5 个苹果果实品质性状：

| 性状 | 关键词示例 |
|------|-----------|
| 果实硬度（Firmness） | 细胞壁降解、果胶酶、质地 |
| 果皮颜色（Color） | 花青素、MYB 转录因子、光照响应 |
| 果实酸度（Acidity） | 苹果酸、液泡 pH、MA 基因座 |
| 采收期（Harvest Date） | 乙烯合成、成熟指数、采前落果 |
| 糖度（Sugar Content） | 可溶性固形物、Brix、蔗糖转运 |

---

## 系统架构

```
用户提问
   │
   ▼
前端 Web UI (Next.js)
   │  HTTP
   ▼
FastAPI 后端
   ├─ 路由判断（关键词分析）
   │     ├─ 论文路由  → Qdrant: papers collection（2934 向量点）
   │     ├─ 基因路由  → Qdrant: 18 个 gene/QTL/GWAS collection
   │     └─ 混合路由  → 论文 + 基因双路检索，合并排序
   │
   ├─ fastembed 语义编码（all-MiniLM-L6-v2）
   │
   └─ LLM 生成（DeepSeek / 任意 OpenAI 兼容接口）
         │
         ▼
   结构化回答（Level A 直接证据 / Level B 间接证据 + 文献引用）
```

---

## 知识库数据概况

| 数据类型 | 来源 | 规模 |
|---------|------|------|
| 学术论文 PDF | 手工筛选入库 | 54 篇主论文 + 16 份补充材料，共 2934 个向量点 |
| 性状特异性基因数据 | 人工整理（硬度/颜色/酸度/采收期/糖度各一份） | 5 个精选 CSV |
| GDR QTL/GWAS 原始数据 | Genome Database for Rosaceae | 含候选基因、染色体坐标、参考基因组信息 |
| GDR 精选层 | 在 GDR 原始数据基础上人工清洗 | 解析候选基因字段、统一 display_title |
| 通用基因知识库 | 基线兜底层 | 42 MB CSV，覆盖全性状 |

Qdrant 共维护 **18 个向量集合**，按性状和数据来源分层组织。

---

## 评测结果

基于 **28 题消融实验**（LLM-as-Judge 自动评分），对比四种配置：

| 配置 | 基因召回率 | 引用率 | 证据分层率 | 综合得分 |
|------|:---------:|:------:|:---------:|:-------:|
| A0 无 RAG（纯 LLM） | 58% | 0% | 0% | 4.50 / 10 |
| A1 仅论文检索 | 59% | 100% | 39% | 4.96 / 10 |
| A2 仅基因检索 | 83% | 100% | 86% | 7.00 / 10 |
| **A3 混合检索（完整系统）** | **81%** | **100%** | **86%** | **7.07 / 10** |

各性状得分（A3 完整系统）：颜色 8.2、硬度 7.6、采收期 7.5、酸度 7.0、糖度 6.25。

详细结果见 [`workspace/default/evaluation/ablation/`](workspace/default/evaluation/ablation/)。

---

## 快速启动

### 前置条件

- Docker 和 Docker Compose
- DeepSeek API Key（或其他兼容 OpenAI 协议的 LLM 服务 API Key）

### 启动步骤

```bash
git clone <repo-url>
cd apple-breeding-rag

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM_API_KEY 和 LLM_BASE_URL

# 启动所有服务（Qdrant + 后端 + 前端）
docker compose up -d --build
```

首次启动时，后端会自动将 `backend/data/` 下的 PDF 和 CSV 文件入库到 Qdrant，无需手动操作。

### 访问入口

| 服务 | 地址 |
|------|------|
| Web 问答界面 | http://localhost:3000 |
| API 文档（Swagger） | http://localhost:8000/docs |
| Qdrant 向量库控制台 | http://localhost:6333/dashboard |

---

## 使用方式

### Web 界面

1. 打开 [http://localhost:3000](http://localhost:3000)
2. 点击右上角设置，填入 LLM API Key（和 Base URL，默认指向 DeepSeek）
3. 在输入框提问，例如：
   - "苹果果实硬度相关的 QTL 位点有哪些？"
   - "MdMYB1 在苹果花青素合成中的调控机制是什么？"
   - "MA 基因座与苹果酸度的关系如何？"
4. 系统自动检索并返回带引用编号的回答，来源文献/基因条目显示在回答下方

### API 直接调用

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
    {"title": "MdPG1 — polygalacturonase", "type": "gene", "score": 0.79}
  ]
}
```

---

## 项目结构

```
apple-breeding-rag/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI 服务入口，40+ 接口
│   │   ├── rag.py        # RAG 检索、路由、证据分层逻辑
│   │   ├── ingest.py     # PDF/CSV 向量化入库
│   │   └── settings.py   # 环境配置（Qdrant、LLM、集合名）
│   ├── data/
│   │   ├── papers/       # 70 个 PDF 文件
│   │   └── genes/        # 18 个 CSV 基因数据文件
│   ├── .env.example      # 环境变量模板
│   └── Dockerfile
├── frontend/
│   └── app/
│       └── page.js       # 主问答界面（React）
├── scripts/
│   ├── pipeline/         # 论文采集与入库流水线
│   ├── data_prep/        # 基因数据清洗与转换
│   └── evaluation/       # 评测与消融实验脚本
├── workspace/default/
│   └── evaluation/ablation/   # 论文引用的最终评测结果（只读）
├── thesis/               # 毕业论文文件
└── docker-compose.yml    # 三服务编排（Qdrant + Backend + Frontend）
```

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | Python / FastAPI / Uvicorn |
| 向量数据库 | Qdrant v1.15 |
| 语义编码 | fastembed（all-MiniLM-L6-v2） |
| LLM 接口 | DeepSeek（兼容 OpenAI SDK，可替换） |
| 前端 | Next.js 14 / React 18 |
| 容器化 | Docker Compose |

---

## 环境变量说明

编辑 `backend/.env`（参考 `backend/.env.example`）：

```env
QDRANT_URL=http://qdrant:6333
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.deepseek.com    # 可替换为其他 OpenAI 兼容地址
LLM_MODEL=deepseek-chat
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
AUTO_INGEST=true                          # 启动时自动入库
```
