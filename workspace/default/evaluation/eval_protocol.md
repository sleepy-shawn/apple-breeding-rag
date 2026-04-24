# 苹果育种 RAG 系统评估协议

## 测试集概览

| 类别 | 题目数 | 覆盖性状 |
|------|--------|----------|
| 硬度/质地 (F) | 5题 | MdNAC18, MdNAC5, MdPG, MdEXP, MdACS/ACO |
| 颜色/花青素 (C) | 5题 | MdMYB1/10, MdDFR, MdANS, MdHY5, MdCOP1 |
| 酸度/苹果酸 (A) | 5题 | Ma1/MdALMT9, MdVHP1, MdPEPC, MdMYB73 |
| 成熟期/贮藏性 (H) | 4题 | MdNAC18, MdACS/ACO, MdBPM2/MdRGLG3/MdNAC83, MdHDT3 |
| 糖分 (S) | 4题 | MdSUT, MdINV, MdSWEET9b, MdWRKY9, MdCIbHLH1 |
| 通用/方法 (G) | 5题 | GWAS vs QTL, 染色体热点, RAG vs LLM, KASP, pan-genome |
| **合计** | **28题** | |

新增题目覆盖：
- `S002-S004`：ABA-MdSWEET9b 糖积累、MdCIbHLH1 调控糖代谢、SSC 基因组选择
- `H003-H004`：MdBPM2/MdRGLG3-MdNAC83 贮藏性网络、MdHDT3 表观遗传调控乙烯
- `G003-G005`：RAG 对比纯 LLM、KASP 育种转化、苹果泛基因组意义

## 评分标准

每道题满分 10 分，分四个维度：

### 1. 基因命中率 (Gene Recall, 4分)
- 4分：答案中提及所有 expected_genes 中的基因
- 3分：提及 >75% 的期望基因
- 2分：提及 >50% 的期望基因
- 1分：提及 >25% 的期望基因
- 0分：未提及任何期望基因

### 2. 机制准确性 (Mechanism Accuracy, 3分)
- 3分：准确描述基因功能和作用机制，无错误
- 2分：大体正确，有少量不精确
- 1分：部分正确
- 0分：错误或无关

### 3. 引用可追溯性 (Citation Traceability, 2分)
- 2分：答案中有明确的引用编号，对应真实证据源
- 1分：有引用但来源不清晰
- 0分：无引用

### 4. 证据分级 (Evidence Level, 1分)
- 1分：正确区分了 Level A（遗传关联）和 Level B（支持证据）
- 0分：未区分

## 评测链路

正式评测分三步：

1. `run_ablation.py`
   运行 4 种系统配置（A0 No-RAG、A1 papers-only、A2 genes-only、A3 hybrid），输出逐题结果到 `workspace/default/evaluation/ablation/ablation_results.csv`
2. `llm_judge.py`
   对 `mechanism_score_manual` 为空的记录做 LLM-as-Judge 自动机制评分，填充 `mechanism_score_auto` 和 `judge_reason`
3. `generate_report.py`
   基于 judged CSV 生成论文可直接使用的对比表和按性状汇总表

## 配置说明

| 配置 | 名称 | 说明 |
|------|------|------|
| A0 | No-RAG | 直接调用基础 LLM，不经过 `/api/chat` |
| A1 | Papers-only | `/api/chat` + `route="papers"` |
| A2 | Genes-only | `/api/chat` + `route="genes"` |
| A3 | Hybrid | `/api/chat` + `route="hybrid"` |

## 运行前提

- `docker compose up -d` 已启动 backend / qdrant / web
- 若要运行 `A0` 和 `llm_judge.py`，必须配置 `LLM_API_KEY`
- `LLM_API_KEY` 可通过 shell 环境变量提供，也可写入 `backend/.env`
- 如果未配置 `LLM_API_KEY`，当前后端会退化为“检索摘要模式”，此时 A1/A2/A3 仍可运行，但 A0 与真实自动判分不可用

## 运行命令

```bash
# 启动系统
docker compose up -d

# 单次问答检查
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "...", "route": "auto", "top_k": 6}'

# 运行消融实验（默认 28 题）
python scripts/evaluation/run_ablation.py \
  --output workspace/default/evaluation/ablation

# 若当前没有 LLM key，可先只跑 RAG 三组
python scripts/evaluation/run_ablation.py \
  --configs A1,A2,A3 \
  --output workspace/default/evaluation/ablation

# 自动机制评分
python scripts/evaluation/llm_judge.py \
  --input workspace/default/evaluation/ablation/ablation_results.csv \
  --output workspace/default/evaluation/ablation/ablation_results_judged.csv

# 生成论文表格
python scripts/evaluation/generate_report.py \
  --input workspace/default/evaluation/ablation/ablation_results_judged.csv
```

输出文件：

- `ablation_results.csv`：逐题逐配置结果
- `ablation_results.jsonl`：带原始回答与 source 细节的版本
- `ablation_results_judged.csv`：补齐机制评分后的正式结果
- `ablation_summary.json`：按配置与性状聚合
- `ablation_table.md`：论文总表
- `trait_detail_table.md`：Hybrid 性状分表

## 基线性能目标（毕业论文）

| 指标 | 目标值 |
|------|--------|
| 硬度性状 F1 基因命中率 | ≥ 80% |
| 颜色性状 F1 基因命中率 | ≥ 70% |
| 酸度性状 F1 基因命中率 | ≥ 70% |
| 整体 Citation Rate | ≥ 85% |
| Level A/B 正确区分率 | ≥ 75% |

## 结果解释注意事项

- `gene_score`、`citation_score`、`level_score` 由脚本规则自动计算
- `mechanism_score_auto` 由 judge 模型打分，是唯一依赖外部 LLM 凭据的评分维度
- `full_total` 只有在 `mechanism_score_auto` 填充后才是正式总分
- 当前 `score_answer()` 仍沿用现有规则，不在本轮升级中重写
