# Current Status

更新时间：2026-04-22

## Final Thesis Snapshot

当前项目已经按“毕业设计最终版本”口径冻结到一版可写论文、可交给 Claude、可继续演示的状态。

- 最终论文库当前为 `50` 组正式论文条目。
- `backend/data/papers` 当前共有 `70` 个 PDF，其中主论文 `54` 个，补充材料/附件 `16` 个。
- 2026-04-22 新增并已 ingest 的 final papers 为：
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
- `papers` collection 当前为 `2934` 个向量点，说明新增论文已经进入在线检索系统。

论文库盘点文件见：

- `workspace/default/reports/paper_inventory_summary.md`
- `workspace/default/reports/backend_paper_inventory.csv`

## Final Gene Data Snapshot

当前基因数据目录已按“最终运行层 + 原始材料层 + 历史归档层”收口。

- 当前顶层运行核心为 `18` 个 CSV：
  - `genes.csv`
  - `genes_*_curated.csv` 共 `5` 个
  - `genes_gdr.csv`
  - `genes_gdr_<trait>.csv` 共 `5` 个
  - `genes_gdr_curated.csv`
  - `genes_gdr_curated_<trait>.csv` 共 `5` 个
- `raw_candidates/` 继续保留，用于原始候选材料和可复现的数据转换流程
- `genes_acidity.csv`、`genes_structured.csv`、`sample_genes.csv`、`genes_gdr_polyphenol.csv` 等非运行核心文件已移入 `backend/data/genes/archive/`

基因数据说明见：

- `backend/data/genes/README.md`

## Final Evaluation Result

如果后续论文只采用“最终论文集冻结后”的结果，应该优先引用下面这一版：

- Final frozen baseline：`baseline_final_paper_set`
- 路径：`workspace/default/evaluation/runs/baseline_final_paper_set/`

自动评测结果：

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

如果论文中需要展示“迭代提升过程”，可以补充说明：

- `baseline_firmness_texture_curated` 是 final paper freeze 之前的最佳历史结果，Overall 为 `8.25/10`
- `baseline_final_paper_set` 是当前最终论文集对应的冻结结果，Overall 为 `8.2/10`

写论文时不要混用这两版口径。若强调“最终系统版本”，应优先使用 `baseline_final_paper_set`。

## Current Project Layout

当前项目只保留几条清晰主线：

- `backend/`
  - FastAPI、RAG 检索、ingest 和数据配置。
- `frontend/`
  - Web 界面、上传入口、LLM 本地配置和展示页。
- `scripts/`
  - 当前仍在使用的主线脚本。
- `thesis/`
  - 当前论文正文、格式修订版、Claude handoff。
- `workspace/`
  - 当前最终 baseline 和精选报告。
- `archive/`
  - 学校材料、历史归档和历史脚本。

## Current Thesis Files

当前 `thesis/` 下真正活跃的文件只有这些：

- `thesis/葛帅毕业论文_格式修订版.docx`
- `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`

如果需要给 Claude 建立上下文，优先使用：

1. `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`
2. `workspace/default/evaluation/runs/baseline_final_paper_set/summary.md`
3. `workspace/default/reports/paper_inventory_summary.md`
4. `README.md`

## Current System Capability

Apple Breeding RAG 当前已经具备：

- 论文 PDF 检索
- 结构化 gene/QTL/GWAS 检索
- trait-specific collections
- 带引用与 Level A / Level B 的证据型回答
- 前端上传 PDF 和 gene 文件
- 自动化 baseline 评测

当前服务入口：

- Backend：`http://localhost:8000`
- Frontend：`http://localhost:3000`
- Qdrant：`http://localhost:6333/dashboard`

## Cleanup Applied

这次已经按“final thesis version”假设完成了收口：

- 旧论文工作稿已移到 `archive/history/thesis/`
- 候选抓取池已移到 `archive/history/workspace-source/`
- 旧 baseline `baseline_firmness_texture_curated` 已移到 `archive/history/evaluation-runs/`
- 导师审阅表已从当前 `workspace/default/reports/` 中删除
- 当前 `workspace/default/` 只保留最终 baseline 和必要报告
- 一次性阶段脚本已移入 `archive/history/scripts/`

## Things To State Carefully

- `firmness / harvest / sugar` 等高分部分依赖人工 curated 或 golden layer，应表述为“人工确认核心知识层”，不要写成系统自动发现的新知识。
- QTL/GWAS 坐标仍采用保护性策略：
  - 保留 `reference_genome`
  - 保留 source-reported `chr/pos`
  - 不做 liftover
  - 不做跨研究坐标直接合并
- 自动评测用于版本比较，不能替代导师或领域专家审核。

## Notes

当前主线已经默认采用：

- `thesis/葛帅毕业论文_格式修订版.docx` 作为活跃论文主文件
- `baseline_final_paper_set` 作为最终结果口径
