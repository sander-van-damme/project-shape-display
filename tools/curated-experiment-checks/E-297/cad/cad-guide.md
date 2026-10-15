# CAD-pakket — twee afzonderlijke axiaal bewegende koppelingshelften

De aangeleverde STL's en STEP-onderdelen zijn al geëxporteerd. De eigenaar hoeft `generate.py` niet uit te voeren. Print vanuit de twee meegeleverde Bambu-projecten in `owner-print-tests/2026-10-16-two-half-clutch-*`; de STEP-bestanden zijn aanvullende constructiegegevens, geen printerprojecten.

`generate.py` bouwt de parametrische onderdelen met CadQuery en verenigt de bestaande E-295-draadmesh met de nieuwe schroefvoet. De functionele draad wordt niet geschaald of opnieuw benaderd. `e295-thread.stl`, `e295-pin.stl`, `extract_e295.py` en `../validation/e295-source.json` leggen de herkomst vast. De gesloten pin komt uit de nominale E-295-demonstratie: hetzelfde fysiek succesvol bevonden draadprofiel en 0,175-mm radiale relief, maar een gesloten top en nieuwe printoriëntatie blijven wijzigingen die fysiek moeten worden beproefd.

## Vaste maatvoering

Alle maten in mm; Z is de schroefas, rijselectie omhoog en kolomselectie omlaag. Vier celassen liggen op `(±2,54, ±2,54)`.

| Onderdeel / functie | Maat |
|---|---:|
| Raster / vierkante pin | 5,08 / 4,40 |
| Iedere selector: totale slag | 2,40 |
| Tipafstand zonder selectie | 3,36 |
| Tipafstand bij alleen rij of alleen kolom | 0,96 |
| Axiale tandinschuiving bij beide selecties | 1,44 |
| Rotorvoetflens / dikte | Ø4,30 / 0,72 |
| Rotorhals | Ø3,20, Z 0,72–2,00 |
| Overgang naar geleidekop | Ø3,20→3,60, Z 2,00–2,20 |
| Geleidekop / tandbasis | Ø3,60, Z 2,20–6,20 |
| Twee tegenoverliggende tanden | 76° sector, binnenstraal 0,60, buitenstraal 1,80 |
| Tandhoogte / totale rotorhoogte | 2,40 / 8,60 |
| Invangvlak | laatste 0,24 hoog; sector versmalt naar 56° |
| Blinde dubbel-D-boring nominaal | Ø2,50 / vlakmaat 1,90 / diepte 5,48 |
| Gesloten materiaal tussen boring en tanden | 0,72 |
| Dubbel-D-as | Ø2,20 / vlakmaat 1,60 |
| DD-ingrijping bij vrij / geselecteerd | 4,92 / 2,52 |
| Nominale ruimte tot blind gatdak | 0,56 bij grootste ingrijping |
| Twee combbladen / tussenruimte | elk 0,96 / 0,96 |
| Axiale speling rond flens | 0,24 totaal; rotor nominaal gecentreerd |
| Onderste / bovenste combopening | 2,50 / 3,50 |
| Comb breedte binnen raster | 4,60; 0,48 ruimte tussen buren |
| Externe geleidetab / sleufbreedte | 3,30 / 3,70 |
| Externe verhoogde-standshim | 2,40 hoog; tong 3,40 breed |
| Stationaire rotorgeleiding | Ø4,00-gaten, platen 1,20 dik |
| E-295 draad | grootste Ø3,20 / spoed 3,00 / diepte 0,90 / profielhoek 90° |

De tandtop versmalt hoekvormig, dus de lineaire terugname is straalafhankelijk; het is geen constante 0,24-mm afschuining langs de hele flank. De verticale hoofdflanken dragen in beide draairichtingen. De invangvlakken vervangen voorzichtig fasezoeken niet.

## Z-datums van de complete proef

| Element | Nominale Z |
|---|---:|
| Onderste rotorvoet, rij uit / aan | 7,00 / 9,40 |
| Bovenste rotorvoet, kolom uit / aan | 27,56 / 25,16; rotor omgekeerd |
| Vaste onderste rotorgeleiding | 11,80–13,00 |
| Vaste bovenste rotorgeleiding | 21,56–22,76 |
| Inputkraag: onder / boven | 1,20 / 3,00 |
| Inputretainer en lang geleidegat | 3,24–5,60 |
| Inputas tip | 11,92 |
| Schroef-DD-staart tip | 22,64 |
| Schroef: conisch steunvlak | 29,72–30,77 |
| Vast steunvlak raakt schroefconus bij Ø3,20 | 30,22 |
| Schroefflens bovenzijde / retainer onderzijde | 31,97 / 32,21 |
| Begin / einde functionele buitendraad | 32,96 / 48,96 |
| Pinonderkant in neutraal | 38,21 |
| Beproefde pinonderkant | 35,21–41,21 (±3,00) |
| Twee vierkante pingleidingen | 42,00–43,20 en 51,20–52,40 |

De schroef draagt zijn axiale last via de vaste conische zitting, niet via de kolomcomb. De bovenplaat begrenst oplichten tot nominaal 0,24 mm. De inputkraag is tussen vaste steunvlakken opgesloten; een Ø4,60-kamer begrenst haar radiale beweging. Geen van beide assen hoeft axiaal mee te bewegen met de selector.

De vaste Ø4,00-geleidingen omsluiten de Ø3,60-rotorkoppen tijdens de volledige selectorslag. Een eerdere uitvoering zonder deze geleidingen kon in een toegestane gekantelde stand een naburige rotor raken. Deze negatieve bevinding is de reden voor de langere koppen en geïntegreerde geleideplaten; zuiver coaxiale botsingsvrijheid was onvoldoende.

