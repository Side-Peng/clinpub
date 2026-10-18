# 测试发现清单（FINDINGS）

> 记录验证过程中发现的**管线本身的问题**，而不是测试数据或测试配置的问题。
> 每条发现都要走完：现象 → 根因 → 修复 → 三平台同步 → CHANGELOG → 复验。

## 判定标准

| 类型 | 记不记 | 例子 |
|---|---|---|
| **管线缺陷**（要改插件） | ✅ 记，并修 | 关卡判据写死、字段不存在、脚本不读某字段 |
| 文档与实现不一致 | ✅ 记，并修 | workflow 声称读 `project.title`，模板里没这字段 |
| 测试数据/配置问题 | ❌ 不记（不是插件问题） | 测试数据里 `comorbidity` 分四类 |
| 措辞/格式偏好 | ⚠️ 直接改，不单独立条 | 中英标点混用 |

## 状态汇总

| 编号 | 标题 | 严重度 | 状态 |
|---|---|---|---|
| F-001 | Phase 0 关卡强制要求 `variables.outcome`，探索性研究被卡死 | 高 | ✅ 已修 |
| F-002 | 标题机制整条链路断裂（字段缺失 + 脚本不读 + BOM） | 高 | ✅ 已修 |
| F-003 | `"None"` 被 pandas 当缺失值吞掉，合法分类静默变成 30% 缺失 | **严重** | ✅ 已修 |
| F-004 | ID 角色判定用裸 `"id"` 子串匹配，`comorbidity` 被判成 ID | 中 | ✅ 已修 |
| F-005 | `_figure_config.R` 模板用下划线开头变量名，R 语法错误，**从未能 source 成功** | **严重** | ✅ 已修 |
| F-006 | `r_patterns.md` 的森林图模板用已废弃的 `geom_errorbarh()` | 低 | ✅ 已修 |
| F-007 | 拼装脚本不解析占位符、产生重复标题、小节与章节同级 | 中 | ✅ 已修 |
| F-008 | DSH 技能里"调用 reference-agent"指向空气（agent 卡未进 refs） | 中 | ✅ 已修 |
| F-009 | 拼装脚本从未实现引用编号与 References 生成 | **严重** | ✅ 已修 |
| F-010 | 图表规范未落地：字号不随画布、轴标题转平、主图导出位图 | 高 | ✅ 已修 |
| F-011 | 改导出格式后旧 png/tiff 残留，形成"假更新" | 中 | ✅ 已修 |

---

## F-001 — 探索性研究被 Phase 0 关卡卡死

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 0 初始化 |
| 现象 | 横断面探索性研究（用户明确"不定义结局"）无法通过 Phase 0 关卡 |
| 根因 | 关卡判据硬编码 `variables.outcome` 非空，未考虑"先有数据、后有结局"的研究形态 |
| 影响面 | 所有探索性/数据驱动型研究（横断面、描述性、data2idea 承接的项目） |
| 修复 | 新增 `analysis_mode: confirmatory \| exploratory`；判据改为 `outcome` 非空 **或** `analysis_mode: exploratory` |
| 改动位置 | `pipeline/templates/project_config.yml`、`commands/clinpub.md`、`pipeline/workflows/next-step.md`、`commands/data-prep.md`、codex `clinpub` / `clinpub-data-prep` 技能 |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| CHANGELOG | `[3.0.0] Added — 探索性分析模式（测试驱动）` |
| 复验 | 测试项目 `analysis_mode: exploratory` + `outcome: ""` → 关卡自检通过 ✅ |

---

