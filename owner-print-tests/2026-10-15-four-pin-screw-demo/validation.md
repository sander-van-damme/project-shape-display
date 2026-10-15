# CAD-, maakbaarheids- en bewijsgrenzen van de vierpinproef

Dit is een **DEFERRED fysieke proef**, geen gevalideerd werkend prototype. De STL-geometrie is volledig uitgewerkt en gecontroleerd. De fysieke passing, wrijving, brugkwaliteit en statische houding zijn onbekend.

## Geometrie en werking

Alle maten zijn CAD-maten in mm. Referentie `z=0` is de onderkant van de gemonteerde onderplaat.

| Onderdeel / vlak | Maat / positie | Functie en marge |
|---|---|---|
| Vier middelpunten | `(±2,54; ±2,54)` | 5,08 mm pitch, 5 pinnen per D&D-inch |
| Onderplaatvloer | z 0–1,2, vier toegangsgaten Ø3,6 | Onderste axiale kraagsteun; nominale radiale opleg 0,4 |
| Schroefkraag | Ø4,4 × 3,6; z 1,2–4,8 | Eén stuk met de schroef; kraagkamer 3,9 hoog geeft 0,3 axiale ruimte |
| Hex in kraagonderzijde | 2,2 AF; 2,0 rechte diepte; 0,4 inloop naar 3,0 AF | 2,0 AF handbit; 0,1 speling per vlak; 1,2 dik dak; niet als automatische capture gevalideerd |
| Lagerhals / lagerdek | Ø3,2 × 1,9; dek z 5,1–6,7 met Ø3,5 gaten | 0,15 radiale speling; kraag kan niet door dek of onderplaat |
| Draad boven hals | Ø3,2; lengte 16; lead 3; diepte 0,9; 90° profiel | Dezelfde BOSL2-kernel als de recente brede fysieke test, met afgeschuinde punt |
| Vierkante pin | 4,4 breed × 18 lang | Onderste 6 mm binnendraad; daarboven 3,52 vierkante holte; gesloten 0,8 dikke top |
| Lage/hoge geleiding | z 14–15,2 / 24,2–25,4 | Vierkante gaten 4,60; per-zijde speling 0,10; webben 0,48; middenafstand 10,2 |
| Pinonderzijde | z 7,7–13,7, plus maximaal 0,3 kraaglift | Volle 6 mm draadgrijping over de proefslag; geen bedoelde botsing met lagerdek |
| Pintop | z 25,7–31,7; neutraal 28,7 | Fysieke neutraalpositie 3 mm boven laag; maatje 3,3 boven frame |

De vorm van het frame is alleen een kleine demonstratiehouder. Het is geen voorstel om duizenden afzonderlijke 24 mm frames te assembleren. Per pin zijn er twee geprinte delen: schroef inclusief kraag/socket, en hol staafje. De onderplaat, kooi en handkop worden gedeeld. Tape houdt alleen de twee gezamenlijke framedelen bijeen.

Het koppelpad is: **hand → hexkop → schroefkraag → schroefdraad → geleide pin**. Het reactiekoppel gaat van de pin via twee vierkante gaten naar de kooi. De ring onder de kraag draagt neerwaartse axiale kracht; het lagerdek begrenst opwaartse dockkracht. De buur heeft een eigen schroef en wordt nergens bewust gekoppeld. De brede handgreep blijft ruim onder het raster; alleen de smalle bit gaat door een toegangsgat. Bij verplaatsen moet de bit volledig teruggetrokken zijn.

### Antirotatie, scheefstand en toppen

Alleen een nominale topvoeg vermelden zou onvoldoende zijn. Met de twee gaten kan een pin iets verplaatsen, kantelen en om zijn as draaien. De conservatieve rechthoekige geleidingsgrens gebruikt het gehele gat als maximale doorsnede-enveloppe. Met 10,2 mm geleidingsafstand, 0,20 mm totale zijdelingse vrijheid en maximaal 7,2 mm top-overstek boven het bovenste geleidingsmidden (inclusief axiale kraaglift) resteert:

