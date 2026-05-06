<!-- refreshed: 2026-05-05 -->
# Architecture

**Analysis Date:** 2026-05-05

## System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    USER  (Claude Code Chat)                           │
│  Input: /clinpub, /clinpub-data2idea <file>, /clinpub-milestone <N> │
└──────────────────────┬───────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────────────┐
│        LAYER 1: COMMANDS  (commands/clinpub/*.md)                    │
│  Thin entry points with frontmatter (name, description, allowed-     │
│  tools). Each maps to a pipeline workflow. 8 commands total.         │
│                                                                      │
│  /clinpub  /clinpub-init-project  /clinpub-data-prep                 │
│  /clinpub-analysis  /clinpub-writing  /clinpub-review                │
│  /clinpub-milestone  /clinpub-data2idea                              │
└──────────────────────┬───────────────────────────────────────────────┘
                       │  @-references to workflows
                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│        LAYER 2: WORKFLOWS  (pipeline/workflows/*.md)                 │
│  Phase orchestration logic. Each workflow defines steps in the       │
│  DISCUSS → PLAN → EXECUTE → VERIFY cycle.                           │
│                                                                      │
│  init-project.md  data-prep.md  analysis.md                          │
│  writing.md  review.md  data2idea.md  milestone.md                   │
└──────────┬──────────────┬──────────────┬─────────────────────────────┘
           │              │              │
           ▼              ▼              ▼
┌──────────────────────────────────────────────────────────────────────┐
│        LAYER 3: AGENTS  (agents/*.md)                                │
│  7 specialized AI agent role contracts. Each has defined inputs,     │
│  outputs, scope, and completion markers.                             │
│                                                                      │
│  analyst-agent  reference-agent  writer-agent  topic-miner-agent     │
│  clinpub-planner  clinpub-executor  clinpub-verifier                 │
└──────┬──────────────────┬──────────────────┬─────────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│        SUPPORT LAYER: SCRIPTS + HOOKS + REFERENCES + TEMPLATES       │
│                                                                      │
│  scripts/*.py      — Tool scripts (data profiling, search, PDF)      │
│  hooks/*.js/*.sh   — PreToolUse hooks (phase guard, boundary,        │
│                      prompt injection detection)                     │
│  pipeline/references/ — Standards, methods, gates, patterns          │
│  pipeline/templates/ — Project config, study types, milestones       │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| clinpub (main command) | Full 5-phase pipeline entry | `commands/clinpub/clinpub.md` |
| init-project command | Phase 0 entry: project init | `commands/clinpub/init-project.md` |
| data-prep command | Phase 1 entry: data cleaning | `commands/clinpub/data-prep.md` |
| analysis command | Phase 2 entry: statistical analysis | `commands/clinpub/analysis.md` |
| writing command | Phase 3 entry: manuscript writing | `commands/clinpub/writing.md` |
| review command | Phase 4 entry: peer review | `commands/clinpub/review.md` |
| milestone command | Phase gate review | `commands/clinpub/milestone.md` |
| data2idea command | Topic mining (standalone) | `commands/clinpub/data2idea.md` |
| init-project workflow | Phase 0 orchestration | `pipeline/workflows/init-project.md` |
| data-prep workflow | Phase 1 orchestration | `pipeline/workflows/data-prep.md` |
| analysis workflow | Phase 2 orchestration | `pipeline/workflows/analysis.md` |
| writing workflow | Phase 3 orchestration | `pipeline/workflows/writing.md` |
| review workflow | Phase 4 orchestration | `pipeline/workflows/review.md` |
| milestone workflow | Phase gate verification | `pipeline/workflows/milestone.md` |
| data2idea workflow | Topic mining orchestration | `pipeline/workflows/data2idea.md` |
| Analyst Agent | R/Python data analysis | `agents/analyst-agent.md` |
| Reference Agent | PubMed literature search | `agents/reference-agent.md` |
| Writer Agent | IMRAD manuscript drafting | `agents/writer-agent.md` |
| Topic Miner Agent | Data-driven topic discovery | `agents/topic-miner-agent.md` |
| Clinpub Planner | Analysis PLAN.md creation | `agents/clinpub-planner.md` |
| Clinpub Executor | Analysis execution (atomic commits) | `agents/clinpub-executor.md` |
| Clinpub Verifier | Cross-phase verification | `agents/clinpub-verifier.md` |
| Agent contracts | 7 agent contract definitions | `pipeline/references/agent-contracts.md` |
| Quality gates | 4 phase boundary gates | `pipeline/references/gates.md` |
| Analysis methods | Statistical method reference library | `pipeline/references/analysis_methods.md` |
| R patterns | R visualization core standards | `pipeline/references/r_patterns.md` |
| Verification patterns | 15 verification patterns | `pipeline/references/verification-patterns.md` |
| Journal standards | SCI Q1/Q2 publication standards | `pipeline/references/journal_standards.md` |
| Checkpoint protocol | Checkpoint/milestone protocol | `pipeline/references/checkpoints.md` |
| Manifest format | Agent handoff manifest spec | `pipeline/references/manifest-format.md` |
| Mandatory initial read | Agent context loading protocol | `pipeline/references/mandatory-initial-read.md` |
| Workflow guard hook | Phase ordering enforcement | `hooks/clinpub-workflow-guard.js` |
| Phase boundary hook | Prerequisite milestone check | `hooks/clinpub-phase-boundary.sh` |
| Prompt guard hook | Prompt injection detection | `hooks/clinpub-prompt-guard.js` |
| Install script | npm CLI installer | `bin/install.js` |
| Data profiler | Variable profiling tool | `scripts/data_profiler.py` |
| NCBI search | PubMed/NCBI API client | `scripts/ncbi_search.py`, `scripts/ncbi_client.py` |
| PubMed search | PubMed search wrapper | `scripts/pubmed_search.py` |
| Tavily search | Web search tool | `scripts/tavily_search.py` |

## Pattern Overview

**Overall:** Layered pipeline architecture with phase-gate governance.

**Key Characteristics:**
- **Three explicit layers**: Commands (entry) → Workflows (orchestration) → Agents (execution)
- **Phase-gate progression**: 5 sequential phases with mandatory milestone reviews between each
- **DISCUSS → PLAN → EXECUTE → VERIFY lifecycle**: Every phase follows this four-step cycle
- **Filesystem-only agent communication**: Agents never message each other directly; all handoffs go through file manifests
- **Contract-driven agents**: Each agent has a formal contract defining scope, inputs, outputs, and completion markers
- **Hook-enforced governance**: 3 PreToolUse hooks enforce phase ordering, boundary conditions, and security
- **Adaptive analysis planning**: Phase 2 dynamically builds analysis plans based on data diagnosis, not from a fixed menu

## Layers

### Layer 1: Commands (`commands/clinpub/`)

- Purpose: Thin user-facing entry points (slash commands)
- Location: `commands/clinpub/*.md`
- Contains: 8 Markdown files with YAML frontmatter (name, description, allowed-tools)
- Depends on: Pipeline workflows via `@./pipeline/workflows/` references
- Used by: Claude Code runtime (invoked via `/clinpub-xxx` commands)

**Command-to-workflow mapping:**

| Command | Runtime Name | Workflow |
|---------|--------------|----------|
| `clinpub.md` | `/clinpub` | Loads all 5 workflows sequentially |
| `init-project.md` | `/clinpub-init-project` | `pipeline/workflows/init-project.md` |
| `data-prep.md` | `/clinpub-data-prep` | `pipeline/workflows/data-prep.md` |
| `analysis.md` | `/clinpub-analysis` | `pipeline/workflows/analysis.md` |
| `writing.md` | `/clinpub-writing` | `pipeline/workflows/writing.md` |
| `review.md` | `/clinpub-review` | `pipeline/workflows/review.md` |
| `milestone.md` | `/clinpub-milestone <N>` | `pipeline/workflows/milestone.md` |
| `data2idea.md` | `/clinpub-data2idea <file>` | `pipeline/workflows/data2idea.md` |

### Layer 2: Workflows (`pipeline/workflows/`)

- Purpose: Phase orchestration logic defining step-by-step execution
- Location: `pipeline/workflows/*.md`
- Contains: 7 workflow files, each with `<process>` blocks containing numbered `<step>` elements
- Depends on: Agent files (via `@./agents/`), reference documents, scripts
- Used by: Commands layer

**Workflow step pattern (every workflow follows this order):**
1. `discuss_*` — User discussion/decision point
2. `create` / `execute` / `draft` — Main execution
3. `verify` / `validate` — Output verification
4. `checkpoint_confirm` — User verification checkpoint
5. `milestone` — Phase gate review (delegates to `pipeline/workflows/milestone.md`)

### Layer 3: Agents (`agents/`)

- Purpose: Specialized AI agent role contracts, each with defined scope
- Location: `agents/*.md`
- Contains: 7 agent documents
- Key pattern: Filesystem-only communication via `MANIFEST.yaml` handoffs

**Agent contracts are defined in `pipeline/references/agent-contracts.md` with:**
- Role, scope, inputs, outputs, communication rules, completion markers
- Cross-agent read/write matrix (which directories each agent can read/write)
- Strict rules: single writer per directory, no circular dependencies, shared read/exclusive write

### Support Layer

**Scripts (`scripts/`):**
- Purpose: Executable Python tools for data profiling, literature search, PDF reading
- Used by: Topic Miner Agent, Reference Agent
- Key tools: `data_profiler.py`, `ncbi_search.py`, `pubmed_search.py`, `tavily_search.py`

**Hooks (`hooks/`):**
- Purpose: PreToolUse hooks that enforce pipeline governance
- 3 hooks registered in `.claude/settings.json`:
  - `clinpub-workflow-guard.js` — Blocks Write/Edit to directories outside current phase
  - `clinpub-phase-boundary.sh` — Blocks Bash commands that violate phase ordering
  - `clinpub-prompt-guard.js` — Scans data files for prompt injection

**References (`pipeline/references/`):**
- 9 reference documents providing domain knowledge and standards
- Key: `analysis_methods.md` (statistical method decision tree), `gates.md` (4 quality gates), `verification-patterns.md` (15 patterns), `agent-contracts.md` (7 contracts)

**Templates (`pipeline/templates/`):**
- 10 template files + 5 study type templates
- Templates for: project config, milestone, validation, spec, UAT, verification report, context, idea report
- Study type templates: RCT, cohort, case-control, cross-sectional, descriptive

### Installer (`bin/install.js`)

- Purpose: npm-installable CLI that converts commands to Claude Code skills
- Key mechanism: Rewrites `@./` references to installed resource directory path
- Environment checks: Node.js >= 22, R, Python, Claude Code >= 2.1.88
- Registers 3 hooks in `.claude/settings.json`

## Data Flow

### Primary Request Path (Full Pipeline)

1. User invokes `/clinpub` in Claude Code chat (`commands/clinpub/clinpub.md`)
2. Command loads all 5 workflow files via `@./pipeline/workflows/` references
3. Workflow begins Phase 0: init-project (`pipeline/workflows/init-project.md`)
4. Each workflow step executes: discuss → create → verify → checkpoint → milestone
5. Phase transitions require milestone sign-off (`pipeline/workflows/milestone.md`)
6. Agents are invoked as sub-agents when specialized tasks are needed (analysis, writing, verification)

### Topic Mining Flow (data2idea)

1. User invokes `/clinpub-data2idea <filepath>` (`commands/clinpub/data2idea.md`)
2. Topic Miner Agent profiles data (`agents/topic-miner-agent.md`)
3. Python script `scripts/data_profiler.py` generates data profile
4. PubMed literature search via `scripts/ncbi_search.py` or `scripts/pubmed_search.py`
5. 3-5 candidate topics generated with feasibility scores
6. User selects topic → generates `idea/to_project_config.yml`

### Agent-to-Agent Handoff Flow

1. Producing agent writes output files + `MANIFEST.yaml` in output directory
2. Producing agent's manifest declares downstream consumers
3. Consuming agent reads manifest, validates required files exist
4. Consuming agent verifies quality conditions from manifest
5. If conditions pass, consuming agent begins its work
6. If conditions fail, consuming agent reports failure and does NOT proceed

### Phase 2 Adaptive Analysis Flow

1. Load `02_PreprocessedData/data/cleaned.csv`, diagnose data structure
2. Build adaptive analysis proposal based on data characteristics (groups, timepoints, outcome type)
3. Discuss proposal with user, get confirmation on methods
4. Organize methods into dependency-ordered waves (waves = 1 to N, not fixed)
5. Execute wave by wave, user confirms after each wave
6. Each method outputs: figure(s) + table(s) + README.md
7. All outputs go to `04_Outputs/XX_MethodName/`
8. Final verification before Phase 2 milestone

**State Management:**
- Project state tracked in `project_config.yml` and `.planning/STATE.md`
- `.planning/STATE.md` tracks: current_phase, completed milestones, pending decisions, blockers
- `.planning/ROADMAP.md` tracks: all phases with status (Complete/In Progress/Not Started)
- Each phase has its own context log in `.planning/phases/NN-phase-name/00-CONTEXT.md`
- Phase gate completions recorded in `.planning/phases/NN-phase-name/MILESTONE.md`

## Key Abstractions

**Agent Contract:**
- Purpose: Defines role boundaries, inputs, outputs, and completion markers for each agent
- Examples: `pipeline/references/agent-contracts.md` (all 7 contracts in one file)
- Pattern: Contract-based delegation with filesystem-only communication

**MANIFEST.yaml Handoff:**
- Purpose: Lightweight contract between producing and consuming agents
- Examples: All agents write `MANIFEST.yaml` after completing outputs
- Pattern: Filesystem-based type checking — manifest declares expected files and quality conditions

**Phase Gate (Milestone):**
- Purpose: Formal phase transition control with verification and user sign-off
- Examples: `pipeline/workflows/milestone.md`, `pipeline/references/gates.md`
- Pattern: Verify success criteria → collect decisions → generate MILESTONE.md → update STATE.md/ROADMAP.md → user sign-off

**Adaptive Analysis Wave:**
- Purpose: Dynamically built analysis plan based on data diagnosis, organized in dependency waves
- Examples: `pipeline/workflows/analysis.md` Step 2-3, `pipeline/references/analysis_methods.md` Section 2
- Pattern: Data diagnosis → method proposal → user confirmation → wave execution → inter-wave checkpoints

**DISCUSS → PLAN → EXECUTE → VERIFY Cycle:**
- Purpose: Per-phase lifecycle ensuring user involvement at key decision points
- Examples: Every workflow follows this pattern implicitly
- Pattern: Discuss with user first → create execution plan → execute → verify outputs → milestone

## Entry Points

**Main Pipeline:** `/clinpub` command
- Location: `commands/clinpub/clinpub.md`
- Triggers: User types `/clinpub` in Claude Code
- Responsibilities: Load all 5 phase workflows, guide user from Phase 0 through Phase 4

**Topic Mining:** `/clinpub-data2idea <filepath>` command
- Location: `commands/clinpub/data2idea.md`
- Triggers: User has raw data and wants paper topic ideas
- Responsibilities: Profile data, search literature, generate candidate topics

**Milestone Review:** `/clinpub-milestone <N>` command
- Location: `commands/clinpub/milestone.md`
- Triggers: Manual milestone re-run or status check
- Responsibilities: Verify phase completion, record decisions, gate progression

**npm Installer:** `npx clinpub-cc`
- Location: `bin/install.js`
- Triggers: User installs clinpub via npm
- Responsibilities: Convert commands to skills, copy resources, register hooks

## Architectural Constraints

- **Sequential phases**: Phases must execute in order (0→1→2→3→4). Hook-enforced: Write/Edit to Phase N directory is blocked if current phase < N.
- **Filesystem-only communication**: Agents never message each other directly. All handoffs go through `MANIFEST.yaml` + output files.
- **Single writer per directory**: Each output directory has exactly one author agent. No two agents write to the same directory.
- **No circular dependencies**: Agent A reads from Agent B's output, never vice versa. Read/write matrix in `agent-contracts.md` enforces this.
- **Gate blocking**: Four quality gates cannot be bypassed (except Gate 1 IRB which has no override). Failed gates block next phase.
- **Manifest validation**: Downstream agents must validate MANIFEST.yaml before consuming outputs. Missing or failed conditions block processing.
- **Threading**: Not applicable (prompt-based pipeline, not concurrent execution).
- **Global state**: `.planning/STATE.md` and `.planning/ROADMAP.md` act as shared state. Only orchestrator (not agents) updates these files.
- **Circular imports**: Not applicable to Markdown-based architecture.

## Anti-Patterns

### Agent Contract Duplication (Low Risk)

**What happens:** Agent role definitions exist in two places: individual `agents/*.md` files AND `pipeline/references/agent-contracts.md`. Some details may diverge over time.
**Why it's wrong:** Dual sources of truth can become inconsistent.
**Do this instead:** Consider consolidating all contract details into `agent-contracts.md` and having individual agent files reference it via `@`-link.

### Hook Logic in Install Script (Medium Risk)

**What happens:** The hook registration logic in `bin/install.js` (lines 149-211) duplicates knowledge about hook file paths and matchers. If hooks are added/removed, both the hook file and the installer must be updated.
**Why it's wrong:** Hard-coded hook definition arrays in the installer lead to drift.
**Do this instead:** Consider a hook manifest file that the installer reads dynamically.

## Error Handling

**Strategy:** Defensive blocking rather than error recovery. Hooks block operations before they can fail. Agents report missing preconditions and stop.

**Patterns:**
- **Hook-level blocking**: Workflow guard blocks writes to wrong phase directory; phase boundary blocks commands when prerequisite milestone missing
- **Checkpoint verification**: User confirms at key points before proceeding
- **Manifest validation**: Downstream agents validate input manifests before consuming
- **Gate enforcement**: Failed quality gates block phase transitions
- **No automatic error recovery**: If preconditions fail, agent reports to user and stops

## Cross-Cutting Concerns

**Logging:** Not formalized. Phase context logs are written to `.planning/phases/NN-phase-name/00-CONTEXT.md`. No centralized logging framework.

**Validation:** Two-tier:
1. Hook-level (automated, PreToolUse): phase ordering, file access, prompt injection
2. Workflow-level (manual, checkpoint): user verification of outputs
3. Gate-level (structured): 4 quality gates with explicit pass/fail criteria per gate

**Authentication:** Not applicable (this is a pipeline framework, not a service). External API keys (`NCBI_API_KEY`, `TAVILY_API_KEY`) are read from environment.

---

*Architecture analysis: 2026-05-05*
