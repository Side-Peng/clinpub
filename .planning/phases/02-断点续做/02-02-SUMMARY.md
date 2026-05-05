---
phase: 02-断点续做
plan: 02
status: complete
created: 2026-05-05
---

# Plan 02-02 SUMMARY: `/clinpub-next-step` + clear 提示标准化

## 目标
创建 `/clinpub-next-step` 命+ 标准化 clear 提示格式，更新 STATE.md 的「下一步」节。

## 关键交付
- `commands/clinpub/next-step.md` — 完整的推进命令入口
- `.planning/STATE.md` — 标准化的「下一步」节（三要素格式）

## 实现内容
1. **next-step.md**:
   - frontmatter + objective（D-05~D-07 行为模式）
   - interfaces（Phase 正则、Plan checkbox 读取、Wave 进度读取）
   - process:
     - 读取当前状态（STATE.md Phase + ROADMAP.md checkboxes + project_config.yml waves）
     - 完成验证（Phase 0-4 各阶段工件检测）
     - 推进决策（粒度自动判断：Wave vs Phase）
     - MILESTONE.md 生成（Pitfall 4 规避）
     - Clear 提示输出（D-08/D-09 三要素格式）
   - success_criteria
2. **STATE.md**:
   - 「下一步」节标准化为三要素格式：`/clear` + 建议命令 + 进度总结

## 关键决策引用
- D-05: 粒度自动判断
- D-06: 完成验证
- D-07: 检查点（MILESTONE.md）
- D-08: 统一输出
- D-09: 三要素提示

## 自检
- [x] `grep -c "name: clinpub:next-step"` = 1
- [x] D-05~D-09 全部引用
- [x] 5 个 process 小节完整
- [x] MILESTONE.md 引用 11 处
- [x] STATE.md「下一步」无代码块，有三要素

## Self-Check: PASSED
