# E-301 — Pico W, één bestaande schroefpin

**Aanbevolen uitvoering:** Pico W via computer-USB; TMC2208 met VIO 3,3 V;
PD-trigger **9 V** naar VM via zekering, schakelaar en diode; lage fasestroom via
Vref én UART. **Geen Uno, levelshifter of 6V-regelaar nodig. Geen nieuwe print.**

**Status: software op host gevalideerd; fysiek niet getest.** De precieze witte
V1.2-module en paarse PD-print zijn niet eenduidig geïdentificeerd. Er zijn hier
geen foto's van beide PCB-zijden of metingen beschikbaar. De controles hieronder
zijn daarom **verplicht vóór inschakelen**; bij onduidelijkheid stoppen en het
exacte PCB-schema laten controleren. Kleur/versienummer alleen is geen pinout.

Begin hier; volg de stappen in volgorde. Het [schema](wiring.svg), de
[netlijst](wiring.md), [onderbouwing](research.md) en het
[resultatenformulier](resultaten.md) horen bij elkaar. De bestaande
[montagehandleiding](../assembly.md) en het frame blijven bruikbaar.

## 1. Controleer onderdelen, zonder voeding

Al aanwezig volgens eigenaar: Pico W RP2040, witte TMC2208 V1.2 StepStick,
PD-trigger met 5/9/12/15/20V-keuze, PD-adapter, levelshifter en Ø8 × 8,2-mm
vierdraads motor rond 40 Ω per spoel. Levelshifter blijft ongebruikt.

Nog te controleren/aan te vullen (geen bestelling uitgevoerd):

| Aantal | Onderdeel |
|---|---|
| 1 | Multimeter, USB-**data**kabel passend op Pico W (origineel micro-USB), PD-kabel |
| 1 elk | Snelle 250mA-zekering + houder; DC-schakelaar ≥24V/1A binnen handbereik; SS14 |
| 1 elk | Elco **100µF/25V**, keramisch **100nF/25V** bij driver VM-GND |
| 1 | Keramisch 100nF bij driver VIO-GND (naast bestaande moduleontkoppeling) |
| 1 | **TPS3808G01DBVR**, instelbare supervisor, op correct gemarkeerde SOT23-6-adapter |
| 1 | Keramisch 100nF bij supervisor VDD-GND |
| 1 elk | 162kΩ en 10kΩ, **1%**, voor VM-spanningsdeler |
| 4 | 10kΩ: EN-pull-up, STEP-pulldown, RESET-pull-up, MR-pull-up |
| 1 | 1kΩ voor UART-TX |
| divers | Geïsoleerde aansluitdraden, eventuele headers, degelijke soldeer-/gaatjesprint en afneembare RUN-jumper |

De supervisor is het enige extra actieve onderdeel. Hij voorkomt dat terugkerende
motorvoeding een oude beweging hervat. Het kleine IC vraagt soldeerervaring:
gebruik een voorgemonteerde adapter of laat juist dit deel monteren/controleren.
Een kale SOT23-chip mag niet los tussen breadboarddraden hangen.
Bestaande ring/slang/kabelbinders uit de montagehandleiding hergebruiken.

Controlelijst met USB én PD los:

1. Noteer merk/opdruk en maak een tekening/foto van beide zijden van de StepStick.
   Vergelijk **exact die revisie** met fabrikantdocumentatie. Zoek VM, beide GND,
   VIO, STEP, DIR, EN/ENN, PDN_UART en de vier motoruitgangen. Controleer dat VIO
   niet vast aan 5VOUT/VM zit. Controleer twee **R110 = 0,110 Ω** shunts; een
   gewone multimeter kan 0,110 Ω niet nauwkeurig bevestigen. Opdruk en PCB-schema
   zijn hier de basis, geen verzonnen weerstandmeting.
2. Bij FYSETC staat V1.2 als UART-variant beschreven; dezelfde wiki noemt een
   jumper bij PDN_UART voor headerbereikbaarheid. Dit bewijst niet dat jouw clone
   al doorverbonden is. Meet spanningsloos continuïteit van de bedoelde header naar
   de **PDN_UART-net/pad** volgens het passende PCB-schema (IC-pin14 bij TMC2208-LA,
   alleen identificatie voor iemand met meetervaring). Alleen de gedocumenteerde
   UART-brug sluiten als die verbinding ontbreekt. **Geen CLK-brug sluiten en
   geen onbekende drie pads allemaal verbinden.** Geen juiste tekening/verbinding:
   nog niet inschakelen. UART-firmwarecontrole later is een tweede controle.
