# Softwarevalidatie E-302

18 oktober 2026. Basis: nieuwste `main` op commit `c1a8a0d` (tijdens het werk bijgewerkt vanaf `505bb91`). Er zijn geen nieuwe
fysieke motor-, Pico- of printtests uitgevoerd. Het eerdere positieve
E-301-eigenaarsverslag blijft historische fysieke evidentie, geen validatie van
de nieuwe PIO-interface of bewegingsprofielen.

## Reproduceerbare controles

Vanuit deze `software/`-map:

```sh
python -m unittest discover -s tests -v
python tests/micropython_smoke.py
python -m desktop.cli --simulate --export demo.json demo
python -m desktop.cli --simulate --export sweep.json run desktop/example_steps.json
python -m desktop.app --simulate
```

De tests vereisen geen Pico, pyserial-installatie of GUI-display. De laatste
opdracht opent de GUI; voor echte USB is `requirements.txt` nodig.

| Onderdeel | Wat werkelijk is gecontroleerd |
|---|---|
| UART/PIO | CRC-vectoren, corrupte bits, exacte echo, ontbrekende/truncated antwoorden, time-outs, trailing bytes, herstel; uitvoering van de echte PIO-bron in een instructiecyclusmodel met TX/RX-FIFO's, stopbits en GPIO-richting |
| PIO-assembler | De officiële MicroPython v1.26.1 `rp2.asm_pio` assembleert 22 geldige instructies; ±2% antwoordbitduur in het model |
| TMC2208 | Profielen/registergrenzen, getekende 24-bit codering, alle microstepstanden, IFCNT-wrap/verloren writes, CRC/headerfouten, reset/driverfouten, stopwrites ondanks verloren RX, theoretische stroom en float32-eindwaarden |
| Planner | Sample-held integratie, trapezium/driehoek, laagste/hoogste representabele VACTUAL, kleine acceleratie, tijd/afstand, deceleratie, geschreven nul vóór omkeren, cycli, dwells en expliciete grenzen |
| Integratie | JSON-framing en ongeldige opdrachten zonder configuratieverlies; heartbeat/foutlatch/herstel zonder herstart; reference/bounds; holding/warmup; twee onafhankelijke motoren; UART-latentie en gespreide healthchecks |
| Desktop/CLI | Profiel/meetgegevens/CSV/JSON, fail-fast sweeps, geen vervolgstap na onvolledige pinbeweging, heartbeat, reconnect zonder oude opdrachten, STOP-prioriteit en lazy RPM-bereiken |
| Tkinter | Echte GUI op een tijdelijke Linux Xorg-display gestart: alle zes tabs, basisconfiguratie/JSON, kalibratie, bewegen/omkeren/STOP en vergelijking van beide choppermodi; geen callbackfouten |
| MicroPython | Officieel v1.26.1 `mpy-cross`, import en runtime-smoke op unix standaard en een float32-build, inclusief lange-uptijdklok en signed-registergrenzen |

105 unit-/integratietests slagen. De actuele testtelling en firmwarehash staan in [validation.json](validation.json).
De smoke gebruikt echte firmwarefuncties en registermocks; geen nagemaakte
planner of fictieve sensorsamples.

## Interpreter en timing

MicroPython bron: officiële tag `v1.26.1`, commit
`647c8b96cae7e202c7a020395b7cfe65e5b8ce04`.
De unix-interpreter is voor deze controle lokaal gebouwd zonder ongebruikte
btree/SSL/FFI. De tweede build gebruikt `MICROPY_FLOAT_IMPL_FLOAT`, net als de
RP2040. `mpy-cross main.py` controleert alle broncode; het resulterende `.mpy`
is een testartefact en hoeft niet naar de Pico.

Met die interpreter vanuit `software/`:

```sh
micropython -X heapsize=512k tests/micropython_smoke.py
```

Ook een **echte 32-bit i386-build** met float32, 4-byte pointers en objectrepr A
(dezelfde representatiekeuzes als RP2040) is onder QEMU gecontroleerd. Het
ongewijzigde bronbestand importeert én de volledige runtime-smoke slaagt met
**192 KiB en 200 KiB heap**. Met 192 KiB gebruikt import na garbage collection
45.696 bytes; met drie gesimuleerde controllers 50.272 bytes. De simulator
bewaart hiervoor alleen de laatste 128 writeframes als debughistorie; UART-tellers
blijven cumulatief. Dit is een gerichte geheugen-/interpretercontrole, geen
emulatie van de RP2040-periferie of garantie van dezelfde vrije heap op een Pico.

De float32-run dekt specifiek een klokregressie: telkens 1 ms optellen bij een
float van 32768 s verloor tijd. De huidige klok bewaart integer microseconden.
Getekende VACTUAL-extremen worden zonder onjuiste float32-afronding behouden.

De hoofdloop werkt nominaal om de 20 ms, met 40 ms extra reactiereserve voor
UART-controles in de planner. Er gaat hoogstens één compacte periodieke
healthcheck door per scheduler-pass. Lange configuratie/diagnose is tijdens
beweging geweigerd; vooraf geconfigureerde motoren kunnen afzonderlijk starten.
Tests voegen 1,5 ms per read en 0,8 ms per write toe en controleren de
meermotorlogica en pinbegrenzing. Dit zijn opgelegde modeltijden, geen gemeten
RP2040-uitvoeringstijden. Werkelijke afwijkingen staan in de timingtelemetrie.

## Grenzen en eerstvolgende fysieke controle

Hosttests bewijzen geen elektrische PIO-werking, USB-CDC-latentie, werkelijk
beschikbare Pico-heap, GPIO-/EN-bedrading of fysieke motorprestatie. Er zijn geen
koppel-, fasestroom-, RPM-, positie- of motortemperatuurmetingen gegenereerd.
Windows-installatie is geleverd en statisch bekeken; de GUI is daadwerkelijk
op Linux uitgevoerd, niet op een Windowsmachine.

Kopieer alleen `main.py` naar een Pico W met MicroPython 1.26.1 en controleer
boot/import, driveridentificatie en korte onbelaste beweging. Test vervolgens
STOP/heartbeat, PIO versus de bestaande tweepins-UART en pas daarna een pin
met eigen slaggrenzen. [Exacte volgorde en schema](WIRING.md).

De repositorystructuurcheck heeft op de oorspronkelijke basis al zeven meldingen:
oversized E-266/E-283/E-286/E-288/E-293 en beide bestaande AGENTS.md-bestanden.
De uiteindelijke levering is afzonderlijk van build-scratch gecontroleerd;
deze bestaande meldingen worden niet via ongevraagde historische wijzigingen
opgelost. E-302-CAD/STL/3MF en alle E-301-resultaten zijn ongewijzigd.
