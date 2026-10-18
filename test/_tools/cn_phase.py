"""把正文里的 Phase N 改成 阶段 N（保留机器可读格式与技术标识）。"""
import io
import re
from pathlib import Path

ROOT = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub")

# 必须原样保留的行/片段（机器可读或代码约定）
PROTECT = [
    "阶段：Phase",          # STATE.md 解析格式，hooks 依赖
    "phases/",              # 目录路径
    "phase_number",         # mustache 占位符
    "phase_name",
    "Phase\\s*(",           # 正则片段
    "Phase_",
]

# 只替换「Phase + 数字/占位符」的正文用法
PAT = re.compile(r"Phase(?=\s*(?:\d|\{N\}|\{phase))")

TARGETS = []
for pat in ("claude-code/**/*.md", "docs/*.md"):
    TARGETS += sorted(ROOT.glob(pat))
TARGETS += [ROOT / "README.md", ROOT / "CHANGELOG.md"]

changed_files = 0
changed_lines = 0
skipped = 0

for p in TARGETS:
    if not p.exists():
        continue
    text = io.open(p, encoding="utf-8").read()
    out_lines = []
    file_changed = False
    for line in text.split("\n"):
        if any(k in line for k in PROTECT):
            out_lines.append(line)
            skipped += 1
            continue
        new = PAT.sub("阶段", line)
        if new != line:
            changed_lines += 1
            file_changed = True
        out_lines.append(new)
    if file_changed:
        io.open(p, "w", encoding="utf-8").write("\n".join(out_lines))
        changed_files += 1

print(f"  改动文件 {changed_files} 个，{changed_lines} 行")
print(f"  受保护跳过 {skipped} 行（含前缀：阶段：Phase / phases/ / phase_number ...）")
