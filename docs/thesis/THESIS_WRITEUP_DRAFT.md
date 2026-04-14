# 苹果育种 RAG 系统论文正文草稿

更新时间：2026-04-10

## 1. 课题背景与研究意义

苹果果实品质性状如硬度、果皮颜色、酸度、采收期和糖度，是苹果遗传育种研究中的核心关注对象。这些性状通常由多基因共同调控，并且同时受到环境因素、成熟时期、采后贮藏条件以及不同遗传背景的共同影响。随着苹果全基因组关联分析（GWAS）、数量性状位点定位（QTL mapping）和候选基因功能验证研究的不断积累，相关知识已经广泛分布于论文正文、补充材料、数据库记录以及不同格式的基因表格之中。

传统的文献检索方式依赖人工查阅和整理，存在检索效率低、证据分散、不同研究结果难以横向比较等问题。尤其在苹果育种场景下，研究者往往需要同时回答如下问题：某一品质性状的核心候选基因有哪些；相关 GWAS/QTL 是否提供直接遗传关联证据；不同研究使用的参考基因组是否一致；以及某一候选基因是否已有功能验证支持。单纯依靠关键词搜索或人工阅读大量文献，难以高效构建面向具体育种问题的证据链。

检索增强生成（Retrieval-Augmented Generation, RAG）为这一问题提供了新的技术路径。RAG 通过先检索相关知识片段，再结合大语言模型或模板化生成模块进行回答，可以在保持可追溯性的前提下，提高复杂领域问答的效率。然而，通用 RAG 系统在专业育种场景中也存在明显不足，例如对 trait-specific 数据区分不够、对基因/QTL/GWAS 结构化信息利用不足，以及在参考坐标系不一致时可能产生错误解释。

因此，本课题围绕苹果品质育种知识问答需求，设计并实现了一个面向苹果育种场景的 RAG 原型系统。该系统以论文 PDF、基因表、QTL/GWAS 结构化数据和人工 curated 核心知识层为基础，支持 trait-specific 检索、证据型回答生成、坐标参考系保护提示以及自动化评测，为后续苹果育种知识服务和智能问答研究提供工程基础。

## 2. 系统总体目标

本系统的总体目标是构建一个面向苹果品质育种问题的可追溯知识问答原型，使系统能够针对研究者提出的 trait-specific 问题，自动检索相关论文和结构化基因证据，并以带引用的形式输出回答。为实现这一目标，系统需满足以下要求：

1. 能够管理苹果品质相关的论文 PDF、补充材料和结构化基因/QTL/GWAS 数据。
2. 能够针对硬度、颜色、酸度、采收期和糖度等主要品质性状进行专题化检索。
3. 能够区分直接遗传关联证据和间接功能支持证据，并以可追溯方式展示。
4. 能够识别并提示不同研究间 QTL/GWAS 坐标参考系不一致的问题，避免错误的跨研究坐标合并。
5. 能够通过固定测试题集对系统效果进行自动化评估，并支持后续版本比较。

## 3. 系统架构设计

### 3.1 总体架构

本系统采用“数据获取与整理层 - 向量检索与问答服务层 - 前端交互与评测层”的分层架构。整体上，原始论文和结构化基因数据首先经过抓取、清洗、分层和 staging 处理，再进入后端向量数据库；用户通过 Web 前端提交问题后，后端根据问题自动识别 trait，并路由到对应的 trait-specific collection 中检索证据，最后返回带有引用来源的回答结果。

系统核心目录包括：

- `backend/`：后端 API、RAG 检索、数据 ingest 和配置逻辑。
- `frontend/`：基于 Next.js 的交互页面。
- `scripts/`：论文抓取、数据清洗、GDR 转换、评测和报告脚本。
- `workspace/default/`：工作区，用于保存自动抓取结果、评测输出、报告和中间状态。
- `config/pipeline.toml`：pipeline 统一配置文件。

### 3.2 数据层设计

系统中的数据主要分为两类：非结构化论文数据和结构化基因/QTL/GWAS 数据。

