# Changelog

All notable changes to the clinpub project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.0.0] - 2026-10-18

> **破坏性变更**：不兼容 2.x 的项目状态（`.clinpub/` 结构与流程语义均变）。已有项目需重新初始化，或用 `import-project` 采纳现有材料。

### Changed — 文案中文化

- **全部技能描述改为中文**（10 个 DSH 技能 + 10 个 claude-code 命令 + 10 个 codex 技能）。主要使用者为中文工作者，描述直接决定技能路由，中文表述更贴合实际使用语境。英文版待后续翻译。
- **插件清单描述改为中文**：`plugin.json` / `package.json` / `marketplace.json` 的 `description`、`displayName`，以及 codex 的 `interface.shortDescription` / `longDescription` / `defaultPrompt`。

### Changed — 分析：从"一次规划"到"迭代决策"

- **阶段2 改为迭代循环**：不再一次确认全部分析方法。每批 1–3 个方法，执行后记录结果与解读，依据决策规则决定下一批，直到饱和或触及预算。
- **新增 `pipeline/references/analysis_decision_policy.md`**：决策规则库（8 条结果驱动 + 6 条数据驱动 + 分叉判据 + 5 条饱和判据 S1–S5）。每批方法选择必须可追溯到规则编号（R/D/U）。
- **新增 `.clinpub/ANALYSIS_LOG.md`**：每批六段记录（依据 / 本批方法 / 结果要点 / 解读 / 下一批决策 / **否决项**）。"否决项"是 Discussion 局限性段的核心素材。
- **新增 `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md`**：分析冻结时的收敛摘要，阶段3 的主要输入。阶段2 的完成判据从此是它而不是 waves。
- **`analysis_budget` 取代 `analysis_plan.waves`**：`project_config.yml` 中改为 `max_batches` / `max_methods` / `ask_on_branch`。

### Changed — 写作：从 IMRAD 顺序到递进式

- **阶段3 改为递进写作**：图表骨架 → Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract。每一节必须读取前节的实际内容。
- **新增 `FIGURE_SKELETON.md`**：在写任何正文前排定图表并为每张写一句不含统计量的结论。引言不再是起点，图表才是。
- **新增 `NARRATIVE.md`**：Introduction 动笔前的叙事设计（一句话卖点 / Gap / 叙事弧 / 期刊调性）。Introduction 从它展开，而非从零硬写。
- **新增 `05_Manuscript/sections/`**：六节各自成文件，带 frontmatter（`section` / `status` / `inputs` / `depends_on`）。这是对 2.3.0「单一 manuscript.md」的有意识回退——写作顺序 ≠ 输出顺序。
- **`manuscript.md` 变为生成物**：由 `scripts/assemble_manuscript.py` 按 IMRAD 顺序拼装，禁止手改。存在 `draft` / `stale` 章节时脚本拒绝生成。
- **新增章节依赖 DAG 与 stale 传播**：改任一节，下游自动标 `stale`。
- **写作可反哺分析**：写到 Discussion 发现分析缺口时，允许退回阶段2 补分析（同一缺口不得退回两次）。
- **新增 `pipeline/references/writing_standards.md`**：写作唯一标准——事实/解释分层、各节结构、统计量格式、报告规范对照、交付前 10 项检查。
- **取消"一键成稿 / 逐步写作"双模式**：改为 `writing.pause_after` 配置（默认在 Results 与 Discussion 后暂停）。`pause_after: []` 等价原一键成稿。

### Changed — 命令精简（14 → 10）

- **合并 `overview` / `do` / `next-step` / `milestone` 为 `/clinpub` 枢纽**：四种模式——无参看状态、`help` 看参考、`next` 核验并推进、其余文本按意图路由。
  - 原先四个命令各维护一份状态判据（改一处要改三处），合并后判据只写一份。
  - **"推进"与"关卡核验"成为原子动作**：必须先核验、生成 `MILESTONE.md`、取得签字，才更新 `STATE.md` / `ROADMAP.md`。
- **删除 `clinpub-knowledge` 技能**：它只是参考索引，各技能已自带 `参考资源` 清单。
- `dsh/build.mjs` 增加**过期技能清理**：合并/删除的技能若留在 `.dsh/skills/`，DSH 仍会发现它——生成时显式删除不在清单内的目录。

### Changed — 智能体

