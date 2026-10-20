# E-302 — eenvoudig motorframe met geïntegreerde korte schroef

**Status:** READY — CAD en Bambu-slices gecontroleerd; fysiek nog niet getest.\
**Prioriteit:** P1 binnen deze eigenaarsopdracht; geen deadline of automatische printopdracht.\
**Laatst beoordeeld:** 19 oktober 2026.\
**Bron:** [E-302](../../06-experiments/E-302-improved-microstepper-test-frame.md).

## Wat deze proef oplost

Eén ronde rotor vervangt de losse schroefvoet en grote vierkante koppeling.
De bewezen **radiale C-passing met drie ribben** en de functionele schroefdraad
(Ø3,2 / spoed3 / lengte16 mm) zijn behouden. De mond ligt lager dan bij revisie4,
met een opnieuw gecontroleerd aangrijpgebied. Een bestaande 0,50-mm sluitring
neemt de neerwaartse last op; de ronde bovenste geleiding en aanslag verzorgen
radiale geleiding en begrensde oplichting. Geen pinlast bedoeld op de motoras.

De motor ligt in twee stijve halve cilindrische zittingen, zonder veerbruggen.
Twee robuuste pennen met een rond en een langwerpig pasgat lijnen de helften uit.
De bestaande elastiekjes houden ze samen. Vier kleine spacers dienen uitsluitend
voor het bepalen van de huispassing; geen nieuwe veren of bevestigingsmiddelen.
De nieuwe [eigenaarobservaties](resultaten.md) zijn apart vastgelegd.

## Direct printen

Open **[microstepper-frame-v3.3mf](microstepper-frame-v3.3mf)** in Bambu Studio.
Printer, PLA, proces, objectoriëntaties en lokale rotorbrim zijn opgeslagen.
Geen CAD-export of handmatig overtypen van instellingen nodig.

| Onderdeel | Aantal | Doel |
|---|---:|---|
| Nieuwe framehelft met pennen / met gaten | Elk 1 | Stijve zitting en uitlijning |
| Geïntegreerde korte schroef/koppeling C | 1 | Rond, 28 mm totaal; 16 mm draad |
| Bestaande 18-mm testpin | 1 | Een al goed passende bestaande pin mag worden hergebruikt |
| Spacers 0,60 / 0,72 / 0,84 mm | 1 / 2 / 1 | Dubbele 0,72 als controle van printvariatie |

Eén plaat: **67 × 54 × 28 mm modelgrenzen**, lokale rotorbrim blijft binnen
het totale rechthoekige plaatbereik. Geen lange schroef, extra koppelingen of
softwarepakket. Hergebruik de motor, ring en twee elastiekjes.

![CAD-montage en compacte plaat](images/cad.png)

- Bambu Studio **02.08.02.61**, **X1 Carbon / 0,4-mm nozzle**, Generic PLA,
  Textured PEI Plate; 220 °C nozzle / 55 °C bed.
- Laag/eerste laag **0,12/0,12 mm**, Arachne, twee wanden, nominale lijnbreedte
  0,45 mm; minimum bead75%, minimum feature10%; 100% zigzag-infill.
- Buitenwand/kleine omtrek/eerste laag/brug15 mm/s, binnenwand20 mm/s;
  default/binnenwandacceleratie1000, buitenwand/eerste laag500 mm/s².
- Supports uit, raft0, per laag printen. **Alleen rotor: buitenbrim2 mm,
  afstand0,12 mm**. Geen support in tandwielholte of pinboring.
- XY-contour/gat/elephant-footcompensatie0. Onderdeelfan100% na eerste laag,
  hulpfan0%, minimum laagtijd8 s. Geen automatische heroriëntatie/herschikking.
- Framehelften op hun vlakke **buitenzijde**, uitsparingen omhoog; pennen groeien
  omhoog. Rotor rechtop met tandwielmond op het bed, schroefdraad bovenaan.
  Alleen het kleine holtedak overbrugt circa2,5 mm. Pin op bestaande printvoet;
  spacers op vlakke strookzijde. Hun diktes zijn vijf/zes/zeven lagen.
- Slicer-estimatie: **3 uur 5 minuten / 10,70 g PLA**. Details in [verificatie](verification.md).

## Montage en proef

Volg de korte [montagehandleiding met doorsnede](assembly.md). Eerst lege helften,
motorzitting en werkelijke tandhoogtes controleren; daarna rotor en pin met de
hand. Alleen bij soepele werking vijf bewegingen binnen de **handmatig
gecontroleerde 3-mm slag**, met de reeds werkende elektronica/software.

De proef beantwoordt vier vragen: blijven de helften uitgelijnd; zit de motor
vast; draait de rotor vrij zonder axiale asbelasting; beweegt de pin herhaaldelijk
op/neer? Vul alleen uitgevoerde controles in [resultaten.md](resultaten.md) in.
Stop bij forceren, PCB-druk, asbeweging, slip, schade of vastlopen.

**CAD, slicer en fysieke proef blijven gescheiden.** READY betekent een digitaal
gecontroleerd printpakket, geen bewezen mechanische betrouwbaarheid. Werkelijke
motor-/tand-/PCB-maten, passing en herhaalbaarheid blijven te controleren.

## Bestanden

`components/`: STLs; `cad/`: parametrische frame/rotorbasis/spacers;
`scripts/`: reproduceerbare meshopbouw, Bambu-bouw en controles; `metadata/`:
instellingen, CAD-/slicerrapporten en hashes; `images/`: montage en baanbeelden.
De scripts gebruiken de originele v2-schroef/pinmeshes uit dezelfde repository.
Engineeringreproductie staat in [verification.md](verification.md).

**Stopconditie:** deze compacte levering. Geen nieuw elektronica-, software-,
sensor-, motorbank- of vervolgonderzoek gestart.
