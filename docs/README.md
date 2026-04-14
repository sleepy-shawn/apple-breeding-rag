# Docs Layout

`docs/` 用来承载项目说明、论文写作材料、研究笔记和老师审阅相关文件，避免这些文档继续堆在项目根目录。

## 目录说明

- `assets/`
  - 架构图、流程图、论文插图等静态资源。

- `project/`
  - 项目阶段性进展、开发记录、里程碑说明。

- `research/`
  - 原始研究笔记、抽取文本、大段整理材料。

- `review/`
  - 给老师或人工审阅使用的清单、Excel、评审导出表。

- `thesis/`
  - 毕业论文写作辅助材料、给 Claude 的交接文档、写作草稿和完成度判断。

## 归档原则

- 根目录尽量只保留运行和开发直接相关的内容：
  - `backend/`
  - `frontend/`
  - `scripts/`
  - `config/`
  - `workspace/`
  - `archive/`
  - `README.md`
  - `docker-compose.yml`

- 论文写作与审阅材料优先放到 `docs/`。
- 大体积原始模板、学校表格和历史资料继续放在 `archive/`。
