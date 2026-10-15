# Hybride schroefaandrijving: tijd, schaal en kosten

Dit deel van [E-295](../../../../06-experiments/E-295-compact-screw-drive-development.md) vergelijkt **dezelfde draaiende schroeven en niet-meedraaiende holle staafjes**. Het introduceert geen andere hoogtedrager. De uitkomsten zijn reproduceerbare berekeningen met expliciete, **nog niet gemeten** snelheid-, koppel-, fout- en kostenparameters. Geen snelheid, levensduur of productieopbrengst hieronder is fysiek aangetoond.

## Wat deze vergelijking wel beslist

Een enkele onderliggende draaikop houdt de onderdelen per pin eenvoudig en is een geschikte eerste demonstrator. Diezelfde kop kan een kleine wijziging bedienen, maar verandert 6.400 willekeurige hoogtes niet in 30 seconden. Meerdere onafhankelijke koppen helpen alleen voor zover het werk werkelijk over hun bereik verdeeld is. Een traverserende bank met een gemeenschappelijke draaibus en een beperkt aantal selectieve koppen kan meer parallelisme leveren zonder 6.400 afzonderlijke koppelingen aan de pinnen te monteren; zijn lokale selectie en betrouwbare aangrijping zijn nog belangrijke mechanische onzekerheden.

Een gedeelde reset plus lokale kop is zinvol bij **voorbereiden van een nieuw speelveld**, mits de reset per schroef veilig kan slippen. Reset standaard uitvoeren vóór iedere kleine wijziging zou de speelervaring verslechteren. Het aantal onderdelen dat aan iedere pin hangt is een belangrijker eerste keuzepunt dan alleen het aantal motoren.

Het historische [A-007](../../../../04-architecture-candidates/A-007-scanning-screw-column-matrix.md) gebruikte een dichte update als afwijzingscriterium. Dat resultaat blijft een historische vergelijking. De huidige opdracht staat langere voorbereiding en snelle beperkte wijzigingen toe: daarom wordt die eerdere doorslaggevende tijdgrens hier niet als uitsluiting van alle schroefscanners overgenomen.

## Reproduceerbare aannames

Broncode: [hybrid_timing_cost.py](../hybrid_timing_cost.py). Volledige getallen en tussenresultaten: [hybrid_results.json](../hybrid_results.json).

```sh
python3 tools/curated-experiment-checks/E-295/hybrid_timing_cost.py
python3 tools/curated-experiment-checks/E-295/hybrid_timing_cost.py --json
```

| Parameter | Planningswaarde; allemaal aannames tenzij anders vermeld |
|---|---|
| Raster | 80 × 80, pitch 5,08 mm; 406,4 × 406,4 mm totaal; 16 × 16 D&D-vakken |
| Strikt binnen 400 mm | 78 × 78 = 6.084 pinnen, 396,24 mm; onvolledige laatste D&D-vakken. 75 × 75 = 381 mm geeft 15 volledige vakken. Resolutie hoeft hiervoor niet omlaag. |
| Verplaatsing | 0–40 mm; neutraal fysiek op 20 mm |
| Lead | 3 mm/omwenteling, uit recente/historische CAD; geen snelheidmeting |
| Draaikop | 600 rpm; 3.000 rpm/s versnellen en vertragen |
| XY | 150 mm/s, 1.500 mm/s²; stilstand bij iedere aangedreven pin |
| Aankoppelen en losnemen | 0,75 s: naderen 0,15; fase zoeken 0,20; zitting 0,10; terugtrekken 0,15; besturing/settling 0,15 |
| Gemiste aankoppeling | Aangenomen 2%; mislukte poging 0,60 s. Fout wordt **voor draaien** gedetecteerd. Geen gemeten betrouwbaarheid. |
| Homing | 120 rpm, maximale neerwaartse slag 40 mm plus 0,50 s overloop; iedere schroef heeft veilige lokale slip in de bedienende kop/contact |
| Loopvolgorde | Deterministische slingerroute langs adressen; geen perfecte route-optimalisatie |

