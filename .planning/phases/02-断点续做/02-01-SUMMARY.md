---
phase: 02-断点续做
plan: 01
status: complete
created: 2026-05-05
---

# Plan 02-01 SUMMARY: `/clinpub-do` 命令

## 目标
创建 `/clinpub-do` 命令入口，实现工作区状态自动检测 + NL 意图路由。

## 关键交付
- `commands/clinpub/do.md` — 完整的路由命令入口

## 实现内容
1. **frontmatter**: 命令名称 `clnpub:do`，支持可选 NL 参数
2. **objective**: 定义 D-01~D-04 四种行为模式（无参、有 NL、三合一路由、NL 回退）
3. **interfaces**: STATE.md Phase 解析正则 + 各 Phase 工件检测模式
4. **execution_context**: 引用所有路由目标命令
5. **process**:
   - 参数解析 + NL 意图推断规则（7 组优先级排序的关键词映射）
   - 命令名称映射表（Phase 0-4 + next-step + milestone）
   - 无参行为状态检测（STATE.md 读取 + 工件检测 + 路由决策树）
   - 输出格式规范（统一模板）
   - 用户确认流程（路由后不自动执行）
6. **success_criteria**: 8 个命令路由完整 + NL 回退逻辑

## 关键决策引用
- D-01: 无参 → 状态摘要 + 建议
- D-02: NL 优先于状态
- D-03: 三合一路由
- D-04: NL 推断失败回退到无参

## 自检
- [x] `grep -c "name: clinpub:do"` = 1
- [x] NL 意图关键词表包含 7+1 组（含第 7 组回退）
- [x] 8 个命令路由映射完整
- [x] D-01~D-04 全部引用

## Self-Check: PASSED
