---
name: overview
description: "Clinical data analysis and publication pipeline command reference. Lists the core phase commands plus standalone tools. Each phase must be invoked individually to ensure rigor. Adapts to any clinical research article type."
argument-hint: ""
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
Clinical data analysis and publication pipeline command reference. You are a senior medical statistician + academic writing consultant.

**This is a reference overview only — each phase must be invoked individually as a separate command.** There is no "one-click execute all phases" mode. Clinical research requires deliberate, phase-by-phase execution with user review at each stage.
</objective>

<process>
## Core Pipeline (Phase 0-3)

Each phase is an independent command. Invoke them one at a time. Between phases, review deliverables and user sign-off before proceeding. Writing (Phase 3) completes the core pipeline.

| # | Command | Purpose | Key Output |
|---|---------|---------|------------|
| 0 | `/clinpub:initialize` | Discuss research framework + ask target journal → project config + directory structure | `project_config.yml` |
| 1 | `/clinpub:data-prep` | Data cleaning → EDA → quality report | `cleaned.csv` |
| 2 | `/clinpub:analysis` | Wave-based statistical analysis → figures + tables | `04_Outputs/` |
| 3 | `/clinpub:writing` | Literature search → IMRAD manuscript drafting | `manuscript.md` |

## Standalone Tools (no phase number — invocable anytime the prerequisite exists)

| Command | Purpose | Key Output |
|---------|---------|------------|
| `/clinpub:improving` | Self-review the draft → revision plan → directly revise text + analysis (repeatable) | updated `manuscript.md` |
| `/clinpub:coverletter` | Gather target-journal submission requirements → tailored cover letter | `cover_letter.md` |
| `/clinpub:review` | Post-submission: intake real reviewer comments → response letter → delegate revision to improving | `final/` |
| `/clinpub:modify` | Adjust completed analysis outputs (figure style, method, variables) | updated `04_Outputs/` |
| `/clinpub:data2idea <file>` | Topic mining: paper ideas from data without full analysis | idea report |
| `/clinpub:milestone <N>` | Phase gate: verify status, re-run verification, user sign-off | `MILESTONE.md` |

## Usage

```
# Always start with Phase 0
/clinpub:initialize

# After Phase 0 completes and user signs off, proceed one phase at a time
/clinpub:data-prep
/clinpub:analysis
/clinpub:writing

# After the manuscript is drafted, use standalone tools as needed:
/clinpub:improving      # continuously improve the draft (self-review + revise)
/clinpub:coverletter    # prepare the submission cover letter for the target journal
/clinpub:review         # after submission, handle real reviewer comments
```

**Do NOT attempt to execute all phases in a single command.** Each phase requires user review of its outputs before proceeding.
</process>

<success_criteria>
- User understands that phases are independent commands, not auto-executed
- Each phase is invoked individually with user sign-off between phases
- Project directory structure follows standard layout
- All outputs meet publication-grade standards (target journal level)
</success_criteria>
