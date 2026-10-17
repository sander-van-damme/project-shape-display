# Bedrading en bediening

Gebruik één **Arduino Uno R3 (ATmega328P, 5-V logica)** en een **TMC2208**
StepStick met UART-aansluiting, twee externe **R110** shunts en Vref-trimmer.
Geen sensoren, homing of automatische hoogtecorrectie. Het programma telt
alleen verstuurde stappen en weet niet of de motor daadwerkelijk volgt.

## Onderdelen

| Aantal | Onderdeel / specificatie |
|---|---|
| 1 | Bestaande Ø8 × 8,2-mm bipolaire 4-draads motor, circa 40 Ω per fase |
| 1 | Uno R3 + USB-datakabel; geen Nano-boardselectie nodig |
| 1 | TMC2208 met R110, bereikbaar PDN_UART, VIO, EN, STEP, DIR, Vref |
| 1 | Geregelde **6,0-V DC** voeding, minimaal 0,3 A; liefst labvoeding op **0,25-A stroomlimiet** |
| 1 elk | Aan/uit-schakelaar in motorvoeding; 250-mA snelle zekering; SS14-Schottkydiode (1 A / 40 V) |
| 1 elk | 100-µF / ≥16-V elco en 100-nF keramisch, direct bij VM/GND |
| 1 elk | 1-kΩ serieweerstand voor UART-TX; 10-kΩ pull-up voor EN |
| divers | Multimeter, geïsoleerde draad/connectoren; PCB-afstandhouders of isolerende onderlegger |

Een klein koellichaam op de driver mag, maar mag geen pinnen/kortsluiting raken.
Een fan is voor deze lage stroom niet als vereiste opgelegd. De micro-motor kan
zelf wél warm worden; korte proeven en temperatuurcontrole blijven nodig.

## Aansluitingen

Zie het [bedradingsschema](wiring.svg). **D2, D3 enz. zijn de pinnummers op de
Uno-header.** De TMC-zijde gebruikt de **op het gekozen PCB gelabelde namen**;
de fysieke positie van een 16-pins cloneheader is niet universeel. Het is geen
chip-QFN-pinout. Zoek de UART-soldeerbrug van jouw MC2208 V1.2 op in zijn PCB-schema
en sluit die indien nodig spanningsloos. Geen trace doorsnijden of motor aanpassen.

| Uno / bron | TMC2208-aansluiting / bestemming |
|---|---|
| Uno **D2** | **STEP** |
| Uno **D3** | **DIR** |
| Uno **D4** | **EN / ENN** (actief laag) |
| Uno **5V** via **10 kΩ** | Zelfde **EN**-knooppunt; houdt de motor uit tijdens reset/upload |
| Uno **D8** (SoftwareSerial RX) | **PDN_UART** rechtstreeks |
| Uno **D9** (SoftwareSerial TX) via **1 kΩ** | Zelfde **PDN_UART**-knooppunt |
| Uno **5V** | **VIO**; uitsluitend logica |
| Uno **GND**, voeding − | **GND**; gemeenschappelijk referentiepunt |
| 6,0 V + → zekering → schakelaar → SS14 | **VM / VMOT**; diodeband (kathode) naar VM |
| Elco + en 100 nF | **VM**, na diode; elco − naar **GND** |
| Gemeten eerste spoelpaar | **1A / A1** en **1B / A2** (één H-brug/fase A) |
| Gemeten tweede spoelpaar | **2A / B1** en **2B / B2** (één H-brug/fase B) |
| MS1, MS2 | **GND**; microstapkeuze wordt via UART overschreven |
| CLK (alleen indien aanwezig) | GND volgens modulehandleiding, interne oscillator |

Let op verschillende labelconventies: `1A/1B` is één fase, maar bij `A1/A2`
is dát één fase. Gebruik de fasemarkering in het **schema van jouw module**,
niet twee willekeurige aangrenzende motorklemmen. Verbind geen uitgang met GND.
De historische kleurregel blauw/zwart en rood/wit is alleen een aanwijzing;
de andere kleurregel is foutief. Meet spanningsloos: binnen een paar circa 40 Ω,
tussen paren geen continuïteit. Bij 0 Ω, onderbroken spoel, significant andere
weerstand of onduidelijke labels: niet inschakelen.

