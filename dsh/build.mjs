#!/usr/bin/env node
/**
 * ClinPub 3.0 — DSH 技能生成器
 *
 * 为什么有这个脚本
 * ----------------
 * DSH 的技能是「拉取式」的：技能正文会被注入上下文，但技能里 `@` 引用的文件
 * 不会自动展开。Claude Code 命令用 `!`cat ...`` 做 push，DSH 没有对应机制。
 *
 * 所以这里在**构建期**把 workflow 正文内联进 SKILL.md —— 技能被加载时正文必然
 * 进入上下文，等价于 Claude Code 的 `!cat`。（见 docs/CLINPUB-3.0-DESIGN.md D3）
 *
 * 单一数据源：claude-code/commands/*.md + claude-code/pipeline/workflows/*.md
 * 输出：.dsh/skills/<name>/SKILL.md
 *
 * 用法：
 *   node dsh/build.mjs          # 生成
 *   node dsh/build.mjs --check  # 只比对，不写文件（CI 用）
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync, rmSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO = resolve(HERE, '..')
const SRC = join(REPO, 'claude-code')
const OUT = join(REPO, '.dsh', 'skills')

const CHECK = process.argv.includes('--check')

/** 每个技能：命令文件、要内联的 workflow、要列出路径的参考资源。 */
const SKILLS = [
  {
    name: 'clinpub',
    command: 'clinpub.md',
    workflows: ['next-step.md', 'milestone.md'],
    refs: [
      'pipeline/references/gates.md',
      'pipeline/references/checkpoints.md',
      'pipeline/templates/milestone.md',
    ],
    whenToUse:
      '想知道当前进度、查看命令参考、推进到下一阶段，或不确定该运行哪条命令时。',
  },
  {
    name: 'clinpub-initialize',
    command: 'initialize.md',
    workflows: ['init-project.md', 'import-project.md'],
    refs: ['pipeline/references/import-heuristics.md', 'pipeline/references/checkpoints.md'],
    whenToUse: '新项目开始，或要把已有的研究材料导入 ClinPub 结构时。',
  },
  {
    name: 'clinpub-data-prep',
    command: 'data-prep.md',
    workflows: ['data-prep.md'],
    refs: ['pipeline/references/import-heuristics.md'],
    whenToUse: '阶段1：拿到了原始患者级数据，需要清洗成 cleaned.csv 时。',
  },
  {
    name: 'clinpub-data2idea',
    command: 'data2idea.md',
    workflows: ['data2idea.md'],
    refs: [
      'pipeline/references/pre-phase-research.md',
      'pipeline/references/reference-library.md',
      'agents/topic-miner-agent.md',
    ],
    whenToUse: '有数据但还没定选题，想让数据告诉你能做什么研究时。',
  },
  {
    name: 'clinpub-analysis',
    command: 'analysis.md',
    workflows: ['analysis.md'],
    refs: [
      'pipeline/references/analysis_decision_policy.md',
      'pipeline/references/analysis_methods.md',
      'pipeline/references/r_patterns.md',
      'pipeline/references/comparison-methods.md',
    ],
    whenToUse: '阶段2：数据已清洗，需要做统计分析。可反复运行，每次推进一批方法。',
  },
  {
    name: 'clinpub-writing',
    command: 'writing.md',
    workflows: ['writing.md'],
    refs: [
      'pipeline/references/writing_standards.md',
      'pipeline/references/journal_standards.md',
      'pipeline/references/citation-strategy.md',
      'pipeline/references/reference-library.md',
      'pipeline/references/concatenation-protocol.md',
      'pipeline/templates/section.md',
      'pipeline/templates/figure-skeleton.md',
      'pipeline/templates/narrative.md',
      'agents/writer-agent.md',
      'agents/reference-agent.md',
    ],
    whenToUse: '阶段3：分析已冻结，需要写 IMRAD 手稿。从图表骨架和 Results 开始。',
  },
  {
    name: 'clinpub-modify',
    command: 'modify.md',
    workflows: ['modify.md'],
    refs: [
      'pipeline/references/analysis_methods.md',
      'pipeline/references/r_patterns.md',
      'pipeline/references/analysis_decision_policy.md',
      'agents/modify-agent.md',
    ],
    whenToUse: '分析做完后要改图、改方法、换变量或加新方法时。',
  },
  {
    name: 'clinpub-improving',
    command: 'improving.md',
    workflows: ['improving.md'],
    refs: [
      'pipeline/references/writing_standards.md',
      'pipeline/references/journal_standards.md',
      'pipeline/references/analysis_decision_policy.md',
      'pipeline/references/reference-library.md',
      'agents/writer-agent.md',
      'agents/reference-agent.md',
      'agents/modify-agent.md',
    ],
    whenToUse: '手稿已有草稿，想自审并直接改进（可反复调用，不写回复信）。',
  },
  {
    name: 'clinpub-review',
    command: 'review.md',
    workflows: ['review.md'],
    refs: [
      'pipeline/references/journal_standards.md',
      'pipeline/references/reference-library.md',
      'agents/reference-agent.md',
    ],
    whenToUse: '投稿后收到真实审稿意见，需要逐条回复并修稿时。不模拟审稿人。',
  },
  {
    name: 'clinpub-coverletter',
    command: 'coverletter.md',
    workflows: ['coverletter.md'],
    refs: ['pipeline/references/journal_standards.md'],
    whenToUse: '手稿完成、要按目标期刊准备投稿信时。',
  },
]

