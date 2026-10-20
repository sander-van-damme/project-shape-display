# Ø8-mm microstappenmotor — varianten, stroom en grenzen

**Bronstand: 20 oktober 2026.** [Componenten](components.md) · [Elektronica](electronics.md) · [DES-009](DES-009-traveling-motor-bank-screw-pins.md)

Dit is een **gericht, voorlopig bronnenoverzicht**, geen afgerond exhaustief literatuuronderzoek. Het afzonderlijk aangevraagde diepgaande onderzoeksrapport was bij deze vastlegging nog niet beschikbaar. Een passende productspecificatie bewijst niet dat alle motoren in de voorraad van dezelfde OEM, winding of partij komen. Onderstaande getallen zijn **geen toestemming om een bepaalde stroom continu te gebruiken**.

## 1. Wat aan de eigen motoren is vastgesteld

| Eigenschap | Status en bron |
|---|---|
| Metalen motorhuis | **9,2 mm hoog, circa Ø8 mm** — eigenaarmeting, gemeld op 20 oktober 2026; meetmethode/tolerantie niet vastgelegd |
| Kale motoras | **Circa Ø0,8 mm** — eigenaarmeting; niet verwarren met buitendiameter van het tandwiel |
| Uitvoeringen | Twee varianten met verschillend uitstekend tandwiel, klein zijprintje, vier draden — eigenaarobservatie; exacte uitstekende lengtes niet gemeten |
| Tandwiel | C-koppeling met drie ribben paste fysiek; **9 tanden/module 0,2/Ø2,2 mm** komen uit een catalogusbeeld en zijn niet allemaal aan de eigen voorraad gemeten |
| Werking | Eén motor beweegt een schroefpin op en neer; met hogere ingestelde stroom minder vastlopen — eigenaarobservatie, **geen gemeten koppel, snelheid of spoelstroom** |
| Motoridentiteit | **PM08-2 / PM08-02 is nu een aannemelijkere hypothese**, door overeenkomende 9,2-mm huismaat en Ø0,8-mm as. Exact typenummer, OEM en windingvariant blijven onbevestigd |

Deze metingen **spreken de eerdere veronderstelling van een 8,2-mm huis en Ø1,5-mm as tegen**. De oude 8,2/1,5-getallen kwamen van een verkopersafbeelding, niet van een schuifmaat op de gebruikte motor.

## 2. Gedocumenteerde typen en verwante aanbiedingen

