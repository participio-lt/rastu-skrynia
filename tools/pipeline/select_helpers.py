import json, sys, re, hashlib, collections, random
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

def make(it, cat):
    if rights_label(first(it.get("rights"))) == "Kita": return None
    t = first(it.get("title")); d = " ".join(it.get("dcDescription") or []).strip()
    ts = first(it.get("edmTimespanLabel"))
    return {"id": hashlib.sha1(it["id"].encode()).hexdigest()[:10], "eid": it["id"], "cat": cat, "title": t, "desc": d,
        "creator": first(it.get("dcCreator")), "provider": first(it.get("dataProvider")),
        "date": ts if isinstance(ts, str) else (ts or {}).get("def",""), "year": first(it.get("year")),
        "place": (first(it.get("edmPlaceLabel")) or {}).get("def","") if it.get("edmPlaceLabel") else "",
        "rights": first(it.get("rights")), "rl": rights_label(first(it.get("rights"))),
        "europeana": "https://www.europeana.eu/item" + it["id"], "source": first(it.get("edmIsShownAt")),
        "thumb": first(it.get("edmPreview")) + "&size=w400", "tech": technique(t + " " + d) if cat == "juostos" else ""}
