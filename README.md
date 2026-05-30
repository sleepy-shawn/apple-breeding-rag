# 苹果品质育种知识问答系统

**Apple Breeding RAG — Retrieval-Augmented Generation for Apple Fruit Quality Traits**

面向苹果果实品质育种场景的检索增强问答系统。整合 75 篇育种相关论文与 18 份性状基因/QTL/GWAS 数据集，对用户问题自动路由检索、跨源去重、关键词感知 rerank，最后由 LLM 流式生成带引用、引用可点击跳转、可对照"纯模型回答"的可追溯回答。

> 园艺专业本科毕业设计。代码、数据清洗脚本与评测协议均开源，欢迎复用。

---

## 项目动机

苹果基因组与果实品质性状研究文献分散、基因表异构（不同研究使用不同参考基因组与命名约定），人工跨文献交叉比对效率低。本系统：

- 把已发表论文与候选基因表统一向量化，按性状分层组织
- 用启发式 + 关键词感知的 rerank，让"问题里出现哪个性状/基因"自动决定查哪个库
- 用流式 LLM 输出综述风格的回答，每条结论都附 `[N]` 可点击跳转的证据卡片
- 提供"纯 LLM 直答"对照模式，便于答辩或评测时直观展示 RAG 的价值

覆盖 5 个苹果果实品质性状：

| 性状 | 关键基因示例 |
|------|----------|
| 果实硬度 Firmness | *MdNAC18* / *MdPG1* / *MdEXP* / *MdACS* / *MdACO* |
| 果皮颜色 Color | *MdMYB1* / *MdMYB10* / *MdDFR* / *MdANS* / *MdUFGT* |
| 果实酸度 Acidity | *Ma1* / *MdALMT9* / *MdVHA-A* / *MdVHP1* / *MdMYB73* |
| 采收期 Harvest | *MdNAC83* / *MdHDT3* / *MdBPM2* / *MdRGLG3* |
| 糖度 Sugar | *MdSUT1* / *MdSWEET9b* / *MdWRKY9* / *MdCIbHLH1* |

---

## 核心特性

- 🔀 **智能路由检索**：根据问题里出现的性状词与基因符号，自动选择走论文库、性状基因库，还是混合检索
- 📚 **多层向量索引**：19 个 Qdrant collection，按"性状 × 数据来源 × 质量层级"分层（人工精选 → GDR curated → GDR 原始）
- 🎯 **关键词感知 rerank**：在余弦相似度之上叠加 11 项启发式（性状关键词、基因名 regex、错配硬扣、论文标题匹配等），并做严格关键词 strong/weak/fallback 三级硬过滤
- 🌊 **SSE 流式输出**：首字延迟约 1 秒，答案边生成边显示，附流式光标动画
- ⚡ **纯模型对照模式**：一键切换为"不查检索，仅 LLM 训练知识作答"，直观展示 RAG 价值
- 🔗 **可追溯引用**：答案里的 `[1] [2]` 是可点击 chip，点开自动滚动并高亮对应证据卡片
- 🛡 **反幻觉硬约束**：System prompt 内置"禁止杜撰别名/locus ID/突变坐标/数字"规则，并对 Ma1、MdMYB73 等高频写错的基因加入「重点事实勘误清单」
- 📤 **证据导出**：每条回答可一键导出为 Markdown（含证据卡片），方便归档/分享
- 📱 **二维码分享**：About modal 内嵌动态二维码（基于 `window.location.origin`），现场答辩听众扫码即可在自己手机上同步查看
- 🎨 **学术排版**：Fraunces + Newsreader + Noto Serif SC 衬线字体栈，基因名按学术惯例渲染为斜体，染色体编号用 mono pill

---

## 系统架构