| Type/aanbieding | Elektrisch | Mechanisch / overig | Bewijsklasse en beperking |
|---|---|---|---|
| **PM08-02**, [Tempero PDF v1.0](historical/trial-0/micro-stepper-datasheet.pdf) | **3,3 V nominale spanning; 40 Ω ±7% per spoel**; 2 fasen, bipolair | Ø8 × 9,2 mm; as Ø0,8 mm; 18°/volle stap = 20 stappen/omw.; pull-in ≥5 gf·cm (onbelast); isolatieklasse F; omgeving −10 tot +50 °C | **Leveranciersdatasheet**, geen op de eigen voorraad geverifieerd OEM-certificaat of maximaal-toegestane fasestroom |
| **PM08-2**, [Tempero productpagina](https://temperosystems.com.au/products/pm08-2-8mm-micro-stepper-motor-2-phase-4-wire/) | 3,3 V nominale spanning; verkoper zegt ook *can run on 5v* | Asuitsteking lang 4 mm / kort 3,5 mm; tandwiel 9 tanden, module 0,2, volgens pagina Ø2,0 mm | **Verkopersclaim**; 5 V kunnen draaien is geen vrijgave voor continu bedrijf; tandwiel-Ø wijkt af van Amazon |
| **Abovehill B08346RFVZ**, [Amazon](https://www.amazon.com/Abovehill-Stepper-2-Phase-4-Wire-Connection/dp/B08346RFVZ) | 39,2 Ω; geschatte fasespanning 5–6 V; circa 0,12 A en 0,14 A “short-circuit current” | Catalogusfoto Ø8 × **8,2 mm**, as **Ø1,5 mm**, tandwiel Ø2,2 mm / 9 tanden / m0,2 | **Verkoper**; huis/as weersproken door eigenaarsmetingen; 0,14 A is **geen bewezen veilige piek- of continulimiet** |
| **PM08-02**, [VIC-TECH productpagina](https://www.micro-steppermotor.com/sale-11879303-8mm-micro-stepper-motor-2-phase-4-wire-mini-stepper-motor-with-copper-gear-for-camera-lenses-pm08.html) | 3,3 V, 40 Ω ±7% in detailtabel, elders ±10% | Ø8 × 9,2 mm, Ø0,8 mm as, 18°; mogelijke PCB-/kabel-/connectorvarianten | **Fabrikant-gepresenteerde verkoopsite** van Changzhou Vic-Tech; aanwijzing voor leverancier/OEM-familie, **geen bewezen herkomst van onze motoren** |
| **PM08-002**, [VIC-TECH aanbieding “385mA”](https://www.micro-steppermotor.com/sale-53946140-8mm-diameter-2-phase-4-wire-micro-stepper-motor-with-385ma-current-and-18-degree-step-angle-for-prec.html) | Kop: **385 mA/fase**, **20,4 Ω**, **3,3 V** | Kop: Ø8 × 9,2 mm, Ø0,8 mm as, 18° | **Intern tegenstrijdige verkooptekst**: dezelfde pagina bevat een tabel voor een **Ø20-mm, 1,8°-hybridemotor, 5 V/0,24 A**. De 385 mA mag **niet** als limiet voor PM08-02 of onze motoren worden overgenomen |
| **SM08133**, [VIC-TECH fabrikantpagina](https://www.vic-motor.com/8mm-mini-micro-stepper-motor-2-phase-18-degree-step-angle-2-product/) | 3,3 V; **20 Ω ±10% in kop, 40 Ω ±7% in detailtabel** | 8-mm klasse, 18°; klasse E en 0–55 °C volgens detailtabel | **Ander model, tegenstrijdige bron**. Bewijst geen 20-Ω-winding van onze PM08-motoren |
| **08BY25**, [andere 8-mm motorfamilie](https://www.motormicro.com/product/08by25-8mm-micro-stepper-motor-18-degree) | Geadverteerde 10/20/40-Ω-versies met verschillende stromen | Huislengte circa 10,7 mm; 18° | **Vergelijkingsfamilie, niet uitwisselbaar met PM08-02**. Stroomratings niet naar onze motor overzetten |

Een Amazon-gebruikersreview van **10 juni 2024** identificeerde de aangeboden motor als “PM08-2”, 18°/stap, met negen tanden. Dit is een **gebruikersidentificatie**, geen fabrikantbevestiging. Meerdere verkooppagina's kunnen bovendien dezelfde tekst/tekening hergebruiken; overeenstemming tussen die pagina's is geen onafhankelijke meting.

**Herkomst:** Tempero verspreidt een eigen versie-1.0-PDF; VIC-TECH biedt PM08-02 aan en presenteert zich als fabrikant. Zonder markering op de motor, traceerbare bestelling of OEM-verklaring is **niet bewezen** dat Tempero de fabrikant is, dat VIC-TECH de daadwerkelijke producent van onze partij is, of dat alle “PM08-2”-aanbiedingen identiek zijn.

## 3. Wat de bronnen wel en niet begrenzen

| Gegeven | Bronstatus | Technische interpretatie |
|---|---|---|
| **3,3 V** bij **40 Ω ±7%** | PM08-02 leveranciersdatasheet | Nominale DC-fasespanning en koude weerstand; **geen expliciete maximaal toelaatbare stroom** |
| **−10 tot +50 °C** | PM08-02 leveranciersdatasheet | Opgegeven **omgevingstemperatuurbereik**, niet maximale motoroppervlak- of windingtemperatuur |
| **Isolatieklasse F** | PM08-02 leveranciersdatasheet | Materiaalklasse; **geen toestemming** om de motor continu op een bepaalde windingtemperatuur of stroom te bedrijven |
| **5 gf·cm pull-in, onbelast** | PM08-02 leveranciersdatasheet | Ongeveer **0,49 mN·m**; geen bruikbare belastings-/toerentalkromme of gegarandeerde schroefkracht |
| **Max response >800 pps; max starting >1000 pps**, onbelast | PM08-02 leveranciersdatasheet | Ondergrensclaims onder onvolledige testcondities; de volgorde response/starting is ongebruikelijk. **Geen bewezen maximumtoerental onder pinlast** |
| **“Dielectric strength 3 mA max”** | PM08-02 leveranciersdatasheet | Een isolatie-/lekstroomgegeven, **niet** de toegestane spoelstroom |
| **0,12 A / 0,14 A “short circuit”** | Abovehill verkoper | Onduidelijke testmethode; **geen motorlimiet** |
| **385 mA/fase** | VIC-TECH intern vervuilde verkooppagina | **Niet bruikbaar** voor deze motor zonder gecorrigeerd typenummer en fabrikantdocument |
| **Maximale continue fasestroom, kortdurende piekstroom, duty cycle, windingtemperatuurstijging, thermische weerstand, koppel-toerentalkromme, asbelasting** | **Onbekend** voor de eigen motoren | Niet afleiden uit een driverdatasheet, isolatieklasse, advertentie of korte geslaagde beweging |

Bij **3,3 V / 40 Ω = 82,5 mA** loopt er *theoretisch* DC door één fase met 3,3 V direct over die winding (bij 40 Ω koud). Bij ±7% weerstand is dat circa **77–89 mA**. Dit is **geen geverifieerde continue RMS-stroomrating voor sinusvormige chopperaansturing**. Bij de Abovehill-opgave is **5/39,2 ≈ 128 mA** en **6/39,2 ≈ 153 mA** slechts de wet van Ohm; de opgegeven 0,12/0,14 A zijn daarmee niet tot thermische limieten gepromoveerd.

## 4. TMC2208: berekende instellingen zijn geen motorstroommetingen

Zie de [ADI/TRINAMIC TMC2208-datasheet rev1.13](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf), §9–9.1, en onze [elektronicabasis](electronics.md).

Voor de **aangenomen**, nog niet op de PCB geverifieerde configuratie (externe R110-shunts, `R_sense=0,110 Ω`, `VSENSE=1`, analoge Vref-schaal actief, SpreadCycle):

```text
I_piek = (IRUN+1)/32 × 0,180 V/(0,110+0,030) Ω × (Vref/2,5 V)
I_RMS  = I_piek/√2
```

| Vref echt gemeten aan trimmer | IRUN | Theoretische piek/fase | Theoretische RMS/fase | Status |
|---:|---:|---:|---:|---|
| 0,80 V | 5 | 77 mA | **55 mA** | E-301 referentie-instelling; één pin bewoog |
| 1,18 V | 5 | 114 mA | **80 mA** | Berekening, geen stroommeting |
| 1,18 V | 10 | 209 mA | **148 mA** | Eigenaar meldt duidelijk betrouwbaardere beweging; temperatuur en stroom **niet gemeten** |

Bij gelijke windingweerstand zou **148 mA RMS/fase circa 3,2× zoveel koperverlies per fase** geven als **82,5 mA RMS/fase**. Bij ideale tweefasen-sinusaansturing en 40 Ω komt dit neer op circa **1,74 W totaal koperverlies**; dat is **geen voorspelde temperatuur** en de vergelijking met nominale 3,3-V-DC-bekrachtiging veronderstelt gelijke RMS-definitie en windingtemperatuur. De 148 mA kunnen voor continu bedrijf te hoog zijn; de bron levert **geen betrouwbare veilige tijdslimiet**.

**VM circa 9 V** is de voedingsspanning van de stroomgeregelde driver, **niet 9 V DC continu over de spoel**. De TMC2208-chipgrens voor VM is geen motorgrens. Vref op de GUI aanpassen zonder de fysieke trimmer te verdraaien verandert de analoge referentie niet. De theoretische formules gelden alleen als de werkelijke module, shunts en registers overeenkomen; hoge snelheid en tegen-EMK kunnen verhinderen dat de doelstroom bereikt wordt. Driver-overtemperatuurbeveiliging beschermt **niet** automatisch de motorwikkelingen.

## 5. Toerental en betekenis voor Shape Display

De schroefspoed is **3 mm per omwenteling**. Voor **40 mm in 1 s** zou bij constante snelheid **13,33 omw./s = 800 rpm** nodig zijn, **zonder** aanloop-, stop-, koppel- en spelingverliezen. Bij 18°/stap is dit **circa 267 volle stappen/s**. Dit is een **kinematische berekening**, geen aangetoonde prestatie.

De in de GUI gekozen **5000 rpm is een opdrachtwaarde**, niet een gemeten toerental. Dat getal correspondeert bij 20 volle stappen/omw. met circa **1667 volle stappen/s**, maar bewijst niet dat de rotor volgt of dat de pin die snelheid onder belasting haalt. De leveranciersclaims in pps zijn geen volledige torque-speed curve.

## 6. Consequentie voor het actuele v3-frame

In [v3 CAD](../../owner-print-tests/2026-10-19-microstepper-frame-v3/cad/rig.scad) is de cilindrische motorzitting getekend met `cylinder(d=8.2,h=8.5)`, vanaf Z=2 tot Z=10,5 mm. Een **9,2-mm huis** zou vanaf dezelfde basis tot **Z=11,2 mm** reiken; de bovenliggende constructie en axiale positie moeten opnieuw worden beoordeeld. De plaatselijke bovenste uitsparing is geen bewezen oplossing voor het volledige huis en het PCB. De bestaande **3MF blijft een digitale slice, geen bewezen passende motorhouder**. Geen CAD/STL/3MF is door deze documentatieaanpassing gewijzigd.

## 7. Kleinste besluitvormende controles — niet automatisch gestart

1. **Motor spanningsloos en van driver los:** meet de weerstand van beide spoelparen (rekening houdend met meetsnoeren). Rond **37–43 Ω** ondersteunt de 40-Ω-variant; een duidelijk andere waarde betekent andere winding/bedrading of meetprobleem, **niet** automatisch een defect.
2. **Vóór printen of motorbedrijf:** meet per gebruikte motorvariant huislengte, kale as en daadwerkelijke tandwieluitsteking; corrigeer dan pas frame/rotor-CAD en slice een nieuwe 3MF. De 9,2-mm maat maakt de oude READY-plaat onvoldoende onderbouwd.
3. **Alleen indien hogere stroom nodig blijft:** meet motortemperatuurstijging bij **vastgelegde echte Vref, IRUN, looptijd en duty cycle**, aanvankelijk kort en met veilige stop. Meet daarnaast echte omwentelingen/pinverplaatsing onder representatieve belasting. Pas daarmee kunnen bruikbare stroom en snelheid worden gekozen; **geen datasheetloze 148-mA-continuvrijgave**.

**Beslisgrens:** deze bronnen rechtvaardigen een correctie van de framegeometrie en een voorzichtige motorproef, maar **nog geen definitieve maximale stroom, duty cycle, RPM of complete-bankarchitectuur**.
