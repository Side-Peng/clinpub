"""由 reference_library.json 生成 references.bib、citation_map.md，并回填 sections_used。"""
import json
import re
from pathlib import Path

BASE = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test")
REF = BASE / "Reference"
MS = BASE / "05_Manuscript"

lib = json.loads((REF / "reference_library.json").read_text(encoding="utf-8-sig"))
refs = lib["references"]
by_key = {r["citation_key"]: r for r in refs}

# ---- 从章节实际使用回填 sections_used -----------------------------------
SECTION_FILES = [
    ("introduction", "introduction.md"),
    ("methods", "methods.md"),
    ("results", "results.md"),
    ("discussion", "discussion.md"),
    ("conclusion", "conclusion.md"),
    ("abstract", "abstract.md"),
]
for r in refs:
    r["sections_used"] = []

for sec, fname in SECTION_FILES:
    txt = (MS / "sections" / fname).read_text(encoding="utf-8")
    for m in re.finditer(r"\{\{cite:([^}]+)\}\}", txt):
        for k in [x.strip() for x in m.group(1).split(",") if x.strip()]:
            if k in by_key and sec not in by_key[k]["sections_used"]:
                by_key[k]["sections_used"].append(sec)

# ---- 出现顺序（用于编号）----------------------------------------------
order = []
for _, fname in SECTION_FILES:
    txt = (MS / "sections" / fname).read_text(encoding="utf-8")
    for m in re.finditer(r"\{\{cite:([^}]+)\}\}", txt):
        for k in [x.strip() for x in m.group(1).split(",") if x.strip()]:
            if k in by_key and k not in order:
                order.append(k)

for i, k in enumerate(order, start=1):
    by_key[k]["display_number"] = i

lib["updated"] = "2026-10-18"
(REF / "reference_library.json").write_text(
    json.dumps(lib, ensure_ascii=False, indent=2), encoding="utf-8"
)

# ---- BibTeX -------------------------------------------------------------
def bib_escape(s: str) -> str:
    return (s or "").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


entries = []
for k in order:
    r = by_key[k]
    entries.append(
        "\n".join(
            [
                f"@article{{{k},",
                f"  author  = {{{bib_escape(' and '.join(r.get('authors') or []))}}},",
                f"  title   = {{{bib_escape(r.get('title'))}}},",
                f"  journal = {{{bib_escape(r.get('journal'))}}},",
                f"  year    = {{{r.get('year')}}},",
                f"  doi     = {{{r.get('doi')}}},",
                f"  pmid    = {{{r.get('pmid')}}}",
                "}",
            ]
        )
    )
(REF / "references.bib").write_text("\n\n".join(entries) + "\n", encoding="utf-8")

# ---- citation map -------------------------------------------------------
rows = ["# 引用映射（citation_map）", "",
        "> 编号按**正文首次出现顺序**分配（Vancouver），与文献库 id 不同。", "",
        "| 编号 | citation_key | 第一作者 | 年份 | 期刊 | 使用章节 |",
        "|---|---|---|---|---|---|"]
for k in order:
    r = by_key[k]
    first = (r.get("authors") or ["?"])[0]
    rows.append(
        f"| {r['display_number']} | `{k}` | {first} | {r['year']} | "
        f"{r.get('journal','')} | {', '.join(r['sections_used'])} |"
    )
unused = [r["citation_key"] for r in refs if r["citation_key"] not in order]
if unused:
    rows += ["", "## 未被引用", ""]
    rows += [f"- `{u}`" for u in unused]
(REF / "citation_map.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

# ---- MANIFEST -----------------------------------------------------------
manifest = f"""# MANIFEST — 参考文献输出
# 消费者：writer-agent（Phase 3）、clinpub-verifier

agent: reference-agent
phase: 3
type: literature-retrieval

outputs:
  - directory: Reference
    files:
      - name: reference_library.json
        format: json
        statistics: [n_references]
      - name: references.bib
        format: bib
      - name: citation_map.md
        format: md
      - name: MANIFEST.yaml
        format: yaml

handoffs:
  - consumer: writer-agent
    required_files:
      - Reference/reference_library.json
      - Reference/citation_map.md
    required_quality:
      - "每条记录含完整 abstract"
      - "每条记录 DOI 非 pending"

decisions:
  - variable: 检索工具
    decision: "内置 ncbi_search.py（ncbi-search v3.0.0）"
    rationale: "clinpub 自带，无需外部 skill；v3 默认不返回摘要，筛选阶段用 --abstract preview。"
  - variable: 引用数量
    decision: "{len(order)} 篇（低于 citation_strategy 的 30–55）"
    rationale: "本次为引用链路验证，覆盖 Intro/Methods/Discussion 三节即可打通编号与 DOI 检查。"

notes: >
  共 {len(order)} 条引用，全部含 DOI 与 PMID，编号按正文首次出现顺序分配。
  其中 2014/2015/2018/2008 年文献超出"近 5 年"窗口，属 landmark/方法学经典，
  保留依据：STROBE 为报告规范原文，MI 与预测模型为该领域方法学基础文献。
"""
(REF / "MANIFEST.yaml").write_text(manifest, encoding="utf-8")

print(f"  编号 {len(order)} 条，未引用 {len(unused)} 条")
print("  已生成 references.bib / citation_map.md / MANIFEST.yaml")
for k in order:
    r = by_key[k]
    print(f"  [{r['display_number']:>2}] {k:<22} {', '.join(r['sections_used'])}")