- **智能体 8 → 6**：停用 `clinpub-planner` 与 `clinpub-executor`。迭代循环本身承担规划职能，"先规划全部再执行"的原子提交模式已无位置；原子提交由 `analyst-agent` 承担。
- `analyst-agent` 改为**执行编排器指派的一批**方法，不再等待预先写好的 PLAN.md；明确写入边界（不写 ANALYSIS_LOG / ANALYSIS_SUMMARY）。
- `modify-agent` 不再写 PLAN.md 或直接改手稿，改为回传 `affects_sections` 供编排器做 stale 传播。
- `clinpub-verifier` 的验证对象改为 `ANALYSIS_LOG.md` / `ANALYSIS_SUMMARY.md`。

### Changed — 上下文成本

- **`do` 不再注入 10 个 workflow**（约 −92 KB/次）：它只做路由，不需要流程全文。
- **`commands/next-step.md` 从 378 行精简为判据摘要**：原先与 workflow 全文重复，双份维护。
- `initialize` 不再注入 `r_patterns.md`（阶段0 不写 R 代码）。

### Added

- `scripts/assemble_manuscript.py`：拼装 + 校验（缺节 / 非 final / 上游 stale 三类拒绝）+ 字数统计。
- `pipeline/templates/section.md`、`figure-skeleton.md`、`narrative.md`。
- claude-code / codex 同步至 3.0。

### Added — 标题延后拟定（测试驱动）

- **`project_config.yml` 新增 `project.title`**：原先 writing workflow 声称"标题写入 `project.title` 供拼装读取"，但模板里根本没有这个字段。
- **`assemble_manuscript.py` 读取并输出标题**：写入 manuscript.md 的 frontmatter 与一级标题；为空时给出警告而非失败。读取用 `utf-8-sig`，否则 Windows 编辑器的 BOM 会让首行匹配失败。
- **`writing.md` 的 frontmatter 步骤改为"只追加"**：`title` / `word_count` 等由脚本写入，agent 不得重写已有字段。
- 约定：初始化只记**工作标题**（`project.name`），正式标题在阶段3 `write_abstract_title` 产出——**先写完全文，再定标题**。

### Changed — 术语中文化：Phase → 阶段

- **中文文案统一为「阶段N」**（无空格）：命令说明、README、文档、workflow 正文、技能描述全部改用 `阶段0 / 阶段1 / 阶段2 / 阶段3`。
- **保留 `STATE.md` 的 `阶段：Phase N`**：该行由 `hooks/clinpub-workflow-guard.js` 用正则 `阶段：Phase\s*(\d)` 解析，属机器可读标识，与人类可读文案分开。
- **英文为主的文档保持 `Phase`**（`AGENTS.md`、`CLAUDE.md`、`agents/*.md`、`milestone.md`、`init-project.md` 等）：英文句子里嵌「阶段」会变成半中半英，故保留原文；待中译/英译时统一。

### Changed — 图表风格包与矢量导出

- **新增风格包机制**（`quality.style`）：`nature` / `lancet` / `jama` / `nejm`，一次选定整套规格——栏宽、字号、线宽层级、配色角色、导出格式。`quality.style_overrides` 可按名覆盖单项，不必改代码。
- **栏宽属于风格包**，不是全局常量：Nature 89/183 mm、Lancet 90/190、JAMA 86/178、NEJM 86/173。Science/Cell 等更窄的栏宽可在后续加包。
- **字号由画布推导**：`pub_base_size(width_mm)` 按单/双栏返回该包的字号，落在期刊要求的 5–7 pt 区间；配置里显式给值才覆盖。
- **导出改为矢量优先**：主图默认 `pdf + svg`。Nature 官方 figure guide 明确不接受 tiff/png 作主图（tiff 只用于 Extended Data，300 dpi）。补充材料仍可显式 `formats = "tiff"`。
- **配色按角色**（main/contrast/accent/neutral/ink）。顺带纠正：原先 `theme_pub` 的 `#0072B5`/`#BC3C29` 其实是 **NEJM** 的前两色；Nature 的色盲友好方案是 Okabe-Ito（`#0072B2`/`#D55E00`）。
- **修正 `axis.title.y` 被转平**：覆盖该元素时不带 `angle = 90`，会把继承来的竖排标题转成横排。
- **`r_patterns.md` §1.2/§1.3 由代码副本改为契约**：原来那两节直接复制了 190 行实现，代码一改文档就漂移；现在只写规格与禁止事项，实现只有一份（`_figure_config.R`）。
- **字号统一**：轴标签（`axis.text`）与轴标题（`axis.title`）改为**同磅值**（原先标签小 0.5pt，横竖视觉重量不一致）。图例文字同样对齐到基础字号。
- **字重统一为加粗**：轴标题、轴刻度、图例、副标题全部 `face = "bold"`。此前轴标题 bold、刻度 regular，同为 7pt 却看着"一大一小"；现在同字号同字重，层级靠位置区分。
- **字体固定为 Arial**：`base_family` 默认由风格包的 `font` 提供（不再用 `"sans"`——它在不同平台会落到 DejaVu/Helvetica，字宽不一致）。
- **`theme_pub()` 支持 `width_mm`**：原先不传画布宽度时一律按双栏推导，导致 89 mm 单栏图用的是 6.5pt（应为 7pt）。单栏图现在必须传 `width_mm = FIG_WIDTH_MM[["single"]]`。
- **冻结默认面板规格**（`r_patterns.md` §2.1）：散点 `size 1.05 / alpha 0.55 / 抖动 0.14`，箱体 `width 0.30 / linewidth = LW_DATA × 0.65`，中位线 `fatten 2.2`。三条互相牵制——字加粗后点必须放大、框线要相应收回，否则"头重脚轻"。
- **新增图表交付检查清单**（`writing_standards.md`）：物理尺寸 / 格式 / 字号 / 可编辑文字 / 统计量 / 样本量 / 图例冗余 / 风格一致性，共 13 项。

