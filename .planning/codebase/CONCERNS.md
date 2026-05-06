# Codebase Concerns

**分析日期:** 2026-05-05

## 安全风险

### 1. `.gitignore` 全局忽略数据文件导致 sample data 无法提交

- **问题**: `.gitignore` 中 `*.csv`、`*.xlsx`、`*.xls` 为全局模式（无路径前缀），导致整个仓库中所有 CSV/Excel 文件都被忽略。
- **文件**: `.gitignore` 第5-7行
- **影响**: `examples/sample_data/` 下的测试数据（`84例-认知-0120.xlsx`、`认知因子对应.xlsx`）无法被 git 跟踪，导致集成测试重复执行时都需要手动寻找替代数据。`examples/04-INTEGRATION-CHECKLIST.md` 引用这些文件但不提交，直接破坏了 checklist 的可执行性。
- **当前缓解**: 无。文件完全无法提交。
- **建议**: 对全局通配加 `!` 覆盖例外，改为路径限定模式：
  ```
  # 仅忽略项目中自动生成的数据目录
  01_RawData/
  02_PreprocessedData/data/
  examples/sample_data/**/*.xlsx  # 允许跟踪示例数据
  ```
  或者将 sample data 迁移到 `tests/fixtures/` 目录并添加白名单规则。

### 2. API Key 泄露风险 — 安装脚本输出提示将 key 写入 `.env`

- **问题**: `ncbi_client.py:print_api_key_tip()` 输出的安装指引中（第96-98行）建议用户将 `NCBI_API_KEY` 写入 `.env`。虽然 `.env` 在 `.gitignore` 中，但用户可能误操作提交。
- **文件**: `scripts/ncbi_client.py` 第93-98行
- **影响**: API key 写入 `.env` 后若 `git add --force` 或被 `.gitignore` 意外修改则可能泄露。
- **当前缓解**: `.env` 在 `.gitignore` 中。
- **建议**: 改为推荐环境变量方式（`export NCBI_API_KEY=xxx` 写入 `~/.bashrc`），删除提示中写入 `.env` 的建议。提供 `.env.example` 模板。

### 3. 无 `.env.example` 文件

- **问题**: 仓库中不存在 `.env.example` 模板文件，新增开发者无法快速了解需要配置哪些环境变量。
- **影响**: 用户可能遗漏 `TAVILY_API_KEY` 或 `NCBI_API_KEY` 设置，导致 Tavily 搜索不可用或 PubMed 检索被限速。
- **建议**: 创建 `.env.example`：
  ```env
  # Required
  TAVILY_API_KEY=tvly-your-key-here
  
  # Optional — improves PubMed rate limit from 3 req/s to 10 req/s
  NCBI_API_KEY=your-key-here
  ```

## 技术债务

### 1. （已清理）测试基础设施已删除

- **说明**: 所有测试文件（`tests/` 目录、`package.json` 的 test script、`.github/workflows/test.yml`）已在 2026-05-05 按开发者要求删除。本项目为纯开发环境，测试由开发者外部完成。
- **影响**: 无需关注。

### 2. `pymupdf` 僵尸依赖

- **问题**: `requirements.txt` 中声明 `pymupdf>=1.23`，但 `pdf_reader.py` 已被删除（见 commit 41d33ca "remove pdf_reader.py"），整个仓库中没有任何代码导入 `pymupdf` 或 `fitz`。
- **文件**: `requirements.txt` 第4行
- **影响**: 无意义的依赖项污染，浪费 pip install 时间。
- **建议**: 删除 `pymupdf` 行。如需保留 PDF 功能，需明确哪个功能依赖它。

### 3. 残留 `.pyc` 字节码

- **问题**: `scripts/__pycache__/pdf_reader.cpython-313.pyc` 来自已删除的 `pdf_reader.py`，是脏数据。
- **文件**: `scripts/__pycache__/pdf_reader.cpython-313.pyc`
- **影响**: 无功能影响，但属于垃圾文件。
- **建议**: 删除整个 `__pycache__/` 目录（已在 `.gitignore` 中但需要手动清理）。可以在 `.github/workflows/` 中添加一个清理 check。

### 4. `phase-boundary.sh` 存在逻辑重复执行问题