## Werkelijke montagevolgorde

1. Begin met uitsluitend het middenframe. Houd het aan de bovenrand rechtop; eventueel houdt een tijdelijk stukje tape de smalle framevoet op de tafel. De beide buitenhelften blijven volledig weg. De halve lagergaten aan beide X-zijden zijn bereikbaar.
2. Monteer eerst de verste rij (Y=+2,54): schuif haar linker inputas met onderste rotor vanaf −X en haar rechter paar vanaf +X in de halve zittingen van het middenframe. De inputkragen liggen op hun vaste steunvlakken. Houd de delen licht op hun plaats; niets vastpersen.
3. Breng de betreffende rijcomb eerst van de open X-zijkant in de lege voorruimte op Y=−8, met de bladen op hun juiste Z-hoogte. Schuif haar vervolgens in +Y-richting naar de verste rij, zodat beide U-monden de twee rotorflenzen gelijktijdig vangen. De voorste rij is hierbij nog afwezig.
4. Plaats nu de twee input/rotorparen van de voorste rij (Y=−2,54), opnieuw ieder vanaf zijn eigen X-zijde. Breng de tweede comb op dezelfde manier via de lege voorruimte naar haar twee flenzen. De combbladen passen tussen de vaste inputretainer en de onderste rotorgeleiding.
5. Maak de bovenste kolomgroepen buiten het frame: schroef twee pinnen op hun schroeven, schuif twee bovenrotoren op de neerwaartse DD-staarten en vang hun flenzen met één kolomcomb. Breng de complete linker kolomgroep vanaf −X en de rechter groep vanaf +X in de nog open halve schroef-, rotor- en pingleidingen. Houd de tanden uit elkaar; alle selectors staan uit.
6. Schuif pas nu de linker en rechter buitenframehelften vanaf hun eigen X-zijde op de integrale paspennen. Controleer dat iedere selectortab in zijn sleuf ligt. Fixeer de twee externe framevoegen met kleine stukjes tape aan de voet en bovenrand, buiten bewegende delen. De paspennen registreren de delen; tape houdt de voegen dicht.
7. Twee shims per verhoogde selector ondersteunen beide uiteinden. Rij uit = omlaag zonder shims; rij aan = omhoog met shims. Kolom uit = omhoog met shims; kolom aan = omlaag zonder shims. Houd een rail met de hand terwijl de shims worden verwisseld. De verlengde uiteinden steken bij de rijen 4,84 mm buiten het frame, zodat de rail rechtstreeks heen en terug kan worden bewogen.

Deze volgorde is functioneel noodzakelijk: wanneer eerst een buitenframehelft wordt gesloten, kan de tweede rotor van een rij niet meer zijdelings in een reeds gemonteerde capturecomb worden gestoken. Ook de volgorde achterste rij vóór voorste rij voorkomt dat de tweede rij het invoerpad van de eerste comb blokkeert.

De twee combbladen zijn één gezamenlijk onderdeel per selector. Hun verbindingen liggen buiten de draaiende flenzen. Geen aparte lager-, ring-, veer- of terugveercomponent wordt per pin toegevoegd. De drie frameonderdelen splitsen door de lagerassen, waardoor de opgesloten kragen daadwerkelijk gemonteerd kunnen worden. De paspenboringen zijn Ø2,10, de pennen Ø1,80 en 1,80 lang; niets hoeft vastgeperst te worden.

## Bestanden en controlegrens

- `parts/*-print.stl`: individuele delen in de gecontroleerde printoriëntatie.
- `parts/*.stl`: lokale constructiestanden voor assemblage en onafhankelijke botsingscontrole.
- `parts/*.step`: exacte analytische CAD voor de nieuwe parametrische onderdelen. Schroef en pin worden als hun volledige functionele STL geleverd; er is geen misleidende gladde STEP-vervanger voor hun draad.
- `assembly-off.stl`, `assembly-r0-c0.stl`: volledige nominale assemblages, inclusief shims bij de verhoogde selectoren. Dit zijn inspectiemodellen, geen printplaten.
- `parameters.json`, `mesh-validation.json`: nominale parameters, geslotenheid, volumes en hashes.
- De functie `assembly()` zet opgegeven geometrische standen. Haar hoekargumenten zijn poseparameters, geen simulatie van wrijving of van automatisch aangrijpen. De echte vierselectietoestanden en buurvrijloop worden fysiek volgens de testinstructies beproefd.

Test A bevat vier sets van telkens twee rotoren, één enkele capturecomb en twee handassen: strak, nominaal, nominaal, ruim. Radiale passingen zijn respectievelijk 0,12 / 0,15 / 0,20; axiale flensspeling 0,18 / 0,24 / 0,30. Dit zijn samenhangende passingsklassen, geen afzonderlijke schatting van elke printerfout. Test B gebruikt de nominale klasse, acht rotoren, vier inputassen, vier schroeven, vier pinnen, vier selectors, drie frameonderdelen, één handkey en acht gedeelde selector-shims: 36 delen.

De echte print, laaghechting van de dunne hals, conische lagerwrijving, torsie, herhaald aangrijpen, losbreken, terugdrijven onder last en montagegemak blijven fysieke vragen. De vier handmatig benaderde INPUT-assen worden zowel geselecteerd als ongeselecteerd gedraaid; dat toetst de echte rij-/kolomkoppeling, maar kwalificeert geen gemeenschappelijke vierassige aandrijving.
