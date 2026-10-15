import sys, json, re, collections
sys.path.insert(0, sys.argv[1])
from eu import search
OUT = sys.argv[2]
PHOTO = "http://data.europeana.eu/concept/48"
# Global exclusions: anything that is not a craft object
BAD = re.compile(r"negatyv|nuotrauk|fotograf|kino|film|magnet|garso|ordin|medal|apdovanoj|ženkl|alpinist|kartotek|masoni|riterio|kariuomen|redaktor|leidėj|portret|ekspozicij|paroda|atvirukas|plakatas|brėžinys|eskizas|projektas|ansambl|moneta|dirbtuv|audėjos|koklis|pilkapyn|suvenyr|jubiliejin|proginis|taupyklė|seifas|banko|indėnų|pekino|metalinė kaukė|vaikų krikštas|jėzaus|kristaus|tikybos|parašė|kortelė|mokykl|skaut|reprodukc|piešinys|grafika|raižinys|akvarel|tapyba|aliejus", re.I)
CATS = [
 ("juostos", ['title:(juosta OR juostos OR juostelė OR juostų)', '"rinktinė juosta"', '"pintinė juosta"', '"vytinė juosta"', '"tautinė juosta"'],
   r"juost", r"skardelė|šluotelė|adata|verpstukas|peiliukas|plokštelė|takelis|kilim|arnotas|dalmatika|kapa\b|galionas|nėrin|vinjet|rankšluost|diržo|sagt|ženkliuk|antsiuv|raištis|apyrank|tilto|žemėlap|nugarėl|presas|archyv|vandens|indo|kauno pilis", 80),
 ("sodai", ['"šiaudinis sodas"', 'title:(sodas OR sodai OR sodelis) AND (šiaudų OR šiaudinis OR šiaudelių)', 'title:šiaudinis', 'title:šiaudinukas'],
   r"sod|šiaud", r"vienuolyn|namas|pastatas|kolektyv|dvarinink|fontan|sakur|muziejaus sodas|girios|medeinos|oi,", 40),
 ("margučiai", ['title:(margutis OR margučiai OR "velykų kiaušinis" OR "velykinis kiaušinis")'],
   r"margut|kiaušin", r"balius|susirašinėj|dzimdzi", 40),
 ("verbos", ['title:(verba OR verbos)', '"vilniaus verba"'],
   r"verb", r"robertas|operatori|režisier|jūreivis|teatro|mitingas|aprūko|kalno|lauko|tako|motyvas", 30),
 ("karpiniai", ['title:(karpinys OR karpiniai)', '"popieriaus karpinys"', '"karpinys" AND "užuolaidėlė"'],
   r".", r"pekino", 30),
 ("rūpintojėliai", ['title:(rūpintojėlis OR dievukas OR "šventojo skulptūrėlė")', '"liaudies skulptūra" AND title:(šventas OR šventoji OR šv.)'],
   r"rūpintojėl|dievuk|šv\.|šventas|šventoji|skulptūr", r"telšių miesto kapinėse|bažnyčioje|akmens|\bį kristų|salako|žlibin", 40),
 ("kryžiai", ['title:("kryžius-saulutė" OR "kryžiaus viršūnė" OR "koplytstulpio viršūnė" OR "geležinis kryžius" OR "kalvystės kryžius")', 'title:(koplytstulpis OR stogastulpis OR koplytėlė) AND TYPE:IMAGE'],
   r"kryž|koplyt|stogastulp", r"procesij|ordinas|garbės", 40),
 ("lovatiesės", ['title:(lovatiesė OR lovatiesės OR "lovatiesės skiautė" OR kilimėlis OR "sieninis kilimėlis" OR staltiesė OR divonas OR užuolaidėlė)'],
   r"lovaties|kilim|staltie|divon|užuolaid", r"juostų|kilimas$", 40),
 ("rankšluosčiai", ['title:(rankšluostis OR rankšluosčiai)'],
   r"rankšluost", r"verpstė|karstui|tauragė", 30),
 ("pirštinės", ['title:(pirštinės OR riešinės OR kojinės)'],
   r"pirštin|riešin|kojin", r"guminės|darbo|boksininko|odinės", 40),
 ("drabužiai", ['title:(prijuostė OR sijonas OR marškiniai OR liemenė OR nuometas OR "galvos raištis" OR karūnėlė OR skara)'],
   r"prijuost|sijon|marškin|liemen|nuomet|karūnėl|skara", r"masoniš|vėrinys|kabuč", 40),
 ("prieverpstės", ['title:(prieverpstė OR prieverpstės OR kultuvė OR kočėlas OR verpstė)'],
   r"prieverpst|kultuv|kočėl|verpst", r"ratelis|rankšluost|sėtuvė", 40),
 ("skrynios", ['title:("kraitinė skrynia" OR "kraičio skrynia" OR kraitskrynia OR kuparas OR "skrynia")'],
   r"skryn|kupar", r"drabužiams|seifas|taupyk|banko", 30),
 ("kaukės", ['title:("užgavėnių kaukė" OR "medinė kaukė" OR kaukė)'],
   r"kauk", r"metalinė|ekspozicij|dujų", 40),
]
def fetch(q, limit=400):
    items, cursor = [], "*"
    while cursor and len(items) < limit:
        d = search(q, rows=100, cursor=cursor, qf=["COUNTRY:Lithuania","TYPE:IMAGE"], profile="standard")
        items += d.get("items", []); cursor = d.get("nextCursor")
    return items
result = {}
for key, queries, want, bad, cap in CATS:
    seen, keep = set(), []
    for q in queries:
        for it in fetch(q):
            i = it["id"]
            if i in seen: continue
            seen.add(i)
            t = (it.get("title") or [""])[0]
            desc = " ".join(it.get("dcDescription") or [])
            if not it.get("edmPreview") or it.get("previewNoDistribute"): continue
            if PHOTO in (it.get("edmConcept") or []): continue
            if not re.search(want, t, re.I): continue
            if BAD.search(t) or re.search(bad, t, re.I): continue
            if key == "juostos" and re.search(r"fotojuost|negatyv|kino|film|kasetė|magnet", desc, re.I): continue
            keep.append(it)
    result[key] = keep
    print(f"{key}: {len(keep)} kept (cap {cap})")
json.dump(result, open(OUT, "w"), ensure_ascii=False)
