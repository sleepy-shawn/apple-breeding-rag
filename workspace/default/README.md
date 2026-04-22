# Default Workspace

这是项目当前唯一保留的活跃工作区，也是毕业设计最终版本默认引用的工作区快照。

## 当前保留内容

- `evaluation/`
  - 固定题集、评测协议和最终 baseline。
- `reports/`
  - 论文库存盘点和 QTL 参考系审计报告。

## 当前冻结结果

- 最终论文库盘点：`reports/paper_inventory_summary.md`
- 最终论文版 baseline：`evaluation/runs/baseline_final_paper_set/`
- 旧 baseline 若要保留，应转入 `archive/history/`，不要继续当作当前版本主结果
- 候选抓取池已归档到 `archive/history/workspace-source/source_papers_candidate_pool_2026-04-22/`

## 说明

旧评测结果、候选抓取池、状态缓存和旧报告已经迁移到 `archive/history/`。如果后续需要重新开启抓取和 staging 流程，可以运行 `python3 scripts/pipeline/init_pipeline_workspace.py` 重新生成完整工作区骨架。
