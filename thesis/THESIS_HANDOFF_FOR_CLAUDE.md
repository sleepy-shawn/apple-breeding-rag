# Apple Breeding RAG Thesis Handoff

本文档用于给 Claude 或其他写作助手快速建立当前最终版本上下文。  
请以本文件为准，不要再引用旧的 `docs/` 结构或早期库存数字。

更新时间：2026-04-22

## 1. 一句话项目定义

本项目是一个面向苹果品质育种场景的专题化 RAG 系统，融合论文 PDF、补充材料、结构化 gene 表、QTL/GWAS 数据和人工 curated 核心知识层，用于回答“某个品质性状相关的重要候选基因是什么、证据来自哪里、证据强弱如何”这一类科研问题。

聚焦的 trait：

- `firmness`
- `color`
- `acidity`
- `harvest`
- `sugar`

## 2. 论文写作时应采用的最终版本口径

### 2.1 最终论文库

当前最终论文库已经冻结为：

- `50` 组正式论文条目
- `70` 个 PDF 文件
- 其中主论文 `54` 个
- 补充材料/附件 `16` 个

对应盘点文件：

- `workspace/default/reports/paper_inventory_summary.md`
- `workspace/default/reports/backend_paper_inventory.csv`

### 2.2 本轮最终新增并已 ingest 的论文

2026-04-22 已作为“最终版新增论文”加入并完成 ingest 的 paper ID：

- `055`
- `056`
- `057`
- `058`
- `059`
- `060`
- `062`
- `063`
- `064`
- `065`
- `066`

这些论文已经进入后端 `papers` collection。

### 2.3 当前 papers collection 状态

- Qdrant collection：`papers`
- 当前向量点数：`2934`

这说明新增 final papers 已经进入在线检索系统，不再只是本地 PDF 文件。

### 2.4 当前最终 gene 数据口径

当前 `backend/data/genes/` 已经收口为三层：

1. 最终运行层
   - `genes.csv`
   - `genes_<trait>_curated.csv`
   - `genes_gdr.csv`
   - `genes_gdr_<trait>.csv`
   - `genes_gdr_curated.csv`
   - `genes_gdr_curated_<trait>.csv`

2. 原始材料层
   - `backend/data/genes/raw_candidates/`
   - 用于保留补充材料和原始候选基因表，支撑可复现的数据转换流程

3. 历史归档层
   - `backend/data/genes/archive/`
   - 包含早期 trait 子表、中间产物、空表和当前毕设主线未接入的数据

可直接写进论文的口径是：

- 当前最终 gene 运行层共有 `18` 个核心 CSV
- 其中包含通用 gene 检索底座、5 个 trait-specific curated 表、GDR 总表、5 个 GDR trait 子表、GDR curated 总表和 5 个 GDR curated trait 子表

## 3. 最终应引用的评测结果

### 3.1 final thesis version 的冻结结果

如果论文要写“当前最终版本结果”，应优先采用：

- run name：`baseline_final_paper_set`
- 路径：`workspace/default/evaluation/runs/baseline_final_paper_set/summary.md`

结果如下：

| Trait | Avg Total |
|------|-----------|
| Overall | 8.2/10 |
| Firmness | 8.6/10 |
| Color | 8.0/10 |
| Acidity | 8.2/10 |
| Harvest | 8.5/10 |
| Sugar | 9.0/10 |
| General | 7.0/10 |

其他指标：

- Retrieval hit rate：`1.0`
- Citation rate：`1.0`
- Level distinction rate：`1.0`
- Error count：`0`

### 3.2 旧 baseline 如何处理

项目中还有一版更早的最佳结果：

- `baseline_firmness_texture_curated`
- Overall：`8.25/10`

但这版结果对应的是 final paper freeze 之前的论文库。  
如果论文强调“最终系统版本”，不要把 `8.25/10` 当作最终结果直接使用。更稳妥的写法是：

- `baseline_firmness_texture_curated` 用于说明系统迭代过程中的历史最佳结果
- `baseline_final_paper_set` 用于说明当前最终论文集冻结后的系统结果

## 4. 当前项目目录结构

项目根目录：`/Users/shuaige/code/apple-breeding-rag`

核心目录：

- `backend/`
  - FastAPI、RAG 检索、ingest、数据配置。

- `frontend/`
  - Next.js Web 前端、聊天界面、上传入口、LLM 浏览器本地配置。

- `scripts/`
  - 当前仍在使用的主线脚本。

- `workspace/`
  - 当前工作区，只保留最终 baseline 与精选报告。

- `thesis/`
  - 当前论文正文、格式修订版、Claude handoff。

- `archive/`
  - 学校材料、历史归档和历史脚本。

## 5. 系统方法可以怎样写进论文

可以把系统概括为四层：

1. 数据获取与整理层  
   负责论文收集、PDF 整理、gene/QTL/GWAS 表清洗、curated layer 构建。

2. 检索与问答服务层  
   基于 FastAPI 和 Qdrant 构建后端，支持 trait-specific collection、route、rerank 和证据型回答。

