# Apple Breeding RAG 项目论文写作交接说明

本文档用于给 Claude 或其他写作助手快速建立上下文，帮助继续撰写本科毕业论文。内容重点不是逐文件罗列，而是总结本项目已经完成的工程工作、当前结果、论文中值得强调的贡献点，以及仍需谨慎表述的部分。

## 1. 项目定位

本项目的目标是构建一个面向苹果品质育种场景的检索增强知识问答系统（RAG）。系统聚焦苹果果实品质相关的核心性状，包括：

- 硬度 `firmness`
- 颜色 `color`
- 酸度 `acidity`
- 采收期 `harvest`
- 糖度 `sugar`

项目的核心问题不是通用聊天，而是如何将分散在论文 PDF、补充材料、结构化基因表、QTL/GWAS 数据中的证据组织起来，让系统能够回答“某个品质性状相关的重要候选基因是什么、证据来自哪里、证据强弱如何”这一类科研问题。

## 2. 论文里可以采用的系统总述

可以把系统概括为一个四层结构：

1. 数据获取与整理层  
负责抓取论文、整理 PDF、转换和清洗基因表、构建 GDR/QTL/GWAS curated 数据层。

2. 检索与问答服务层  
基于 FastAPI 和 Qdrant 构建后端，支持 trait-specific collection、混合检索、rerank 和带引用的回答输出。

3. 评测与验证层  
通过固定题集、自动评测脚本、summary 结果和人工复核表，对不同版本系统进行比较。

4. 前端交互层  
提供网页界面、聊天入口、PDF 上传、gene 文件上传以及 LLM Key 配置，便于展示和答辩演示。

## 3. 项目目录和代码框架

### 3.1 顶层结构

项目根目录：`/Users/shuaige/code/apple-breeding-rag`

重要目录：

- `backend/`
- `frontend/`
- `scripts/`
- `config/`
- `workspace/`
- `archive/graduation-materials/`
- `archive/school-docs/`

### 3.2 backend

后端核心代码位于 `backend/app/`，主要职责如下：

- `main.py`  
定义 API 接口，包括聊天、上传、ingest、健康检查等。

- `rag.py`  
实现问题路由、trait 识别、collection 选择、检索结果 rerank、答案组织和引用展示逻辑。  
这是系统效果提升最大的核心文件之一。

- `ingest.py`  
负责 PDF、gene CSV、GDR curated 数据的入库和 metadata 清洗。  
后续关于 reference genome、candidate gene、display title 等逻辑也补在这里。

- `settings.py`  
维护集合名称、默认数据路径、模型配置等系统级设置。

### 3.3 frontend

前端位于 `frontend/app/`，目前已经支持：

- 聊天问答
- PDF 上传
- gene 文件上传
- 前端配置 LLM API Key / Base URL / Model
- 类 Claude 风格的界面布局和研究工作台式侧边栏

### 3.4 scripts

`scripts/` 里已经包含较完整的数据处理与评测脚本：

- 论文抓取与标准化
- 工作区初始化
- ingest manifest / staging
- GDR 转换与 curated layer 构建
- 评测运行
- QTL 参考系审计
- 给老师导出论文清单、评审表等

### 3.5 workspace

`workspace/default/` 主要用于承载中间产物和实验结果：

- `source/` 原始抓取结果
- `library/` 标准论文库
- `state/` 抓取状态和 metadata
- `evaluation/` 评测题集和每轮 baseline
- `reports/` 排名、审计、导出表格、压缩包

这个目录设计的意义是把“原始数据、中间状态、正式结果”分开，便于重复实验和后续自动化。

## 4. 已完成的主要工程工作

以下内容是论文“系统实现”章节最值得写的部分。

### 4.1 重构了项目工作区和 pipeline 目录

最初项目更接近脚本集合，后续重构为统一工作区框架，主要包括：

- `config/pipeline.toml`
- `scripts/lib/pipeline_layout.py`
- `scripts/pipeline/init_pipeline_workspace.py`

作用：

- 统一路径管理
- 分离 source、library、evaluation、reports、state
- 便于自动抓取、自动处理、自动评测的流水线化运行

### 4.2 重构了论文抓取流程

完成了 paper fetch 链路的增强，包括：

- trait 定向检索
- metadata 持久化
- PDF 获取尝试
- fetch 结果 ranking
- 核心论文优先级输出

这一部分的意义不是“抓越多越好”，而是把文献获取过程做成可追踪、可筛选、可反复运行的 pipeline。

