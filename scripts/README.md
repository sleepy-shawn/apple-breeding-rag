# Scripts Layout

`scripts/` 已按职责拆分，便于后续维护。

## 目录

- `pipeline/`
  - 论文抓取、工作区初始化、标准论文目录、manifest、staging、覆盖率扫描等流水线脚本。

- `data_prep/`
  - 基因表清洗、trait 拆分、GDR 转换、curated layer 构建等结构化数据处理脚本。

- `evaluation/`
  - 自动评测和 QTL/GWAS 参考系审计脚本。

- `reports/`
  - 给老师和项目管理使用的库存导出、Excel 汇总、盘点报告脚本。

- `thesis/`
  - 论文写作辅助脚本，例如根据模板生成 Word 初稿。

- `lib/`
  - 多个脚本共用的基础模块，目前主要是 pipeline 路径配置逻辑。

## 推荐原则

- 如果脚本直接参与数据流转，优先放进 `pipeline/`。
- 如果脚本主要负责把原始表处理成结构化 CSV，放进 `data_prep/`。
- 如果脚本输出的是总结、Excel、盘点表，放进 `reports/`。
- 论文相关脚本和自动评测脚本尽量不要和数据处理脚本混放。
