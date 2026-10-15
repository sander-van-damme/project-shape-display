# Printtest — vijf compacte schroefstaafjes van 4,4 mm

> **Nog niet fysiek getest.** Deze kleine plaat toetst of de succesvolle recente draad ook soepel werkt in een slanke pin. De meegeleverde buitenvoetjes zijn tijdelijke handtest-/printsteunen en passen zelf niet in een 5,08-mm raster.

**Status:** READY\
**Prioriteit:** P1\
**Laatst beoordeeld:** 2026-10-15\
**Reden:** één kleine plaat combineert aantoonbaar bewegende schroefgeometrie met de compacte Trial 5-doorsnede; bron, meshes en echte slicerpaden zijn gecontroleerd. Fysieke passing en hechting blijven onbekend.\
**Technische bron:** [E-295 — compacte geometrie en bewijs](../../tools/curated-experiment-checks/E-295/research/compact-geometry.md), voortbouwend op [short-thread-fit](../short-thread-fit/test.md) en het originele Trial 5.

## 1. Waarom deze test? — CTO

**Vraag:** kunnen 4,4-mm vierkante pinnen met 6 mm binnendraad onderaan even prettig heen en terug bewegen als de eerdere brede testmoeren, zonder binnendraad-supports of schuren? Drie nominale exemplaren tonen eventuele printspreiding.

**Beslissing:** drie bruikbare nominale paren rechtvaardigen een kleine onafhankelijke bewegingsdemonstratie. Wisselende nominale resultaten vragen eerst verklaring; alleen succes van de ruimste variant is geen bewijs voor betrouwbare productie. De plaat bewijst geen 40-mm slag, draagkracht of levensduur.

**Afkeur/stop:** harde blokkade, scheuren, loskomende lagen, scheefgeprinte schroef of functionele draad die gevijld/gesneden moet worden. Geen tang, boormachine of krachtproef; stop zodra het blokkeert. Een mislukte variant is een bruikbaar resultaat, geen reden om haar passend te forceren.

## 2. Printklaar — CTO

| Bestand in deze map | Inhoud | Herkenning |
|---|---|---|
| [**compact-five-pairs.stl**](compact-five-pairs.stl) | Complete plaat: vijf schroeven en vijf holle pinnen, tien losse delen | 1–5 stippen op beide voeten; behoud de plaatvolgorde |
| [plate-preview.png](plate-preview.png) | Afbeelding van exact dezelfde STL | Geen montagepositie: alle delen staan apart op het bed |
| [coupon.scad](coupon.scad), [thread-kernel.scad](thread-kernel.scad), [generate.py](generate.py) | Reproduceerbare bron; pinned BOSL2 vermeld in bron | **Niet nodig om te printen** |
| [geometry-validation.json](geometry-validation.json) | Maatvoering, mesh-, volume- en passingchecks | CAD-bewijs, geen fysieke test |