3. Zoek op het PD-bord de werkelijke OUT+/OUT− en de DIP-tabel voor **dit bord**.
   Er is geen universele DIP-code. Markeer 9V-keuze, maar sluit de uitgang nog
   nergens op aan. Controleer dat adapterlabel een **9V-PD-profiel** noemt.
4. Meet de motorparen: elk paar circa40 Ω, tussen de paren geen verbinding.
   Label A+/A− en B+/B−. Draadkleur is geen bewijs. Bij 0 Ω/onderbreking of
   sterk afwijkende waarde stoppen.
5. Bouw volgens [wiring.md](wiring.md) en [wiring.svg](wiring.svg), nog zonder motor.
   Laat de supervisor→RUN-jumper voor de eerste upload tijdelijk los.
   Verbind GND's; houd VM en 3,3 V strikt gescheiden. Controleer polariteit van
   diode en elco, alle pullweerstanden en afwezigheid van kortsluiting.

## 2. Software installeren (motorvoeding UIT)

We gebruiken **MicroPython v1.26.1 voor RPI_PICO_W** met Thonny. Deze stabiele,
vaste versie gebruikt alleen ingebouwde modules; geen Arduino-core/libraries,
Wi-Fi-instellingen of account nodig. Een nieuwere versie is geen hier geteste
vervanging. De Python-bronnen vormen de complete toepassing; de interpreter
compileert ze op de Pico bij laden. Er is geen zelfgebouwde UF2 nodig.