### Fixed — 引用链路（测试驱动）

- **拼装脚本从未实现引用编号与 References 生成（严重）**：`writing.md` 与 `concatenation-protocol.md` 都规定"按正文出现顺序连续编号、文末生成 Vancouver References"，但 `assemble_manuscript.py` 只输出一行占位注释——文档描述了能力，代码里不存在，且不报错。
  - 现在：章节写 `{{cite:CitationKey}}` / `{{cite:Key1,Key2}}`，脚本按**跨章节首次出现顺序**连续编号为 `[n]` / `[n,m]`，并生成带 `doi:` 的 Vancouver References（作者 ≤6 人，超出用 et al）。
  - 键不在库中时给 `[WARN] 引用键不在文献库中`，不再静默产出无引用的手稿。

### Changed — 文献检索升级到 ncbi-search v3.0.0

- **内置脚本同步上游 v3.0.0**（`ncbi_search.py` / `ncbi_utils.py` / `pubmed_search.py` / `pubmed_fetch.py` / `pmc_fetch.py` / `test_ncbi.py`），三平台一致。
- **破坏性变更需注意**：`--abstract` 默认值由"返回摘要"改为 `none`（仅标题+元数据）。只调 `ncbi_search.py` 而不显式指定 `--abstract` 时，拿到的是无摘要列表——`reference-agent.md` 的说明已同步更正，并写入三级摘要的用途与 token 成本。
- **新增能力**：`--count-only`（只取命中数）、`--offset`（翻页）、`--min-year/--max-year`（年份区间）、`--mesh`（MeSH 在线校验）、`pmc_fetch --sections`（只取指定章节）、中文术语自动英译（~80 词）。
- **准确性修复**（上游）：作者解析误触发（`Vitamin D deficiency` 3 → 44,191 条）、解剖词不再强标 MeSH、多库路由重写、Gene 库用 `[Gene Name]` + 学名映射、dbSNP 纯 rsID 走 `[UID]` 并支持批量。
- **健壮性**（上游）：Tier1 改用 ESummary v2.0（带宽 −80~90%）、PMID→PMCID 改 ELink 批量（~100×）、SQLite WAL + 容量上限、错误体不写缓存、重试 4 次并尊重 Retry-After。
- 新增 `pipeline/references/parameters.md`、`result_format.md`；`query_syntax.md` 升级到 v3。
- `.gitignore` 新增 `.ncbi_cache/`（脚本缓存不再入库）。

### Changed — DSH 技能补齐 agent 角色卡

- `clinpub-writing` / `clinpub-improving` / `clinpub-review` / `clinpub-data2idea` 的参考资源补充 `agents/*.md`。此前 workflow 里写着"调用 reference-agent"，但 DSH 没有该机制、技能里也没有角色卡，指令指向空气。

### Fixed — 手稿拼装（测试驱动）

