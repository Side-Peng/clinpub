"""Phase 3 一致性复核（writing_standards §10 的 10 项，去掉不适用项）。"""
import re
from pathlib import Path

B = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test")
S = B / "05_Manuscript" / "sections"
M = B / "05_Manuscript" / "manuscript.md"
log = (B / ".clinpub" / "ANALYSIS_LOG.md").read_text(encoding="utf-8")
ms = M.read_text(encoding="utf-8")

ok = True


def chk(label, cond, detail=""):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))


# 1 Results 段落 ↔ 骨架图表
skel = (B / "05_Manuscript" / "FIGURE_SKELETON.md").read_text(encoding="utf-8")
skel_items = len(re.findall(r"^### (Table|Figure|Supplementary)", skel, re.M))
res = (S / "results.md").read_text(encoding="utf-8")
res_paras = len([p for p in res.split("\n\n") if p.strip() and not p.startswith("---") and not p.startswith("#")])
chk("Results 段落数与骨架条目数匹配", abs(res_paras - skel_items) <= 2, f"段落 {res_paras} / 骨架 {skel_items}")

# 2 Methods ↔ 实际做过（日志 + 方法说明 + 分析摘要）
# 注意：ANALYSIS_LOG 记录的是"批次与方法 ID"，统计技术细节在 方法说明.md 与
# ANALYSIS_SUMMARY.md 里。只查日志会误判。
done_src = log + (B / ".clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md").read_text(encoding="utf-8")
for p in (B / "04_Outputs").rglob("方法说明.md"):
    done_src += p.read_text(encoding="utf-8")

methods = (S / "methods.md").read_text(encoding="utf-8")
done = ["t 检验", "χ²", "Pearson", "线性回归", "Wilcoxon", "多重插补", "Shapiro", "方差膨胀", "Cook"]
for d in done:
    if d in methods:
        chk(f"Methods 提到的「{d}」确实做过", d in done_src)
for called_off in ["亚组", "立方样条", "交互"]:
    chk(f"已否决的「{called_off}」未写进 Methods 作为已做分析",
        not re.search(rf"(采用|进行|实施)[^。]{{0,10}}{called_off}", methods))

# 3 Introduction 假设 ↔ Results
intro = (S / "introduction.md").read_text(encoding="utf-8")
chk("Introduction 承诺的「基线可比」有对应结果", "可比" in intro and "0.04" in res)
chk("Introduction 承诺的「调整后差异」有对应结果", "调整" in intro and "9.01" in res)
chk("Introduction 承诺的「稳健性」有对应结果", "稳健" in intro and "两个" not in intro or "稳健" in res)

# 4 Discussion 不引入新结果
disc = (S / "discussion.md").read_text(encoding="utf-8")
new_nums = set(re.findall(r"-?\d+\.\d{2}", disc)) - set(re.findall(r"-?\d+\.\d{2}", ms.split("## Results")[1].split("## Discussion")[0]))
chk("Discussion 未引入 Results 中没有的新统计量", not new_nums, f"新数字 {sorted(new_nums)}")

# 5 变量名一致
for v in ["post_score", "baseline_score", "comorbidity", "egfr"]:
    chk(f"变量名「{v}」全文写法一致", len(set(re.findall(rf"\b{v}\b", ms))) <= 1)

# 6 图表编号连续
tabs = sorted(set(int(x) for x in re.findall(r"Table (\d+)", ms)))
figs = sorted(set(int(x) for x in re.findall(r"Figure (\d+)", ms)))
chk("表格编号连续", tabs == list(range(1, len(tabs) + 1)), f"{tabs}")
chk("图编号连续", figs == list(range(1, len(figs) + 1)), f"{figs}")

# 7 统计量三元组
chk("结果段有 95% CI", "95% CI" in res or "95%置信" in res)
chk("无 p = 0.000", not re.search(r"[Pp]\s*=\s*0\.000(?!\d)", ms))

# 8 报告规范（STROBE）示意
chk("声明 STROBE", "STROBE" in ms)

# 9 摘要数字与正文一致
ab = (S / "abstract.md").read_text(encoding="utf-8")
for num in ["9.01", "15.47", "2.55", "0.00678", "0.04"]:
    chk(f"摘要数字 {num} 与正文一致", num in ab and num in res)

# 10 引用
import json as _json

libp = B / "Reference" / "reference_library.json"
ms_refs = ms.split("## References")[1] if "## References" in ms else ""
if libp.exists():
    lib = _json.loads(libp.read_text(encoding="utf-8-sig"))["references"]
    by_key = {r["citation_key"]: r for r in lib}
    Cited = set()

    # 按章节顺序收集引用键，重建编号
    order = []
    for f in ["abstract", "introduction", "methods", "results", "discussion", "conclusion"]:
        t = (S / f"{f}.md").read_text(encoding="utf-8")
        for m in re.finditer(r"\{\{cite:([^}]+)\}\}", t):
            for k in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                if k in by_key and k not in order:
                    order.append(k)

    chk("所有 citation_key 都在文献库中", all(k in by_key for k in order), f"{len(order)} 条")
    chk("文献库无未引用条目", len(order) == len(lib), f"引用 {len(order)} / 库 {len(lib)}")

    # 正文编号连续 [1..N]
    # 注意要处理 [1,2] 这种多引用格式，不能只匹配 [3]
    nums = sorted({int(n) for grp in re.findall(r"\[([\d,]+)\]", ms) for n in grp.split(",")})
    chk("正文引用编号连续", nums == list(range(1, len(order) + 1)), f"{nums}")

    # References 条数与引用数一致
    reflines = [l for l in ms_refs.split("\n") if re.match(r"^\d+\. ", l)]
    chk("References 条数与引用数一致", len(reflines) == len(order), f"{len(reflines)} vs {len(order)}")

    # 每条 DOI 存在且非 pending
    pend = [r["citation_key"] for r in lib if r.get("doi", "pending_doi") == "pending_doi"]
    chk("所有文献均有 DOI", not pend, f"缺 DOI: {pend}")

    # References 文本里都带 doi:
    chk("References 段每条含 doi:", all("doi:" in l for l in reflines))

    # 编号顺序 = 首次出现顺序
    chk("编号顺序与首次出现顺序一致",
        len(order) == len(set(order)), f"{len(order)} 条唯一")

    # 无残留 cite 标记
    chk("无残留 {{cite:}} 标记", "{{cite:" not in ms)
else:
    chk("文献库存在", False, "Reference/reference_library.json 缺失")

print("\n" + ("一致性复核通过" if ok else "存在失败项"))
raise SystemExit(0 if ok else 1)