**6 V nooit op Uno 5V, VIO of USB zetten.** Uno krijgt USB-voeding; alleen de
minpolen worden gedeeld. Motordriver niet omgekeerd insteken. VM meten na de diode:
typisch 5,5–5,8 V, **altijd minstens 4,75 V** tijdens draaien. Een 5-V-bron met
deze diode heeft te weinig marge. De elco moet aan de driverzijde van de schakelaar
blijven. Zet de schakelaar binnen handbereik. Wacht na uitschakelen op VM <0,5 V.
**Nooit een motorstekker aansluiten/losmaken zolang VM aan staat.**

## Verplichte stroominstelling, vóór de motor aansluiten

1. Controleer beide shunts op de driver: markering **R110**. Is het een ander
   bord of een andere shuntwaarde, gebruik de berekening in `sources.md` en het
   echte PCB-schema; de onderstaande getallen gelden dan niet automatisch.
2. Upload eerst de code. EN is hoog vanaf reset en heeft daarnaast een 10-kΩ
   pull-up. Laat de motor nog los. USB en motorvoeding aan; geen ARM-commando.
3. Multimeter op DC volt: zwart GND, rood Vref-meetpunt/trimmer volgens het
   modulehandleiding. Gebruik een geïsoleerde trimschroevendraaier; raak geen
   andere pinnen. Stel **Vref = 0,80 V** in. Niet afgaan op de potmeterhoek.
4. Schakel VM uit, wacht tot <0,5 V, sluit pas dan de motor aan. Controleer de
   polariteit en windingparen opnieuw. Vref alleen verandert de huidige chip-
   stroom niet naar de gewenste lage waarde: **de UART-configuratie is verplicht**.
5. Bij ARM schrijft en controleert de firmware de driverconfiguratie terwijl
   EN hoog blijft. Geen correcte chip-ID/configuratie/IFCNT-writebevestiging:
   **geen beweging**. `ERROR` oplossen in bedrading/UART-soldeerbrug; nooit EN
   handmatig laag verbinden of de softwarecontrole verwijderen.

De code zet SpreadCycle, VSENSE=1, IRUN=IHOLD=5, 8 microstappen en geen interpolatie.
Bij 0,80 V/R110 is de berekende fasepiek circa **77 mA**, RMS circa **55 mA**.
Supply-stroom is **niet** de fasestroom; stel geen Vref op basis van de voedingampèremeter af.
De formule en beperkingen staan in [sources.md](sources.md).

Als de motor bij 0,80 V koel blijft maar onder de droge last niet start, mag je
dezelfde proef eerst bij **1,00 V**, daarna maximaal **1,20 V** herhalen; motor
telkens los aansluiten volgens de uitschakelprocedure en Vref zonder motor
verstellen. Dat geeft nominale pieken 96 en 116 mA, geen toestemming om verder
op te voeren. Stroominstelling in het resultatenformulier noteren. Als de motor
al warm wordt of blokkeert: stoppen en afkoelen, geen stroomverhoging.

## Software installeren en uploaden

1. Installeer **Arduino IDE 2.x** van <https://www.arduino.cc/en/software>.
2. Installeer in Boards Manager **Arduino AVR Boards 1.8.8**.
3. Installeer in Library Manager **TMCStepper 0.7.3**. SoftwareSerial zit in de
   AVR-core. Open `controller/controller.ino`; houd `motion_policy.h` ernaast.
4. Selecteer **Arduino Uno**, de juiste USB-poort en Upload. Motorvoeding uit
   tijdens uploaden. Open Serial Monitor op **115200 baud**, regelafsluiting **Newline**.
5. Firmware meldt dat de uitgang uit staat. Geen automatische beweging bij start.

Alternatief met Arduino CLI, vanuit deze testmap:

```sh
arduino-cli core update-index
arduino-cli core install arduino:avr@1.8.8
arduino-cli lib install TMCStepper@0.7.3
arduino-cli compile --fqbn arduino:avr:uno controller
arduino-cli upload --fqbn arduino:avr:uno --port /jouw/USB-poort controller
```

