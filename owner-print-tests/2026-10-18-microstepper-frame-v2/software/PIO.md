# Eén GPIO voor TMC2208-UART

De `PIOUARTTransport` in `main.py` gebruikt één RP2040-state-machine en één
GPIO per driver. De volledige firmware staat in `main.py`; dit document bevat
geen extra Pico-module. Referentie: officiële [TMC220x/TMC2224-datasheet,
rev. 1.13](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf),
§4.1–4.4 en register `SLAVECONF` (§5).

## Bedrading van het UART-deel

Voeg bij beide varianten gemeenschappelijke massa toe. Gebruik 3,3 V voor
`VCC_IO`. De module moet zijn eventuele PDN/UART-soldeerbrug correct hebben.
De volledige motor-, EN-, STEP- en DIR-bedrading staat in [bedradingshandleiding](WIRING.md).

```text
Eén GPIO / PIO (bijvoorbeeld GP4, één kanaal per driver):

Pico GP4 ── 1 kΩ ──┬── TMC2208 PDN_UART
                   └── 10 kΩ ── 3V3

Twee GPIO's / hardware-UART1 (diagnosefallback):

Pico GP4 / TX ── 1 kΩ ──┬── TMC2208 PDN_UART
Pico GP5 / RX ───────────┘
```

Bij PIO wordt de GPIO alleen tijdens de aanvraag als uitgang ingeschakeld;
daarna is hij ingang met pull-up. De externe 10 kΩ zorgt voor een voorspelbaar
hoog rustniveau; de 1 kΩ beperkt stroom bij een bedradingsfout. Gebruik korte
draden. Verbind bij PIO **geen afzonderlijke actieve TX-uitgang** met dezelfde
draad. Bij de fallback begrenst de 1 kΩ de stroom tussen TX en de antwoordende
driver, volgens datasheetfiguur 4.1; RX ontvangt de verzonden bytes als echo.

## Timing en uitvoering

De PIO-klok is `8 × baud`; standaard 921.600 Hz bij 115.200 baud. Een
fractionele RP2040-klokdeler rondt die klok af. De standaard UART-synchronisatie
van de TMC2208 volgt de aangeleverde baudrate. Het programma beslaat 22 van de
32 instructiewoorden en kan door meerdere state-machines op hetzelfde
PIO-blok worden gedeeld. Er wordt geen volledig PIO-blok gereset.

| Gebeurtenis | PIO-cycli / gevolg |
| --- | --- |
| Elke TX-bit | `OUT [6]` + `JMP` = exact 8 cycli |
| Laatste stopbit | Volledige 8 cycli hoog, daarna `SET PINDIRS,0` |
| Ontvangst gereed | 3 cycli na vrijgeven; standaard driverantwoord pas na 8 bittijden |
| Eerste RX-databit | 12 cycli na gedetecteerde startflank, midden van databit 0 |
| Volgende RX-databits | Elke 8 cycli |
| Stopcontrole | 76 cycli na startflank, midden van stopbit |
| Driveruitgang vrij | Datasheet: 4 bittijden na laatste stopbit |
| Tussen transacties | Minstens 12 bittijden rust na ontvangst |
| Herstel na fout | Uitgang vrijgeven, 80 bittijden wachten en SM opnieuw initialiseren |

Ingangssynchronisatie en het waarnemen van een startflank voegen een kleine
faseverschuiving toe; het midden van een UART-bit biedt hiervoor marge. De
modellen testen ook antwoordbits met ±2% afwijkende duur. Dit is geen meting
van lijnkwaliteit, jitter of de toleranties van het fysieke bord.

De aanvraag wordt vooraf volledig in de TX-FIFO geladen: één besturingswoord
en maximaal drie datawoorden. Hierdoor kan een MicroPython-pauze geen
ongewenste lange ruimte tussen aanvraagbytes maken. Aan de ontvangende kant
worden acht antwoordbytes in 3 + 3 + 2 bytes verpakt, gevolgd door één
statuswoord. Alle vier woorden passen in de RX-FIFO. Er is geen Python-interrupt
of polling binnen een UART-byte nodig en een garbage collection-pauze verliest
dus geen reeds gestarte complete antwoordframe. Softwarepolling blijft nodig
om een ontbrekend antwoord tijdig als fout te melden.

De stopbit wordt gecontroleerd; een lage stopbit levert een expliciete
framingfout. Het transport verwijdert bij hardware-UART de verplichte exacte
TX-echo. De PIO-variant ontvangt geen eigen echo. De driverlaag controleert
antwoordheader, registeradres en CRC en controleert schrijfacties via IFCNT.
Een CRC is geen bevestiging van beweging.

De timeout is standaard 20 ms en moet lang genoeg zijn voor aanvraag,
maximale SENDDELAY en antwoord. `SENDDELAY` 0/1 betekent 8 bittijden;
2/3 betekent 24, tot 14/15 = 120. De datasheet reset ontvangst bij meer dan
63 bittijden tussen opeenvolgende startbits; daarna is minimaal 12 bittijden
rust nodig. Foutafhandeling respecteert beide. Het PIO-transport controleert
ook op een langdurig lage bus voordat het een aanvraag start.

De gedocumenteerde baudgrenzen zijn minimaal 9.000 baud en maximaal
`fCLK / 16` van de **driver**, niet van de RP2040. Bij de veronderstelde
12 MHz driverklok is dat 750.000 baud. Deze implementatie richt zich op
115.200 baud; hogere instellingen vergen aparte elektrische validatie.

## Adressering en bewezen bereik

De TMC2208 heeft vast adres **0**. Twee of drie onafhankelijk regelbare
drivers krijgen afzonderlijke GPIO-kanalen en verschillende state-machine-ID's
(0–7), of afzonderlijke hardware-UART-kanalen. Ze mogen niet samen antwoorden
op één gedeelde draad. Selectie via externe analoge schakelaars kan volgens
§4.4, maar is hier niet nodig en niet geïmplementeerd.

`tests/test_transport.py` voert de PIO-instructies uit de echte firmwarebron
in een cyclusmodel uit, inclusief FIFO's, TX- en RX-shiftregisters,
bitvertragingen en GPIO-richting. Tests dekken volledige stopbits,
ontvangstomschakeling, framingfouten, FIFO-capaciteit zonder CPU-bediening,
CRC, echo, time-outs en herstel. Het programma is daarnaast met de officiële
`rp2.asm_pio`-assembler van MicroPython **v1.26.1** geassembleerd: 22 geldige
instructies. Dit bewijst geen fysieke communicatie op een Pico.

Minimale fysieke controle: motorvoeding bereikbaar uitschakelbaar houden,
uitgangen uitgeschakeld laten, eerst herhaald `diagnose` uitvoeren bij 115200
baud en driver-ID/IFCNT controleren. Vergelijk zo nodig de tweepinsvariant.
Controleer met een logic analyzer dat de GPIO na de volledige stopbit vrijkomt
en de eerste antwoordbyte intact is. Pas daarna een langzame, korte
motorbeweging uitvoeren volgens de gebruikshandleiding.
