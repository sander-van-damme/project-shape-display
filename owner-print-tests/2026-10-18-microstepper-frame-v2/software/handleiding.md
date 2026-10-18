# E-302 motor-testsoftware

Werkend softwareplatform voor **Pico W / RP2040, MicroPython 1.26.1 en TMC2208**.
Eén bestand op de Pico; lokale Python/Tkinter-bediening op Windows/Linux.
De PIO-verbinding, snelheden en meermotorbesturing zijn met softwaremodellen
gecontroleerd, **nog niet fysiek met deze nieuwe firmware**.

## Beginnen

1. Volg [bedrading en opstart](WIRING.md). STEP en DIR aan GND; EN via GP6
   met een externe pull-up. De bestaande fysieke motorvoedingsschakelaar blijft bereikbaar.
2. Installeer officiële **MicroPython 1.26.1 voor RPI_PICO_W** via BOOTSEL.
   Kopieer uitsluitend **[main.py](main.py)** naar de hoofdmap van de Pico als `main.py`
   (bijvoorbeeld via Thonny → Opslaan op Raspberry Pi Pico). Er zijn geen andere
   Pythonbestanden op de Pico nodig. Sluit daarna Thonny/PuTTY zodat de COM-poort vrij is.
3. Installeer Python 3.8 of nieuwer met Tkinter. Vanuit deze `software/`-map:

   ```text
   python -m pip install -r requirements.txt
   python -m desktop.app
   ```

   Windows: `start_windows.bat`; Linux: `./start_linux.sh`. Op Debian/Ubuntu kan
   `python3-tk` en toegang tot de seriële poort via de groep `dialout` nodig zijn.
4. Kies de gevonden COM-poort en verbind. Begin met een **vrije, losgekoppelde
   motor**, profiel `e301_conservative`, kort bij 10 RPM en bijvoorbeeld 100 RPM/s.
   Start doet automatisch driveridentificatie, configuratie en controle.
   De rode **STOP** schakelt direct uit; de normale stop remt af.
5. Zonder hardware: kies **SIMULATIE**. Dezelfde firmware, protocolafhandeling en
   planner draaien dan tegen een registermodel; exports blijven als simulatie gemarkeerd.

[Desktop, CLI, profielen, sweeps en kalibratie](DESKTOP.md) ·
[Serieel protocol](PROTOCOL.md) · [Driverinstellingen](DRIVER.md) ·
[Bewegingsberekeningen](MOTION.md) · [PIO-timing](PIO.md) ·
[Uitgevoerde validatie](VALIDATION.md).

## Wat je kunt onderzoeken

Vrij draaien met live RPM/richtingswijzigingen; een aantal omwentelingen,
tijdsduur of herhaalde heen/terugcycli; acceleratie en deceleratie; RPM-sweeps;
vergelijking van choppermodus, microsteps, stroom en acceleratie. Instellingen
staan in profielen. CSV/JSON bevat de aangevraagde instellingen, berekende
beweging, driverdiagnostiek en afzonderlijk ingevoerde metingen/observaties.
Een fout, afgebroken beweging of verdwenen verbinding beëindigt de sweep.

De standaard is de eerder gebruikte lage stroom: **IRUN=IHOLD=5, VSENSE=1,
Vref handmatig 0,80 V, aangenomen R110, 8 microsteps en voorlopig 20 volle
stappen/omwenteling**. De berekende circa 77 mA fasepiek / 55 mA RMS zijn geen
metingen. Vref wordt fysiek met de trimmer ingesteld; UART meet of wijzigt dit niet.

Er is geen 120-RPM-cap. Grenzen volgen uit signed 24-bit VACTUAL, de ingestelde
motorparameters en expliciete pintestgrenzen. Berekenbare hoge RPM bewijst geen
bruikbaar motorkoppel, juiste rotatie of beweging zonder stappenverlies.
**Circa 40 mm in minder dan één seconde is een onderzoeksdoel**, geen gemeten
prestatie en geen softwareacceptatie-eis.

## Pintest en meerdere motoren

Voor een pintest moet je zelf de bruikbare minimum-/maximumpositie, effectieve
verplaatsing per omwenteling en huidige handmatige positie invoeren. **50 mm
pinlengte is geen 50 mm slag.** De firmware begrenst de berekende beweging,
inclusief remweg, maar ziet geen slip, vastlopen of echte positie. Na noodstop,
communicatiefout of wijziging van de omzetting moet je de positie opnieuw bepalen.
Een normale afgeronde beweging houdt de berekende referentie bij.

`MOTOR_CHANNELS` boven de controllersectie van `main.py` kiest PIO of de bewezen
tweepins-UART-topologie. Voor motor 2/3 staan voorbeeldregels klaar: activeer ze
met elk een eigen PDN_UART-draad, EN-GPIO en PIO-state-machine. Eén TMC2208 heeft
vast adres 0; MS1/MS2 geven hem **geen** afzonderlijk UART-adres. De GUI ontdekt
de geconfigureerde motoren via `hello`. De meermotorlogica is alleen gesimuleerd.

## Onderhoud en grenzen

Alle firmware staat letterlijk in `main.py`, georganiseerd in transport,
registerdriver, planner, motorcontroller en protocol. Desktopcode gebruikt alleen
de standaardbibliotheek en pyserial. Er is geen Wi-Fi/cloudservice. De simulator
onderaan de firmware wordt op de Pico niet gebruikt. Geen OTP-programmering,
StallGuard, CoolStep, encoder of automatische positiebepaling.

Deze map is de actieve software voor E-302. De E-301-firmware/Uno-code en hun
fysieke resultaten blijven ongewijzigde historische bronnen. CAD/STL/3MF zijn
niet gewijzigd. Er is geen nieuwe printtest of nieuw experimentnummer gemaakt.
