"""收尾：阶段N 去空格、修混合表述与重复括号。"""
import io
import re
from pathlib import Path

ROOT = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub")

TARGETS = []
for pat in ("claude-code/**/*.md", "docs/*.md"):
    TARGETS += sorted(ROOT.glob(pat))
TARGETS += [ROOT / "README.md", ROOT / "CHANGELOG.md"]

# 针对性修补（先做，避免被通 regex 打乱）
FIXES = [
    ("写作阶段（阶段 3）的 Discussion", "写作阶段的 Discussion"),
    ("写作阶段（阶段3）的 Discussion", "写作阶段的 Discussion"),
    ("**During 阶段 3 chapter writing:**", "**阶段3 分章写作时：**"),
    ("阶段 3 spec: 分段撰写时", "阶段3 规范：分段撰写时"),
    ("- 依赖 阶段 1 data-prep 的缺失值诊断结果", "- 依赖阶段1 data-prep 的缺失值诊断结果"),
    ('description: "阶段 2 orchestration: 迭代式统计分析。', 'description: "阶段2 编排：迭代式统计分析。'),
    ('description: "阶段 3 orchestration: 递进式写作。', 'description: "阶段3 编排：递进式写作。'),
    ("# Milestone: 阶段 {N} — {name}", "# Milestone: 阶段{N} — {name}"),
    ("当前状态: 阶段 {N} ({name})", "当前状态: 阶段{N} ({name})"),
]

n_fix = 0
n_space = 0
files = 0

for p in TARGETS:
    if not p.exists():
        continue
    text = io.open(p, encoding="utf-8").read()
    orig = text

    for a, b in FIXES:
        if a in text:
            text = text.replace(a, b)
            n_fix += 1

    # 中文里的「阶段 3」→「阶段3」（用户要求紧凑写法）
    before = text
    text = re.sub(r"阶段 (?=\d)", "阶段", text)
    if text != before:
        n_space += len(re.findall(r"阶段(?=\d)", before))

    if text != orig:
        io.open(p, "w", encoding="utf-8").write(text)
        files += 1

print(f"  修补文件 {files} 个；定向修补 {n_fix} 处；去空格 {n_space} 处")
