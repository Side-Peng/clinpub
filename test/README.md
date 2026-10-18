# ClinPub 3.0 验证测试

> 目的：用一份合成数据跑通 Phase 0 → 3，验证 3.0 的**迭代分析**与**递进写作**是否真的按设计工作。
>
> ⚠️ **本目录就是项目根**。所有管线产物（`.clinpub/`、`01_RawData/`、`04_Outputs/`、`05_Manuscript/`）都落在 `test/` 下，
> 不是仓库根。运行管线时请把 `test/` 当作工作目录。

## 数据

- `data/patients.csv` —— 120 例 × 11 列，合成数据，含预埋信号与约 8% 缺失
- `data/DATA_DICTIONARY.md` —— 变量字典与"预埋特征"说明

> 数据放在 `data/` 而不是 `01_RawData/`：根 `.gitignore` 会忽略任何 `01_RawData/`（保护真实患者数据），
> 而这份合成数据需要入库。Phase 0 时应把它复制进 `01_RawData/`。

## 测试路线

### Phase 0 — 初始化

```
/clinpub-initialize
```

预期：

- [ ] **显式询问目标期刊**（不预设）
- [ ] 询问研究类型（RCT / 队列 / 病例对照 / 横断面 / 描述性）
- [ ] 生成 `project_config.yml`、`.clinpub/{PROJECT,ROADMAP,STATE}.md`
- [ ] 建立标准目录（`01_RawData/` … `05_Manuscript/`）
- [ ] 输出末尾提示运行 `/clinpub next` 做关卡核验

**易错点**：agent 容易直接开跑而不问期刊。若它没问，记为失败项。

### Phase 1 — 数据清洗

```
/clinpub-data-prep
```

预期：

- [ ] 产出 `02_PreprocessedData/data/cleaned.csv`
- [ ] 缺失值处理策略**有说明**（8% 该补还是完整病例？）
- [ ] 产数据质量报告
- [ ] 异常值检测有记录（`bmi`、`eGFR` 可能越界）

### Phase 2 — 迭代分析（3.0 核心）

```
/clinpub-analysis
```

预期（**逐条验证，这是本次测试的重点**）：

- [ ] **不是一次给出全部方法**，而是第一批只提 1–3 个（通常是基线表 + 主分析）
- [ ] 建出 `.clinpub/ANALYSIS_LOG.md`，每批**六段齐全**（依据 / 本批方法 / 结果要点 / 解读 / 下一批决策 / **否决项**）
- [ ] 每批方法选择标注了**规则编号**（R01、D01…）
- [ ] 第一批结果出来后，第二批判定**引用了第一批结果**（不是走原计划）
- [ ] 出现**分叉**时（如"组间显著 → 是否做敏感性分析"）会询问，而非自作主张
- [ ] 结束时写明**命中的饱和判据**（S1–S5）
- [ ] 产出 `ANALYSIS_SUMMARY.md`
- [ ] 图 ≥300 DPI、英文标注、全部 `source("04_Outputs/_figure_config.R")`

**失败信号**：一口气列出 8 个方法并直接开跑 = 退回了 2.x 行为。

### Phase 3 — 递进写作（3.0 核心）

```
/clinpub-writing
```

预期：

- [ ] **先出 `FIGURE_SKELETON.md`**（图表排序 + 每张一句结论），而不是先写引言
- [ ] **Results 先于 Introduction 产出**（看文件时间戳或对话顺序）
- [ ] 每节写进 `05_Manuscript/sections/*.md`，带 frontmatter（`status` / `inputs` / `depends_on`）
- [ ] Methods 的 Statistical Analysis 与 `ANALYSIS_LOG.md` **双向一致**
- [ ] Discussion 引用了敏感性分析或**被否决的备选方案**
- [ ] Introduction 之前有 `NARRATIVE.md`（含一句话卖点与 Gap）
- [ ] 拼装由 `python scripts/assemble_manuscript.py` 完成，`manuscript.md` 是生成物

**失败信号**：直接开始写 Introduction = 退回了 2.x 顺序。

### 级联验证（3.0 新增）

```
/clinpub-modify
```

改动一项分析（例如改一张图的样式），预期：

- [ ] `ANALYSIS_LOG.md` 追加了 `Batch M-{n}（modify）`
- [ ] `sections/results.md` 的 `status` 变为 `stale`
- [ ] 下游章节（discussion / conclusion / introduction / abstract）全部 `stale`
- [ ] 此时运行 `assemble_manuscript.py` 会被**拒绝**
- [ ] 重写后 status 回到 `final`，拼装通过

## 记录方式

每完成一个阶段，在下方追加一行：

| 阶段 | 结果 | 备注 |
|---|---|---|
| Phase 0 | ✅ 通过 | 暴露 F-001（探索性关卡）、F-002（标题链路） |
| Phase 1 | ✅ 通过 | 暴露 F-003（`None` 被吞）、F-004（ID 子串误伤） |
| Phase 2 | ✅ 通过 | 2 批 4 方法，S1 饱和；暴露 F-005（图表配置语法） |
| Phase 3 | ✅ 通过 | 6 节 final + 拼装；暴露 F-007（占位符/重复标题） |
| 引用 | ✅ 通过 | 12 篇真实文献；暴露 F-009（引用链路未实现） |
| 图表风格 | ✅ 通过 | 4 风格包 + 矢量导出；暴露 F-010、F-011 |
| 级联（modify） | ⏳ 未测 | stale 传播与重拼未跑 |

## 发现的问题怎么处理

测试的目的不是"跑通"，而是**暴露管线的缺陷并修掉**。固定闭环：

```
发现 → 记入 FINDINGS.md → 改源码 → 三平台同步 → 写 CHANGELOG → 复验打勾
```

- **管线缺陷**（关卡判据、字段缺失、脚本行为）→ 必须记 + 必须修
- **测试数据/配置问题**（如 `comorbidity` 分四类）→ 不记，测试不追究
- **纯措辞偏好** → 直接改，不单独立条

明细见 [`FINDINGS.md`](FINDINGS.md)。

> ⚠️ 修完插件后记得重跑 `node dsh/build.mjs`——DSH 技能是生成物，
> 改了 commands/workflows 不重新生成，DSH 用的还是旧逻辑。
