# E-302 lokale desktopbediening

Gebruik Python 3.8 of nieuwer met Tkinter. Windows: installeer Python van
python.org met de Tk-optie en dubbelklik `start_windows.bat`. Het script maakt
lokaal `.venv` en installeert alleen pyserial. Start zonder hardware via
`start_windows.bat --simulate`. Internet is alleen bij deze eerste installatie
nodig, nooit voor bediening of registratie.

Linux: installeer zo nodig `python3-tk` en `python3-venv` via je pakketbeheerder;
voer `./start_linux.sh` uit. Voor `/dev/ttyACM*` kan lidmaatschap van `dialout`
nodig zijn; gebruik geen root om de GUI te starten. Met bestaande omgeving:

```sh
python -m pip install -r requirements.txt
python -m desktop.app --simulate
python -m desktop.app
```

Voer commando's uit vanuit deze `software/`-map. Kopieer **alleen `main.py`** naar
de Pico; `desktop/` draait op de computer. Sluit Thonny/PuTTY voor verbinding:
slechts één programma kan dezelfde USB-poort gebruiken. Zie [bedrading en
opstartprocedure](handleiding.md) vóór een fysieke proef.

## Bediening

1. Kies COM-poort en **Verbinden**. Poorten worden elke twee seconden gezocht.
   `SIMULATIE` voert de echte firmware op Python uit met gesimuleerde registers.
   Motorselectie toont de in firmware geconfigureerde kanalen.
2. Onder **Motor / driver** wijzig je chopper, microstappen, volle stappen per
   omwenteling, IRUN, IHOLD en handmatig gemeten Vref via gewone velden.
   **Basisinstellingen toepassen** bewaart andere driverinstellingen; bij
   StealthChop wordt een te kleine TPOWERDOWN op 20 gezet voor autotuning.
   Een standaardprofiel vult de velden én de geavanceerde JSON-editor; gebruik
   **Driverconfiguratie toepassen** om dat volledige profiel toe te passen.
   **Instellingen / registergrenzen** toont het schema. De JSON-editor ondersteunt
   alle instellingen; onbekende of ongeldige waarden worden geweigerd zonder
   de vorige configuratie te vernietigen. Wijzigen kan alleen bij stilstand.
3. Onder **Beweging** kies je continu, omwentelingen, duur of op/neercycli.
   RPM met een minteken keert de richting om. Geef acceleratie/deceleratie in
   RPM/s. **Start motor** controleert en configureert de driver automatisch.
   **RPM live toepassen** en **Richting wisselen** wijzigen een continue test.
   De richtingswissel remt af tot nul voordat hij omkeert.
4. **Gecontroleerd stoppen** gebruikt de ingestelde remhelling. De rode
   **STOP · ALLE MOTOREN** en Escape stoppen direct via het afzonderlijke `!`
   protocol. STOP blijft boven alle tabbladen bereikbaar en onderbreekt een
   lopend serieel verzoek en wachtende opdrachten. Bij driver-UART-uitval kan
   deze opdracht de driver niet gegarandeerd bereiken; schakel VM fysiek uit.
5. Voor een pin kies je **Pintest** en stel je alle mechanische velden expliciet
   in: min/max, schroefspoed en handmatig bevestigde startpositie. Een pin van
   50 mm definieert geen slag. Herbevestig de referentie na verlies/fout/STOP.
6. **Diagnostiek** toont driveridentificatie, status, fouten, configuratie en
   UART-tellers. Wis een fout pas nadat de oorzaak is opgelost. Er is geen
   StallGuard, encoder, automatische homing of gemeten motortemperatuur.

Er wordt iedere 0,5 s een heartbeat verstuurd, ook in de CLI. Firmware stopt
bij het ingestelde heartbeatverlies. Opnieuw verbinden stuurt eerst STOP en
hervat nooit een beweging of sweep. Reconnect probeert de geselecteerde
poort; als Windows een ander COM-nummer toewijst, selecteer dat nieuwe nummer.
Sluiten van de app stuurt STOP. De fysieke voedingsschakelaar blijft nodig.

