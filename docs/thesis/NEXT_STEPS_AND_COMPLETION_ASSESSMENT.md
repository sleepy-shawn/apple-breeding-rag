# Next Steps and Completion Assessment

更新时间：2026-04-07

## 当前完成度判断

当前 Apple Breeding RAG 已经从 demo 阶段进入“可展示原型”阶段。按毕业设计系统完成度估计，当前约为 **75% 到 82%**。

这个判断基于以下事实：

- 数据层已经接入论文 PDF、基因/QTL/GWAS 表、GDR curated layer 和人工 golden gene layer。
- 检索层已经支持 Qdrant、trait-specific collections、rerank 和坐标参考系保护。
- 问答层已经支持证据引用、Level A/B 分层、无 LLM fallback 摘要和 LLM Key 配置。
- 前端层已经具备 Web 交互、上传 PDF、上传基因表和本地 LLM 配置入口。
- 评测层已经具备固定题集、baseline 输出、summary、CSV 和 manual review 文件。
- 文档层已有 README、CURRENT_PROGRESS、thesis framework bundle 和 QTL/GWAS reference-system audit。

最新自动评测 baseline：

- Run: `baseline_firmness_texture_curated`
- Overall: `8.25/10`
- Firmness: `8.6/10`
- Color: `8.0/10`
- Acidity: `8.2/10`
- Harvest: `8.5/10`
- Sugar: `9.0/10`
- Retrieval hit rate: `1.0`
- Citation rate: `1.0`
- Level distinction rate: `1.0`

结论：当前主要问题已经不是系统能否运行，而是知识库证据是否足够严谨、最终实验版本是否冻结、论文叙述是否清楚。

## 距离毕业设计成品还差什么

### 1. 科学证据严谨性

当前 firmness、harvest、sugar 的分数提升主要来自人工整理的 curated/golden gene layer。这在工程原型中是合理的，但论文中必须谨慎表述为“人工确认核心知识层”或“curated knowledge layer”，不能表述为系统自动发现的新生物学结论。

下一步最好补齐：

- `doi`
- `pmid`
- `source_paper_title`
- `supplement_table`
- `evidence_strength`
- `manual_review_status`

### 2. 老师人工确认

最需要老师确认的不是系统架构，而是核心知识是否适合作为毕业设计知识库证据。

优先确认：

- Firmness/Honeycrisp/texture: `MdNAC18 / MdNAC5 / MdPG / MdEXP-A1 / MdEXP / MdERF3 / MdERF118 / MdACS1 / MdACO1 / MdPAE10`
- Harvest/ripening: `MdNAC18 / MdACS1 / MdACO1 / MdETR1 / MdEIN3`
- Sugar/sucrose: `MdSUT1 / MdSUT4 / MdINV / MdSPS / MdHXK1`

### 3. 最终 baseline 冻结

当前已经有多个 baseline。论文写作时建议只冻结一个最终版本，例如：

- `baseline_thesis_v1`

冻结后，论文中的结果表、截图、系统说明都只引用这一个版本，避免不同阶段结果混在一起。

### 4. LLM 正式回答测试

当前自动评测主要基于无 LLM fallback 摘要。毕业展示前建议用实际 LLM Key 跑一轮人工样例，确认回答风格更像科研问答。

建议保存 5 到 8 个展示问题的输出：

- 硬度/Honeycrisp
- 果皮颜色/MdMYB10
- 酸度/Ma1 或 MdALMT9
- 采收期/MdNAC18 或乙烯通路
- 糖度/MdSUT 或 MdINV
- GWAS/QTL 参考坐标系说明

### 5. 前端展示稳定性

前端目前可用，但如果面向答辩，还可以做最后一轮 polish：

- 上传成功后的状态提示
- 引用卡片的证据层级展示
- 错误提示和 loading 状态
- 最终展示问题的快捷入口

这不是核心算法问题，但会影响答辩观感。

## 推荐下一步优先级

1. 让老师确认 curated/golden gene layer 的核心基因和证据描述。
2. 给 curated CSV 补 DOI、PMID、source paper、supplement table 和 evidence strength。
3. 冻结最终数据与评测版本，生成 `baseline_thesis_v1`。
4. 用真实 LLM Key 跑 5 到 8 个展示问题，保存最终截图和结果。
5. 最后再考虑 embedding 模型对比，例如 bge-base vs bge-large。

## 关于 QTL/GWAS 坐标参考系

当前不建议做复杂 liftover。

原因：

- 现有数据中混有 `GDDH13 v1.1`、`Malus x domestica Whole Genome v1.0`、`Honeycrisp Genome v1.1.a1`、`HFTH1 Whole Genome v1.0` 和少量 `Pyrus pyrifolia`。
- 如果没有明确每条记录的 genome build 和 marker 映射文件，强行统一坐标反而可能引入错误。

当前策略：

- 保留 source-reported `chr/pos`
- 保留 `reference_genome`
- 通过 `coordinate_note` 提醒不能跨研究直接合并坐标
- 不做 liftover
- 不做跨参考基因组物理共定位结论

论文推荐表述：

> 本系统保留 QTL/GWAS 数据源报告的染色体与位置信息，并记录参考基因组来源。但由于不同研究使用的参考基因组和标记系统并不完全一致，本文不进行跨研究坐标 liftover 或物理共定位合并，坐标字段仅作为来源元数据和证据追溯信息使用。

## 总体判断

当前系统已经可以支撑毕业论文中的系统设计、实现和初步实验章节。后续最关键的工作不是继续大规模改代码，而是：

- 提高 curated 数据的证据严谨性
- 建立老师人工确认闭环
- 冻结最终 baseline
- 准备答辩展示样例

一句话总结：

> 系统工程完成度已经较高，RAG 检索链路和评测框架可展示；当前主要风险是人工 curated 证据需要老师确认和来源补强。
