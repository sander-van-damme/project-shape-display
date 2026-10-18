# TMC2208: instellingen en interpretatie

Bron: [officiële ADI/Trinamic datasheet, revisie 1.13, 25 mei 2022](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf),
§4–5 (UART/registers), §6–9 (chopper/stroom), §12 (VACTUAL),
§13 (diagnostiek), §15/17 (klok/elektrische grenzen).

`main.py` bevat de volledige registerimplementatie, validatie, profielen en
`CONFIG_SCHEMA`. De GUI gebruikt dezelfde instellingen via `configure`.
Configuratie wijzigen kan alleen stilstaand. Een ongeldige invoer wordt
afgewezen voordat registers of bestaande configuratie veranderen.

## Beginprofielen

- `e301_conservative`: werkende historische uitgangsinstellingen behouden:
  SpreadCycle, 8 microstappen, `VSENSE=1`, `IRUN=IHOLD=5`, externe R110,
  handmatig geregistreerde Vref 0,80 V, `TOFF=4`, `HSTRT=5`, `HEND=0`, `TBL=1`.
- `stealthchop_low_current`: dezelfde lage stroom, StealthChop2 met automatische
  PWM-regeling/afregeling, interpolatie, `TPOWERDOWN=20`, `IHOLDDELAY=4`.
  Firmware voorziet vóór bewegen een stilstaande initialisatie van 150 ms.
  Dit is een uitvoerbaar startprofiel; goede afregeling bij deze kleine stroom
  moet nog fysiek blijken. De datasheet waarschuwt voor de ondergrens van de
  stroommeting bij StealthChop (§6.3). `PWM_AUTO/PWM_SCALE` zijn zichtbaar.
- `spreadcycle_16_microsteps`: dezelfde conservatieve stroom, 16 microstappen.

De eerdere fysieke proef valideert alleen de historische configuratie en
geobserveerde pinbeweging, niet deze nieuwe firmware/profielen of een maximumsnelheid.

## Beschikbare parameters

Namen zijn de exacte JSON-configuratiesleutels. Getallen voor bitvelden zijn
**registercodes**, tenzij anders vermeld. De defaults staan in de firmware en
worden door `hello` aan de desktop doorgegeven.