Bij meerdere motoren: pas iedere motorconfiguratie eerst toe terwijl alle
motoren stilstaan. Daarna kunnen voorbereide kanalen afzonderlijk tegelijk
starten. Volledige configuratie/diagnose/foutherstel tijdens beweging wordt
geweigerd zodat lange registerreeksen de bewegingsupdates niet blokkeren.

## Automatische tests en resultaten

**Automatische tests** maakt alle combinaties van RPM-bereik/stap,
acceleraties, choppermodi, microstepping en IRUN. De andere bewegingsvelden
komen uit **Beweging**. Bij `continuous` gebruikt een sweep de opgegeven duur
voor iedere stap. Er is geen vaste tijds-/cycluslimiet. De reeks stopt bij de
**eerste fout** en gaat niet door naar een volgende instelling. Het
voorbeeldbestand `desktop/example_steps.json` laat expliciete stappen zien;
zo kun je ook IHOLD, PWM-parameters en deceleratieprofielen vergelijken.

Alle handmatige en automatische bewegingen worden geregistreerd onder
**Resultaten**: ingesteld, berekend, driverdiagnose en UART-statistieken.
Selecteer een rij en voeg echte metingen met meetmethode/instrument toe.
Lege velden zijn onbekend. Waarnemingen zoals “warm” horen in vrije tekst,
niet in een verzonnen temperatuurwaarde. `vref_v` in driverconfiguratie is
handmatige invoer voor de stroomberekening; leg de echte Vref-meting daarnaast
vast bij het testresultaat. UART meet noch wijzigt de potentiometer.

CSV bevat één rij per test en JSON-kolommen voor instellingen, meetherkomst,
diagnostiek en tijdsamples; JSON bewaart dezelfde volledige structuur.
Exporteer vóór het afsluiten: resultaten staan tijdens de sessie in geheugen.
Bestandsvensters openen alleen wanneer alle motoren stilstaan en niet in
houdstroom staan, zodat een modaal venster STOP nooit tijdens beweging blokkeert.
Een driverfout, onderbroken test en simulatie zijn expliciet gelabeld.

**Kalibratie**: doe een eenrichtingsproef, noteer de berekende omwentelingen en
meet echte omwentelingen óf verplaatsing met bekende spoed. Nieuwe factor =
oude factor × gemeten/berekend. De factor corrigeert een schaalafwijking,
geen slip of verloren stappen. Gebruik voor kalibratie geen netto nulstand
van een heen-en-terugcyclus. Toepassen gebeurt uitsluitend bij stilstand.

**Instellingen/profiel opslaan** bewaart motorconfiguratie, beweging,
mechanische invoer en sweepvelden in JSON. Laden vult invoervelden zonder
beweging te starten of een fysieke referentie automatisch geldig te maken;
pas driver en mechanica bewust toe. Bestanden zijn lokaal en overdraagbaar.

## CLI zonder GUI

```sh
python -m desktop.cli ports
python -m desktop.cli --simulate --export demo.json demo
python -m desktop.cli --port COM7 shell
python -m desktop.cli --port /dev/ttyACM0 --export resultaten.csv run desktop/example_steps.json
python -m desktop.cli --simulate request '{"cmd":"diagnose","motor":"m1"}'
```

In een Windows CMD-shell gebruik je voor de laatste opdracht dubbele quotes
met ge-escapete binnenquotes, of gebruik de interactieve `shell`. Daar geef
je gewone JSON per regel, zonder shellquoting:

```json
{"cmd":"move","mode":"continuous","rpm":30,"accel":100,"decel":100}
{"cmd":"speed","rpm":60}
{"cmd":"speed","rpm":-30}
{"cmd":"stop"}
```

`status`, `diagnose`, `clear_fault`, `!` en `quit` mogen zonder JSON. `--motor m2`
selecteert een ander geconfigureerd kanaal. In interactieve modus loopt de
heartbeat tijdens wachten op invoer. Ctrl+C, einde invoer en afsluiten sturen
STOP. Een eenmalige `request` wacht een eindige beweging af; continu draaien
vereist de interactieve shell zodat de controller aanwezig blijft.