De scriptfunctie `rest_to_rest` gebruikt een driehoekig of trapeziumvormig snelheidsprofiel. Voor lineaire of hoekafstand `s`, snelheid `v` en versnelling `a` geldt `t = 2√(s/a)` voor korte bewegingen, anders `t = s/v + v/a`. Daardoor kost 5 mm draaien bij de planningsinstelling ongeveer **0,365 s**, niet alleen de 0,167 s uit constante maximumsnelheid. Een aangrenzende XY-stap van 5,08 mm kost ongeveer 0,116 s. Verplaatsing, fase zoeken, aandrijven en terugtrekken zijn serieel opgeteld; verplaatsing begint pas wanneer de kop vrij is.

De 4- en 16-kopsberekeningen verdelen het oppervlak in onafhankelijke vaste vierkante gebieden. Elk gebied heeft eigen XY, nadering en rotatie. De eindtijd is de **traagste kop**, niet simpelweg totaaltijd gedeeld door aantal koppen. Startpunt is het eerste rasteradres in ieder gebied; terugkeer na afloop is niet nodig en niet geteld. De motorlichamen kunnen breder zijn dan hun bereikgrens: botsingsvrije montage, verticaal versprongen lichamen of overdracht onder het koppelvlak moeten nog ontworpen worden. Deze getallen bewijzen geen verpakkingsoplossing voor 16 koppen en gelden niet automatisch voor meerdere koppen op één gemeenschappelijke XY-wagen.

Dit zijn mechanische scenario-totalen inclusief de genoemde settling en gemiste-koppelingstoeslag. Kaartvoorbereiding, eventueel verplaatsen van miniaturen, onbekende storingsafhandeling en een speelklare eindcontrole hebben geen tijdmodel en mogen niet als bewezen nul worden gelezen. De koppelpogingen zijn bovendien onafhankelijk verondersteld; systematische verkeerde uitlijning kan een hele bank raken en wordt niet door de retry-formule opgelost. De losse voorbeelden in [xy-drive.md](xy-drive.md) gebruiken andere expliciete acceleratie-/XY-aannames; deze scriptinstellingen zijn de gemeenschappelijke basis van de tabellen hier.

## Volledige scène, lokale wijziging en neutraal voorbereiden

| Taak | Veranderde pinnen | 1 XY-kop | 4 onafhankelijke gebieden | 16 onafhankelijke gebieden |
|---|---:|---:|---:|---:|
| Twee willekeurige scènes, hoogtes elk 0–40 mm | 6.400; gemiddelde stap 13,2 mm | 160,8 min | 40,6 min | 10,2 min |
| Bekende willekeurige scène terug naar 20 mm | 6.400; gemiddelde stap 10,0 mm | 149,6 min | 37,6 min | 9,5 min |
| Vanuit neutraal één heuvel, diameter circa 102 mm, hoogte max. 15 mm | 305 | 375,8 s | 375,8 s | 106,7 s |
| 25 verspreide lokale wijzigingen, elk ±2–10 mm | 25 | 51,8 s | 19,4 s | 8,0 s |
| 25 aaneengesloten wijzigingen, 5 × 5 pinnen | 25 | 32,1 s | 32,1 s | 32,1 s |
| 100 aaneengesloten wijzigingen, 10 × 10 pinnen | 100 | 126,8 s | 126,8 s | 126,8 s |

Een 5 × 5 groep is precies één D&D-vak bij 5,08 mm pitch. De geclusterde voorbeelden liggen bewust geheel binnen één bedieningsgebied: extra vaste koppen helpen daar niet. De heuvel ligt binnen één gebied van het 4-kopssysteem, maar over vier gebieden van het 16-kopssysteem. De lage tijd van een verspreide wijziging met 16 koppen is dus geen algemene belofte voor alle wijzigingen van 25 pinnen.