## F-002 — 标题机制整条链路断裂

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 0 初始化（用户提出"标题最后再定"） |
| 现象 | 设计要求"写完全文再拟定标题"，但实现不支持 |
| 根因 | 三个独立缺陷叠加：<br>① `project_config.yml` 模板**没有** `project.title` 字段<br>② `assemble_manuscript.py` **完全不读**标题<br>③ 读取配置用 `utf-8`，Windows 的 BOM 会让首行 `project:` 匹配失败 |
| 影响面 | 所有项目——`manuscript.md` 从来就没有标题，且 workflow 指示 agent 去读一个不存在的字段 |
| 修复 | ① 模板新增 `project.title`（注明 Phase 3 写入）<br>② 脚本读取并输出到 frontmatter + 一级标题，为空时**警告**而非失败<br>③ 改用 `utf-8-sig`<br>④ `writing.md` 的 frontmatter 步骤改为"只追加"，防止 agent 覆盖脚本写入的 `title` |
| 改动位置 | `pipeline/templates/project_config.yml`、`scripts/assemble_manuscript.py`、`pipeline/workflows/writing.md` |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅（脚本 SHA256 三份一致） |
| CHANGELOG | `[3.0.0] Added — 标题延后拟定（测试驱动）` |
| 复验 | 无标题 → 警告；写入标题 → frontmatter `title` + `# 标题` 正确 ✅ |

### 附带教训：BOM 已第三次咬人

1. section 文件解析（`assemble_manuscript.py` 的 `parse_frontmatter`）
2. 命令文件描述解析（`dsh/build.mjs` 的 `splitFrontmatter`）
3. 本次配置读取（`read_project_title`）

**规律**：凡是用 PowerShell `Set-Content -Encoding UTF8` 或 Windows 编辑器产出的文件都带 BOM。
**对策**：所有文本读取一律用 `utf-8-sig` 或显式 `lstrip("\ufeff")`；所有文本写入一律用
`(New-Object System.Text.UTF8Encoding($false))`（无 BOM）。

---

## F-003 — `"None"` 被当成缺失值吞掉（严重）

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 1 数据画像 |
| 现象 | `comorbidity` 有 36 例（30%）被报为缺失，但原始 CSV 里这 36 例写的是 `None`（= 无共病） |
| 根因 | `pd.read_csv` 默认 `keep_default_na=True`，pandas 的默认 NA 记号表**包含 `"None"`**。于是"无共病"这一**合法分类**被静默转换成 NaN |
| 危害 | 缺失率虚高（0% → 30%），触发错误的缺失处理策略（本该四分类分析，却变成"MICE 插补 30% 缺失变量"）。**不报错、不警告**，是最危险的一类缺陷 |
| 放大效应 | `高缺失` 列表里出现该变量 → 若照做，会对一个根本没缺失的分类变量做插补 |
| 修复 | ① 读取改为 `keep_default_na=False` + 显式 `NA_VALUES`（空串、NA、N/A、NaN、NULL、-、.、缺失、不详）<br>② 新增 `AMBIGUOUS_NA_TOKENS` 扫描：被保留为分类但看起来像缺失的取值写入 `ambiguous_na_tokens` 告警 |
| 改动位置 | `scripts/data_profiler.py`（`NA_VALUES`、`_scan_ambiguous_na`、`profile_data`） |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅（SHA256 一致） |
| 复验 | 重跑画像：`comorbidity` 缺失 0；`ambiguous_na_tokens=[{column: comorbidity, tokens: [none]}]`；`missing_summary` 只剩 bmi 7.5% / baseline_score 5.0% / egfr 4.2% ✅ |

> **教训**：`"None"`、`"NA"`、`"NULL"` 在临床数据里既可能是缺失、也可能是分类。默认行为选了"当缺失"，
> 对"无共病 / 无吸烟史 / 无家族史"这类变量是错的。必须显式声明 NA 记号，并把歧义暴露给用户。

---

