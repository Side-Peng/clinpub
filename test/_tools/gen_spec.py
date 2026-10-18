"""Phase 1：用画像结果填充 spec 模板（只填 Phase 1 已知字段）。"""
import io
import json
import re

BASE = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub"

tpl = io.open(BASE + r"\dsh\pipeline\templates\spec.md", encoding="utf-8").read()
prof = json.load(io.open(BASE + r"\test\02_PreprocessedData\data_profile.json", encoding="utf-8"))
cfg = io.open(BASE + r"\test\project_config.yml", encoding="utf-8-sig").read()

name = re.search(r'name:\s*"([^"]+)"', cfg).group(1)
design = re.search(r'design:\s*"([^"]+)"', cfg).group(1)

fmap = {
    "{{phase_number}}": "1",
    "{{phase_name}}": "Data Preparation",
    "{{study_title}}": name,
    "{{date}}": "2026-10-18",
    "{{study_type}}": design,
    "{{design_description}}": f"{design}研究，{prof['n_rows']} 例，探索性设计（主要结局待定）",
    "{{journal_name}}": "Alzheimer's & Dementia",
    "{{impact_factor}}": "待查",
    "{{STROBE / CONSORT / TRIPOD / PRISMA}}": "STROBE",
    "{{N}}": str(prof["n_rows"]),
    "{{primary_outcome}}": "待定（analysis_mode: exploratory）",
    "{{primary_exposure}}": "comorbidity / group（候选）",
}

out = tpl
for k, v in fmap.items():
    out = out.replace(k, v)

io.open(BASE + r"\test\03_AnalysisMethods\01-spec.md", "w", encoding="utf-8").write(out)

left = re.findall(r"\{\{[^}]+\}\}", out)
print("  已生成 03_AnalysisMethods/01-spec.md")
print("  行数", len(out.splitlines()), "| 剩余占位符种类", len(set(left)))
print("  剩余示例:", ", ".join(sorted(set(left))[:8]))
