# Elektronica en firmware — huidige testbasis

[Terug naar DES-009](DES-009-traveling-motor-bank-screw-pins.md).

**Pico W en TMC2208 vormen een fysiek bruikbare testbasis, geen definitieve
keuze voor alle elektronica van de motorbank.** Op 18 oktober 2026 bewoog
één compacte schroefpin omhoog en omlaag met de E-301-firmware. Het latere
E-302-softwarepakket is uitgebreider, maar nog niet fysiek gevalideerd.
Geen van beide bewijst een complete motorbank of parallelle pinbeweging.

## Werkelijk uitgevoerde proef versus nieuwste software

| Onderdeel | E-301: fysieke eigenaarproef, 18 oktober | E-302: nieuw softwarepakket, nog geen fysieke proef |
|---|---|---|
| Controller | Raspberry Pi Pico W, MicroPython, USB/PuTTY | Pico W; zelfstandige `main.py`, desktop-GUI/CLI en logbestanden |
| Driver | Witte Silent2208/TMC2208 V1.2-module; exacte fabrikant/PCB niet onafhankelijk vastgesteld | Dezelfde testbasis; modulemapping en shunts blijven te controleren |
| Voeding | VM circa 9 V gemeten; VIO eerst 0,09 V, na kabelcorrectie 3,3 V | USB voor Pico; bestaande circa 9 V voor VM; VIO 3,3 V |
| UART | GP4 TX via 1 kΩ, GP5 RX direct naar dezelfde UART-node; UART-selectie gesoldeerd | Standaard GP4 via 1 kΩ als één-GPIO PIO-UART, bus-pull-up 10 kΩ; tweepins hardware-UART als fallback |
| EN/ENN | Losse EN gemeten 3,24 V blokkeerde beweging. **EN aan GND** maakte beweging mogelijk | **GP6 plus 10 kΩ naar VIO**: hoog tijdens opstart/configuratie, laag na succesvolle configuratie |
| STEP/DIR | Los; eigenaar meldde kleine onbedoelde opstartbewegingen | Beide vast aan GND; dit gewijzigde gedrag nog fysiek te toetsen |
| Beweging | Via UART/VACTUAL; S100 was een instelling, geen gemeten 100 rpm | Ook VACTUAL; rampen, cycli en berekende tijdintegratie. **PIO maakt UART-signalen, geen STEP-pulsen** |
| Stroominstelling | Vref circa 0,80 V; SpreadCycle, VSENSE=1, IRUN=IHOLD=5, 8 microstappen; R110 aangenomen | Conservatief E-301-profiel plus aanvullende profielen; instellingen blijven berekeningen totdat gemeten |
| Mechanisch bewijs | Eén pin op/neer, ducttapekoppeling en handmatig uitgesneden motorzitting | CAD/slicer en softwarevalidatie; geen nieuwe fysieke passing-, motor- of pinproef |

De succesvolle E-301-bedrading wijkt af van de oorspronkelijke
[aansluitlijst](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/wiring.md),
waarin EN los blijft. **Gebruik dat historische schema niet zonder het
[fysieke resultatenverslag](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md).**
EN permanent laag kan de motor al vóór de lage UART-stroomconfiguratie
bekrachtigen. Een aanwezige module-pull-up is vermoed, niet bewezen.

De losse motor keerde na heen/terug niet naar dezelfde stand terug; de
positieafwijking stapelde op. De foutgrootte en oorzaak zijn onbekend. De
melding `DONE planned rev=1.000` bevestigt een geplande beweging, geen
werkelijke rotatie. E-302 is geen bewezen oplossing van deze retourfout. Ook 20 volle stappen
per omwenteling blijft een aanname. Snelheid, kracht, stroom, temperatuur,
volledige slag en stop-/supervisorwerking zijn niet instrumenteel gevalideerd.

## Waar staan code, schema's en resultaten?