- **占位符不再要求手工替换**：`assemble_manuscript.py` 现在自己解析 `{{Table:N}}` / `{{Figure:N}}` / `{{SupplementaryTable:N}}` / `{{SupplementaryFigure:N}}` / `{{Method:name}}` / `{{Section:name}}`，残留时给 stderr 警告。原先 workflow 要求 agent 手工改 `manuscript.md`——与"生成物禁止手改"自相矛盾，下次拼装必然覆盖。
- **消除重复标题**：章节文件自带 `# Results` 时，拼装结果会出现 `## Results` + `# Results` 两个标题。脚本现在剥掉章节自带的首个 H1。
- **修正标题层级**：章节内小标题原与章节标题同为 `##`，现统一下移一级（`## → ###`），目录层级不再错乱。

### Fixed — R 绘图规范（测试驱动）

- **森林图模板使用已废弃 API**：`r_patterns.md` 用 `geom_errorbarh()`，在 ggplot2 4.0.0 起被弃用（`height` 被静默改名为 `width`），未来版本将移除。改为 `geom_errorbar(..., orientation = "y")` 并补充 3.x/4.x 兼容说明。

### Fixed — 图表配置模板（测试驱动）

- **`_figure_config.R` 语法错误，从未能加载**：模板用 `_config_paths` 等**下划线开头**的变量名，而 R 的标识符不允许以下划线开头，`source()` 直接抛 `unexpected symbol`。该脚本是阶段2 的强制共享配置，所有方法脚本都要 source 它——**会导致阶段2 任何方法都跑不起来**。已改为 `config_paths` / `config_found` / `cfg_path`。

### Fixed — 数据画像（测试驱动）

- **`"None"` 被吞成缺失值**：`pd.read_csv` 默认 `keep_default_na=True`，会把 `None`/`NA`/`NULL` 等**合法分类**转成 NaN。"无共病"被当成"数据缺失"，缺失率 0% → 30%，后续插补策略全错且**不报错**。改为 `keep_default_na=False` + 显式 `NA_VALUES`，并新增 `ambiguous_na_tokens` 把歧义取值暴露给用户。
- **ID 角色判定子串误伤**：`ID_PATTERNS` 含裸 `"id"`，用 `in` 做子串匹配，`comorbidity`（内含 `bid`→`id`）被误判为 ID 变量并排除出分析。改为按 token 整词判定（`_is_id_variable`），支持 `patient_id` / `patientId` / `case_id`，不再误伤。

### Added — 探索性分析模式（测试驱动）

- **`analysis_mode: confirmatory | exploratory`**：横断面等探索性研究允许"先有数据、后有结局"。
- 阶段0 关卡判据放宽为 `variables.outcome` 非空 **或** `analysis_mode: exploratory`；同步修改 `commands/clinpub.md`、`workflows/next-step.md`、`commands/data-prep.md` 与 codex 对应技能。

### Added — DeepSeek Harness（主版本）

- **自 3.0 起 DSH 为主实现**：`.dsh/skills/`（14 个技能，仓库内自动发现）+ `dsh/`（共享核心）。
- 迁移设计见 `docs/MIGRATION-TO-DSH.md`。

### Removed

- **Qoder 平台（`qoder/`）整体移除**（2026-10-18）。该平台自 3.0 起不再维护，历史版本可从 git 记录取回。
- `agents/clinpub-planner.md`、`agents/clinpub-executor.md`
- `analysis_plan.waves`、`Wave`/`波次` 概念、`02-01-SUMMARY.md` 约定

## [Unreleased]

### Fixed — Claude Code
- **消除 hooks 双重定义**: hooks 配置仅内联保留于 `.claude-plugin/plugin.json`（官方支持的“或”选项之一），删除冗余的 `hooks/hooks.json`，避免双重执行风险（参考 anthropics/claude-code#34573）。CI 校验同步改为验证 plugin.json 内联 hooks 字段。

### Changed
- **文献搜索脚本升级**: 同步 ncbi-search v3——新增 `pmc_fetch.py`（PMC 开放获取全文）、`test_ncbi.py`（单元测试），升级 `ncbi_utils.py`（SQLite 缓存）/`ncbi_search.py`（EFetch 摘要）/`pubmed_search.py`（宽松 NL 策略）/`pubmed_fetch.py`（自动分批）至三平台一致（claude-code / codex / qoder）。
- **CI 一致性检查**: 纳入新增脚本 `pmc_fetch.py`、`test_ncbi.py`；同步 `data_profiler.py` 至三平台一致。
- **手稿输出收敛为单一文件**: 写作管线（claude-code / codex / qoder）手稿输出改为 `05_Manuscript/manuscript.md` 单一文件，各章节按 IMRAD 顺序直接追加，移除 `05_Manuscript/sections/` 段文件目录。
- **安装命令统一执行上下文**: README 与各平台 INSTALL.md 统一为仓库根目录执行安装命令（`git clone` + `cd clinpub`）；新增 `codex/marketplace.json` 与 Qoder 安装说明（v1.0.0 首发）。

