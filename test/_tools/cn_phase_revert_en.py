"""按文件语言回退：英文为主的文档把「阶段」改回 Phase。"""
import io
import re
from pathlib import Path

ROOT = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub")

TARGETS = []
for pat in ("claude-code/**/*.md", "docs/*.md"):
    TARGETS += sorted(ROOT.glob(pat))
TARGETS += [ROOT / "README.md", ROOT / "CHANGELOG.md"]

CJK = re.compile(r"[\u4e00-\u9fff]")

reverted = []
mixed = []

for p in TARGETS:
    if not p.exists():
        continue
    text = io.open(p, encoding="utf-8").read()
    if "阶段 " not in text:
        continue
    cjk = len(CJK.findall(text))
    total = len(re.sub(r"\s", "", text)) or 1
    ratio = cjk / total

    if ratio < 0.12:
        # 英文为主：整体回退
        text = text.replace("阶段 ", "Phase ")
        io.open(p, "w", encoding="utf-8").write(text)
        reverted.append((str(p.relative_to(ROOT)), round(ratio, 3)))
    elif ratio < 0.35:
        mixed.append((str(p.relative_to(ROOT)), round(ratio, 3)))

print(f"  回退（英文为主）{len(reverted)} 个：")
for f, r in reverted:
    print(f"    {f:<52} CJK {r}")
print(f"\n  双语/混合（需人工看）{len(mixed)} 个：")
for f, r in mixed:
    print(f"    {f:<52} CJK {r}")
