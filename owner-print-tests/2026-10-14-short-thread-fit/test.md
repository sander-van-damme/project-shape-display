# Printtest — vijf korte schroef-moerparen

> Fysiek getest; eigenaar heeft de resultaten op 14 oktober 2026 gerapporteerd. Dit bevestigt handmatige passing van losse paren, **niet** de afmetingen van een compacte pin of meerdere onafhankelijke pinnen.

**Status:** COMPLETED

**Prioriteit:** afgerond (voorheen P1)

**Laatst beoordeeld:** 2026-10-14

**Reden:** vijf geprinte schroef/moerparen fysiek met de hand getest; varianten verschillen duidelijk in gevoelde weerstand. De compacte pinarchitectuur is nog niet bewezen.

**Technische bron:** [E-281](https://github.com/sander-van-damme/project-shape-display/blob/main/06-experiments/E-281-short-thread-repeatability-print-test.md), voortbouwend op E-277/E-279.

## 1. Waarom deze test? — CTO

**Vraag:** passen korte rechtop geprinte 90°-draadparen zonder forceren of schuren, en verschillen drie nominale exemplaren onderling? Berekeningen tonen vrije nominale geometrie, maar meten geen laagruwheid, krimp of wrijving.

**Beslissing:** drie goed bewegende nominale paren rechtvaardigen later een ondersteunde mechanische proef. Wisselend succes vraagt eerst onderzoek naar de printspreiding. Alleen succes met de ruime variant rechtvaardigt geen duizenden individueel passende onderdelen. Falen van alle paren stopt deze ongewijzigde printvariant.

**Afkeur:** herhaald vastlopen, beschadigde draad, scheve print of individueel schuren/snijden aan de draad nodig. Stop bij weerstand; geen tang, boormachine of belasting tot breuk.

## 2. Printklaar — CTO

| STL-bestand in deze map | Inhoud | Herkenning |
|---|---|---|
| [five-short-thread-pairs.stl](five-short-thread-pairs.stl) | 5 schroeven + 5 moeren, al op één plaat geplaatst | 1–5 voelbare stippen op elke handgreep/moer |

- **Printjobs:** één kleine plaat, tien losse onderdelen. Geen extra kopieën toevoegen.
- **Varianten:** stippen 1, 2, 3 zijn dezelfde functionele geometrie, radiale CAD-speling 0,15 mm; 4 is 0,10 mm; 5 is 0,20 mm. Alle schroefdraden zijn identiek. De stippen liggen buiten het schroefdraadcontact. Dit zijn gekozen proefwaarden, geen gemeten printertoleranties.
- **Materiaal:** gewone PLA die je al hebt; geen aankoop nodig.
- **Printer/profiel:** X1 Carbon, 0,4-mm nozzle, 0,20-mm lagen inclusief eerste laag, 2 wanden, 100% infill, 0,45-mm lijnbreedte; schaal 100%. Richtwaarden: buitenste/kleine perimeters maximaal 30 mm/s, eerste laag 20 mm/s, acceleratie maximaal 1000 mm/s². Gebruik je normale PLA-temperatuur/koeling en laat vertragen voor korte lagen aan. Geen XY-/gatcompensatie toevoegen voor deze eerste vergelijking; noteer bestaande compensatie.
- **Oriëntatie:** laat de onderdelen staan zoals geleverd: schroeven op hun brede vierkante voet, moergaten verticaal. Geen automatische heroriëntatie. Print per laag, niet object-na-object.
- **Supports/brim:** uit; ook geen raft. De voet blijft onderdeel van de schroef en is de handgreep, geen af te breken support. Alleen een skirt is vrijblijvend. Controleer in de preview dat alle tien onderdelen op de plaat staan; bij ontbrekende draad of onverwachte supports niet printen.
- **Afmetingen:** hele set 94 × 32,15 × 19 mm; schroefvoet 14 × 14 × 3 mm, draad boven voet 16 mm; moer 10,3 × 10,3 × 10 mm plus 0,4-mm stippen.
- **Verwachte tijd/materiaal:** circa **1 uur 7 minuten / 10,6 g PLA** (8,53 cm³), berekend met PrusaSlicer 2.7.2 en het vergelijkingsprofiel; geen gemeten X1C-tijd. Eigen slicer, opwarmen en laagkoeling kunnen langer uitvallen. Geen meegeleverde G-code gebruiken.
- **Extra benodigdheden:** alleen handen; liniaal en pen optioneel. Geen lijm, gereedschap of gewichtjes vereist.
- **STL-controle:** 2026-10-14: tien gesloten, afzonderlijke meshes; afmetingen en oriëntatie gecontroleerd; 425 gesimuleerde coaxiale montagestanden vrij. De exacte plaat is met supports uit én aan gesliced: geen support-, brug- of overhangpaden. Visuele controle van geometrie en paden; geen bewijs van fysieke passing.

**Voor Sander:** open de STL rechtstreeks in je slicer. Je hoeft niets te compileren. Deze proef is vrijblijvend, zonder deadline. De korte schroeven vervangen de ingetrokken lange S40-proef; ze bewijzen geen lange printstabiliteit.

## 3. Test in enkele stappen — CTO

1. Laat afkoelen en neem de tien delen van de plaat. Tel stippen en houd paren 1–5 bij elkaar. Kijk naar scheefstand, ontbrekende draad, stringing en beschadiging. Verwijder alleen losse draadjes die vrij loskomen; niet aan functionele draad schuren. Noteer iedere nabewerking.
2. Houd de brede schroefvoet vast. Zet de moer met de stippen boven voorzichtig op het uiteinde. Draai de moer, van boven gezien, rechtsom om haar op de schroef te laten zakken; kort linksom zoeken mag. Niet duwen of een verkeerde draadstart doordraaien.
3. Draai tot de schroefpunt ongeveer 1 mm boven de moer uitkomt. Draai vervolgens ongeveer één omwenteling verder naar beneden (ongeveer 3 mm), en terug. Blijf minstens circa 1 mm boven de voet/stippen: niet vastdraaien tegen de voet. Stop bij voelbare harde blokkade. Herhaal vijfmaal; noteer soepel/ruw/vast en zichtbare axiale speling bij heel zacht trekken/duwen. Geen breuk- of zware houdproef.
4. Test eerst alle eigen paren. Als 1–3 verschillen: probeer moer 1 ook op schroef 2 en 3. Zo wordt zichtbaar of een probleem met de moer, schroef of combinatie meeverhuist. Noteer dit apart; niet alle combinaties hoeven getest.

**Succes:** alle drie nominale paren starten zonder kracht, doorlopen circa één omwenteling op volle inschroeflengte in beide richtingen en blijven vijf cycli bruikbaar zonder schuren/beschadiging. Kleine ribbelige weerstand mag als waarneming worden gemeld; het is geen gemeten motorbelasting.

**Onbekend blijft:** houdkracht, lange-screw-stabiliteit, snelheid, levensduur, geleiding, 40/50-mm slag en opbrengst van duizenden delen. Deze test heeft geen externe antirotatie- of lastfixture; eigen gewicht/handgevoel is geen belastingskwalificatie.

## 4. Resultaten — Sander (eigenaarrapportage 2026-10-14)

**Testdatum:** gerapporteerd op 14 oktober 2026; exacte printdatum niet afzonderlijk vermeld.

**Printer:** Bambu Lab X1 Carbon. Filament, nozzle, laaghoogte, compensatie, werkelijke printtijd en verbruik niet gerapporteerd. De profielspecificaties in §2 zijn aanbevelingen en geen bevestigde werkelijke printinstellingen.

**Handtest:** alle vijf paren werden volgens de eigenaar vijfmaal heen en terug gedraaid. Geen schade en geen nabewerking. Exacte inschroeflengte, axiale speling en benodigd draaimoment niet gemeten of gerapporteerd.

| Paar | Radiale CAD-speling | Gevoel volgens eigenaar | Resultaat |
|---|---:|---|---|
| 1 — nominaal | 0,15 mm | Een beetje stroef, niet extreem | 5 cycli; geen schade |
| 2 — nominaal | 0,15 mm | Vrij soepel; lichte weerstand | 5 cycli; geen schade |
| 3 — nominaal | 0,15 mm | Vrij soepel; lichte weerstand | 5 cycli; geen schade |
| 4 — krapper | 0,10 mm | Zeer stroef, veel weerstand, voelt niet goed | 5 cycli; geen schade |
| 5 — ruimer | 0,20 mm | Heerlijk soepel; geen voelbare weerstand; voelt het best | 5 cycli; geen schade |

**Kruisproef (moer 1 / schroef 2–3):** niet gerapporteerd.

**Bron en beperking:** eerstehands kwalitatieve eigenaarobservaties; geen gemeten wrijving, belasting, uitgebreide levensduur of statistische printeropbrengst. De drie nominale paren hebben dezelfde CAD-geometrie; verschillen in handgevoel kunnen op print- of oppervlaktevariatie wijzen, maar de oorzaak is nog niet vastgesteld.

## 5. Interpretatie en vervolg — na feedback

**Positief handmatige passing:** alle vijf paren konden vijf cycli bewegen zonder beschadiging of nabewerking. Bij deze print is 0,10 mm onaangenaam stroef; 0,15 mm bruikbaar met voelbare variatie; 0,20 mm het soepelst. Dat laatste is **niet** bewezen als optimale productiespeling: last, backlash/speling, geleiding, motorsnelheid en slijtage blijven onbekend.

**Essentiële geometrische beperking:** de moeren in deze test zijn **10,3 mm breed**. Daarmee is geen passend draadmechanisme bewezen binnen een fijn raster zoals de historische pitch van 5,08 mm. De eigenaar meldt dat de veel smallere, oorspronkelijk geprinte Trial 5-familie destijds **wel goed werkte**; de historische CAD noemt 4,4 mm buitenbreedte en korte binnendraad onderaan, maar welke exacte variant toen succesvol was, is onbekend. Zie [trial5-short-replica](../2026-10-14-trial5-short-replica/test.md).

**Besluit:** teststatus **COMPLETED**; geen nieuwe tolerantieprint voor dezelfde vraag nodig. De cruciale open ontwerpvraag is compacte op/neergaande beweging van **meerdere onafhankelijk aanstuurbare pinnen zonder buureffecten**. De 0,20-mm-passing is een kandidaat, geen vastgelegde eindtolerantie. Geen nieuwe printopdracht uit deze rapportage.
