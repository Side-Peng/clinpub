# Checkpoint & Milestone Protocol

## 设计原则

- **Claude 自动完成一切可自动化的工作** — checkpoint 仅用于验证和决策，不做手动操作
- **每个 checkpoint 必须有明确的恢复信号** — user 输入 approved/continue 即可继续
- **每个 milestone 必须有完整的成功标准验证** — 不满足不可进入下一 Phase
- **所有状态持久化** — checkpoint/milestone 记录写入 `.clinpub/`

## Checkpoint 类型

### 1. `decision` — 用户决策点

当分析路径有分支时（如缺失值策略、方法选择），需要用户做决策。

```xml
<checkpoint type="decision" gate="blocking">
  <context>Phase 1 — 缺失值处理策略</context>
  <question>变量 XXX 缺失率 25%，如何处理？</question>
  <options>
    - A: 删除该变量（推荐，因缺失率过高）
    - B: MICE 插补（需验证插补合理性）
    - C: 转为分类（缺失作为单独类别）
  </options>
  <recommendation>A — 缺失率 >20% 通常不适合插补</recommendation>
  <resume_signal>输入 A/B/C 选择</resume_signal>
</checkpoint>
```

### 2. `verify` — 验证确认点

当自动步骤完成后，需要用户确认结果是否符合预期。

```xml
<checkpoint type="verify" gate="blocking">
  <context>Phase 1 — 数据清洗完成</context>
  <summary>
    - 原始数据: 500 行 × 30 列
    - 清洗后: 485 行 × 32 列
    - 缺失处理: 3 个变量 MICE 插补，1 个变量删除
    - 异常值: 5 个超出 3×IQR，已 winsorize
  </summary>
  <review_artifacts>
    - 02_PreprocessedData/reports/data_quality.html
    - 02_PreprocessedData/data/cleaned.csv
  </review_artifacts>
  <resume_signal>输入 approved 继续，或描述需要调整的地方</resume_signal>
</checkpoint>
```

### 3. `milestone` — Phase 关卡评审

Phase 完成时，正式验证所有成功标准并记录。

```xml
<milestone gate="blocking">
  <phase>1 — data-prep</phase>
  <status>complete</status>
  <verification>
    - [x] cleaned.csv 存在于 02_PreprocessedData/data/
    - [x] 数据质量报告已生成
    - [x] 缺失值已按策略处理
    - [x] 异常值已记录
    - [x] 衍生变量已创建
    - [x] 清洗代码可独立复现
  </verification>
  <decisions>
    | Decision | Choice | Rationale |
    |----------|--------|-----------|
    | 缺失值策略 | MICE 插补 (m=5) | 5-20% 缺失率 |
    | 异常值处理 | Winsorize 1%/99% | 保留样本量 |
  </decisions>
  <signoff>用户确认 → 进入 Phase 2</signoff>
</milestone>
```

## Milestone 记录格式

每次 Phase 完成时，写入 `.clinpub/phases/NN-phase-name/MILESTONE.md`：

```markdown
# Milestone: Phase N — [Name]

**完成日期**: YYYY-MM-DD
**状态**: ✅ Complete / ⚠️ Partial

## 交付物清单
- [x] deliverable 1
- [x] deliverable 2

## 关键决策
| 决策 | 选择 | 理由 |
|------|------|------|
| ... | ... | ... |

## 产出文件
- path/to/output
- path/to/output

## 未解决问题
- 无

## 用户签字
- [x] 用户确认进入 Phase N+1

## 下一步
Phase N+1: [name] — [目标简述]
```

## 流程集成

每个 Phase Workflow 末尾自动执行 milestone 检查：

1. 运行成功标准验证清单
2. 汇总关键决策和产出
3. 生成 MILESTONE.md
4. 更新 ROADMAP.md 状态为 complete
5. 等待用户签字放行
6. 签字后更新 STATE.md 指向下一 Phase
