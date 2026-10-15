# Test B — 2×2-mechanisme: Bambu-project en echte toolpaths

Open [**clutch-matrix.3mf**](clutch-matrix.3mf) als **project** en behoud de opgeslagen printer-, filament- en processinstellingen. De archive bevat de benoemde meshes, echte geslicete G-code en Bambu-previews. De status en montagevoorwaarden staan in [test.md](test.md); een slicercontrole is geen fysieke goedkeuring.

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
| Brim | **Alleen buiten, 3 mm breed, 0 mm afstand tot onderdeel** |
| Compensaties | XY-contour **0**, XY-gat **0**, elephant foot **0 mm**, circle compensation uit, krimp 100% |
| Volgorde / overige | **Per laag**; geen automatische oriëntatie, arrangement of schaling; aligned seam, scarf seam uit, arc fitting uit |

## Bambu-raming en broncontrole

- model printing time: 4h 18m 29s; total estimated time: 4h 29m 43s
- total filament length [mm] : 5984.98
- total filament weight [g] : 17.85

**219 lagen; 36 afzonderlijke onderdelen.** Bronafmetingen: 137.46 × 92.30 × 26.32 mm. Dit zijn slicerramingen, geen gemeten printtijd of verbruik. De totale tijd omvat de officiële start-/eindprocedure; purge en feitelijke kalibratietijd kunnen verschillen.

De opgeslagen 3MF is opnieuw door Bambu Studio geopend en zonder externe profielen opnieuw gesliced. De opgeslagen instellingen bleven gelijk. De G-code is **niet byte-identiek**: de her-slice genereert ook andere extrusiepaden. De nominale bead-footprints zijn laag voor laag vergeleken in [reslice-comparison.json](reslice-comparison.json), en de kritische screens zijn opnieuw uitgevoerd op de her-slice in [reopened-critical-paths.json](reopened-critical-paths.json). Bronfacetten, oriëntatie en schaal zijn onafhankelijk vergeleken; de exacte foutmarge staat in [validation.json](validation.json).

Bij Test B is het maximale symmetrische bead-oppervlakverschil per laag **6,879%**, op Z=23,16 mm waar alleen de schroeven nog worden geprint. De her-slice verandert onder andere de kleine infill-/naadruimten; zij is geen bit- of padgelijkheidsbewijs. Kritische screens zijn op beide versies uitgevoerd: alle nominale rotornekken, tandcomponenten en schroefdoorsneden blijven samenhangend; de lokale draadwandonderbrekingen in de pinnen veranderen van 102 naar 104 laag-/pincombinaties. Zie de exacte resultatenbestanden.

## Oriëntatie, overhangs en kritische paden

Buitenste framehelften liggen met hun brede buitenwand op het bed, registratiepennen omhoog; het middenstuk ligt op zijn vlakke deelvlak. Een eerdere omgekeerde frameoriëntatie met zwevende platen is na padcontrole verworpen. De selectorstaven staan op hun doorlopende rug, inclusief de bedienlippen. Rotoren: vangflens beneden, tanden boven. Inputassen: kraag beneden. Schroeven: DD-tail beneden, met 45° verbreding naar de kraag; het intact overgenomen E-295-schroefprofiel staat verticaal. Pinnen: **gesloten top op het bed**, binnendraad bovenaan. Dat vermijdt support in de draad en de moeilijk verwijderbare oude CAD-voeten, maar deze omgekeerde oriëntatie is nog niet fysiek bewezen.

De schroeven zijn **26,32 mm hoog op een DD-voet van 2,2 × 1,6 mm** (circa 3,10 mm² daadwerkelijke eerste-laagfootprint). De eerder onderzochte 0,12-mm brimspleet liet de brim los staan en is vervangen door **0 mm afstand**, zodat de externe brim werkelijk contact maakt. Het is één laag van 0,12 mm, niet de oude 0,24-mm CAD-voet. Brimcontact, lage snelheid/versnelling en begrensde testlengte helpen de hechting; geen supportpad zien bewijst geen stabiliteit. Controleer de eerste lagen, en stop bij loskomen, scheefstand of aanlopen van de nozzle. Na afkoelen alleen de externe brim losmaken; het aandrijfprofiel en de draad niet wegschuren. Noteer schade en benodigde nabewerking.

De volledige padcontrole vindt **0 lagen met nieuwe losstaande footprintcomponenten**, maximale vrije brug-/overhangmiddellijn **5.120 mm**, maximale afstand van een begin/eindpunt tot vorige-laagmateriaal **0.823 mm**. Er zijn **geen supportpaden**. Deze waarden gebruiken nominale lijnbreedten; samenhang of overlap bewijst geen hechting, doorhang, sterkte of passing.

De lokale screens controleren de vrijgehouden centrale DD-/pinboring, de dunne rotornek en twee afzonderlijke doorlopende tanddelen. Zie de feitelijke tellingen in [critical-paths.json](critical-paths.json), het [overzicht van lagen](toolpaths.png) en de [kritische detailpaden](critical-toolpaths.png). Ook een lokaal gesloten éénlijnswandje is nog geen gekwalificeerde torsiesectie.

**Specifieke negatieve padbevindingen:** alle 360 gecontroleerde gewone buis-/laagcombinaties hebben een gesloten wand; in de draadzone zijn **102 van 200** combinaties lokaal niet gesloten, maximaal **0,207 mm** langs de nominale wandmiddellijn. Her-slice: **104/200**, maximum eveneens circa **0,207 mm**. Dit zijn nominale paden, geen gemeten fysieke gaten. Het sluit aan bij de bekende lokale Arachne-onderbrekingen van E-295, maar de nieuwe printoriëntatie moet nog fysiek worden beproefd. Alle 560 centrale pinboringschecks blijven vrij.

Alle 80 gecontroleerde rotor-neklagen zijn gesloten; alle 160 tand-/laagcombinaties bevatten twee samenhangende tanden. In alle 528 gecontroleerde externe schroefdraad-/laagcombinaties is het gedeponeerde materiaal één samenhangend vlak. In het werkende draaddeel blijft de creststraal minimaal **1,592 mm**; de overgenomen tip loopt smaller toe. De kleine centrale schroefkern is niet overal volledig gevuld: de nominale dekking van de Ø0,9-mm middenschijf zakt lokaal tot **84,4%**, ondanks 100% ingestelde infill. Dit meet geen echte porositeit of sterkte; vermijd belastings-/breukproeven. Het volledige profiel en de schroefpassing vragen de handtest.

[Eerste-laagcontrole van de vier schroefvoeten](brim-contact.json): met 0-mm brimspleet is de berekende afstand **0 mm** en is de nominale footprintoverlap met de brim **0,042–0,044 mm²** per schroef. Dat toont contact in de toolpaths; werkelijke hechting, rechtop blijven en schadevrije brimverwijdering zijn onbekend.

De beperkte proef moet axiale vangst, rotatiefrictie, schuifpassing, laagsterkte, aangrijpen en vrijgeven fysiek toetsen. FDM kan hoeken afronden, brugdaken laten doorhangen en toleranties per exemplaar veranderen. Gebruik de testuitkomst, geen schatting van printerprecisie, om een passing te kiezen.

[Herkomst en hashes](build-provenance.json) · [Reproduceerbare builder en padcontrole](../../tools/curated-experiment-checks/E-297/printing/reproduction.md). Controle is uitgevoerd met de Bambu-CLI, softwaregerenderde Bambu-previews en onafhankelijke inspectie van de echte G-code. Geen interactieve GUI-handcontrole, printerverbinding of fysieke print uitgevoerd.
