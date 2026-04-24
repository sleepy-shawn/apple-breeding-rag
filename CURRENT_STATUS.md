# Current Status

更新时间：2026-04-23

## Final Thesis Snapshot

当前项目已经按“毕业设计最终答辩版本”口径冻结到一版可写论文、可继续演示、可交给写作助手继续维护的状态。

- 最终论文库当前为 `50` 组正式论文条目。
- `backend/data/papers` 当前共有 `70` 个 PDF，其中主论文 `54` 个，补充材料/附件 `16` 个。
- `papers` collection 当前为 `2934` 个向量点，说明最终论文集已经进入在线检索系统。
- 当前论文主文件为 `thesis/实验进行中-gpt修改版本.docx`。

论文库盘点文件见：

- `workspace/default/reports/paper_inventory_summary.md`
- `workspace/default/reports/backend_paper_inventory.csv`

## Final Gene Data Snapshot

当前基因数据目录已按“最终运行层优先”收口。

- 当前顶层运行核心为 `18` 个 CSV：
  - `genes.csv`
  - `genes_*_curated.csv` 共 `5` 个
  - `genes_gdr.csv`
  - `genes_gdr_<trait>.csv` 共 `5` 个
  - `genes_gdr_curated.csv`
  - `genes_gdr_curated_<trait>.csv` 共 `5` 个
- 当前仓库仅保留运行核心 CSV，不再保留原始候选材料和过程性中间产物。

基因数据说明见：

- `backend/data/genes/README.md`

## Final Evaluation Result

当前论文正文应统一采用 `workspace/default/evaluation/ablation/` 下的 28 题消融实验结果。

当前正式评测口径：

- 题集规模：`28` 题
- 评测配置：`A0 No-RAG`、`A1 Papers-only`、`A2 Genes-only`、`A3 Hybrid`
- 机制维度：`LLM-as-Judge` 自动评分（DeepSeek）
- 论文最终应引用：`A3 Hybrid（完整系统）`

完整系统结果：

| Category | Avg Total |
|----------|-----------|
| Overall | 7.07/10 |
| Color | 8.2/10 |
| Firmness | 7.6/10 |
| Harvest | 7.5/10 |
| Acidity | 7.0/10 |
| Sugar | 6.25/10 |
| General | 5.8/10 |

关键指标：

- Citation rate：`100%`
- Evidence stratification rate：`86%`
- Gene recall：约 `81%`
- 最优配置：`A3 Hybrid`

对应文件：

- `workspace/default/evaluation/ablation/run_notes.md`
- `workspace/default/evaluation/ablation/ablation_table.md`
- `workspace/default/evaluation/ablation/trait_detail_table.md`
- `workspace/default/evaluation/Table_5_1_ablation_results.docx`

## Current Project Layout

当前项目只保留几条清晰主线：

- `backend/`
  - FastAPI、RAG 检索、ingest 和数据配置。
- `frontend/`
  - Web 界面、上传入口、LLM 本地配置和展示页。
- `scripts/`
  - 当前仍在使用的主线脚本。
- `thesis/`
  - 当前论文正文、活跃主文件和 handoff。
- `workspace/`
  - 当前论文仍直接引用的评测结果与报告。
## Current Thesis Files

当前 `thesis/` 下真正活跃的文件是：

- `thesis/实验进行中-gpt修改版本.docx`
- `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`

如果需要给写作助手建立上下文，优先使用：

1. `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`
2. `workspace/default/evaluation/ablation/run_notes.md`
3. `workspace/default/evaluation/ablation/ablation_table.md`
4. `workspace/default/evaluation/ablation/trait_detail_table.md`
5. `workspace/default/reports/paper_inventory_summary.md`

## Current System Capability

Apple Breeding RAG 当前已经具备：

- 论文 PDF 检索
- 结构化 gene/QTL/GWAS 检索
- trait-specific collections
- 带引用与 Level A / Level B 的证据型回答
- 前端上传 PDF 和 gene 文件
- 自动化消融评测

当前服务入口：

- Backend：`http://localhost:8000`
- Frontend：`http://localhost:3000`
- Qdrant：`http://localhost:6333/dashboard`

## Things To State Carefully

- `firmness / harvest / sugar` 的提升部分依赖人工 curated 层，应表述为“人工确认核心知识层”，不要写成系统自动发现的新知识。
- `general` 类得分较低与题型设计有关，不应简单解读为系统在方法类问题上完全失效。
- QTL/GWAS 坐标仍采用保护性策略：
  - 保留 `reference_genome`
  - 保留 source-reported `chr/pos`
  - 不做 liftover
  - 不做跨研究坐标直接合并
- 自动评测用于版本比较与问题定位，不能替代导师或领域专家审核。

## Notes

当前主线已经默认采用：

- `thesis/实验进行中-gpt修改版本.docx` 作为活跃论文主文件
- `workspace/default/evaluation/ablation/` 作为当前论文结果口径
