import io
import re

P = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test\figstyle\style_nature.svg"
s = io.open(P, encoding="utf-8").read()

n = 0
for m in re.finditer(r"style='([^']*)'[^>]*>([^<]*)</text>", s):
    st, txt = m.group(1), m.group(2)
    size = re.search(r"font-size:\s*([\d.]+)", st)
    weight = "bold" if "font-weight: bold" in st else "plain"
    n += 1
    print("  {:<22} size={:>5} weight={}".format(txt[:20], size.group(1) if size else "?", weight))
print("  共 {} 个文本元素".format(n))