## F-004 — ID 角色判定子串误伤

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 1 数据画像 |
| 现象 | `comorbidity` 的 `role` 被判为 `id`，在 `role_summary.id` 里与 `patient_id` 并列 |
| 根因 | `ID_PATTERNS` 含裸 `"id"`，判定用 `p in name_lower` 子串匹配。`comorbidity` → `c-o-m-o-r-b-i-d-i-t-y` 内含 `"id"`（`bid`→`id`） |
| 危害 | 被当成行标识符 → 可能被排除出分析；而它其实是核心暴露变量 |
| 修复 | 改为**整词**判定 `_is_id_variable()`：按 `_ - 空格 /` 切词 + camelCase 拆分，只有 token 恰为 `id`/`pid` 或 `<常见前缀>+”id”`（patientid、subjectid…）才算 ID；同时移除 `MATCH_PATTERNS` 里的裸 `"id"` |
| 改动位置 | `scripts/data_profiler.py`（`_ID_EXACT`、`_ID_PREFIXES`、`_is_id_variable`、`MATCH_PATTERNS`、`detect_variable_role`） |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | `patient_id/subject_id/participantId/case_id/record_id/pid/id/序号` → `id`；`comorbidity` → `unknown`；`validity_score` → `biomarker`（不被 `id` 子串误伤）✅ |

---

## F-005 — `_figure_config.R` 模板语法错误，从未能加载（严重）

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 2 会话初始化（生成图表配置并 source 验证） |
| 现象 | `source("04_Outputs/_figure_config.R")` 报 `04_Outputs/_figure_config.R:28:2: unexpected symbol` |
| 根因 | 模板使用 `_config_paths` / `_config_found` / `_cfg_path` 作变量名。**R 的标识符不允许以下划线开头** |
| 危害 | 该脚本是 Phase 2 的强制共享配置，所有方法脚本都要 `source()` 它 → **Phase 2 一个方法都跑不起来**。而 workflow 里写着"生成后 `Rscript -e 'source(...)'` 验证"，说明这个验证步骤从未真正执行过 |
| 附带影响 | 2.x 起就一直存在；因为是模板文件，每个新项目都会复制同一份错误 |
| 修复 | 变量改名为 `config_paths` / `config_found` / `cfg_path`（含末尾 `rm()` 清理列表） |
| 改动位置 | `pipeline/templates/_figure_config.R` |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | `source()` 成功；`apply_theme/get_palette/save_figure/theme_pub` 四个函数均存在 ✅ |

> **教训**：模板文件也必须被真正执行过一次。这次能发现，是因为测试走的是"复制后立即 source 验证"，
> 而不是"复制完就当它能用"。

---

## F-006 — `r_patterns.md` 森林图模板使用已废弃 API

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 2 Batch 2（绘制效应量森林图） |
| 现象 | `geom_errorbarh()` 告警：`deprecated in ggplot2 4.0.0`，`height` 被静默改名为 `width` |
| 根因 | 管线自带规范 `r_patterns.md` 的森林图模式写于 ggplot2 3.x 时代 |
| 危害 | 目前仅告警；但 `height` 参数被静默改写，未来版本将直接移除该函数 → 模板会失效。且新手会照抄 |
| 修复 | 改为 `geom_errorbar(..., orientation = "y", width = ...)`，并加兼容提示（3.x/4.x 分支写法） |
| 改动位置 | `pipeline/references/r_patterns.md`（森林图模式） |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | 用新写法重跑方法 03，无任何 deprecation 告警 ✅ |

---

## F-007 — 拼装脚本的三个输出缺陷

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 3 拼装 |
| 现象 | ① `manuscript.md` 里 `{{Table:1}}` 等占位符原样残留；② `## Abstract` 后紧跟 `# Abstract`（重复标题）；③ 章节内小标题与章节标题同为 `##`，目录层级错乱 |
| 根因 | ① 脚本只拼装不解析占位符，而 workflow 的「终稿处理」要求 agent **手工**替换 —— 与"`manuscript.md` 是生成物、禁止手改"直接冲突，下次拼装必然覆盖；② 章节文件自带 `# Results`，脚本又加 `## Results`；③ 脚本未规范小标题层级 |
| 危害 | 交付物带未解析占位符；标题重复在投稿排版阶段会被期刊模板放大 |
| 修复 | ① 脚本新增 `resolve_placeholders()`（Table/Figure/SupplementaryTable/SupplementaryFigure/Method/Section），残留时 stderr 警告；② 剥掉章节自带的首个 H1；③ 章节内 H2–H5 统一下移一级 |
| 改动位置 | `scripts/assemble_manuscript.py`、`pipeline/workflows/writing.md`（终稿处理第 1 步改为"由脚本完成，不要手改"） |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | 占位符残留 0；H1 数量 1；层级 `# → ## → ###` 正确 ✅ |

