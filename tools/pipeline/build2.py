import json, sys, os, re, base64, collections
S, OUT = sys.argv[1], sys.argv[2]
BUNDLE = 10
items = json.load(open(f"{S}/data/final2.json"))
def vivid(s):
    best = 0
    for h in s.get("pal") or []:
        r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5)); best = max(best, max(r, g, b) - min(r, g, b))
    return best
os.makedirs(f"{OUT}/b", exist_ok=True)
for f in os.listdir(f"{OUT}/b"): os.remove(f"{OUT}/b/{f}")
newby = collections.defaultdict(list)
for s in items:
    if s.get("old"):
        assert os.path.exists(f"{OUT}/img/{s['id']}.jpg"), s["id"]
    else:
        newby[s["cat"]].append(s)
bi, total = 0, 0
for cat in sorted(newby):
    lst = sorted(newby[cat], key=lambda s: -vivid(s))
    for k in range(0, len(lst), BUNDLE):
        chunk = lst[k:k+BUNDLE]; data = {}
        for s in chunk:
            raw = open(f"{S}/img2/{s['id']}.jpg", "rb").read()
            data[s["id"]] = "data:image/jpeg;base64," + base64.b64encode(raw).decode()
            s["b"] = bi
        txt = json.dumps(data, separators=(",", ":"))
        open(f"{OUT}/b/{bi:03d}.json", "w").write(txt); total += len(txt); bi += 1
KEEP = ["id","cat","title","desc","creator","provider","rl","rights","europeana","source","w","h","pal","fam","tech","reg","place","date","mat","b","via"]
data = []
for s in items:
    d = {k: s[k] for k in KEEP if k in s and s[k] not in ("", [], None)}
    if s.get("old"): d.pop("b", None)
    if "desc" in d: d["desc"] = re.sub(r"\s*\n\s*\n\s*", "\n\n", re.sub(r"[ \t]+", " ", d["desc"])).strip()
    data.append(d)
json.dump(data, open(f"{S}/data/page_data.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("bundles", bi, "bundle MB", round(total / 1e6, 1), "items", len(data), "data KB", round(len(json.dumps(data, ensure_ascii=False)) / 1024))
print("files in version:", len(os.listdir(f"{OUT}/img")) + bi + 1)