`minimale nominale buurvoeg ≥ 5,08 − 4,60 − 2 × 7,2 × (4,60 − 4,40)/10,2 ≈ 0,198 mm`.

Dit is een conservatieve nominale CAD-grens, geen gemeten printertolerantie. Een te ruim geprint gat, dunner staafje, elastische doorbuiging of kapotte web kan de marge opeten. De fysieke test moet dus ook daadwerkelijk buurcontact bekijken. De geleidingspasvorm kan omgekeerd te nauw uitvallen; dat is een apart resultaat van de draadpassing.

Een 4,88 mm top is niet stilzwijgend aan dit prototype toegevoegd: zelfs een rechte 4,4 mm pin in een 4,60 mm gat kan genoeg yaw toelaten om de projectie van zo'n kap boven 5,08 mm te brengen. Scheefstand en zijdelingse vrijheid komen daar nog bij. De huidige 4,4 mm top behoudt dezelfde doorsnede als het geleide staafje en heeft 0,68 mm nominale voeg. Een vrijwel gesloten terreinoppervlak vraagt daarna een expliciete kap-/geleidingproef.

### Axiale opsluiting en koppeling

Twee tegenovergesteld verschoven lagerhalzen kunnen samen 0,30 mm centrumafstand verliezen. De twee kragen blijven nominaal `5,08 − 4,4 − 0,30 = 0,38 mm` vrij. De onderste kraagopleg is 0,4 mm radiaal en wordt aan één kant 0,25 mm bij maximale halsverschuiving; sterkte van die PLA-opleg is nog niet gemeten. De 0,3 mm axiale kamerruimte kan bij aankoppelen de geselecteerde pin iets optillen. Dat moet los van echt buurmeebewegen worden genoteerd.

De hex werkt in twee richtingen maar vraagt hoekfasering; de hand zoekt die voorzichtig. De CAD-controle valideert alleen een reeds uitgelijnde, correct gefaseerde bit, geen willekeurige blind docking. Een geprinte 2 mm bit kan afronden voordat een socket goed beoordeeld is; een aanwezige metalen 2 mm sleutel onderscheidt die foutbronnen. Een motor of automatische veerkop wordt niet meegeleverd.

Bij lead 3 en een typische steekdiameter 2,3 is de spoedhoek circa 22,6°. Voor een 90° inbegrepen draadprofiel ligt de elementaire statische zelfremgrens rond `μ > tan(22,6°) × cos(45°) ≈ 0,294`. Werkelijke wrijving is onbekend en verandert met print, materiaal en slijtage. Een soepel handpaar bewijst dus geen houden zonder kop. Daarom bevat de proef loslaten en een zeer lichte handmatige observatie.

## Mesh- en montagecontrole

[validate.py](validate.py) gebruikt de werkelijk geleverde STLs en manifold3d via trimesh. Per tolerantieplaat zijn er 12 gesloten lichamen met consistente oriëntatie, alle op z=0. Het controleert 25 hoogtes over 6 mm slag, elk bij twee axiale kraagstanden, dus **150 schroef-pinposities totaal**. Voor iedere stand worden frameclearance en een correct gefaseerde onderkop tegenover geselecteerde en naburige schroeven getest. Alle berekende intersectievolumes zijn nul; de [resultaat-JSON](cad-validation.json) bevat versies, dimensies en SHA-256-hashes.

Deze test gebruikt ideale coaxiale schroefmontage. De hierboven genoemde kantelgrens is een afzonderlijke geometrische analyse, geen force-/deflectiesimulatie. Er is geen beweerde gemeten koppel-, snelheids- of houdkrachtwaarde.

De [doorsnede](assembly-section.png) is uit de geleverde nominale STL-lichamen gemaakt, met links laag, rechts hoog en één geplaatste handkop. [render-section.py](render-section.py) reproduceert die afbeelding zonder externe CAD-export.