Er is een eenvoudige ondergrens: zelfs zonder XY en zonder schroefrotatie kosten 6.400 succesvolle transacties van 0,75 s **80 minuten gedeeld door het effectief gebruikte aantal koppen**. Bij deze transactietijd zijn ten minste 160 gelijktijdig nuttige koppen nodig om alleen aankoppelen binnen 30 s te krijgen. Hogere schroefsnelheid lost die overhead niet op. Dit weerlegt een specifieke 30-s-belofte voor een gestopte scanner, niet het schroefprincipe en ook niet de bruikbaarheid van lokale updates.

De gevoeligheid staat volledig in JSON: snel 1.200 rpm/0,45 s koppelen, planning 600 rpm/0,75 s, voorzichtig 300 rpm/1,50 s. Ook 1,5 en 2 mm lead worden doorgerekend. Alle varianten blijven aannames; vooral 1.200 rpm aan een lange dunne FDM-schroef moet eerst op slingeren, wrijving en torsie worden getest. Kortere lead vertraagt de rotatieterm maar kan de belasting/retentie verbeteren; de koppeltijd blijft gelijk. De drukproef wordt niet om een timingberekening op 3 mm vastgezet.

| Gevoeligheid voor de volledige willekeurige scène | Eén kop | Vier gebieden |
|---|---:|---:|
| Snelle maar onbewezen set: 1.200 rpm, 0,45 s transactie, 6.000 rpm/s en 3.000 mm/s² | 100,8 min | 25,4 min |
| Planningsset | 160,8 min | 40,6 min |
| Voorzichtige set: 300 rpm, 1,50 s transactie, 1.500 rpm/s en 750 mm/s² | 293,2 min | 74,0 min |
| Alleen lead naar 2 mm; overige planningswaarden gelijk | 184,5 min | 46,7 min |
| Alleen lead naar 1,5 mm; overige planningswaarden gelijk | 208,1 min | 52,7 min |

## Gemeenschappelijke draaibus met herbruikbare selectieve koppen

De [gedeelde-aandrijvingsstudie](shared-global-drive.md) werkt de mechanismen verder uit. De hier berekende variant heeft `k` naast elkaar liggende koppen die onder een rij bewegen, een gemeenschappelijke draaibus en **selectie/losnemen per herbruikbare kop**. De pin houdt zijn eenvoudige integrale aandrijfeinde. Er zijn `k` selectorassemblages, niet 6.400 residentiële koppelingen. Breed uitlopende motoren/selectoren moeten onder het smalle koppelvlak worden gerangschikt; het script kwalificeert deze verpakking niet.

Iedere geadresseerde groep heeft eerst een opwaartse en daarna een neerwaartse deelpassage wanneer beide richtingen nodig zijn. **Iedere richting krijgt zijn eigen aankoppel-/fasezoektransactie** wanneer axiaal aankoppelen ook de selectie verzorgt. Koppen die omlaag moeten mogen tijdens de opwaartse passage nog niet gekoppeld zijn. Bij continu doordraaien bepaalt per richting de grootste stap de draaitijd; de andere koppen moeten op hun eigen doelhoek veilig losnemen. Een gemeenschappelijke bus biedt dus geen gratis individuele instelling. De berekening telt 0,15 s voor richtingwissel en 0,05 s vrijgavetijd per gebruikte richting. Ook worden gezamenlijk gewachte koppelpogingen geteld: bij 80 gelijktijdige contacten en aangenomen 2% onafhankelijke missers wordt vaker ergens een koppeling gemist dan bij één kop. De verwachte extra rondes zijn `Σ[1−(1−p^r)^k]`, geen aangenomen constant nul.

De onderstaande snelle variant is slechts een **voorwaardelijke ondergrens met gecontroleerd losnemen tijdens draaien**. Een vrijgaveduur van 0,05 s op 600 rpm komt bij 3 mm lead al overeen met 1,5 mm beweging. De totale aangenomen terugtrekduur van 0,15 s vertegenwoordigt zelfs 4,5 mm als de volle koppeling tot het einde blijft aandrijven. Dat is geen kleine automatisch verwaarloosbare fout. Voorspellend vrijgeven vraagt een reproduceerbaar moment waarop de krachtoverdracht stopt; de deels uitgetrokken zeskant mag niet beschadigen. Een aparte koppeling op iedere herbruikbare kop kan dit veranderen, maar voegt `k` nauwkeurige modules toe en zit niet verstopt in de pin.

