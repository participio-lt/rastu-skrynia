"""Builds index.html (GitHub Pages) and artifact.html (Claude artifact body) from the template and data."""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "tools" / "template.html").read_text(encoding="utf-8")
data = (root / "data" / "page_data.json").read_text(encoding="utf-8").replace("</", "<\\/")
tut = json.dumps(json.loads((root / "data" / "tutorials.json").read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")
page = tpl.replace("/*__DATA__*/", data).replace("/*__TUT__*/", tut)

cut = page.index("</style>") + len("</style>")
head, body = page[:cut], page[cut:]
desc = "Lietuvių tradicinių rankdarbių įkvėpimo katalogas: juostos, margučiai, sodai, karpiniai, kaukės ir kiti raštai iš Lietuvos muziejų."
(root / "index.html").write_text(
    '<!doctype html>\n<html lang="lt">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    f'<meta name="description" content="{desc}">\n' + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n",
    encoding="utf-8")
(root / "artifact.html").write_text(page, encoding="utf-8")
print("index.html", round(len(page.encode()) / 1024), "KB")
