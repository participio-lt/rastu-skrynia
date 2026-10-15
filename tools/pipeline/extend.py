import json, sys, re, collections, random
S = sys.argv[1]; sys.path.insert(0, S + "/scripts")
from select_helpers import first, rights_label, WEAVE, J_BAD, TRUST_NODESC, make
raw = json.load(open(f"{S}/data/raw.json"))
final = json.load(open(f"{S}/data/final.json"))
dropped = set(json.load(open(f"{S}/data/dropped.json")))
have = collections.Counter(s["cat"] for s in final)
used_eid = {s["eid"] for s in final}
import hashlib
hid = lambda e: hashlib.sha1(e.encode()).hexdigest()[:10]
CAPS = {"juostos":300,"margučiai":130,"verbos":20,"karpiniai":160,"rūpintojėliai":100,"kryžiai":100,"lovatiesės":120,
        "rankšluosčiai":80,"pirštinės":120,"drabužiai":100,"prieverpstės":100,"skrynios":100,"kaukės":120,"sodai":0}
EXTRA_BAD = {
 "kryžiai": (r"rajonas|kaimo|atlaidai|byla|vaik|fotorinkin|\br\.|brėžin|aplank|kapinėse|šventor|bažnyčio|mūrinė", {"Heritage Conservation Library of the Cultural Heritage Center"}),
 "kaukės": (r"tradicin|pomirtin|rytiet|keramik|metalin|gipsin|kaukė [ivx]+$|dekoratyvin", set()),
 "drabužiai": (r"karūnėl|krosnies|eskiz|apatinis sijonas|masoni", set()),
 "prieverpstės": (r"kultuv|kočėl|ratel", set()),
 "pirštinės": (r"odinės|rakauskaitės|darbo|guminės", set()),
 "rūpintojėliai": (r"nuotrauk|atviruk|tapyb|paveiksl", set()),
 "skrynios": (r"taupyk|seifas|banko|pinigų", set()),
}
random.seed(11)
new = []
for cat, items in raw.items():
    need = CAPS.get(cat, 0) - have[cat]
    if need <= 0: continue
    bad, badprov = EXTRA_BAD.get(cat, (r"$^", set()))
    pool, seen_desc = [], set()
    for it in items:
        if it["id"] in used_eid or hid(it["id"]) in dropped: continue
        t = first(it.get("title")); d = " ".join(it.get("dcDescription") or []).strip()
        prov = first(it.get("dataProvider"))
        if re.search(bad, t, re.I) or prov in badprov: continue
        if cat == "juostos":
            if J_BAD.search(t) or J_BAD.search(d): continue
            if d and not WEAVE.search(d): continue
            if not d and prov not in TRUST_NODESC: continue
        if d and len(d) > 40 and d in seen_desc: continue
        seen_desc.add(d)
        if rights_label(first(it.get("rights"))) == "Kita": continue
        pool.append(it)
    byp = collections.defaultdict(list)
    for it in pool: byp[first(it.get("dataProvider"))].append(it)
    for p in byp.values():
        random.shuffle(p); p.sort(key=lambda it: 0 if it.get("dcDescription") else 1)
    order, provs = [], sorted(byp, key=lambda p: -len(byp[p]))
    while any(byp.values()):
        for p in provs:
            if byp[p]: order.append(byp[p].pop(0))
    got = 0
    for it in order:
        if got >= need: break
        r = make(it, cat)
        if r and r["id"] not in {n["id"] for n in new}:
            new.append(r); used_eid.add(it["id"]); got += 1
    print(f"{cat}: had {have[cat]}, pool {len(pool)}, adding {got}")
json.dump(new, open(f"{S}/data/new2.json", "w"), ensure_ascii=False)
print("new total", len(new))
