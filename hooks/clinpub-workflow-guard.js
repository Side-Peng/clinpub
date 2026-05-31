/**
 * clinpub-workflow-guard.js
 *
 * Claude Code hook that enforces analysis workflow stage ordering.
 * Blocks actions that skip required pipeline phases.
 *
 * Installed as: PreToolUse hook for Write/Edit/Bash tools
 * Trigger: When agent attempts file operations that violate phase ordering
 */

const fs = require("fs");
const path = require("path");

const PROJECT_DIR = process.env.PROJECT_DIR || process.cwd();

// clinpub canonical project directory layout per phase
const PHASE_MAP = {
  0: { name: "init", allowed_dirs: [".clinpub", "project_config.yml"] },
  1: { name: "data-prep", allowed_dirs: ["01_RawData", "02_PreprocessedData"] },
  2: { name: "analysis", allowed_dirs: ["03_AnalysisMethods", "04_Outputs"] },
  3: { name: "writing", allowed_dirs: ["05_Manuscript", "Reference"] },
  4: { name: "review", allowed_dirs: ["05_Manuscript/final"] },
};

function getCurrentPhase() {
  const statePath = path.join(PROJECT_DIR, ".clinpub", "STATE.md");
  if (!fs.existsSync(statePath)) return -1;

  const content = fs.readFileSync(statePath, "utf-8");
  // D-02: Authoritative source — match structured line only
  const phaseMatch = content.match(/阶段：Phase\s*(\d)/);
  if (phaseMatch) return parseInt(phaseMatch[1], 10);

  // D-04: Legacy fallback — kept for backward compatibility.
  //       New code path above handles the structured line match.
  const completedMatches = content.match(/✅/g);
  return completedMatches ? completedMatches.length : 0;
}

function getTargetDir(filePath) {
  const relative = path.relative(PROJECT_DIR, filePath).replace(/\\/g, "/");
  return relative.split("/")[0];
}

function validatePhaseAccess(currentPhase, targetDir) {
  // Allow always-accessible directories
  const alwaysAllowed = [
    ".clinpub",
    "scripts",
    "hooks",
    "pipeline",
    "agents",
    "commands",
    ".gitignore",
    "CHANGELOG.md",
    "package.json",
    "CLAUDE.md",
    "README.md",
  ];

  if (alwaysAllowed.includes(targetDir)) return { allowed: true };

  // Check which phase owns this directory
  for (const [phaseNum, phaseConfig] of Object.entries(PHASE_MAP)) {
    if (phaseConfig.allowed_dirs.some((d) => targetDir.startsWith(d))) {
      if (parseInt(phaseNum, 10) > currentPhase) {
        return {
          allowed: false,
          reason: `Directory '${targetDir}' belongs to Phase ${phaseNum} (${phaseConfig.name}), but project is currently in Phase ${currentPhase}. Complete Phase ${currentPhase} first.`,
        };
      }
      break;
    }
  }

  return { allowed: true };
}

/**
 * Hook entry point.
 * Input (stdin JSON): { tool_name, tool_input }
 * Output (stdout JSON): { hookSpecificOutput: { hookEventName, decision, reason } } | stderr JSON + exit 2 on block
 */
function main() {
  let input = "";
  process.stdin.setEncoding("utf-8");
  process.stdin.on("data", (chunk) => (input += chunk));
  process.stdin.on("end", () => {
    try {
      const { tool_name, tool_input } = JSON.parse(input);

      // Only guard file write operations
      if (!["Write", "Edit"].includes(tool_name)) {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      const filePath = tool_input.file_path;
      if (!filePath) {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      const currentPhase = getCurrentPhase();
      if (currentPhase < 0) {
        // No state file — allow (project may not be initialized)
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      const targetDir = getTargetDir(filePath);
      const result = validatePhaseAccess(currentPhase, targetDir);

      if (!result.allowed) {
        process.stderr.write(JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "PreToolUse",
            decision: "block",
            reason: result.reason
          }
        }) + '\n');
        process.exit(2);
      } else {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
      }
    } catch (e) {
      // On parse error, allow (don't break workflow)
      console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
    }
  });
}

main();
