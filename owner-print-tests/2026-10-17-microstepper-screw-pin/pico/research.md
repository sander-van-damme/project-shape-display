# E-301 — voedingskeuze en broncontrole

17 oktober2026. Dit is datasheetonderzoek plus berekening, zonder hardwaremetingen.
Repositorybasis `8cc371d` was schoon; E-301 kwam niet voor. Bestaande Uno-code,
CAD, STL,3MF, houder en schroefgeometrie blijven behouden.

## Keuze: PD9V, stroomgeregelde TMC2208

| Optie | Beoordeling |
|---|---|
| 5V | IC kan in een passend5V-only-circuit werken. Dat bewijst niet dat deze onbekende V1.2-module op5V betrouwbaar werkt. Standaardcircuit heeft circa5,2V nodig; FYSETC noemt5,5V moduleminimum. PD-kabelverlies en SS14 verlagen VM verder. Aanpassing/bypass van5VOUT vraagt exact PCB-ontwerp en beperkt spanningsbereik. Hier afwijzen. |
| **9V** | Beschikbaar PD-profiel; ruim boven regelaarminimum, onder drivermaximum. Chopper beperkt de fasestroom; winding krijgt geen permanente9V gelijkspanning. Beste combinatie van marge en eenvoud. |
| 6V extra regelaar | Met diode dicht bij moduleondergrens; extra converter, aansluitingen en verlies zonder aangetoonde winst. Niet nodig. |

De hogere VM helpt de stroom opbouwen tegen inductie/tegen-EMK; motorinductie,
koppel en werkelijke haalbare snelheid zijn onbekend. Bij40Ω is de ohmse
faseval op77mApiek circa3,1V. Zonder stroomregeling zou9V/40Ω ongeveer225mA
betekenen: daarom nooit motor rechtstreeks op PD aansluiten. Voedingsampères,
Vref en registerwaarden zijn verschillende grootheden.

