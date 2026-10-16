# Test A — koppelingspassing: Bambu-project en echte toolpaths

Open [**clutch-fit.3mf**](clutch-fit.3mf) als **project** en behoud de opgeslagen printer-, filament- en processinstellingen. De archive bevat de benoemde meshes, echte geslicete G-code en Bambu-previews. De status en montagevoorwaarden staan in [test.md](test.md); een slicercontrole is geen fysieke goedkeuring.

## Opgeslagen profiel

De instellingen volgen het door de eigenaar **ongewijzigd geprinte E-295 compacte passingproject**. De nieuwe koppeling, nieuwe schroeftail, cap-omlaag pinoriëntatie en frameonderdelen zijn daarmee nog niet fysiek gekwalificeerd.

| Instelling | Werkelijk opgeslagen waarde |
|---|---|
| Slicer / printer / nozzle | Bambu Studio **02.08.02.61**; **Bambu Lab X1 Carbon**, **0,4 mm**, hardened steel, Standard hotend |
| Materiaal | Generic PLA, Ø1,75 mm; flowratio **0,98**, dichtheid **1,24 g/cm³**, volumestroom maximaal **12 mm³/s** |
| Temperatuur / bed | Nozzle **220 °C**, eerste en overige lagen; **Textured PEI Plate 55 °C** |
| Koeling | Partfan **100%**, eerste laag uit; auxfan **0%**; korte-laagvertraging **8 s**, minimum **10 mm/s** |
| Laag / eerste laag | **0,12 / 0,12 mm**, 100% schaal, bronoriëntatie behouden |
| Wanden / vulling | **Arachne**, **2** nominale wanden; **100% zig-zag**; 5 boven-/onderlagen, bovenschaal 0,6 mm |
| Lijnbreedten | **0,45 mm** nominaal voor alle categorieën; werkelijke Arachne-breedte varieert |
| Arachne | Minimum feature 25%, min. wandbreedte 85% nozzle; overgangslengte 100%, filter 25%, hoek 10°, verdeling 1 |
| Snelheid | Gewone wanden/top/infill/gap fill **30 mm/s**, kleine perimeterdrempel **20 mm**; eerste laag/bruggen **20 mm/s**; overhangstappen **30/20/10/10 mm/s** |
| Reizen / versnelling | **150 mm/s**; model en travel **1000 mm/s²**, eerste-laagextrusie **500 mm/s²**; officiële X1C-startprocedure heeft eigen bewegingen |
| Supports / skirt / raft | **Uit / 0 / 0**; prime tower uit |
| Brim | Uit |
| Compensaties | XY-contour **0**, XY-gat **0**, elephant foot **0 mm**, circle compensation uit, krimp 100% |
| Volgorde / overige | **Per laag**; geen automatische oriëntatie, arrangement of schaling; aligned seam, scarf seam uit, arc fitting uit |

## Bambu-raming en broncontrole

- model printing time: 32m 54s; total estimated time: 44m 8s
- total filament length [mm] : 651.14
- total filament weight [g] : 1.94

**72 lagen; 20 afzonderlijke onderdelen.** Bronafmetingen: 137.60 × 21.00 × 8.60 mm. Dit zijn slicerramingen, geen gemeten printtijd of verbruik. De totale tijd omvat de officiële start-/eindprocedure; purge en feitelijke kalibratietijd kunnen verschillen.

De opgeslagen 3MF is opnieuw door Bambu Studio geopend en zonder externe profielen opnieuw gesliced. De opgeslagen instellingen bleven gelijk. De G-code is **niet byte-identiek**: de her-slice genereert ook andere extrusiepaden. De nominale bead-footprints zijn laag voor laag vergeleken in [reslice-comparison.json](reslice-comparison.json), en de kritische screens zijn opnieuw uitgevoerd op de her-slice in [reopened-critical-paths.json](reopened-critical-paths.json). Bronfacetten, oriëntatie en schaal zijn onafhankelijk vergeleken; de exacte foutmarge staat in [validation.json](validation.json).

Bij Test A bedraagt het maximale symmetrische materiaaloppervlakverschil per laag **1,306%**. Beide versies houden alle nominale en ruime nekdoorsneden gesloten en behouden beide tanden. De krappe variant heeft **2** onderbroken neklagen in het geleverde bestand en **3** na her-slice; dit bevestigt de kwetsbaarheid van die variant. De grootste onderbreking na her-slice is **0,358 mm** langs de nominale nekmiddellijn. Dit is geen gelijkheidsclaim voor fysieke prints.

## Oriëntatie, overhangs en kritische paden

Beide rotorhelften worden met de vlakke vangflens op het bed en de tanden omhoog geprint. De bovenste helft wordt pas bij montage omgedraaid. Het DD-gat blijft open vanaf het bed; alleen het blinde dak vraagt een korte brug. De gekoppelde kambladen staan op hun rug; ook de bedienlip raakt nu het bed. Een eerdere kandidaat met een zwevende lip is na werkelijke padcontrole vervangen. De couponassen hebben hun brede voet op het bed. Er zijn geen aangebouwde dunne, af te knippen E-295-pinvoeten.

De volledige padcontrole vindt **0 lagen met nieuwe losstaande footprintcomponenten**, maximale vrije brug-/overhangmiddellijn **1.493 mm**, maximale afstand van een begin/eindpunt tot vorige-laagmateriaal **0.499 mm**. Er zijn **geen supportpaden**. Deze waarden gebruiken nominale lijnbreedten; samenhang of overlap bewijst geen hechting, doorhang, sterkte of passing.

De lokale screens controleren de vrijgehouden centrale DD-/pinboring, de dunne rotornek en twee afzonderlijke doorlopende tanddelen. Zie de feitelijke tellingen in [critical-paths.json](critical-paths.json), het [overzicht van lagen](toolpaths.png) en de [kritische detailpaden](critical-toolpaths.png). Ook een lokaal gesloten éénlijnswandje is nog geen gekwalificeerde torsiesectie.

**Specifieke negatieve padbevinding:** de krappe 0,12-mm variant heeft in beide exemplaren één lokale onderbreking van de nominale nekwand: rotor 1 op Z=1,80 mm circa 0,356 mm, rotor 2 op Z=1,92 mm circa 0,366 mm langs de geometrische wandmiddellijn. Dit is een nominale bead-footprintscreen, geen gemeten fysiek gat. Vorige-laagmateriaal is aanwezig, maar de plek kan de huls verzwakken. Bekijk [de exacte zwakke plekken](tight-neck-gaps.png) en noteer gaatjes/scheuren; niet als bruikbare passing kiezen wanneer de nek beschadigd is. Alle 40 neklagen van de vier nominale rotoren en alle 20 van de ruime rotoren zijn in deze screen gesloten. De 160 gecontroleerde tand-/laagcombinaties behouden twee afzonderlijke samenhangende tanden.

De beperkte proef moet axiale vangst, rotatiefrictie, schuifpassing, laagsterkte, aangrijpen en vrijgeven fysiek toetsen. FDM kan hoeken afronden, brugdaken laten doorhangen en toleranties per exemplaar veranderen. Gebruik de testuitkomst, geen schatting van printerprecisie, om een passing te kiezen.

[Herkomst en hashes](build-provenance.json) · [Reproduceerbare builder en padcontrole](../../tools/curated-experiment-checks/E-297/printing/reproduction.md). Controle is uitgevoerd met de Bambu-CLI, softwaregerenderde Bambu-previews en onafhankelijke inspectie van de echte G-code. Geen interactieve GUI-handcontrole, printerverbinding of fysieke print uitgevoerd.
