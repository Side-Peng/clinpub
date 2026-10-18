---
name: data2idea
description: "从临床数据表（CSV/XLSX）挖掘选题。分析变量结构、分布特征、缺失情况与相关性，结合 PubMed 文献检索定位研究空白，产出 3–5 个带可行性评分的结构化候选课题。不做统计分析，不写手稿。"
argument-hint: "<filepath>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
Clinical research topic mining consultant. Input patient-level CSV or XLSX data, output structured paper topic report with 3-5 candidate topics.

**Does not perform statistical analysis or manuscript writing — only topic discovery.**
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/data2idea.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/topic-miner-agent.md"`
</execution_context>

<process>
Execute the data2idea workflow from pipeline/workflows/data2idea.md end-to-end.

The dedicated **topic-miner-agent** (agents/topic-miner-agent.md) handles execution:

1. **Data profiling**: Run data_profiler.py → variable inventory, distributions, missing patterns, study type prediction
2. **Parallel literature scan**: Dispatch multiple subagents to search PubMed simultaneously — one per variable group — ensuring deep coverage and compound novelty detection
3. **Topic generation**: 3-5 structured candidate topics with feasibility scores

After user selects a topic, guide them to use `clinpub` for full analysis pipeline.
</process>

<success_criteria>
- Data profile generated (variable inventory, missing report, study type prediction)
- Literature scan completed with gap analysis
- 3-5 candidate topics with feasibility scores, variable mapping, and target journals
- User has selected a topic (or returned to refine)
</success_criteria>
