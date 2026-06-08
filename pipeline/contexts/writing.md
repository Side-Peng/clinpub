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

1. Methods (most structured, write first)
2. Results (data-driven, write after methods)
3. Introduction (funnel structure, write after results are clear)
4. Discussion (narrative, write after introduction)
5. Abstract (structured, write last)

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