```
                      用户提问
                         │
                         ▼
              ┌────────────────────────┐
              │  Next.js 14 前端       │
              │  • SSE 流式消费        │
              │  • 引用可点击跳证据    │
              │  • 二维码 / 导出 MD    │
              └────────────┬───────────┘
                           │  POST /api/chat/stream
                           ▼
              ┌────────────────────────┐
              │  FastAPI 后端          │
              │                        │
              │  ┌──────────────────┐  │
              │  │ 路由判断          │  │  ← 启发式 + 性状关键词
              │  │ auto/papers/genes│  │
              │  │  hybrid/llm_only │  │
              │  └─────────┬────────┘  │
              │            ▼           │
              │  ┌──────────────────┐  │
              │  │ 多 collection    │  │  ← Qdrant 向量检索
              │  │ 向量召回（dense）│  │  ← fastembed all-MiniLM-L6-v2
              │  └─────────┬────────┘  │
              │            ▼           │
              │  ┌──────────────────┐  │
              │  │ 去重 + rerank    │  │  ← 11 项启发式调权
              │  │   ↓ 硬过滤        │  │  ← strong/weak/fallback
              │  └─────────┬────────┘  │
              │            ▼           │
              │  ┌──────────────────┐  │
              │  │ 上下文 sandwich  │  │  ← top-1 头尾各放一次
              │  │ + 反幻觉 prompt  │  │  ← 重点基因勘误清单
              │  └─────────┬────────┘  │
              │            ▼           │
              │  ┌──────────────────┐  │
              │  │ LLM 流式生成     │  │  ← OpenAI 兼容（DeepSeek/Qwen）
              │  └─────────┬────────┘  │
              └────────────┼───────────┘
                           ▼
              SSE: meta → delta × N → audit → done
```

---

## 知识库数据概况