> **教训**：凡是"生成物"与"手工补充"并存的流程，最终一定会有人手改生成物。
> 要么全部由脚本生成，要么把生成物当草稿——不能两个都声明。

---

## F-008 — DSH 技能缺少 agent 角色卡引用

| 项 | 内容 |
|---|---|
| 发现阶段 | 整合 ncbi-search v3 时 |
| 现象 | `clinpub-writing` / `clinpub-improving` / `clinpub-review` 的 workflow 里写着"调用 reference-agent 检索"，但技能正文与参考资源里**没有** `agents/reference-agent.md`。在 Claude Code 里 agent 是可分派的实体，在 DSH 里没有该机制——模型照着 workflow 找 agent，会找不到任何东西 |
| 根因 | `dsh/build.mjs` 只内联 workflow 与 pipeline 参考，agent 角色卡需要显式写进 `refs` 才会出现在技能里；早期只有 `modify`/`improving` 写了 agent 引用 |
| 危害 | DSH 版在涉及文献检索、写作、审稿回复的技能里缺失角色约定与检索流程细则，行为会退化为"随便搜一下" |
| 修复 | 给 `clinpub-writing`（writer + reference）、`clinpub-improving`（writer/reference/modify）、`clinpub-review`（reference）、`clinpub-data2idea`（topic-miner）补上 agent 卡引用 |
| 改动位置 | `dsh/build.mjs` |
| 同步 | DSH 重新生成 ✅ |
| 复验 | 4 个技能的「参考资源」段均含对应 agent 卡；`--check` 幂等 ✅ |

---

## F-009 — 引用链路整段未实现（严重）

| 项 | 内容 |
|---|---|
| 发现阶段 | Phase 3 补做文献（前一轮因无文献库被跳过，暴露后补测） |
| 现象 | `manuscript.md` 的 References 段只有一行注释 `<!-- 引用列表由 concatenation-protocol 生成 -->`，正文没有任何引用编号 |
| 根因 | `writing.md` 的「终稿处理」第 2 步写着"读 `reference_library.json`，按正文出现顺序从 [1] 连续编号，文末生成 Vancouver References"，`concatenation-protocol.md` 也有同样规定——但 `assemble_manuscript.py` **只输出一行占位注释**，没有任何实现。文档描述了能力，代码里不存在 |
| 危害 | 交付的手稿没有参考文献，且正文无法标注引用。这是投稿的硬阻断项；而它**不报错**，因为脚本认为"References 段已生成" |
| 为什么之前没发现 | 第一轮测试因无文献库、按"测试优先"跳过了文献步骤。**跳过文献 = 跳过整条引用链路**，所以缺陷一直隐藏在未执行的代码里 |
| 修复 | 脚本新增：① 解析章节里的 `{{cite:Key,Key}}` 标记；② 按正文首次出现顺序**跨章节连续编号**（Vancouver 规则，不是按文献库 id）；③ 生成 Vancouver References（作者≤6 人、超则 et al、每条带 `doi:`）；④ 键不在库中时 stderr 警告 |
| 改动位置 | `scripts/assemble_manuscript.py`、`pipeline/workflows/writing.md`（终稿处理第 2 步改为"由脚本完成"） |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | 12 篇真实文献（PubMed 检索，全部含 DOI）→ 正文编号 `[1]`–`[12]` 连续、`[1,2]` 等多引用格式正确、References 12 条全带 DOI、无残留 `{{cite:}}` ✅ |

