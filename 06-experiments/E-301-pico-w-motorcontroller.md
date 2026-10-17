---
status: complete
builds-on: [E-295]
---

# E-301 — Pico W voor de bestaande microstepper-schroefpinproef

**Eigenaarsopdracht, 17 oktober 2026.** Vraag: kan de bestaande Ø8 × 8,2-mm
stappenmotor de compacte pin betrouwbaar omhoog/omlaag bewegen, bij welke
werkelijke snelheid? E-301 levert de elektronica/firmware om dat zonder Uno te
meten; er is geen nieuwe fysieke motoruitslag. Basiscommit `8cc371d`, aanvankelijk
schone repository; E-301 was beschikbaar. Bestaande CAD, STLs,3MF, motorhouder en
schroefgeometrie zijn ongewijzigd; geen print of aankoop uitgevoerd/opgedragen.

## Aanbevolen opstelling

Computer-USB→Pico W, uitsluitend3,3V UART→TMC2208/R110,
9V USB-C PD→zekering/schakelaar/SS14/ontkoppeling→VM. Start opVref0,80V met
UART VSENSE1, IRUN=IHOLD5: berekend77mApiek/55mARMS. Geen6V-regelaar of
levelshifter. Een TPS3808G01 bewaakt VM rond7V en reset de Pico via RUN bij
uitval; na boot probeert de firmware OFF via UART en vervallen opdracht/nul.
Actuele eigenaarskeuze: STEP/DIR/EN volledig los, zonder externe weerstanden.
VACTUAL regelt beweging/richting; TOFF0 schakelt bij stop de uitgangen uit.
Zwevende EN kan niet door software worden overruled; volledige UART-uitval
kan stoppen verhinderen. De eerdere GPIO-uitvoering blijft alleen in Git-historie.

De concrete witte V1.2-module en paarse PD-print zijn niet door kleur/opdruk
bevestigd. Hun werkelijke pinmapping, R110-shunts, UART-brug en9V-DIP-keuze
zijn verplichte controles vóór inschakelen. Een fysiek onzekere aansluiting
wordt niet ingevuld met een generieke StepStick-pinvolgorde.

## Oplevering en bewijs

- [Praktische handleiding, onderdelen en installatie](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/handleiding.md).
- [Visueel schema](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/wiring.svg) en [exacte aansluitlijst](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/wiring.md).
- [Complete MicroPython-toepassing](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/main.py), met afzonderlijke UART-driver, controller en gedeelde bewegingspolicy in dezelfde map.
- [Datasheetafweging en berekeningen](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/research.md).
- [Reproduceerbare softwarevalidatie en beperkingen](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/verification.md), [17 hosttests](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/tests/test_firmware.py) en [resultatenformulier](../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md).

Bestaande commando's en limieten behouden:2–120rpm, ±1omw perM,
PIN ±½omw,1–20cycli,30s idle/120s run, onmiddellijke `!`-verwerking met
begrensde UART-wachttijd. Ongeldige invoer schakelt nu ook uit. Onafhankelijke
specialistische controles betroffen de oorspronkelijke GPIO-uitvoering.
De UART-only-revisie is met aangepaste hosttests gecontroleerd; geen nieuwe
onafhankelijke of fysieke controle geclaimd. Positie is een tijdgebaseerde planning.

**Niet fysiek getest:** upload/interpretatie op de Pico, echte UART, fasepiek,
Vref/VM/PD/supervisortiming, reset/herstel, motorwarmte, staphoek, koppel,
slag/herhaalbaarheid en werkelijke snelheid. CPython-bytecompilatie en mocks zijn
geen Pico-runtime- of hardwarekwalificatie. De bestaande Uno-implementatie blijft
als historisch alternatief behouden.

**Stopconditie:** één aanbevolen bedrade opstelling, volledige software,
schema/handleiding en zonder hardware uitvoerbare validatie geleverd. Vrijgave
voor inschakelen vereist de expliciete PCB- en spanningscontroles; geen nieuwe
mechanische proef of volledige displayarchitectuur onderzocht.
