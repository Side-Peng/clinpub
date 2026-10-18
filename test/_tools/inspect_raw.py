"""检查 pubmed_fetch 的 JSON 结构。"""
import io
import json

p = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test\Reference\_raw.json"
raw = io.open(p, encoding="utf-8-sig").read()
i = min([x for x in [raw.find("["), raw.find("{")] if x >= 0])
data = json.loads(raw[i:])

print("顶层类型:", type(data).__name__)
if isinstance(data, dict):
    print("顶层键:", list(data.keys())[:10])
    for k, v in data.items():
        if isinstance(v, list):
            print(f"  {k}: list len={len(v)}")
            if v:
                print("  首元素类型:", type(v[0]).__name__)
                print("  首元素键:", list(v[0].keys()) if isinstance(v[0], dict) else v[0])
elif isinstance(data, list):
    print("长度:", len(data))
    for x in data[:3]:
        print("  元素:", type(x).__name__, list(x.keys()) if isinstance(x, dict) else str(x)[:80])