| Bron | Functie |
|---|---|
| [E-301](../../06-experiments/E-301-pico-w-motorcontroller.md) | Overzicht en fysieke eigenaarupdate |
| [E-301-resultaten](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md) | Leidende beschrijving van werkelijk gebruikte bedrading, metingen en problemen |
| [E-301 firmware](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/main.py) | UART-driver, controller en bewegingspolicy in dezelfde map |
| [E-301 onderzoek](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/research.md) | Berekeningen en bronnen |
| [E-302 softwarehandleiding](../../owner-print-tests/2026-10-18-microstepper-frame-v2/software/handleiding.md) | Nieuwste softwarevertrekpunt, nog fysiek te toetsen |
| [E-302 bedrading en schema](../../owner-print-tests/2026-10-18-microstepper-frame-v2/software/WIRING.md) | Voorgestelde EN-/STEP-/DIR-configuratie en beide UART-varianten |
| [E-302 driver](../../owner-print-tests/2026-10-18-microstepper-frame-v2/software/DRIVER.md), [validatie](../../owner-print-tests/2026-10-18-microstepper-frame-v2/software/VALIDATION.md) | Registerdetails en grenzen van host-/PIO-tests |

E-302-validatie betreft unit-/integratiesimulatie, PIO-instructiecycli en
MicroPython op een host, inclusief float32; geen fysieke validatie.

## TMC2208: officiële referentie en relevante registers

Fabrikantbron: **TRINAMIC/Analog Devices, TMC2208/2 & TMC2224 family Datasheet,
rev. 1.13, 25 mei 2022**, [officiële PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf).
De PDF is op 18 oktober 2026 rechtstreeks gecontroleerd. Onderstaande
verwijzingen gebruiken de gedrukte paginanummers. De IC-datasheet bevestigt
geen headerindeling of fabrikant van onze specifieke witte module.

| Register | Adres; toegang | Betekenis; datasheet |
|---|---|---|
| GCONF | 0x00; R/W | Analoge stroomreferentie, shunts, SpreadCycle, richting, `pdn_disable`, `mstep_reg_select`; §5.1 p.23 |
| GSTAT | 0x01; R + write-one-to-clear | Reset, driverfout, charge-pump-onderspanning; p.24 |
| IFCNT | 0x02; R | Geaccepteerde UART-writes modulo 256; p.24. Geen fysiek bewegingsbewijs |
| IOIN | 0x06; R | Ingangsniveaus, VERSION=0x20, SEL_A=1 voor TMC220x; p.24–25 |
| IHOLD_IRUN | 0x10; W | Houd-/loopstroomcode 0…31 = 1/32…32/32; IHOLDDELAY; §5.2 p.28 |
| TPOWERDOWN | 0x11; W | Vertraging tot stroomreductie, eenheid 2^18 klokcycli; p.28 |
| TPWMTHRS | 0x13; W | StealthChop/SpreadCycle-snelheidsdrempel; p.28 |
| VACTUAL | 0x22; W | Signed 24-bit snelheid; nul keert terug naar STEP-besturing; p.28, §12 p.61 |
| CHOPCONF | 0x6C; R/W | TOFF, VSENSE, microstapresolutie, interpolatie en chopperinstellingen; §5.4.1 p.31–32 |
| DRV_STATUS | 0x6F; R | Driverfouten, temperatuurvlaggen, stroomcode, modus en open-load; §5.4.3 p.35 |
| PWMCONF | 0x70; R/W | StealthChop-PWM, autoscale/autograd en vrijloop/passief remmen; §5.4.2 p.33–34 |

W betekent alleen schrijfbaar: geen readback claimen voor bijvoorbeeld
IHOLD_IRUN of VACTUAL. IFCNT bevestigt schrijftelegrammen; leesbare registers
laten daarnaast configuratiecontrole toe. DRV_STATUS-temperatuurvlaggen
betreffen de driverchip, geen gemeten motortemperatuur. Open-load is bij lage
stroom, stilstand of hoge snelheid onbetrouwbaar (§13.3 p.63). TMC2208 heeft
geen StallGuard/CoolStep; de diagnostiek meet geen mechanische positie of koppel.

## Stroom, microsteps en toepasselijke grenzen

- **ENN hoog schakelt de uitgangen uit** (§2.2 p.9). UART kan een hoog
  elektrisch EN-niveau niet overrulen. VCC_IO is 3,00–5,25 V; bij de Pico
  gebruiken we 3,3 V. Standaard VM met interne 5V-regelaar: **5,5–36 V**
  (§18.1 p.68). De afzonderlijke 5V-onlyschakeling bewijst geen werking
  van een onbekende StepStick op 5 V.
