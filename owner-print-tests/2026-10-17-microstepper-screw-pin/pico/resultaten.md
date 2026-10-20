# E-301 — resultaten en fysiek eigenaarsverslag

> **Maatcorrectie 20 oktober 2026:** huis circa Ø8 ×9,2 mm, kale as circa Ø0,8 mm; twee benaderend gemeten tandwieluitstekingen. Zie [actuele eigenaarmetingen](../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md). Oude 8,2-mm huishoogte/Ø1,5-mm as en catalogusuitstekingen hieronder zijn historische brongegevens, geen actuele motorafmetingen. Bestaande CAD wordt hiermee niet aangepast of vrijgegeven.

## Eerste fysieke eigenaarsproef — 18 oktober 2026

**Status:** gedeeltelijk uitgevoerd. **Positieve functionele uitkomst:** de bestaande
Ø8 × 8,2-mm vierdraads microstappenmotor heeft een geprinte compacte schroefpin
daadwerkelijk *omhoog én omlaag* bewogen in het geprinte frame, bij een
Vref van circa **0,80 V**. Dit is **door de eigenaar geobserveerd**, geen
instrumentele koppel-, kracht-, positie- of snelheidsmeting. De eigenaar meldt
dat de motor de huidige pin zonder zichtbare moeite bewoog.

**Bewijsklasse:** eigenaarverslag en tijdens de proef gerapporteerde
multimetermetingen/terminaluitvoer. Geen onafhankelijk gevalideerde
elektronicatest, motorstroommeting of kwantitatieve mechanische karakterisering.
Het is onbekend of de gebruikte pin de volledige uiteindelijke hoogte had;
de eigenaar wil later een volledige schroef/pin testen.

### Werkelijk gebruikte elektronica en foutdiagnose

| Controle/gebeurtenis | Waarneming van eigenaar | Betekenis / beperking |
|---|---|---|
| Microcontroller/driver | Pico W met MicroPython-firmware uit de UART-only E-301-revisie en witte Silent2208/TMC2208 V1.2-module | Exacte modulefabrikant en alle printcomponenten niet onafhankelijk vastgesteld |
| Motorvoeding VM–GND | Ongeveer **9 V** gemeten op de TMC | Voedingsspanning aanwezig op meetmoment; gedrag onder belasting niet gemeten |
| Logicaspanning VIO–GND, eerste poging | **0,09 V** | Verkeerd aangesloten kabel vermoed; UART gaf timeout/echo |
| Logicaspanning VIO–GND, na correctie | **3,3 V** op TMC; Pico 3V3 was afzonderlijk ook 3,3 V | Verkeerde aansluiting hersteld; UART daarna werkend |
| UART-selectie op TMC-module | Onderste buitenste soldeerpad had continuïteit naar de gemarkeerde UART-header; eigenaar heeft de UART-selectie gesoldeerd | Daarna correcte communicatie; exacte PCB-netlijst niet volledig doorgemeten |
| UART-verbinding | GP4 (TX) via 1 kΩ en GP5 (RX) rechtstreeks naar dezelfde UART-header, GND gemeenschappelijk | PuTTY op COM7 accepteerde `?`, daarna `ARM MOTOR` met `ARMED MOTOR; pin must be detached` |
| Eerste mislukte beweging | Terminal meldde `DONE planned rev=1.000`, maar motor draaide niet | Alleen geplande tijdsbeweging bevestigd, geen fysieke rotatie; UART was niet het probleem |
| EN onaangesloten | **3,24 V** gemeten vóór, tijdens en na een bewegingsopdracht | ENN is actief-laag; dit hield de motoruitgangen uit. Een aanwezige module-pull-up is aannemelijk, niet bewezen |
| EN voor succesvolle proef | **EN rechtstreeks aan GND** van dezelfde driver; STEP en DIR bleven los | Motor draaide en kon later de schroefpin verplaatsen |
| Vref | Eerst **1,35 V** gemeten; teruggesteld tot **0,79 V**, voor de pinproef gerapporteerd als circa **0,80 V** | Lage analoge stroomreferentie; fasepiek/RMS is *niet gemeten* |
| Stroomregeling | Firmware stelt VSENSE=1, IRUN=IHOLD=5 in, veronderstelt twee R110-shunts | Bij 0,80 V theoretisch circa 77 mA piek / 55 mA RMS; geen gemeten motorstroom |
| USB-terminal | PuTTY communiceert; lokaal echo stond eerst uit en veroorzaakte typeverwarring/`unknown command` | Geen hardwarefout; dit bewijst alleen Pico-USB, los van TMC-UART |
| Opstartgedrag | Met STEP en DIR bewust los zag eigenaar onbedoelde kleine links/rechts-beweging bij opstart | Consistent met zwevende ingang(en), maar exacte elektrische oorzaak niet gemeten; **voor uiteindelijke uitvoering vermijden** |

