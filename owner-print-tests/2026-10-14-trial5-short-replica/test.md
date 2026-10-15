# Trial 5 — verkorte printtest

**Status: DEFERRED (printpoging met supports, geen functionele passingtest).** Deze compacte test blijft inhoudelijk relevant ondanks de geslaagde grotere [short-thread-fit](../2026-10-14-short-thread-fit/test.md). Geen herprintverplichting.

## Doel en herkomst

Controleer of een verkorte versie van [het oorspronkelijke trial-5/actuator.scad](https://github.com/sander-van-damme/project-shape-display/blob/41484f96999847c139b9010e73009d73e9459c89/trial-5-grid-and-cubes-and-rod/actuator.scad) betrouwbaar te printen en met de hand op en neer te bewegen is. De historische geometrie is de basis: **4,4-mm buitenbreedte, 0,44-mm dunne wand, uitsluitend 10 mm binnendraad aan het onderste uiteinde, en een volledig geschroefde 3,2-mm as, pitch 3, 30° profielhoek**. Het staafje is verkort van 50,8 naar **18 mm**; de schroef heeft **18 mm** draad plus een tijdelijke **7×7×1,6-mm handgreep/printvoet**.

**Belangrijke onzekerheid:** het historische bestand specificeert `$slop=0.65`. Bij een onderzochte versie van BOSL2 neemt de interne snijradius dan zo sterk toe dat de draad mogelijk helemaal niet aangrijpt. De historische *werkelijk succesvol geprinte variant* en libraryversie zijn niet geïdentificeerd. Daarom testen we drie nominale paren met `slop .20`, één krapper (.16) en één ruimer (.24). Die laatste kan kleine openingen in de dunne wand veroorzaken: **een klein gat is op zichzelf geen afkeur**. Deze proef is een zelfstandige **parametrische reconstructie**, geen exacte export met originele BOSL2. De details van de draad-inloop en aansluiting op de holte zijn vereenvoudigd en kunnen invloed hebben op passing.

## Printbestand

- [**trial5-short-comparison-plate.stl**](trial5-short-comparison-plate.stl): complete plaat met vijf losse schroeven en vijf losse staafjes, van links naar rechts drie identieke (.20), krapper (.16), ruimer (.24). **Ready-to-import STL; geen code compileren.**
- [generate-trial5-short.mjs](generate-trial5-short.mjs): bron voor reproduceerbaarheid (Node.js 18+, `node generate-trial5-short.mjs`). Niet nodig om te printen.
- Plaat ongeveer 69×7×19,6 mm; tien gesloten afzonderlijke meshlichamen, gevalideerd op 14 oktober 2026. Een print is geprobeerd, maar supports vulden de binnendraad; daardoor geen functionele passing of load-rating van deze replica vastgesteld.

**X1 Carbon / PLA (voorlopig):** importeer STL op 100%, onderdelen rechtop zoals geleverd; gebruik 0,4-mm nozzle, 0,08–0,12-mm laaghoogte, traag voor kleine buitenperimeters (bijv. 30 mm/s), een kleine brim voor de smalle staafjes en geen supports op de functionele draad. **Verplicht eerst Bambu Studio-preview controleren:** alle draadflanken moeten daadwerkelijk worden geëxtrudeerd, de dunne wand mag geen losstaande filament-eilandjes opleveren en alle tien delen moeten voldoende bedhechting hebben. Als de preview ontbrekende draadlagen of instabiele staafjes toont, niet printen; lever dan de preview voor herziening aan. De vroegere lange staafjes werden juist afgekeurd omdat printondersteuning niet was aangetoond. **Printtijd en filament zijn niet gesliced en blijven onbekend.** De test is nog geen volledige bewegingsrig, maar een handmatige passingtest.

## Eigenaarfeedback — 14 oktober 2026

- **Historische positieve fysieke ervaring:** eigenaar heeft de oorspronkelijke Trial 5-schroef/holle-pin-familie jaren eerder geprint en meldt dat deze goed werkte. De nominale buitenbreedte van 4,4 mm uit de oorspronkelijke CAD is relevant voor fijne pinpitch. Exacte destijds succesvolle variant, parameters, printerprofiel en herhaalbaarheid zijn onbekend; dit is historische eigenaarobservatie, geen validatie van deze nieuw gegenereerde replica.
- **Nieuwe printpoging:** de eigenaar zette supports aan in Bambu Studio. De supports vulden het interne schroefgat; hij heeft het materiaal niet verwijderd en heeft de draadpassing daarom niet getest. Dit is een support-/slicerconflict, **geen aangetoond mechanisch falen**.
- **Vervolg:** voorlopig **DEFERRED**, geen onmiddellijke herprint. Het goed functioneren van de 10,3-mm brede moeren uit `short-thread-fit` bewijst niet dat deze veel compactere pin werkt; de compacte geometrie blijft een wezenlijk open punt. Er is geen nieuwe test besteld.

## Handmatige meting (enkel na geslaagde print)

1. Laat afkoelen; label de identieke paren 1–3 en de varianten 4–5 vóór je ze los sorteert. Inspecteer dunne wanden, draad en eventuele gaten zonder de functionele passing bij te schuren.
2. Houd het holle staafje recht en draai met de schroefvoet voorzichtig in en uit. Begin met voldoende draadgrijping; probeer één volledige omwenteling vooruit en terug, tot vijfmaal. **Niet forceren, geen tang, geen zware last en niet bijna volledig uitschroeven**: een oud fysiek staafje brak juist nabij die stand.
3. Noteer vooral het verschil tussen de drie identieke paren; vergelijk daarna krapper en ruimer. Een kleine opening onderaan mag blijven als de constructie functioneert.

| Paar | Print intact? | Draad grijpt? | Beweegt heen/terug? | Stroefheid/speling/schade | Kleine gaten? |
|---|---|---|---|---|---|
| 1 — .20 | | | | | |
| 2 — .20 | | | | | |
| 3 — .20 | | | | | |
| 4 — .16 | | | | | |
| 5 — .24 | | | | | |

**Resultaatstatus:** 14 oktober 2026 gerapporteerd: printpoging met supports in Bambu Studio; interne opening gevuld; niet schoongemaakt, dus alle vijf passingresultaten onbekend. Verdere printerinstellingen niet gerapporteerd.

**Succes:** drie nominale paren printen intact, grijpen met de hand aan en bewegen vijfmaal heen en terug zonder onacceptabel vastlopen of beschadiging. **Onbekend:** volledige slag, houdkracht, naastliggende staafjes, motorvermogen, productiesnelheid en lange-termijnstabiliteit. Falen of geen feedback wordt niet geïnterpreteerd als succes. Nooit alvast productcompatibiliteit afleiden uit een CAD-preview.