1. Installeer [Thonny](https://thonny.org/). Kies onder Extra/Opties/Interpreter
   **MicroPython (Raspberry Pi Pico)** en de bijbehorende USB-poort.
2. USB en PD los, motor los, RUN-jumper los; EN-pull-up aangesloten. Houd BOOTSEL
   ingedrukt terwijl je de Pico op computer-USB aansluit. Laat los zodra het
   station **RPI-RP2** verschijnt.
3. Download de **v1.26.1 UF2 voor Pico W** via de
   [officiële downloadpagina](https://micropython.org/download/RPI_PICO_W/)
   (niet Pico 2 W en geen preview). Kopieer naar RPI-RP2; de Pico herstart.
4. Open in Thonny de meegeleverde `tmc2208.py`, `motion_policy.py` en
   `controller.py`. Sla ze met **dezelfde namen op Raspberry Pi Pico**, direct
   in de hoofdmap `/`. Sla als laatste `main.py` in diezelfde hoofdmap op.
   Kopieer de map `tests` niet naar de Pico. Verwijder eventuele oude eigen
   `boot.py` die pinnen/motoren bedient; bewaar zo nodig eerst een lokale kopie.
5. Herstart de Pico door USB los/vast. Bij losgenomen RUN-jumper en VM uit
   verschijnt `E-301 Pico W OFF...`. Er mag geen STEP-puls/beweging zijn.
   Zet een voltmeter tussen EN en GND: EN moet circa3,3 V zijn.
6. Sluit Thonny voor de bewegingsproef. Gebruik een eenvoudige seriële terminal
   zoals PuTTY (Windows) of een aanwezige serial monitor: **115200, 8N1, geen
   flow control, newline/LF bij Enter**. De USB-baudkeuze stelt de TMC-UART niet in;
   de code gebruikt intern UART1 op115200. Windows-poort is COM…, Linux meestal
   `/dev/ttyACM…`, macOS `/dev/cu.usbmodem…`.
   Typ `?` en Enter: je krijgt de commandohulp. Typ commando's als tekst, zonder
   Python-aanhalingstekens. **Eén commando per keer; wacht het antwoord af.**

Bij aanpassen/uploaden later: `OFF`, VM uit, wachten tot VM<0,5V, USB los,
RUN-jumper los. Daarna USB aan en Thonny Stop/Ctrl-C; de `finally`-afhandeling
zet EN hoog. Bewerk bestanden, herstart en controleer OFF. RUN-jumper altijd
terug vóór motorgebruik. Geen scripts via Thonny Run starten terwijl VM aan staat.

## 3. Kies en meet 9 V; controleer beveiliging (motor nog los)

1. Koppel PD-bord los van de schakeling. Kies 9V volgens zijn eigen DIP-tabel,
   sluit adapter aan en meet OUT+/OUT−. Verwacht rond9V; **8,55–9,45V** is de
   hier gebruikte acceptatieband. Bij 5V-fallback/12V/15V/20V stoppen; DIP nooit
   onder aangesloten motorvoeding omschakelen.
2. PD weer los, verbind met zekering→schakelaar→SS14→VM; diodeband naar VM.
   Verbind de supervisor→RUN-jumper. Zet Pico USB aan, dan PD en VM-schakelaar.
   De Pico blijft in reset zolang VM te laag is; de USB-poort kan daarbij verdwijnen.
3. Meet VM na de diode: normaal circa8–9V, hier accepteren **7,7–9,45V**;
   meet VIO circa3,3V en EN circa3,3V. Meet supervisor SENSE circa `VM/17,2`.
   De spanningsdrempel is berekend6,97V, geen gemeten waarde. Doe een veilige
   functionele resettest: VM uit → Pico USB-poort valt weg; VM aan → OFF-melding,
   EN blijft hoog. Terminal zo nodig opnieuw verbinden. Géén ARM automatisch.
   Als deze test faalt: niet verder, supervisor/RUN-bedrading herstellen.
4. Met motor los, voeding aan en zonder ARM: stel Vref-meetpunt op
   **0,80V** met multimeter en geïsoleerde trimschroevendraaier. Raak geen andere
   pinnen. Gebruik het bevestigde Vref-meetpunt, niet willekeurig de koelplaat.
   EN blijft hoog. Noteer Vref en beide shuntopdrukken.
5. Typ `ARM MOTOR`: verwacht `ARMED MOTOR`. Dit controleert chip-ID, alle zeven
   writes met elk een IFCNT-bevestiging, leesbare configuratie en foutstatus.
   **ARM schakelt EN nog niet laag.** Geen ARMED: `OFF`, voeding uit, UART-brug,
   RX/TX/1k/GND en boardidentiteit nalopen. Nooit EN aan GND leggen als oplossing.
6. Typ `OFF`. VM uit en wachten op <0,5V. USB ook los voor aansluiten motor.

Bij Vref0,80V, tweeR110, VSENSE1 en IRUN=IHOLD5 is de berekende fasestroom
**77mA piek /55mA RMS**, niet de stroom die de PD-adapter levert. UART is
verplicht: Vref alleen geeft deze limiet niet. De motor heeft geen sluitend
passende fabrikantdatasheet; verhoog de stroom in deze aanbevolen opstelling
niet boven0,80V. Anders zou een nieuwe stroom-/warmtebeoordeling nodig zijn.
Een multimeter op de voedingsingang bewijst de fasepiek niet. Werkelijke
fasepiek kan alleen met geschikte stroomprobe of differentiële shuntmeting
worden gecontroleerd; laat dat uitvoeren als de identiteit/stroominstelling
onzeker is. Een geaarde scoopclip op een motoruitgang kan kortsluiting maken.

## 4. Losse motor eerst

1. Sluit de twee gemeten spoelparen spanningsloos aan, **pin/mechanische last los**.
   USB aan, VM aan. Na boot staat de uitgang OFF; terminal opnieuw verbinden indien nodig.
   Een opstartmelding kan vóór de verbinding verstuurd zijn; controleer met `?`.
2. Typ achtereenvolgens `ARM MOTOR`, `S 5`, `M 1`, telkens antwoord afwachten.
   Tel aan een verwijderbare asmarkering één werkelijke omwenteling; alleen
   dezelfde eindhoek bewijst geen enkele omwenteling. Dan `M -1`.
   Motor mag niet ratelen/blokkeren; stop direct met `!` of de VM-schakelaar.
3. De firmware neemt voorlopig20 hele stappen/omwenteling aan, dus160 STEP-pulsen.
   Klopt één omwenteling niet: `OFF`, beide voedingen uit. Pas `FULL_STEPS` in
   `motion_policy.py` aan op een **bevestigde** staphoek, upload als boven en test
   opnieuw zonder pin. Niet gokken op een verhouding onder blokkering.
4. Controleer foutstop met losse motor op5rpm: start `M 1`, stuur `!` tijdens
   draaien. Verwacht STOP/OFF. `M 1` wordt nu geweigerd tot nieuwe ARM.
5. Controleer uitval/herstel: nieuwe ARM en `M 1`, VM-schakelaar uit tijdens
   beweging. Wacht op VM<0,5V, VM weer aan. Verwacht uitsluitend OFF, geen
   hervatte puls/beweging. Ook USB los/vast met VM aanwezig moet OFF blijven.
   Na30s zonder commando moet OFF volgen. **Elk falen blokkeert de pinproef.**
6. UART-foutproef is optioneel met motor los: voedingen uit, alleen TX losnemen,
   opnieuw voeden en ARM proberen: geen ARMED/beweging. Daarna alles uit en TX
   terug. Nooit motoruitgangen onder spanning losmaken.

Een korte uitlijnbeweging wanneer een expliciet M/C-commando de spoelen voor
het eerst bekrachtigt is mogelijk; dat is geen fysieke homing. De firmware
heeft geen sensor en kan gemiste stappen niet detecteren. `OFF` laat de as vrij.

## 5. Bestaand frame en schroefpin

1. `OFF`, VM uit, wachten op<0,5V, USB los. Gebruik de bestaande montage,
   ring en slangkoppeling. Controleer dat alles droog en handmatig over3mm vrij
   loopt. Geen nieuwe print, draadschuren, geforceerde passing of aangedreven eindstop.
2. Zet pin handmatig op **7,1mm boven geleideblok**, controleer vrij bereik
   **5,6–8,6mm**, terug op7,1. Markeer nul en koppeling om slip te zien.
3. USB en VM aan, terminal verbinden, `ARM PIN`, `S 5`, `M 0.25`, `M -0.25`.
   Dit vraagt ±0,75mm bij3mm spoed. Controleer draairichting en retour.
4. Vanuit software-nul `C 1`: midden→+1,5mm→−1,5mm→midden, dus3mm totale slag.
   Bij soepel bewegen herhalen op `S 10`,20,40, eventueel60 en120; telkens `C 1`.
5. Op een bruikbare snelheid `C 10`. Bij heel lage rpm stopt de proef mogelijk
   op de120s-grens: dit is een veiligheidsstop, geen bewijs van motorfalen.
   Na elke OFF/stop/reset opnieuw spanningsloos handmatig centreren voor ARM PIN.
6. Registreer alle resultaten in [resultaten.md](resultaten.md). Eerst zonder
   extra last; een bestaande optionele5g-proef alleen na soepel droog bewegen.

**Stop bij vastlopen, ratelen, slip, scheuren, geur, snel oplopende warmte of
motorhuis rond45°C.** Bij twijfel eerst VM uit. Een uitgeschakelde pin kan onder
last zakken. Laat de proef niet onbeheerd; houd de schakelaar bereikbaar.

## Commando's en limieten

| Commando | Betekenis |
|---|---|
| `?` | Hulp |
| `ARM MOTOR` | Pin los; verifieert/configureert driver; nog geen beweging |
| `ARM PIN` | Eigenaar verklaart handmatige middenstand als nul |
| `S 5` | Doelsnelheid2–120rpm; standaard5 |
| `M 0.25` / `M -0.25` | Relatieve beweging; maximaal±1omw/opdracht |
| `C 1` / `C 10` | 1–20 cycli vanaf PIN-nul, elk +½,−1,+½omw |
| `!` | Softwarestop zonder Enter, ook tijdens bewegen |
| `OFF` | Uit; nul vervalt. Ctrl-C in terminal stopt de toepassing ook veilig. |

PIN-mode heeft een absolute limiet±½omw rond nul. Overschrijdende opdracht
wordt geheel geweigerd. Ook ongeldige commando's schakelen conservatief uit
(strenger dan Uno). Andere invoer tijdens beweging vervalt; geen wachtrij.
Stuur pas na DONE/CYCLE-resultaat een volgend commando.30s inactiviteit en120s
per bewegingsopdracht schakelen uit. Een gebroken USB-verbinding is geen
gegarandeerde directe stop; fysieke schakelaar gebruiken. Bij VM-uitval volgt
hardware-reset; opnieuw verbinden, centreren, ARM. UART/configuratiefouten
worden vóór elk segment en ongeveer elke100ms gecontroleerd; timeout35ms per
read. `!` kan door een lopende UART-transactie kort vertraagd worden.

Doel-rpm is geen gemeten snelheid: ramp, Python-uitvoering en periodieke UART
controles vertragen vooral korte slagen. Meet echte omwentelings-/cyclustijd.
Nominale constante snelheid is `3 × rpm/60 mm/s`; bij120rpm dus6mm/s vóór
ramp/overhead. Een volledige C-cyclus bevat2omw en drie pauzes van0,3s.
De afgelegde afstand is **6mm per cyclus** (1,5+3+1,5), bij een **3mm slag**.
Noteer cyclustijd apart.