| Instelling | Waarden / betekenis |
|---|---|
| `full_steps_per_rev` | Positief geheel getal; standaard **20 is een aanname**, fysiek controleren. |
| `microsteps` | 1, 2, 4, 8, 16, 32, 64, 128, 256. MRES-codes 8…0; selectie via register, niet MS1/MS2. |
| `clock_hz` | Veronderstelde TMC-klok, standaard 12 MHz; datasheet externe klok 4…18 MHz. Dit wijzigt geen fysieke klok. |
| `calibration_factor` | Positieve correctiefactor voor berekende snelheid/omwentelingen; standaard 1. |
| `chopper`, `shaft` | `spreadcycle` / `stealthchop`; `shaft` keert de fysieke richting om. |
| `irun`, `ihold` | 0…31: stroomfactor `(code+1)/32`. Nul is normaal **1/32**, geen uitschakeling. |
| `iholddelay` | 0…15; 0 onmiddellijk, anders `code × 2^18 / fCLK` seconde per afbouwstap. |
| `tpowerdown` | 0…255; vertraging na standstildetectie `code × 2^18 / fCLK`; minimaal 2 bij automatische StealthChop-regeling. |
| `hold_on_stop` | `false`: na normale beweging uitgangen uit. `true`: normaal stoppen houdt uitgangen aan zodat IHOLD/afbouw werken. Noodstop/fout/heartbeatverlies schakelt altijd uit. |
| `i_scale_analog` | `true`: Vref schaalt stroom; `false`: interne spanningsreferentie, Vref-trimmer bepaalt de stroom dan niet. |
| `vsense` | 0: nominale sense-drempel 325 mV; 1: 180 mV. |
| `vref_v` | Handmatig gemeten/geregistreerde Vref in volt; geen meting of wijziging via UART. De registratie wijzigt alleen de berekening. |
| `rsense_ohm` | Veronderstelde externe shuntweerstand in ohm; standaard 0,11 voor R110. |
| `toff` | 1…15 tijdens ingeschakelde uitgang; uitzetten schrijft 0. TOFF=1 vereist TBL≥2. Off-time `24+32×TOFF` klokcycli. |
| `hstrt`, `hend` | HSTRT 0…7 betekent +1…+8; HEND 0…15 betekent −3…+12. Som van **effectieve** waarden maximaal 16. |
| `tbl` | 0…3: comparatorblanking 16, 24, 32, 40 klokcycli. |
| `intpol` | Interpolatie naar 256; verandert het aantal ingestelde microstappen per interne stap niet. |
| `multistep_filt` | Datasheet STEP-filter; behouden standaardinstelling. Geen dubbele STEP-flanken ingesteld. |
| `tpwmthrs` | 0…1048575; 0 schakelt snelheidsafhankelijke modusovergang uit. Boven drempelsnelheid schakelt StealthChop naar SpreadCycle; §5.2 geeft hysterese. |
| `pwm_ofs`, `pwm_grad` | 0…255; vaste/initiële PWM-offset en snelheidsgradiënt. |
| `pwm_freq` | 0…3: PWM-frequentie `2*fCLK/{1024,683,512,410}`. |
| `pwm_autoscale` | Automatische stroomregeling. Uit: IRUN/IHOLD schalen slechts PWM, de berekende stroom wordt niet afgedwongen. |
| `pwm_autograd` | Automatische gradiëntafregeling; vereist `pwm_autoscale=true` en initialisatie bij stilstand. |
| `pwm_reg`, `pwm_lim` | REG 1…15: regeltempo; LIM 0…15: limiet van PWM-offset bij terugkeer naar StealthChop. |
| `freewheel` | 0 normaal; 1 vrijloop; 2 beide lage MOSFETs kortsluiten; 3 beide hoge MOSFETs kortsluiten. Alleen StealthChop met IHOLD=0, na afbouw. |
| `senddelay` | 0…15, gecodeerde antwoordvertraging: `8 × (1 + 2×floor(code/2))` bittijden. Default 0. |

Externe shunts blijven geselecteerd (`internal_Rsense=0`), passend bij de
bestaande R110-module. De interne-sensevariant vereist een andere Vref-
stroomreferentiebedrading (§10) en is geen uitwisselbaar softwareprofiel.
OTP-programmering, testmodus en het uitschakelen van kortsluitbeveiligingen
worden niet blootgesteld. GCONF `pdn_disable` en `mstep_reg_select` staan aan.

## Snelheid, stroom en kalibratie zijn berekeningen

Volgens §12 telt VACTUAL stappen op de **gekozen** resolutie:

```text
microstappen/s = VACTUAL × fCLK / 2^24
RPM_berekend = microstappen/s × 60 / (microsteps × full_steps_per_rev)
               × calibration_factor
```

`VACTUAL` is signed 24-bit two's complement: −8388608…8388607;
negatieve waarden worden als de lage 24 bits geschreven. Nul keert terug naar
STEP-besturing; daarom moet STEP fysiek vast laag zijn. Alleen de registergrens
begrenst de softwareconversie; er is geen 120-RPM-limiet. Afronding gebeurt naar
de dichtstbijzijnde registerwaarde. De laagste niet-nulsnelheid is de waarde bij
`abs(VACTUAL)=1`; een bewegingsdoel dat nul afrondt wordt afgewezen.
Het representabele bereik bewijst geen haalbaar motortoerental: stroomregeling,
elektrische sequencertiming, mechanica en stappenverlies blijven fysieke grenzen.