- **Printjobs:** één plaat; geen extra kopieën of brede moeren nodig.
- **Varianten:** 1, 2, 3 identiek: **0,175 mm radiale CAD-relief**; 4: **0,15 mm**; 5: **0,20 mm**. Alle buitenschroeven zijn functioneel identiek. Dit is geen gemeten printercorrectie. Minimale wand bij de drie toleranties: 0,425/0,450/0,400 mm; bovenholtewand 0,44 mm.
- **Geometrie:** buitenschroef d 3,2 mm, spoed 3, diepte 0,9, 90°-profiel uit de recente geslaagde test; draad 16 mm boven een 10 × 10 × 2,4-mm handgreep. Pin 4,4 × 4,4 × 18 mm, binnendraad onderste 6 mm, overige holte 3,52-mm vierkant; bovenkant open voor inspectie. Buitenvoet 12 × 12 × 0,24 mm, geen support in het gat. Hele plaat **72 × 27 × 18,4 mm**.
- **Materiaal/printer:** gewone PLA die je al hebt; Bambu Lab X1 Carbon, **0,4-mm nozzle**, schaal 100%. Geen aankoop nodig.
- **Slicer:** Bambu Studio met **Arachne-wandgenerator**; laaghoogte én eerste laag **0,12 mm**. Twee wanden, 100% infill voor de kleine massieve delen. Nominale lijnbreedte 0,45 mm; laat Arachne dunne wanden variabel vullen. Buitenste/kleine perimeters maximaal 30 mm/s; eerste laag 20 mm/s; acceleratie maximaal 1000 mm/s². Gebruik je normale PLA-temperatuur/koeling en vertragen bij korte lagen. Geen XY-/gat- of elephant-foot-compensatie toevoegen voor deze vergelijking; noteer aanwezige compensaties.
- **Oriëntatie:** rechtop zoals geleverd; niet automatisch draaien. Print per laag, niet object-na-object. Alle tien delen moeten het bed raken.
- **Supports/brim:** **alle supports UIT, automatisch brim UIT, geen raft.** De ontworpen 0,24-mm pinvoet is al de buitenbrim. Er hoeft niets uit het gat te worden verwijderd. Laat de voet tijdens de passingtest zitten; dit voorkomt beschadiging van de dunne wand bij losknippen.
- **Preview:** controleer dat de bovenste vierkante buiswanden aanwezig zijn, alle schroefdraden worden geprint en alle vijf binnengaten open blijven. Geen enkel supportpad hoort in de holte. In de onderste draadzone zijn kleine lokale Arachne-lijnonderbrekingen van circa 0,1 mm gevonden: die zijn op de vorige laag ondersteund, maar kunnen kleine gaatjes of zwakke plekken geven. Inspecteer en noteer die na het printen; geen draad nabewerken. Ontbreekt een groot wanddeel of begint een eiland zonder ondersteuning, print dan niet met dat profiel en bewaar de preview. De meegeleverde bron hoeft niet opnieuw geëxporteerd te worden.
- **Verwachte tijd/materiaal:** onafhankelijke **PrusaSlicer 2.7.2**-vergelijking, 0,12 mm/Arachne: ongeveer **42 minuten / 3,17 g PLA**, exclusief X1C-opstart/kalibratie. CAD-volume 2,538 cm³. Dit is geen gemeten X1C-tijd; Bambu Studio kan afwijken. Er wordt geen printer-G-code meegeleverd.
- **Extra:** handen en liefst een gewone liniaal. Bewaarde onderdelen van short-thread-fit zijn optioneel voor vergelijking, geen nieuwe brede print.
- **STL/printcontrole:** 2026-10-15: tien gesloten afzonderlijke meshes; 305 coaxiale montagestanden zonder CAD-botsing. Exacte plaat met supports uit én aan gesliced: geen support-, brug- of overhangpaden. Onafhankelijke controle van 153 lagen: geen nieuw los deel zonder overlap met de vorige laag. De bovenste buiswand is doorlopend in de paden; onderin blijven de genoemde kleine lijnonderbrekingen. Dat onderbouwt de ontworpen korte print, maar bewijst geen fysieke hechting, laagsterkte of passing. Zie [exacte sliceruitvoer en profiel](../../tools/curated-experiment-checks/E-295/validation/compact-arachne.json), [laagbeelden](../../tools/curated-experiment-checks/E-295/validation/compact-toolpaths.png) en [detail van een lokale lijnonderbreking](../../tools/curated-experiment-checks/E-295/validation/compact-local-bead-gap.png).

**Voor Sander:** open **compact-five-pairs.stl** rechtstreeks in je slicer. Je hoeft geen CAD of Python te compileren. Deze proef is vrijblijvend, zonder deadline. De bestaande grote test is afgerond; deze plaat stelt de nieuwe vraag naar compactheid.

## 3. Test in enkele stappen — CTO