3. 评测与验证层  
   通过固定题集、自动评测脚本和多轮 baseline 对系统进行比较。

4. 前端交互层  
   提供聊天、上传 PDF、上传 gene 表和本地 LLM Key 配置。

## 6. 当前最值得强调的工程工作

### 6.1 trait-specific collections

系统没有只用一个统一 `genes` 库，而是拆成：

- `genes`
- `genes_firmness`
- `genes_color`
- `genes_acidity`
- `genes_harvest`
- `genes_sugar`
- `genes_gdr`
- `genes_gdr_curated_*`

这样做的理由是：苹果品质性状问题是强专题性的，不同 trait 混在一个语义空间里会带来明显噪声。

### 6.2 trait-specific route + rerank

在 `backend/app/rag.py` 中已经实现：

- 问题 trait 识别
- trait-specific 集合优先检索
- paper + gene hybrid retrieval
- 基于 gene name / candidate gene / source title / trait 匹配的重排序

这一部分是性能提升的关键来源。

### 6.3 curated / golden knowledge layer

项目后期为了补强弱项，引入了小规模人工 curated 层，尤其补强了：

- firmness
- harvest
- sugar

这一层的价值在于：

- 用高质量、可解释的核心证据补强问答
- 避免把大量噪声 QTL/marker 直接当作主答案

### 6.4 QTL/GWAS reference guard

系统没有强行把不同研究的 `chr + pos` 当成同一参考系，而是采取保护性策略：

- 保留原始 `chr/pos`
- 保留 `reference_genome`
- 在回答中提示不要跨研究直接合并坐标
- 不做 liftover

这是一个“更谨慎而不是更炫”的工程决策。

## 7. 论文里哪些点可以写成贡献

可以重点写这些：

1. 面向苹果品质育种场景构建了专题化 RAG 系统。
2. 融合论文 PDF、补充材料、结构化 gene 表和 GDR/QTL/GWAS 数据。
3. 设计了 trait-specific route 与 rerank 机制，提高相关性和可解释性。
4. 建立了可重复的自动评测框架。
5. 对 QTL/GWAS 坐标参考系采用了保护性审计与提示机制，避免错误解释。
6. 对最终 gene 数据目录进行了运行层、原始材料层和历史归档层的分层治理，提升了项目可维护性。

## 8. 论文里必须克制的表述

### 8.1 不要把人工 curated layer 写成自动知识发现

正确写法：

- 人工确认核心知识层
- curated knowledge layer
- 用于补强弱项的高质量知识子集

不要写成：

- 系统自动发现新的关键基因
- 系统自主完成知识挖掘

### 8.2 不要夸大坐标统一能力

不要写：

- 已完成跨研究 QTL 坐标统一
- 已实现精确共定位分析

正确写法：

- 审计并标注参考基因组
- 保留原始位置
- 在回答中提示参考系风险

### 8.3 自动评测不能替代专家判断

自动评测应写成：

- 用于比较系统版本
- 用于发现弱项和检索回归
- 最终有效性仍需导师或领域专家确认

## 9. 当前推荐 Claude 参考的本地文件

优先级从高到低：

1. `CURRENT_STATUS.md`
2. `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`
3. `workspace/default/evaluation/runs/baseline_final_paper_set/summary.md`
4. `workspace/default/reports/paper_inventory_summary.md`
5. `README.md`
6. `backend/data/genes/README.md`

如果需要展开细节，再看：

- `backend/app/rag.py`
- `backend/app/ingest.py`
- `backend/app/main.py`
- `workspace/default/reports/qtl_reference_system_audit.md`

## 10. 现在最适合写进摘要或结论的表述

可以参考下面这段思路：

> 本研究面向苹果品质育种场景，构建了一个融合论文 PDF、结构化基因表、QTL/GWAS 数据及人工 curated 核心知识层的检索增强知识问答系统。系统通过 trait-specific collection、问题路由、重排序和证据分层输出，实现了对苹果硬度、颜色、酸度、采收期和糖度等问题的专题化问答。基于最终冻结的论文集与固定测试题集，系统在自动评测中取得了较稳定表现，并能够以带引用的方式返回候选基因及其证据来源，为苹果育种知识服务系统的构建提供了工程基础。

## 11. Cleanup Assumptions Already Applied

为了把项目收成“毕业设计最终版本”，本轮已经默认采用以下假设：

1. `thesis/葛帅毕业论文_格式修订版.docx` 作为当前活跃论文主文件。
2. 候选抓取池已转入 `archive/history/workspace-source/`，不再作为当前 workspace 活跃内容。
3. 旧 baseline `baseline_firmness_texture_curated` 已转入 `archive/history/evaluation-runs/`，当前结果只保留 `baseline_final_paper_set`。
4. `workspace/default/` 已收缩为最终 baseline 与精选报告快照，旧 pipeline 骨架不再保留在当前工作区。
5. 历史阶段脚本已转入 `archive/history/scripts/`，当前 `scripts/` 只保留主线脚本。