论文数据主要来源于苹果育种相关研究论文 PDF 及其补充材料，存储于 `backend/data/papers/` 和工作区标准论文目录中。系统通过抓取脚本、清单文件和标准化目录结构对论文进行统一管理，为后续 PDF 解析和入库提供基础。

结构化数据主要存储于 `backend/data/genes/`，包括：

- 通用基因表；
- trait-specific gene tables；
- GDR 原始转换结果；
- GDR curated layer；
- 人工整理的 golden/curated 核心知识层。

在当前版本中，系统重点维护了如下核心 collections：

- `genes_firmness`
- `genes_color`
- `genes_acidity`
- `genes_harvest`
- `genes_sugar`
- `genes_gdr_curated_*`

这种按 trait 组织的设计可以降低跨性状检索噪声，提高候选基因与问题之间的匹配效率。

### 3.3 RAG 检索与回答层设计

后端采用 FastAPI 构建服务，Qdrant 作为向量数据库。系统在接收用户问题后，首先进行问题路由判断：

1. 检测问题是否属于某一 trait；
2. 若检测到特定 trait，则优先检索对应的 trait-specific collection；
3. 再结合通用基因集合或论文集合进行补充检索；
4. 对检索结果执行 rerank，提升与该 trait、关键基因和问题语义更匹配的证据排名；
5. 输出带来源编号的回答。

系统回答支持两种模式：

- 未配置 LLM API Key 时，返回检索摘要；
- 配置 LLM 后，调用兼容 OpenAI 风格接口的大模型生成完整回答。

为了增强科研可解释性，系统要求回答尽量按照“Level A 直接证据”和“Level B 间接证据”组织。其中，Level A 指 GWAS/QTL/p-value 等遗传关联证据，Level B 指表达分析、功能验证或机制支持证据。

### 3.4 参考坐标系保护机制

在苹果 QTL/GWAS 场景中，不同研究可能基于不同参考基因组，例如 GDDH13 v1.1、Malus x domestica Whole Genome v1.0、Honeycrisp Genome v1.1.a1 或 HFTH1 Whole Genome v1.0。若简单地将不同来源的 `chr/pos` 视为同一坐标系，会导致跨研究结果错误合并。

为避免这一问题，系统采用“最小安全策略”：

- 保留 source-reported `chr/pos`；
- 尽量解析并保留 `reference_genome`；
- 为每条结构化记录添加 `coordinate_note`；
- 在回答中提示“不同参考基因组下的坐标不能直接比较”；
- 当前版本不进行 liftover，不进行跨研究物理共定位结论。

这一策略兼顾了工程可用性和论文表述的严谨性。

## 4. 系统实现

### 4.1 后端实现

后端核心由 `main.py`、`rag.py`、`ingest.py`、`settings.py` 和 `schemas.py` 构成。

其中：

- `main.py` 负责定义 API 路由、上传接口、ingest endpoint 和聊天接口；
- `rag.py` 负责 trait 检测、collection 路由、rerank、答案生成和 source item 组织；
- `ingest.py` 负责论文 PDF 切分、结构化 gene row 解析、元数据补充以及向量化前文本构造；
- `settings.py` 负责 collection 名称、自动 ingest 文件名和环境变量配置；
- `schemas.py` 负责请求与返回结构定义。

为了支持前端即时检索，系统实现了上传 PDF 和上传基因表后直接触发 ingest 的能力。同时，为保证检索结果的稳定性和解释性，系统将坐标参考系保护信息保留在 metadata 中，但不将其加入 embedding 文本，从而避免因说明性字段过长而干扰语义检索。

### 4.2 数据 pipeline 实现

在数据 pipeline 方面，系统将原始抓取、标准论文库、评测结果和报告目录统一收口到 `workspace/default/` 下，并通过 `pipeline.toml` 进行路径管理。当前工作流包括：

1. 初始化工作区；
2. 抓取候选论文；
3. 对抓取结果进行 core/candidate/reject 分层；
4. 创建标准论文目录；
5. 构建 ingest manifest；
6. 将整理后的文件 staging 到后端数据目录；
7. 重建向量库；
8. 运行自动评测。

这一流程提高了系统的可重复性，降低了研究过程中数据目录混乱的问题。