- **问题**: 第135行的 `check_phase_boundary()` 调用将 stdout/stderr 全部重定向到 `/dev/null` 只检查返回值，然后第136行为了捕获错误消息又无条件重新调用一次。函数被执行两次。
- **文件**: `hooks/clinpub-phase-boundary.sh` 第135-136行
- **影响**: 每次 Bash 工具调用触发 hook 时重复执行相同的文件检查和 grep 操作，轻微性能浪费。
- **建议**: 重构为一次调用并同时获取返回值和输出：
  ```bash
  if ! output=$(check_phase_boundary "$target_phase" 2>&1); then
    # 非零退出码 = blocking
    echo "$output" | grep "BLOCK:" | head -1 ...
  fi
  ```

### 5. `workflow-guard.js` 存在错误

- **问题**: 
  - 第22行目录名拼写错误 `"05_Manuscript/final"` 应为 `"05_Manuscripts/final"`（少了 `l`），但实际项目中根本不存在 `05_Manuscript/` 目录（该目录是 Phase 3 运行时生成的）。这个验证永远匹配不到任何文件，形同虚设。
  - 注释（第6-7行）说 hook 守卫 Write/Edit/Bash，但代码第92行只守卫 Write 和 Edit。
- **文件**: `hooks/clinpub-workflow-guard.js`
- **影响**: Phase 4 的目录守卫实际无效，但无实际安全后果（因为 Phase 4 目录本就不存在）。
- **建议**: 修正拼写，或删除 Phase 4 的检查（直到 Phase 4 被实现）。

### 6. 无 R 代码存在

- **问题**: 整个仓库中没有 `.R` 或 `.r` 文件。但 `analyst-agent.md` 的核心输出是生成 R 分析代码，`r_patterns.md` 是 429 行的大参考文档，`INSTALL.md` 列出了 18 个 R 包依赖。
- **影响**: 整个统计分析的 R 代码生成能力完全未经测试。R 包兼容性、可视化质量、统计分析正确性都无法验证。
- **建议**: 至少添加 1-2 个示例 R 分析脚本并存为版本控制（可以使用 `tests/fixtures/` 路径），以便 CI 可验证 R 语法正确性。

### 7. CRLF/LF 换行符不一致

- **问题**: git 当前报告 24 个文件有 LF → CRLF 替换警告（Windows 环境）。这些 .md 文件从 Unix LF 签出后被转换为 Windows CRLF。
- **影响**: 跨平台合作时 git diff 会显示完全冲突的换行符更改，污染代码审查。特别是 `pipeline/workflows/` 和 `agents/` 目录下的 .md 文件。
- **建议**: 在仓库根目录添加 `.gitattributes` 文件：
  ```gitattributes
  * text=auto
  *.md text eol=lf
  *.sh text eol=lf
  *.js text eol=lf
  ```

## 未完成的工作

### 1. Phase 0-4 端到端流程未实战验证

- **问题**: STATE.md 将"用真实临床数据跑一遍完整 pipeline"列为第一优先级后续工作，但从未执行。
- **文件**: `.planning/STATE.md` 第82行
- **影响**: 整个 pipeline 的 Phase 0→1→2→3→4 各阶段衔接、milestone 系统、checkpoint 机制均未经过真实数据验证。无法保证工作流编排在真实场景中的可靠性。
- **建议**: 用 `examples/sample_data/` 的数据（前提是解决 `.gitignore` 问题）跑一遍完整流程。

### 2. Hook 注册未经过验证

- **问题**: STATE.md 将 "Hook 注册" 列为可选后续工作，`install.js` 虽然实现了 `registerHooks()` 函数，但从未有真实运行记录。
- **文件**: `.planning/STATE.md` 第83行、`bin/install.js` 第169-211行
- **影响**: hook 注册到 `.claude/settings.json` 的逻辑未经过端到端测试，可能存在路径问题、JSON 解析问题或冲突处理问题。
- **建议**: 手动验证 `registerHooks()` / `unregisterHooks()` 的幂等性。

### 3. 未跟踪的新文件（`docs/`、`manifest-format.md`、`project_config.example.yml`）

- **问题**: 以下文件未被 git 跟踪：
  - `docs/getting-started.md` — 新手入门文档（潜在价值较高）
  - `pipeline/references/manifest-format.md` — MANIFEST.yaml 格式定义，定义了 Agent 间文件交换协议（关键架构文档）
  - `examples/project_config.example.yml` — 示例项目配置（对用户有用）