/** 去掉 YAML frontmatter，返回 { meta, body }。 */
function splitFrontmatter(text) {
  // 归一化行尾：仓库里同时存在 LF 与 CRLF 文件，CRLF 会让 `.*$` 匹配不到值。
  const t = text.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n')
  if (!t.startsWith('---')) return { meta: {}, body: t }
  const end = t.indexOf('\n---', 3)
  if (end === -1) return { meta: {}, body: t }
  const head = t.slice(3, end)
  const body = t.slice(end + 4).replace(/^\n+/, '')
  const meta = {}
  for (const line of head.split('\n')) {
    const m = line.match(/^(\w[\w-]*):\s*(.*)$/)
    if (m) meta[m[1]] = m[2].trim().replace(/^["']|["']$/g, '')
  }
  return { meta, body }
}

/** 把命令正文里的 XML 式标签转成标题，并移除 execution_context（由内联 workflow 取代）。 */
function normalizeCommandBody(body) {
  return body
    .replace(/<execution_context>[\s\S]*?<\/execution_context>/g, '')
    .replace(/<objective>/g, '## 目标')
    .replace(/<\/objective>/g, '')
    .replace(/<process>/g, '## 流程')
    .replace(/<\/process>/g, '')
    .replace(/<success_criteria>/g, '## 成功标准')
    .replace(/<\/success_criteria>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

/** 把 workflow 正文的 step 标签转成小标题。 */
function normalizeWorkflowBody(body) {
  return body
    .replace(/<step name="([^"]+)"[^>]*>/g, '### $1')
    .replace(/<\/step>/g, '')
    .replace(/<substep name="([^"]+)"[^>]*>/g, '#### $1')
    .replace(/<\/substep>/g, '')
    .replace(/<required_reading>[\s\S]*?<\/required_reading>/g, '')
    .replace(/<purpose>/g, '')
    .replace(/<\/purpose>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

function buildSkill(skill) {
  let description = ''
  let commandBody = ''

  if (skill.command) {
    const raw = readFileSync(join(SRC, 'commands', skill.command), 'utf8')
    const { meta, body } = splitFrontmatter(raw)
    description = meta.description || ''
    commandBody = normalizeCommandBody(body)
  } else {
    description =
      'ClinPub 知识库索引：方法库、写作规范、质量门控、引用策略与项目模板。需要查阅时加载。'
  }

  // DSH 目录描述上限 500 字符（超出会被截断）
  if (description.length > 480) description = description.slice(0, 477) + '…'

  const parts = []
  parts.push('---')
  parts.push(`name: ${skill.name}`)
  parts.push(`description: ${JSON.stringify(description)}`)
  if (skill.whenToUse) parts.push(`whenToUse: ${JSON.stringify(skill.whenToUse)}`)
  parts.push('---')
  parts.push('')
  parts.push(`# ${skill.name}`)
  parts.push('')

  if (commandBody) {
    parts.push(commandBody)
    parts.push('')
  } else {
    parts.push('## 知识库')
    parts.push('')
    parts.push('本技能是 ClinPub 3.0 的共享知识入口。按需读取下列文件（路径相对本技能目录）。')
    parts.push('')
  }

  for (const wf of skill.workflows) {
    const raw = readFileSync(join(SRC, 'pipeline', 'workflows', wf), 'utf8')
    const { body } = splitFrontmatter(raw)
    parts.push('---')
    parts.push('')
    parts.push(`## 执行流程（内联自 pipeline/workflows/${wf}）`)
    parts.push('')
    parts.push(normalizeWorkflowBody(body))
    parts.push('')
  }

  if (skill.refs.length) {
    parts.push('---')
    parts.push('')
    parts.push('## 参考资源')
    parts.push('')
    parts.push('路径相对本技能目录（`../../../dsh/` 指向仓库共享核心）。**按需读取**，不要一次全读。')
    parts.push('')
    for (const ref of skill.refs) {
      parts.push(`- \`../../../dsh/${ref}\``)
    }
    parts.push('')
  }

  parts.push('---')
  parts.push('')
  parts.push(
    '> 本文件由 `node dsh/build.mjs` 生成，请勿手改。修改源文件：`claude-code/commands/` 与 `claude-code/pipeline/workflows/`。'
  )
  parts.push('')

  return parts.join('\n')
}

function main() {
  if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true })

  let written = 0
  let skipped = 0
  let pruned = 0
  const problems = []
  const wanted = new Set(SKILLS.map((s) => s.name))

  // 清理：合并/删除过的技能如果留在目录里，DSH 仍会发现它——必须显式删除。
  if (!CHECK) {
    for (const entry of readdirSync(OUT, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue
      if (wanted.has(entry.name)) continue
      rmSync(join(OUT, entry.name), { recursive: true, force: true })
      pruned++
      console.log(`  - 已移除过期技能：${entry.name}`)
    }
  }

  for (const skill of SKILLS) {
    if (skill.command && !existsSync(join(SRC, 'commands', skill.command))) {
      problems.push(`缺少命令文件：${skill.command}`)
      continue
    }
    for (const wf of skill.workflows) {
      if (!existsSync(join(SRC, 'pipeline', 'workflows', wf))) {
        problems.push(`缺少 workflow：${wf}`)
      }
    }

    const content = buildSkill(skill)
    const dir = join(OUT, skill.name)
    const file = join(dir, 'SKILL.md')

    if (CHECK) {
      const existing = existsSync(file) ? readFileSync(file, 'utf8') : ''
      if (existing !== content) problems.push(`过期：${skill.name}`)
      else skipped++
      continue
    }

    mkdirSync(dir, { recursive: true })
    writeFileSync(file, content, 'utf8')
    written++
  }

  if (problems.length) {
    console.error(CHECK ? '[FAIL] 技能与源文件不一致：' : '[FAIL] 生成失败：')
    for (const p of problems) console.error('  - ' + p)
    process.exit(1)
  }

  console.log(
    CHECK
      ? `[OK] ${skipped} 个技能均为最新`
      : `[OK] 已生成 ${written} 个技能（清理 ${pruned} 个）→ .dsh/skills/`
  )
}

main()
