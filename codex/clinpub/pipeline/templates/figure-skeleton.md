# 图表骨架（FIGURE SKELETON）

> 位置：`05_Manuscript/FIGURE_SKELETON.md`
> 作用：阶段3 的**第一步**。在写任何正文之前，先把所有表与图排定，并为每张写一句大白话结论。
> 依据：`pipeline/references/writing_standards.md` §2

---

## 一、图表清单

<!--
排序规则：
- 顺序 = Results 的叙述顺序 = 读者理解顺序（不是分析执行顺序）
- 图表清单按「研究类型 + 报告规范」生成，不套固定三件套：
  · RCT     → CONSORT 流程图 + 主要终点表 + 安全性表
  · 队列/病例对照/横断面 → STROBE 参与者流程图 + 基线表 + 主要分析表 + 敏感性分析
  · 描述性  → 基线表 + 分布/趋势图
-->

| 序号 | 类型 | 标题（英文） | 一句话结论（中文，不含统计量） | 支撑的分析方法 |
|---|---|---|---|---|
| Table 1 | 基线表 | {{title}} | {{one_sentence}} | {{method_id}} |
| Figure 1 | {{type}} | {{title}} | {{one_sentence}} | {{method_id}} |

---

## 二、一句话结论汇总（连读检查）

<!--
把上表「一句话结论」按顺序连起来读一遍。
如果连起来不能构成一个完整的故事，说明图表顺序或选图有问题。
-->

{{conclusion_1}}
{{conclusion_2}}
{{conclusion_3}}

---

## 三、缺失与待补

<!-- 若报告的规范要求某类图表但当前没有，写在这里，并在 Discussion 局限性中说明。 -->

- [ ] {{missing_item}} — 原因：{{reason}}

---

## 四、报告规范对照

| 规范 | 适用 | 已覆盖项 | 缺项 |
|---|---|---|---|
| {{guideline}} | {{study_type}} | {{covered}} | {{missing}} |

> 规范来源：CONSORT / STROBE / PRISMA（见 EQUATOR Network）
> STROBE 官方清单：https://www.strobe-statement.org/checklists/
