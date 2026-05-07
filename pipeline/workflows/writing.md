---
name: writing
description: "Phase 3 orchestration: IMRAD sequential pipeline (Introduction → Methods → Results → Discussion). Each section: reference-agent pre-search → writer-agent draft → user review pause. Shared reference library (JSON) for cross-section deduplication. Placeholders for cross-references. Final concatenation in Plan 03-03."
---

<purpose>
Draft a complete IMRAD manuscript in Chinese (English figures/tables) targeting SCI Q1/Q2 journals. Two-agent workflow: Reference Agent conducts literature search, Writer Agent writes following the appropriate study type template.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
@./pipeline/references/reference-library.md
@./agents/reference-agent.md
@./agents/writer-agent.md
</required_reading>

<context_files>
@./pipeline/contexts/writing.md
</context_files>

<process>

<step name="discuss_writing_plan" priority="first">
Discuss with user before drafting:

1. **Core argument**: main finding and novelty angle
2. **Target journal**: confirm alignment with journal_standards.md
3. **Manuscript structure**: any journal-specific section requirements
4. **Reference Agent pre-search**: confirm search terms and strategy
5. **Figures/tables**: which outputs to include, order, and integration
</step>

<step name="reference_pre_search" priority="high">
Reference Agent performs comprehensive literature search:

1. Search PubMed for: disease domain + exposure/biomarker + outcome + population
2. Build citation_map.md with PMID, DOI, location, citation reason, supported argument
3. Build references.bib in Vancouver format with DOIs
4. Retrieve full text for key references via Unpaywall/pdf-reader
5. Write all outputs to `Reference/` directory
6. Write MANIFEST.yaml in `Reference/` listing writer-agent as consumer

See `@./agents/reference-agent.md` for detailed search protocol.
</step>

<step name="sequential_section_writing" priority="high">
以 IMRAD 顺序（Introduction → Methods → Results → Discussion）逐段撰写。每段分三阶段：reference-agent 文献预搜索 → writer-agent 撰写 → 用户审阅。

**顺序**: Introduction → Methods → Results → Discussion（D-01）

**核心约束**:
- 同一 writer-agent 分 4 轮对话（D-02），每轮仅给该段上下文
- 不扩展 writer-agent.md 的角色定义（D-02）
- 全文 >5000 字，自然成段论述，不用 bullet point（D-04）
- Results 段落风格：描述关键发现 + 指向图表，不使用 "As shown in Table X" 作为段落开头（D-13）

---

### 逐段循环

对每段（section in [introduction, methods, results, discussion]）执行以下三步：

#### Step A: Reference-Agent 文献预搜索（D-06）

调用 reference-agent 搜索该段的 PubMed 文献。搜索策略（参考 `agents/reference-agent.md`）:

| 段落 | 搜索关键词 | 引用量 |
|------|-----------|--------|
| Introduction | disease + exposure + outcome + population | 10-15 篇 |
| Methods | methodology, standard guidelines, published protocols | 3-5 篇 |
| Results | （非必要，仅对比时搜索） | 0-3 篇 |
| Discussion | 对比同类研究 + 机制解释 + 临床意义相关文献 | 15-25 篇 |

搜索后更新 `Reference/reference_library.json`：
1. 读取已有库
2. 新引用逐条去重（检查 `citation_key`）
3. 分配新 ID（max_id + 1）
4. 写入库
5. 更新 `Reference/MANIFEST.yaml`

#### Step B: Writer-Agent 撰写（D-02, D-03）

调用 writer-agent（同一 agent，不扩展 role 定义），仅传入该段所需的上下文：

| 段落 | 上下文来源（D-03 自动读取） |
|------|---------------------------|
| Introduction | Reference/reference_library.json（已有引用）、Reference/citation_map.md、Reference/literature_notes/ |
| Methods | project_config.yml（study_type, variables）、pipeline/templates/study_types/{type}.md、03_AnalysisMethods/*/README.md |
| Results | 04_Outputs/*/（所有 figure + table + README，其中 README 必须有「Results」subsection）|
| Discussion | Reference/reference_library.json、Reference/citation_map.md、project_config.yml（target_journal, scope）|

撰写规则：
- Methods 从 spec + analysis pipeline outputs 自动生成初稿（D-05）
- 使用 shared reference library (`Reference/reference_library.json`) 查询已有引用
- 使用占位符进行交叉引用：`{{Table:N}}` `{{Figure:N}}` `{{Method:name}}` `{{Section:name}}`（D-11）
- 自然成段论述，不使用 bullet point（D-04）
- 每段写入 `05_Manuscript/sections/`，命名规则：
  - `05_Manuscript/sections/01-introduction.md`
  - `05_Manuscript/sections/02-methods.md`
  - `05_Manuscript/sections/03-results.md`
  - `05_Manuscript/sections/04-discussion.md`