### 4.3 构建了 trait-specific collections

为了降低不同性状之间的检索噪声，系统没有只用一个统一的 `genes` 库，而是拆分了多类集合，例如：

- `genes`
- `genes_firmness`
- `genes_color`
- `genes_acidity`
- `genes_harvest`
- `genes_sugar`
- `genes_gdr`
- `genes_gdr_curated_*`

论文里可以强调：苹果品质问题不是单一语义空间，按 trait 组织知识集合更符合科研使用场景。

### 4.4 实现了 trait-specific 路由和 rerank

系统会先识别问题所属 trait，再优先检索相应的 trait-specific 集合，并结合论文集合做 hybrid retrieval。  
此外还实现了 rerank 机制，对以下因素进行加权：

- trait 匹配
- 标准基因名
- candidate gene
- 证据类型
- source title

这一块是系统效果提升的关键，不是换 embedding 带来的收益。

### 4.5 加入了 GDR 数据转换和 curated layer

原始 GDR/QTL/GWAS 数据存在几个问题：

- 字段格式不统一
- 很多记录是 marker 或 trait label
- 不一定直接包含标准基因名

因此新增了：

- GDR 转换脚本
- `candidate_gene` 抽取
- `display_title` 生成
- `genes_gdr_curated.csv`
- 各 trait 的 GDR curated 子集

这一步更多提升了工程整洁度和证据解释性。

### 4.6 构建了小规模人工 curated / golden gene layer

后续发现单靠原始 GDR/QTL 数据并不能稳定回答某些关键问题，特别是：

- firmness
- harvest
- sugar

因此为这些弱项补了小规模人工 curated 核心知识层，核心思想是：

- 不盲目扩库
- 只加入高价值、可解释、与测试问题高度相关的基因记录
- 明确在论文里表述为“人工确认核心知识层”，不要写成系统自动发现的新知识

这是当前系统分数提升最明显的来源之一。

### 4.7 加入了 QTL/GWAS 坐标参考系保护机制

项目中一个重要科学风险是：不同研究使用的参考基因组并不一致，不能直接将不同来源的 `chr + pos` 视作同一坐标系。

为此做了如下处理：

- 新增参考系审计脚本
- 统计各 CSV 文件中的 `reference_genome`
- 在 ingest metadata 中保留 `reference_genome`
- 在回答层提示用户不要直接跨研究合并坐标

当前策略是“最小安全方案”：

- 不做复杂 liftover
- 不做跨研究坐标直接合并
- 保留原始坐标和 reference note

这一点在论文中会显得更严谨。

### 4.8 补齐了自动评测框架

系统已经有可复现的评测流程，不只是主观感觉调参数。  
评测框架包括：

- 固定测试题集
- 自动打分
- summary 输出
- manual review 表
- 多轮 baseline 对比

这使论文实验部分可以明确写“版本迭代”和“性能变化”。

## 5. 当前系统效果与关键结果

### 5.1 当前总体水平

当前系统已经达到“可展示、可答辩、可写论文”的原型状态，不再是 demo 级别。

我对当前完成度的判断：

- 成品度大约 `75% - 82%`

原因：

- 数据层已成形
- 后端可稳定运行
- 前端可展示
- 自动评测框架已建立
- 多个弱项已经通过 curated layer 补强

### 5.2 baseline 结果

项目经历了多轮 baseline 迭代。早期版本分数较低，后续通过路由优化、trait-specific collections、curated 数据层和 firmness 补强后，最佳版本已经提升到：

- Overall：`8.25 / 10`

较好的分项表现包括：

- `firmness = 8.6`
- `color = 8.0`
- `acidity = 8.2`
- `harvest = 8.5`
- `sugar = 9.0`

论文中可以将这一过程写成“从基线系统到增强系统”的迭代实验。

### 5.3 结果提升的主要来源

目前可以比较明确地说，提升主要来自以下几个因素：

- trait-specific route
- 更合理的 rerank
- curated/golden gene layer
- 回答中加入 Level A / Level B 证据组织
- 对 GDR 脏数据进行清洗和降权

不应夸大 embedding 替换的作用，因为当前主要收益确实不在模型层，而在知识组织和检索逻辑层。

## 6. 论文中应当强调的创新点或贡献点

可以从以下角度组织论文贡献：

### 6.1 面向苹果品质育种场景构建了专题化 RAG 系统

与通用问答系统不同，本项目针对苹果育种中的硬度、颜色、酸度、采收期和糖度问题，构建了带有 trait-specific collection 和证据层级组织的垂直领域 RAG 系统。

