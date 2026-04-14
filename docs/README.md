# Docs Layout

`docs/` 用于集中管理项目说明、研究笔记、老师审阅材料和毕业论文写作辅助文档。这里的内容默认不参与运行时 ingest，也不作为在线服务依赖项，而是服务于开发协作、论文撰写和答辩准备。

## 目录结构

- `assets/`
  - 架构图、流程图、论文插图和答辩可复用的静态资源。

- `project/`
  - 项目进展、阶段性里程碑、版本说明和当前状态总结。

- `research/`
  - 原始研究笔记、摘录文本、人工梳理材料和过程性分析文档。

- `review/`
  - 给老师或人工审阅使用的清单、Excel、文献列表和导出报表。

- `thesis/`
  - 毕业论文写作支持文件，包括给 Claude 的交接材料、章节草稿和完成度判断。

## 使用原则

- 与运行直接相关的内容优先保留在项目根目录及其运行子目录：
  - `backend/`
  - `frontend/`
  - `scripts/`
  - `config/`
  - `workspace/`
- 写作、审阅、说明和研究记录优先放入 `docs/`。
- 大体积模板、学校过程材料和历史归档优先放入 `archive/`，避免与当前工作文档混放。

## 当前重要文档

- `project/CURRENT_PROGRESS.md`
  - 当前系统状态、最近完成的能力和建议的下一步。

- `thesis/THESIS_HANDOFF_FOR_CLAUDE.md`
  - 适合交给 Claude 继续写论文的项目交接说明。

- `thesis/NEXT_STEPS_AND_COMPLETION_ASSESSMENT.md`
  - 当前完成度、成品差距和后续优先级判断。

- `review/literature_list_for_supervisor.xlsx`
  - 给老师审阅使用的文献列表。

- `assets/apple_breeding_rag_architecture.svg`
  - 可用于论文或答辩展示的系统架构图。

## 维护建议

- 新增写作材料时，优先按用途归类，而不是继续堆放到根目录。
- 如果某份文档只用于历史保存而不再维护，请移动到 `archive/`。
- 对外分享项目时，优先引用根 README 和本目录说明，避免直接引用过程性草稿。
