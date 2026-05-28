# Roadmap: clinpub

**6 phases** | **17 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | 工作量 |
|---|-------|------|-------------|--------|
| 1 | Bug Fixes | ✅ Complete | 2026-05-05 | |
| 2 | 断点续做 | ✅ Complete | 2026-05-05 | |
| 3 | 手稿拼接+引用策略 | ✅ Complete | 2026-05-11 | 大 |
| 4 | 方法增强 | ✅ Complete | 2026-05-07 | |
| 5 | Phase 前调研流程 | ✅ Complete | 2026-05-11 | |
| 6 | 图表+文档优化 | 图表质量 + WAVE 说明中文/改名 | CHART-01, DOC-01, DOC-02 | 小 |

---

## Phase Details

**Phase 1: Bug Fixes**
Goal: 修复影响基础可用性的两个 bug
Requirements: BUG-01, BUG-02
Success criteria:
1. Hook 正则在 STATE.md 写 `- 阶段：Phase N` 时正确识别，不回退到 Phase 0
2. 用户修改清洗数据需求时，Phase 1 所有关联文件（profile、spec 等）自动联动更新
**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md — BUG-01: Hook 正则修复（STATE.md 标识行 + getCurrentPhase() 新正则）
- [x] 01-02-PLAN.md — BUG-02: 数据联动更新（data-prep 重新进入检测 + 工作流刷新步骤）

**Phase 2: 断点续做**
Goal: 支持工作中断后恢复，无需从头摸索上下文
Requirements: NEXT-01, NEXT-02, NEXT-03
Success criteria:
1. `/clinpub-do` 读取工作区状态（STATE.md 和当前文件结构），自动路由到合适的命令
2. `/clinpub-next-step` 自动推进到下一 Phase 或 Wave
3. Phase/Wave 结束时自动提示 clear 并输出下一步提示
**Plans:** 2 plans

Plans:
- [x] 02-01-PLAN.md — `/clinpub-do` 命令：工作区状态自动检测 + NL 意图路由
- [x] 02-02-PLAN.md — `/clinpub-next-step` 命令 + clear 提示标准化

**Phase 3: 手稿拼接**
Goal: IMRAD 各段独立撰写引用后拼接为终稿 + 引用策略标准化
Requirements: WRITE-01, WRITE-02, CITE-01, CITE-02
Success criteria:
1. Introduction/Methods/Results/Discussion 各段独立完成引用和撰写
2. 终稿由各段拼接生成，非重写
3. 引用在合并时统一整理，不重复不遗漏
4. 默认引用策略 30-55 篇范围，分段建议+总量兜底
5. 开始撰写前与用户讨论各段引用数量、时间范围、IF 偏好
**Plans:** 5 plans

Plans:
- [x] 03-01-PLAN.md — 分段撰写流程改造: workflow 改造为逐段顺序撰写 + reference-agent 预搜索 + 用户审阅 pause
- [x] 03-02-PLAN.md — 引用管理与交叉引用: shared reference library JSON schema + placeholder 约定 + 去重规则
- [x] 03-03-PLAN.md — 终稿拼接输出: 7 步拼接协议（段落合并 + 占位符替换 + 引用统一编号 + YAML frontmatter + MANIFEST.yaml）
- [x] 03-04-PLAN.md — 命令入口适配: 更新 commands/clinpub/writing.md 描述和引用
- [x] 03-05-PLAN.md — 引用策略标准化: 策略参考文档 + writing workflow 插入讨论步 + reference-agent 搜索支持 IF/年份过滤

**Phase 4: 方法增强**
Goal: 处理未知方法和标准组间对比
Requirements: METH-01, METH-02
Success criteria:
1. 用户提到未知统计方法时自动搜索，总结后与用户讨论
2. 组间对比自动按组数选择标准检验 → 输出到分析报告中
**Plans:** 2 plans

Plans:
- [x] 04-01-PLAN.md — 组间对比方法决策树文档（comparison-methods.md），覆盖 2组/3+组×连续/分类+配对 全覆盖 + 效应量标准
- [x] 04-02-PLAN.md — reference-agent method_search 未知方法搜索模式 + 分析工作流集成

**Phase 5: Phase 前调研流程**
Goal: 调研→建议→讨论→执行 的标准化流程
Requirements: FLOW-01
Success criteria:
1. 每个 Phase 前自动调研相关领域和技术方案
2. 以建议方式与用户讨论，收集反馈后再执行
**Plans:** 2 plans

Plans:
- [x] 05-01-PLAN.md — 创建 pre-phase-research.md 参考文档（轨道选择、Track A/B 协议、RESEARCH.md 模板）
- [x] 05-02-PLAN.md — 扩展 reference-agent 添加 phase_research 模式

**Phase 6: 图表+文档优化** ✅ Complete (2026-05-28)
Goal: 图表美观 + 文档中文本地化
Requirements: CHART-01, DOC-01, DOC-02
Success criteria:
1. 图表参考优质案例优化，统一风格
2. WAVE 下 README 全部为中文，改名为"方法说明"

Plans:
- [x] 06-01-PLAN.md — R 可视化规范升级（theme_pub() 优化 + KM 曲线 + 热图 + 字体规范）
- [x] 06-02-PLAN.md — 文档中文本地化（方法说明模板 + 6 个管线文档更新）

---

## Requirement Mapping Validation

| Category | Count | Mapped | Unmapped |
|----------|-------|--------|----------|
| Bug Fixes | 2 | 2 (Phase 1) | 0 ✓ |
| 断点续做 | 3 | 3 (Phase 2) | 0 ✓ |
| 手稿拼接 | 4 | 4 (Phase 3) | 0 ✓ |
| 方法增强 | 2 | 2 (Phase 4) | 0 ✓ |
| Phase 前调研 | 1 | 1 (Phase 5) | 0 ✓ |
| 图表+文档 | 3 | 3 (Phase 6) | 0 ✓ |
| **Total** | **15** | **15** | **0 ✓** |

## Phases

```mermaid
flowchart LR
    P1[Phase 1: Bug Fixes] --> P2[Phase 2: 断点续做]
    P2 --> P3[Phase 3: 手稿拼接+引用策略]
    P3 --> P4[Phase 4: 方法增强]
    P4 --> P5[Phase 5: Phase前调研]
    P5 --> P6[Phase 6: 图表+文档优化]
```

---
*Roadmap created: 2026-05-05*
