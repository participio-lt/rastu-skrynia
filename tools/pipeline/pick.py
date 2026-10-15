import json, sys, re, hashlib, collections, random
raw = json.load(open(sys.argv[1])); OUT = sys.argv[2]
random.seed(7)
CAPS = {"juostos":110,"sodai":40,"margučiai":30,"verbos":10,"karpiniai":24,"rūpintojėliai":28,"kryžiai":28,
        "lovatiesės":28,"rankšluosčiai":22,"pirštinės":26,"drabužiai":26,"prieverpstės":26,"skrynios":22,"kaukės":28}
WEAVE = re.compile(r"aust|pint|rinkt|vyt|kaišyt|dimų|siūl|apmat|ataud|kut|vilnon|lin|medvilnin|šilk|ornament|rašt|woven|braid", re.I)
J_BAD = re.compile(r"takas|varpelio|abituriento|čiurlioniui|pilkapis|pusnuomečio|šilko juostelė|truikio|szyd|ofiarowali|siuvinėt", re.I)
TRUST_NODESC = {"The Lithuanian National Museum of Art","Vincas Mykolaitis-Putinas Memorial Apartment-Museum","Rokiškis Regional Museum"}
def first(x): return (x or [""])[0]
def technique(t):
    t = t.lower()
    for pat, name in [(r"slucko|kontuš","Kontušo"),(r"rinktin","Rinktinė"),(r"pintin|pinta","Pintinė"),(r"vytin|vyta","Vytinė"),
                      (r"kaišytin","Kaišytinė"),(r"dimų|dimin","Dimų"),(r"austin|austa|woven","Austinė")]:
        if re.search(pat, t): return name
    return ""
def rights_label(u):
    m = {"publicdomain/mark":"Viešasis domenas","publicdomain/zero":"CC0","licenses/by/":"CC BY","licenses/by-sa/":"CC BY-SA",
         "licenses/by-nc/":"CC BY-NC","licenses/by-nc-sa/":"CC BY-NC-SA","licenses/by-nd/":"CC BY-ND","licenses/by-nc-nd/":"CC BY-NC-ND"}
    for k,v in m.items():
        if k in u: return v
    return "Kita"
sel = []
for cat, items in raw.items():
    pool = []
    seen_desc = set()
    for it in items:
        t = first(it.get("title")); d = " ".join(it.get("dcDescription") or []).strip()
        prov = first(it.get("dataProvider"))
        if cat == "juostos":
            if J_BAD.search(t) or J_BAD.search(d): continue
            if d and not WEAVE.search(d): continue
            if not d and prov not in TRUST_NODESC: continue
        if d and d in seen_desc and len(d) > 40: continue
        seen_desc.add(d)
        if rights_label(first(it.get("rights"))) == "Kita": continue
        pool.append(it)
    # provider round-robin for variety, items with descriptions first
    byp = collections.defaultdict(list)
    for it in pool: byp[first(it.get("dataProvider"))].append(it)
    for p in byp.values():
        random.shuffle(p); p.sort(key=lambda it: 0 if it.get("dcDescription") else 1)
    order = []
    provs = sorted(byp, key=lambda p: -len(byp[p]))
    while any(byp.values()):
        for p in provs:
            if byp[p]: order.append(byp[p].pop(0))
    for it in order[:CAPS[cat]]:
        t = first(it.get("title")); d = " ".join(it.get("dcDescription") or []).strip()
        sel.append({
            "id": hashlib.sha1(it["id"].encode()).hexdigest()[:10],
            "eid": it["id"], "cat": cat, "title": t, "desc": d,
            "creator": first(it.get("dcCreator")), "provider": first(it.get("dataProvider")),
            "date": first(it.get("edmTimespanLabel")) if isinstance(first(it.get("edmTimespanLabel")), str) else (first(it.get("edmTimespanLabel")) or {}).get("def",""),
            "year": first(it.get("year")),
            "place": (first(it.get("edmPlaceLabel")) or {}).get("def","") if it.get("edmPlaceLabel") else "",
            "rights": first(it.get("rights")), "rl": rights_label(first(it.get("rights"))),
            "europeana": "https://www.europeana.eu/item" + it["id"], "source": first(it.get("edmIsShownAt")),
            "thumb": first(it.get("edmPreview")) + "&size=w400",
            "tech": technique(t + " " + d) if cat == "juostos" else "",
        })
    print(cat, len(pool), "->", min(len(order), CAPS[cat]))
print("total", len(sel))
json.dump(sel, open(OUT,"w"), ensure_ascii=False, indent=0)
print(collections.Counter(s["tech"] for s in sel if s["cat"]=="juostos"))
print(collections.Counter(s["rl"] for s in sel))
