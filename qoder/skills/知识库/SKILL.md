---
name: 知识库
version: 1.0.0
description: Internal knowledge base for clinpub pipeline — analysis methods, R patterns, journal standards, reporting guidelines, agent contracts, and templates.
description_zh: 临床研究发表管线的内部知识库——分析方法、R代码模板、期刊标准、报告规范、Agent契约和项目模板。
user-invocable: false
---

# ClinPub 知识库

本技能是内部知识库，被其他技能引用。用户不可直接调用。

## 参考文档索引

### 分析方法与代码
- [分析方法目录](references/analysis_methods.md) — 支持的统计方法完整目录
- [R代码模板](references/r_patterns.md) — 共享图表配置、配色方案、图表模板
- [组间比较决策树](references/comparison-methods.md) — 2组/3+组×连续/分类/配对的检验选择

### 期刊与质量标准
- [期刊分级标准](references/journal_standards.md) — Q1-Q4期刊要求、报告规范
- [质量门](references/gates.md) — 4个质量门：IRB、数据、分析、投稿
- [检查点](references/checkpoints.md) — 阶段内决策点与验证门

### Agent与协作
- [Agent契约](references/agent-contracts.md) — 所有Agent的角色、I/O、读写矩阵
- [MANIFEST格式](references/manifest-format.md) — 输出目录的MANIFEST.yaml规范
- [必读文件](references/mandatory-initial-read.md) — 每个Agent启动时必须读取的文件

### 文献与引用
- [引用策略](references/citation-strategy.md) — 各段引用数量和策略
- [检索语法](references/query_syntax.md) — PubMed搜索语法参考
- [引用库格式](references/reference-library.md) — 共享引用库JSON schema
- [文献拼接协议](references/concatenation-protocol.md) — 7步稿件拼接协议

### 验证
- [验证模式](references/verification-patterns.md) — 8种验证模式
- [预阶段研究](references/pre-phase-research.md) — 预阶段文献检索协议

### 项目导入
- [导入启发式](references/import-heuristics.md) — 文件角色推断规则

### 项目模板
- [项目配置模板](references/templates/project_config.yml) — 主配置文件
- [状态模板](references/templates/state.md) — STATE.md模板
- [路线图模板](references/templates/roadmap.md) — ROADMAP.md模板
- [项目结构](references/templates/project.md) — 目录结构规范
- [里程碑模板](references/templates/milestone.md) — 阶段里程碑文档
- [导入里程碑](references/templates/import-milestone.md) — 导入模式里程碑
- [方法说明模板](references/templates/method-readme.md) — 每方法文档模板
- [选题报告模板](references/templates/idea_report.md) — 选题挖掘报告
- [验证报告模板](references/templates/verification-report.md) — 验证输出模板
- [图表配置R脚本](references/templates/_figure_config.R) — 共享图表配置模板
- [研究类型模板](references/templates/study_types/) — 5种研究类型（RCT/队列/病例对照/横断面/描述性）
