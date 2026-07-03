# ClinPub — 临床研究发表管线

端到端临床数据分析与 SCI 发表管线，覆盖从原始数据到论文投稿的完整流程。

> End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals.

## 平台版本

本仓库包含 ClinPub 在多个 AI 编码平台上的适配版本，各版本共享相同的方法论和流程设计，按平台特性独立实现。

| 平台 | 目录 | 状态 | 安装方式 |
|------|------|------|----------|
| [Claude Code](claude-code/) | `claude-code/` | v2.2.0 稳定版 | `claude --plugin-dir ./claude-code` 或 marketplace |
| [QoderWork](qoder/) | `qoder/` | v1.0.0 首发版 | 复制到 `~/.qoderworkcn/plugins-custom/clinpub` |
| [Codex](codex/) | `codex/` | 计划中 | — |

## 管线概览

```
Phase 0          Phase 1         Phase 2           Phase 3         Phase 4
项目初始化  →  数据清洗  →  统计分析  →  论文写作  →  同行评审
                ↓              ↓               ↓
            cleaned.csv    图表+表格     manuscript.md
```

核心能力：

- **12+ 统计方法**：基线表、组间比较、回归、生存分析、ROC、LASSO、PSM、RCS、MICE、中介/调节、聚类等
- **5 种研究类型**：RCT、队列、病例对照、横断面、描述性
- **双模式写作**：一键成稿 / 逐步写作，内置反 AI 写作规则
- **PubMed 内置检索**：文献搜索、引用管理、Vancouver 格式输出
- **出版级输出**：≥300 DPI 图表、可配置主题/配色、CONSORT/STROBE/PRISMA 规范

## 快速开始

### Claude Code

```bash
# 开发模式
claude --plugin-dir ./claude-code

# Marketplace
claude plugin install clinpub
```

详见 [claude-code/INSTALL.md](claude-code/INSTALL.md)

### QoderWork

```bash
# 将 qoder/ 目录复制到插件目录
cp -r qoder/ ~/.qoderworkcn/plugins-custom/clinpub
```

安装后在对话中 `@编排器` 启动项目，或 `@项目初始化` 开始新项目。

## 项目结构

```
clinpub/
├── claude-code/    # Claude Code 插件（.claude-plugin 格式）
├── qoder/          # QoderWork 插件（.qoder-plugin 格式）
├── codex/          # Codex 适配（计划中）
├── docs/           # 通用开发文档
└── CHANGELOG.md    # 版本历史
```

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)

## 贡献

各平台版本的贡献指南见对应目录：

- [Claude Code 贡献指南](claude-code/CONTRIBUTING.md)
- Qoder / Codex 版本遵循相同的代码独立原则

## License

MIT