De oorspronkelijke `UART STOP UNCONFIRMED: UART timeout/echo` trad op
terwijl VM al aanstond maar VIO aanvankelijk vrijwel 0 V was. Na corrigeren
van VIO en solderen van de UART-selectie kon de firmware de chip configureren.
Er is **geen** succesvolle geverifieerde stop-/brownout-/supervisortest gerapporteerd.
Een `ARMED MOTOR` bevestigt registers/communicatie, **niet** dat de motoras beweegt.

**Opmerking over EN:** de werkende benchbedrading wijkt af van het
oorspronkelijke UART-only-schema, waarin EN los bleef. Een permanent lage EN
laat de uitgangen toe voordat de lage UART-stroominstellingen worden geschreven;
de eigenaar heeft dit voor de proef bewust geaccepteerd. Bij navolging
moet deze afwijking zichtbaar zijn, niet als een bevestiging van de oude
EN-los-bedrading worden voorgesteld.

### Beweging, snelheid en herhaalbaarheid

- **Losse motor:** na EN→GND draaide hij via `VACTUAL`/UART. Bij een
  `M 1`-opdracht leek de as **iets meer dan één omwenteling** te maken;
  geen geijkte hoek- of stapmeting.
- **Retourbeweging:** na voorwaarts en achterwaarts sturen kwam de as niet op
  dezelfde stand terug. De eigenaar zag dat de **positieafwijking zich opstapelde**
  bij herhaling. Geen maat van de afwijking, geen bewijs van de oorzaak.
- **Geluid:** bij `S 10` een hoorbaar piepend geluid; bij `S 100` leek
  de motor rustiger te draaien. Geluid is geen bewijs van beter koppel of
  nauwkeuriger stappen.
- **Met schroefpin:** op de ingestelde **S 100** en **Vref ~0,80 V**
  bewoog de pin zichtbaar op en neer. De eigenaar vond dit relatief vlot,
  maar ziet de bewegingssnelheid nog als ontwerpvraag. Hij schat ruwweg dat
  **ongeveer vier omwentelingen** nodig waren voor de bekeken op/neerbeweging.
  **Niet geteld, niet getimed, exacte slag onbekend.** Deze schatting niet
  verwarren met de nominale **3 mm schroefspoed per omwenteling** of de
  oorspronkelijke 3-mm-frameslag.
- **Niet vastgesteld:** volledig aantal echte volle stappen per 360°,
  werkelijke VACTUAL-snelheid, maximale belasting/koppel, eventuele gemiste
  stappen, slippercentage, aantal foutloze cycli, retourhoogte in mm,
  effectieve motor-/driver-temperatuur, continue bedrijfscyclus of
  betrouwbare uitschakeling na UART-uitval.

De lopende retourfout bewijst dat deze opstelling **niet positioneringsnauwkeurig
gekwalificeerd** is. Mogelijke bijdragen zijn tijdgestuurde beweging,
onnauwkeurige oscillatoraanname, gemiste stappen, vrijvallen van de as tussen
segmenten of de tijdelijke koppeling. Geen daarvan is nu afzonderlijk bewezen.
Kalibratie is bewust **niet** de eerstvolgende prioriteit.

### Werkelijk geprint frame: wat werkte en wat niet

**Positief (eigenaarobservatie):** het tweedelige frame is verder bruikbaar,
toegankelijk en gemakkelijk open te maken. Het kan met **elastiekjes**
worden vastgezet; de eerste bevestiging kost wat moeite, maar de eigenaar
wil dit principe behouden.

