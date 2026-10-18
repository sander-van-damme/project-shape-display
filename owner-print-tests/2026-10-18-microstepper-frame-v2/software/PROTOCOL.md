# USB-serieel protocol v1

USB CDC van MicroPython, desktop opent op 115200 baud, 8N1. Dit is onafhankelijk
van de TMC-UART op GP4. Eén UTF-8 JSON-object per regel, maximaal 8192 bytes vóór
newline. Requests worden na elkaar afgehandeld. `id` is optioneel; indien aanwezig
een integer (geen boolean). Antwoord: `{"id":1,"ok":true,"result":{...}}` of
`{"id":1,"ok":false,"error":"uitleg"}`. Zonder id is antwoord-id `null`.
Onbekende/ongeldige opdrachten wissen geen correcte configuratie of lopende test.

**De losse byte `!` stopt alle motoren onmiddellijk**, ook midden in een onvolledige
of te lange regel. Deze byte is daarom gereserveerd, ook binnen JSON-strings.
Er volgt geen aparte bevestiging; vraag `status`. Een normale JSON-stop remt af.
STOP en foutstop invalideren de pintestreferentie wanneer de stop abrupt is.

Zend `{"cmd":"heartbeat"}` elke 0,5 s. De default timeout is 2 s, ingesteld via
`HEARTBEAT_TIMEOUT_S` in `main.py`. De watchdog geldt voor beweging, initialisatie
en ingeschakelde houdstroom. Na timeout volgen EN hoog, beste poging tot UART-uit
én een foutlatch; herstel/verbinding hervat nooit automatisch. De standalone CLI
verzorgt heartbeats zolang hij een test begeleidt. Een losse terminal moet ze zelf
sturen. De stoplatentie bevat de lopende begrensde UART-transactie/USB-afhandeling.

| `cmd` | Velden / resultaat |
|---|---|
| `hello` | Protocol/firmwareversie, motor-ID's, standaardprofielen, volledig configuratieschema en heartbeat-timeout |
| `heartbeat` | Resultaat `alive:true` |
| `status` | Optioneel `motor`; resultaat `motors:[...]` met één of alle statussen; geen nieuwe driver-UART-reads |
| `configure` | `motor`, `config:{...}`; gedeeltelijke wijziging, gevalideerd vóór hardwarewijziging |
| `diagnose` | `motor`; volledige actuele driverregisters en theoretische stroom |
| `move` | `motor`, `mode`, signed `rpm`, positieve `accel`/`decel` in RPM/s; zie hieronder |
| `speed` | `motor`, signed `rpm`, optioneel `accel`/`decel`; alleen tijdens continu draaien; nul remt af tot stop |
| `stop` | Optioneel `motor` (anders alle), optioneel `emergency:true` (standaard false) |
| `mechanics` | `motor`, `settings:{mode:"free"}` of alle expliciete pinvelden hieronder |
| `reference` | `motor`, `position_mm`; handmatig bepaalde positie binnen ingestelde grenzen, bij stilstand |
| `clear_fault` | `motor`; opnieuw configureren/controleren bij stilstand; geen herstart en geen nieuwe pinreferentie |

`move.mode`: `continuous`; `revolutions` met positieve `revolutions`; `duration`
met positieve `duration_s`; `cycles` met positieve `revolutions`, positief geheel
`cycles`, optioneel niet-negatief `dwell_s`. Eén cyclus is heen én terug. Het teken
van RPM bepaalt de eerste richting. Duur omvat acceleratie én deceleratie;
eindigen wordt bevestigd nadat nul is toegepast. Er zijn geen arbitraire maxima
voor omwentelingen, duur of cycli, wel eindigheid/numerieke representatie en
signed 24-bit VACTUAL. Een RPM die naar VACTUAL=0 afrondt wordt als doel geweigerd.

Voorbeelden (elke regel apart; blijf tussendoor heartbeats sturen):

```json
{"id":1,"cmd":"hello"}
{"id":2,"cmd":"move","motor":"m1","mode":"revolutions","rpm":100,"accel":200,"decel":200,"revolutions":1}
{"id":3,"cmd":"status","motor":"m1"}
{"id":4,"cmd":"mechanics","motor":"m1","settings":{"mode":"pin","min_mm":0,"max_mm":3,"lead_mm_per_rev":3,"position_mm":1.5}}
{"id":5,"cmd":"move","motor":"m1","mode":"cycles","rpm":30,"accel":100,"decel":100,"revolutions":0.25,"cycles":5,"dwell_s":0.3}
```

De **voorbeeldgrenzen 0–3 mm zijn geen gemeten slag van jouw E-302**. Vul eigen
bruikbare grenzen in. De genoemde 50-mm-pin geeft geen automatische slagwaarde.

Status bevat `state` (`idle`, `warming`, `running`, `holding`, `fault`), `config`,
`motion`, `mechanics`, `diagnostics`, `uart` en `fault`. `motion` rapporteert onder
meer aangevraagde/werkelijk naar VACTUAL omgerekende RPM, geïntegreerde signed
omwentelingen, totale afgelegde weg, duur, cycli, restant, updatevertragingen en
`completed`/`completion_reason`. Dit zijn **berekende commandoresultaten**.
`mechanics.position_mm_calculated` is `null` zonder geldige handmatige referentie.
Een onderschepte grens heet `boundary`, is geen voltooid experiment en laat een
sweep stoppen. Driverfouten zijn geen stall-/motorpositie-/motortemperatuursensor.

Volledige configuratie/diagnose gebeurt bij stilstand van alle motoren; dat voorkomt
dat een lange registerreeks een actieve beweging ophoudt. Voor gelijktijdige tests:
configureer eerst de gekozen motoren, start ze daarna afzonderlijk. Een al
geconfigureerde driver krijgt vóór iedere start een actuele compacte controle.
Tijdens beweging worden compacte statuscontroles gespreid over de kanalen.
`status` blijft bereikbaar en geeft de laatst ontvangen driverdiagnostiek.

Het firmwarehoofdbestand bevat alle protocolbroncode: `Firmware.handle`,
`Firmware.feed` en `MotorController`. `desktop/transport.py` bevat USB-framing,
request-ID's, time-outs en de simulatoradapter; `desktop/worker.py` verzorgt
heartbeat, reconnect, STOP-prioriteit en de testvolgorde.
