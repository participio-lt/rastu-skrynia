# Raštų skrynia

Lietuvių tradicinių rankdarbių įkvėpimo katalogas: juostos, margučiai, sodai, karpiniai, kaukės, kryžiai, prieverpstės ir kiti raštai iš Lietuvos muziejų rinkinių.

Svetainė: https://participio.lt/rastu-skrynia/

Projektą kuria [Lietuvos piliečių mokslo asociacija](https://www.pilieciumokslas.lt/) ir [VšĮ „Participio“](https://participio.lt/).

## Ką galima daryti

- Naršyti 1411 objektų pagal rūšį, spalvą, tikslų atspalvį, etnografinį regioną ir juostų techniką.
- Perjungti du vaizdus: **Katalogas** (tvarkingas sąrašas) ir **Koliažas** (išmėtytos skiautės, kurias galima tempti).
- Atverti objektą: muziejaus aprašas, kilmės vieta, datavimas, medžiagos, licencija ir nuoroda į pilną įrašą.
- Rasti pamokas ir šaltinius skiltyje „Kaip pasidaryti“ (64 patikrintos nuorodos, pirmiausia LNKC nematerialaus paveldo sąvado įrašai).
- Išsisaugoti patikusius objektus (lieka tik toje naršyklėje).

Lankytojų darbų įkėlimas veikia tik Claude artefakto versijoje, nes jam reikia Claude duomenų saugyklos. GitHub Pages versijoje šis mygtukas nerodomas.

## Iš kur duomenys

- **Europeana** (europeana.eu): objektai, kuriuos paskelbė Lietuvos muziejai ir bibliotekos. Įtraukti tik įrašai su licencija, leidžiančia nekomercinį rodymą: viešasis domenas, CC0, CC BY, CC BY-SA ir CC BY-NC variantai.
- **Wikimedia Commons**: dalis šiaudinių sodų nuotraukų (CC BY-SA ir viešasis domenas).
- Į rinkinį neįtrauktos kino, fotografijų ir negatyvų juostos, apdovanojimų juostelės, dokumentai, nuotraukos, tapyba ir ne Lietuvoje sukurti dirbiniai. Visi paveikslėliai buvo peržiūrėti rankiniu būdu.
- Regionas nurodomas tik tada, kai jį aiškiai rodo muziejaus nurodyta kilmės vieta.

Paveikslėliai yra sumažintos peržiūros kopijos (iki 400 px pločio). Kiekvieno objekto licencija ir autorius nurodyti jo kortelėje, o pilnas įrašas pasiekiamas per nuorodą. Paveikslėliams galioja jų pačių licencijos, ne šios saugyklos kodo licencija.

Duomenys surinkti 2026-10-15.

## Struktūra

```
index.html            svetainė (GitHub Pages)
img/                  390 objektų paveikslėliai po vieną failą
b/                    likusių objektų paveikslėliai, sugrupuoti po 10 į JSON paketus
data/page_data.json   duomenys, įterpiami į puslapį
data/items.json       tie patys objektai su Europeana identifikatoriais
data/tutorials.json   „Kaip pasidaryti“ nuorodos
tools/template.html   puslapio šablonas (stilius, logika)
tools/build_page.py   surenka index.html iš šablono ir duomenų
tools/pipeline/       skriptai, kuriais duomenys buvo surinkti ir atrinkti
```

## Kaip atnaujinti puslapį

Pakeitus `tools/template.html` arba failus `data/` aplanke:

```
python3 tools/build_page.py
```

Peržiūrėti savo kompiuteryje:

```
python3 -m http.server 8000
```

ir atverti http://localhost:8000.

## Apie surinkimo skriptus

`tools/pipeline/` aplanke yra skriptai, kurie buvo paleisti vieną kartą surenkant duomenis: paieška Europeana API (`eu.py`, `collect.py`), atranka (`pick.py`, `select_helpers.py`, `extend.py`), paveikslėlių apdorojimas ir spalvų paletės (`process.py`, `proc2.py`), regionų ir medžiagų išrinkimas iš pilnų įrašų (`enrich.py`) ir paketų kūrimas (`build2.py`). Jie palikti tam, kad būtų aišku, kaip duomenys atsirado. Norint juos paleisti iš naujo, reikia Python, Pillow ir Europeana API rakto.
