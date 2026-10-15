# Frontklauwen: keuze, maatvoering en onzekerheid

**16 oktober 2026 — ontwerpberekening, geen fysieke koppelingsuitslag.** De uiteindelijke geometrie staat in [`cad/generate.py`](cad/generate.py). De twee afzonderlijke koppelingshelften bewegen rechtstreeks met de rij omhoog en de kolom omlaag. Deze notitie vergelijkt alleen tanduitvoeringen binnen dat vaste principe.

## De gekozen twee tanden

Beide helften hebben twee tegenoverliggende sectorvormige tanden op een 180°-steek: buitendiameter **3,60 mm**, binnenradius **0,60 mm**, sectorhoek **76°**, tandhoogte **2,40 mm**. De achterste double-D-socket is blind: de dichte kap van 0,72 mm (6,20-mm tandvoet minus 5,48-mm socketdiepte) laat een brede tandvoet toe zonder doorlopende as in het koppelvlak. De onderste 2,16 mm van iedere tand heeft rechte verticale flanken. Over de bovenste **0,24 mm** versmalt de sector van 76° naar **56°**, gelijkmatig aan beide zijden. De passende relatieve stand is 90°, modulo 180°.

De inloop is dus een hoekvormige afschuining, geen overal 0,24-mm-brede kant. De terugligging per flank is `r sin(10°)`: 0,104 mm aan de binnenradius, 0,208 mm bij r=1,20 en 0,313 mm aan de buitenradius. Ook de grootste nominale horizontale toename per 0,12-mm-laag is daarmee circa 0,156 mm; de daadwerkelijke paden blijven bepalend. De centrale vrijruimte verwijdert een nulbrede sectorpunt; de binnenste tip is nog maar `2×0,60×sin(28°)=0,563 mm` breed. Dat kritische binnenstuk moet in de Arachne-paden aanwezig en verbonden blijven; de bredere buitenste flank levert het grootste koppel.

De axiaal gevangen rotorflens blijft Ø4,30 mm en de hals Ø3,20 mm; de kleinere Ø3,60-mm-maat geldt voor het geleide hulslichaam en de tanden. De onafhankelijke controle vond bij de eerdere Ø4,30-mm-tandkop een buurbotsing met toegelaten scheefstand. Het eindontwerp gebruikt daarom deze kleinere kop plus integrale Ø4,00-mm-framegeleidingen rond de hulslichamen. Hun werkbereik moet uit de actuele afzonderlijke botsingscontrole blijken; de tandberekening hieronder veronderstelt coaxiale delen.

De **rechte** zijflanken nemen koppel in beide richtingen op. De afschuining helpt alleen bij lokaal invangen. Bij belasting tijdens alleen topcontact kan zij juist axiale scheidkracht opwekken. Daarom eerst volledig zetten en pas daarna draaien. Bij deselectie eerst input stoppen en torsie ontlasten; een positief teruggetrokken selector voorkomt afhankelijkheid van zwaartekracht, maar heft flankwrijving onder belasting niet op.

## Waarom twee in plaats van drie of vier?

Vergelijking bij dezelfde diameter, ±14° uiteindelijke hoekvrijheid en dezelfde 20° totale tipversmalling. De getoonde breedte is de chord bij gemiddelde flankradius r=1,20 mm; het is een doorsnedeberekening, geen slicerresultaat.

| Tanden per helft | Sectorhoek onder/boven | Tipbreedte bij r=1,20 | Direct volledig insteekbare fases | Maximaal naar dichtstbijzijnde venster zoeken | Hoogte-equivalent bij 3-mm lead als output die hoek indexeert |
|---|---:|---:|---:|---:|---:|
| **2, gekozen** | 76° / 56° | **1,127 mm** | 15,6% | 76° | 0,633 mm |
| 3 | 46° / 26° | 0,540 mm | 23,3% | 46° | 0,383 mm |
| 4 | 31° / 11° | 0,230 mm | 31,1% | 31° | 0,258 mm |

Meer tanden verkorten het fasezoeken, maar laten hier veel minder materiaal over. Vier tanden houden bij de tip minder dan één nominale 0,4-nozzle-lijn over; drie zijn een mogelijk compromis, maar twee geven de duidelijkste eerste fysieke test met brede contactvlakken. Een geheel dakvormige tand kan meer fases door axiale druk proberen te indexeren, maar houdt een FDM-crest en een dode top-op-top-fase, en vergroot de axiale uitloopkracht bij onvolledig zetten. Daarom geen claim van zelfindexering en geen extra dakvariant op de eerste plaat.

De gekozen eindspeling is ±14° rond de passende stand, dus **28° totale hoekspeling**, gelijk aan 0,233 mm schroefbeweging bij 3-mm lead. Dit is alleen de nominale geometrische speling van de tanden; de DD-profielen, draad en geleiding voegen eigen speling toe. De genoemde zoekhoeken gelden voor zoeken in de gunstigste richting. Blind één kant op zoeken kan bijna tweemaal zo ver gaan. De hoogte-equivalenten begrenzen een specifieke indexeerbeweging, niet iedere mogelijke topmeeloop of verkeerde bediening.

## Axiale selectie en tolerantiemarge

De feitelijke paired-comb vangt een rotorflens van **0,72 mm** tussen twee kammen met **0,96 mm vrije tussenruimte**; iedere kam is 0,96 mm dik. Eén rotor kan dus 0,24 mm totaal zweven. Met beide nominale rotoren midden in hun vangruimte ligt de relatieve fase-afstand binnen **±0,24 mm**; de volledige flank-tot-flankvariatie is 0,48 mm. Dat onderscheid voorkomt dubbel tellen van speling.