**Motorzitting — moet beter:** één uiteinde van de bestaande motor bevat
een klein printplaatje/terminal waarop de vier motordraden uitkomen.
De geprinte zitting bood daarvoor onvoldoende ruimte. De eigenaar heeft
**plastic uit het frame moeten wegsnijden**; daarna zat de motor niet meer
goed gestabiliseerd. De ongewijzigde CAD-zitting is dus *niet* fysiek
bevestigd als passend voor de werkelijke motorvorm.

**Aandrijfkoppeling — moet beter:** de verbinding van motor naar schroef is
in de proef met **ducttape** gemaakt; dat werkte voldoende om beweging
te demonstreren, maar was erg lastig te monteren. De in de originele
montagehandleiding voorgestelde siliconenslang is **niet als gebruikte
koppeling bevestigd**. De motoren hebben al een klein tandwieltje:
onderzoek voor een latere framevariant een **eenvoudige opsteekkop**
die daar overheen past, het koppel kan overbrengen en hoogteverschillen
kan verdragen. Volgens de eigenaar bestaan **twee uitvoeringen van deze
motor met verschillend uitstekende tandwielen**; afmetingen/speling nog
niet gemeten. Ook de printtolerantie van het frame moet meegenomen worden.

**Kabels en stekkers:** de tijdelijke opstelling heeft veel losse draden.
Eigenaar overweegt een breadboard/ordelijkere testbekabeling. De motor heeft
een **zeer kleine bestaande vierpolige connector**, kleiner dan standaard
GPIO-Dupontstekkers; exacte connectorfamilie/steek nog onbekend.
Een foto en maat kunnen later identificatie mogelijk maken, zodat niet
elke motor met de hand gesoldeerd moet worden. De eigenaar meldt circa
**200 exemplaren** van deze motor, niet individueel gekarakteriseerd.

**Eventuele volgende frameversie:** ruimte voor **twee of drie naast elkaar
geplaatste motoren** zou handig zijn als dat nauwelijks extra complexiteit
geeft; voor deze proef is slechts één motor gebruikt. Geen claim dat
meerdere onafhankelijke pinnen al tegelijk zijn getest.

### Interpretatie en vervolggrens

**Aangetoond:** de huidige motor, driver en geïmproviseerde koppeling kunnen
ten minste één bestaande compacte schroefpin in beide richtingen bewegen bij
circa 0,80 V Vref. Dit rechtvaardigt een eenvoudiger te monteren
framevariant en daarna gerichte kracht-/snelheidsmetingen.

**Nog niet aangetoond:** volledige werkhoogte, kwantitatieve krachtreserve,
duurzaamheid, herhaalbaarheid, correcte 360°-kalibratie, maximale stroom,
betrouwbare simultane aandrijving of geschiktheid voor het grote display.
De eigenaar wil later volledige pin/schroef, snelheid, staphoek, belasting,
temperatuur en uiteindelijk motorlimieten verkennen. Dat is **vervolginteresse,
geen reeds uitgevoerde test en geen opdracht om nu extra prints of
vernielingsproeven te starten**.

**Kleinste zinvolle vervolg:** eerst een passend motorvak rond het
draadprintje en een reproduceerbare, axiaal tolerante tandwielkoppeling.
Behoud de bruikbare toegankelijke framehelften. Dan kan een volgende
fysieke proef een vollengte-pin met bruikbare belastingsmeting testen.
Kalibratie of grotere elektronica-architectuur hoeft dit besluit niet
vooraf te gaan.

---

## Overige checklist uit het oorspronkelijke protocol — niet automatisch als geslaagd beschouwen

Onderstaande velden zijn een bewaard invulformulier. Niet ingevuld betekent
**niet gecontroleerd**, ook wanneer de proef wel zichtbare beweging opleverde.

### Resterende elektronicacontroles

