# E-301 — verificatie van de UART-only-revisie

17 oktober 2026. Deze revisie voert de vastgelegde eigenaarskeuze uit:
STEP/DIR/EN volledig los, uitsluitend UART-besturing. De eerdere GPIO-review
betrof de oorspronkelijke uitvoering en geldt niet als review van deze revisie.
Er zijn geen fysieke meetresultaten toegevoegd.

## Uitgevoerd

Vanuit repositoryroot:

```sh
python3 -m py_compile owner-print-tests/2026-10-17-microstepper-screw-pin/pico/*.py
python3 -m unittest discover -s owner-print-tests/2026-10-17-microstepper-screw-pin/pico/tests -v
./repo check
```

**CPython-bytecompilatie geslaagd; 17 hosttests geslaagd.** De tests voeren de
geleverde UART-driver, controller en bewegingspolicy uit met vervangen UART,
klok en, voor de opstarttest, machine-module:

- Vaste CRC-vectoren, onjuiste CRC/chip-ID/SEL_A en UART-timeout.
- Lage stroominstelling ongewijzigd: R110/Vref0,80/VSENSE1/IRUN=IHOLD5;
  configuratie met TOFF0, alle writes IFCNT-bevestigd inclusief tellerwrap.
  Iedere configuratieregisterwrite afzonderlijk laten wegvallen: geen ARM.
- VACTUAL +447=`0x000001BF`, −447=`0x00FFFE41`; 120rpm geeft nominaal
  0,500439s per omwenteling bij20 hele stappen en8 microstappen. Afgeronde
  snelheid bepaalt de duur; bij2rpm waarde7 en31,956602s. Grenzen signed24-bit.
- Startvolgorde nonzero VACTUAL met uitgeschakelde brug → TOFF4. Stopvolgorde
  TOFF0 → VACTUAL0; TOFF-readback en eigen IFCNT-bevestiging van VACTUAL0.
  Write-only registers worden niet teruggelezen; geen OTP-writes.
- Healthchecks accepteren bewust wisselende TOFF4/TOFF0 en runtime-IFCNT;
  onverwachte configuratie/reset/teller/foutstatus schakelt de software uit.
- Vooruit/achteruit, tien cycli, nul/NaN/Inf, invoer-/afstands-/snelheidsgrenzen,
  overvolle regels, `!`, gefragmenteerde `OFF` tijdens beweging en geen wachtrij.
- Alle51.681 combinaties van161 softwareposities en321 afstanden rond de
  PIN-limiet; alleen de geplande afstand wordt begrensd, geen fysieke positie.
- 30s idle en120s totale run. Iedere stop maakt bij OFF/fout de nul ongeldig;
  normaal segmenteinde behoudt de geplande nul voor C-cycli.
- RX-verlies tijdens beweging: TX verstuurt alsnog TOFF0 en VACTUAL0, ook zonder
  bevestiging; melding `UART STOP UNCONFIRMED`. Volledig UART-verlies: test
  bevestigt juist dat de software geen fysieke stop kan garanderen.
- `main.py` initialiseert uitsluitend GP4 en GP5. Opstart en KeyboardInterrupt
  proberen dezelfde UART-stop; geen toegang tot GP2/GP3/GP6. Geen hervatte opdracht
  na herinitialisatie van de Controller.

[validation.json](validation.json) bevat het actuele testresultaat en de behouden
mechanische hashes. De bestaande mechanische bestanden en Uno-code zijn voor
deze wijziging niet aangepast. Het bijgewerkte SVG is opnieuw gegenereerd en
visueel gecontroleerd. Geen nieuwe hardwarearchitectuur of experiment toegevoegd.

`./repo check` meldt de bestaande omvangsmeldingen voor E-266,E-283,E-286,
E-288,E-293 en de twee bestaande AGENTS-bestanden. Geen nieuwe structuurmelding.

## Grenzen van deze validatie

Dit is uitvoering met mocks op CPython, geen RP2040/MicroPython-runtimecontrole.
Geen fysieke UART-transmissie, oscillatorfrequentie, aspositie, motorwarmte,
stroom of herhaalbaarheid gemeten. VACTUAL is tijdgebaseerd: oscillatorafwijking,
UART-latentie, uitlijnbewegingen en niet-vastgehouden pauzes kunnen afstand en
retourpositie veranderen. Er is geen encoder of terugmelding van echte beweging.
De eenvoudige beweging heeft constante snelheid, zonder de vroegere STEP-ramp.

De software kan de zwevende fysieke EN-ingang niet overrulen. Bij volledig
UART-verlies, opstart of reset is geen fysieke stopgarantie mogelijk.
`STOP UNCONFIRMED` is geen succesvolle hardwarestop. Deze beperkingen horen bij
de door de eigenaar vastgelegde aansluiting; geen workaround toegevoegd.
