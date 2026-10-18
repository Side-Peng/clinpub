"""Results 章节自检：字数、解释性措辞、统计量格式、占位符。"""
import re
from pathlib import Path

p = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test\05_Manuscript\sections\results.md")
txt = p.read_text(encoding="utf-8")
body = txt.split("---", 2)[2]

cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
print(f"  汉字数        : {cjk}")

banned = {
    "解释性-提示": r"提示",
    "解释性-说明": r"说明(?!了共)",
    "解释性-表明": r"表明",
    "解释性-因此": r"因此",
    "解释性-机制": r"机制",
    "解释性-因果": r"因果",
    "解释性-可能由于": r"可能由于",
    "开头套话": r"^As shown in",
    "p=0.000": r"p\s*=\s*0\.000",
}
hits = []
for k, pat in banned.items():
    for m in re.finditer(pat, body, re.M):
        hits.append((k, body[max(0, m.start() - 12):m.start() + 12].replace("\n", " ")))
if hits:
    for k, ctx in hits:
        print(f"  [WARN] {k}: …{ctx}…")
else:
    print("  解释性措辞    : 未发现 ✅")

ph = re.findall(r"\{\{[^}]+\}\}", body)
print(f"  占位符        : {ph}")

stat = re.findall(r"P = [0-9.]+", body)
print(f"  P 值写法      : {len(stat)} 处，样例 {stat[:3]}")
ci = len(re.findall(r"95% CI", body))
print(f"  95% CI        : {ci} 处")