#### Step C: 用户审阅暂停（checkpoint）（D-01）

段撰写完成后，pause 等待用户审阅：

```markdown
## {段名} 初稿完成 — 请审阅

已写入 `05_Manuscript/sections/{文件名}`。

### 审阅要点
- [ ] {段名}的结构和内容是否符合预期
- [ ] 引用是否准确，引用量是否合适（{引用量建议}）
- [ ] 占位符是否需要调整或补充
- [ ] 语言风格是否自然（Humanizer 检查通过）
- [ ] 需要修改或补充的内容

### 下一步
- 输入 `通过` / `继续` → 进入下一段撰写
- 提出修改意见 → 调整当前段后重新审阅
```

当用户确认后（`通过` 或 `继续`），进入下一段循环。
</step>

<step name="humanizer_review" priority="medium">
Humanizer 自检在每个段落撰写时由 writer-agent 内嵌执行（见 writer-agent.md humanizer_rules 节），不再单独执行全篇 humanizer。

在 sequential_section_writing 步骤的 Step B（writer-agent 撰写）中，writer-agent 在每段写入前执行 Humanizer checklist：

| Check | AI Pattern | Fix |
|-------|-----------|-----|
| Paragraph openings | Sequential markers | Content-driven progression |
| Transition words | Repeated formulaic | Specific logical connectors |
| Sentence structure | Uniform patterns | Varied sentence types |
| Conclusions | Hollow or generic | Specific future direction |
| Citations | Impersonal | Author-contextualized |
| Explanations | Over-explaining methods | Just state, don't justify |

如果用户审阅时指出语言问题，writer-agent 直接在该段内修正，不重写全篇。
</step>

<step name="verify_manuscript" priority="high">
Final verification:

1. IMRAD structure complete (all 5 sections present)
2. All citations have DOIs
3. All referenced figures/tables exist in 04_Outputs/
4. STROBE/CONSORT checklist covered
5. Language consistent: Chinese manuscript body, English figures/tables
6. No AI-template patterns detected
7. Word count within target journal limits
8. References de-duplicated
9. MANIFEST.yaml exists in `05_Manuscript/` listing clinpub-verifier as consumer
10. 分段的完整性：05_Manuscript/sections/ 下 4 个段文件全部存在
11. 各段文件非空，不含 AI-template 模式

If manifest is missing, write it here.
</step>

<step name="placeholder_concatenation" priority="medium">
注意：终稿拼接（合并各段 → 替换占位符 → 统一引用编号 → 生成 manuscript.md + YAML frontmatter + sections/ 输出）在 {{@./.planning/phases/03-手稿拼接/03-03-PLAN.md}} 中处理。本步骤仅确保各段独立文件就绪。

当前各段文件和引用库就绪后，进入 checkpoint_confirm。
</step>

<step name="checkpoint_confirm" priority="medium">
Present a `checkpoint:verify` to user confirming the manuscript is ready for review:

- [ ] IMRAD structure complete
- [ ] All citations verified with DOIs
- [ ] Humanizer review passed
- [ ] STROBE/CONSORT compliance checked

If user requests changes, address them. If approved, proceed to milestone.
</step>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 3 and gate into Phase 4:

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 3
# 2. Collect writing decisions (study type template, target journal)
# 3. Generate .planning/phases/03-writing/MILESTONE.md
# 4. Update ROADMAP.md: Phase 3 → ✅ Complete, Phase 4 → 🔄 In Progress
# 5. Update STATE.md: current_phase → 4
# 6. Request user sign-off
```

See @./pipeline/workflows/milestone.md for full protocol.
</step>

</process>

<success_criteria>
- Complete IMRAD manuscript in 05_Manuscript/ (each chapter as draft.md)
- citation_map.md and references.bib in Reference/
- All citations have DOIs
- All figures/tables referenced in text
- STROBE/CONSORT compliance
- Humanizer review passed
- User has reviewed and approved draft
- 各段（Introduction/Methods/Results/Discussion）独立完成引用和撰写
- 每段写入 05_Manuscript/sections/ 独立文件
- 每段撰写前 reference-agent 完成文献搜索
- 每段撰写后用户完成审阅
- 引用库引用不重复
- 各段使用占位符进行交叉引用
- 全文各段合计 >5000 字
</success_criteria>
