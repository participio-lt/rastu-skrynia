import json, sys, os, colorsys
from PIL import Image, ImageDraw
S = sys.argv[1]
def dist(a,b): return sum((x-y)**2 for x,y in zip(a,b))**0.5
def family(rgb):
    r,g,b = [c/255 for c in rgb]
    h,l,s = colorsys.rgb_to_hls(r,g,b); h*=360
    if l < 0.17: return "juoda"
    if l > 0.80 and s < 0.35: return "balta"
    if s < 0.16 or (s < 0.25 and l < 0.3): return "pilka"
    if 15 <= h < 48 and (l < 0.42): return "ruda"
    if h < 12 or h >= 345: return "raudona"
    if h < 40: return "oranžinė"
    if h < 68: return "geltona"
    if h < 170: return "žalia"
    if h < 255: return "mėlyna"
    if h < 300: return "violetinė"
    return "rožinė"
items = json.load(open(f"{S}/data/new2.json")) + json.load(open(f"{S}/data/commons_items.json"))
out, missing = [], []
for s in items:
    p = f"{S}/dl_commons/{s['id']}.raw" if s.get("via") == "commons" else f"{S}/dl/{s['id']}.raw"
    try:
        im = Image.open(p); im.load(); im = im.convert("RGB")
    except Exception as e:
        import traceback; traceback.print_exc() if len(missing) < 1 else None; missing.append(s["id"]); continue
    if im.width > 400: im = im.resize((400, round(im.height*400/im.width)), Image.LANCZOS)
    if im.width < 120 or im.height < 120: missing.append(s["id"]); continue
    im.save(f"{S}/img2/{s['id']}.jpg", "JPEG", quality=78, optimize=True, progressive=True)
    s["w"], s["h"] = im.size
    sm = im.copy(); sm.thumbnail((120,120)); W,H = sm.size; px = sm.load()
    border = [px[x,y] for x in range(W) for y in (0,1,H-2,H-1)] + [px[x,y] for y in range(H) for x in (0,1,W-2,W-1)]
    bg = tuple(sorted(c[i] for c in border)[len(border)//2] for i in range(3))
    allp = [px[x,y] for x in range(W) for y in range(H)]
    fg = [c for c in allp if dist(c,bg) > 42]
    if len(fg) < 0.12*len(allp): fg = allp
    q = Image.new("RGB", (len(fg),1)); q.putdata(fg)
    q = q.quantize(colors=7, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:21]; counts = sorted(q.getcolors(), reverse=True)
    cols = []
    for n, idx in counts:
        c = tuple(pal[idx*3:idx*3+3]); share = n/len(fg)
        for cc in cols:
            if dist(cc["rgb"], c) < 30: cc["share"] += share; break
        else: cols.append({"rgb": c, "share": share})
    cols = sorted([c for c in cols if c["share"] >= 0.05], key=lambda c: -c["share"])[:5]
    s["pal"] = ["#%02x%02x%02x" % c["rgb"] for c in cols]
    fam = {}
    for c in cols: fam[family(c["rgb"])] = fam.get(family(c["rgb"]),0) + c["share"]
    s["fam"] = sorted([f for f,v in fam.items() if v >= 0.10], key=lambda f: -fam[f])
    out.append(s)
json.dump(out, open(f"{S}/data/new2_processed.json","w"), ensure_ascii=False)
print("ok", len(out), "missing", len(missing))
from collections import defaultdict
bycat = defaultdict(list)
for s in out: bycat[s["cat"]].append(s)
COLS, T, PER = 12, 108, 120
for cat, its in bycat.items():
    for k in range(0, len(its), PER):
        chunk = its[k:k+PER]; rows = (len(chunk)+COLS-1)//COLS
        sheet = Image.new("RGB", (COLS*T, rows*(T+12)), "white"); d = ImageDraw.Draw(sheet)
        for i, s in enumerate(chunk):
            im = Image.open(f"{S}/img2/{s['id']}.jpg"); im.thumbnail((T-4,T-4))
            x, y = (i%COLS)*T, (i//COLS)*(T+12)
            sheet.paste(im, (x+2, y+2)); d.text((x+2, y+T-1), str(k+i), fill="red")
        sheet.save(f"{S}/sheets2/{cat}_{k//PER}.png")
print({k: len(v) for k,v in bycat.items()})
