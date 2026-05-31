# 代码规范与约定

**分析日期:** 2026-05-05

## 命名约定

### 文件命名

| 类型 | 模式 | 示例 |
|------|------|------|
| Agent 卡片 | `kebab-case-agent.md` | `analyst-agent.md`, `clinpub-planner.md` |
| 命令入口 | `kebab-case.md` | `clinpub.md`, `data-prep.md` |
| 工作流 | `kebab-case.md` | `analysis.md`, `init-project.md` |
| 参考文档 | `snake_case.md` | `analysis_methods.md`, `verification-patterns.md` |
| 模板 | `UPPERCASE.md` | `VALIDATION.md`, `UAT.md` |
| Python 脚本 | `snake_case.py` | `data_profiler.py`, `ncbi_search.py` |
| Hook 脚本 | `kebab-case.js` / `kebab-case.sh` | `clinpub-workflow-guard.js`, `clinpub-phase-boundary.sh` |
| 安装脚本 | `kebab-case.js` | `install.js` |
| Node.js 测试 | `*.test.cjs` | 尚未创建具体文件 |

### 目录命名

- **Phase 目录**: `0X_Name`（两位数序号 + 帕斯卡命名），如 `01_RawData`, `04_Outputs`
- **方法目录**: `XX_MethodName`（两位数序号 + 帕斯卡命名），如 `01_BaselineTable`
- **参考目录**: `snake_case` 或 `kebab-case`，如 `study_types/`, `literature_notes/`
- **项目文件**: `.clinpub/`, `.claude/`, `pipeline/`, `agents/`

### 变量命名

- **Python**: `snake_case`（见 `scripts/data_profiler.py` 中的 `detect_variable_role`, `profile_data`, `infer_study_type`）
- **JavaScript**: `camelCase`（见 `bin/install.js` 中的 `extractFrontmatter`, `convertCommandToSkill`）

### 函数命名

- **Python**: `snake_case`，动词开头。如 `def profile_data(filepath)`, `def infer_study_type(profile)`
- **JavaScript**: `camelCase`，动词开头。如 `function extractFrontmatter(content)`, `function registerHooks(isGlobal)`

### 常量命名

- **Python**: `UPPER_SNAKE_CASE`。如 `OUTCOME_PATTERNS`, `EXPOSURE_PATTERNS`, `MATCH_PATTERNS`
- **JavaScript**: `UPPER_SNAKE_CASE`。如 `PHASE_MAP`, `SOURCE_DIR`, `CLEANED_DATA`

## Git 规范

### 提交信息格式

所有提交遵循 Conventional Commits 风格：

```
<type>(<scope>): <description>
```

**Types**（实际使用过的）:
- `feat` — 新功能
- `refactor` — 重构
- `fix` — 修复
- `docs` — 文档

**Scopes**（实际使用过的）:
- 两位 phase 编号 + 两位优先级序号：`01-04`, `02-01`, `03-02`
- `ci` — CI 配置变更

**Description**: 小写、祈使语气。如 `add environment checks to install.js`

**历史示例**（`git log`）:
```
c564bc3 feat(04): create end-to-end integration test checklist (QUA-03)
985e389 feat(03-02): add scripts.test to package.json
3bd79ee feat(03-02): add CI test workflow and tests directory skeleton
0f325ec docs(03-01): unify DPI wording to reference FIGURE_DPI constant
1f7ecaf feat(02-02): add environment checks to install.js
5c47adc refactor(01-03): migrate prompt-guard.js to hookSpecificOutput + advisory mode
64ee9ab fix(ci): simplify release workflow, fix YAML encoding
```

### 提交原则

- 每个提交是原子性的（一个功能/修复/重构一个提交）
- `clinpub-executor` Agent 要求创建原子提交（`agent-contracts.md` 中定义）
- 提交信息包含 QUA 标签用于追溯，如 `(QUA-03)`

## 文件组织

### 目录布局

```
clinpub/
├── commands/clinpub/     # 用户可见的斜杠命令入口（8个.md）
├── agents/               # Agent 角色卡片（7个.md）
├── pipeline/
│   ├── workflows/        # Phase 编排（7个.md）
│   ├── references/       # 标准参考文档（9个.md）
│   ├── templates/        # 模板（10个.md + study_types/ 子目录）
│   └── contexts/         # 上下文配置（2个.md）
├── scripts/              # Python 工具脚本（5个.py）
├── hooks/                # Claude Code Hook（2个.js + 1个.sh）
├── tests/                # 测试目录（当前仅 .gitkeep）
├── bin/                  # npm bin 入口（install.js）
├── .github/workflows/    # CI 工作流（test.yml, release.yml）
├── .clinpub/            # 项目管理和跟踪
└── CLAUDE.md, SKILL.md, package.json, README.md 等
```

