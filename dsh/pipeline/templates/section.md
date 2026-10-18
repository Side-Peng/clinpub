<!--
  模板：章节文件 frontmatter 与结构
  用途：writer-agent 每写一节，按此格式创建 05_Manuscript/sections/{key}.md
  复制到目标位置后，把占位符替换为实际内容。
-->
---
section: {{section_key}}          # results | methods | discussion | conclusion | introduction | abstract
status: draft                     # draft | final | stale
inputs:                           # 这一节据以写成的内容源（必须真实读取过）
  - {{input_path_1}}
  - {{input_path_2}}
depends_on: []                    # 上游章节 key，用于 stale 传播
---

<!-- 正文从下一行开始。整节只有一个 ## 标题，标题名由拼装脚本统一注入，此处不写。 -->

{{section_body}}

<!--
写作约束（写完请自查，不写进正文）：
1. 只做本节该做的事（见 writing_standards.md 各节职责）
2. Results 禁止任何解释；解释归 Discussion
3. 交叉引用用占位符：{{Table:N}} {{Figure:N}} {{Method:name}} {{Section:name}}
4. 自然成段，不用 bullet point（正文 >5000 字的要求）
5. 引用用 [id]，由拼装阶段统一编号
-->
