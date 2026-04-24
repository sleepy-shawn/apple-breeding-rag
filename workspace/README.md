# Workspace Layout

`workspace/` 现在是一个“论文最终版工作区快照”。这里不再保留旧 pipeline 骨架、候选抓取池或历史状态缓存，只保留论文里仍直接引用的评测结果与报告。

## 当前结构

- `default/evaluation/`
  - 固定题集、评测协议、28 题消融实验结果和表 5-1 导出文件。

- `default/reports/`
  - 当前仍直接需要查看的精选报告，不再保留导师审阅表。

## 当前论文应直接引用的评测入口

- `workspace/default/evaluation/ablation/run_notes.md`
- `workspace/default/evaluation/ablation/ablation_table.md`
- `workspace/default/evaluation/ablation/trait_detail_table.md`
- `workspace/default/evaluation/Table_5_1_ablation_results.docx`

## 当前保留的关键报告

- `workspace/default/reports/paper_inventory_summary.md`
- `workspace/default/reports/backend_paper_inventory.csv`
- `workspace/default/reports/qtl_reference_system_audit.md`

## 使用原则

- 当前论文与答辩统一采用 `ablation/` 下的 28 题消融实验结果。
- 历史实验结果不再作为当前版本主结果，统一视为追溯材料。
- 如果将来重新开启 pipeline，可运行 `scripts/pipeline/init_pipeline_workspace.py` 重新生成完整工作区骨架。
