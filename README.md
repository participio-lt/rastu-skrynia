# Raštų skrynia

Lietuvių tradicinių rankdarbių įkvėpimo katalogas: juostos, margučiai, sodai, karpiniai, kaukės, kryžiai, prieverpstės ir kiti raštai iš Lietuvos muziejų rinkinių.

Svetainė: https://participio.lt/rastu-skrynia/

Projektą kuria [Lietuvos piliečių mokslo asociacija](https://www.pilieciumokslas.lt/) ir [VšĮ „Participio“](https://participio.lt/).

## Ką galima daryti

- Atsidarius puslapį juodame fone objektų nuotraukos iš visų rūšių išsiskleidžia iš vidurio į tankų debesį, kaskart išdėliotą vis kitaip. Objektai lėtai plūduriuoja ir pasislenka pagal pelę. Užvedus pelę ant objekto, jis padidėja, kaimynai pasitraukia, o kairėje jis parodomas didesnis su pavadinimu, vieta ir data. Kol pelė nėra ant objekto, niekas nepažymėta. Kitus objektus rodo rodyklės viršuje dešinėje, klaviatūros rodyklės arba braukimas telefone: senas debesis išlekia, naujas išsiskleidžia.
- Viršuje dešinėje vaizdą galima perjungti į „Lenta“. Lentoje tie patys objektai išdėlioti tinkleliu. Juos galima rikiuoti pagal spalvą, laiką, rūšį ar regioną, o bet kurį objektą nutempti, kur patinka. Paspaudus „Spalva“, atsiranda spalvų taškeliai: taškelis palieka tik tos spalvos objektus. „Sutvarkyti“ grąžina objektus į vietas.
- Meniu „Rūšys“ ir „Ieškoti“ leidžia rinktis rūšį, žodį, spalvą ar regioną. Filtras galioja abiem vaizdams. Debesies vaizde nuotraukos tada susitvarko į tvarkingą tinklelį. „Išvalyti“ grąžina debesį.
- Pasirinkus juostas, galima rinktis techniką (rinktinė, pintinė ir kitos).
- Atverti objektą: muziejaus aprašas, kilmės vieta, datavimas, medžiagos, licencija ir nuoroda į pilną įrašą. Iš objekto spalvų galima rasti kitus panašių spalvų objektus.
- Rasti pamokas ir šaltinius per „Kaip pasidaryti“ (64 patikrintos nuorodos, pirmiausia LNKC nematerialaus paveldo sąvado įrašai).
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
