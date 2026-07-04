#!/usr/bin/env bash
# clinpub-phase-boundary.sh
#
# Claude Code hook that enforces phase boundary conditions.
# Checks that prerequisite milestones are complete before starting a new phase.
#
# Installed as: PreToolUse hook for Bash tool
# Trigger: When agent runs analysis commands (Rscript, python analysis scripts)
#
# Output protocol:
#   allow  → stdout: {"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"allow"}}
#   block  → stderr: {"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"block","reason":"..."}} + exit 2

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
STATE_FILE="$PROJECT_DIR/.clinpub/STATE.md"
ROADMAP_FILE="$PROJECT_DIR/.clinpub/ROADMAP.md"

# clinpub canonical project layout
RAW_DATA_DIR="01_RawData"
PREPROCESSED_DIR="02_PreprocessedData"
CLEANED_DATA="02_PreprocessedData/data/cleaned.csv"
ANALYSIS_DIR="03_AnalysisMethods"
OUTPUTS_DIR="04_Outputs"
MANUSCRIPT_FILE="05_Manuscript/manuscript.md"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

check_phase_boundary() {
  local target_phase="$1"
  local prev_phase=$((target_phase - 1))

  if [ "$prev_phase" -lt 0 ]; then
    echo -e "${GREEN}OK: Phase 0 has no prerequisite.${NC}"
    return 0
  fi

  if [ ! -f "$STATE_FILE" ]; then
    echo -e "${RED}BLOCK: .clinpub/STATE.md not found. Run '/clinpub init' first.${NC}"
    return 1
  fi

  if grep -qE "阶段：Phase\s*$prev_phase" "$STATE_FILE" 2>/dev/null; then
    echo -e "${GREEN}OK: Phase $prev_phase milestone complete.${NC}"
    return 0
  fi

  local milestone_dir="$PROJECT_DIR/.clinpub/phases/"
  if [ -d "$milestone_dir" ]; then
    local prev_milestone
    prev_milestone=$(find "$milestone_dir" -name "MILESTONE.md" -path "*$prev_phase*" 2>/dev/null | head -1)
    if [ -n "$prev_milestone" ] && grep -qi "Complete\|✅" "$prev_milestone" 2>/dev/null; then
      echo -e "${GREEN}OK: Phase $prev_phase milestone file found and complete.${NC}"
      return 0
    fi
  fi

  if [ -f "$PROJECT_DIR/pipeline/references/gates.md" ]; then
    echo -e "${YELLOW}WARNING: Phase $prev_phase milestone not confirmed.${NC}"
    echo -e "${YELLOW}Gate verification required before starting Phase $target_phase.${NC}"
  fi

  echo -e "${RED}BLOCK: Phase $prev_phase is not marked as complete in STATE.md.${NC}"
  echo -e "${RED}Complete Phase $prev_phase and get milestone signoff before proceeding.${NC}"
  return 1
}

check_data_exists() {
  local phase="$1"

  case "$phase" in
    1)
      if [ ! -d "$PROJECT_DIR/$RAW_DATA_DIR" ] || [ -z "$(ls "$PROJECT_DIR/$RAW_DATA_DIR/"*.csv 2>/dev/null)" ]; then
        echo -e "${RED}BLOCK: No raw data files found in $RAW_DATA_DIR/.${NC}"
        return 1
      fi
      ;;
    2)
      if [ ! -f "$PROJECT_DIR/$CLEANED_DATA" ]; then
        echo -e "${RED}BLOCK: $CLEANED_DATA not found. Complete Phase 1 data preparation first.${NC}"
        return 1
      fi
      ;;
    3)
      if [ ! -d "$PROJECT_DIR/$OUTPUTS_DIR" ] || [ -z "$(ls "$PROJECT_DIR/$OUTPUTS_DIR/" 2>/dev/null)" ]; then
        echo -e "${RED}BLOCK: No analysis outputs found in $OUTPUTS_DIR/. Complete Phase 2 first.${NC}"
        return 1
      fi
      ;;
    4)
      if [ ! -f "$PROJECT_DIR/$MANUSCRIPT_FILE" ]; then
        echo -e "${RED}BLOCK: $MANUSCRIPT_FILE not found. Complete Phase 3 writing first.${NC}"
        return 1
      fi
      ;;
  esac

  return 0
}

main() {
  local input
  input=$(cat)

  local command
  command=$(echo "$input" | grep -o '"command":"[^"]*"' | head -1 | cut -d'"' -f4 2>/dev/null || echo "")

  if [ -z "$command" ]; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"allow"}}'
    exit 0
  fi

  # Import mode bypass with crash-safety validation
  if [ -f "$STATE_FILE" ] && grep -q "import_mode:.*true" "$STATE_FILE" 2>/dev/null; then
    # Only bypass if STATE.md has full structure (not crash residue)
    if grep -qE "阶段：Phase\s*[0-9]+" "$STATE_FILE" 2>/dev/null; then
      echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"allow"}}'
      exit 0
    fi
    # Crash residue: fall through to normal phase boundary checks
  fi

  local target_phase=-1

  if echo "$command" | grep -qi "Rscript.*analysis\|python.*analysis\|$ANALYSIS_DIR\|$OUTPUTS_DIR"; then
    target_phase=2
  elif echo "$command" | grep -qi "data_prep\|preprocess\|clean.*data\|$PREPROCESSED_DIR"; then
    target_phase=1
  elif echo "$command" | grep -qi "manuscript\|writing\|05_Manuscript"; then
    target_phase=3
  elif echo "$command" | grep -qi "review\|final"; then
    target_phase=4
  fi

  if [ "$target_phase" -lt 0 ]; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"allow"}}'
    exit 0
  fi

  if ! check_phase_boundary "$target_phase" >/dev/null 2>&1; then
    local reason
    reason=$(check_phase_boundary "$target_phase" 2>&1 | grep "BLOCK:" | head -1)
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"decision\":\"block\",\"reason\":\"$reason\"}}" >&2
    exit 2
  fi

  if ! check_data_exists "$target_phase" >/dev/null 2>&1; then
    local reason
    reason=$(check_data_exists "$target_phase" 2>&1 | grep "BLOCK:" | head -1)
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"decision\":\"block\",\"reason\":\"$reason\"}}" >&2
    exit 2
  fi

  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","decision":"allow"}}'
}

main