### Removed
- **GitHub 自动 Release workflow**: 删除 `.github/workflows/release.yml`，推送 `v*` 标签不再自动创建 GitHub Release，改为手动发布。
- **codex 遗留文件清理**: 移除 `codex/clinpub/scripts/scripts/` 嵌套目录（脚本上移一层）、失效的 `hooks/hooks.json`、`CONVERSION_SUMMARY.md` 及过时设计文档（`docs/superpowers/`）。

## [2.3.0] - 2026-07-28

> 本次改动最初作用于 **Claude Code 版本**（`claude-code/`）；qoder 已于 2026-08-18 同步至 v2.3.0，OpenAI Codex 已于 2026-09-07 同步至 v2.3.0。

### Added — Claude Code
- **`/clinpub:improving`**: 独立的论文持续改进工具——自审稿件 → 生成修改计划 → 用户确认 → 直接修稿（全文 + 分析代码重跑 + 数值级联）。不写回复信、不模拟审稿人，可反复调用。新增 `commands/improving.md` 与 `pipeline/workflows/improving.md`。
- **`/clinpub:coverletter`**: 依据初始化设定的目标期刊，联网搜集期刊官网投稿要求（WebSearch/WebFetch，含离线回退），生成量身定制的 Cover Letter（输出 `05_Manuscript/cover_letter.md`）。新增 `commands/coverletter.md` 与 `pipeline/workflows/coverletter.md`。

### Changed — Claude Code
- **`/clinpub:review` 改为“投稿后”流程**: 由“模拟审稿”改为处理用户提供的真实审稿意见——录入意见 → 撰写逐条回复信 + 改进方向 → 用户确认 → 调用 `improving` 执行修稿（单一修稿实现，不重复）。改写 `commands/review.md` 与 `pipeline/workflows/review.md`。
- **初始化显式询问目标期刊**: `initialize` / `init-project.md` 将目标期刊提升为必问项，不再预设；`project_config.yml` 模板去除 `target_journal: "SCI Q1/Q2"` 默认值。适配任意临床研究文章类型。
- **管线收敛为阶段0-3**: 写作（阶段3）为核心管线终点；improving / coverletter / review 与 modify 一样为“随时可调用”的独立工具，不占 Phase 编号。相应更新 hooks（workflow-guard.js / phase-boundary.sh）、编排器（overview / do / next-step）、门控（gates.md）、里程碑（milestone.md）及相关参考文档。
- **文案去期刊硬绑定**: 移除文档/清单中的 “SCI Q1/Q2”“simulated peer review” 硬绑定表述。
- **版本**: `2.2.1 → 2.3.0`（claude-code 插件与 npm 元数据）。

### Added — OpenAI Codex
- **`clinpub:improving`**: 独立的论文持续改进工具——自审稿件 → 生成修改计划 → 用户确认 → 直接修稿（全文 + 分析代码重跑 + 数值级联）。不写回复信、不模拟审稿人，可反复调用。新增 `codex/clinpub/skills/clinpub-improving/` 与 `pipeline/workflows/improving.md`。
- **`clinpub:coverletter`**: 依据初始化设定的目标期刊，搜集期刊投稿要求并生成量身定制的 Cover Letter（含离线回退）。新增 `codex/clinpub/skills/clinpub-coverletter/` 与 `pipeline/workflows/coverletter.md`。

### Changed — OpenAI Codex
- **`clinpub:review` 改为“投稿后”流程**: 由“模拟审稿”改为处理用户提供的真实审稿意见——录入意见 → 撰写逐条回复信 + 改进方向 → 用户确认 → 调用 `improving` 执行修稿。改写 `codex/clinpub/skills/clinpub-review/` 与 `pipeline/workflows/review.md`。
- **初始化显式询问目标期刊**: `clinpub-init` 将目标期刊提升为必问项，不再预设；适配任意临床研究文章类型。
- **管线收敛为阶段0-3**: 写作（阶段3）为核心管线终点；improving / coverletter / review 与 modify 一样为独立工具，不占 Phase 编号。同步更新编排器（clinpub / next-step / overview）、门控（gates.md）、里程碑（milestone.md）及相关参考文档。
- **文案去期刊硬绑定**: 移除 Codex 文档/清单中的 “SCI Q1/Q2” 与 “simulated peer review” 硬绑定表述。
- **版本**: `2.2.0 → 2.3.0`（`codex/clinpub/.codex-plugin/plugin.json` 与 `codex/marketplace.json`）。