| Taak | Bank van 8 koppen | Bank van 16 | Bank van 80 |
|---|---:|---:|---:|
| Twee willekeurige volledige scènes | 54,6 min | 31,3 min | 7,0 min |
| Bekende willekeurige scène naar neutraal | 48,1 min | 27,0 min | 5,7 min |
| Neutraal naar één heuvel, 305 pinnen | 85,4 s | 60,9 s | 29,6 s |
| 25 verspreide wijzigingen | 53,4 s | 51,1 s | 33,6 s |
| 25 wijzigingen, één D&D-vak | 14,5 s | 14,5 s | 14,5 s |
| 100 wijzigingen, vier D&D-vakken | 54,9 s | 29,7 s | 29,7 s |

De tweede, mechanisch duidelijkere variant **stopt de gemeenschappelijke bus op iedere verschillende doelhoogte, trekt de afgewerkte koppen terug en start opnieuw voor de overige koppen**. Iedere stop krijgt versnellen/vertragen, 0,15 s terugtrekken en 0,05 s settling. Exact gelijke doelen mogen samen los; er wordt geen gratis afronding naar hoogteklassen toegepast. Dat geeft:

| Taak met gestopte vrijgave | Bank 8 | Bank 16 | Bank 80 |
|---|---:|---:|---:|
| Twee willekeurige volledige scènes | 83,6 min | 64,0 min | 38,1 min |
| Neutraal naar de heuvel | 145,7 s | 121,2 s | 73,9 s |
| 25 verspreide wijzigingen | 53,4 s | 51,5 s | 34,0 s |
| 25 wijzigingen, één D&D-vak | 19,5 s | 19,5 s | 19,5 s |
| 100 wijzigingen, vier D&D-vakken | 76,2 s | 55,4 s | 55,4 s |

Dit is een aanzienlijk verschil dat een fysieke selectieproef moet oplossen voordat een snelle bankarchitectuur wordt gekozen. Een terras met enkele gelijke hoogtes profiteert meer van de gestopte bank dan een willekeurig veld met vrijwel allemaal verschillende doelen. Ook na vrijgave moet de schroef onder last blijven staan; passieve retentie en werkelijk vrije buren zijn voorwaarden, geen gevolg van een correcte timer.

**Dit zijn voorwaardelijke procestijden, geen uitgewerkte bouwbelofte.** De grootste ontbrekende voorwaarden zijn: alle actieve koppen aantoonbaar gezeten; tijdens normaal draaien geen slip; iedere kop op tijd los; de niet-geselecteerde koppen werkelijk vrij. Een zeskant die tijdens fase zoeken al een schroef draait geeft nog geen gemeenschappelijke nulhoek. Zonder afzonderlijke zittingsinformatie kan een willekeurige zeshoekfase bij 3 mm lead tot ongeveer 0,5 mm ongekende beweging geven. Dat kan in deze vroege fase aanvaardbare hoogtedrift zijn, maar een niet-zittende kop of doorlopend slippen is geen kleine drift en mag niet als succesvolle selectie worden gerapporteerd. Een handmatig gecontroleerde 2- of 4-kopsproef kan dit eerst toetsen; uitgebreide sensoren zijn nu niet nodig.

Een vlakke wrijvingscup vermijdt hoekfase, maar de aandrukkracht kan groot worden: bij aangenomen 2 mNm, μ = 0,3 en effectieve straal 1,36 mm is circa 4,9 N per cup nodig, ongeveer 390 N voor 80 cups. Dat krachtpad moet naar de dragende basis en schroefkraag lopen. Het aantal motoren verlagen zonder deze krachten en de 80 selectoren te tellen is geen systeemvereenvoudiging.

## Reset, groepsbeweging en hybride gebruik

