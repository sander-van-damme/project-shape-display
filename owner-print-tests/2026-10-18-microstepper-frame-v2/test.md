# E-302 — Improved Microstepper Test Frame, revisie 3

**Status:** READY — CAD en Bambu-slice gecontroleerd; fysiek nog niet getest.\
**Prioriteit:** P1 binnen deze eigenaarsopdracht. Geen automatische printopdracht.\
**Laatst beoordeeld:** 18 oktober 2026.\
**Technische bron:** [E-302](../../06-experiments/E-302-improved-microstepper-test-frame.md).

**Wijziging op eigenaarfeedback:** één duidelijk open PCB-uitsparing, meer oorspronkelijke
cilindersteun, plus korte/lange schroeven en 18-/50-mm pinnen op de plaat. De lange schroef
ligt horizontaal met eigen supports. De veren zijn aanvullend.

## 1. Waarom deze test?

Kan de bestaande motor stevig zonder nabewerking worden gemonteerd, met vrije
PCB/draden, en kan een afneembare vrouwelijke koppeling de bestaande tanden
bij verschillende insteekdieptes aandrijven? E-301 bewoog fysiek omhoog/omlaag,
maar vereiste snijwerk en ducttape. Deze print toetst uitsluitend die twee
mechanische verbeteringen. CAD en toolpaths voorspellen geen fysieke passing.

## 2. Printklaar

Open **[microstepper-frame-v2.3mf](microstepper-frame-v2.3mf)** rechtstreeks in
Bambu Studio. Printer, filament, proces, oriëntatie en plaat zijn opgeslagen.
Geen CAD compileren of instellingen overtypen. [Plaatbeeld](plate.png).

| Onderdeel | Aantal | Herkenning / doel |
|---|---:|---|
| Complementaire framehelften | 2 | Eén gezamenlijke PCB-uitsparing; veren erbuiten |
| Koppeling A | 1 | Eén inkeping; ribtipstraal 0,95 mm, diepste aangrijping |
| Koppeling N | 2 | Twee inkepingen; 1,00 mm, identieke nominale herhalingen N1/N2 |
| Koppeling C | 1 | Drie inkepingen; 1,05 mm, ruimste passing |
| Korte schroef | 1 | Ongewijzigd, 16 mm draad; bij 18-mm pin |
| Lange schroef | 1 | 48 mm draad / 50,4 mm totaal; bij 50-mm pin; horizontaal ondersteund |
| Standaardpin | 1 | 18 mm hoog, bestaande draad en printvoet |
| Lange pin | 1 | 50 mm hoog; dezelfde draad en printvoet |

- Eén plaat, geometrie **76 × 98 × 50 mm**, exclusief lokale brim/supportuitloop. Schroeven en pinnen zitten nu op de plaat;
  bestaande exemplaren blijven bruikbaar. Hergebruik de bestaande 0,50-mm sluitring.
- X1 Carbon, 0,4-mm-nozzle, Generic PLA, Textured PEI Plate; Bambu Studio **02.08.02.61**.
- Laag/eerste laag 0,12/0,12 mm; Arachne, nominale lijnbreedte0,45 mm,
  2 wanden, 100% zigzag-infill; minimum bead75%, minimum feature10%.
- Buitenwand/kleine omtrek15, binnenwand20, eerste laag15, brug15 mm/s.
  Default/binnenwandacceleratie1000; buitenwand/eerste laag500 mm/s².
- Globaal supports uit, raft0, geen brim; print per laag. **Alleen de lange schroef**
  heeft opgeslagen objectinstellingen: normale snug supports vanaf de plaat,
  hoek45°, top-/bodemafstand0,24 mm, XY-afstand0,35 mm, twee bovenste
  interfacelagen met0,2-mm lijnafstand, basisafstand2 mm; buitenbrim3 mm
  met0,12-mm objectafstand. Support-/interfacesnelheid20/15 mm/s.
  XY-contour-, gat- en
  elephant-footcompensatie0. Geen automatische oriëntatie of herschikking.
- PLA220°C, bed55°C; onderdeelfan100% na eerste laag; hulpfan0%;
  minimum laagtijd8 s. Globale waarden: [saved-settings.json](saved-settings.json);
  objectinstellingen: [saved-object-settings.json](saved-object-settings.json).
- Frame op splitvlak; koppelingsvierkant open naar bed, tandwielboring omhoog.
  Beide pinnen rechtop op hun 12 × 12 × 0,24-mm printvoet; korte schroef op vierkante voet.
  Lange schroef horizontaal, as5 mm boven plaat; normale supports onder de draad.
  Brede frame-/kopvoeten verzorgen hechting. Ondersteuningen blijven uit de boringen. Zie [supportcontrole](long-screw-support.md).
- Slicerschatting oorspronkelijke slice: **14,13 g, 4 uur 17 minuten totaal**
  (model4u02m; opstart inbegrepen in totaal). Geen gemeten printverbruik/tijd.
- Zelfstandige heropening/reslice geslaagd, zonder externe profielen;
  opgeslagen instellingen identiek. Kleine baanverschillen tussen slices zijn
  apart beoordeeld; geen byte-identieke G-code geclaimd.
- Drie ribben op alle64 gecontroleerde rechte boringlagen aanwezig in beide
  slices. Nominale minimum radiale lobuitsteking circa0,195 mm;
  centrale radius0,80 mm vrij. Dit bewijst printbanen, geen grip op echte tanden.

Zie [montage met afbeeldingen](assembly.md) en [verificatie](verification.md).

## 3. Test in enkele stappen

1. Lange schroef van supports ontdoen en draad op schade controleren volgens
   de montagehandleiding. Eerst met de hand door de 50-mm pin draaien.
   Spanningsloos N1 en N2 los op hetzelfde tandwiel passen, afnemen en vergelijken.
   Bij klemmen C proberen; bij slip A. Geen kracht, lijm, tape of nabewerking.
2. Motor in open frame leggen met PCB zijwaarts; draden vrij houden. Ring en
   koppeling plaatsen, axiale ruimte controleren en elastiekjes sluiten.
3. Kies korte schroef/18-mm pin of lange schroef/50-mm pin. De 50 mm is totale hoogte, geen grotere slag.
   Controleren dat metalen huis niet kantelt/verdraait en PCB nergens belast wordt.
   Met de hand draaien en veilige bestaande slag controleren.
4. Vijf korte op/neerbewegingen met de bestaande werkende bediening; let op
   markeringen voor slip en op zichtbare beweging van huis/as.
5. Drie keer demonteren/hermonteren; indien beschikbaar herhalen met een motor
   met andere tandwielhoogte. Resultaten in [resultaten.md](resultaten.md).

**Succes:** zonder nabewerking stevig, eenvoudig op/afschuiven, bruikbare
hoogtevariatie, geen merkbare asbelasting en vijf bewegingen zonder zichtbare slip.
**Stop/afkeur:** forceren, PCB-/soldeercontact, tandwiel tegen dak/flens,
los motorhuis, scheur/blijvende vervorming, onvoldoende overlap, vastlopen of slip.
Een niet geteste tweede motor betekent dat hoogtevariatie onbekend blijft.

## 4. Mijn resultaten

Gebruik het korte [resultatenformulier](resultaten.md). Leeg betekent onbekend.

## 5. Interpretatie en vervolg

Fysieke passing, montagekracht, grip, levensduur en motorvariatie: **nog onbekend**.
Na fysieke feedback kan `rig.scad` worden aangepast; er is geen vervolgprint
of nieuw onderzoek gestart. Stop bij de oplevering van deze test.
