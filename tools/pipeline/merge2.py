import json, sys, re, collections, os, shutil
S = sys.argv[1]
DROP = {"juostos":[6,89,99,103,108,120,132,148], "sodai":[7,10,11], "kaukės":[13,20,27,34,37,55,59,91],
 "kryžiai":[0,5,6,7,8,9,44], "rūpintojėliai":[0,4,5,8,10,13,14,20,21,26,27,32,33,38,43,77],
 "lovatiesės":[3,15,24,29,31,42,51,60,67,77,88,89], "rankšluosčiai":[2,32,41], "pirštinės":[5,11,51,93],
 "drabužiai":[4,15,22,29,35,41,47,52], "prieverpstės":[8,22], "skrynios":[4,10,15,27]}
new = json.load(open(f"{S}/data/new2_processed.json"))
by = collections.defaultdict(list)
for s in new: by[s["cat"]].append(s)
drop = {by[c][i]["id"] for c, idx in DROP.items() for i in idx}
new = [s for s in new if s["id"] not in drop]
old = json.load(open(f"{S}/data/final.json"))
for s in old: s["old"] = True
for s in new:
    if s.get("via") == "commons":
        s["creator"] = re.sub(r"^myself \(User:(.+)\)$", r"\1", s["creator"])
allx = old + new
# Region: only when the record's own title or description names it
REG = [
 ("Aukštaitija", r"aukštait|rokišk|kupišk|biržų|biržai|pasvali|panevėž|utenos|utena|zarasų|ignalin|anykšč|molėt|ukmerg|švenčion"),
 ("Žemaitija", r"žemait|telši|plung|rietav|mažeik|skuod|šilal"),
 ("Dzūkija", r"dzūk|varėn|alytaus|alytus|druskinink|lazdij|merkin|marcinkon"),
 ("Suvalkija", r"suvalk|sūduv|marijampol|vilkaviš|šakių|šakiai|kalvarij|kazlų rūd"),
 ("Mažoji Lietuva", r"mažosios lietuvos|mažoji lietuva|klaipėdos krašt|šilutė|šilutės|rusnė|nidos|neringos|pagėg"),
]
cnt = collections.Counter()
for s in allx:
    txt = (s["title"] + " " + s["desc"]).lower()
    hits = [name for name, rx in REG if re.search(rx, txt)]
    s["reg"] = hits[0] if len(hits) == 1 else ""
    cnt[s["reg"] or "-"] += 1
print("regions", cnt.most_common())
print(collections.Counter(s["cat"] for s in allx))
print("total", len(allx), "new", len(new))
json.dump(allx, open(f"{S}/data/all2.json", "w"), ensure_ascii=False)