Een gemeenschappelijke relatieve beweging behoudt hoogteverschillen. Zij maakt een onbekend terrein **niet vanzelf vlak**. Vlak initialiseren vraagt een fysiek onderreferentiepunt voor elke pin, een begrensde slag en lokale ontkoppeling/slip zodra die pin aankomt. Eén centrale motorkoppelbegrenzer kan de reeds gestopte pinnen niet individueel beschermen terwijl andere nog bewegen. Een schroef abrupt tegen een blind boveneinde laten vastlopen is geen geschikte onderstop. De stop moet via het geleid staafje en de basis dragen, vóór verlies van draadengagement of botsing; links-/rechtsom blijven beschikbaar.

De volgende aparte berekening begint met onbekende hoogtes: maximaal 40 mm omlaag op 120 rpm, 0,5 s overloop, daarna 20 mm omhoog op 600 rpm terwijl dezelfde groep gekoppeld blijft. Hij veronderstelt een reeds bewezen venster `hoogste loopkoppel < laagste slipkoppel < laagste schadekoppel`.

| Resetwijze | Gelijktijdige contacten | Tijd onbekend → verhoogd neutraal |
|---|---:|---:|
| Eén kop serieel | 1 | 16,2 uur |
| Bank | 8 | 125,5 min |
| Bank | 16 | 64,5 min |
| Eén volledige rij tegelijk | 80 | 12,8 min |
| Hele veld tegelijk | 6.400 | 10,2 s, uitsluitend kinematische procestijd |

De veldwijde 10 s is geen geselecteerde architectuur. Bij een illustratief, **niet gemeten** koppel van 2 mNm per schroef vraagt gelijktijdig draaien van 6.400 schroeven circa **161 W mechanisch op 120 rpm** en circa 804 W op 600 rpm, vóór transmissieverlies. Bij een band op 2,2 mm wielstraal is de opgetelde tangentiële contactkracht circa 5,8 kN, verdeeld over de contacten. Volledige slip tijdens homing produceert plaatselijke warmte. Een rij van 80 beperkt gelijktijdige belasting en repliceert 80 contact-/slipmodules op een verplaatsbare bank in plaats van 6.400 in het veld. Een harde tandwielbus zonder die lokale ontkoppeling kan niet veilig onbekende gemengde hoogtes tegen een stop draaien.

De scriptberekening van 16,2 uur voor één kop is een conservatieve **onbekende** beginstand met maximale neerwaartse sweep voor iedere pin. Zij is geen voorspelling voor dagelijks spelen vanuit bekende hoogtes. Bekende pinnen kunnen direct naar doel bewegen; een tijdens assemblage mechanisch ingesteld nulpunt voorkomt die eerste automatische sweep. Een gezette neutrale tafel hoeft niet vóór ieder gebruik opnieuw volledig te homen.

Concrete hybride keuzes:

| Combinatie | Wanneer zinvol | Wat nog aangetoond moet worden |
|---|---|---|
| Eén XY-kop; neutraal bij assemblage handmatig ingesteld | Kleinste hardware en gerichte wijzigingen; eerste 4-pin demonstratie | Positieve koppeling, reverseren, passieve laststeun en buur-isolatie |
| 4 onafhankelijke XY-gebieden | Meerdere verspreide gebeurtenissen; geen reductie van het aantal pinonderdelen | Botsingsvrije bereikgrenzen; werkverdeling; gemeten hele transactie |
| Verplaatsbare resetbank + XY | Voorbereiding na grote, onbekende of verloren toestand; lokaal spelen met eenvoudige kop | Slipvenster en echte onderstop; snel wisselen van bank naar vrije XY-kop |
| Kleine gemeenschappelijke bank met 4–8 selectieve koppen + één XY-kop | Groepen/heuvel/plateau in bulk, verspreide details lokaal | Individueel stop-/selectiemechanisme op bank; aankoppelfase; ruimte onder 5,08-mm raster |
| Veldwijde reset + XY | Alleen aantrekkelijk als zeer snelle voorbereiding opweegt tegen duizenden contacten | Complete kracht-, thermische, lokale slip- en serviceoplossing; nog geen minimale prototypekeuze |

