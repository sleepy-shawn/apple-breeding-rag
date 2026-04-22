# Workspace Layout

`workspace/` 现在是一个“最终版工作区快照”。这里不再保留旧 pipeline 骨架、候选抓取池或历史状态缓存，只保留论文里仍直接引用的 baseline 与报告。

## 当前结构

- `default/evaluation/`
  - 固定题集、评测协议和当前冻结的 thesis baseline。

- `default/reports/`
  - 当前仍直接需要查看的精选报告，不再保留导师审阅表。

## 已清理内容

- 旧 baseline 已迁移到 `archive/history/evaluation-runs/`
- 原先杂乱的派生报告已迁移到 `archive/history/workspace-reports/`
- `workspace/` 现在只保留“当前论文还会直接引用”的部分

## 当前保留的主 baseline

- `workspace/default/evaluation/runs/baseline_final_paper_set/`

## 当前保留的关键报告

- `workspace/default/reports/paper_inventory_summary.md`
- `workspace/default/reports/backend_paper_inventory.csv`
- `workspace/default/reports/qtl_reference_system_audit.md`

## 使用原则

- 如果将来重新开启 pipeline，可运行 `scripts/pipeline/init_pipeline_workspace.py` 重新生成完整工作区骨架
- 历史实验结果不再留在当前工作区，统一放入 `archive/history/`