## [2.2.1] - 2026-07-10

### Changed
- **`/clinpub:init` 重命名为 `/clinpub:initialize`**: 避免与 Claude 原生 `/init` 命令冲突，原生命令恢复可用。插件命名空间仍保持 `clinpub`，命令行为不变。

## [2.2.0-codex] - 2026-07-04

### Added — OpenAI Codex Plugin Support
- **`.codex-plugin/plugin.json`**: Codex plugin manifest (converted from Claude Code format)
- **`skills/` directory**: 11 skills converted from Claude Code commands
  - `clinpub help` — Command reference overview
  - `clinpub-data2idea` — Topic mining from data
  - `clinpub-init` — 阶段0: Project initialization
  - `clinpub-data-prep` — 阶段1: Data cleaning
  - `clinpub-analysis` — 阶段2: Statistical analysis
  - `clinpub-writing` — 阶段3: IMRAD manuscript writing
  - `clinpub-review` — 阶段4: Peer review simulation
  - `clinpub next` — Phase gate review
  - `clinpub-modify` — Modify analysis outputs
  - `clinpub` — Workspace state router
  - `clinpub next` — Auto-advance to next phase
- **Codex plugin structure**: Complete plugin with agents, pipeline, scripts, hooks
- **Validation**: Plugin passes all validation checks
- **Documentation**: README.md, INSTALL.md, CONVERSION_SUMMARY.md

### Changed — Plugin Format Conversion
- **Manifest**: `.claude-plugin/plugin.json` → `.codex-plugin/plugin.json`
- **Commands**: `commands/*.md` → `skills/*/SKILL.md` (YAML frontmatter format)
- **Preserved**: All agents, pipeline, scripts, hooks unchanged

### Documentation
- **codex/README.md**: Comprehensive plugin documentation
- **codex/INSTALL.md**: Detailed installation guide with troubleshooting
- **codex/CONVERSION_SUMMARY.md**: Migration guide from Claude Code

## [2.2.0] - 2026-06-29

### Added — 共享图表配置脚本（_figure_config.R）
- **`pipeline/templates/_figure_config.R`**: 共享图表配置模板，整合 `theme_pub()`、`get_palette()`、`save_figure()` 等可视化函数
- **阶段2 `generate_figure_config` 步骤**: 从模板生成 `04_Outputs/_figure_config.R`，所有方法 R 脚本通过 `source()` 加载
- **`r_patterns.md §1.0.1`**: 新增共享配置脚本使用说明，§1.1–§1.5 代码段标注为参考实现
- **跨文档约束**: `AGENTS.md`、`analyst-agent.md`、`modify-agent.md`、`agent-contracts.md` 统一添加 `_figure_config.R` 引用规则与代码独立性例外说明
- **终验检查项**: 分析工作流新增第 7 项验证 — 确认 `_figure_config.R` 存在且所有方法脚本包含 `source()` 调用

### Added — 原生文献检索能力
- **`scripts/ncbi_search.py`**: 多数据库主入口（PubMed / Gene / Protein / dbSNP / ClinVar / Taxonomy 等，vendor 自 `github.com/Side-Peng/ncbi-search`，MIT）
- **`scripts/pubmed_search.py`**: PubMed 专用检索（MeSH 自动扩展、年份/类型过滤）
- **`scripts/pubmed_fetch.py`**: PMID 批量取全文
- **`scripts/ncbi_utils.py`**: E-Utilities 共享工具（限流、重试、XML 清洗）
- **`pipeline/references/query_syntax.md`**: PubMed 检索语法参考

