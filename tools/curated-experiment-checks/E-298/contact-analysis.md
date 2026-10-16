# Onafhankelijke contactanalyse — twee punten en twee holtes

Dit is een **ideale geometrische en quasistatische berekening**, geen fysieke uitslag. E-297 blijft ongewijzigd. De nieuwe helften behouden zijn twee afzonderlijke axiale bewegingen, dubbele D-geleiding, flens, 5,08-mm raster, tandhoogte 2,40 mm en twee tegenoverliggende tanden. Iedere brede tand krijgt een in twee richtingen toelopende kroon: zowel radiaal als omtreksgewijs loopt zij uit naar een klein vlakje van ongeveer **0,30 × 0,30 mm** bij straal 1,20 mm. Het is dus geen lange messnede. Tussen de tanden blijven twee open complementaire holtes over. Bij 90° relatieve fase vallen de punten van beide identieke helften in elkaars holtes; speling voorkomt dat een nauwkeurig negatief van iedere kroon vereist is.

## Drie gerichte varianten

| Variant | Kroonhoogte | Piekverschuiving | Helling bij r=1,20 mm | Nominale rechte flankoverlap |
|---|---:|---:|---:|---:|
| A — minder lange kroon | 0,48 mm | 0° | 36,62° / 36,62° | 0,48 mm |
| B — steilere kroon | 0,60 mm | 0° | 42,89° / 42,89° | 0,24 mm |
| C — kleine asymmetrie | 0,60 mm | +12° op beide punten | 33,77° / 56,67° | 0,24 mm |

Beide punten per helft blijven exact 180° uit elkaar. De kroonvoet beslaat 76° en straal 0,60–1,80 mm. De drie varianten veranderen alleen de kroon; de holtes ontstaan tussen de tegenoverliggende punten. De brede rechte wortelflanken blijven in beide draairichtingen beschikbaar. De scherpere punt concentreert echter juist de eerste contactbelasting: bredere wortels bewijzen geen puntsterkte.

De oorspronkelijke 0,16-mm kroon verloor meerdere bovenste lagen in de echte slicerpaden. Daarom is de uiteindelijke CAD-top vergroot naar 0,30 mm. Ook die is kleiner dan een 0,4-mm nozzle. **0,30 mm is geen gegarandeerd fysiek puntformaat.** De slicer kan de top overslaan, afronden of breder afzetten. De werkelijke laatste geëxtrudeerde laag en de eerste fysieke print bepalen de effectieve puntbreedte. Een wiskundig nulvlak zou deze productiegrens alleen verbergen. De printanalyse moet de bewaarde kroonlagen en hun lijnbreedten controleren.

## Contactenveloppe, inclusief punt-op-punt

Voor twee identieke, tegenover elkaar gekeerde helften is de benodigde afstand tussen hun tandwortelvlakken:

`D(φ) = max over r,θ [h(r,θ) + h(r,φ−θ)]`.

Het minteken komt van het omklappen van de bovenste helft. Bij deze ideale lineaire kroon is elke omtrekshoogte maximaal op r=1,20 mm; de maximale driedimensionale hoogte kan daarom op die straal berekend worden. De gegenereerde CAD-loft interpoleert corresponderende polygoonpunten langs rechte 3D-lijnen, niet in cilindrische coördinaten; vooral radiale krimp en hoekverdraaiing maken de onderstaande ideale kromme een benadering. De echte facetten worden apart geometrisch gecontroleerd. Deze onafhankelijke formule is geen vervanging voor de STEP/mesh-controle.

[`contact_analysis.py`](contact_analysis.py) bemonstert θ met 0,025° en φ met 0,25°. De [resultaten](contact-analysis.json) en [grafiek](contact-envelope.svg) tonen voor alle drie varianten:

- D ligt tussen 2,40 en 4,80 mm.
- Buiten de maximale topplateaus bestaan in dit ideale model geen extra lokale vallen voordat de passende fase bereikt wordt. De open holtes introduceren dus geen extra horizontale vastlooppassage in deze bemonsterde ideale geometrie.
- Volledige eindstand vraagt D ≤ 3,36 mm. Het volledige insteekvenster ligt tussen 76 en 104° per periode van 180°; de grens zelf is flankcontact, geen vrije speling. In de eindige meshbemonstering zijn 76,25–103,75° volledig vrij. De wortelflanken staan pas vrij als dat venster bereikt wordt.
- De 0,30-mm omtrekstop beslaat 14,32°. Twee toppen overlappen in een **28,65° breed topcontactplateau**: bij A/B φ = 0° ± 14,32°; bij C φ = 24° ± 14,32°, steeds modulo 180°. Axiale druk alleen levert daar geen bepaalde draairichting. Gedrukte bredere toppen kunnen het plateau vergroten.

Een tweede, onafhankelijke controle gebruikt de **werkelijke STL-driehoeken**: [`mesh_contact_envelope.py`](mesh_contact_envelope.py) berekent verticale snijhoogten op 61 radii met 0,02-mm stappen en 720 hoeken met 0,25° stappen, en vervolgens de contactafstand voor 720 fases. De [meshresultaten](mesh-contact-envelope.json) bevatten de bronhashes en vinden ook geen extra bemonsterde lokale vallen buiten het topplateau. Dit is eindige geometrische bemonstering: geen contactkracht-, vervormings- of wrijvingsbewijs.