### 4.3 人工 curated layer 的实现思路

在迭代过程中发现，仅依靠自动抽取的 raw gene/QTL/GWAS 数据，难以稳定回答一些关键科研问题。例如 firmness 中的 Honeycrisp 脆度问题，系统容易被大量泛化的 texture/QTL 记录占据前排，无法稳定返回 `MdNAC18`、`MdPG` 或 `MdEXP-A1` 这类更符合科研语境的核心候选基因。

因此，系统引入了人工 curated/golden layer 作为高价值小规模知识层。该层不是对大规模数据的替代，而是对评测弱项和答辩关键场景的针对性补强。当前已构建：

- `genes_firmness_curated.csv`
- `genes_harvest_curated.csv`
- `genes_sugar_curated.csv`

这些表主要用于提升关键 trait 问题的检索稳定性和回答可解释性。

## 5. 实验设计与结果分析

### 5.1 评测方法

系统使用固定题集进行自动化评测。题目覆盖：

- firmness
- color
- acidity
- harvest
- sugar
- general

每道题设置预期基因和预期机制，并根据回答中关键基因命中情况、引用情况和 Level A/B 区分情况进行打分。评测脚本会输出 `results.csv`、`results.jsonl`、`summary.md`、`summary.json` 和 `manual_review.csv`，便于后续版本比较和人工复核。

### 5.2 当前最佳结果

当前最佳 baseline 为 `baseline_firmness_texture_curated`，其结果如下：

- Overall: `8.25/10`
- Firmness: `8.6/10`
- Color: `8.0/10`
- Acidity: `8.2/10`
- Harvest: `8.5/10`
- Sugar: `9.0/10`
- Retrieval hit rate: `1.0`
- Citation rate: `1.0`
- Level distinction rate: `1.0`

实验结果表明，trait-specific collection 与人工 curated layer 的结合，显著提升了系统在苹果品质问题上的稳定性和证据可追溯性。尤其在 firmness 方向，加入 Honeycrisp/texture curated layer 后，系统对 `MdNAC18`、`MdEXP-A1`、`MdPG` 等关键基因的召回能力明显提升。

### 5.3 结果讨论

虽然当前分数已经达到较高水平，但仍需注意以下问题：

1. 部分高分来自人工 curated/golden layer，因此这些结果更适合作为“知识工程增强”的结果，而不是完全自动知识发现的结果。
2. 当前自动评测仍带有规则化特征，不能替代老师或研究者的人工判断。
3. QTL/GWAS 坐标虽然已加入参考系保护，但仍未完成跨研究统一分析，因此不适宜在论文中宣称实现了全面的坐标级整合。

## 6. 当前局限与后续工作

本系统目前已经具备毕业设计中系统设计、实现和初步实验验证所需的主要功能，但仍存在以下局限：

- curated layer 的证据来源字段尚未完全补齐 DOI、PMID、supplement table 等信息；
- 不同参考基因组下的 QTL/GWAS 坐标尚未统一；
- 某些 trait 仍依赖少量人工知识层来稳定输出；
- 当前前端展示尚可进一步优化以适配答辩展示。

后续工作可包括：

1. 让导师或领域专家确认 curated/golden layer 中核心基因的科学合理性；
2. 进一步补充人工层的来源元数据；
3. 冻结最终数据和 baseline 版本，形成毕业论文中的正式实验版本；
4. 使用真实 LLM 配置进行展示样例测试；
5. 在有充分坐标映射信息的前提下，再考虑 reference build 统一和 liftover。

## 7. 可直接用于论文的总结表述

本研究构建了一个面向苹果品质育种问题的 RAG 原型系统。系统融合论文 PDF、基因表、QTL/GWAS 结构化数据和人工 curated 核心知识层，通过 trait-specific 向量检索、证据重排序、引用追踪与自动化评测，实现了面向硬度、颜色、酸度、采收期和糖度等关键品质性状的知识问答。实验结果表明，所构建系统在固定评测题集上取得了较稳定的性能，并且能够在保持可追溯性的前提下输出具有科研可解释性的证据型回答，为苹果育种知识服务与智能问答研究提供了可行的工程基础。