1. Laat afkoelen en neem alle delen rustig van de plaat. Houd paren 1–5 bij elkaar. **Laat de brede dunne pinvoetjes zitten.** Kijk door de open buis en noteer losse voet, scheefstand, ontbrekende draad, gaten, scheuren of stringing. Alleen loshangende draadjes verwijderen; geen draad bijschuren of uitboren. Noteer iedere nabewerking.
2. Houd de pin bij haar printvoet, zodat je de dunne buis niet samenknijpt. Steek de schroefpunt vanaf de voetkant recht in de binnendraad. Draai voorzichtig; even terugdraaien om de draadstart te vinden mag. Niet drukken of een verkeerde draadstart doordraaien.
3. Draai tot de vrije axiale afstand tussen **bovenkant schroefhandgreep en onderkant pinvoet ongeveer 6 mm** is. De schroef steekt dan circa 10 mm in de pin. Draai één omwenteling uit tot ongeveer 9 mm afstand, en terug. Dat is circa 3-mm beweging met de volledige 6-mm binnendraad nog in aangrijping. Draai niet tegen de voet en niet bijna volledig los. Herhaal **vijfmaal heen en terug**. Houd de pin tegen rotatie en draai de schroef: zo blijft het gekozen schroef-staafprincipe zichtbaar.
4. Noteer per paar start, soepel/lichte weerstand/stroef/vast, voelbare speling en schade. Bij verschillen tussen 1–3: probeer pin 1 op schroef 2 en 3. Zo wordt zichtbaar of weerstand vooral met de pin of de schroef meeverhuist. Geen belastings- of breuktest.
5. **Optioneel, als de oude onderdelen bewaard zijn:** probeer compacte pin 5 op dezelfde oude schroef waarop de brede 0,20-mm moer zo soepel liep. Vergelijk ook die brede moer op diezelfde schroef. Noteer richting en gevoel. De draadprofielen zijn nominale matches; de contactlengtes 6 tegenover 10 mm en handgrepen verschillen, dus dit is een nuttige kwalitatieve vergelijking, geen wrijvingsmeting of bewijs dat alleen de compactheid een verschil veroorzaakt.

**Succes:** alle drie nominale paren starten zonder kracht, bewegen vijfmaal heen/terug op volle draadgrijping en blijven intact zonder nabewerking van de draad. Voelbare variatie mag worden gerapporteerd; zij wordt niet gemiddeld weggeschreven. “Even soepel als het oude paar 5” is een waarneming, geen gemeten motorbelasting.

**Onbekend:** gesloten top, externe geleiding, buurbeweging, belasting, zelfremming, lange-schroefstabiliteit, 40-mm slag, snelheid, slijtage en opbrengst van duizenden onderdelen. De tijdelijke 12-mm pinvoeten passen niet in het raster. Eventueel **na** alle passingtesten alleen aan de buitenkant vlak afknippen is een afzonderlijke observatie over verwijderbaarheid; trimmen is niet nodig voor deze proef en succes ervan wordt niet verondersteld.

## 4. Mijn resultaten — Sander

**Testdatum:**\
**Printer / PLA / nozzle / laaghoogte / wandgenerator:**\
**XY-/gat-/elephant-footcompensatie, indien gebruikt:**\
**Werkelijke printtijd / materiaal:**\
**Print gelukt?** [ ] ja [ ] deels [ ] nee **[x] nog niet geprint**

| Paar | Print intact en gat vrij? | Start zonder kracht? | Vijf cycli 6↔9-mm afstand? | Gevoel / speling / schade / nabewerking |
|---|---|---|---|---|
| 1 — 0,175 | niet getest | niet getest | niet getest | |
| 2 — 0,175 | niet getest | niet getest | niet getest | |
| 3 — 0,175 | niet getest | niet getest | niet getest | |
| 4 — 0,15 | niet getest | niet getest | niet getest | |
| 5 — 0,20 | niet getest | niet getest | niet getest | |

**Kruisproef pin 1 op schroef 2/3 (indien nodig):**\
**Vergelijking met bewaarde brede test (optioneel, welke onderdelen?):**\
**Voet bleef vast op het bed? Dunne wanden intact?**\
**Foto / video / opmerking (optioneel):**

## 5. Interpretatie en vervolg — CTO, pas na feedback

**Fysiek resultaat:** onbekend; alle vakken hierboven zijn nog open.\
**GO / NO-GO / keuze tolerantie:** nog open.\
**Status na feedback:** nog open. Geen automatische nieuwe print of grotere serie. Uitblijvende feedback is geen meetresultaat.