De asymmetrie maakt beide ontsnappingshellingen verschillend en verschuift de probleemfase; zij verwijdert die fase niet. Zelfs bij ideale nulbrede punten heeft een periodieke scheidingsfunctie een maximum. Bij exact contact op dat maximum kan de contactnormaalkegel een zuiver axiale reactiekracht toelaten. **Er is geen bewijs dat een starre, passieve, identieke tweepuntskoppeling zichzelf uit werkelijk iedere beginfase zet.** Een kleine externe tik of bewuste hoekcorrectie kan een diagnostische handeling zijn, maar telt niet als geslaagde zelfuitlijning zonder fasehulp.

## Druk, wrijving en draaibeweging

Voor één geïdealiseerd glijdend hellingcontact op straal r geeft een eenvoudige Coulomb-screening:

`T / F_axiaal ≈ r × (tan α − μ) / (1 + μ tan α)`.

Zonder wrijving is dit `r tan α`; automatische glijneiging vereist in dit eenvoudige model `tan α > μ`. De formule is geen garantie voor de hele koppeling: dubbele contacten, radiale hellingen, DD-wrijving, scheefstand, laagrichels en het benodigde schroefkoppel veranderen de beschikbare kracht.

Bij **aangenomen**, niet gemeten μ = 0,30 zijn de illustratieve koppelverhoudingen A 0,435 Nmm/N, B 0,590 Nmm/N, C 0,369 en 1,006 Nmm/N. Een te overwinnen schroefkoppel van bijvoorbeeld 1 Nmm zou alleen op basis van dit contactmodel circa 2,30 N voor A of 1,69 N voor B vragen, vóór andere verliezen. Dit is geen belastingvoorschrift voor de kleine PLA-punten. Test A moet de bruikbare kracht, schade en zelfzetting vaststellen. Een grotere helling helpt het theoretische koppel maar verkort de rechte draagflanken en kan andere contactpieken vergroten; er is zonder fysieke wrijvings- en sterktegegevens geen bewezen optimale hoek.

De onafhankelijke scripts rekenen beide hellingen expliciet uit. Op de dalende tak naar grotere φ bepaalt de rechter crownhelling de contact-envelope; op de andere tak de linker. Bij C ontstaat dus geen uniforme, grotere zelfrichtkracht in beide richtingen.

## Toleranties en pinhoogte

De oorspronkelijke eindstand heeft 1,44 mm tandpenetratie. Rechte flankoverlap is nu `1,44 − 2 × kroonhoogte`: A 0,48 mm, B/C 0,24 mm. Het eerdere E-297-budget van ±0,72 mm garandeert **niet meer** dat rechte flanken dragen. Een koppeling kan dan op haar hellingen koppel overbrengen en axiaal uit elkaar willen lopen. De E-297-claim over resterende rechte overlap mag dus niet overgenomen worden.

Een negatieve afwijking van 0,24 mm maakt B/C recht-op-recht overlap nul; voor A blijft dan 0,24 mm. Daarom moet de werkelijke selectorzetting en flankoverlap worden gemeten. Een vaste stop die nominaal aanwezig is, bewijst niet dat de echte print hem bereikt. De nominale halfselectie-tipafstand blijft 0,96 mm, zodat de geometrische EN-eindstanden van E-297 op nominale maat behouden blijven. Tussenstanden zijn niet digitaal geïsoleerd.

Bij een 3-mm lead is `Δz = 3 × Δφ / 360°`. Naar het dichtstbijzijnde insteekvenster is maximaal 76° nodig: **0,633 mm** pinhoogteverandering als alleen de schroef draait. De asymmetrische geometrie kan de langere dalende route kiezen; conservatief gerekend vanaf haar verschoven maximum is tot 100° of **0,833 mm** denkbaar. Een volle 180° periode komt overeen met 1,50 mm. Dit zijn ideale indexeerbewegingen, geen harde bovengrens voor herhaald handmatig heen-en-weer bewegen of tipmeeloop. Meet werkelijke draaihoek én pinhoogte. Ook DD- en tandspeling geven extra beweging; 28° nominale tandspeling correspondeert met 0,233 mm.

## Meerdere gelijktijdig geselecteerde pinnen

Een stilgehouden gedeelde input sluit zelfuitlijning niet uit: iedere vrije outputschroef kan zelfstandig zijn fase aanpassen. Maar één paar op het topplateau, één te stroef paar of één beschadigde punt kan nog steeds de gedeelde rij/kolom tegenhouden. Andere paren kunnen alvast gedeeltelijk aangrijpen. Zonder onafhankelijke veerweg bestaat geen passieve omzeiling van zo'n blokkade; veren zijn uitdrukkelijk niet toegevoegd.

Test B is daarom een **voorwaardelijke fysieke falsificatieproef**, geen bewezen oplossing. Zet eerst twee en daarna vier outputs bewust op verschillende fases, houd alle inputfases vast, sluit de echte gedeelde selectoren en registreer iedere schroefhoek, pinhoogte en selector-eindstand. Neem expliciet nominale punt-op-puntfases en de verschoven C-probleemfase mee. Een verkeerde fase die de hele staaf blokkeert is een nuttige negatieve uitslag. Het ontwerp mag dan niet als volledig zelfrichtend worden beschreven. Stop bij deze concrete tests; er volgt geen automatische nieuwe onderzoekscampagne.
