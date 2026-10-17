# E-301 — resultaten (nog niet uitgevoerd)

Status: [ ] niet uitgevoerd [ ] gedeeltelijk [ ] voltooid. Datum: ____

## Verplichte elektronicacontroles

- Exacte StepStick fabrikant/revisie en gebruikt PCB-schema: ____
- VM/VIO/GND/fase-uitgangen volgens dat schema bevestigd: ____
- Twee R110-opdrukken gezien: ____ ; geen nauwkeurige shuntmeting geclaimd.
- PDN_UART-brug: [ ] al doorverbonden [ ] volgens schema gesloten [ ] onbekend → STOP
- PD-trigger type en eigen DIP-stand voor9V: ____
- Adapterlabel9V-profiel: ____ ; gemeten PD-uitgang: ____ V
- VM na diode, los/belast: ____ / ____ V ; VIO: ____ V ; Vref: ____ V (doel0,80)
- TPS3808G01DBVR/adapterpinout gecontroleerd: ____ ; SENSE: ____ V
- RUN-jumper aanwezig vóór test: ____ ; STEP/DIR/EN volledig los, zonder weerstanden: ____
- MicroPython UF2-versie: ____ ; alle vier Python-bestanden geplaatst: ____
- ARM MOTOR geaccepteerd met TOFF0: ____ ; UART-fout blokkeert ARM: ____
- `!` tijdens losse motorbeweging: ____ ;30s idle: ____
- VM uit/herstel tijdens beweging: ____ ; UART-stop na boot bevestigd: ____
- Eventuele onbedoelde beweging bij opstart/reset/uitval: ____
- USB los/herstel: ____ ; UART-stop na reboot: ____
- Werkelijke fasepiek indien instrumenteel gemeten, methode/instrument: ____
  Geen meting? Schrijf **niet gemeten**; nominale berekening77mApiek/55mARMS.

Bij een mislukte controle geen pinproef. Geen hogere Vref dan0,80V in deze opstelling.

## Mechanische proef — bestaand formulier hergebruikt


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
