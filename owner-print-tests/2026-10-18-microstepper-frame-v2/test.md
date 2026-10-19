# E-302 — Improved Microstepper Test Frame, revisie 4

**Status:** READY — herziene CAD en Bambu-slice gecontroleerd; revisie 4 nog niet fysiek getest.\
**Prioriteit:** P1 binnen deze eigenaarsopdracht; geen automatische printopdracht of deadline.\
**Laatst beoordeeld:** 19 oktober 2026.\
**Technische bron:** [E-302](../../06-experiments/E-302-improved-microstepper-test-frame.md).

## 1. Eigenaarfeedback en wijziging

De eigenaar heeft revisie 3 geprint: kop A (één inkeping) is te strak, beide N-koppen
(twee inkepingen) gingen kapot, C (drie inkepingen) is goed. De kop is echter te
lang om samen met de motor in het frame te passen. De horizontale lange schroef
printte slecht; supports waren moeilijk te verwijderen en de schroef werkte niet
goed. De korte schroef is geen probleem. Dit zijn eigenaarobservaties, geen
maatmetingen of duurproef; de werkelijk gebruikte printerinstellingen zijn niet opgegeven.

Revisie 4 gebruikt uitsluitend passing C, **2 mm korter: 15,6 in plaats van 17,6 mm**.
Het motoruiteinde is ingekort; lagerhals, ringvlak en vierkante schroefzitting blijven
op dezelfde hoogte. De lange schroef staat rechtop met twee afneembare zijsteunen en
acht kleine afbreekverbindingen, vier per zijde. Het functionele draadprofiel,
beide pinnen, frame en korte schroef zijn behouden. Oudere A/N-STLs en de horizontale
schroef blijven historische bestanden; zij staan niet op de actuele plaat.

## 2. Printklaar

Open **[microstepper-frame-v2.3mf](microstepper-frame-v2.3mf)** rechtstreeks in
Bambu Studio. De X1 Carbon/0,4-mm printer, PLA, proces en plaat zijn opgeslagen.
[Plaatbeeld](images/plate.png), [montage](assembly.md), [verificatie](verification.md).

| Onderdeel | Aantal | Herkenning / doel |
|---|---:|---|
| Complementaire framehelften | 2 | Bestaande geometrie, gezamenlijke PCB-uitsparing |
| Kortere koppeling C | 2 | C1/C2 identiek, elk drie inkepingen; ribtipstraal 1,05 mm |
| Korte schroef | 1 | Bestaande 16-mm draad, ongewijzigd |
| Lange schroef met zijsteunen | 1 | Rechtop, 48-mm draad / 50,4-mm totale hoogte |
| Pin 18 mm / pin 50 mm | Elk 1 | Bestaande draad en integrale printvoet |

Eén plaat, modelgrenzen **76 × 98 × 50,4 mm**, exclusief lokale brim. Bestaande
framehelften, pinnen en korte schroef kunnen worden hergebruikt; selecteer alleen
C1/C2 en de lange schroef als je uitsluitend de wijzigingen wilt printen en slice
opnieuw voor de bijbehorende tijdschatting. De onderstaande controles gelden voor
de volledige opgeslagen plaat. Hergebruik de bestaande 0,50-mm sluitring.

- Bambu Studio **02.08.02.61**, X1 Carbon / 0,4-mm nozzle, Generic PLA, Textured PEI Plate.
- Laag/eerste laag 0,12/0,12 mm; Arachne, nominale lijnbreedte 0,45 mm,
  twee wanden, 100% zigzag-infill, minimum bead 75%, minimum feature 10%.
- Buitenwand/kleine omtrek 15, binnenwand 20, eerste laag 15, brug 15 mm/s.
  Default/binnenwandacceleratie 1000, buitenwand/eerste laag 500 mm/s².
- Automatische supports **overal uit**, raft 0, print per laag. De zijsteunen en
  afbreekverbindingen zijn **meegetekende geometrie** in het lange-schroefobject.
  Alleen dat object krijgt buitenbrim 3 mm met 0,12-mm afstand; elders geen brim.
- XY-contour-, gat- en elephant-footcompensatie 0. Geen automatische oriëntatie of herschikking.
- PLA 220 °C, bed 55 °C, onderdeelfan 100% na eerste laag, hulpfan 0%, minimum laagtijd 8 s.
- Frame op splitvlak; koppen met vierkante holte naar bed en tandwielboring omhoog.
  Schroeven op vierkante voet; pinnen rechtop op hun bestaande 12 × 12 × 0,24-mm voet.
- Slicerschatting volledige plaat: **13,22 g PLA, 4 uur 12 minuten totaal**.
  Geen werkelijk gemeten tijd/verbruik. Globale instellingen: [metadata/saved-settings.json](metadata/saved-settings.json);
  objectinstellingen: [metadata/saved-object-settings.json](metadata/saved-object-settings.json).

## Bestanden in deze map

De instructies, resultaten en printklare `microstepper-frame-v2.3mf` staan bovenaan.

| Submap | Inhoud |
|---|---|
| `components/` | Onderdeel-STLs en samengestelde plaat; oude varianten in `archive/` |
| `cad/` | OpenSCAD-bronnen |
| `scripts/` | Genereren, bouwen en controleren |
| `metadata/` | JSON-instellingen, maat-/slicecontroles en bouwherkomst |
| `images/` | Eén bestand per afbeelding; montage als SVG |
| `software/` | Bestaande zelfstandige motorsoftware met eigen handleiding |

## 3. Korte test

1. Verwijder de zijsteunen volgens de [supportinstructie](long-screw-support.md).
   Controleer de lange schroef eerst met de hand in de 50-mm pin; stop bij beschadiging of klemmen.
2. Pas C1 en C2 spanningsloos op het tandwiel. Controleer of kop en motor samen
   zonder kracht in het frame passen; beoordeel werkelijke tandoverlap volgens de montagehandleiding.
3. Monteer met de bestaande ring; houd PCB/draden vrij. Controleer handmatig de
   bestaande 3-mm proefslag. 50 mm pinhoogte is geen 50-mm slag.
4. Pas daarna vijf korte op/neerbewegingen met de werkende bediening; let op slip,
   asbelasting en huisbeweging. Stop bij klemmen, scheuren of vervormen.
5. Noteer alleen uitgevoerde waarnemingen in [resultaten.md](resultaten.md).

## 4. Interpretatie en stopconditie

Passing C is gekozen op eigenaarfeedback over de oude lengte. De kortere C,
montage in het frame, stabiliteit van de rechtopstaande lange schroef en schadevrije
supportverwijdering zijn nog niet fysiek bewezen. Deze levering verwerkt de feedback;
er is geen nieuw onderzoek, firmwarewerk of automatische vervolgprint gestart.
