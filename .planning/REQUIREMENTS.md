# Requirements: clinpub

**Defined:** 2026-05-05
**Core Value:** 用户提供原始临床数据，clinpub 输出结构化的分析结果和可投稿的 IMRAD 手稿

## v1 Requirements

### Bug Fixes

- [ ] **BUG-01**: Hook 正则 `当前.*Phase` 改为匹配 STATE.md 的 `- 阶段：` 格式，避免回退到 Phase 0
- [ ] **BUG-02**: 用户要求修改清洗数据时，全面检查 Phase 1 所有受影响文件（profile、spec 等）联动更新

### 断点续做

- [ ] **NEXT-01**: 添加 `/clinpub-do` 命令，读取工作区状态自动路由到合适的命令
- [ ] **NEXT-02**: 添加 `/clinpub-next-step` 命令，自动推进到下一 Phase 或 Wave
- [ ] **NEXT-03**: Phase 和 Wave 结束时自动提示 `clear` 压缩上下文，然后进入下一阶段

### 手稿拼接

- [ ] **WRITE-01**: IMRAD 各段（Introduction/Methods/Results/Discussion）独立撰写，各自完成引用
- [ ] **WRITE-02**: 终稿由各段拼接而成，非重写，引用在合并时统一整理

### 未知方法处理

- [ ] **METH-01**: 用户提到未知统计方法时，自动搜索资料总结后再与用户讨论
- [ ] **METH-02**: 组间对比方法固化：两组（连续 t检验/分类 卡方），三组（连续 ANOVA+校正/分类 卡方）

### Phase 前调研

- [ ] **FLOW-01**: 每个 Phase 前先调研，以建议方式与用户讨论，结合用户反馈再执行

### 引用策略

- [ ] **CITE-01**: 默认引用约 50 篇、近 5 年文献
- [ ] **CITE-02**: 引用前与用户讨论各部分引用数量、时间范围、影响因子偏好

### 图表优化

- [ ] **CHART-01**: 参考优质图表技能案例，优化作图质量

### 文档本地化

- [ ] **DOC-01**: WAVE 下的 README 使用中文撰写
- [ ] **DOC-02**: WAVE 下的 README 改名为"方法说明"

## v2 Requirements

- **npm 发布**: 待私测满意后再发版
- **自动化测试**: 纯开发环境，开发者自行处理

## Out of Scope

| Feature | Reason |
|---------|--------|
| npm 包发布 | 私测满意后再发版，不设时间线 |
| 自动化单元测试 | 纯开发环境，开发者自行测试 |
| CI/CD 测试流水线 | 同上，已删除 `.github/workflows/test.yml` |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BUG-01 | Phase 1 | Pending |
| BUG-02 | Phase 1 | Pending |
| NEXT-01 | Phase 2 | Pending |
| NEXT-02 | Phase 2 | Pending |
| NEXT-03 | Phase 2 | Pending |
| WRITE-01 | Phase 3 | Pending |
| WRITE-02 | Phase 3 | Pending |
| METH-01 | Phase 4 | Pending |
| METH-02 | Phase 4 | Pending |
| FLOW-01 | Phase 5 | Pending |
| CITE-01 | Phase 6 | Pending |
| CITE-02 | Phase 6 | Pending |
| CHART-01 | Phase 7 | Pending |
| DOC-01 | Phase 7 | Pending |
| DOC-02 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-05*
*Last updated: 2026-05-05 after initial definition*
