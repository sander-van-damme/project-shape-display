# E-301 — aansluitlijst bij het visuele schema

[Visueel schema](wiring.svg). Netnamen in gekleurde labels zijn elektrische
verbindingen, ook als er geen doorlopende lijn over het blad is getekend.
Alle GND-labels zijn één gemeenschappelijke verbinding. Maak korte draden bij de
driver en condensatoren. Labels op de module moeten met het exacte PCB-schema
bevestigd zijn; het TMC-blok is **geen fysieke header-volgorde**.

## Pico W: bovenaanzicht met USB-connector boven

Links van boven naar beneden fysieke1–20; rechts van boven naar beneden40–21.
Niet tellen vanaf een willekeurig gedraaid board. Vergelijk de officiële
[Pico W-pinout](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#wireless-board-layout).
De andere Pico-pinnen blijven los, inclusief VBUS/VSYS/3V3_EN.

| Pico-signaal | Fysieke pin | Naar |
|---|---:|---|
| GP2 | 4 | Driver STEP; dezelfde node via10kΩ naarGND |
| GP3 | 5 | Driver DIR |
| GP4 / UART1 TX | 6 | **1kΩ serie** → PDN_UART-node |
| GP5 / UART1 RX | 7 | Rechtstreeks dezelfde PDN_UART-node |
| GP6 | 9 | Driver EN/ENN; dezelfde node via10kΩ naar3,3V |
| 3V3(OUT) | 36 | Driver VIO; supervisor VDD; alle3,3V-pullups |
| GND | 38 | Driver GND, PD OUT−, supervisor GND, alle GND-labels |
| RUN, geen GPIO | 30 | Supervisor RESET_N via afneembare J1-jumper |

VIO krijgt uitsluitend3,3V; **5VOUT van de TMC blijft onaangesloten aan de Pico**.
Voed de Pico alleen via zijn USB-connector. Verbind PD+ nooit met VBUS/VSYS/VIO.

## Driver en motor

| Bevestigde TMC-node | Verbinding |
|---|---|
| VM / VMOT | PD OUT+ →250mA snelle zekering→schakelaar→SS14-anode→kathode/band→VM |
| Alle driver GND | Gemeenschappelijke GND |
| VM-GND | 100µF/25V elco (+naarVM, −naarGND), parallel100nF/25V; vlak bij driver |
| VIO-GND | 100nF keramisch, vlak bij driver; moduleonderdelen behouden |
| STEP, DIR, EN, PDN_UART, VIO | Volgens Pico-tabel |
| MS1, MS2 | GND (UART overschrijft microstapkeuze) |
| CLK indien aanwezig | GND na bevestiging dat dit CLK_IN is; interne klok |
| DIAG / INDEX / 5VOUT | Niet extern aansluiten |
| Vref | Alleen gemarkeerd meetpunt/trimmer; instellen op0,80V t.o.v.GND |
| FaseA: OA1/OA2 of M1A/M1B | Gemeten spoelpaarA, circa40Ω |
| FaseB: OB1/OB2 of M2A/M2B | Gemeten spoelpaarB, circa40Ω |

Bij andere labels: `1A/1B` kan één fase zijn; bij `A1/A2` is dát één fase.
Alleen het echte PCB-schema beslist; aangrenzende pins hoeven geen spoelpaar te
zijn. Geen motoruitgang aan GND, geen uitgang over twee fasen combineren.

UART: TX via1k en RX direct samen op **één** PDN_UART-net. De1k scheidt TX van
het antwoord van de driver; het is geen levelshifter. Eventuele twee
UART-headers zijn alleen uitwisselbaar als het PCB-schema dat aantoont.
Verplichte UART-brugcontrole staat in de [handleiding stap1](handleiding.md#1-controleer-onderdelen-zonder-voeding).

## Supervisor: alleen TPS3808G01DBVR, SOT23-6 / DBV

Gebruik een gemarkeerde adapter. De onderstaande fysieke IC-pinnen zijn uit het
TI-DBV-schema, niet de mogelijk afwijkend gerangschikte adapterheader. Let op de
pin1-markering/bovenaanzicht; WSON/DRV gebruikt een andere pinvolgorde.

| DBV-pin | Naam | Verbinding |
|---:|---|---|
| 1 | RESET_N, open drain | ViaJ1 naarPico RUN fysieke30; **10kΩ naar3,3V op supervisorzijde** |
| 2 | GND | GND |
| 3 | MR_N | 10kΩ naar3,3V; geen losse zwevende draad |
| 4 | CT | Open, geen draad/condensator; standaard20ms hersteldelay |
| 5 | SENSE | VM →**162kΩ1%**→SENSE→**10kΩ1%**→GND |
| 6 | VDD | Pico3,3V;100nF naarGND vlak bij IC |

De spanningsdeler bemonstert **VM ná diode/schakelaar**, niet vóór de schakelaar.
Supervisor en Pico delen USB3,3V. Bij VM onder ongeveer6,97V trekt RESET_N RUN
laag: GPIO's worden hoogohmig, EN-pullup schakelt de motor uit en STEP-pulldown
houdt pulsen tegen. Bij herstel boot de Pico opnieuw in OFF, zonder oude
beweging of nul. Er is geen automatische herarming. J1 is alleen tijdelijk los
voor installatie met VM uit; maak hem herkenbaar en zet hem terug vóór testen.

Dit is een getekende en berekende benchschakeling, geen gebouwde/gecertificeerde
veiligheidscontroller. Supervisorvertraging is typisch20µs; willekeurige
ultrakorte harde VM-kortsluitpulsen zijn niet fysiek gekwalificeerd. De lokale
100µF en detectie rond7V geven bij normale adapteruitval marge vóór de
TMC-ondergrens. Verplichte fysieke hersteltest: zie handleiding.
