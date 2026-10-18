"""把 {{cite:Key}} 标记插入各章节。可重复执行（已存在则不重复插入）。"""
from pathlib import Path

S = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test\05_Manuscript\sections")

# (文件, 锚点句, 在锚点句之后插入的标记)
EDITS = [
    ("introduction.md",
     "症状评分的轻微变化，往往对应着睡眠、日常活动能力与照护负担的实质差别。",
     "{{cite:Vyas2020,Triolo2024}}"),
    ("introduction.md",
     "这种\"适应证混杂\"使得直接比较治疗组与未治疗组的观察性研究极易得出偏倚的方向。",
     "{{cite:Lee2022,Remschmidt2015}}"),
    ("introduction.md",
     "但随机试验的人群经过严格筛选，合并症少、依从性高，与真实临床环境中的患者存在系统性差异。",
     "{{cite:Steffens2026}}"),
    ("methods.md",
     "研究按 STROBE 声明的条目组织报告。",
     "{{cite:vonElm2008}}"),
    ("methods.md",
     "插补模型纳入结局、分组、年龄、性别、体质指数与共病状态，并按 Rubin 规则汇总。",
     "{{cite:Allotey2019,Wijesuriya2025}}"),
    ("discussion.md",
     "本研究的效应量（标准化均数差约 0.56）落在同类干预研究报告的中等效应区间内。",
     "{{cite:Tunvirachaisakul2018,Goke2024,Joel2014}}"),
    ("discussion.md",
     "从机制上看，症状评分的改善可能通过症状负荷的减轻而非器官功能的改变实现——本研究中肾功能与分组及结局均无关联，提示所观察到的变化并不以肾功能改善为中介。",
     "{{cite:Hou2025}}"),
]

for fname, anchor, marker in EDITS:
    p = S / fname
    txt = p.read_text(encoding="utf-8")
    if marker in txt:
        print(f"  [skip] {fname}: 已含 {marker}")
        continue
    if anchor not in txt:
        print(f"  [MISS] {fname}: 未找到锚点「{anchor[:28]}…」")
        continue
    txt = txt.replace(anchor, anchor + marker, 1)
    p.write_text(txt, encoding="utf-8")
    print(f"  [ok]   {fname}: +{marker}")