Bronnen: [ADI TMC2208 datasheet rev1.13 §3.3, §9–9.1, §18](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf)
en [FYSETC modulehandleiding, Technical Specifications en Versions Difference](https://fysetc.github.io/TMC2208/).
De chipdatasheet is leidend voor registergedrag; de FYSETC-pagina bevat elders
algemene featureclaims die niet voor de2208 gelden (geen StallGuard/CoolStep).

## Stroominstelling

Externe shunts R110: `Rs=0,110Ω`; UART `I_scale_analog=1`, `internal_Rsense=0`,
SpreadCycle, `VSENSE=1`, `IRUN=IHOLD=5`,8microstappen, geen interpolatie,
`TPOWERDOWN=0`, `TPWMTHRS=0`. Vref-trimmer blijft meebepalen.
`VACTUAL` is nul bij stop en signed nonzero tijdens beweging; TOFF is0 bij
stop/ARM en4 tijdens beweging.

`Ipk=(CS+1)/32 ×0,180/(Rs+0,030) ×Vref/2,5`;
`Irms=Ipk/√2`. BijVref0,80V:77,14mApiek/54,55mARMS. Ideale totale
koperwarmte voor beide sinusfasen: `40×Ipk²≈0,238W`; geen temperatuurvoorspelling.
Toleranties en lage digitale schaalfactor beperken de nauwkeurigheid. De
chipaanbeveling van een hogere CS voor nauwkeurige microstappen past niet goed
bij deze miniatuurmotor/R110-combinatie. Shunts vervangen heeft voor deze kleine
proef geen aangetoonde meerwaarde. Een lage stroom is geen bewezen veilige
continue motorbelasting zolang passende motorspecificaties ontbreken.

Voor deze aanbevolen proef blijft Vref0,80V vast; de optionele hogere Vref uit
de historische Uno-handleiding geldt hier niet. Begin kort en onbelast, registreer
warmte. De afwijkende PM08-PDF is geen sluitende motoridentificatie, zoals
[de bestaande bronanalyse](../sources.md) al vastlegt. Ook20stappen/omw is voorlopig.

`IHOLD_IRUN`, `TPOWERDOWN`, `TPWMTHRS`, `VACTUAL` zijn write-only. Firmware claimt
daarom geen register-readback van de stroom: ze controleert voor **iedere write**
IFCNT+1 inclusief wrap, CRC/echo op antwoorden en volledige GCONF/CHOPCONF-readback.
GSTAT en DRV_STATUS bewaken reset/onderspanning/short/temperatuur. Dit verifieert
communicatie en configuratie; geen gemeten windingstroom of fysieke beweging.
OTP wordt nooit geprogrammeerd.

## Printvarianten en logica

De officiële FYSETC-bron noemt V1.2 UART en tevens een te sluiten PDN-jumper.
Dat is onvoldoende om een ongeïdentificeerde witte clone aan die exacte
headerposities te koppelen. De aansluiting wordt als benoemde netten geleverd;
exacte fysieke mapping, shunts en brug zijn verplichte eigenaarcontroles.
PD-DIP-standen zijn eveneens onbekend; meet de gekozen9V vóór aansluiting.

TMC VIO=3,3V past rechtstreeks op Pico GPIO en UART. Een bidirectionele
3,3/5V-levelshifter is overbodig en voegt onderdelen toe. De Pico levert geen
motorstroom en krijgt zelf computer-USB. De1k in TX voorkomt buscontentie.

## Herstel van motorvoeding

De bestaande voedingsbewaking blijft behouden; er is geen nieuwe
veiligheidsarchitectuur toegevoegd. Driverreset kan standaardregisters herstellen. De gekozen TPS3808G01 gebruikt
VM-spanningsdeler162k/10k en reset de Pico hardwarematig via RUN. Berekening:
`0,405×(162+10)/10=6,966V`; met weerstanden1% en chipdrempel±2% grofweg6,69–7,25V,
plus hysterese bij stijgende VM. CT open geeft12–28ms hersteldelay.
In de UART-only-revisie zijn de EN-pullup en STEP-pulldown verwijderd op
expliciet verzoek van de eigenaar. Herstel wist de vluchtige firmwarestatus;
de firmware probeert OFF via UART. Dit blokkeert de driver niet rechtstreeks
tijdens een Pico-reset. De zwevende EN kan niet door software worden overruled.

[TI TPS3808 datasheet §5–7](https://www.ti.com/lit/ds/symlink/tps3808.pdf)
geeft typische20µs detectie; er is geen hier bewezen vanggarantie voor elke
willekeurig korte transient. De lokale100µF ondersteunt normale voedingsuitval:
bij aangenomen0,1A daalt VM circa1V/ms. Dat is een illustratieve berekening,
geen gemeten maximumverbruik. Werking/brownout-herstel moet fysiek worden getest.

Pico pinout/RUN: [officiële Raspberry Pi documentatie, wireless board layout](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#wireless-board-layout).
Interpreter/API: [MicroPython v1.26.1 Pico W UF2](https://micropython.org/download/RPI_PICO_W/),
[RP2 API](https://docs.micropython.org/en/v1.26.0/rp2/quickref.html),
[UART](https://docs.micropython.org/en/v1.26.0/library/machine.UART.html).
MicroPython is gekozen voor eenvoudige USB-installatie en kleine, inspecteerbare
firmware. De interne UART-generator draait door tijdens healthchecks;
stoplatentie en oscillatorafwijking beïnvloeden de tijdgebaseerde afstand.

## UART-only-beweging — actuele revisie

Gecontroleerd in [de TMC2208 datasheet rev1.13, §5.2 en §12](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf):
`f_micro = VACTUAL × fCLK / 2^24`, `rpm = f_micro ×60/(USC×FULL_STEPS)`.
USC is de ingestelde microstapresolutie, hier8; niet stilzwijgend256 aannemen.
Met nominaal12MHz is één VACTUAL-eenheid0,7152557373 microstappen/s.
De dichtstbijzijnde gehele snelheidswaarde bepaalt de duur:
`t = abs(geplande_microstappen)/(abs(VACTUAL)×fCLK/2^24)`.

VACTUAL(0x22) is signed24-bit two's complement in de laagste24bits van de
UART-data: +447=`0x000001BF`, −447=`0x00FFFE41`. De bovenste8bits zijn nul.
Richting komt uit het teken; geen DIR-GPIO. Geen ramp in deze eenvoudige
revisie. Voor ieder segment wordt nonzero VACTUAL geschreven terwijl TOFF0 is,
dan TOFF4. Bij einde/stop eerst TOFF0, daarna VACTUAL0. Zo wordt de zwevende
STEP-ingang niet relevant terwijl de uitgangen bewust ingeschakeld staan.

De tijd start bij het versturen van de TOFF4-write, niet pas na IFCNT-bevestiging.
Dit blijft een benadering van het chip-ontvangstmoment; geen encoderpositie.
De softwarepositie wordt pas na een voltooid en gestopt segment bijgewerkt.
Bij afbreken vervalt de nul. Tijdens beweging controleert health de verwachte
TOFF4-configuratie, na stoppen TOFF0; IFCNT volgt ook runtimewrites. VACTUAL
blijft write-only: geen verzonnen readback. Bij communicatieverlies worden beide
stopwrites zonder voorafgaande reads geprobeerd; volledige UART-uitval kan
niet door software worden opgelost.