Er is echt voor Uno gecompileerd met deze core/library. Upload, fysieke UART,
motorstroom en beweging kunnen hier zonder aangesloten hardware niet zijn getest.

## Commando's

| Invoer | Werking |
|---|---|
| `?` | Korte hulp |
| `ARM MOTOR` | Controleert driver; alleen gebruiken met **pin losgenomen** |
| `S 5` | Doelsnelheid 5 rpm; instelbaar **2–120 rpm** |
| `M 1` / `M -1` | Eén motoromwenteling in beide richtingen, alleen na staphoekcontrole |
| `OFF` | Uitgang uit; verklaarde middenstand ongeldig |
| `ARM PIN` | Alleen na **handmatig op 7,1-mm uitstekende pin centreren**; verklaart die stand als nul |
| `M 0.25` / `M -0.25` | Relatief ±¼ omwenteling ≈ ±0,75 mm; richting eerst controleren |
| `C 1` | Vanaf nul: +½, −1, +½ omwenteling; één volledige 3-mm op/neercyclus |
| `C 10` | Tien cycli; maximaal 20 per commando en 120 s aaneengesloten |
| `!` | Onmiddellijke softwarestop; ook tijdens beweging, geen newline nodig |

Begin los van de pin bij `ARM MOTOR`, `S 5`, `M 1`; **tel** één werkelijke
omwenteling aan een verwijderbare markering. Alleen terugkeren naar dezelfde
markering is onvoldoende: twee omwentelingen eindigen daar ook. De code neemt
voorlopig **20 hele stappen/omw** aan, afkomstig uit de afwijkende PDF, en dus
160 STEP-pulsen/omw met 8 microstappen. Als de werkelijke omwenteling anders is,
pas `FULL_STEPS` in `motion_policy.h` aan en upload/test opnieuw **vóór montage
van de pin**. Verwar “microstappenmotor” niet met een gegarandeerde staphoek.

`M` is begrensd tot maximaal 1 omwenteling per opdracht; in PIN-mode geldt
daarnaast de absolute softwaregrens **±½ omwenteling** rond de handmatige nul.
Een opdracht buiten die grens wordt geheel geweigerd. Beide draairichtingen
zijn elektrisch mogelijk. Bij omgekeerde mechanische richting kun je
`REVERSE_DIR` wijzigen; schroefdraden en motordraden niet onder spanning omsteken.

De korte snelheidsramp maakt het gemiddelde bij kleine slagen lager dan de
ingestelde snelheid. Nominale continue snelheid: `3 × rpm / 60` mm/s.
`C` werkt alleen vanuit software-nul. Tijdens beweging worden andere seriële
tekens weggegooid, behalve `!`; er ontstaat geen wachtrij met latere bewegingen.
Na **30 s zonder commando** of **120 s beweging** schakelt de uitgang uit en
vervalt de nul. Daarna opnieuw handmatig centreren, niet blind ARM PIN sturen.
Een verdwenen USB-verbinding stopt niet onmiddellijk: gebruik de fysieke
VM-schakelaar. De uitgeschakelde pin kan onder last terugzakken.

Na een stop met de **VM-schakelaar** kan de Uno nog stappen versturen terwijl
de driver zijn instellingen verliest. **VM niet opnieuw inschakelen zolang de
Uno nog gewapend is:** stuur ook `!`, of druk met VM uit op Uno RESET. Daarna
handmatig centreren en pas na herstel van VM opnieuw ARM uitvoeren, zodat de
lage stroominstelling opnieuw wordt geschreven vóór EN laag mag worden.

**Stop direct bij blokkeren, ratelen zonder verplaatsing, slangslip, scheurvorming,
geur, motorhuis rond 45 °C of duidelijk snel stijgende temperatuur.** Eerst `!`
of VM-schakelaar, dan spanningsloos onderzoeken. Een blokkering niet langer
aandrijven om te kijken of hij loskomt. Geen aangedreven mechanische eindstop zoeken.