- De berekende stroom bij externe shunts is
  `I_piek = (CS+1)/32 × V_FS/(R_sense+0,030 Ω) × min(Vref/2,5 V,1)`;
  `I_RMS = I_piek/√2` (§9–9.1 p.52–54). VSENSE=1 geeft V_FS=0,180 V.
  Met R110 aangenomen, CS=5 en Vref=0,80 V volgt **77,14 mA piek /
  54,55 mA RMS per fase**. Dit is geen gemeten stroom of bevestigde
  continue motorbelasting. IRUN=0 is normaal 1/32, geen uitstand; TOFF=0
  schakelt de uitgangen uit.
- IRUN 16…31 geeft volgens p.28 de beste microstapkwaliteit. Lage Vref,
  met name onder circa 0,5–1 V, vermindert de analoge precisie; p.54
  adviseert passende shunts en circa 2–2,4 V voor beste precisie.
  De bestaande lage-stroominstellingen blijven proefbasis met die beperking.
- StealthChop-autotuning heeft een ondergrens die afhangt van motor,
  voeding, blanking en PWM: `I_lower ≈ tBLANK × fPWM × VM/Rcoil`
  (§6.3.1 p.41). Geen universele minimale driverstroom. Een nieuw
  StealthChop-profiel is nog geen bewezen verbetering van SpreadCycle.
- Via MRES zijn fullstep tot 256 microstappen instelbaar; interpolatie
  naar 256 maakt de stroomgolf gladder, maar bewijst geen overeenkomstige
  mechanische positioneernauwkeurigheid (§5.4.1, §11).
- Bij VACTUAL geldt `f_micro = VACTUAL × fCLK / 2^24` en
  `rpm = f_micro × 60 / (microsteps × volle_stappen_per_omwenteling)`
  (§12 p.61). De interne klok is nominaal 12 MHz, niet gemeten aan onze
  driver. Gebruik de gekozen resolutie, niet automatisch 256. De
  TSTEP/TPWMTHRS-referentie is juist wel 1/256 stap.

## Consequenties voor een bank met meerdere motoren

De TMC2208 heeft **vast UART-adres 0** (§4.1 p.18, §4.4 p.21).
MS1/MS2 geven geen unieke adressen. Onafhankelijke motoren vragen meerdere
drivers met aparte communicatiekanalen of expliciete busselectie; de fabrikant
toont analoge schakelaars als mogelijkheid. Een gedeelde draad kan wel
identieke writes uitzenden, maar maakt de motoren niet onafhankelijk.
E-302 gebruikt aparte kanalen; parallelle fysieke werking is nog niet bewezen.
De keuze van kanaalindeling, timing en voeding blijft open voor DES-009.

## Overige bronnen en documentstatus

| Bron | Gebruik en status |
|---|---|
| [Pico W-datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf), [pinout](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf), [officiële boarddocumentatie](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#wireless-board-layout) | Fabrikantbronnen voor board/pinnen; ophalen gaf hier HTTP 403 op 18 oktober 2026, revisie niet opnieuw vastgesteld. Repositorybedrading verwijst al naar deze bronketen |
| [MicroPython Pico W](https://micropython.org/download/RPI_PICO_W/), [RP2 API v1.26.0](https://docs.micropython.org/en/v1.26.0/rp2/quickref.html) | Softwareprojectdocumentatie; firmware/hostvalidatie in E-301/E-302 noemt 1.26.1 |
| [TI TPS3808-datasheet](https://www.ti.com/lit/ds/symlink/tps3808.pdf) | Fabrikantbron voor bestaande E-301-supervisorberekening, §5–7; revisie hier niet opnieuw vastgesteld, fysieke supervisorwerking niet bevestigd |
| [FYSETC TMC2208-handleiding](https://fysetc.github.io/TMC2208/) | Modulevergelijking, geen bevestiging van de fabrikant of pinmapping van onze witte module |

Externe PDFs zijn niet in het dossier gedupliceerd: expliciete toestemming
voor herdistributie is bij deze consolidatie niet vastgesteld. De stabiele
bronlinks en vastgestelde documentversie blijven centraal beschikbaar.