De conservatieve rekentoets gebruikt **±0,72 mm** totale axiale afwijking: ±0,24 mm gecombineerde gecentreerde vangspeling, ±0,24 mm expliciet gezamenlijk Z-/eindstopbudget en ±0,24 mm extra constructiereserve. De laatste twee zijn **ontwerpbudgetten, geen gemeten printertoleranties**. De toets laat zien wat dit model verdraagt; Test A moet vaststellen welke spelingen werkelijk ontstaan.

| Toestand | Nominale geometrie | Conservatieve grens bij ±0,72 mm |
|---|---:|---:|
| Geen selectie | 3,36 mm vrije afstand tussen tandtoppen | minstens 2,64 mm vrij |
| Alleen rij, +2,40 mm | 0,96 mm vrije tandtopafstand | minstens **0,24 mm vrij** |
| Alleen kolom, −2,40 mm | 0,96 mm vrije tandtopafstand | minstens **0,24 mm vrij** |
| Rij én kolom | 1,44 mm tandpenetratie | 0,72–2,16 mm penetratie |
| Rechte flank op rechte flank in 11 | `1,44 − 2×0,24 = 0,96 mm` | minstens **0,24 mm** |
| Tandtop tot tegenoverliggende tandwortel in 11 | `2,40 − 1,44 = 0,96 mm` | minstens **0,24 mm** |

Beide tipafschuiningen moeten worden afgetrokken. De onafhankelijke review corrigeerde een eerdere tussenberekening die er slechts één aftrok; bovenstaande eindmaten en marges rekenen beide correct mee. De controle betreft ideale coaxiale geometrie; scheefstand, vervorming, ruwe flanken en onvolledig gezette selectoren blijven fysieke vragen.

De koppeling gedraagt zich bij de vier eindstanden als mechanische AND. Tijdens een continue slag kan zij eerder aanraken: met genormaliseerde rij-/kolomslag r en c is de tipafstand `3,36 − 2,40(r+c)`. Contact begint bij **r+c=1,40**. Staat één selector al volledig in, dan begint aanraken na 40% van de tweede slag; nominale recht-op-recht overlap begint na 60%. De geometrie garandeert dus geen digitale uitschakeling voor alle tussenstanden. Stop de input tijdens selecteren, adreswisselen en terugtrekken.

## Faseblokkering blijft een echte testvraag

Een afschuining maakt top-op-top niet onmogelijk. Een zeer vrije E-295-schroef kan bovendien door tandtopwrijving met de input meedraaien zonder dat de relatieve fase verbetert. Alleen een bewegende pin bewijst daarom geen aangrijping: **de selector moet zijn eindstand bereiken en de koppelhelften moeten volledig gezet zijn**.

Bij meerdere geselecteerde kruispunten kan één verkeerd gefaseerd paar de gemeenschappelijke stijve staaf tegenhouden. Test B heeft afzonderlijk bereikbare inputassen; die mogen om beurten voorzichtig naar een passende fase worden gedraaid terwijl de echte rij-/kolomstaven actief blijven. Dit toetst het gevraagde mechanisme. Het bewijst geen automatische gelijktijdige invang van willekeurige outputfases op één star gekoppelde globale aandrijfbus: daarvoor hoeft geen gezamenlijke insteekhoek te bestaan. Outputindexering kan de geselecteerde pinhoogte veranderen; topmeeloop, blokkering en indexeringsverplaatsing worden apart genoteerd. Er worden geen veren of andere selectiearchitecturen toegevoegd om een negatief resultaat te verbergen.

## Belasting en korte fysieke controle

Er is geen gemeten benodigd schroefkoppel of toelaatbaar PLA-koppel. Als rekenvoorbeeld, niet als belastingsvoorschrift: T=2 Nmm en uniforme flankdruk over beide tanden bij gemiddelde radius 1,20 mm geeft 0,833 N per tand. Het nominale rechte contactvlak is 1,20×0,96=1,152 mm², circa 0,72 MPa gemiddelde druk. Bij 0,24 mm resterende rechte overlap wordt dat circa 2,89 MPa; draagt maar één tand, dan verdubbelen deze waarden. Lokale piekdruk en laaghechting zijn onbekend. De bestaande d=1,4-mm-schroefkern heeft bij hetzelfde koppel al circa 3,71 MPa ideale cirkeltorsiespanning. Een brede tand bewijst daarom niet de sterkte van de hele krachtroute.

Voor [Test A](../../../owner-print-tests/2026-10-16-two-half-clutch-fit/test.md): vergelijk de gelabelde spelingen en identieke nominale exemplaren; observeer insteken, 0/30/60/90° relatieve fases, zacht zoeken, volledige zetting, beide draairichtingen, positieve ontkoppeling en vrij roteren in de axiale vangruimte. De daadwerkelijke plaatvarianten staan in het testmanifest; de vergelijking met drie/vier tanden hierboven vraagt geen extra printserie.

Voor [Test B](../../../owner-print-tests/2026-10-16-two-half-clutch-matrix/test.md): controleer per cel 00/10/01/11, beide inschakelvolgordes en beide enkele-deselectieroutes; alle 16 binaire matrixcommando's en bewust verschillende schroeffases bij meerdere geselecteerde cellen. De gekoppelde set hoort het cartesisch product van geselecteerde rijen en kolommen te zijn. Een diagonaal vraagt twee passes. Observeer pinhoogte én selectorzetting en noteer bij iedere bediende input wat de drie buren doen. Geen tang, boormachine of doorgedrukte blokkade.

De gekozen geometrie en marges zijn berekend. De succesvolle E-295-draadpassing is eigenaarbewijs voor die draad; zij bewijst geen fysiek aangrijpen, lossen, wrijving, houdkracht of levensduur van deze koppeling. Die uitkomsten blijven onbekend tot de fysieke tests zijn uitgevoerd.
