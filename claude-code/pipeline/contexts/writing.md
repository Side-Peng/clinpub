# Writing Context

Use this context during Phase 3 manuscript writing.

## Language Policy

- **Manuscript body**: per `language.manuscript` config (default: Chinese)
- **Figures and tables**: per `language.figures_tables` config (default: English)
- **References**: Vancouver format with DOIs

Language modes:
| `language.manuscript` | 正文语言 | 图表语言 | 说明 |
|----------------------|---------|---------|------|
| `zh-CN`（默认） | 中文 | 英文 | 中文正文 + 英文图表 |
| `en-US` | 英文 | 英文 | 全英文论文 |
| `mixed` | — | — | 预留，暂未实现 |

## Chapter Writing Order

按**递进式**顺序撰写（ClinPub 3.0），见 `workflows/writing.md`：

0. 图表骨架 `FIGURE_SKELETON.md`（先排图表 + 一句结论）
1. **Results**（数据驱动：描述关键发现 + 指向图表，不解释）
2. **Methods**（从 `ANALYSIS_LOG.md` + 方法说明 + 配置自动生成，三段式）
3. **Discussion**（叙事结构：主要发现 → 与已有文献对比 → 机制 → 临床意义 → 局限性）
4. **Conclusion**（两句话）
5. 叙事设计 `NARRATIVE.md`（想清楚怎么引人入胜）
6. **Introduction**（倒金字塔：领域背景 → 知识缺口 → 研究目的与假设）
7. Abstract + Title

## Study Type Templates

Reference the appropriate template in `pipeline/templates/study_types/`:

| Type | File | Reporting Standard |
|------|------|-------------------|
| RCT | `rct.md` | CONSORT |
| Cohort | `cohort.md` | STROBE |
| Case-Control | `case_control.md` | STROBE |
| Cross-Sectional | `cross_sectional.md` | STROBE |
| Descriptive | `descriptive.md` | STROBE (observational) |

## Humanizer Reminders

Before finalizing each chapter, check:
1. No "first/second/finally" paragraph sequencing
2. No repeated formulaic transitions ("it is worth noting")
3. No uniform sentence structures (3+ consecutive same-pattern)
4. No hollow conclusions ("more research is needed")
5. Citations have specific author context, not "Studies show..."
6. Natural figure/table integration, not "As shown in Table X"

## Target Journal Standards

- Target journal and tier read from `project_config.yml` → `journal.name` and `journal.tier`
- Apply corresponding tier standards from `pipeline/references/journal_standards.md`
- Effect size + 95%CI required alongside p-values (Q3+ mandatory)
- Exact p-values (not just "p < 0.05")
- FDR/Bonferroni for multiple comparisons
- Software versions reported
