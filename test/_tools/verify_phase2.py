"""Phase 2 verify_outputs：结构、共享配置、图件、日志完整性。"""
import io
import os
import re
from pathlib import Path

BASE = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test")
M = BASE / "03_AnalysisMethods"
O = BASE / "04_Outputs"

ok = True


def check(label, cond, detail=""):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))


# 1. 目录一致性
methods = sorted(d.name for d in M.iterdir() if d.is_dir())
outputs = sorted(d.name for d in O.iterdir() if d.is_dir())
check("03_AnalysisMethods 与 04_Outputs 子目录一一对应",
      set(methods) == set(outputs),
      f"{methods} vs {outputs}")

# 2. 每个方法脚本都 source 共享配置
for m in methods:
    script = M / m / "run.R"
    check(f"{m} 有 run.R", script.exists())
    if script.exists():
        txt = script.read_text(encoding="utf-8")
        check(f"{m} source(_figure_config.R)",
              'source("04_Outputs/_figure_config.R")' in txt)

# 3. 每个输出目录有 方法说明.md
for o in outputs:
    check(f"{o} 有 方法说明.md", (O / o / "方法说明.md").exists())

# 4. 图件 DPI
from PIL import Image

pngs = sorted(O.rglob("*.png"))
check("存在图件", len(pngs) > 0, f"{len(pngs)} 个 png")
for p in pngs:
    with Image.open(p) as im:
        dpi = im.info.get("dpi")
    d = round(dpi[0]) if dpi else None
    check(f"{p.name} DPI >= 300", bool(d and d >= 300), f"{d}")

# 5. 三格式导出
for p in pngs:
    stem = p.with_suffix("")
    for ext in (".svg", ".tiff"):
        check(f"{stem.name}{ext} 存在", stem.with_suffix(ext).exists())

# 6. 日志完整性
log = (BASE / ".clinpub" / "ANALYSIS_LOG.md").read_text(encoding="utf-8")
batches = re.findall(r"^## Batch (\d+)", log, re.M)
check("ANALYSIS_LOG 有批次", bool(batches), f"Batch {batches}")
for b in batches:
    seg = log.split(f"## Batch {b}")[1].split("\n## Batch ")[0]
    for sec in ("### 依据", "### 本批方法", "### 结果要点", "### 解读", "### 下一批决策", "### 否决项"):
        check(f"Batch {b} 含「{sec[4:]}」", sec in seg)

# 7. 方法脚本与日志方法清单一致
logged = set(re.findall(r"`(\d{2}_\w+)`", log))
check("日志方法清单与实际目录一致", logged <= set(methods), f"日志={sorted(logged)}")

print("\n" + ("全部通过 ✅" if ok else "存在失败项 ❌"))
raise SystemExit(0 if ok else 1)
