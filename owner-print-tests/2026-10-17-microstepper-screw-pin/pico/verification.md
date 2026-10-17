# E-301 — verificatie en beperkingen

17 oktober2026, basiscommit `8cc371d`. De werkboom was aan het begin schoon;
E-301 was ongebruikt. Dit pakket bevat geen nieuwe fysieke resultaten.

## Uitgevoerd

Vanuit repositoryroot:

```sh
python3 -m py_compile owner-print-tests/2026-10-17-microstepper-screw-pin/pico/*.py
python3 -m unittest discover -s owner-print-tests/2026-10-17-microstepper-screw-pin/pico/tests -v
./repo check
```

**CPython-bytecompilatie geslaagd;14hosttests geslaagd.** De tests voeren de
echte geleverde driver/controller/policy uit met vervangen UART, GPIO en klok:

- CRC vergeleken met vaste protocolvectoren; verkeerde CRC, chip-ID, SEL_A en
  uitblijvend antwoord weigeren ARM.
- Iedere van de zeven configuratiewrites apart laten wegvallen: geen ARM of
  STEP. IFCNT-wrap254→5 correct. Write-only registers niet teruggelezen;
  OTP_PROG nooit aangeroepen.
- Alle51.681combinaties van161PIN-posities en321afstanden rond de gehele
  softwaregrens gecontroleerd; geen toegestane overschrijding.
- Tien volledige cycli keren naar nul terug met3200pulsen; beide richtingen.
- Nul/NaN/Inf/te grote beweging, ongeldige snelheid/cycli, overloop van de
  commandoregel en meerdere regels rond een stop blijven uitgeschakeld.
- `!` tijdens beweging,30s idle,120s totale beweging en UART-fout tijdens beweging
  stoppen met EN hoog en STEP laag. Reset/configuratie/IFCNT/temperatuur/short/CRC
  tijdens gewapende idle schakelen eveneens uit; geen automatische herarming.
- `main.py` gestart met vervangen hardwaremodules; een geïnjecteerde
  KeyboardInterrupt bij actieve uitgangen voert `finally: app.off()` uit.
- Nieuwe Controller na gemodelleerde harde reset start OFF; oude beweging vervalt.
  Dit model bewijst niet de analoge detectietijd van de supervisor.

[validation.json](validation.json) legt de mechanische-bestandschecks vast:
alle bestaande STL/3MF/SCAD, de mechanische generator, tekeningsgenerator en
layout zijn byte-identiek aan HEAD. Ook de oorspronkelijke Uno-controller en
bewegingspolicy zijn niet aangepast. Geen CAD/slicer opnieuw uitgevoerd.
De SVG is gegenereerd, naar PNG gerenderd en visueel gecontroleerd.

`./repo check` meldt uitsluitend reeds bestaande omvangsmeldingen voor E-266,
E-283,E-286,E-288,E-293 en de twee bestaande AGENTS-bestanden. De nieuwe E-301
veroorzaakt geen nieuwe structuur-/referentiemelding. Niet de hele check als
succes gerapporteerd; bestaande documenten niet voor deze taak herschreven.

## Onafhankelijke controles

Op verzoekruimte van de eigenaar twee afgebakende specialistische controles:

1. Elektrisch:9V-keuze,5V-modulebeperking, stroomformule,3,3V-logica,
   supervisorpinout en herstelveiligheid gecontroleerd. Advies verwerkt:
   TPS3808G01DBVR→RUN voorkomt hervatting na gedetecteerde voedingsuitval met
   minder onderdelen dan een aparte latch. Typische detectietijd is geen
   universele garantie voor elke ultrakorte transient.
2. Firmware: CRC/echo/IFCNT/readback/foutmaskers, limieten, ENABLE en GPIO-mapping
   gecontroleerd. Geen concrete blokkerende firmwarefout gevonden. Aanbevelingen
   verwerkt:115200baud, één commando per keer,120s kan C vroeg afbreken,
   werkelijke snelheid afzonderlijk meten wegens ramp/UART-overhead.

## Niet uitgevoerd / vrijgave vóór fysiek gebruik

Geen aangesloten Pico/driver/motor/PD-bord. Geen target-upload, MicroPython-
interpretatie op RP2040, fysieke UART/STEP-timing, gemeten fasepiek of warmte,
bewezen draairichting/staphoek, belastbaarheid, pinverplaatsing of herhaalbaarheid.
Er was geen MicroPython-targetcompiler geïnstalleerd; een poging de vastgezette
mpy-cross1.26.1 te verkrijgen gaf geen beschikbare distributie. Ook directe
PDF-download via de shellproxy was niet beschikbaar; brononderzoek liep via
de webtool. De toepassing wordt als `.py` op de officiële Pico W-interpreter
geïnstalleerd. CPython-compilatie vervangt die fysieke runtimecontrole niet.

De concrete V1.2-pinmapping, tweeR110, bereikbaarheid PDN_UART/soldeerbrug,
PD-DIP-keuze,9V-profiel, Vref, spoelparen en supervisor-reset/herstel zijn
**verplichte controles vóór inschakelen of belasten**, uitgewerkt in de
[handleiding](handleiding.md). Gebruik bij twijfel iemand die de exacte print
kan identificeren/nameten; geen generieke headerposities gokken. Een succesvolle
benchproef bewijst alleen deze motor/pin/stroom/snelheid/last, geen volledige
Shape Display en geen40mm-slag.
