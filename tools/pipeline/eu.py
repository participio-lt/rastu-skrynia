import json, sys, urllib.request, urllib.parse, collections
API="https://api.europeana.eu/record/v2/search.json"
def search(query, rows=100, cursor="*", qf=(), reuse=("open","restricted"), profile="rich"):
    params=[("wskey","api2demo"),("query",query),("rows",rows),("cursor",cursor),("profile",profile)]
    params+= [("qf",q) for q in qf]
    params+= [("reusability",r) for r in reuse]
    url=API+"?"+urllib.parse.urlencode(params)
    import subprocess
    out=subprocess.run(["curl","-s","--max-time","90",url],capture_output=True,check=True).stdout
    return json.loads(out)
if __name__=="__main__":
    q=sys.argv[1]; qf=sys.argv[2:] 
    d=search(q, rows=100, qf=qf)
    print("total", d.get("totalResults"))
    types=collections.Counter(); rights=collections.Counter(); prov=collections.Counter()
    for it in d.get("items",[]):
        for t in it.get("dcType",[]) or ["-"]: types[t]+=1
        for t in it.get("rights",[]): rights[t]+=1
        for t in it.get("dataProvider",[]): prov[t]+=1
    print("TYPES", types.most_common(15)); print("RIGHTS", rights.most_common(8)); print("PROV", prov.most_common(8))
    for it in d.get("items",[])[:40]:
        print("-", (it.get("title") or [""])[0][:70], "|", (it.get("dcType") or [""])[0][:30], "|", ((it.get("dcDescription") or [""])[0])[:90].replace("\n"," "))
