# ClinPub → DeepSeek Harness 迁移方案

> 状态：**🚧 进行中 — DSH 已定为 3.0 主实现**（2026-10-18 决定：Qoder 平台移除，以后主版本以 DSH 为主）
> 目标平台：DeepSeek Harness (DSH) Desktop **0.2.1-rc.2**（已复核；旧版 0.2.0-rc.2 的结论见 [§2.3](#23-版本复核021-相对-020)）

## 实施进度（2026-10-18）

> ⚠️ **本文档 §5.2 的命令映射表写于命令精简之前（14 个）。**
> 2026-10-18 已将 `overview` / `do` / `next-step` / `milestone` 合并为 `clinpub` 枢纽，
> 并删除 `knowledge`，**现行命令为 10 个**——以仓库根 `README.md` 的命令表为准。

| 项 | 状态 |
|---|---|
| `.dsh/skills/` **10** 个技能 | ✅ 已生成，**DSH 实测全部加载** |
| `dsh/` 共享核心（pipeline / scripts / agents） | ✅ 与 3.0 核心字节一致 |
| `dsh/build.mjs` 生成器 | ✅ 幂等（`--check` 通过） |
| 技能正文内联 workflow | ✅ 已验证（如 `clinpub-writing` 503 行含全部 step） |
| 参考资源相对路径 `../../../dsh/…` | ✅ 实测可解析 |
| 阶段守卫（`tools/pre-execute`） | ⏳ 未实现（v0.2） |
| bundle（`package.json` + `cordis.patch.yml`，跨项目安装） | ⏳ 未实现（v0.3） |
| 端到端跑真实数据 | ⏳ 未验证 |

> **当前源码方向**：`claude-code/commands` + `claude-code/pipeline` 是编写源，`.dsh/skills/` 是生成物。
> 待 DSH 版验证过真实数据后再翻转方向（见 [§12 开放问题](#9-开放问题)）。
>
> **踩过的坑（CRLF）**：仓库里行尾不统一，`initialize` / `coverletter` / `improving` 三个命令是 CRLF。
> 按 `\n` 切 YAML frontmatter 会残留 `\r`，导致 `description` 解析为空、技能被 DSH 静默丢弃。
> `build.mjs` 已在 `splitFrontmatter` 里归一化行尾。
> 关联版本：clinpub v2.3.0（三平台齐平）
> 本文与「管线升级」的关系见 [§0](#0-与管线升级的关系先读这一段)
>
> **⚠️ 本文档假设 DSH 处于快速演进期**。所有 DSH 契约都标注了采集版本，**每个开发阶段开始前必须重新复核一遍** [§2.3](#23-版本复核021-相对-020)。

---

## 0. 与管线升级的关系（先读这一段）

本文是**迁移适配方案**，不是**管线内容方案**。两者解耦，但有明确的先后与复用关系：

| | 管线升级（另行规划） | 本文（平台迁移） |
|---|---|---|
| 改什么 | `pipeline/` 的流程内容：阶段划分、门控、模板、方法库 | 命令/智能体/钩子在 DSH 上的**存在形态** |
| 影响面 | 四个平台全部受影响 | 只新增 `dsh/` |
| 顺序建议 | **先定稿管线语义** | 再按最终语义生成 `dsh/` |

**为什么建议这个顺序**：`dsh/` 的 10 个技能是 `commands/*.md` 的**翻译产物**。如果先翻译、再改管线，13 个技能要返工一遍（这与 `CHANGELOG.md` 里 qoder 从 v2.2.0 追到 v2.3.0、codex 又追一次的返工模式完全一样）。

**但有一个例外**：**目录骨架与共享引用策略**（`.dsh/skills/` + `dsh/`，见 [§5.1](#51-目录结构)）与管线内容无关，可以先行落地；它同时也是本文的核心交付物，定下来就不会返工。

**已确定的耦合点**（管线升级若触及，`dsh/` 必须同步）：

1. 阶段编号与目录归属（阶段0–3 → `.clinpub/`、`01_RawData/` … `05_Manuscript/`）
2. `.clinpub/STATE.md` 的阶段行格式（钩子用正则 `阶段：Phase\s*(\d+)` 读取）
3. 命令清单（10 个 → 10 个技能，增删都要同步）
4. 智能体清单（8 个 → 8 个 Agent Preset + 1 个带 `agent_preset` 白名单的委派工具）
5. 门控数量与位置（`pipeline/references/gates.md`）

---

## 1. 迁移结论

| 结论 | 说明 |
|---|---|
| **技术可行** | 无架构级阻塞；DSH 的原生能力覆盖面**优于** Codex/Qoder 的适配面 |
| **不是移植，是适配层** | 提示词内容（约 450KB）基本原样复用；需替换 4 个 Claude Code 专有机制 |
| **工作量重心** | 不在"搬文本"，在**编排语义重建**（8 智能体 → 8 个 Agent Preset）与**安装形态** |
| **顺带收益** | ClinPub 可反向吃到 DSH 原生能力：`/name` 用户直调、插件市场、版本门禁 |
| **最大风险** | DSH 处于 rc 阶段，**一个版本就移除了整个 hooks 子系统**（0.2.0→0.2.1）。方案必须假设上游包随时消失 |

**四个 Claude Code 专有机制需替换**：

1. 命令里的 Shell 注入（`` !`cat ${CLAUDE_PLUGIN_ROOT}/...` ``）→ DSH 无对应物，改为**构建期内联进 SKILL.md 正文**（唯一能保住 push 确定性的做法）
2. `allowed-tools:` frontmatter → DSH 技能格式**无此字段**（全量扫描 0 命中），改由 **preset 的工具插件列表**控制
3. Task 工具的 `subagent_type: <agent-name>` → 8 个具名委派工具，各自钉一个 `agentPreset`（能力保住了，形态变了）
4. **`hooks/*.js` PreToolUse 守卫 → 自写原生插件监听 `tools/pre-execute`**（0.2.1 已移除钩子桥接包；原生写法反而更好用）

---

## 2. 迁移基线（实测数据）

### 2.1 仓库现状

来源 `claude-code/`（其余两平台为等价独立实现，仅作对照）：

| 目录 | 文件数 | 字节 | 迁移处置 |
|---|---:|---:|---|
| `commands/` | 10 | 见实测 | → 10 个技能 `SKILL.md`（**改写**） |
| `agents/` | 8 | 80,675 | → 8 份角色卡（**原样保留**，作为子 preset 的角色技能） |
| `pipeline/workflows/` | 12 | 128,667 | → 技能 `references/`（**保留**，改引用语法） |
| `pipeline/references/` | 16 | 189,505 | → 共享 `references/`（**保留**） |
| `pipeline/templates/` | 19 | 68,404 | → 共享 `references/templates/`（**保留**） |
| `pipeline/contexts/` | 2 | 3,581 | → 并入对应技能 |
| `scripts/` | 7 | 115,690 | → 共享 `scripts/`（**原样**，Python 无平台差异） |
| `hooks/` | 3 | 15,528 | → 桥接挂载（**1 个需补 pwsh 版**） |

`codex/clinpub/` 与 `qoder/` 的文件数对照（`skills` 13 / `agents` 8 / `pipeline` 49 / `scripts` 7 / `hooks` 3）证实三平台共享核心一致，迁移可复用同一套内容。

### 2.2 运行时环境（本机实测）

| 组件 | 状态 |
|---|---|
| R | 4.4.3 ✅ **740 个包**，ClinPub 依赖的 23 个包中 **仅缺 `ggsurvfit`** |
| Python | 系统 3.12.3 ✅；DSH 随附 3.12.14（pandas 3.0.1 / numpy 2.3.5 / openpyxl 3.1.5 ✅） |
| Python 缺口 | DSH 随附环境**无** scipy / statsmodels / lifelines / matplotlib / sklearn |
| DSH 桌面 | **0.2.1-rc.2**（`runtime.json` 的 `desktopVersion`；asar 182MB） |
| DSH CLI（PATH） | **0.2.1-rc.2** ✅（2026-10-17 已从 `0.2.0-rc.2` 升级并对齐） |

> **行动项**：
> 1. `ggsurvfit` 需补装，否则生存分析图表脚本失败；
> 2. ~~把 PATH 上的 `dsh` 升到 0.2.1~~ ✅ **已完成**——注意 npm 的 `latest` 标签仍指向 `0.2.0-rc.2`，**必须显式指定版本**：
>    `npm install -g @deepseek-ai/dsh@0.2.1-rc.2`（或 `@deepseek-ai/dsh@next`）；
> 3. 若未来 Python 侧要接管统计，需为 DSH 随附 Python 安装 scipy/statsmodels——**当前不影响**（ClinPub 统计以 R 为主）。

### 2.3 版本复核（0.2.1 相对 0.2.0）

> 这一节是全文档最容易被未来版本推翻的部分。**每次开工前先读它，再决定要不要重跑一遍核对。**

#### 破坏性变更（必须改方案）

| 变更 | 影响 | 处置 |
|---|---|---|
| **hooks 子系统整体移除**：`dsh-hooks-claude-code`、`dsh-hooks-codex`、`dsh-hook-protocol`、`dsh-webhook*` [E20] | 原 v0.2「直接复用 hooks.json」**作废** | 改为自写 `tools/pre-execute` 插件（见 [§3.3](#33-钩子--自写原生插件021-起桥接已不存在)），**反而更好** |
| **标准 preset 移除 Codex / Claude Code 子代理提供方**，并移除 `tool-ralph` [E25] | "跨引擎委派"的路没了 | ClinPub 不依赖它们，影响有限 |
| **标准 preset 移除 `backgroundMode: continuable`** [E25] | 子代理默认回到 **`one-shot` 前台** | 要 8 个 agent 并行，必须在自己 preset 里显式写 `backgroundMode: continuable` + `enableRunInBackground` |

#### 新增能力（可利用）

| 变更 | 机会 |
|---|---|
| **插件市场**：`dsh-plugin-market` / `-index` / UI「发现」页 / `plugin_market` 工具 [E23] | ClinPub 可发布一个**市场索引**，用户加 URL 即可浏览安装；比"下 tarball"体验好得多 |
| **`engines.dsh` 版本门禁** [E24] | 安装前就拒绝不兼容版本，**不下载、不执行构建脚本**；ClinPub 应声明 `engines.dsh` |
| 新增 `dsh-time-context`、`dsh-tool-schedule` 等 | 与 ClinPub 关系不大 |

#### 未变（结论仍成立）

| 组件 | 核对结果 |
|---|---|
| `dsh-tool-subagent` | **字节数完全一致**（33,853）→ `persona`/`toolFilter` 仍被拒绝、`agentPreset` 仍可单独设 [E15] |
| `tool-result-pruner` | 配置仍是 `8192/4096/1024` [E17] |
| 技能子系统（`dsh-skill-filesystem` / `dsh-tool-skill`） | 仍在随附包中 |
| 扩展点事件 | `tools/pre-execute`、`agent/pre-step`、`agent/turn-stopping`、`subagent/start` **全部仍在** [E21] |
| `dsh-plugin-manager` 的 `install_bundle` | 仍在；仍要求 `danger-full-access` 或逐次批准 [E24] |
| 包总数 | 289 → **306** |

#### 顺带发现

- `dsh-persona` 的配置简化：标准 preset 现在只写 `prefix`，去掉了 `suffix` 与 `{{cwd}}` 占位符 [E25]
- 已解决：升级前本机 `dsh --version` 输出 `0.2.0-rc.2`，与桌面的 `0.2.1-rc.2` 不一致；**已于 2026-10-17 升级并对齐**

---

## 3. 平台语义映射表

每条均标注证据来源。证据编号见 [§11](#11-证据索引)。

### 3.1 命令 → 技能

| 项 | Claude Code | DSH | 证据 |
|---|---|---|---|
| 载体 | `commands/*.md` | 技能目录 `<name>/SKILL.md` | E3 E5 |
| 命名 | `analysis`，调用为 `/clinpub:analysis` | **强制 kebab-case** `^[a-z0-9]+(-[a-z0-9]+)*$` → `clinpub-analysis`，调用为 `/clinpub-analysis` | E5 |
| 必填 frontmatter | `name` / `description` | `name` / `description`（**≤500 字符**，超出截断） | E3 E5 |
| 可选字段 | `argument-hint`、`allowed-tools` | `whenToUse`、`metadata`、`disable-model-invocation`、`user-invocable` | E3 |
| 发现位置 | 插件 `commands/` 自动发现 | `<repo>/.dsh/skills`(100) → `<repo>/.agents/skills`(200) → `customSkillDirs`(300) → `~/.dsh/skills`(400) → `~/.agents/skills`(500) → `bundledSkillDir`(600) | E3 E4 |
| 发现深度 | 递归 | **仅一层**：`<root>/<name>/SKILL.md` 或 `<root>/<name>.md`；**不支持嵌套 `**/SKILL.md`** | E3 E4 |
| 调用 | `/clinpub:analysis` | 模型侧 `skill({name})`；用户侧 `/clinpub-analysis` 直接注入 | E6 |
| 资源指引 | `@./` + `${CLAUDE_PLUGIN_ROOT}` | 技能结果携带 `<skill_resources>`：`Base directory for this skill: <path>`，正文相对路径按它解析 | E6 |
| 工具授权 | `allowed-tools:` 声明 | **无对应字段**，由 preset / 委派工具 `toolFilter` 控制 | E3 |
| Shell 注入 | `` !`cat ...` `` 执行并注入 | **无对应物** → 改为正文引用 + 模型按需 `read` | E3 E6 |

### 3.2 智能体 → Agent Preset

| 项 | Claude Code | DSH | 证据 |
|---|---|---|---|
| 定义 | `agents/*.md`（8 个，frontmatter + 角色卡） | 8 个 **Agent Preset**（`@deepseek-ai/dsh-agent-preset`），每个 preset 自带 persona + 工具插件列表 | E7 E15 |
| 选择方式 | Task 工具 `subagent_type: analyst-agent` | 委派工具配置 **`allowedAgentPresets`** → 工具 schema 自动暴露 `agent_preset` 枚举参数，**由模型按任务选择** | E15 |
| 隔离上下文 | 每次独立上下文 | `spawn` 提供方：子代理看不到本对话 | E7 |
| 角色注入 | 角色卡全文进入子代理 | preset 内的 `@deepseek-ai/dsh-persona`（`prefix`），**构建期把角色卡内联进去** | E15 D7 |
| 深度 | 无显式限制 | 默认 `maxDepth: 1` → **子代理不能再委派**（与 ClinPub "只有编排器委派"契约一致 ✅） | E7 |
| 并发 | — | `backgroundMode: continuable`，上限 `maxActiveSubagents` 默认 8 ✅（对应 8 个智能体） | E8 |
| 模型路由 | — | 可公开 `provider`/`model`/`reasoning_effort`（需 `modelSelectionSettings: true`） | E7 |

> **⚠️ 关键：`persona` / `toolFilter` 已废弃**
> 多个 DSH 包的 **README 仍写着** `dsh-tool-subagent` 支持实例级 `persona` / `toolFilter`，但 **0.2.0-rc.2 的代码会直接抛错**：
> `tool-subagent: persona is no longer supported; configure persona and tool plugins in an Agent Preset and select it with agentPreset (spawn only)`
> 因此**不能**用"8 个工具各绑一份 persona"的写法。正确做法是：定义 8 个 preset，用一个委派工具配 `allowedAgentPresets` 白名单放开。这个差异是本次调研最重要的发现，**文档与代码不一致时以代码为准**。[E15]
>
> 另注：preset 选择**仅 `spawn` 提供方支持**，`fork` 提供方不支持。

### 3.3 钩子 → 自写原生插件（**0.2.1 起，桥接已不存在**）

> **🔴 0.2.1-rc.2 重大变更**：`dsh-hooks-claude-code` / `dsh-hooks-codex` / `dsh-hook-protocol` / `dsh-webhook*` **全部从随附包中移除** [E20]。
> 原先"直接复用现有 hooks.json"的方案**作废**。
>
> 但**扩展点本身仍在**：`tools/pre-execute`（35 处）、`agent/pre-step`（63 处）、`agent/turn-stopping`（11 处）[E21]。
> 桥接只是这些事件的一个**打包消费者**，CLinPub 可以自己实现同样的事——而且**更好**。

| ClinPub 钩子 | 新实现 | 事件 | 说明 |
|---|---|---|---|
| `clinpub-workflow-guard.js` | 原生插件 | `tools/pre-execute` | 越阶段写目录 → `{ kind: 'deny', reason }` |
| `clinpub-phase-boundary.sh` | 原生插件 | `tools/pre-execute` | **不再需要 bash 与 pwsh 双份**——JS 直接判断，Windows/macOS/Linux 一致 |
| `clinpub-prompt-guard.js` | 原生插件 | `tools/pre-execute` | 命中 `read` 时扫注入模式 |

**自写守卫的最小形态**（比 `ctx.on` 更简洁：DSH 提供同步的 `ctx.tools.guard()`）[E22 E26]：

```js
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.guard(exec => {
    if (exec.name !== 'write' && exec.name !== 'edit') return
    const filePath = exec.arguments?.file_path        // ✅ 与 Claude Code 同名
    if (!filePath) return
    const phase = readPhase(process.cwd())            // 读 .clinpub/STATE.md
    const dir = firstSegment(filePath)
    if (blocked(phase, dir)) {
      return `目录 ${dir} 属于 Phase ${n}，当前是 Phase ${phase}`  // 返回字符串 = 拒绝
    }
  })
}
```

**关键确认** [E26]：
- `ctx.tools.guard(guard)` 是**同步**守卫，位于 `tools/pre-execute` waterfall **之后**；返回字符串即拒绝，且"任何守卫都不能强制放行被另一个守卫拒绝的调用"
- `exec` 携带 `arguments`（源码 `snapshotJsonValue(exec.arguments)`），因此能拿到目标路径
- **`write` 与 `edit` 的参数名都是 `file_path`**——与 Claude Code 一致，`clinpub-workflow-guard.js` 的逻辑可近乎原样移植
- 用 `agent.ctx` 注册的守卫只作用于该 agent；普通上下文注册则全局生效

**仍有待运行时确认**：preset 级插件里 `ctx.tools` 是否可直接注入（设计上可以，需 v0.2 首次装载时验证）。

**相比桥接的四个改进**：

1. **`reason` 是一等字段** —— 原桥接的 `additionalContext` 在 `PreToolUse` 上会被忽略，拒绝原因会丢；原生插件直接返回 `reason`，用户一定看得到 [E9 已作废]
2. **无 bash 依赖** —— 不需要 `.sh`，也不需要为 Windows 补 `.ps1`
3. **无 matcher 大小写陷阱** —— 直接用 `exec.name === 'write'` 判断
4. **无退出码语义** —— 不依赖 `exit 2` 与 stderr 约定

**仍需注意**：

- 插件的 `apply` 里所有注册都要走 `ctx.effect` / `ctx.on`，否则卸载时不会清理
- `deny` 对象形状为 `{ kind: 'deny', reason: string }`；另有 `{ kind: 'cancel' }` [E22]
- 每会话只读一次 STATE.md 之类可加缓存，但要注意 DSH 侧没有"文件变更"事件可挂

### 3.4 安装与分发

| 项 | Claude Code | DSH 0.2.1-rc.2 | 证据 |
|---|---|---|---|
| 清单 | `.claude-plugin/plugin.json` | `package.json` 内 `dsh.bundle.patch` 指向 `cordis.patch.yml` | E10 |
| 分发单元 | Marketplace / `--plugin-dir` | **bundle**（组合包） | E10 |
| 安装 | `claude plugin install` | `dsh plugin add ./目录`、`github:user/repo`、`./xxx.tgz`、npm 包名 | E10 |
| **新增：插件市场** | — | `dsh-plugin-market` + 索引 URL（用户自加），Web「发现」标签页可浏览安装；`plugin_market` 工具（默认禁用，Creator 模式启用） | E23 |
| **新增：版本门禁** | — | 安装前校验 `engines.dsh`；不满足则**不下载、不执行构建脚本**即失败；可用 `compatibility.json` 逐版本豁免 | E24 |
| 技能注入 | — | bundle 行配置 `bundledSkillDir`（rank 600） | E4 |
| **桌面版限制** | — | **`dsh plugin --profile desktop` 被拒绝**（"profile desktop is managed exclusively by the Electron application"，实测）→ 桌面版必须走**应用内插件管理器 / 插件页** | E11 |
| patch 语义 | — | **按行覆盖，替换整份 `config`，不深合并** → 覆盖时必须重述所有键 | E10 |
| 层顺序 | — | bundles 列表 → profile `cordis.patch.yml` → `$DSH_HOME/cordis.patch.yml` → `--patch` overlay | E10 |

> **✅ 版本一致性已解决（2026-10-17）**：CLI 已升级到 **0.2.1-rc.2**，与桌面版对齐。
> 升级要点（供 `INSTALL.md` 参考）：
> - npm 的 `latest` 标签仍指向 `0.2.0-rc.2`，**直接 `npm i -g @deepseek-ai/dsh` 不会升级**，必须 `@0.2.1-rc.2` 或 `@next`
> - 升级后 npm 的 `dsh` 启动壳会重建（升级前它曾因应用更新而丢失）
> - npm 11 会拦下 5 个包的安装脚本，但 **Windows 上均非必需**：`dsh-subprocess-local` 的后装脚本只补 POSIX 可执行位；`koffi` / `node-pty` 自带 win32-x64 预编译产物（实测均可加载）
>
> **桌面 profile 仍不可由 CLI 操作**：`dsh --profile desktop --dump-config` 依旧报 "profile desktop is managed exclusively by the Electron application"（0.2.1 未变）。

---

## 4. DSH 侧架构设计

### 4.1 三层对应关系

```
Claude Code                          DSH 0.2.1-rc.2
─────────────────────────────────────────────────────────────
commands/*.md (13 斜杠命令)    →     .dsh/skills/<name>/SKILL.md（14 技能）
agents/*.md (8 智能体)         →     8 个具名委派工具，各自钉一个 Agent Preset
                                     （agentPreset，不暴露 agent_preset 枚举）
hooks/*.js,*.sh (3 钩子)       →     自写原生插件：ctx.on('tools/pre-execute')
                                     （桥接包 dsh-hooks-claude-code 已移除）
pipeline/** (共享核心)         →     dsh/pipeline/**（原样，改引用语法）
scripts/*.py                   →     dsh/scripts/**（原样）
.clinpub/ + 项目目录            →     不变（STATE.md 契约不变）
```

### 4.2 关键设计决策

| 决策 | 选择 | 理由 |
|---|---|---|
| **技能根位置** | **`.dsh/skills/`（仓库根）** | 命中 DSH 的 `project-dsh` 发现根（rank 100）[E4] → **在仓库内工作时零安装生效**，契合 ClinPub "clone 即用"的形态；同一份目录又可被 v0.3 的 bundle 通过 `bundledSkillDir` 引用，**不必两处维护** |
| 共享核心是否复制 | **单份，`dsh/pipeline/` 唯一** | 避免 qoder 式的 references 分叉（每个技能各拷一份 → 5 处同步） |
| 技能正文引用风格 | 正文用**相对路径**引用 `dsh/pipeline/**` | DSH 技能结果会给出 base directory，相对路径可直接解析 [E6] |
| **平台形态** | **独立 Agent Preset（`clinpub`）**，不挂 standard preset [D1] | ① patch 是整份替换而非深合并，挂 standard 会在上游更新/用户装其他插件时被覆盖；② 450KB 临床提示词常驻会污染通用会话；③ 临床写作是有明确生命周期的 Task Domain，符合"启动 ClinPub 模式"的心智模型 |
| 角色卡归属 | 8 个 **Agent Preset**，persona 用 `dsh-persona` 的 `prefix`；角色卡**构建期内联**（不靠运行时读文件） [D7] | 子代理在首轮思考前必须已有角色约束，否则"逐字跳过加载"不可接受；构建期内联既保证 100% 生效，又保持源文件模块化 |
| 委派形态 | **8 个各自命名的委派工具**，每个固定绑定一个 `agentPreset`（**不**暴露 `agent_preset` 枚举） [D2] | 工具名与 description 直接进顶层索引，可发现性优于单工具枚举；参数在 schema 层隔离；`persona`/`toolFilter` 作为工具配置已废弃 [E15]，但「每工具钉一个 preset」合法（`agentPreset` 单独设置即可） |
| `do` / `next-step` 路由器 | **提示词技能为主**；`ctx.commands.register()` 仅用于纯 UI 操作 [D3] | ⚠️ 命令 handler 的返回值**按设计不进模型**（"without sending it to the model"），不能用来 push 工作流文本 [E12] |
| 工作流注入方式 | **构建期内联进 SKILL.md 正文**（push 确定性） [D3] | 技能被加载时正文**必然**进入上下文，等价 Claude Code 的 `!cat`；运行时读取依赖模型自觉，不可靠 |
| 阶段守卫 | **自写原生插件** `ctx.on('tools/pre-execute')` + 保留 `.clinpub/STATE.md` 契约 | 桥接包已移除 [E20]；原生插件用 `{kind:'deny', reason}` 返回原因（一等字段），且**不需要 bash/pwsh 双份**、无 matcher 大小写陷阱 [E22] |
| 并行委派 | 显式声明 `backgroundMode: continuable` + `enableRunInBackground` | 0.2.1 的 standard preset **移除了** `backgroundMode: continuable`，默认回到 `one-shot`（前台）；要 8 个 agent 并行必须自己写 [E25] |

> **⚠️ 重复发现注意**：由于 `.dsh/skills` 是 rank 100 的**项目根**，只要 DSH 的 cwd 在本仓库内，技能**已经**自动被发现。此时 bundle **不要再**声明 `bundledSkillDir` 指向同一目录，否则同一批技能会从两个提供方各出现一次。二选一：
> - **仓库内开发/使用** → 只靠 `.dsh/skills`（rank 100），bundle 不声明技能根；
> - **跨项目安装** → bundle 声明 `bundledSkillDir` 指向包内技能目录，并让用户**在其他项目目录**（非本仓库）工作。

---

## 5. 文件级映射表

### 5.1 目录结构

```
clinpub/
├── claude-code/          # 现有：Claude Code 插件
├── codex/                # 现有：Codex 插件
├── qoder/                # 现有：Qoder 插件
├── .dsh/                 # ★ 新增：DSH 技能根（rank 100，仓库内自动生效）
│   └── skills/                  # 必须是一层目录（不支持嵌套 **/SKILL.md）
│       ├── clinpub-overview/SKILL.md
│       ├── clinpub-data2idea/SKILL.md
│       ├── clinpub-initialize/SKILL.md
│       ├── clinpub-data-prep/SKILL.md
│       ├── clinpub-analysis/SKILL.md
│       ├── clinpub-writing/SKILL.md
│       ├── clinpub-improving/SKILL.md
│       ├── clinpub-coverletter/SKILL.md
│       ├── clinpub-review/SKILL.md
│       ├── clinpub-milestone/SKILL.md
│       ├── clinpub-modify/SKILL.md
│       ├── clinpub-do/SKILL.md
│       ├── clinpub-next-step/SKILL.md
│       └── clinpub-knowledge/SKILL.md     # 知识库入口（对齐 qoder「知识库」）
├── dsh/                  # ★ 新增：DSH 平台目录（bundle + 共享核心）
│   ├── package.json          # dsh.bundle.patch → cordis.patch.yml（v0.3）
│   ├── cordis.patch.yml      # 技能提供方 + 钩子桥接 + 8 个 Agent Preset + 委派白名单 + 真命令（v0.3）
│   ├── index.js              # 插件入口：apply(ctx, config)（v0.3）
│   ├── README.md             # 平台说明
│   ├── INSTALL.md            # 安装指南（含桌面版限制）
│   ├── pipeline/             # ★ 共享核心（单份）
│   │   ├── workflows/        # 12 个（原样）
│   │   ├── references/       # 16 个（原样）
│   │   └── templates/        # 19 个（原样）+ study_types/
│   ├── agents/               # ★ 8 份角色卡（原样，构建期内联进子 preset 的 persona）
│   ├── scripts/              # ★ 7 个 Python（原样）
│   └── index.js              # ★ 插件入口：tools/pre-execute 守卫（阶段/前置/注入扫描）
│                             #   注：claude-code 的 hooks/ 不复制过来——逻辑已并入 index.js
├── docs/
│   ├── MIGRATION-TO-DSH.md   # ★ 本文
│   └── ...
├── CHANGELOG.md              # 记 [Unreleased] — DeepSeek Harness
└── README.md                 # 平台表加一行
```

> **为什么技能根在 `.dsh/skills/` 而共享核心在 `dsh/`**：前者**必须**在仓库根的 `.dsh/` 下才能命中 rank 100 的项目级发现；后者是平台资产，与 `claude-code/`、`codex/`、`qoder/` 平级。技能正文用相对路径引用共享核心（如 `../../dsh/pipeline/workflows/analysis.md`），DSH 会用技能 base directory 解析 [E6]。
>
> ⚠️ **`.gitignore` 注意**：根 `.gitignore` 已忽略 `.qoder/` 和 `.claude/`（本地状态目录），**`.dsh/` 未被忽略** → 技能会正常进版本控制 ✅。但若将来 `.dsh/` 下出现本地状态（如缓存），需补忽略规则。

### 5.2 命令 → 技能映射（13 + 1）

| # | 源（`claude-code/commands/`） | 目标技能名 | 用户调用 | 阶段 |
|---|---|---|---|---|
| 1 | `overview.md` | `clinpub-overview` | `/clinpub-overview` | — |
| 2 | `data2idea.md` | `clinpub-data2idea` | `/clinpub-data2idea` | — |
| 3 | `initialize.md` | `clinpub-initialize` | `/clinpub-initialize` | 0 |
| 4 | `data-prep.md` | `clinpub-data-prep` | `/clinpub-data-prep` | 1 |
| 5 | `analysis.md` | `clinpub-analysis` | `/clinpub-analysis` | 2 |
| 6 | `writing.md` | `clinpub-writing` | `/clinpub-writing` | 3 |
| 7 | `improving.md` | `clinpub-improving` | `/clinpub-improving` | 工具 |
| 8 | `coverletter.md` | `clinpub-coverletter` | `/clinpub-coverletter` | 工具 |
| 9 | `review.md` | `clinpub-review` | `/clinpub-review` | 工具 |
| 10 | `milestone.md` | `clinpub-milestone` | `/clinpub-milestone` | 门控 |
| 11 | `modify.md` | `clinpub-modify` | `/clinpub-modify` | 工具 |
| 12 | `do.md` | `clinpub-do` | `/clinpub-do` | 路由 |
| 13 | `next-step.md` | `clinpub-next-step` | `/clinpub-next-step` | 推进 |
| 14 | —（qoder「知识库」对齐） | `clinpub-knowledge` | `/clinpub-knowledge` | 知识库 |

> Codex 侧的阶段0 技能名是 `clinpub-init`（见根 `README.md`）。DSH 统一用 `clinpub-initialize`，与 claude-code / qoder 对齐，并在 `dsh/README.md` 注明差异。

### 5.3 技能 → workflow 引用映射

| 技能 | 需引用的 workflow |
|---|---|
| `clinpub-initialize` | `init-project.md` + `import-project.md` |
| `clinpub-data-prep` | `data-prep.md` |
| `clinpub-analysis` | `analysis.md` |
| `clinpub-writing` | `writing.md` |
| `clinpub-improving` | `improving.md` |
| `clinpub-coverletter` | `coverletter.md` |
| `clinpub-review` | `review.md` |
| `clinpub-modify` | `modify.md` |
| `clinpub-milestone` | `milestone.md` |
| `clinpub-do` | `init-project` / `data-prep` / `analysis` / `writing` / `improving` / `coverletter` / `review` / `next-step` / `milestone` + `references/checkpoints.md` |
| `clinpub-next-step` | `next-step.md` |
| `clinpub-data2idea` | `data2idea.md` |
| `clinpub-knowledge` | 全部 16 份 `references/` + 19 份 `templates/` |

### 5.4 智能体 → Agent Preset 映射（8）

> **决策（D2）**：**8 个各自命名的委派工具**，每个通过 `agentPreset` **钉死**一个 preset，**不设** `allowedAgentPresets`，因此**不**暴露 `agent_preset` 枚举参数。
> 合法性依据：`agentPreset` 可单独设置；`allowedAgentPresets` 为 `undefined` 时构造器直接返回、不校验、`choices` 也为 `undefined` → 工具 schema 不出现该参数 [E15]。

| # | 角色卡 | Preset id | 工具名（模型可见） | 工具级 description 要点 |
|---|---|---|---|---|
| 1 | `analyst-agent.md` | `clinpub-analyst` | `clinpub_analyst` | 数据清洗、统计建模、出版级图表 |
| 2 | `reference-agent.md` | `clinpub-reference` | `clinpub_reference` | PubMed/NCBI 检索、引文核实 |
| 3 | `writer-agent.md` | `clinpub-writer` | `clinpub_writer` | IMRAD 撰写、图表整合 |
| 4 | `topic-miner-agent.md` | `clinpub-topic-miner` | `clinpub_topic_miner` | 数据画像→候选课题 |
| 5 | `clinpub-planner.md` | `clinpub-planner` | `clinpub_planner` | 波次依赖图规划 |
| 6 | `clinpub-executor.md` | `clinpub-executor` | `clinpub_executor` | 按计划执行、原子提交 |
| 7 | `clinpub-verifier.md` | `clinpub-verifier` | `clinpub_verifier` | 跨阶段验证（15 种模式） |
| 8 | `modify-agent.md` | `clinpub-modify` | `clinpub_modify` | 改图/改方法/加方法 |

**每个子 preset 需要自带的最小插件集**（子 preset **不继承**父 preset 的工具，必须各自声明）：

```yaml
- id: preset-clinpub-analyst
  name: '@deepseek-ai/dsh-agent-preset'
  config:
    id: clinpub-analyst
    name: ClinPub Analyst
    description: 数据清洗与统计分析（R 为主）
    plugins:
      - id: persona
        name: '@deepseek-ai/dsh-persona'
        config:
          # ★ 角色卡全文在【构建期】由生成脚本内联到这里，运行时不读文件
          prefix: |
            You are the ClinPub analyst agent. <analyst-agent.md 全文>
      - id: tool-fs
        name: '@deepseek-ai/dsh-tool-fs'
      - id: tool-fs-search
        name: '@deepseek-ai/dsh-tool-fs-search'
      - id: tool-pwsh
        name: '@deepseek-ai/dsh-tool-pwsh'
      - id: tool-todo
        name: '@deepseek-ai/dsh-tool-todo'
```

**父侧：8 个工具实例**（每个只钉一个 preset）：

```yaml
- id: tool-subagent-clinpub-analyst
  name: '@deepseek-ai/dsh-tool-subagent'
  config:
    provider: spawn                  # ⚠️ preset 选择仅 spawn 支持
    toolName: clinpub_analyst
    backgroundMode: continuable
    agentPreset: clinpub-analyst     # 单独设置即可，无需 allowedAgentPresets
    maxDepth: 1
# … 另外 7 个同理，各自不同 toolName + agentPreset
```

**为什么这样比单工具枚举可靠**（D2 结论）：

1. **可发现性**：8 个工具名 + description 直接进 Function Calling 顶层索引；单工具时 8 项能力全挤在一个 enum 的 description 里，受截断与注意力稀释影响。
2. **参数隔离**：每个工具是独立 schema（虽由 DSH 生成，参数集相同），但**在工具名层面就完成了分类**，模型不需要先解析枚举值再判断。
3. **错误回退**：调错时报错直接定位到具体工具名，模型有明确回退信号。

> **⚠️ 一条来自 Gemini 但**不成立**的论据**：它称"每个专用工具可定义专属入参 Schema（如必须包含 `raw_data_path`）"。
> DSH 的委派工具 schema 由 `dsh-tool-subagent` **固定生成**（`description` / `prompt` + 可选 `agent_preset`/`provider`/`model`/`run_in_background`），**不能**为每个实例自定义入参字段 [E15]。因此"参数校验"这条理由在 DSH 上**不适用**；选择 8 工具应基于「可发现性 + 错误定位」两条。

> **尚未验证**：8 个委派工具会让工具目录多出 7 份 schema，需实测 token 开销与选择准确率是否真的优于枚举。见 [§9.2](#92-需要实测验证实施前必做)。

---

## 6. 分阶段实施计划

> **统一原则（决策 D4）**：**从 v0.1 起所有产物就由同一个构建脚本生成**，严禁手写两套路径规则。
> 源文件（`claude-code/commands/*.md` + `pipeline/**` + `agents/**`）是唯一真源；DSH 产物是**编译输出**。
> 这样 v0.1 与 v0.3 之间只换输出目标，不换生成逻辑，彻底消除"两套目录最后分叉"的风险。

### v0.1 — 核心工作流内联化原型（单 preset，可跑通）

**目标**：在 DSH 里 `/clinpub-overview` 立刻可用，验证 450KB 提示词平移后的实际手感。

| 交付物 | 说明 |
|---|---|
| **`dsh/build.mjs`（构建脚本，约 200–300 行）** | 读源文件 → 生成 `SKILL.md`（工作流**内联进正文**）+ 生成 `cordis.patch.yml` |
| `.dsh/skills/**`（14 个技能，**生成物**） | 技能正文 = 命令模板 + 对应 workflow 全文**内联**（push 确定性，决策 D3） |
| `dsh/pipeline/**`、`dsh/scripts/**`、`dsh/agents/**` | 从 `claude-code/` 复制（源，不改内容） |
| `dsh/README.md` + `dsh/INSTALL.md` | 在仓库内工作时自动生效；跨项目需复制/软链到 `~/.agents/skills` |
| `dsh/clinpub.config.json`（或 `.mjs`） | **单一数据源**：命令清单、角色清单、工具集、阶段映射 |

**验收**：在 DSH 中打开本仓库，技能目录出现 14 个 `clinpub-*`；`/clinpub-overview` 输出命令参考；`/clinpub-analysis` 的正文里**确实包含** workflow 全文（不是一句"请去读某某文件"）。

**已知不足**：跨项目使用需手动安装；无阶段守卫；无命名智能体。

> **为什么 v0.1 就内联**：DSH 技能的 pull 语义（只给 base directory）会让"模型声称按流程执行但没读文件"成为可能。理论上可以用 `tools/pre-execute` 在工具调用前拦截，但**"模型有没有真的读过工作流"这件事本身无法可靠判定**（读文件只是众多前置动作之一）。内联是**唯一**能 100% 还原 Claude Code `!cat` 确定性的做法（见 D3）。

### v0.2 — 阶段守卫（自写原生插件）

> **⚠️ 0.2.1 起方案已变**：不再有 `hooks.json` 可桥接，也不再需要 `.ps1`。改为在 `dsh/index.js` 里直接监听 `tools/pre-execute`。

| 交付物 | 说明 |
|---|---|
| `dsh/index.js` 中的 `tools/pre-execute` 守卫 | 三合一：阶段目录守卫 + 前置条件检查 + 数据文件注入扫描；返回 `{kind:'deny', reason}` |
| `dsh/state.mjs`（阶段读取器） | 从 `.clinpub/STATE.md` 读 `阶段：Phase N`，兼容 `import_mode: true` 的两种分支；带缓存 |
| ~~`dsh/hooks/*.sh` / `*.js` / `hooks.json`~~ | **不再需要**——三份钩子脚本的逻辑并入插件 |
| `docs/MIGRATION-TO-DSH.md` 增补 | 记录原生守卫与旧钩子的行为对齐表 |

**验收**：越阶段写入被拒绝**且原因可读**（`reason` 直接显示）；`.clinpub/STATE.md` 的阶段行能被正确读取；`import_mode: true` 的两种分支（有效导入 / 崩溃残留）行为与 claude-code 版一致；**Windows/macOS/Linux 行为完全一致**（因为都是 JS，不再有 bash 依赖）。

### v0.3 — 模块化解耦与可分发 bundle

| 交付物 | 说明 |
|---|---|
| `dsh/package.json` + `dsh/cordis.patch.yml` + `dsh/index.js` | bundle 三件套 |
| **8 个 `dsh-agent-preset` 声明** | `clinpub-analyst` … `clinpub-modify`，每个自带内联 persona + 裁剪后的工具插件集，见 [§5.4](#54-智能体--agent-preset-映射8) |
| **8 个具名委派工具** | 每个固定绑定一个 `agentPreset`，**不**设 `allowedAgentPresets`（决策 D2） |
| `ctx.commands.register()` | **仅**用于纯 UI 操作（如 `/clinpub-status` 打印状态），**不**用于注入工作流文本 |
| `bundledSkillDir` 行 | 指向包内技能目录（**跨项目安装场景**；仓库内使用则省略，见 [§4.2](#42-关键设计决策) 的重复发现注意） |
| 构建流水线 | 单一数据源 → 生成 `SKILL.md` + `cordis.patch.yml`（决策 D4/D5） |
| 分发产物 | `pnpm pack` → `clinpub-dsh-<ver>.tgz` |

**验收**：`dsh plugin add ./clinpub-dsh-0.3.0.tgz`（或应用内插件管理器）安装后，在**任意**研究项目目录下 14 个技能均可用；8 个具名委派工具可见且各自 persona 正确；阶段守卫生效且原因可读。

---

## 7. 验收方案（真实临床项目试跑）

按用户选择：**在 DSH 里真跑一个临床研究项目**。

### 7.1 前置

- [ ] 补装 `ggsurvfit`：`Rscript -e 'install.packages("ggsurvfit")'`
- [ ] 准备一份**脱敏**患者级数据（每行一患者，每列一变量）
- [ ] 新建独立研究项目目录（**不要**建在 clinpub 仓库内，以真实检验跨项目安装）

### 7.2 试跑路线（阶段0 → 3）

| 阶段 | 使用的技能 | 通过标准 |
|---|---|---|
| 0 | `/clinpub-initialize` | 生成 `.clinpub/{PROJECT,ROADMAP,STATE}.md` + `project_config.yml`；**显式询问目标期刊**；IRB 门控签字 |
| 1 | `/clinpub-data-prep` | 生成 `02_PreprocessedData/data/cleaned.csv` + 数据质量报告；缺失率/样本量检查通过 |
| 2 | `/clinpub-analysis` | `04_Outputs/_figure_config.R` 存在且被**所有**方法脚本 `source()`；每方法产出图+表+方法说明；图 ≥300 DPI |
| 3 | `/clinpub-writing` | `05_Manuscript/manuscript.md` **单一文件**，IMRAD 完整，引用带 DOI |
| 门控 | `/clinpub-milestone` | 4 个门控（IRB / 数据质量 / 分析有效性 / 投稿准备）逐项签字 |
| 工具 | `/clinpub-improving` | 能自审 → 改稿 → 数值级联一致 |

### 7.3 平台特性专项验证

| # | 验证项 | 判定 |
|---|---|---|
| 1 | `/clinpub-*` 用户直调注入 | 输入 `/clinpub-overview` 即注入技能正文，模型无需再调 `skill` |
| 2 | 技能目录出现 14 项且描述 ≤500 字符 | 会话首条 `<available_skills>` 含全部 14 项 |
| 3 | 技能**一层发现**约束 | 把技能放嵌套目录 → 确认**不出现**（验证约束理解正确） |
| 4 | 阶段守卫（write/edit） | 在阶段1 写 `04_Outputs/` → 被拒绝**且原因可读** |
| 5 | 守卫的**跨平台一致** | 同一个 JS 守卫在 Windows（pwsh）/ macOS（bash）下行为完全一致 |
| 6 | 守卫的**工具名判定** | `exec.name === 'write' | 'edit'` 生效；确认 DSH 侧就是这两个小写名 |
| 7 | **8 个具名委派工具**可见 | 工具目录出现 `clinpub_analyst` … `clinpub_modify`；**不出现** `agent_preset` 参数（因为未设 `allowedAgentPresets`） |
| 8 | 每个工具确实绑到对应 preset | 调 `clinpub_analyst` 时子代理 persona 是分析角色、工具集受限；子代理**无**父对话上下文 |
| 8b | `persona`/`toolFilter` 废弃确认 | 在工具 config 里写 `persona` → **激活时报错**（验证 E15 仍成立） |
| 9 | 状态文件兼容 | 另三平台创建的既有项目，在 DSH 中能继续（`.clinpub/STATE.md` 兼容） |
| 10 | `backgroundMode` 行为 | 不显式设置时是 `one-shot`（阻塞等待）；显式设 `continuable` 后 8 个 agent 能并行 |
| 11 | **插件市场可见性**（若发布） | 加索引 URL 后能在 Web「发现」页搜到 ClinPub，`engines.dsh` 门禁生效 |

### 7.4 回滚

`dsh/` 是**纯新增目录**，不改动 `claude-code/` / `codex/` / `qoder/`。回滚 = 删除 `dsh/` + 卸载 bundle（`dsh plugin --profile <p> remove <pkg>`，或应用内插件管理器移除）。README / CHANGELOG / 平台表的改动单独 revert。

---

## 8. 风险与对策

| # | 风险 | 影响 | 对策 |
|---|---|---|---|
| 1 | **返工风险**：先迁移后改管线 | 14 个技能重译一遍 | 按 [§0](#0-与管线升级的关系先读这一段) 先定稿管线语义；至少先冻结「命令清单 + 阶段划分」 |
| **2** | **上游包突然消失**（0.2.0→0.2.1 直接删了整个 hooks 子系统） | 方案整段作废、返工 | **能自写就不依赖上游包**：守卫自写 `tools/pre-execute`、技能构建期内联；只依赖长期稳定的核心服务（skill/subagent/tools） |
| 3 | ~~**版本不一致**：桌面 0.2.1 与 PATH 上的 CLI 0.2.0 并存~~ | ✅ **已解决**（CLI 已升级到 0.2.1-rc.2） | 升级时注意：npm `latest` 滞后，须显式指定版本 |
| 4 | **桌面版无法用 CLI 装 bundle** | 安装文档写错 → 用户装不上 | `INSTALL.md` 明确：桌面版走应用内插件管理器 / 插件页；CLI 用于非 desktop profile |
| 5 | **patch 行覆盖语义** | 覆盖 `skill-filesystem` 行时丢掉其他键 | 覆盖时必须**重述整份 `config`**（不深合并） |
| 6 | **DSH 版本迭代快**（rc 阶段） | 契约变动 | 本文所有契约标注证据版本；**每个阶段开工前重跑 [§2.3](#23-版本复核021-相对-020) 的复核清单** |
| 7 | **子代理内是否有 `skill` 工具**（未验证） | 角色卡只能内联（80KB YAML）或倒退为整卡注入 | v0.3 前置验证；退路是 persona 内联角色卡（可行但臃肿） |
| 8 | bundle 在 Host 进程执行 JS | 分发的安全面 | 优先 tarball / 插件市场分发；声明 `engines.dsh`，避免用户为构建脚本授权 |
| 9 | Python 统计依赖缺失 | 若未来 Python 接管统计则阻塞 | 当前不影响（R 为主）；`INSTALL.md` 记录 DSH 随附 Python 的包清单 |
| 10 | 技能 description 500 字符上限 | 路由描述被截断 → 模型选错技能 | 改写时按 ≤500 字符精炼 description |
| 11 | **README 与 `lib/` 不一致**（`persona`/`toolFilter` 已废弃但 README 未更新） | 按文档写必然激活失败 | **以 `lib/` 为准**；E15 已记录；实现前对每个用到的包做一次代码级核对 |
| 12 | **自写守卫的注册泄漏** | 插件卸载后监听器仍挂着，重复拦截 | 全部走 `ctx.effect` / `ctx.on`（DSH 会自动清理）；不要用裸 `addListener` |
| 13 | **8 个 preset 的维护成本** | 每个子 preset 要重述工具插件集，DSH 升级时易漂移 | 用脚本从单一数据源生成 `cordis.patch.yml`，而不是手写 |
| 14 | **并行委派默认关闭**（0.2.1 移除了 `backgroundMode: continuable`） | 8 个 agent 退化为串行，耗时长 | 在 ClinPub preset 里显式 `backgroundMode: continuable` + `enableRunInBackground` |

---

## 9. 开放问题

> 原 9.1 的架构类问题已由 [§10 会审](#10-外部会审与裁决记录) 裁决（D1–D8），此处只保留**仍未决**与**待实测**项。

### 9.1 仍需用户决策

| # | 问题 | 状态 |
|---|---|---|
| 1 | 管线升级的具体范围与时间点？（决定 v0.1 何时启动） | **未决**——阻塞 v0.1 的内容定稿 |
| 2 | 命令数量是否变化（现 13 + 知识库 = 14）？ | **未决**——随管线升级 |
| 3 | 8 个智能体是否压缩到 5 个（D8 建议） | **未决**且需跨平台同步，见下 |
| 4 | 是否发布到 npm / **插件市场**，还是仅 tarball | **未决**——0.2.1 新增市场，是一个新选项 |

> **关于 D8（8→5 合并）的重要提醒**：
> ClinPub 四平台共享 `agents/` 角色卡。**在 DSH 上单方面合并 5 个会破坏"四平台语义等价"约定**。
> 因此这条必须作为**管线升级**的一部分统一决定，而不是 DSH 适配的局部优化。
> 另注：Gemini 提的 5 个角色（DataAnalyst / LitResearcher / ManuscriptWriter / ReviewerCompliance / Orchestrator）
> **未覆盖** `topic-miner`（data2idea）与 `modify`（modify）两个**用户可调用**入口——合并前需先决定它们归谁。

### 9.2 需要实测验证（实施前必做）

> **2026-10-17 更新**：第 1–3 项已改为读源码解决，结论见下，无需再跑。**真正需要跑一次的只剩第 9 项**。

| # | 待验证 | 状态 / 为什么重要 | 验证方法 |
|---|---|---|---|
| 1 | 守卫能否拿到写入路径 | ✅ **已确认**：`exec.arguments.file_path`，`write`/`edit` 同名 [E26] | 读 `dsh-tool-fs` 源码 |
| 2 | 守卫机制是否存在且可同步拒绝 | ✅ **已确认**：`ctx.tools.guard()`，返回字符串即拒绝 [E26] | 读 `dsh-tools` 源码 |
| 3 | 技能正文内联后，经 `skill` 工具加载是否被 `tool-result-pruner` 截断 | ⚠️ **仅在压缩触发后**发生（阈值 8192）[E17]；ClinPub 独立 preset 可调高或去掉该行 | 内联 >8192 字符技能，触发压缩后观察 |
| 4 | 项目根 `.dsh/skills` 与 `bundledSkillDir` 指向同一目录时是否**重复** | ⚠️ **会**——每挂一个 provider 就注册一次，两个 root 各扫描一遍；结论：**二选一，不要同时配** | 若要确认可两者都配数条目 |
| 5 | 8 个委派工具 vs 1 工具+枚举，模型实际选择准确率 | ⏳ 需数据 | 同任务集跑两组，对比选对率与 token 开销 |
| 6 | 应用内插件页能否装本地 bundle 到 desktop profile | ⏳ 需 GUI 操作 | 走插件页试一次 |
| 7 | 子代理是否继承父会话的修剪与压缩设置 | ⏳ | 委派长任务后观察子会话是否提前压缩 |
| 8 | 子 preset 挂 `skill-filesystem` 是否只对子作用域可见 | ⏳ 设计上应如此（preset 是独立组合） | 观察父会话目录是否被污染 |
| **9** | **`ctx.tools` 能否在 preset 级插件中注入 / 守卫是否对子代理生效** | ⏳ **唯一必须跑一次的项** | 写 5 行探针插件装进临时 profile，跑一次 headless 并观察日志 |

### 9.3 需要确认的语义细节

| # | 问题 |
|---|---|
| 1 | `bundledSkillDir` 是否支持相对路径 / `!!js` 表达式？ |
| 2 | 子 preset 的 `persona.prefix` 有无长度上限？（单个角色卡 5–15KB） |
| 3 | `PreToolUse` 的 `ask` 决策在 approval policy = `never` 时会怎样（直接拒绝还是放行）？ |
| 4 | YAML 锚点（`&`/`*`）能否在 DSH 的 patch 层里跨条目复用？——若不能，只能用 `cordis:group` 或代码生成 |

---

## 10. 外部会审与裁决记录

第二轮（2026-10-17）就 8 个迁移决策征询了外部模型意见。下表逐条裁决，**凡与本地源码证据冲突的，以证据为准**。

| 编号 | 议题 | 外部建议 | 裁决 | 依据 |
|---|---|---|---|---|
| **D1** | 平台形态 | 独立 Agent Preset | ✅ **采纳** | 理由成立；但补充：DSH **没有** `--preset` 也没有项目级 `.cordis.yml` 锁定 [E18]，真正的"一键进入模式"只能靠**独立 profile**（`dsh --profile clinpub`，实测 CLI 仅支持 `--profile`/`--patch`） |
| **D2** | 委派形态 | 8 个具名工具 > 单工具枚举 | ✅ **采纳** | 合法：`agentPreset` 可单独设置，不设 `allowedAgentPresets` 就不暴露枚举 [E15]。**但驳回其"专属入参 Schema"论据**——DSH 委派工具 schema 固定生成，无法自定义字段 [E15] |
| **D3** | push 确定性 | `commands.register` 为最优 | ❌ **驳回** | 命令 handler 返回值**按设计不进模型**（"without sending it to the model"）[E19]，无法 push 工作流文本。其"第二方案"（UserPromptSubmit 钩子 + additionalContext）在 **0.2.1 也随 hooks 子系统一起消失** [E20]。**内联进 SKILL.md 正文成为唯一可行路径**（技能加载时正文必进上下文，等价 `!cat`） |
| **D4** | 分期策略 | v0.1 就统一构建产物，禁止两套 | ✅ **采纳** | 与本文 §0 的返工担忧一致；但**修正其"必然分叉"论断**——两阶段技能格式完全相同，差异仅在**发现根**（rank 100 vs 600）与打包方式，故"统一生成"是收益而非必需 |
| **D5** | 投入时机 | 建 Core/Adapter 抽象层 + 构建期转译 + 版本锁死 | ✅ **采纳** | 但需注意成本：ClinPub 目前是**零构建**的纯文本项目，引入 Node 构建脚本是新增维护面。建议构建脚本保持**无第三方依赖**（仅 `node:fs`） |
| **D6** | 8 preset 维护 | YAML 锚点 / 代码生成 / 复合插件 | ⚠️ **部分采纳** | "代码生成"✅；"复合插件"✅（DSH 原生 `cordis:group`，见 standard preset 的 `delegation` 组 [E14]）；"YAML 锚点"❓**其示例结构不符合 DSH patch 格式**（patch 是顶层数组，没有 `presets:` 顶层键），锚点能否跨条目复用**未验证**，列为 §9.3-4 |
| **D7** | 角色卡注入 | 自定义 PersonaProvider 运行时注入 | ❌ **改为构建期内联** | 其反对 (b)「提示子代理去 load skill」的理由**完全成立**（首轮前角色未加载 = 失控）。但其 (c) 方案依赖一个**未验证**的运行时注入钩子，且在 rc 阶段 API 面前风险高。构建期内联同时满足「100% 在首轮前生效」与「源文件模块化」，且**零运行时 API 依赖** |
| **D8** | 8→5 合并 | 合并为 5 个 | ⏸ **暂缓** | 论证（并发冗余、主控上下文搬运、分发错误率）合理，但这是**跨四平台的管线决策**，且其方案遗漏 `topic-miner` / `modify` 两个用户入口。转 §9.1-3 |

> 本轮新增的证据 E17–E19 已并入 [§11 证据索引](#11-证据索引)。

---

## 11. 证据索引

| 编号 | 证据 | 来源 |
|---|---|---|
| E1 | 仓库结构、平台版本、git 状态 | 本仓库实测（`git log` / `git status` / 目录清点） |
| E2 | R 4.4.3 + 740 包（缺 `ggsurvfit`）；Python 3.12.3 / DSH 随附 3.12.14 | 本机 `Rscript` / `python` 实测 |
| E3 | 技能格式、发现根与 rank、一层发现约束、`disable-model-invocation`/`user-invocable`、无 `allowed-tools` | `@deepseek-ai/dsh-skill-filesystem` README（asar 内 `/dsh/node_modules/`） |
| E4 | 本地发现优先级表（rank 100/200/300/400/500/600）、`bundledSkillDir`、`DSH_BUNDLED_SKILL_DIR` | [DSH 参考：Skills 子系统](https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/skills) |
| E5 | 技能名强制 kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`、摘要 500 字符上限 | E4 同页 |
| E6 | `skill` 工具、`/name` 用户直调、`<skill_resources>` base directory 指引 | `@deepseek-ai/dsh-tool-skill` README；E4 同页 |
| E7 | `dsh-tool-subagent` 的 `toolName`、`maxDepth` 默认 1、`spawn` 无父上下文（README 层面） | `@deepseek-ai/dsh-tool-subagent` README（asar 内） |
| E8 | `maxActiveSubagents` 默认 8 | `@deepseek-ai/dsh-subagent` README（asar 内） |
| **E9** | ~~桥接的 7 个事件、`additionalContext` 被忽略、matcher 规则~~ **⚠️ 已作废：该包在 0.2.1 被移除**（见 E20）。仅留作历史记录：`PreToolUse` 的 `additionalContext` 会被忽略 | `@deepseek-ai/dsh-hooks-claude-code` README（**0.2.0-rc.2** asar 内） |
| E10 | bundle 清单、`dsh plugin add`（目录/github/tgz）、加载层顺序、patch 整份替换 config | [打包与安装插件](https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish) |
| E11 | `dsh plugin --profile desktop` 被拒（profile 由 Electron 应用独占） | 本机 `dsh plugin --profile desktop --help` 实测 |
| E12 | `ctx.commands.register(CommandDefinition)`：插件可注册真斜杠命令；**handler 返回值渲染给 UI，不进入模型上下文**（"without sending it to the model"） | [DSH 参考：用户命令子系统](https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/commands) + `dsh-commands/lib/index.js` |
| E13 | DSH 0.2.0-rc.2 随附 **289** 个 `@deepseek-ai/*` 包全清单 | asar 索引解析（清单导出为 `dsh-packages.md`，存于仓库外同级 `clinpub-dsh-migration-probe/`） |
| E14 | 标准 preset 组合（工具行、委派组、`tool-bash` 在 Windows 禁用、`compaction` 组含 pruner） | `@deepseek-ai/dsh-web-app/presets/standard.patch.yml`（asar 内） |
| **E15** | **`persona`/`toolFilter` 作为工具 config 已移除，配置即抛错；替代方案是 `agentPreset` + `allowedAgentPresets`（后者生成工具 schema 的 `agent_preset` 枚举），仅 `spawn` 提供方支持；`agentPreset` 可单独设置且不暴露枚举** | `@deepseek-ai/dsh-tool-subagent/lib/index.js`（asar 内，`apply()` 的字段校验与 `SubagentPresetSelection.resolve()`）——**与同包 README 矛盾，以代码为准** |
| **E16** | ~~退出码 2 以 stderr 作为阻塞原因~~ **⚠️ 已作废：`dsh-hook-protocol` 在 0.2.1 被移除**（见 E20） | `@deepseek-ai/dsh-hook-protocol` README（**0.2.0-rc.2** asar 内） |
| **E17** | `tool-result-pruner` 默认 8192/4096/1024，**仅在压缩触发后**修剪；低于压力不修剪任何内容 | `@deepseek-ai/dsh-compaction-tool-result-pruner` README（asar 内） |
| **E18** | CLI 只有 `--profile` / `--patch` / `--from-default-profile` / `--dump-*`，**无 `--preset`**；profile 位于 `$DSH_HOME/profiles/<name>` | 本机 `dsh --help` 实测 |
| **E19** | 命令 handler 的 `CommandResult` 渲染给 UI，**不进入模型上下文** | `dsh-commands/lib/index.js` + 官方 commands 子系统页 |
| **E20** | **0.2.1-rc.2 移除了整个 hooks 子系统**：`dsh-hooks-claude-code` / `dsh-hooks-codex` / `dsh-hook-protocol` / `dsh-webhook` / `dsh-webhook-github` 均不在随附包内；包总数 289 → **306**；桌面版 `desktopVersion` = `0.2.1-rc.2`。**升级前** PATH 上的 `dsh` CLI 为 `0.2.0-rc.2`，已于 2026-10-17 升级对齐（npm `latest` 标签仍滞后于 `next`） | asar 索引解析 + `runtime.json` + `dsh --version` 实测 |
| **E21** | 扩展点事件**仍然存在**：`tools/pre-execute`(35) / `tools/post-execute`(37) / `agent/pre-step`(63) / `agent/turn-stopping`(11) / `subagent/start`(17)；仅桥接包被移除 | 对 0.2.1 asar 做全量字节搜索 |
| **E22** | `tools/pre-execute` 监听器形状：`ctx.on('tools/pre-execute', async (exec, next) => …)`；返回 `next()` 放行、`{ kind: 'deny', reason }` 拒绝、`{ kind: 'cancel' }` 取消；`exec` 带 `agent` / `name` / `signal` / `parent` | `dsh-experimental-auto-review/lib/index.js` 与 `dsh-workspace-changes/lib/index.js`（0.2.1 asar 内） |
| **E23** | 插件市场：`dsh-plugin-market` + `dsh-plugin-market-index` + Web「发现」页 + `plugin_market` 工具；索引源由用户配置（默认空），安装仍走 `pluginManager.installBundle` | `@deepseek-ai/dsh-plugin-market` README（0.2.1 asar 内） |
| **E24** | 安装前校验 `engines.dsh`；不满足则**不下载、不执行构建脚本**即失败；`compatibility.json` 可逐 `name@version` 豁免；`install_bundle` 要求 `danger-full-access` 或逐次批准 | `@deepseek-ai/dsh-plugin-manager` README（0.2.1 asar 内） |
| **E25** | 0.2.1 标准 preset 变化：新增 `time-context` / `tool-schedule` / `tool-plugin-market`(禁用)；移除 `tool-subagent-codex` / `tool-subagent-claude-code` / `tool-ralph`；**移除 `backgroundMode: continuable`**（默认回 `one-shot`）；`persona` 只剩 `prefix` | `@deepseek-ai/dsh-web-app/presets/standard.patch.yml`（0.2.1 asar 内） |
| **E26** | **`ctx.tools.guard(guard)` 存在**：位于 `tools/pre-execute` 之后的**同步**守卫，返回字符串即拒绝，且不能被其他守卫强制放行；`agent.ctx` 注册的守卫只作用于该 agent。**`exec` 携带 `arguments`**（源码 `snapshotJsonValue(exec.arguments)`），`write`/`edit` 的参数名均为 **`file_path`** | `@deepseek-ai/dsh-tools/lib/index.js` + `dsh-tool-fs/lib/index.js`（0.2.1 asar 内） |

> **证据版本说明**：
> - **E3–E19** 采集于 DSH **0.2.0-rc.2**（E9 / E16 已在 0.2.1 作废）
> - **E20–E25** 采集于 DSH **0.2.1-rc.2**
> - **E15 / E17** 已在 0.2.1 复核，结论不变（`dsh-tool-subagent` 字节完全一致）
>
> **⚠️ E7 与 E15 的冲突**：`dsh-tool-subagent` 的 README 仍写支持 `persona`/`toolFilter`，但源码会抛错。凡是「README 与 `lib/` 冲突」的地方，**以 `lib/` 为准**——这是本次调研最值得记住的一条方法论。
>
> **⚠️ 版本漂移是最大风险**：从 0.2.0 → 0.2.1 一个 rc 版本就移除了整个 hooks 子系统。**任何"直接复用上游包"的方案都必须假定它下个版本可能消失**；能自写就不要依赖，这也是 [D3](#10-外部会审与裁决记录) 选择"构建期内联"而非"运行时读取"的同一逻辑。

---

## 12. 附录：待补装的依赖

```r
# R —— 本机唯一缺失
install.packages("ggsurvfit")
```

```powershell
# 验证 DSH 运行时 Python 的包（记录进 dsh/INSTALL.md）
# 注意：运行时不在安装目录下，而在 ~/.dsh/dsh-runtimes/ 下（由 load_workspace_dependencies 解析）
$py = "$env:USERPROFILE\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
& $py -c "import numpy, pandas, openpyxl, requests; print('ok')"
& $py -c "import importlib.util as u; print([m for m in ['scipy','statsmodels','lifelines','matplotlib','sklearn'] if u.find_spec(m)])"
```

DSH 随附 Python 3.12.14 已含：`numpy` `pandas` `openpyxl` `requests` `Pillow` `python-docx` `python-pptx` `lxml` `XlsxWriter`
**不含**：`scipy` `statsmodels` `lifelines` `matplotlib` `sklearn`
