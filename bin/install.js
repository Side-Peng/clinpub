#!/usr/bin/env node

/**
 * clinpub installer
 *
 * Installs clinpub as Claude Code skills.
 *
 * Usage:
 *   npx clinpub                      # Interactive prompt
 *   npx clinpub --global             # Install to ~/.claude/
 *   npx clinpub --local              # Install to ./.claude/
 *   npx clinpub --global --uninstall # Remove global install
 *
 * What it does:
 *   1. Converts commands/clinpub/*.md → skills/clinpub-<name>/SKILL.md
 *   2. Copies agents/, pipeline/, scripts/, hooks/ → shared resource dir
 *   3. Rewrites @-references to point to installed location
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const { execSync } = require('child_process');

// ─── Colors ────────────────────────────────────────────────────────
const cyan = '\x1b[36m';
const green = '\x1b[32m';
const yellow = '\x1b[33m';
const red = '\x1b[31m';
const bold = '\x1b[1m';
const dim = '\x1b[37m';
const reset = '\x1b[0m';

// ─── Package info ──────────────────────────────────────────────────
const pkg = require('../package.json');
const SOURCE_DIR = path.join(__dirname, '..');

// ─── Parse args ────────────────────────────────────────────────────
const args = process.argv.slice(2);
const hasGlobal = args.includes('--global') || args.includes('-g');
const hasLocal = args.includes('--local') || args.includes('-l');
const hasUninstall = args.includes('--uninstall') || args.includes('-u');

// ─── Paths ─────────────────────────────────────────────────────────
function getPaths(isGlobal) {
  const home = os.homedir();
  const claudeRoot = isGlobal
    ? path.join(home, '.claude')
    : path.join(process.cwd(), '.claude');

  return {
    claudeRoot,
    skillsDir: path.join(claudeRoot, 'skills'),
    resourceDir: path.join(claudeRoot, 'clinpub'),  // shared resources
    // Tilde form for @-references in SKILL.md (portable across machines)
    resourceRef: isGlobal
      ? '~/.claude/clinpub'
      : './.claude/clinpub',
  };
}

// ─── Frontmatter extraction ────────────────────────────────────────
function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: null, body: content };
  return { frontmatter: match[1], body: match[2] };
}

function extractField(fm, field) {
  // Handle quoted strings and multiline
  const regex = new RegExp(`^${field}:\\s*["']?([^"'\\n]+)["']?`, 'm');
  const match = fm.match(regex);
  return match ? match[1].trim() : null;
}

function extractMultilineField(fm, field) {
  const regex = new RegExp(`^${field}:\\s*\\n((?:\\s+-\\s+.+\\n?)*)`, 'm');
  const match = fm.match(regex);
  return match ? match[1] : '';
}

// ─── Convert command → skill ───────────────────────────────────────
function convertCommandToSkill(content, skillName, resourceRef) {
  const { frontmatter, body } = extractFrontmatter(content);
  if (!frontmatter) return content;

  const description = extractField(frontmatter, 'description') || '';
  const argumentHint = extractField(frontmatter, 'argument-hint');
  const toolsBlock = extractMultilineField(frontmatter, 'allowed-tools');

  // Rebuild frontmatter in skill format
  let fm = `---\nname: ${skillName}\ndescription: ${yamlQuote(description)}\n`;
  if (argumentHint) fm += `argument-hint: ${yamlQuote(argumentHint)}\n`;
  if (toolsBlock) fm += `allowed-tools:\n${toolsBlock}`;
  fm += '\n---';

  // Rewrite @-references to point to installed resource dir
  // resourceRef is already in tilde form (e.g., ~/.claude/clinpub or ./.claude/clinpub)
  let newBody = body;
  newBody = newBody.replace(/@\.\//g, `@${resourceRef}/`);
  newBody = newBody.replace(/@pipeline\//g, `@${resourceRef}/pipeline/`);
  newBody = newBody.replace(/@agents\//g, `@${resourceRef}/agents/`);
  newBody = newBody.replace(/@scripts\//g, `@${resourceRef}/scripts/`);
  newBody = newBody.replace(/@hooks\//g, `@${resourceRef}/hooks/`);

  return `${fm}\n${newBody}`;
}

function yamlQuote(s) {
  if (!s) return '""';
  // If contains special chars, quote it
  if (/[:#{}[\],&*?|>!%@`]/.test(s) || s.includes('\n')) {
    return `"${s.replace(/"/g, '\\"')}"`;
  }
  return s;
}

// ─── Copy directory recursively ────────────────────────────────────
function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// ─── Remove directory recursively ──────────────────────────────────
function removeDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

// ─── Hook registration ────────────────────────────────────────────
function getSettingsPath(isGlobal) {
  const home = os.homedir();
  return isGlobal
    ? path.join(home, '.claude', 'settings.json')
    : path.join(process.cwd(), '.claude', 'settings.json');
}

function getHookDefinitions(hooksDir, isGlobal) {
  const guardJs = isGlobal
    ? `node "${path.join(hooksDir, 'clinpub-workflow-guard.js')}"`
    : `node "${path.relative(process.cwd(), path.join(hooksDir, 'clinpub-workflow-guard.js'))}"`;

  const boundarySh = isGlobal
    ? `bash "${path.join(hooksDir, 'clinpub-phase-boundary.sh')}"`
    : `bash "${path.relative(process.cwd(), path.join(hooksDir, 'clinpub-phase-boundary.sh'))}"`;

  const promptJs = isGlobal
    ? `node "${path.join(hooksDir, 'clinpub-prompt-guard.js')}"`
    : `node "${path.relative(process.cwd(), path.join(hooksDir, 'clinpub-prompt-guard.js'))}"`;

  return [
    { matcher: 'Write|Edit', hook: { type: 'command', command: guardJs, timeout: 5000 } },
    { matcher: 'Bash', hook: { type: 'command', command: boundarySh, timeout: 5000 } },
    { matcher: 'Read', hook: { type: 'command', command: promptJs, timeout: 3000 } },
  ];
}

function registerHooks(isGlobal) {
  const settingsPath = getSettingsPath(isGlobal);
  const { resourceDir } = getPaths(isGlobal);
  const hooksDir = path.join(resourceDir, 'hooks');
  const hookDefs = getHookDefinitions(hooksDir, isGlobal);

  const settingsDir = path.dirname(settingsPath);
  fs.mkdirSync(settingsDir, { recursive: true });

  let settings = {};
  if (fs.existsSync(settingsPath)) {
    try {
      settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    } catch (e) {
      settings = {};
    }
  }

  if (!settings.hooks) settings.hooks = {};
  if (!settings.hooks.PreToolUse) settings.hooks.PreToolUse = [];

  const preToolUse = settings.hooks.PreToolUse;

  // Remove existing clinpub hook entries (idempotent: delete then add)
  const clinpubPattern = /clinpub-(workflow-guard|phase-boundary|prompt-guard)/;
  for (let i = preToolUse.length - 1; i >= 0; i--) {
    const entry = preToolUse[i];
    if (entry.hooks && entry.hooks.some(h => clinpubPattern.test(h.command))) {
      preToolUse.splice(i, 1);
    }
  }

  // Add clinpub hook entries
  for (const def of hookDefs) {
    preToolUse.push({
      matcher: def.matcher,
      hooks: [def.hook],
    });
  }

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
  console.log(`  ${green}✓${reset} Hooks registered in ${settingsPath}`);
}

function unregisterHooks(isGlobal) {
  const settingsPath = getSettingsPath(isGlobal);

  if (!fs.existsSync(settingsPath)) return;

  let settings;
  try {
    settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  } catch (e) {
    return;
  }

  if (!settings.hooks || !settings.hooks.PreToolUse) return;

  const preToolUse = settings.hooks.PreToolUse;
  const clinpubPattern = /clinpub-(workflow-guard|phase-boundary|prompt-guard)/;
  let removed = 0;

  for (let i = preToolUse.length - 1; i >= 0; i--) {
    const entry = preToolUse[i];
    if (entry.hooks && entry.hooks.some(h => clinpubPattern.test(h.command))) {
      preToolUse.splice(i, 1);
      removed++;
    }
  }

  if (removed > 0) {
    if (preToolUse.length === 0) {
      delete settings.hooks.PreToolUse;
    }
    if (Object.keys(settings.hooks).length === 0) {
      delete settings.hooks;
    }
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    console.log(`  ${green}✓${reset} Removed ${removed} hook entries from ${settingsPath}`);
  }
}

// ─── Install ───────────────────────────────────────────────────────
function install(isGlobal) {
  const { claudeRoot, skillsDir, resourceDir, resourceRef } = getPaths(isGlobal);
  const location = isGlobal ? 'global' : 'local';
  const locationPath = isGlobal ? '~/.claude/' : './.claude/';

  console.log(`\n${bold}${cyan}clinpub v${pkg.version}${reset} — Clinical Data Analysis Pipeline`);
  console.log(`${dim}Installing ${location} to ${locationPath}${reset}\n`);

  // 1. Create directories
  fs.mkdirSync(skillsDir, { recursive: true });
  fs.mkdirSync(resourceDir, { recursive: true });

  // 2. Copy shared resources (agents, pipeline, scripts, hooks)
  console.log(`${dim}Copying resources...${reset}`);
  const resourceDirs = ['agents', 'pipeline', 'scripts', 'hooks'];
  for (const dir of resourceDirs) {
    const src = path.join(SOURCE_DIR, dir);
    if (fs.existsSync(src)) {
      copyDir(src, path.join(resourceDir, dir));
    }
  }
  // Copy CLAUDE.md as reference
  const claudeMd = path.join(SOURCE_DIR, 'CLAUDE.md');
  if (fs.existsSync(claudeMd)) {
    fs.copyFileSync(claudeMd, path.join(resourceDir, 'CLAUDE.md'));
  }
  console.log(`  ${green}✓${reset} Resources → ${resourceDir}`);

  // 3. Convert commands → skills
  const commandsDir = path.join(SOURCE_DIR, 'commands', 'clinpub');
  if (!fs.existsSync(commandsDir)) {
    console.error(`${red}ERROR: commands/clinpub/ not found${reset}`);
    process.exit(1);
  }

  const commandFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith('.md'));
  let installed = 0;

  for (const file of commandFiles) {
    const baseName = file.replace('.md', '');
    const skillName = `clinpub-${baseName.replace(/:/g, '-')}`;
    const skillDir = path.join(skillsDir, skillName);

    // Clean old version
    removeDir(skillDir);
    fs.mkdirSync(skillDir, { recursive: true });

    // Convert command → skill
    const content = fs.readFileSync(path.join(commandsDir, file), 'utf8');
    const skillContent = convertCommandToSkill(content, skillName, resourceRef);

    fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent);
    console.log(`  ${green}✓${reset} /${baseName} → skills/${skillName}/SKILL.md`);
    installed++;
  }

  // 4. Register hooks in settings.json
  registerHooks(isGlobal);

  // 5. Summary
  console.log(`\n${green}${bold}Installed ${installed} skills${reset}`);
  console.log(`${dim}Resources at: ${resourceDir}${reset}`);
  console.log(`\n${bold}Usage:${reset}`);
  console.log(`  /clinpub                    # Full 5-phase pipeline`);
  console.log(`  /clinpub-data2idea <file>   # Topic mining`);
  console.log(`  /clinpub-analysis           # Statistical analysis`);
  console.log(`  /clinpub-writing            # Manuscript writing`);
  console.log(`  /clinpub-review             # Peer review simulation`);
  console.log(`\n${dim}Restart Claude Code to load new skills.${reset}\n`);
}

// ─── Uninstall ─────────────────────────────────────────────────────
function uninstall(isGlobal) {
  const { skillsDir, resourceDir } = getPaths(isGlobal);
  const location = isGlobal ? 'global' : 'local';

  console.log(`\n${bold}${yellow}Uninstalling clinpub (${location})${reset}\n`);

  // Remove skill directories
  if (fs.existsSync(skillsDir)) {
    const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
    let removed = 0;
    for (const entry of entries) {
      if (entry.isDirectory() && entry.name.startsWith('clinpub-')) {
        removeDir(path.join(skillsDir, entry.name));
        console.log(`  ${green}✓${reset} Removed skills/${entry.name}`);
        removed++;
      }
    }
    console.log(`\n${green}Removed ${removed} skills${reset}`);
  }

  // Remove resource directory
  if (fs.existsSync(resourceDir)) {
    removeDir(resourceDir);
    console.log(`  ${green}✓${reset} Removed ${resourceDir}`);
  }

  // Remove hook registrations from settings.json
  unregisterHooks(isGlobal);

  console.log(`\n${green}${bold}clinpub uninstalled.${reset}\n`);
}

// ─── Interactive prompt ────────────────────────────────────────────
async function promptLocation() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q) => new Promise(resolve => rl.question(q, resolve));

  console.log(`\n${bold}${cyan}clinpub v${pkg.version}${reset}\n`);
  console.log(`Install location:`);
  console.log(`  ${bold}1${reset} — Global  (all projects, ~/.claude/)`);
  console.log(`  ${bold}2${reset} — Local   (current project only, ./.claude/)\n`);

  const choice = await ask(`${cyan}>${reset} Choose (1/2): `);
  rl.close();

  return choice.trim() === '1';
}

// ─── Main ──────────────────────────────────────────────────────────
async function main() {
  // --version: print version and exit
  if (args.includes('--version') || args.includes('-v')) {
    console.log(`clinpub v${pkg.version}`);
    process.exit(0);
  }

  // --help: print usage and exit
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
${bold}${cyan}clinpub v${pkg.version}${reset} — Clinical Data Analysis Pipeline

${bold}Usage:${reset}
  npx clinpub-cc [options]

${bold}Options:${reset}
  --version, -v     Show version number
  --help, -h        Show this help message
  --global, -g      Install globally (~/.claude/)
  --local, -l       Install locally (./.claude/)
  --uninstall, -u   Remove clinpub installation

${bold}Examples:${reset}
  npx clinpub-cc --global        # Global install
  npx clinpub-cc --local         # Local install
  npx clinpub-cc --uninstall     # Uninstall
`);
    process.exit(0);
  }

  if (hasUninstall) {
    uninstall(hasGlobal || !hasLocal);
    return;
  }

  if (hasGlobal) {
    install(true);
  } else if (hasLocal) {
    install(false);
  } else {
    // Interactive
    const isGlobal = await promptLocation();
    install(isGlobal);
  }
}

main().catch(err => {
  console.error(`${red}Error: ${err.message}${reset}`);
  process.exit(1);
});
