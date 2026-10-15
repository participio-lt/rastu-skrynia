import json, sys, re, hashlib, collections
S = sys.argv[1]
proc = json.load(open(f"{S}/data/processed.json"))
raw = json.load(open(f"{S}/data/raw.json"))
EXCL = {"juostos":[8,9,10,18,21,40,51,66,70,75,83,105], "sodai":[2,4], "verbos":[1,3],
 "kryžiai":[1,4,7,11,12,13,14,18,21,24,26], "rūpintojėliai":[4,5,18,19,21,27],
 "pirštinės":[8,19,25], "drabužiai":[4,7,8,14,15,20,24], "prieverpstės":[4,6,8,9,15,22,23],
 "skrynios":[14,17], "kaukės":[2,3,6,7,9,12,16,17,21,22,25,26]}
bycat = collections.defaultdict(list)
for s in proc: bycat[s["cat"]].append(s)
drop = set()
for c, idx in EXCL.items():
    for i in idx: drop.add(bycat[c][i]["id"])
keep = [s for s in proc if s["id"] not in drop]
json.dump(sorted(drop), open(f"{S}/data/dropped.json","w"))
used = {s["eid"] for s in proc}
REFILL = {
 "kryžiai": (r"viršūnė|saulutė|geležinis kryžius|koplytstulpis$|stogastulpis$|koplytėlė$", r"rajonas|kaimo|atlaidai|byla|vaik|fotorinkin|r\.|brėžin", {"Heritage Conservation Library of the Cultural Heritage Center"}, 10),
 "kaukės": (r"užgavėnių kaukė|medinė kaukė", r"tradicin|pomirtin|rytiet|keramik", set(), 10),
}
sys.path.insert(0, f"{S}/scripts")
from select_helpers import make
new = []
for cat, (want, bad, badprov, n) in REFILL.items():
    got = 0
    for it in raw[cat]:
        if got >= n: break
        t = (it.get("title") or [""])[0]
        if it["id"] in used or not re.search(want, t, re.I) or re.search(bad, t, re.I): continue
        if (it.get("dataProvider") or [""])[0] in badprov: continue
        r = make(it, cat)
        if r: new.append(r); used.add(it["id"]); got += 1
print("kept", len(keep), "dropped", len(drop), "new", len(new))
json.dump(keep, open(f"{S}/data/kept.json","w"), ensure_ascii=False)
json.dump(new, open(f"{S}/data/new.json","w"), ensure_ascii=False)