### Changed — 文献检索由外部 skill 改为内置
- **`reference-agent.md`**: 移除 `check_skill_availability` 步骤及 Mode A/B/C fallback；统一通过 Bash 调用 `scripts/ncbi_search.py`
- **`topic-miner-agent.md`**: 移除 ncbi-search 可用性检测；subagent prompt 改为直接 Bash 调用
- **`pipeline/workflows/data2idea.md`**: parallel dispatch subagent prompt 改为直接 Bash 调用
- **`pipeline/references/pre-phase-research.md`**: Track A / Track B 搜索渠道改为内置脚本
- **`AGENTS.md`**: `## External Skills` 段删除 `ncbi-search` 条目；Agent Routing 表补充内置脚本备注；Quirks 段注明 v2.1 起 native
- **`README.md`**: 中英文「关联技能 / External Skills」表删除 `ncbi-search`
- **`INSTALL.md`**: Claude Code skills 列表删除 `ncbi-search`（已是内置能力）

### Fixed
- **`marketplace.json`**: source 格式从 `git:` 改为相对路径 `'./'`，修复插件市场显示问题
- **`README.md`**: 版本徽章修正为实际版本号，marketplace 安装命令纠正

### Removed
- 所有 agent / workflow / reference 文档中的 `skill("ncbi-search")` 调用与 ncbi-search 可用性检测逻辑

## [2.0.0] - 2026-06-19

### Added — Claude Code Plugin 标准迁移
- **`.claude-plugin/plugin.json`**: 插件清单文件（Plugin 身份与元数据）
- **`hooks/hooks.json`**: 声明式钩子配置（3 个 PreToolUse hooks，替代 settings.json 手动注册）
- **`${CLAUDE_PLUGIN_ROOT}`**: 运行时路径替换（替代 install.js 的 `@./` 重写）

### Added — 图表主题与配色配置化
- **`quality.theme`** (`project_config.yml`): 新增 6 个可自定义参数（variant / base_size / base_family / legend_position / title_hjust / panel_border）
- **`quality.color_palette`** (`project_config.yml`): 新增 4 个配色配置字段（preset / custom_colors / group_mapping / continuous）
- **Config Protocol** (`r_patterns.md §1.2`): `apply_theme()` 包装器，从 config 动态读取主题参数
- **Color Config Protocol** (`r_patterns.md §1.1`): `get_palette()` + `get_continuous_scale()` 配色生成器，支持 auto / 预设 / 自定义色值
- **阶段2 `discuss_and_confirm`**: 新增第 8 项（主题样式讨论）和第 9 项（配色方案讨论），用户可在分析前自定义图表风格
- **R 依赖**: 新增 `yaml`、`RColorBrewer`、`viridis` 包

### Changed — 分发方式
- **npm → Plugin**: 从 `npx clinpub@latest` 迁移到 `claude plugin install clinpub`
- **命令命名空间**: `/clinpub-xxx` → `/clinpub:xxx`（Plugin 标准冒号分隔符）
- **命令目录扁平化**: `commands/clinpub/*.md` → `commands/*.md`（Plugin 自动发现）
- **`SKILL.md` → `OVERVIEW.md`**: 避免无 skills/ 目录时自动加载为重复 skill
- **`commands/clinpub/clinpub.md` → `commands/overview.md`**: 重命名避免 `/clinpub:clinpub` 冗余命名
- **`analyst-agent.md`**: `load_project_config`、`statistical_analysis`、`publication_standards` 三处更新引用 Config Protocol 和 Color Config Protocol
- **`analysis.md`**: `discuss_and_confirm` 步骤扩展讨论清单，PLAN YAML 模板追加 `theme_config` 和 `color_palette_config` 段
- **`project_config.yml` 模板**: `quality` 段追加 `theme` 和 `color_palette` 子段

### Removed
- **`bin/install.js`**: 自定义 npm 安装器（504 行），功能完全由 Plugin 系统替代
- **`bin/` 目录**: 不再需要自定义安装脚本
- **`package.json` 的 `bin`/`files`/`scripts` 字段**: 最小化保留元数据

### Fixed
- **`next-step.md` 项目相对 @-引用**: 移除 3 个指向项目文件的 `@./` 引用，改为运行时 Read 指令

## [1.2.0] - 2026-05-25

### Changed
- **README**: 命令参考移除被废弃的 `clinpub` 一键入口，改为独立 Phase 命令参考
- **文献检索**：移除内置 ncbi_search.py/pubmed_search.py，统一使用 ncbi-search skill

### Removed
- **`/clinpub` 一键五阶段执行**：改为独立 Phase 命令参考（见 commit 0866e2b）
- **内置文献检索脚本**：ncbi_search.py, pubmed_search.py, ncbi_client.py, tavily_search.py — 统一由外部 skill 替代

