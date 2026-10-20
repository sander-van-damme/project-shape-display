# E-302 v3 — fysieke resultaten

## Eigenaarobservaties ontvangen op 19 oktober 2026

Bron: rechtstreeks bericht bij deze opdracht. Exacte geprinte revisie, 3MF-hash,
printerinstellingen en maatmetingen niet opgegeven.

- Elektronica en software werken; de motor beweegt de schroefpin omhoog en omlaag.
- Het roterende vierkant loopt regelmatig vast tegen het frame en voegt massa/complexiteit toe.
- De motor zit onvoldoende vast; de geprinte veerbruggen veren in werkelijkheid niet.
- De framehelften verschuiven ten opzichte van elkaar.
- Tandwielpassing C met drie ribben paste goed; die interface behouden.

Dit kwalificeert de nieuwe v3 niet. Oudere negatieve resultaten, waaronder de
gebroken N-koppen en slecht geprinte horizontale lange schroef, blijven in
[het v2-verslag](../2026-10-18-microstepper-frame-v2/resultaten.md) ongewijzigd.

## Eerste maatbeoordeling 20 oktober 2026 — historische tussenstand

Eigenaar: huis circa Ø8 ×9,2 mm; kale as circa Ø0,8 mm; twee tandwieluitstekingen.
C met drie ribben paste goed. Meetmethode/tolerantie en tand-/boss-/PCB-maten onbekend.
Digitale audit gebruikt nu het volledige9,2-mm huis; oude READY ingetrokken.
**DRAFT/BLOCKED**: botsing met draagdek, ontbrekende motorstack; geen nieuwe fysieke
proef, STL/3MF of slice vrijgegeven. Zie [verificatie](verification.md).

## Aanvullende eigenaarmetingen — 20 oktober 2026

Met meetlat, beperkte nauwkeurigheid: A≈1,5 /2,0 mm; B≈2,75 /3,25 mm;
C≈0,25 mm en D≈3 mm voor beide. A/B/C gemeten vanaf het metalen
huisbovenvlak, exclusief boss; D is bossdiameter. A=tandonderkant,
B=tandbovenkant, C=boss-top. Motoren delen volgens eigenaar een connector.

De centrale [registratie van varianten K/L](../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md#1a-eigen-motorpaar--benaderende-eigenaarmetingen-20-oktober-2026)
legt de bron, meetvlakken en onzekerheid vast. A/B-paren volgen de
berichtvolgorde. Eigenaar corrigeert “minder” naar **meer**: B≈3,25 mm voor L
is niet meer tegenstrijdig. Geen verzonnen
tolerantie toegevoegd. De eerdere status onbekend voor deze maten is hiermee
historisch; er zijn nu benaderende metingen.

Geen nieuwe fysieke passingstest, CAD-aanpassing of printvrijgave.

## Nieuwe proef — digitaal READY voor L, fysiek nog niet uitgevoerd

Datum: ____  3MF/hash: ____  Printer/nozzle/PLA: ____\
Werkelijk gewijzigde instellingen: ____  Werkelijke tijd/verbruik: ____\
Print gelukt: [ ] ja [ ] deels [ ] nee [ ] niet geprint

| Controle | Waarneming / meting; leeg = onbekend |
|---|---|
| Helften sluiten volledig; geen zijwaartse beweging/verdraaiing | ____ |
| Uitlijnpennen/gaten heel; gemakkelijk open/dicht, na 3 montages | ____ |
| Motor zonder spacer / 0,60 / 0,72a / 0,72b / 0,84 | ____ |
| Motorhuis vast; PCB, soldeer en vier draden vrij | ____ |
| Tandonderkant b / tandbovenkant t vanaf framebodem | ____ / ____ mm |
| Minimale overlap / dakruimte / mond-bossruimte | ____ / ____ / ____ mm |
| Rotor draait handmatig soepel, geen framecontact of slip | ____ |
| Ring draagt last; oplichting vrij; motoras blijft onbelast | ____ |
| Handmatig gecontroleerde pinhoogtes boven frame / veilige slag | ____ / ____ mm; ____ mm |
| Vijf op/neercycli gevraagd / werkelijk voltooid | ____ / ____ |
| Vastlopen, geluid, schade, verschuiving, terugkeerafwijking | ____ |

Uitkomst: [ ] voldoet voor deze proef [ ] deels [ ] voldoet niet [ ] onbeslist [ ] niet getest.\
Foto / extra opmerking: ____

Geen automatische vervolgopdracht. Een goede korte proef is geen duurtest of
bewijs voor alle motoren, belastingen of een complete motorbank.

## Aanvullende envelopematen en CAD-correctie — 20 oktober 2026

Eigenaar, benaderende meetlatwaarden: PCB6,5–7 mm breed; motor+PCB circa10 mm
diep; PCB vanaf2 tot6 mm boven metalen onderzijde. Variabele lijm onder PCB;
kabels komen bovenaan uit en lopen omhoog. Kale as circa0,1 mm boven tandwiel.
Twee bovenste metalen lipjes circa1 mm; PDF toont ze maar bemaat de contour niet.

De gegevens zijn verwerkt in de L-variant-CAD: zittingØ8,4, huishoogte9,2;
ringbodem12,4, rotormond12,9, inloop0,25. PCB/glue vrij vanaf motorbasis;
bovenliggende kabelroute buiten ring/rotor. Geen nieuwe fysieke proef uitgevoerd.
Nieuwe CAD/STL/3MF is nu **READY voor L** na heropenen/reslice en baancontrole.
Bambu02.08.02.61:2u58m23 /10,20g. Oud printproject gearchiveerd.
Geen nieuwe fysieke proef verricht; zie verification.md.
