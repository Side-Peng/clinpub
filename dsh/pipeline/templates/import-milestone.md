# Milestone: Import — 项目导入

**导入日期**: {{date}}
**导入模式**: {{import_mode}}  <!-- 中途接入（跳过 Phase X-Y） -->
**起始 Phase**: Phase {{starting_phase}} — {{starting_phase_name}}

## 导入文件清单

| # | 来源文件 | 目标位置 | 角色 | 状态 |
|---|---------|---------|------|------|
{{imported_files}}

## 跳过的 Phase 及 Gate 状态

{{skipped_phases_summary}}

### Gate 详细检查

{{gate_check_details}}

**状态说明**:
- ✅ `PASS` — 已验证通过（导入文件满足检查项）
- ⚠️ `UNVERIFIED` — 无法验证（导入项目中无对应产物）
- ❌ `FAIL` — 验证失败（导入文件不满足要求，阻断导入）

## 差距与补做计划

| 缺失项 | 所属 Phase | 补做建议 | 优先级 | 阻断后续? |
|--------|-----------|---------|--------|----------|
{{gap_remediation_plan}}

**优先级说明**:
- `必需` — 必须在后续 Gate 检查前补做，否则阻断
- `建议` — 强烈建议补做，但不阻断流程启动
- `可选` — 补做可提升质量，不阻断

## 用户签字

- [ ] 我确认文件映射正确，已导入的文件在正确位置
- [ ] 我了解跳过的 Gate 中 `UNVERIFIED` 项的风险
- [ ] 我已提供 IRB/伦理审批信息（Gate 1 不可跳过）
- [ ] 我同意从 Phase {{starting_phase}} — {{starting_phase_name}} 开始

**备注**:

---

## 下一步

**Phase {{starting_phase}}**: {{starting_phase_name}}
**目标**: {{next_phase_goal}}

待办事项（含补做项）:
{{next_steps}}