- **影响**: 
  - `manifest-format.md` 未提交意味着下游 Agent 实现无法参考这个格式规范，所有 Agent 的 MANIFEST.yaml 输出格式无标准约束。
  - `project_config.example.yml` 未提交意味着新用户没有可复制的配置模板。
- **建议**: 审阅并提交这些文件，特别是 `manifest-format.md`（它有 template 性质但放在了 references/ 而非 templates/ 下，需要确认路径是否合理）。

### 4. 模板填充验证未执行

- **问题**: STATE.md 列出的"模板填充验证 — 用示例数据填充所有模板，确认占位符无遗漏"从未执行。
- **文件**: `.planning/STATE.md` 第83行
- **影响**: 5 个研究类型模板中可能有未替换的占位符（如 `<Author, Year>`），被 AI Agent 写入稿件时产生格式错误。
- **建议**: 用示例数据端到端执行一次 Phase 3，确认所有模板占位符被正确替换。

## 依赖问题

### 1. R 包无版本锁定

- **问题**: `INSTALL.md` 列出 18 个 R 包但无版本号。CRAN 包的新版本可能引入破坏性变更（如 `ggplot2` 3.5.0 的主题变更）。
- **文件**: `INSTALL.md` 第70-76行
- **影响**: 跨时间、跨机器的 R 分析结果不可复现。
- **建议**: 添加 `renv.lock` 文件（R 的包锁定机制）或用 `sessionInfo()` 生成依赖清单。

### 2. `tavily-python` 标记为依赖但实际为可选

- **问题**: `requirements.txt` 列出 `tavily-python>=0.3` 作为直接依赖。但 `tavily_search.py` 本身是可选工具，仅在 `reference-agent` 的某些搜索场景中使用。
- **文件**: `requirements.txt` 第7行
- **影响**: 用 `pip install -r requirements.txt` 的用户必须安装 tavily，即使他们不需要文献搜索功能。
- **建议**: 拆分为 `requirements-core.txt`（必需: pandas, numpy, requests, openpyxl）和 `requirements-optional.txt`（可选: pymupdf, tavily-python）。在安装文档中说明。

### 3. 无 lockfile

- **问题**: 无 `package-lock.json` 或 `requirements.txt.lock` 文件。
- **影响**: Node.js 的 `npx clinpub-cc` 每次安装可能使用不同版本的依赖（如 `tavily-python` 的子依赖）。
- **建议**: 对于 Python，生成 `requirements.txt` 的固定版本变体。对于 Node.js，`package.json` 本身是纯配置无运行时依赖（仅需要原生 Node 模块），影响较小。

## 配置风险

### 1. `03_AnalysisMethods/**/main.R` 被 gitignore

- **问题**: `.gitignore` 第19行 `03_AnalysisMethods/**/main.R` 忽略分析 R 脚本，但第20行 `!03_AnalysisMethods/**/README.md` 保留 README。这意味着分析源代码不被版本控制，只有注释文档被保留。
- **文件**: `.gitignore` 第19-20行
- **影响**: 分析代码不可版本化、不可回滚、不可 audit。违反最基本的可复现性原则。如果分析师修改 `main.R` 后丢失数据，没有 git 历史可恢复。
- **建议**: 删除 `.gitignore` 中的 `03_AnalysisMethods/**/main.R` 行。分析代码应当被版本控制。如果担心生成文件体积，应使用更精确的忽略规则（仅忽略自动生成的临时文件）。

### 2. `package.json` 要求 Node >= 22.0.0

- **问题**: `engines.node` 要求 Node.js >= 22.0.0，这是一个非常新的 LTS 版本（2024年10月才进入 LTS）。许多系统默认安装的 Node.js 版本可能不满足此要求。
- **文件**: `package.json` 第18行
- **影响**: 安装检查会警告但不会阻止安装（`install.js` 第258-262行的检查是软警告）。用户可能无视警告继续使用，后续 hook 脚本可能因为 Node API 变更而失败。
- **建议**: 降低最低版本到 18 LTS 或 20 LTS，或者明确在 README 和 INSTALL.md 中标注此限制的合理理由。

