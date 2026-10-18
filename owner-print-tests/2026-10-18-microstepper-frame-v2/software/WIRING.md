# Bedrading en reproduceerbare opstart

[Schema voor beide UART-varianten](wiring.svg). Verbind op **netnamen**:
de pinvolgorde van de witte V1.2-module is niet onafhankelijk vastgesteld.
Controleer de eigen print, UART-soldeerbrug en shunts. Geen 5V-signalen op Pico-GPIO.

| Net | Verbinding |
|---|---|
| Pico voeding | USB van computer |
| TMC VIO | Pico 3V3 OUT, fysieke pin 36, gemeten circa 3,3 V |
| GND | Pico GND (bv. pin 38), TMC GND en motorvoeding-GND gemeenschappelijk |
| TMC VM | Bestaande circa 9 V-voeding via bereikbare schakelaar, zekering/diode en bestaande ontkoppeling; nooit via Pico 3V3 |
| Motor | Beide geïdentificeerde windingparen op OA1/OA2 en OB1/OB2; nooit onder spanning ompluggen |
| TMC STEP / DIR | Beide vast aan GND; niet laten zweven |
| TMC EN / ENN | Pico **GP6, fysieke pin 9**, plus **10 kΩ naar VIO**; hoog = uit, laag = uitgangen toegestaan |
| Vref | Fysiek ingesteld en handmatig gemeten; begin circa 0,80 V zoals eigenaarproef |

De externe EN-pull-up houdt de uitgang vóór en tijdens Pico-opstart uit. Firmware
zet EN hoog vóór UART-initialisatie en pas laag na succesvolle configuratie.
EN is een eenvoudige uitgangsblokkering, geen gecertificeerde noodstop. Zonder
fysiek aangesloten EN-draad kan volledige driver-UART-uitval een UART-stop
onmogelijk maken. De software kan de aanwezigheid van die draad niet bewijzen.

## A. Eén GPIO met PIO — nieuwe standaard

```text
Pico GP4 (pin 6) ── 1 kΩ ──┬── TMC PDN_UART / juiste UART-header
                           └── 10 kΩ ── VIO 3,3 V
Pico GP6 (pin 9) ────────────── TMC ENN
                               │
                             10 kΩ
                               │
                            VIO 3,3 V
TMC STEP ── GND       TMC DIR ── GND
```

GP4 verzendt en ontvangt. PIO schakelt de GPIO na de volledige stopbit naar
input, vóór het driverantwoord. Tijdens ontvangen drijft de Pico de lijn niet.
De 1kΩ is serieweerstand; de 10kΩ zorgt voor een duidelijke rust-high op de bus.
Geen tweede RX-draad. Standaard 115200 baud, 8N1, TMC-adres 0.
Timing en foutafhandeling zijn gesimuleerd; verifieer eerst zonder gekoppelde pin.

## B. Twee GPIO's met hardware-UART — vergelijkingsfallback

```text
Pico GP4 TX (pin 6) ── 1 kΩ ──┬── TMC PDN_UART
Pico GP5 RX (pin 7) ───────────┘
```

Kies in `MOTOR_CHANNELS` de uitgecommentarieerde `transport: hardware`-regel
**in plaats van** de PIO-regel voor m1. UART1, 115200, GP4/GP5. RX ziet de
verplichte TX-echo plus het antwoord; firmware controleert beide. Wanneer de
TMC antwoordt blijft de hardware-TX hoog via de 1kΩ: de weerstand begrenst de
stroom en RX zit aan de driverzijde. Verbind TX nooit rechtstreeks zonder weerstand.
Alle overige aansluitingen, inclusief STEP/DIR/EN, blijven zoals boven beschreven.

## Wat historisch werkelijk werkte

In de eigenaarproef van 18 oktober: GP4 TX via 1kΩ en GP5 RX naar dezelfde
UART-header, VIO na kabelcorrectie 3,3 V, VM circa 9 V en Vref circa 0,80 V.
**EN aan GND** maakte beweging mogelijk; losgelaten EN was gemeten 3,24 V en
blokkeerde de motor. STEP/DIR waren toen los; ongewenste opstartbeweging werd
gemeld. Dat bewijst niet dat zwevende ingangen bruikbaar zijn. De aanbevolen
nieuwe EN-/STEP-/DIR-bedrading is een wijziging die nog fysiek moet worden getoetst.
Met EN permanent aan GND kan de motor al vóór de lage UART-stroomconfiguratie
bekrachtigd worden. `enable_pin: None` is alleen een expliciete vergelijkingsoptie
voor die bestaande benchbedrading, met die beperking.

## Opstart en kleinste fysieke vervolgstest

1. Motorvoeding uit. Controleer netnamen, gezamenlijke GND, twee windingparen,
   UART-brug, R110-aanname, vaste STEP/DIR en EN-pull-up. Begin zonder mechanische
   pinbelasting. Houd de motorvoedingsschakelaar bereikbaar.
2. Start Pico via USB; EN hoort hoog. Meet VIO. Schakel VM in en controleer VM
   en fysiek ingestelde Vref. Een ontbrekende VM bij boot wordt gelogd; de eerste
   start voert opnieuw een volledige controle uit.
3. Verbind GUI, kies m1 en `e301_conservative`. Diagnose moet versie `0x20`,
   `SEL_A=1`, geldige CRC/IFCNT en geen driverfout tonen. Een historische resetbit
   wordt bij configuratie gewist en daarna opnieuw gecontroleerd.
4. Test eerst 0,25 omwenteling op 10 RPM met rustige ramp. Controleer richting,
   werkelijke beweging en STOP. Geen handmatige ARM-procedure.
5. Test kort continu draaien en sluit de desktop onverwacht af / trek USB uit.
   Bij nog gevoede Pico moet de heartbeat de motor na circa 2 s uitschakelen;
   bij stroomloze Pico moet de externe EN-pull-up hem uit houden. Controleer dat
   opnieuw verbinden geen beweging hervat. Dit is een fysieke test, geen garantie
   uit de hosttests. Controleer UART-foutstop eerst zonder mechanische belasting.
6. Vergelijk PIO met hardware-UART bij 115200. Meet eventueel met logic analyzer
   dat GP4 tijdens het antwoord input is. Pas daarna korte pinbewegingen met
   **zelf gemeten bruikbare slag** en ruime mechanische marge.

De eventuele bestaande VM-supervisor mag blijven zitten; deze software introduceert
of kwalificeert geen nieuwe voedingsbewaking. UART-status meet geen VM-spanning,
Vref, motorpositie, motortemperatuur of stall. Abrupt uitschakelen kan een last
laten zakken; de fysieke constructie en operator blijven daarvoor bepalend.