TSTEP/TPWMTHRS gebruiken juist de **256-microstapreferentie**, onafhankelijk van MRES:
`TSTEP = 2^24 / (abs(VACTUAL) × 256/microsteps)`.
De snelheid gebruikt de aangenomen oscillatorfrequentie; de interne klok is
nominaal 12 MHz, geen gemeten tijdreferentie aan deze driver.

Theoretische sinusvormige fasestroom (§9/9.1):

```text
analoge_factor = min(Vref / 2,5 V, 1) bij i_scale_analog=true, anders 1
I_piek = (CS+1)/32 × V_FS/(R_sense+0,030 ohm) × analoge_factor
I_RMS = I_piek / sqrt(2)
V_FS = 0,180 V bij vsense=1, anders 0,325 V
CS = IRUN of IHOLD
```

Bij de defaults volgt **77,14 mA piek / 54,55 mA RMS per fase**, theoretisch.
Bij vrijloop/passief remmen vervangt het standstillgedrag de normale IHOLD-
stroomregeling. Analoge Vref schaalt boven 2,5 V niet verder; dit is geen
toestemming om de elektrische pinlimieten te overschrijden. Laag IRUN en lage
Vref verminderen de precisie van microstappen/stroomregeling; ze blijven hier
bewust het startpunt. De GUI vermeldt deze waarschuwingen zonder een verborgen
snelheidslimiet.

Kalibratie gebruikt handmatig getelde omwentelingen of gemeten verplaatsing en
expliciet ingestelde spoed. De nieuwe factor is
`oude_factor × gemeten_omwentelingen / berekende_omwentelingen`.
Dit corrigeert een schaalafwijking; het detecteert geen slip, stall of gemiste
stappen en maakt de positie niet gemeten. Vref, VM, belasting en motortemperatuur
blijven apart geregistreerde handmatige/instrumentele waarnemingen.

## Diagnostiek en UART-bevestiging

Identificatie vereist `IOIN.VERSION=0x20` en `SEL_A=1` (TMC220x-familie).
Configuratiewrites krijgen een afzonderlijke IFCNT-bevestiging; leesbare
GCONF/CHOPCONF/PWMCONF krijgen ook readback. VACTUAL, IHOLD_IRUN, TPOWERDOWN,
TPWMTHRS en SLAVECONF zijn **write-only** en worden nooit als gelezen waarden
voorgesteld. Snelle VACTUAL-writes tellen een verwachte IFCNT op; periodieke
gezondheidscontrole detecteert een verloren write via de modulo-256-teller.
De periodieke compacte controle leest zeven registers en markeert `compact=true`;
TSTEP, MSCNT en PWM-afregelwaarden ontbreken dan expliciet. Een volledige
diagnose bij stilstand leest elf registers en vult deze waarden opnieuw aan.
Ongeldige CRC, antwoordheader, timeout en writebevestiging worden fouten.

De status toont GSTAT reset/driverfout/charge-pump-onderspanning, DRV_STATUS
kortsluiting, temperatuurwaarschuwing/-uitschakeling, comparatorvlaggen,
open-loadvlaggen, modus en stroomcode. Temperatuurvlaggen betreffen de **driverchip**,
niet een gemeten motor- of chiptemperatuur. Open-load is bij lage stroom,
stilstand of hoge snelheid onbetrouwbaar; de vlag blijft informatief.
MSCNT is alleen een modulo-1024 elektrische sequencerstand, geen mechanische
positie. PWM-regelwaarden zijn geen koppel-, belasting- of stallmeting.

StallGuard en CoolStep ontbreken in de TMC2208. Voor deze proef is het alternatief
handmatig waarnemen/meten; er wordt geen encoder of automatische homing toegevoegd.

De TMC2208 heeft volgens §4 **vast slave-adres 0**; MS1/MS2 geven geen unieke
UART-adressen zoals bij andere TMC-types. Meerdere controllers gebruiken daarom
aparte communicatiekanalen. Een gedeelde draad kan ze niet onafhankelijk
aanspreken. De software controleert de meermotorlogica met mocks; gelijktijdige
fysieke werking is niet aangetoond.
