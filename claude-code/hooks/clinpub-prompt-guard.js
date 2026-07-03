/**
 * clinpub-prompt-guard.js
 *
 * Claude Code hook that detects prompt injection attempts in data files.
 * Scans data file contents for suspicious patterns before they enter context.
 *
 * Installed as: PreToolUse hook for Read tool
 * Trigger: When agent reads CSV/XLSX/data files that could contain injected prompts
 */

const fs = require("fs");
const path = require("path");

// Patterns that indicate prompt injection in data files
const INJECTION_PATTERNS = [
  // Direct instruction injection
  /\b(ignore|forget|disregard)\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)\b/i,
  /\byou\s+are\s+now\b/i,
  /\bnew\s+instructions?\b.*:/i,
  /\bsystem\s*:\s*/i,
  /\bassistant\s*:\s*/i,
  /\bhuman\s*:\s*/i,
  /\b<\|im_start\|>\b/,
  /\b<\|im_end\|>\b/,
  /\b<\|endoftext\|>\b/,
  /\[INST\]/i,
  /\[\/INST\]/i,
  /\bact\s+as\s+(?:a\s+)?(?:different|new)\b/i,

  // XML/HTML injection that mimics system tags
  /<role>/i,
  /<\/role>/i,
  /<system>/i,
  /<\/system>/i,
  /<instructions?>/i,
  /<\/instructions?>/i,

  // Suspiciously long strings in CSV columns (>500 chars that look like prose)
  // This is a heuristic — real clinical data rarely has prose longer than 500 chars

  // Base64 encoded payloads (long strings of alphanumeric + /+= )
  /^[A-Za-z0-9+/=]{200,}$/,

  // Unicode homoglyph injection (invisible/special characters)
  /[​-‍﻿⁠-⁤]/,
];

// Data file extensions to scan
const DATA_EXTENSIONS = [".csv", ".tsv", ".xlsx", ".xls", ".txt"];

/**
 * Scan file content for injection patterns.
 * Returns list of detected patterns (empty = safe).
 */
function scanContent(content) {
  const findings = [];
  const lines = content.split("\n");

  for (let lineIdx = 0; lineIdx < lines.length; lineIdx++) {
    const line = lines[lineIdx];

    // Skip empty lines
    if (!line.trim()) continue;

    // Check each pattern
    for (const pattern of INJECTION_PATTERNS) {
      if (pattern.test(line)) {
        findings.push({
          line: lineIdx + 1,
          pattern: pattern.toString(),
          excerpt: line.substring(0, 100),
        });
      }
    }

    // Check for suspiciously long cell values in CSV
    if (line.includes(",")) {
      const cells = line.split(",");
      for (const cell of cells) {
        const trimmed = cell.trim();
        if (trimmed.length > 500 && /[a-zA-Z]/.test(trimmed)) {
          findings.push({
            line: lineIdx + 1,
            pattern: "suspiciously_long_cell",
            excerpt: trimmed.substring(0, 100) + "...",
          });
        }
      }
    }
  }

  return findings;
}

/**
 * Check if file path points to a data file that should be scanned.
 */
function isDataFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return DATA_EXTENSIONS.includes(ext);
}

/**
 * Hook entry point.
 * Input (stdin JSON): { tool_name, tool_input }
 * Output (stdout JSON): { hookSpecificOutput: { hookEventName, decision, additionalContext? } }
 */
function main() {
  let input = "";
  process.stdin.setEncoding("utf-8");
  process.stdin.on("data", (chunk) => (input += chunk));
  process.stdin.on("end", () => {
    try {
      const { tool_name, tool_input } = JSON.parse(input);

      // Only guard Read operations on data files
      if (tool_name !== "Read") {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      const filePath = tool_input.file_path;
      if (!filePath || !isDataFile(filePath)) {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      // Check file exists and is readable
      if (!fs.existsSync(filePath)) {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
        return;
      }

      const content = fs.readFileSync(filePath, "utf-8");
      const findings = scanContent(content);

      if (findings.length > 0) {
        const summary = findings
          .map((f) => `Line ${f.line}: ${f.excerpt}`)
          .join("; ");

        console.log(
          JSON.stringify({
            hookSpecificOutput: {
              hookEventName: "PreToolUse",
              decision: "allow",
              additionalContext: `Warning: Potential prompt injection detected in ${path.basename(filePath)}. Suspicious patterns found at: ${summary}. Proceed with caution and verify file contents manually.`
            }
          })
        );
      } else {
        console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
      }
    } catch (e) {
      // On error, allow (don't break workflow)
      console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PreToolUse", decision: "allow" } }));
    }
  });
}

main();