## Slicercontrole en ontworpen ondersteuning

De onderdelen hebben bewuste bedcontacten: brede kooiwand liggend, onderplaat vlak, schroeven op hun kraag en pinnen op hun vierkante rand. Een 3 mm **buitenbrim met nul spleet** vergroot het contact van de schroef tot circa 10,4 mm diameter en de pin tot een vergelijkbare buitenmaat. Binnenbrim en automatische supports blijven uit. Deze 18–21,5 mm korte delen plus brim beperken het eerdere lange-staafrisico; dat is nog geen fysieke hechtingsgarantie.

Alle drie definitieve STL-bestanden zijn onafhankelijk gesliced met PrusaSlicer 2.7.2, 0,12 mm lagen, Arachne en 3 mm buitenbrim: 200 lagen en circa 1 uur 42 minuten; 0,15 / 0,175 / 0,20 respectievelijk 9,39 / 9,38 / 9,37 g. Het [vergelijkingsprofiel](../../tools/curated-experiment-checks/E-295/validation/comparison-012.ini), [nominale mesh-/padanalyse](../../tools/curated-experiment-checks/E-295/validation/demo-0175.json), [brugdetails](../../tools/curated-experiment-checks/E-295/validation/demo-bridge-details.json) en [padbeelden](../../tools/curated-experiment-checks/E-295/validation/demo-toolpaths.png) zijn bewaard. De rapporten bevatten hashes van de exact geslicede STLs. De slice bevat geen niet-ondersteunde losse laagcomponenten. Er zijn **waarschuwingen over floating bridge anchors, loose extrusions en long bridging extrusions**; die mogen niet als een schone fysieke printkwalificatie worden weggepoetst. Een doorlopende bruglijn van circa 18,34 mm in de kooi heeft tussensteun op de middelste plaat; de grootste daadwerkelijk vrije overspanning is 8,98 mm. Bij het pindak is de vrije centerlijnoverspanning 2,64 mm, binnen de 3,52 mm CAD-holte. Sommige brugankers beginnen op een overbruggende perimeter van dezelfde laag, tot 1,515 mm van materiaal in de vorige laag. Daarom worden de ankers niet als volledig ondersteund gekwalificeerd: lokale doorhang blijft een echte fysieke onzekerheid. De eigenaar controleert dezelfde kritieke plaatsen in Bambu Studio, in het daadwerkelijk gebruikte profiel.

Het ontbreken van slicersupport is op zichzelf geen bewijs van goede printstabiliteit. Het gesloten pindak, hex-dak en de liggende kooigaten moeten hun korte overspanning in echt PLA nog aantonen. Het is ook niet toegestaan supports in de draad te plaatsen om een waarschuwing te verbergen. Daarom blijft deze proef een **voorwaardelijk vervolg na P1**, met expliciete inspectie-/stopcriteria.

## Reproductie

De eigenaar gebruikt uitsluitend de geleverde STL. Voor CAD-onderhoud zijn OpenSCAD, git, trimesh, numpy en manifold3d nodig; voor de doorsnede ook matplotlib. De gepinde BOSL2-checkout moet schoon zijn en exact revision `136e6367e65d52196a3ea51d03156f8b622c60fc` hebben.

```sh
python owner-print-tests/2026-10-15-four-pin-screw-demo/generate.py --bosl2 work/compact-screw-fit/BOSL2 --scratch work/four-pin-demo
python owner-print-tests/2026-10-15-four-pin-screw-demo/validate.py
python owner-print-tests/2026-10-15-four-pin-screw-demo/render-section.py
```

`generate.py` bewaart de bestaande `OPENSCADPATH`, controleert de libraryversie, vangt OpenSCAD-output op en faalt bij waarschuwingen/fouten. De drie platen zijn alternatieven; na een fysieke beslissing wordt hoogstens één gekozen. Er ontstaat geen autonome printwachtrij of vervolgtakenketen.
