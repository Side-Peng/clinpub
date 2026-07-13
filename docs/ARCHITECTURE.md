# clinpub 架构文档

## 系统概述

clinpub 是一个基于 Claude Code 的临床数据分析与发表管线，采用三层架构设计：Commands → Workflows → Agents。

## 目录结构

```
clinpub/
├── .claude-plugin/            # 插件清单（plugin.json）
├── commands/                  # 扁平命令入口（11 个，自动发现）
│   ├── overview.md            # 主入口（/clinpub:overview）
│   ├── data2idea.md           # 选题挖掘（/clinpub:data2idea）
│   ├── data-prep.md           # 数据准备（/clinpub:data-prep）
│   ├── analysis.md            # 统计分析（/clinpub:analysis）
│   ├── writing.md             # 论文撰写（/clinpub:writing）
│   ├── review.md              # 审稿修稿（/clinpub:review）
│   ├── milestone.md           # 关卡评审（/clinpub:milestone）
│   ├── initialize.md                # 项目初始化（/clinpub:initialize）
│   ├── modify.md              # 分析修改（/clinpub:modify）
│   ├── do.md                  # 断点续做（/clinpub:do）
│   └── next-step.md           # 步骤推进（/clinpub:next-step）
├── agents/                    # 专业化 AI Agent（8 个）
│   ├── topic-miner-agent.md   # 选题挖掘 Agent
│   ├── analyst-agent.md       # 统计分析 Agent
│   ├── reference-agent.md     # 文献检索 Agent
│   ├── writer-agent.md        # 论文撰写 Agent
│   ├── clinpub-planner.md     # 研究规划 Agent
│   ├── clinpub-executor.md    # 分析执行 Agent
│   ├── clinpub-verifier.md    # 统计验证 Agent
│   └── modify-agent.md        # 分析修改 Agent
├── pipeline/                  # 管线配置
│   ├── workflows/             # 阶段编排逻辑（10 个）
│   ├── references/            # 参考文档（15 个）
│   ├── templates/             # 模板文件（18 个，含 study_types/）
│   └── contexts/              # 上下文配置
├── scripts/                   # 工具脚本
│   ├── data_profiler.py       # 数据画像
│   ├── ncbi_search.py         # NCBI 多数据库智能检索（主入口）
│   ├── pubmed_search.py       # PubMed 专用检索（MeSH 扩展 + 过滤）
│   ├── pubmed_fetch.py        # PMID 批量取全文
│   └── ncbi_utils.py          # E-Utilities 共享工具（限流/重试）
├── hooks/                     # Claude Code Hooks（3 个）
│   ├── hooks.json             # 声明式钩子配置
│   ├── clinpub-workflow-guard.js
│   ├── clinpub-phase-boundary.sh
│   └── clinpub-prompt-guard.js
└── docs/                      # 文档
```

## 三层架构

### 1. Commands 层（用户接口）

用户通过 Claude Code 的 Plugin 系统调用命令（`/clinpub:xxx`）。每个命令文件定义了触发条件、参数和执行流程。

**入口点**：`commands/overview.md` 是主入口（`/clinpub:overview`），展示命令参考表。

### 2. Workflows 层（编排逻辑）

工作流定义了每个阶段的执行顺序和依赖关系：

| 工作流 | 文件 | 职责 |
|--------|------|------|
| init-project | `pipeline/workflows/init-project.md` | Phase 0：项目初始化 |
| data-prep | `pipeline/workflows/data-prep.md` | Phase 1：数据准备 |
| analysis | `pipeline/workflows/analysis.md` | Phase 2：统计分析 |
| writing | `pipeline/workflows/writing.md` | Phase 3：论文撰写 |
| review | `pipeline/workflows/review.md` | Phase 4：审稿修稿 |
| milestone | `pipeline/workflows/milestone.md` | 阶段关卡评审 |
| data2idea | `pipeline/workflows/data2idea.md` | 选题挖掘 |
| import-project | `pipeline/workflows/import-project.md` | 已有项目导入 |
| modify | `pipeline/workflows/modify.md` | 分析产出修改 |
| next-step | `pipeline/workflows/next-step.md` | 步骤推进 |

### 3. Agents 层（专业化执行）

每个 Agent 是一个独立的角色卡片，定义了：
- 角色定位和职责
- 输入输出规范
- 工具使用权限
- 质量标准

**Agent 协作模式**：
- **Topic Miner Agent**：数据画像 → 文献扫描 → 选题生成
- **Analyst Agent**：数据清洗 → 统计分析 → 图表生成
- **Reference Agent**：文献检索 → PDF 读取 → 引用管理
- **Writer Agent**：IMRAD 撰写 → 图表整合 → 模拟审稿
- **Clinpub Planner**：研究规划 → PLAN.md 生成
- **Clinpub Executor**：分析执行 → 原子提交 → SUMMARY.md
- **Clinpub Verifier**：跨阶段验证 → 15 种验证模式
- **Modify Agent**：分析产出修改 → 图表样式/统计方法/变量调整

### 方法说明模板

Phase 2 的每个分析方法产出三件套：figure + table + 方法说明。方法说明使用中文模板 `pipeline/templates/method-readme.md`，包含：目的、方法、输入数据、输出结果、参数设置、注意事项、软件版本。

## 数据流

```
用户数据 (CSV/XLSX)
    ↓
Phase 0: init-project
    ↓
Phase 1: data-prep → cleaned.csv
    ↓
Phase 2: analysis → figures + tables + stats
    ↓
Phase 3: writing → IMRAD manuscript
    ↓
Phase 4: review → final manuscript
    ↓
投稿就绪
```

## 质量门控

4 道门控确保阶段间质量：

1. **IRB / Ethics Gate**（Phase 0 → 1）
   - IRB 批准文件
   - 数据去标识化
   - 知情同意

2. **Data Quality Gate**（Phase 1 → 2）
   - cleaned.csv 完整性
   - 缺失率受控
   - 样本量充足

3. **Analysis Validity Gate**（Phase 2 → 3）
   - 所有方法已执行
   - 效应量报告
   - 假设检验完整

4. **Submission Gate**（Phase 4 → Submit）
   - IMRAD 完整
   - 图表 ≥300 DPI
   - 引用全有 DOI

## Hooks 机制

3 个 Claude Code Hooks 保护分析流程：

| Hook | 触发时机 | 作用 |
|------|----------|------|
| `clinpub-workflow-guard.js` | Write/Edit | 阻止越阶段写文件 |
| `clinpub-phase-boundary.sh` | Bash | 检查前置 milestone 完成状态 |
| `clinpub-prompt-guard.js` | Read | 扫描数据文件中的 prompt injection |

## 扩展性

### 添加新研究类型

1. 在 `pipeline/templates/study_types/` 添加模板
2. 更新 `pipeline/references/analysis_methods.md`
3. 在 `agents/analyst-agent.md` 添加分析方法

### 添加新 Agent

1. 在 `agents/` 创建 Agent 角色卡片
2. 更新相关 Workflow 的 Agent 引用
3. 在 `pipeline/references/agent-contracts.md` 添加契约

## 技术栈

- **运行时**：Claude Code (Node.js >= 22.0.0)
- **统计分析**：R >= 4.2
- **数据处理**：Python >= 3.9
- **包管理**：npm
