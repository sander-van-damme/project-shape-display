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
| Gebruikt paar: pin18/50 en rotor28/60 mm | ____ |
| Pin50: voet vast, rechtop zonder wiebelen/nozzlecontact | ____ |
| Lange schroef: acht nekjes verwijderd, benodigde kracht/tijd | ____ |
| Draad na verwijderen: resten, littekens, scheuren, handpassing | ____ |
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

## Correctie op eigenaarfeedback — verkeerde spiegeling en geleiding tot50 mm

Eigenaar meldt: één framehelft is verkeerd gespiegeld; vraagt geleiding voor
pinnen tot50 mm. Dit is negatieve eigenaarfeedback, geen nieuwe geslaagde proef.
De oude controle spiegelde de achterste STL met een matrix met determinant−1;
dat is niet met een geprint onderdeel uitvoerbaar. Nieuwe achterkant wordt met
tegengestelde handigheid geëxporteerd; montagecontrole gebruikt alleen rotaties
(determinant+1). De oude achterkant geeft daarbij38,444 mm³ overlap en wordt
nu expliciet als regressie afgekeurd.

Geleiding verlengd tot Z72,7 voor18–50-mm pinlengtes;3-mm slag behouden.
Derde elastiek bij bovengroef houdt beide geleidingshelften samen. Bestaande50-mm
pinmesh gebruikt voor digitale controle, geen nieuwe lange pin op de printplaat.
Geen nieuwe fysieke passing, kromtrekking, wrijving of beweging gemeten.

Nieuwe plaat digitaal READY na opgeslagen3MF heropenen/reslice en baancontrole:
Bambu02.08.02.61,3u46m31 /14,08g. Oude plaat en verkeerde helften ingetrokken.

## Lange schroef en rechtop geprinte50-mm pin — 21 oktober2026

Eigenaar vraagt een extra50-mm pin, rechtop, en verduidelijkt dat verwijderbare
supports voor de schroef bedoeld zijn. Op de vraag of ook een langere schroef
gewenst is, antwoordt de eigenaar bevestigend. De bestaande korte set blijft.

Toegevoegd:50-mm pin en60-mm geïntegreerde rotor (12-mm body +48-mm draad).
Twee zijtorens met acht kleine knipnekjes aan de lange schroef; geen supports
in/aan de pin. Bestaande koppeling, ring, krachtweg en proefslag3 mm behouden.
Geometriecontrole voor de lange combinatie over360° en3-mm slag geslaagd.
3MF opgeslagen, heropend en opnieuw gesliced in Bambu02.08.02.61; beide slices
gecontroleerd, inclusief acht contactverbindingen en open pinboring.
Schatting4u59m21 /16,61g; digitaal READY. Geen fysieke print, gemeten stabiliteit,
verwijderkracht, draadschade of nieuwe geslaagde passingstest. Noteer die later
in het formulier hierboven; leeg blijft onbekend.
