# MANIFEST.yaml Format

> Each agent writes MANIFEST.yaml after completing its output. Downstream agents read it to validate that expected artifacts exist before consuming them.

## Purpose

Filesystem-only handoffs have no type checking. The manifest provides a lightweight contract: "I wrote these files, with these properties, for these consumers." If the manifest says a file has `statistics: [effect_size, ci_95, p_value]` but the actual README is missing effect sizes, the downstream agent catches it at handoff time, not at submission time.

## Schema

Every MANIFEST.yaml follows this structure:

```yaml
# Required — identifies the producer
agent: <agent-name>
phase: <phase-number>

# Required — what type of work was done
type: <work-type>

# Required — what was produced
outputs:
  - directory: <relative-path>
    files:
      - name: <filename>
        format: <file-format>    # csv, docx, png, bib, md, html, etc.
      - name: <filename>
        format: <file-format>
        statistics: [<list of reported stats>]  # for analysis outputs

# Required — handoff targets
handoffs:
  - consumer: <consumer-agent-name>
    required_files:
      - <relative-path-to-file>
    required_quality:  # optional — conditions that must be true
      - "<condition description>"

# Optional — decisions the agent made that affect interpretation
decisions:
  - variable: <variable-name>
    decision: "<what was decided>"
    rationale: "<why>"

# Optional — producer's own notes for downstream
notes: "<free text>"
```

## Per-Agent Templates

### Analyst Agent — Data Preparation

```yaml
agent: analyst-agent
phase: 1
type: data_preparation
outputs:
  - directory: 02_PreprocessedData/data/
    files:
      - name: cleaned.csv
        format: csv
  - directory: 02_PreprocessedData/reports/
    files:
      - name: data_quality.html
        format: html
handoffs:
  - consumer: analyst-agent (Phase 2)
    required_files:
      - 02_PreprocessedData/data/cleaned.csv
```

### Analyst Agent — Statistical Analysis

```yaml
agent: analyst-agent
phase: 2
type: statistical_analysis
methods:
  - id: "01_BaselineTable"
    type: baseline
    outputs:
      - 04_Outputs/01_BaselineTable/Table1.docx
      - 04_Outputs/01_BaselineTable/Table1.xlsx
    statistics: [n, mean, sd, p_value]
  - id: "02_TwoGroupComparison"
    type: comparison
    outputs:
      - 04_Outputs/02_TwoGroupComparison/boxplot_HAMA.png
      - 04_Outputs/02_TwoGroupComparison/comparison_table.xlsx
    statistics: [effect_size, ci_95, p_value]
handoffs:
  - consumer: writer-agent
    required_files:
      - 04_Outputs/01_BaselineTable/Table1.docx
      - 04_Outputs/02_TwoGroupComparison/boxplot_HAMA.png
decisions:
  - variable: HAMA_total
    decision: "analyzed at baseline only"
    rationale: "follow-up missing rate > 40%"
```

### Reference Agent — Literature Search

```yaml
agent: reference-agent
phase: 3
type: literature_search
outputs:
  - directory: Reference/
    files:
      - name: references.bib
        format: bib
      - name: citation_map.md
        format: md
handoffs:
  - consumer: writer-agent
    required_files:
      - Reference/references.bib
      - Reference/citation_map.md
    required_quality:
      - "all entries have DOIs"
      - ">= 20 references"
```

### Writer Agent — Manuscript

```yaml
agent: writer-agent
phase: 3
type: manuscript
outputs:
  - directory: 05_Manuscript/
    files:
      - name: manuscript.md
        format: md
      - name: abstract.md
        format: md
    notes: "Humanizer review passed"
handoffs:
  - consumer: clinpub-verifier
    required_files:
      - 05_Manuscript/manuscript.md
      - 05_Manuscript/abstract.md
    required_quality:
      - "all citations have DOIs"
      - "IMRAD structure complete"
```

## Validation Protocol

### On Write (Producer Side)

The producing agent MUST:
1. Write all output files completely
2. Write MANIFEST.yaml in the same directory as the primary output
3. Include every file listed in `outputs`
4. List all downstream consumers in `handoffs`

### On Read (Consumer Side)

The consuming agent MUST, before starting its own work:

```python
# Pseudocode
manifest = read_yaml("04_Outputs/MANIFEST.yaml")

# Step 1: Check all required files exist
for handoff in manifest.handoffs:
    if handoff.consumer == "my-agent-name":
        for filepath in handoff.required_files:
            assert file_exists(filepath), f"Missing: {filepath}"

# Step 2: Check quality conditions
for condition in handoff.required_quality:
    assert check_condition(condition), f"Quality fail: {condition}"

# Step 3: Log what was found and proceed
print(f"Manifest OK: {len(manifest.outputs)} output groups from {manifest.agent}")
```

### On Failure

If a required file is missing or a quality condition fails:
1. Report the specific failure to the user
2. Do NOT proceed with downstream work
3. The producing agent must fix the gap and re-run