### Docs
- `docs/getting-started.md` 泛化：移除示例数据具体引用，教程改为通用描述

## [1.2.1] - 2026-05-28

### Added — 阶段1-6 优化（GSD 管线执行）

**阶段1: Bug Fixes**
- Hook 正则修复（STATE.md 标识行 + getCurrentPhase() 新正则）
- 数据联动更新（data-prep 重新进入检测 + 工作流刷新步骤）

**阶段2: 断点续做**
- `/clinpub` 命令：工作区状态自动检测 + NL 意图路由
- `/clinpub next` 命令 + clear 提示标准化

**阶段3: 手稿拼接+引用策略**
- 分段撰写流程改造：逐段顺序撰写 + reference-agent 预搜索 + 用户审阅 pause
- 引用管理与交叉引用：shared reference library JSON schema + placeholder 约定 + 去重规则
- 终稿拼接输出：7 步拼接协议（段落合并 + 占位符替换 + 引用统一编号 + YAML frontmatter）
- 命令入口适配：更新 writing.md 描述和引用
- 引用策略标准化：策略参考文档 + writing workflow 插入讨论步 + reference-agent 搜索支持 IF/年份过滤

**阶段4: 方法增强**
- 组间对比方法决策树文档（comparison-methods.md）：2组/3+组×连续/分类+配对 全覆盖 + 效应量标准
- reference-agent method_search 未知方法搜索模式 + 分析工作流集成

**阶段5: Phase 前调研流程**
- pre-phase-research.md 参考文档（轨道选择、Track A/B 协议、RESEARCH.md 模板）
- reference-agent 扩展：phase_research 模式

**阶段6: 图表+文档优化**
- theme_pub() 主题优化：base_size=10, base_family=sans, legend.right, axis.line
- 新增 §2.9 KM 生存曲线美化模板（survminer + theme_pub）
- 新增 §2.10 相关性矩阵热图模板（ggcorrplot + theme_pub）
- 字体族跨平台说明 + Nature 系列尺寸参考
- 方法说明模板（pipeline/templates/method-readme.md）
- 文档中文本地化：6 个管线文档 README→方法说明 + 13 处遗留修复

## [1.1.0] - 2026-04-27

### Added — Must Have 补全
- **3 new agents**: Clinpub Planner, Clinpub Executor (atomic commits), Clinpub Verifier (adversarial verification)
- **4 new references**: mandatory-initial-read, gates (IRB/data/analysis/submission), verification-patterns (8 patterns), agent-contracts (7 agents)
- **5 new templates**: UAT, VALIDATION, verification-report, spec, context
- **3 hooks**: workflow-guard (JS), phase-boundary (SH), prompt-guard (JS for injection detection)
- **`.claude/settings.json`**: Hook registration for Claude Code

### Added — GitHub 发布准备
- **SKILL.md**: Claude Code skill 入口文件（触发描述 + 命令参考 + 架构说明）
- **INSTALL.md**: 安装指南（npx clinpub-cc 一键安装 + 依赖说明 + 故障排除）
- **requirements.txt**: Python 依赖清单
- **`bin/install.js`**: npm 安装器（复刻 GSD 模式：commands → skills 转换 + 资源复制 + 路径重写）
- **`.github/workflows/release.yml`**: 自动发布工作流（打 tag → npm publish → GitHub Release）

### Updated
- **CLAUDE.md**: Added agents, hooks, references, templates, agent routing table
- **README.md**: Added quality gates, hooks, 7-agent collaboration table

## [1.0.0] - 2026-04-27

### Added
- **阶段0 — init**: Project initialization with research framework discussion
- **阶段1 — data-prep**: Data cleaning, EDA, cleaned.csv generation
- **阶段2 — analysis**: Wave-based statistical analysis (10 methods)
- **阶段3 — writing**: IMRAD manuscript writing with Humanizer rules
- **阶段4 — review**: Simulated peer review and revision
- **Topic mining** (`clinpub:data2idea`): Data-driven paper topic discovery
- **Milestone system**: Phase-gate verification with user sign-off
- **Checkpoint system**: In-phase decision points and verification gates
- **4 Agents**: Topic Miner, Analyst, Reference, Writer
- **5 study type templates**: RCT, cohort, case-control, cross-sectional, descriptive
- **12 analysis methods**: Baseline table, group comparison, regression, survival, etc.
- **GSD architecture**: Commands → Workflows → Agents → Scripts layered design
