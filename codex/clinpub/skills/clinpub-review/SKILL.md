---
name: clinpub-review
description: "Phase 4: Simulated peer review and revision. Generate mock peer review, confirm revision items with user, revise manuscript, generate response letter. Loops until satisfactory."
---

# ClinPub Review

Phase 4: Peer review simulation and manuscript revision. Simulate rigorous peer review at target journal level, then iteratively revise.

Review covers: statistical methods, sample size, confounding, result interpretation, language, citations, figures.

## Execution Context

- Workflow: `pipeline/workflows/review.md`

## Process

Execute the review workflow from `pipeline/workflows/review.md` end-to-end.

## Success Criteria

- Review comments generated (categorized: Major/Minor)
- Each comment addressed in revision
- Changes reflected in manuscript
- Response letter written (point-by-point)
- Final manuscript in final/ directory when user satisfied