> **教训**：这一条比 F-005 更隐蔽。F-005 至少"跑就会崩"，而 F-009 是"文档写了、代码没写、跑起来不报错"。
> 它之所以能存活，恰恰是因为测试跳过了文献环节——**没测到的路径等于没写过的代码**。

---

## F-010 — 图表规范未落地（一组四个缺陷）

| 项 | 内容 |
|---|---|
| 发现阶段 | 图表风格重做（用户对比真实项目后提出） |
| 现象 | ① 单栏 89 mm 图上字号是 6.5pt（应为 7pt）；② 纵轴标题躺平；③ 主图默认导出 tiff/png；④ 轴标签比轴标题小 0.5pt |
| 根因 | ① `theme_pub()` 不接收画布宽度，一律按双栏推导；② 覆盖 `axis.title.y` 时没带 `angle = 90`，`element_text()` 的 angle 默认 0，把继承来的旋转冲掉；③ 默认 `formats = c("png","svg","tiff")`，而 Nature 规定主图必须矢量（**不接受 tiff/png**）；④ `axis.text` 写死 `base_size - 0.5` |
| 影响面 | 所有图。②尤其隐蔽——不报错，只是标题方向错了 |
| 修复 | ① `theme_pub(width_mm=)` + `pub_base_size()` 按栏宽推导；② 补 `angle = 90`；③ 默认格式改为 `STYLE$main_formats`（pdf+svg），位图仅补材/预览；④ 轴标签与标题统一 `base_size`、统一 `face = "bold"` |
| 改动位置 | `pipeline/templates/_figure_config.R`、`project_config.yml`、`r_patterns.md` §1.2/§1.3/§2.1、`writing_standards.md` |
| 同步 | claude-code ✅ / dsh ✅ / codex ✅ |
| 复验 | 重画 3 张管线图：SVG 中 8 个文本元素全为 `7.00px / Arial / bold`；数值与重画前逐位一致 ✅ |

---

## F-011 — 导出格式变更后旧位图残留

| 项 | 内容 |
|---|---|
| 发现阶段 | 重画三张管线图 |
| 现象 | 改完脚本重跑后，目录里 `.png` / `.tiff` 仍在，且**文件大小与改动前完全相同**——它们没被重写，只是没被删除 |
| 根因 | 默认导出格式从 `png+svg+tiff` 改成 `pdf+svg` 后，`save_figure()` 不再写位图，但也不会清理旧文件 |
| 危害 | 极易误判"图已更新"。审稿/投稿时可能把旧图当新图提交 |
| 修复 | 新增预览开关 `CLINPUB_FIG_PREVIEW=1`：需要肉眼检查时额外导 png，默认不产出位图。残留旧文件需人工清理（未自动删除，避免误删用户素材） |
| 改动位置 | `pipeline/templates/_figure_config.R`（`save_figure`） |
| 复验 | 清空旧位图后带开关重跑 → 三张 png 均为新生成，尺寸 183×150 / 89×52 / 89×54 mm ✅ |

> **教训**：产物格式一旦变化，旧产物不会自己消失。"文件在"不等于"文件新"。

---

## 待观察（尚未定性）

| 观察 | 现状 | 何时定论 |
|---|---|---|
| 方法子目录延后创建 | 探索性模式下 Phase 0 无法确定方法，`03_AnalysisMethods/{id}/` 空置 | Phase 2 第一批确认方法时补建，看是否顺畅 |
| `comorbidity` 四分类 vs 有序负担评分 | 按四分类处理 | 看 Phase 2 是否影响解释 |
| `group` 在横断面下的角色 | 已定为分组比较变量 | 看 Phase 2/3 是否会与"干预效应"混淆 |
