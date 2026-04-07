# Current Progress

更新时间：2026-04-07

## 当前系统状态

Apple Breeding RAG 已经形成一个可运行、可评测、可继续扩展的苹果品质育种 RAG 原型系统。当前系统包含论文 PDF 检索、基因/QTL/GWAS 表格检索、trait-specific 路由、证据型回答生成、前端交互和自动化 baseline 评测。

后端 Docker 已重建，当前服务健康检查通过：

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Qdrant: `http://localhost:6333/dashboard`

## 最新优化

本轮重点攻克之前较弱的 `harvest` 和 `sugar` 两类问题。

新增人工确认核心知识层：

- `backend/data/genes/genes_harvest_curated.csv`
- `backend/data/genes/genes_sugar_curated.csv`

新增或接入的 collections：

- `genes_harvest`
- `genes_sugar`

对应代码改动：

- `backend/app/settings.py`：新增 harvest/sugar collection 与自动 ingest 文件配置。
- `backend/app/main.py`：新增 harvest/sugar ingest endpoint 和 startup auto-ingest。
- `backend/app/rag.py`：将 harvest/sugar golden collections 加入 trait-specific 检索路由。

## 最新评测结果

最新 baseline：

- Run: `baseline_harvest_sugar_golden`
- 输出目录：`workspace/default/evaluation/runs/baseline_harvest_sugar_golden/`

自动评测结果：

| Trait | Avg Total |
|------|-----------|
| Overall | 7.8/10 |
| Firmness | 6.8/10 |
| Color | 8.0/10 |
| Acidity | 8.2/10 |
| Harvest | 8.5/10 |
| Sugar | 9.0/10 |
| General | 7.5/10 |

其他指标：

- Retrieval hit rate: `1.0`
- Citation rate: `1.0`
- Level distinction rate: `1.0`
- Error count: `0`

与上一版 `baseline_ingest_repair_trait_dedupe` 相比，主要提升来自：

- Harvest: `5.0 -> 8.5`
- Sugar: `5.0 -> 9.0`
- Overall: `7.25 -> 7.8`

## 重要说明

Harvest/sugar 的提升来自少量人工整理的 golden gene layer。这一层适合作为系统能力验证和毕业设计原型展示，但在论文中应表述为“人工确认核心知识层”或“curated knowledge layer”，不要表述成系统自动发现的新生物学结论。

后续最好让老师确认：

- `MdNAC18 / MdACS1 / MdACO1 / MdETR1 / MdEIN3` 是否适合作为 harvest/ripening 核心知识。
- `MdSUT1 / MdSUT4 / MdINV / MdSPS / MdHXK1` 是否适合作为 sugar/sucrose 核心知识。
- 当前 evidence_text 的措辞是否足够严谨。

## 下一步建议

1. 优先补强 firmness 中 `Honeycrisp` 脆度/硬度相关题目，因为 firmness 仍是当前最低分 trait。
2. 等老师反馈后，把确认过的核心文献 supplement 表整理为更可靠的 trait-specific curated dataset。
3. 在换 embedding 模型前，继续优先提高知识库质量和证据表结构化程度。