| 数据类型 | 来源 | 规模 |
|---------|------|------|
| 学术论文 PDF | PubMed + Semantic Scholar 自动抓取 + 人工筛选 | **75 个** PDF（主论文 + 补充材料），约 2900 个向量切片 |
| 性状特异性基因数据 | 已发表文献人工 curated | 5 份 CSV（硬度/颜色/酸度/采收期/糖度） |
| GDR 原始 QTL/GWAS | [Genome Database for Rosaceae](https://www.rosaceae.org/) | 含候选基因、染色体坐标、参考基因组 |
| GDR 精选层 | 在 GDR 基础上人工清洗 | 解析候选基因字段、统一 display_title |
| 通用兜底层 | `genes.csv` 全性状基线 | 42 MB CSV，覆盖五类性状 |

Qdrant 共维护 **19 个向量集合**（1 个 `papers` + 18 个基因 collection），任意一次查询最多触达 7 个 collection（5 个 trait 优先 + 1 个通用 genes + 1 个 papers）。

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

> 通用类得分偏低主要是结构性原因 —— 该类题目不考查特定候选基因，"基因命中"维度（4 分）天然失分。

详细评测协议与原始结果见 [`workspace/default/evaluation/`](workspace/default/evaluation/)。

---

## 快速启动

### 前置条件

- Docker 与 Docker Compose
- DeepSeek API Key（或其他兼容 OpenAI 协议的 LLM 服务凭据）

### 启动步骤

```bash
git clone https://github.com/sleepy-shawn/apple-breeding-rag.git
cd apple-breeding-rag

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM_API_KEY 和 LLM_BASE_URL

# 起整套（Qdrant + Backend + Frontend）
docker compose up -d --build
```

首次启动时，后端会自动把 `backend/data/` 下的 PDF 与 CSV 文件入库到 Qdrant（**无需手动操作**）。后续启动会跳过重建。

### 访问入口

| 服务 | 地址 |
|------|------|
| Web 问答界面 | http://localhost:3000 |
| API 文档（Swagger） | http://localhost:8000/docs |
| Qdrant 控制台 | http://localhost:6333/dashboard |

> 💡 LLM Key 也可以在 Web 界面右上角"配置 LLM Key"按钮临时填入，仅保存在浏览器 localStorage，不会写回 `.env`。

---

## 使用方式

### Web 界面

1. 打开 [http://localhost:3000](http://localhost:3000)
2. 右上角 "配置 LLM Key" 填入 DeepSeek 或其他 OpenAI 兼容服务的 Key
3. 在输入框提问，例如：
   - `Ma1 基因位点对苹果果实酸度有何影响？`
   - `MdMYB10 启动子中的 R6 重复序列对苹果花青素积累有何影响？`
   - `MdNAC18 基因启动子区域的 InDel 变体如何影响苹果果肉硬度和成熟时间？`
4. 答案会**流式生成**，附 `[1] [2]` 可点击引用 chip
5. 想看模型"不查检索"会怎么答？点输入框旁的「**纯模型 · 无 RAG**」chip 一键切换

### REST API（非流式）

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "苹果果实硬度相关基因有哪些？",
    "route": "hybrid",
    "top_k": 6,
    "llm_api_key": "<your-key>"
  }'
```

可用的 `route` 取值：

| route | 行为 |
|-------|------|
| `auto`（默认）| 根据问题里的性状/基因关键词自动决定 |
| `papers` | 只在论文 collection 检索 |
| `genes` | 只在基因 collection 检索 |
| `hybrid` | 论文 + 基因双路召回 |
| `llm_only` | **跳过检索**，直接让 LLM 凭训练知识作答 |

### REST API（SSE 流式）

```bash
curl -N -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"question":"苹果果实硬度相关基因有哪些？","route":"hybrid"}'
```

事件序列：

```
event: meta    data: {"route":"hybrid","sources":[...]}
event: delta   data: {"text":"**"}
event: delta   data: {"text":"结论"}
...
event: audit   data: {"cited":[1,3,5],"invalid":[],"total":6}
event: done    data: {}
```

### 查看数据库里实际有什么

```bash
curl http://localhost:8000/api/files
# {"papers":[...], "genes":[...], "papers_count":75, "genes_count":18}
```

Web 界面右上角"文件夹"按钮也可以直接查看。

---

## 部署：单机 Docker（默认）

```bash
docker compose up -d --build
```

直接暴露 :3000（前端）/ :8000（后端）/ :6333（Qdrant 控制台）。适合本机开发与个人使用。

## 部署：单机 + Nginx 反向代理（推荐用于分享）

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

只对外暴露 :80，前后端走 nginx 路由（`/` → web、`/api/*` → backend、`/docs`、`/health` → backend）。前端 `NEXT_PUBLIC_API_BASE=` 作为构建参数为空，客户端 fetch 走相对路径 `/api/...`，免去 CORS 与外部地址硬编码问题。

### 想把本地演示暴露到公网？

随便一个隧道工具都可以指到 `:80`，例如：

```bash
unset HTTP_PROXY HTTPS_PROXY  # ngrok 不允许走代理
ngrok http 80
```

ngrok 免费版给认证账号绑定一个**永久**的 `*.ngrok-free.dev` 子域名。也可以用 Cloudflare Tunnel、Tailscale Funnel 等替代。

> ⚠️ **公开链接 = 公开 LLM 配额**。系统默认无访问控制，若把链接发出去要么加 nginx Basic Auth，要么只发给信任的人，并在演示后及时关闭。

### 演示一键脚本

提供 `scripts/start-demo.sh` / `scripts/stop-demo.sh`，一键起 docker + ngrok + caffeinate（防 macOS 睡眠）：

```bash
./scripts/start-demo.sh   # 起
./scripts/stop-demo.sh    # 关
```

---

## 项目结构

```
apple-breeding-rag/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI 入口，含 /api/chat /api/chat/stream /api/files
│   │   ├── rag.py        # 路由、检索、rerank、生成（含流式）
│   │   ├── ingest.py     # PDF/CSV 向量化入库
│   │   ├── schemas.py    # Pydantic 模型
│   │   └── settings.py   # 配置（19 个 collection 名称等）
│   ├── data/
│   │   ├── papers/       # 75 个 PDF
│   │   └── genes/        # 18 个 CSV（运行核心）
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── layout.js     # next/font 注入 Fraunces / Newsreader / Noto Serif SC / JetBrains Mono
│   │   ├── globals.css   # 设计系统（CSS 变量 + 纸张噪点背景）
│   │   ├── page.js       # 单页 chat 应用（SSE 消费、模式切换、modal）
│   │   └── page.module.css
│   ├── public/
│   └── Dockerfile
├── nginx/
│   └── nginx.conf        # 反向代理（生产部署用）
├── scripts/
│   ├── pipeline/         # 论文采集与入库流水线
│   ├── data_prep/        # 基因数据清洗与转换
│   ├── evaluation/       # 评测与消融实验脚本
│   ├── start-demo.sh     # 一键演示启动
│   └── stop-demo.sh
├── workspace/default/
│   └── evaluation/       # 评测协议、测试集、运行结果
├── docker-compose.yml         # 开发：直接端口暴露
├── docker-compose.prod.yml    # 生产：nginx 反代统一入口 :80
└── README.md
```

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | Python 3.12 / FastAPI / Uvicorn |
| 向量数据库 | Qdrant v1.15.4 |
| 语义编码 | fastembed（sentence-transformers/all-MiniLM-L6-v2，384 维） |
| LLM 接口 | OpenAI SDK（默认 DeepSeek，兼容任意 OpenAI 协议服务） |
| 前端 | Next.js 14 / React 18，CSS Modules，next/font |
| 字体 | Fraunces (display, variable) / Newsreader (body) / Noto Serif SC (CJK) / JetBrains Mono |
| 反向代理 | Nginx 1.27 (alpine) |
| 容器化 | Docker Compose |

---

## 环境变量

编辑 `backend/.env`（参考 `backend/.env.example`）：

```env
QDRANT_URL=http://qdrant:6333

LLM_API_KEY=<填你的 key>
LLM_BASE_URL=https://api.deepseek.com    # 可替换为 https://dashscope.aliyuncs.com/compatible-mode/v1 等
LLM_MODEL=deepseek-chat

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

AUTO_INGEST_ON_STARTUP=true               # 启动时若 collection 不存在则自动入库
AUTO_INGEST_GENES_FILENAME=genes.csv
```

---

## 设计要点

- **Trait-specific collection 分层检索**：按"人工精选 → GDR curated → GDR 原始"三级优先级召回；不同性状对应不同的 collection 组合，可在覆盖率与精准度之间灵活权衡
- **多维 rerank**：在余弦相似度之上叠加 11 项启发式（性状关键词正/负命中、基因名 regex、性状错配硬扣、论文标题匹配 bonus、generic label penalty 等），并在严格关键词层做 strong/weak/fallback 三级硬过滤
- **上下文 sandwich**：top-1 证据除了放在 prompt 头部 `[1]`，末尾再追加一次精简版（缓解 long-context lost-in-the-middle 问题）
- **反幻觉硬约束**：System prompt 内置三条铁律 ——
  1. 禁止杜撰基因别名、locus ID、SNP 编号、突变坐标
  2. 描述基因机制/上下游关系时，证据未明示就必须写"当前证据未直接说明"
  3. p 值、染色体坐标必须能在证据片段里查到原文，否则不写具体数字
- **重点事实勘误清单**：针对模型在 Ma1、MdMYB73 等高频写错的基因，prompt 里直接给出正确的别名、因果突变描述与靶基因列表，覆盖训练知识里的错误印象
- **坐标参考系保护**：保留各研究 source-reported 的 chr/pos，**不做跨参考基因组 liftover**，通过 `coordinate_confidence` 元数据与回答层提示防止跨研究合并误导
- **Citation 后审计**：流式结束后回送 `audit` 事件，告知前端哪些 `[N]` 编号被引用、是否有越界引用，方便后续校验

---

## 已知局限 & 后续方向

- **检索召回侧目前是 dense-only**：未引入 BM25 sparse 或 cross-encoder rerank，对生僻基因符号的精确匹配偶有遗漏
- **Embedding 模型偏通用**：MiniLM-L6-v2 在中英混排的农学文本上够用但非最优；可考虑切到 BGE-M3 或领域微调的 model
- **评测集规模偏小**：28 题以人工标注为主；后续可扩展到 100+ 题并加入人工评分对照
- **未支持多轮上下文记忆**：每次提问独立检索，不利用前文对话；如需可在 chat history 注入路由 hint
- **基因数据需手动维护**：目前 `genes_*_curated.csv` 是人工整理；可考虑接入 Ensembl Plants / NCBI Gene API 做自动同步

---

## 致谢

- [Genome Database for Rosaceae (GDR)](https://www.rosaceae.org/) 提供原始 QTL/GWAS 数据
- 所有被引用的苹果育种领域论文作者
- [DeepSeek](https://www.deepseek.com/) 提供性价比极高的 LLM 服务
- [Qdrant](https://qdrant.tech/) 与 [fastembed](https://github.com/qdrant/fastembed) 提供向量索引基础设施

---

## License

[MIT License](LICENSE) — 代码与脚本部分。

数据部分（`backend/data/`）：
- 论文 PDF 版权属于各自出版商，仅出于学术研究目的提供检索索引，请勿二次分发
- 人工 curated 的基因表（`genes_*_curated.csv`）以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 释出，使用时请注明出处
- GDR 衍生数据请遵循 [GDR 数据使用协议](https://www.rosaceae.org/data_use)

---

## 引用

如果本项目对你的研究有帮助，欢迎引用：

```bibtex
@misc{applebreedingrag2026,
  title  = {Apple Breeding RAG: Retrieval-Augmented Generation for Apple Fruit Quality Traits},
  author = {Ge, Shuai},
  year   = {2026},
  note   = {Undergraduate thesis project, Northwest A\&F University},
  url    = {https://github.com/sleepy-shawn/apple-breeding-rag}
}
```
