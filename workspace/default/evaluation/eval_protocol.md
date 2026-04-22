# 苹果育种 RAG 系统评估协议

## 测试集概览

| 类别 | 题目数 | 覆盖性状 |
|------|--------|----------|
| 硬度/质地 (F) | 5题 | MdNAC18, MdNAC5, MdPG, MdEXP, MdACS/ACO |
| 颜色/花青素 (C) | 5题 | MdMYB1/10, MdDFR, MdANS, MdHY5, MdCOP1 |
| 酸度/苹果酸 (A) | 5题 | Ma1/MdALMT9, MdVHP1, MdPEPC, MdMYB73 |
| 成熟期 (H) | 2题 | MdNAC18, MdACS, MdACO |
| 糖分 (S) | 1题 | MdSUT, MdINV |
| 通用/方法 (G) | 2题 | GWAS vs QTL, 染色体热点 |
| **合计** | **20题** | |

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

## 运行评估

```bash
# 启动系统
docker compose up -d

# 对每个问题查询API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "...", "route": "auto", "top_k": 6}'

# 或使用评估脚本
cd scripts
python run_evaluation.py \
  --test-file ../workspace/default/evaluation/test_questions.jsonl \
  --output ../workspace/default/evaluation/results_$(date +%Y%m%d).jsonl
```

## 基线性能目标（毕业论文）

| 指标 | 目标值 |
|------|--------|
| 硬度性状 F1 基因命中率 | ≥ 80% |
| 颜色性状 F1 基因命中率 | ≥ 70% |
| 酸度性状 F1 基因命中率 | ≥ 70% |
| 整体 Citation Rate | ≥ 85% |
| Level A/B 正确区分率 | ≥ 75% |

## 对比实验建议

为增强毕业论文说服力，建议做以下消融实验：

1. **无性状专属collection** vs **有性状专属collection**（当前设计）
2. **all-MiniLM-L6-v2** vs **BAAI/bge-base-en-v1.5**（已升级）
3. **仅papers** vs **hybrid（papers+genes）**
4. **无rerank** vs **有关键词rerank**（当前设计）