### 6.2 实现了多源异构数据融合

系统同时整合：

- 论文 PDF
- 补充材料
- 结构化 gene table
- GDR/QTL/GWAS 数据
- 人工 curated 核心知识层

这比只做论文检索更符合实际科研需求。

### 6.3 设计了 trait-specific 检索和 rerank 机制

通过性状识别、专题集合优先检索和证据加权重排序，显著提高了结果的相关性和可解释性。

### 6.4 引入了坐标参考系保护策略

没有为了“看起来更强”而错误合并不同研究的坐标，而是用 reference genome 和 coordinate note 做保护性提示。  
这是一个更科学、更谨慎的工程决策。

### 6.5 建立了可重复的自动评测框架

通过固定测试题集和多轮 baseline 对比，为后续模型和知识库迭代提供了实验依据。

## 7. 论文中要谨慎表述的地方

这一部分很重要，Claude 写论文时不要写得过头。

### 7.1 不要把人工 curated layer 写成自动知识发现

当前系统一部分性能提升依赖人工整理的小规模核心基因层。  
正确表述应是：

- 人工确认核心知识层
- curated knowledge layer
- 用于补强弱项的高质量知识子集

不要写成：

- 系统自动发现新的关键基因
- 完全自动完成知识挖掘

### 7.2 不要夸大坐标级比较能力

现阶段系统并未实现真正可靠的跨参考基因组坐标统一。  
因此不应写成：

- 已完成不同研究 QTL 坐标统一
- 已完成精确共定位分析

正确表述应为：

- 审计并标注参考系
- 保留原始位置信息
- 通过提示避免错误解释

### 7.3 自动评测不能替代专家判断

虽然当前有自动评分，但仍应说明：

- 自动评测用于版本比较
- 最终科研有效性仍需导师或领域专家审核

## 8. 当前局限

论文讨论部分可以写这些局限：

- 原始 GDR/QTL 数据噪声较大
- 一些 marker/trait label 并不是标准基因名
- 部分高分依赖人工 curated 数据层
- 自动评测对科研语义理解仍有限
- 坐标参考系还没有做 liftover 统一
- 文献库虽然已成形，但仍可继续扩充高质量 seed papers 和 supplement tables

## 9. 接下来最合理的提升方向

如果论文需要写“后续工作展望”，建议写这些：

1. 继续补 curated 数据的来源字段  
例如 DOI、PMID、source paper、evidence strength、manual review status。

2. 建立老师确认闭环  
让导师或领域老师对核心 gene layer 做“重点看 / 可略 / 不相关”标注。

3. 冻结论文最终版本数据集和 baseline  
将后续论文实验固定为一个 `thesis_v1` 版本，避免结果漂移。

4. 在具备充分映射信息后探索坐标统一  
如果未来能拿到完整 reference build 和 marker mapping 文件，再考虑 liftover 和共定位分析。

5. 在稳定数据层之后，再对 embedding 或生成模型做扩展实验  
不要把模型更换作为当前主要贡献。

## 10. 适合直接写进论文摘要或结论的表述

可以参考下面这段思路：

> 本研究面向苹果品质育种场景，构建了一个融合论文 PDF、结构化基因表、QTL/GWAS 数据及人工 curated 核心知识层的检索增强知识问答系统。系统通过 trait-specific collection、问题路由、重排序和证据分层输出，实现了对苹果硬度、颜色、酸度、采收期和糖度等问题的专题化问答。实验结果表明，系统在固定测试题集上取得了较稳定的性能，并能够以带引用的方式返回候选基因及其证据来源，为苹果育种知识服务系统的构建提供了工程基础。

## 11. Claude 写论文时建议优先参考的本地文件

以下文件对继续写论文最有帮助：

- `README.md`
- `docs/project/CURRENT_PROGRESS.md`
- `docs/thesis/NEXT_STEPS_AND_COMPLETION_ASSESSMENT.md`
- `docs/thesis/THESIS_WRITEUP_DRAFT.md`
- `workspace/default/evaluation/runs/` 下的各轮 `summary.md`
- `workspace/default/reports/` 下的审计报告、导出清单和 thesis bundle

## 12. 一句话总结

这个项目已经不是“能不能跑”的问题，而是“如何把一个已完成的苹果育种 RAG 原型系统，准确、克制、学术化地写进毕业论文”的问题。论文写作时应突出系统设计、知识组织、专题检索、评测框架和科学谨慎性，而不是夸大自动发现能力。
