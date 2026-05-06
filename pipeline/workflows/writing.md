---
name: writing
description: "Phase 3 orchestration: Reference Agent performs literature search, Writer Agent drafts IMRAD manuscript following study type template. Chapter-by-chapter writing with supplementary search between chapters."
---

<purpose>
Draft a complete IMRAD manuscript in Chinese (English figures/tables) targeting SCI Q1/Q2 journals. Two-agent workflow: Reference Agent conducts literature search, Writer Agent writes following the appropriate study type template.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
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

<step name="draft_imrad_chapters" priority="high">
Write manuscript chapters in order. Each chapter follows the appropriate study type template:

**Wave 1 — Methods** (write first, most structured):
- Read study type template from `pipeline/templates/study_types/`
- Follow STROBE/CONSORT as applicable
- Report software versions and statistical methods clearly

**Wave 2 — Results** (write second):
- Lead with primary finding, follow with secondary analyses
- Each result paragraph references specific figures/tables
- Report effect size + 95%CI + exact p-value
- Natural narrative, not "As shown in Table X"

**Wave 3 — Introduction** (write third, after results are clear):
- Funnel structure: background → known evidence → gap → objective
- Integrate citations from Reference Agent's work

**Wave 4 — Discussion** (write fourth):
- Summary → comparison → mechanisms → clinical implications → limitations → conclusion
- Specific future directions, not "more research needed"

**Wave 5 — Abstract + Title** (write last):
- Structured: Background → Methods → Results → Conclusions
- Keywords: 3-6 terms

Each chapter: write → supplementary search → integrate → next chapter.
</step>

<step name="humanizer_review" priority="medium">
After complete draft, apply Humanizer self-check to each chapter:

| Check | AI Pattern | Fix |
|-------|-----------|-----|
| Paragraph openings | Sequential markers | Content-driven progression |
| Transition words | Repeated formulaic | Specific logical connectors |
| Sentence structure | Uniform patterns | Varied sentence types |
| Conclusions | Hollow or generic | Specific future direction |
| Citations | Impersonal | Author-contextualized |
| Explanations | Over-explaining methods | Just state, don't justify |

Revise any flagged passages.
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

If manifest is missing, write it here.
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
</success_criteria>
