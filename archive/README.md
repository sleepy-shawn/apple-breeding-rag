# Archive Layout

`archive/` 用于存放不直接参与系统运行、但需要长期保留的毕业设计资料、学校过程文件、历史交付物和模板资源。这里的内容默认是“归档资料”，而不是当前运行路径的一部分。

## 目录结构

- `graduation-materials/templates/`
  - 论文模板、格式样例、参考模板和写作排版参考文件。

- `graduation-materials/deliverables/`
  - 已形成的个人产出，例如中期报告、论文 Word/PDF、翻译作业等阶段性交付物。

- `graduation-materials/notes/`
  - 毕业设计过程记录、工作日志、阶段总结和历史笔记。

- `graduation-materials/visuals/`
  - 答辩图、截图、展示素材和其他视觉材料。

- `school-docs/`
  - 学校或学院提供的正式过程材料，例如任务书、开题报告、检查表、审批表等。

## 归档原则

- 模板、学校材料和个人交付物分开保存，避免相互覆盖。
- 运行代码不要依赖 `archive/` 中的历史资料，除非是明确配置为模板输入。
- 若某份材料需要继续迭代，应放入 `docs/` 或项目根目录对应功能区，而不是仅保留在 `archive/`。

## 推荐用法

- 写论文时，从 `graduation-materials/templates/` 取模板。
- 回看学校要求时，从 `school-docs/` 查阅正式文件。
- 回顾阶段性输出或答辩素材时，优先查找 `deliverables/` 和 `visuals/`。

## 说明

`archive/` 的目标是让项目根目录保持干净，同时保留毕业设计全过程的可追溯资料。对于需要长期保留但不应参与运行的数据、文档和样例，优先移动到这里。