- Exacte StepStick fabrikant/revisie en gebruikt PCB-schema: ____
- VM/VIO/GND/fase-uitgangen volgens dat schema bevestigd: ____
- Twee R110-opdrukken gezien: ____ ; geen nauwkeurige shuntmeting geclaimd.
- PDN_UART-brug: [ ] al doorverbonden [ ] volgens schema gesloten [ ] onbekend → STOP
- PD-trigger type en eigen DIP-stand voor9V: ____
- Adapterlabel9V-profiel: ____ ; gemeten PD-uitgang: ____ V
- VM na diode, los/belast: ____ / ____ V ; VIO: ____ V ; Vref: ____ V (doel0,80)
- TPS3808G01DBVR/adapterpinout gecontroleerd: ____ ; SENSE: ____ V
- RUN-jumper aanwezig vóór test: ____ ; STEP/DIR los, EN was bij geslaagde proef aan GND: eigenaarobservatie; verder te documenteren: ____
- MicroPython UF2-versie: ____ ; alle vier Python-bestanden geplaatst: ____
- ARM MOTOR geaccepteerd met TOFF0: ____ ; UART-fout blokkeert ARM: ____
- `!` tijdens losse motorbeweging: ____ ;30s idle: ____
- VM uit/herstel tijdens beweging: ____ ; UART-stop na boot bevestigd: ____
- Eventuele onbedoelde beweging bij opstart/reset/uitval: ____
- USB los/herstel: ____ ; UART-stop na reboot: ____
- Werkelijke fasepiek indien instrumenteel gemeten, methode/instrument: ____
  Geen meting? Schrijf **niet gemeten**; nominale berekening77mApiek/55mARMS.

Bij een mislukte controle geen pinproef. Geen hogere Vref dan0,80V in deze opstelling.

## Niet volledig doorlopen mechanisch meetformulier — bewaarde velden


Testdatum: ____  Werkelijk geprint project/instellingswijzigingen: ____\
Filament: ____  Bestaand paar hergebruikt? ____  Droog, geen nieuwe smering? ____\
Motorhuis Ø/lengte: ____  As/tandwiel: ____  Winding A/B Ω: ____\
Driver/PCB + R110 bevestigd: ____  VM onder last: ____ V  Vref: ____ V\
Gemeten omwentelingen bij `M 1`: ____  `FULL_STEPS` gebruikt: ____\
Printpassing motor/geleiding/houder/ring, brugdoorhang of draadschade: ____

| Vref | Doel rpm | Last g | Cycli gevraagd / geslaagd | Hoogtes min/max/retour mm boven frame | Tijd s | Stappen missen / slip / startproblemen | Motor-/driverwarmte |
|---|---:|---:|---|---|---|---|---|
| 0,80 V | 5 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 10 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 20 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 40 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 60 / 120 indien soepel | 0 | ____ | ____ | ____ | ____ | ____ |
| ____ | gekozen ____ | 0 | 10 / ____ | ____ | ____ | ____ | ____ |
| ____ | 5 / gekozen ____ | 5 optioneel | ____ | ____ | ____ | ____ | ____ |

Temperatuur: meetwaarde met methode indien beschikbaar, anders “koel/lauw/warm”;
geen verzonnen graden. Hoogte/tijd eveneens als meting of schatting benoemen.

**Succes:** meerdere volledige droge op/neercycli bij een voor mij bruikbare
snelheid, zonder vastlopen, zichtbare stapuitval, slangslip of overmatige warmte.\
**Bruikbare snelheid volgens eigenaar:** ____  **Hoogste foutloze geteste snelheid:** ____\
**Uitkomst:** [ ] voldoende voor deze proef [ ] onvoldoende [ ] onbeslist [ ] nog niet getest.\
**Oorzaak bij fout:** [ ] motorstappen [ ] koppeling slipt [ ] verkeerde passing
[ ] voeding/driver [ ] draadschade [ ] onbekend. Opmerkingen: ____


Doel-rpm hierboven is een instelling. Werkelijke omwentelings-/cyclustijd en
meetmethode: ____. Tijdgebaseerd VACTUAL, oscillator-/UART-stopafwijking inbegrepen; niet als constante snelheid
presenteren. C-cyclus heeft3mm slag en6mm afgelegde weg, plus3×0,3s pauze.

Hardwarefouten, resets en voortijdige120s-stop apart vermelden: ____

VACTUAL (berekend): ____ ; geplande duur: ____ ; werkelijke positie niet gemeten door firmware.