## 文档规范

### Agent 卡片格式

所有 Agent 使用 YAML frontmatter + XML 标签结构：

```yaml
---
name: analyst-agent
description: "R primary / Python secondary. Data cleaning, statistical analysis..."
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

XML 标签包括 `<role>`, `<execution_flow>`, `<critical_rules>`, `<success_criteria>` 等。步骤使用 `<step name="..." priority="...">` 定义。

### 命令入口格式

YAML frontmatter 包含 `name`, `description`, `argument-hint`, `allowed-tools` 字段。正文使用 `<objective>`, `<execution_context>`, `<process>`, `<success_criteria>` XML 标签。

### 工作流格式

使用 `<purpose>`, `<required_reading>`, `<process>` 标签。`<process>` 内含编号的 `<step>`。`<required_reading>` 使用 `@./pipeline/references/xxx.md` 引用格式。

### 模板格式

使用 Mustache 风格占位符 `{{placeholder}}`。内部引用使用 `@./` 前缀的相对路径。

### 参考文档格式

使用 Markdown 二级标题分隔章节，表格用于结构化数据（如 gate 条件）。引用的工具使用 `\`bash`` 代码块。

## Agent 合约约定

（定义在 `pipeline/references/agent-contracts.md`）

### 通信规则

1. **仅文件系统通信** — Agent 间无直接消息，通过文件传递
2. **无循环依赖** — Agent A 读 Agent B 的输出，反之不成立
3. **单写入者/目录** — 每个输出目录仅一个 Agent 写入
4. **共享读、独占写** — 多个 Agent 可读 `project_config.yml`，仅编排者写入
5. **状态通过编排者更新** — Agent 不直接更新 STATE.md
6. **Manifest 合约** — 每个 Agent 完成后写入 `MANIFEST.yaml`，下游读取验证

### Agent 输出目录矩阵

| Agent 写 | 目录 |
|----------|------|
| analyst-agent | `02_PreprocessedData`, `03_AnalysisMethods`, `04_Outputs` |
| reference-agent | `Reference/` |
| writer-agent | `05_Manuscript` |
| topic-miner-agent | `idea/` |
| clinpub-planner | `.clinpub/phases/` |
| clinpub-executor | 分析输出 + `.clinpub/` |
| clinpub-verifier | `.clinpub/phases/` (VERIFICATION.md) |

## 代码风格工具

- **格式化工具**: 无。未使用 Prettier、ESLint、Biome 或其他格式化工具
- **Linting 工具**: 无。项目不依赖任何 linter
- **Node.js 包**: 仅 `clinpub-cc` 无生产依赖，无 devDependencies
- **Python 包**: 运行时依赖 `pandas`, `numpy`, `requests`, `openpyxl`，无测试依赖（pytest 仅在 CI 中安装）

## 需要统一的规范

### 高优先级

1. **代码格式化缺失**: 项目没有任何格式化或 linting 工具。建议添加 Prettier (JS) 和 Black (Python)。
2. **无类型检查**: Python 使用 `typing` 模块（见 `data_profiler.py` 导入 `Dict, List, Any, Optional`），但 JS (`install.js`) 无类型注解。应用阶段可以考虑添加 TypeScript 或 JSDoc 注解。
3. **注释语言混杂**: 中英文注释混用。Python 脚本 (`data_profiler.py`) 使用中文注释，JS 脚本 (`install.js`) 使用英文注释。Agent 卡片和文档多数为英文，模板中中文占比高。建议明确每类文件的注释语言约定。

### 中优先级

4. **测试文件命名不一致**: `package.json` 中 `"node --test \"tests/**/*.test.cjs\""` 指定 `.test.cjs` 后缀，但 Python 测试未指定查找模式。建议统一测试文件命名约定（如 `test_*.py`）。
5. **缺少 `.editorconfig`**: 跨编辑器缩进/编码设置无法保证一致性。建议补充 `.editorconfig`。
6. **出口/入口缺乏显式声明**: `package.json` 中 `"files"` 字段手动列出发布文件，但无测试包含在内。建议添加 `"include"` 或 `"exclude"` 规则。

### 低优先级

7. **模板格式不一致**: 部分模板使用 `{{placeholder}}`，部分使用 `{{field}}`。建议统一使用 `{{placeholder}}`（不加空格）。
8. **Agent 术语未完全统一**: 有些地方称 "Phase"，有些称 "阶段"。建议统一为 "Phase N — <中文名>"（参考 `STATE.md` 模式）。

---

*代码规范分析: 2026-05-05*