Een rijresetbank van 80 plus één XY-kop heeft in dit model ongeveer **19 minuten** nodig van een onbekende scène naar neutraal plus de beschreven heuvel (12,8 min + 6,3 min). Als de tafel al neutraal staat, valt de volledige reset weg. Een gemeenschappelijk bestuurde 80-kopsbank zou dezelfde heuvel in ongeveer 30 s instellen met bewezen voorspellende vrijgave, of ongeveer 74 s met de gestopte bus; beide kopen dat met 80 selectiekanalen. Dit is een vergelijking, geen aanbeveling om nu een 80-kopsbank te bouwen. De kleine 4–8-kopsvariant is hoogstens een volgende schaalstap die de eigenaar na een geslaagde 2-/4-kopsproef kan kiezen.

Grove groepsbeweging kan ook zonder homing nuttig zijn. Voor gewenste stappen `d_i` kan een gedeelde groepsstap `b` gevolgd worden door individuele reststappen `d_i−b`. De **mediaan** minimaliseert totale absolute draaislag, maar de **meest voorkomende stap** minimaliseert het aantal nabezochte pinnen wanneer koppelen de kosten bepaalt. Voor een rij waarvan 60 pinnen +10 mm nodig hebben en 20 gelijk moeten blijven, kan +10 mm groepsbeweging plus 20 correcties minder transacties vragen dan 60 losse bezoeken. Bij slechts 20 veranderde pinnen maakt dezelfde groepsbeweging juist 60 correcties nodig. Beide richtingen moeten binnen 0–40 mm blijven; tijdelijke ongewenste terreinhoogtes kunnen geplaatste miniaturen verstoren. Daarom zijn groepsstappen vooral een voorbereidingstechniek of een expliciet gewenste plateauverplaatsing.

## Kosten, onderdelen en assemblage

Alle bedragen zijn **ontwerpbudgetten in USD, geen offertes**. De scriptwaarden maken de vergelijking reproduceerbaar; ze bewijzen geen haalbare aankoopprijs. Belastingen, verzending, gereedschap en arbeid zijn niet meegerekend. Extra lagering, schroefhouders, bedrading en afscherming buiten onderstaande posten kunnen het budget verhogen. De oude $500-doelwaarde wordt hier niet gebruikt om een ongeteste schroefarchitectuur af te wijzen.

| Herhaling | Eén XY-kop | 4 onafhankelijke XY-koppen | Gemeenschappelijke bank van k koppen |
|---|---:|---:|---:|
| Schroef + holle pin | 6.400 paren | 6.400 paren | 6.400 paren |
| Draag-/vangpositie en geleiding | 6.400 posities, in gedeelde platen te integreren | Gelijk | Gelijk |
| Residentiële individuele koppeling aan iedere pin | Geen; integrale drive-tip/kraag | Geen | Geen, als de selector op de bank zit |
| Nauwkeurige herbruikbare kopassemblage | 1 | 4 | k |
| Onafhankelijke XY + nadering + rotatie-aandrijvingen | 4 | 16 | Typisch 4 gemeenschappelijke bewegings-/busassen + k selectoren; selector kan solenoïde/servo zijn, blijft hardware |
| Aansluiting per pin | Geen elektrische draad | Geen | Geen |

Materiaalprojectie voor volledige lengte: 4,4-mm vierkante buis met 3,52-mm vierkante holte heeft circa 6,97 mm² doorsnede; bij 55 mm ongeveer 383 mm³. Een ruwe 50-mm schroefprojectie voegt circa 215 mm³ toe. **0,60 cm³ per paar is dus een geometrische schatting, geen gemeten of geslicede productievariant.** Volledige 40-mm slag, stabiliteit en draagkracht zijn nog niet bewezen. Bij 1,24 g/cm³, 15–45% extra voor toppen/kragen/printsteunen en aangenomen 85% bruikbare opbrengst volgt circa 6,4–8,1 kg filament, ongeveer $129–284 bij $20–35/kg. De feitelijke test-STL heeft een eigen slicerresultaat en is geen volledige productierod.

