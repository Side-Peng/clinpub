"""最后一轮：只保护真正的技术串，不再按整行跳过。"""
import io
import re
from pathlib import Path

ROOT = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub")

TARGETS = []
for pat in ("claude-code/**/*.md", "docs/*.md"):
    TARGETS += sorted(ROOT.glob(pat))
TARGETS += [ROOT / "README.md", ROOT / "CHANGELOG.md"]

CJK = re.compile(r"[\u4e00-\u9fff]")

# 真正的技术串：替换前先挖出来，替换后再放回
TOKENS = [
    (re.compile(r"阶段：Phase"), "\x00FMT\x00"),
    (re.compile(r"phase_number|phase_name"), None),   # 不含 Phase 大写，天然安全
    (re.compile(r"Phase\\s\*\("), None),
]

PHASE_NUM = re.compile(r"Phase(?=\s*\d|\s*\{N\})")
SPACE_AFTER = re.compile(r"阶段\s+(?=\d)")
SPACE_BEFORE = re.compile(r"([\u4e00-\u9fff])\s+阶段")

files = 0
cnt = 0

for p in TARGETS:
    if not p.exists():
        continue
    text = io.open(p, encoding="utf-8").read()

    cjk = len(CJK.findall(text))
    total = len(re.sub(r"\s", "", text)) or 1
    if cjk / total < 0.12:          # 英文文档不动
        continue

    orig = text
    text = text.replace("阶段：Phase", "\x00FMT\x00")   # 暂存格式串
    text, n1 = PHASE_NUM.subn("阶段", text)
    text = text.replace("\x00FMT\x00", "阶段：Phase")   # 还原
    text, n2 = SPACE_AFTER.subn("阶段", text)
    text, n3 = SPACE_BEFORE.subn(r"\1阶段", text)

    if text != orig:
        io.open(p, "w", encoding="utf-8").write(text)
        files += 1
        cnt += n1 + n2 + n3

print(f"  处理文件 {files} 个，替换 {cnt} 处")
