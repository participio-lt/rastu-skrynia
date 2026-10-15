import json, sys, re, collections, os
S = sys.argv[1]
items = json.load(open(f"{S}/data/all2.json"))
def vals(p, key):
    v = p.get(key) or {}
    out = []
    for lang in ("lt", "def", "en"):
        for x in v.get(lang, []):
            if isinstance(x, str) and not x.startswith("http") and x not in out: out.append(x.strip())
    return out
# Municipalities that sit wholly inside one ethnographic region; border municipalities are left untagged on purpose
REG = [
 ("Aukštaitija", r"aukštait|rokišk|kupišk|biržų|biržai|pasvali|panevėž|utenos|utena|zarasų|zarasai|ignalin|anykšč|molėt|ukmerg|švenčion|visagin|pakruoj"),
 ("Žemaitija", r"žemait|telši|plung|rietav|mažeik|skuod|šilal"),
 ("Dzūkija", r"dzūk|varėn|alytaus|alytus|druskinink|lazdij|merkin|marcinkon"),
 ("Suvalkija", r"suvalk|sūduv|marijampol|vilkaviš|šakių|šakiai|kalvarij|kazlų rūd"),
 ("Mažoji Lietuva", r"mažosios lietuvos|mažoji lietuva|klaipėdos krašt|klaipėdos m\.|šilutė|šilutės|rusnė|nidos|neringos|pagėg"),
]
SKIP_PLACE = re.compile(r"^(lietuva|lithuania|litauen)$", re.I)
stats = collections.Counter(); med_c = collections.Counter()
for s in items:
    s["place"] = ""; s["date"] = ""; s["mat"] = []
    f = f"{S}/rec/{s['id']}.json"
    if s.get("via") != "commons" and os.path.exists(f):
        try: obj = json.load(open(f))["object"]
        except Exception: obj = {}
        spatial, created, medium = [], [], []
        for p in obj.get("proxies", []):
            spatial += vals(p, "dctermsSpatial"); created += vals(p, "dctermsCreated"); medium += vals(p, "dctermsMedium")
        places = [re.sub(r",?\s*Lietuva$", "", x).strip() for x in spatial if not SKIP_PLACE.match(x)]
        places = [x for x in dict.fromkeys(places) if x]
        s["place"] = places[0] if places else ""
        s["date"] = created[0] if created else ""
        s["mat"] = list(dict.fromkeys(m.lower() for m in medium))[:5]
        for m in s["mat"]: med_c[m] += 1
    txt = " ".join([s["place"], s["title"], s["desc"]]).lower()
    ptxt = s["place"].lower()
    hits_place = [n for n, rx in REG if ptxt and re.search(rx, ptxt)]
    hits = hits_place or [n for n, rx in REG if re.search(rx, (s["title"] + " " + s["desc"]).lower())]
    s["reg"] = hits[0] if len(set(hits)) == 1 else ""
    stats["place" if s["place"] else "noplace"] += 1; stats["date" if s["date"] else "nodate"] += 1
    stats["reg:" + (s["reg"] or "-")] += 1
print(stats)
print("materials", med_c.most_common(25))
print("dates", collections.Counter(s["date"] for s in items).most_common(12))
print("places", collections.Counter(s["place"] for s in items if s["place"] and not s["reg"]).most_common(20))
json.dump(items, open(f"{S}/data/all3.json", "w"), ensure_ascii=False)
