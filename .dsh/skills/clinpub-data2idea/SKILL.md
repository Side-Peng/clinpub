---
name: clinpub-data2idea
description: "从临床数据表（CSV/XLSX）挖掘选题。分析变量结构、分布特征、缺失情况与相关性，结合 PubMed 文献检索定位研究空白，产出 3–5 个带可行性评分的结构化候选课题。不做统计分析，不写手稿。"
whenToUse: "有数据但还没定选题，想让数据告诉你能做什么研究时。"
---

# clinpub-data2idea

## 目标
Clinical research topic mining consultant. Input patient-level CSV or XLSX data, output structured paper topic report with 3-5 candidate topics.

**Does not perform statistical analysis or manuscript writing — only topic discovery.**

## 流程
Execute the data2idea workflow from pipeline/workflows/data2idea.md end-to-end.

The dedicated **topic-miner-agent** (agents/topic-miner-agent.md) handles execution:

1. **Data profiling**: Run data_profiler.py → variable inventory, distributions, missing patterns, study type prediction
2. **Parallel literature scan**: Dispatch multiple subagents to search PubMed simultaneously — one per variable group — ensuring deep coverage and compound novelty detection
3. **Topic generation**: 3-5 structured candidate topics with feasibility scores

After user selects a topic, guide them to use `clinpub` for full analysis pipeline.

## 成功标准
- Data profile generated (variable inventory, missing report, study type prediction)
- Literature scan completed with gap analysis
- 3-5 candidate topics with feasibility scores, variable mapping, and target journals
- User has selected a topic (or returned to refine)

---

## 执行流程（内联自 pipeline/workflows/data2idea.md）

Mine paper topics from clinical data tables without performing statistical analysis. Three-step process: data profiling → literature scanning → topic generation. Each step shows intermediate results for user feedback.

Agent: @./agents/topic-miner-agent.md — dedicated topic mining specialist.

<process>

### run_data_profile
Read user-provided CSV or XLSX and generate comprehensive data profile:

```bash
python scripts/data_profiler.py <filepath> --output idea/data_profile.json
```

Profile includes:
1. **Variable inventory**: name, data type, missing rate, unique count
2. **Distribution summaries**: 5-number summary for continuous, frequencies for categorical
3. **Missing pattern**: high-missing (>20%) flagged, medium (5-20%) noted
4. **Correlation matrix**: Spearman for numeric variables (warning if >30)
5. **Variable role detection** (auto-inferred):
   - Outcome: outcome, diagnosis, status, death, event, 结局
   - Exposure/group: group, treatment, arm, exposure, trt, 随机
   - Time: time, follow, survival, months, days, 随访
   - Covariates: age, sex, gender, bmi, smoke, etc.
   - Biomarkers: biomarker, protein, gene, serum, plasma, score, etc.
6. **Study type prediction**:
   - Randomized group + baseline + follow-up → RCT
   - Time-to-event + exposure → cohort
   - Case/control + matching ID → case-control
   - Single time-point + exposure + outcome → cross-sectional
   - Descriptive variables only → descriptive
   - Multiple biomarkers + outcome → biomarker panel
7. **Sample size assessment**:
   - <50: descriptive only
   - 50-200: simple comparison
   - 200-500: regression analysis possible
   - 500-2000: most methods supported
   - >2000: complex modeling + subgroup analysis

Present profile to user. Confirm variable roles before proceeding.

### literature_scan_parallel
Based on data profile, dispatch parallel PubMed literature searches — one subagent per variable group.

### Phase 1: Variable Grouping

From `idea/data_profile.json`, extract searchable variable groups:

1. **Disease context**: from user description + variable names → base disease keywords
2. **Biomarker/exposure variables**: each detected biomarker or exposure variable → one search task
3. **Outcome variable**: outcome-related search
4. **Combination search**: top 2-3 variable pairs (e.g., biomarker + outcome) → cross-reference search

Group variables into search tasks (typically 3-8 tasks). Skip variables with <5% prevalence or purely descriptive (ID, date).

### Phase 2: Parallel Dispatch

For each search task, dispatch a **parallel subagent** using the Task tool:

```
Subagent prompt template (one per variable):
─────────────────────────────
You are a PubMed research scout. Search for existing literature on:

**Variable**: {variable_name}
**Disease context**: {disease_keywords}
**Search query**: "{variable_name}" AND "{disease}" AND ("cohort" OR "RCT" OR "observational" OR "association")
**Additional filters**: Last 5 years, English, Human

Tasks:
1. Run PubMed search via the built-in script:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/ncbi_search.py" "<search query>" \
     --db pubmed --years 5 --max 20
   ```
2. Count relevant papers (last 5 years)
3. Identify top 3 high-impact papers (journal IF, citation count if available)
4. Note research trends: increasing/decreasing/stable publication rate
5. Identify research gaps: what has NOT been studied

Return structured summary:
- Variable: {name}
- Search query used: ...
- Papers found (5yr): N
- Top papers: [PMID, title, journal, year]
- Research trend: ↑/↓/→
- Gap identified: one-sentence description
- Novelty score: 🟢/🔶/✅
─────────────────────────────
```

Dispatch all subagents **in parallel** (use single message with multiple Task calls).

### Phase 3: Aggregate Results

After all subagents return:

1. Collect all summaries into `idea/literature_scan.md`
2. Cross-reference gaps across variables — identify **compound novelty** (variable A studied alone, variable B studied alone, but A+B never combined)
3. Rank variables by novelty score
4. Flag any variables with ✅ (well-studied) — suggest differentiation strategy

Check API key before search:
```bash
if [ -z "$NCBI_API_KEY" ]; then
  echo "⚠️ NCBI_API_KEY not set. PubMed at 3req/s rate limit. Parallel search may be slower."
fi
```

Write aggregated results to `idea/literature_scan.md`: per-variable summaries, cross-variable gap analysis, compound novelty findings.

### generate_topics
Synthesize 3-5 candidate topics from data profile + literature scan:

**Topic selection strategy:**
- Large dataset (>5000 rows) → prioritize cohort or RCT topics
- Many biomarkers (>10) → prioritize marker panel or LASSO topics
- No grouping/outcome variables → descriptive study
- User-specified direction → match priority

**Each topic includes:**
- Working title
- Feasibility score (⭐1-5)
- Research type (cohort/RCT/cross-sectional/case-control/diagnostic/descriptive)
- Core research question + hypothesis
- Variable mapping (outcome, exposure, covariates, subgroups)
- Proposed analysis methods
- Key figures/tables needed
- Novelty/gap rationale
- Recommended target journals
- Risk notes (sample size, confounding, variable limitations)

Write complete report to `idea/选题报告.md`. User selects topic → guide them to `clinpub` for full pipeline.

</process>

<success_criteria>
- Data profile generated with variable inventory, roles, study type prediction
- Literature scan with gap analysis completed
- 3-5 candidate topics with feasibility scores, variable mapping, target journals
- User has selected a topic (or returned to refine search)
- User informed about next steps (clinpub pipeline)
</success_criteria>

---

## 参考资源

路径相对本技能目录（`../../../dsh/` 指向仓库共享核心）。**按需读取**，不要一次全读。

- `../../../dsh/pipeline/references/pre-phase-research.md`
- `../../../dsh/pipeline/references/reference-library.md`
- `../../../dsh/agents/topic-miner-agent.md`

---

> 本文件由 `node dsh/build.mjs` 生成，请勿手改。修改源文件：`claude-code/commands/` 与 `claude-code/pipeline/workflows/`。