De vergelijkingsbegroting voegt $80–220 voor gedeeld frame, geleidings-/vangplaten en bevestiging toe en $40–100 voor gemeenschappelijke besturing/voeding. Per onafhankelijke XY-kop: vier motoren $40–80 totaal; rail/band/motion $40–100; spindel/koppeling $20–60; vier drivers $16–32. Voor een gemeenschappelijke bank: motion/bus $130–300; iedere selector $6–18; ieder cup/lager/slipmodule $4–12. Geautomatiseerde foutdetectie is niet begroot; de bank wordt alleen als voorwaardelijk concept vergeleken.

| Volledige veldmaterialen + gekozen aandrijving | Rekenkundige ontwerprange |
|---|---:|
| Eén onafhankelijke XY-kop | $365–876 |
| Vier onafhankelijke XY-koppen | $713–1.692 |
| Zestien onafhankelijke XY-koppen | $2.105–4.956 |
| Bank van 8 selectieve koppen | $459–1.144 |
| Bank van 16 | $539–1.384 |
| Bank van 80 | $1.179–3.304 |

Een extra XY-detailkop bij een bank voegt indicatief $116–272 toe. Combinaties moeten dus worden opgeteld; een globale module is geen gratis voorziening. Een gemeenschappelijke XY-wagen met verscheidene rotoren kan goedkoper zijn dan onafhankelijke gebieden, maar heeft een andere bereik-/wachttijdplanning en is niet door de onafhankelijke-kopstabel gekwalificeerd.

Iedere **$0,10 extra per pin voegt $640** toe. Iedere **10 s extra montage per pin voegt 17,8 uur** toe. Zelfs 20/45/90 s per compleet schroef-pin-paar betekent 35,6/80/160 uur voor 6.400 paren, exclusief inspectie, frames en reparaties. Residentiële miniatuurkoppelingen, losse veertjes of kogellagers moeten daarom aantoonbaar waarde toevoegen. Gedeelde steunplaten en integrale schroefkragen zijn aantrekkelijk zolang ze vervanging van één defect paar niet onmogelijk maken.

Alleen 3,84 liter netto paarvolume extruderen kost bij 5–12 mm³/s al 89–213 uur; dit is een **volumegrens**, geen printtijdvoorspelling. Kleine helixen, minimumlaagtijd, wisselingen, bracing en uitval maken de machinebezetting groter. De effectieve serietijd moet later uit een echte batch-slicer en fysieke opbrengst komen. De huidige kleine tolerantietest dient eerst vast te stellen welke geometrie het produceren waard is.

## Kleinste beslissende bewijs en stopconditie

1. Print eerst de compacte passingstest. Noteer per identiek exemplaar soepelheid, omkeerbaarheid en schade; het beste brede 0,20-mm paar voorspelt niet automatisch de beste compacte passing.
2. Gebruik vier aangrenzende pinnen en één handmatige onderkop om echt op/neer, koppelen/losnemen en niet-bewegen van buren te toetsen. Meet daarna tijd per volledige transactie en bruikbaar koppel; een motorupgrade is pas nuttig als de handmatige koppeling betrouwbaar werkt.
3. Kies daarna **één** aanvullende proef indien de eigenaar een aandrijfrichting wil kiezen: twee herbruikbare selectieve koppen op één bus, of een kleine rijreset met slip. De selectieproef moet doel A laten draaien terwijl B stilstaat, dan omkeren en rollen wisselen. De resetproef begint bewust op verschillende hoogtes en moet de vroeg aangekomen pin onbeschadigd laten wachten terwijl de andere doorgaat.
4. Voor een reset is een gemeten onderscheid tussen loopkoppel, veilige slip en beschadiging doorslaggevend; het is voldoende eerst onder een gekozen conservatieve proeflast te werken. Een gekocht precisiekoppelmeettoestel of volledige sensorarchitectuur is geen voorwaarde voor de kleine handproef.

Deze vergelijking stopt bij de reproduceerbare scenario's en het advies voor de reeds voorbereide kleine proef. Ze start geen vervolgcampagne. De eigenaar beslist na fysieke resultaten of meer koppen, een selectieve bank of resetondersteuning de gewenste speelervaring het beste dient.