### 3. `phase-boundary.sh` 中硬编码路径与 PROJECT_DIR 不一致

- **问题**: `main()` 函数从 stdin 解析 `command` 并检查关键词（如 `$ANALYSIS_DIR`、`$PREPROCESSED_DIR`）来推断目标阶段。但这些路径引用的是硬编码的相对路径（第21-26行），未使用 `PROJECT_DIR` 变量。
- **文件**: `hooks/clinpub-phase-boundary.sh` 第21-26行
- **影响**: Phase boundary 检查依赖于 Bash 命令字符串关键字匹配，而不是实际文件系统状态。如果用户使用不同的目录名（在 `project_config.yml` 中可配置 `paths.raw_data`），hook 的匹配可能失效。
- **建议**: 改为读取 `project_config.yml` 中的自定义路径配置，或声明 `paths` 不可自定义。

## 文档缺失

### 1. git 提交历史中无 Phase 门控记录

- **问题**: 当前 git 历史显示所有 Phase 文档（workflows、references、agents）都是一次性提交的（commit 59562ed、41d33ca 等），没有真实执行 Phase 0-4 的门控记录（MILESTONE.md 等）。
- **影响**: 缺少用户实际通过 pipeline 的验证记录。新用户无法参考"正确完成"的 Phase milestone 示例。
- **建议**: 运行一次完整 pipeline（即使是用很小的示例数据），将所有 milestone、checkpoint、decision 记录提交到仓库作为示例。

### 2. 无贡献指南

- **问题**: 仓库中无 `CONTRIBUTING.md`。虽然该项目主要是 AI Agent 驱动的，但作为开源项目仍需规范化贡献流程。
- **建议**: 添加简单的 `CONTRIBUTING.md` 说明分支策略、测试要求和 PR 流程。

### 3. `.planning/codebase/` 目录存在但无历史分析文档

- **问题**: `.planning/codebase/` 目录被 CLAUDE.md 提及用于存储代码分析文档（STACK.md、ARCHITECTURE.md 等），但在本次分析之前没有文档存在。
- **影响**: 代码映射文档不存在，导致 `/gsd-plan-phase` 无法加载这些参考文档来制定计划。
- **建议**: 在本映射完成后，创建所有焦点的文档（tech、arch、quality、concerns）。

## 建议优先级

### 关键（立即处理）

| # | 问题 | 影响 | 建议动作 |
|---|------|------|----------|
| 1 | `.gitignore` 全局文件忽略 | 示例数据无法提交，checklist 不可执行 | 用 `examples/sample_data/` 白名单覆盖 |
| 2 | `03_AnalysisMethods/**/main.R` 被忽略 | 分析代码无版本控制 | 删除此 gitignore 规则 |

### 高优先级

| # | 问题 | 影响 | 建议动作 |
|---|------|------|----------|
| 3 | `pymupdf` 僵尸依赖 | 无用依赖 | 删除 |
| 4 | 无端到端流程验证 | 整个 pipeline 未经验证 | 用 sample_data 跑一次完整流程 |
| 5 | `manifest-format.md` 未提交 | Agent 间协议无约束 | 提交该文件 |
| 6 | CRLF 不一致 | 跨平台 diff 混乱 | 添加 `.gitattributes` |

### 中优先级

| # | 问题 | 影响 | 建议动作 |
|---|------|------|----------|
| 7 | R 包无版本锁定 | 不能复现分析 | 添加 `renv.lock` |
| 8 | `phase-boundary.sh` 重复执行 | 轻微性能浪费 | 重构函数调用 |
| 9 | `workflow-guard.js` 拼写错误 | Phase 4 守卫无效 | 修正拼写 |
| 10 | 无 `.env.example` | 新用户配置困难 | 创建 `.env.example` |
| 11 | 模板占位符未验证 | 可能输出格式错误 | 用样本数据验证模板 |

### 低优先级

| # | 问题 | 影响 | 建议动作 |
|---|------|------|----------|
| 12 | 无 `CONTRIBUTING.md` | 开源项目规范化 | 添加贡献指南 |
| 13 | `tavily-python` 标记为硬依赖 | 不必要的依赖 | 拆分 requirements |
| 14 | `node >=22` 要求较高 | 部分用户不满足 | 降低版本要求或说明理由 |

---

*Concerns audit: 2026-05-05*
