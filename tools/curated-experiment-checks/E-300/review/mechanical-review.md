# E-300 — onafhankelijke mechanische controle

**Bewijsniveau:** berekende doorsneden en booleans op de werkelijk geëxporteerde meshes. Geen fysieke passing, wrijvingscoëfficiënt, koppelgrens, sterkte of betrouwbare ontkoppeling is hiermee bewezen.

## Bronnen en reproduceerbaarheid

Gelezen: project- en printtest-`AGENTS.md`, missie, huidige prioriteiten, E-299-ontwerpdocumentatie/CAD en het volledige eigenaarsrapport in `owner-print-tests/2026-10-16-self-aligning-point-matrix/test.md`, inclusief de latere opmerkingen over stopblokjes en doorbuiging juist bij de uitsparingen. Historische bronbestanden zijn niet gewijzigd.

Voer vanuit de repositoryroot de volgende scripts uit met een Python-omgeving met CadQuery, trimesh, NumPy en manifold3d:

```sh
python tools/curated-experiment-checks/E-300/review/geometry_review.py
python tools/curated-experiment-checks/E-300/review/array_review.py
python tools/curated-experiment-checks/E-300/review/profile_review.py
```

De JSON-bestanden naast deze tekst bevatten de geteste poses, alle relevante bronhashes en concrete uitkomsten. Zij zijn leidend voor de aantallen na de laatste CAD-generatie.

## Geometrie, sluiting en raster

De controle omvat alle acht rij-/kolommaskers, tussenslagen, beide draairichtingen, relatieve beginfases zonder voorafgaand fasezoeken, de uitersten van de vangspeling op niet-gekoppelde paren, de montage van beide framehelften en doorlopende selector/frame-enveloppen. Geen onderdeelparen zijn geheel uitgesloten. Alleen de bedoelde conische raakvlakken mogen een kleine tessellatie-overlap hebben: uitsluitend het eigen onderste/bovenste rotorpaar, minder dan 0,01 mm³ en volledig verdwenen na 0,003 mm axiaal openen. Die gevallen worden afzonderlijk geregistreerd; een botsing met frame, as, flens of vork wordt nooit zo weggefilterd.

Nominaal resteert bij één geselecteerde helft 2,45 mm axiale scheiding tussen mannelijke tip en vrouwelijke mond. Bij beide geselecteerd bedraagt de tip-/bodemruimte 0,10 mm en steekt de mond 0,05 mm voorbij het begin van de mannelijke conus. Dit zijn CAD-maten vóór printfouten en geen bewijs van volledig contact na het printen.

De ronde conus heeft geen hoekfase. De ruimere mond kan de smallere tip tijdens de eerste benadering opvangen, maar volledig conisch contact vereist daarna werkelijk beschikbare zijwaartse uitlijnruimte. De DD-passing, framegeleiding, bramen en belasting kunnen die beweging beperken. De geometriecontrole houdt de assen verticaal; zij bewijst geen centrering onder een gemeten laterale of hoekfout.

De 3,00-mm nominale rijstand levert nog geen belasting op. Voor de nominale krachtketen wordt 0,24 mm speling aan iedere rotorvangst plus 0,04 mm aan de kolomhouder opgenomen: **3,52 mm rijverplaatsing tot het eerste belastbare contact**. De geometrische rijreserve is 3,75 mm. Verder drukken is geen vrije slag; dan vervormen contactvlakken en constructie. Echte selectiekracht is nog niet gemeten.

Bij rijhelling blijven beide rotorassen verticaal op hun eigen assen. De checker draait uitsluitend de starre rij en verschuift de rotorbases passend bij twee verschillende contacthoogtes. Een willekeurige helling van ±3° bij twee identieke vaste contacthoogtes is niet vrij: diagonale flens/vorkcontacten begrenzen dat. De afzonderlijke proef met één 0,10-mm hogere tapeoplegging op de eerste kolomhouder geeft circa 1,128° rijhelling en controleert een concrete kleine hoogteafwijking. De tape zelf is geen CAD-object en moet werkelijk gemeten en voorzichtig passend gemaakt worden. Een eerdere proxy die hele vergrendelde houders ±0,133 mm verplaatste is uitdrukkelijk geen bewijs van willekeurige tolerantieopvang.

De buurcontrole gebruikt de afzonderlijk geëxporteerde **functionele selectorkernen**, de echte rotoren en 5,08-mm verplaatsingen. Onafhankelijke aan-/uitstanden, ±0,24 mm buurrotorvangspeling, 3,75-mm rijverplaatsing en ±3° rijhelling worden gecombineerd. De externe handpeddel, bedieningsstaarten, testhouders en het proeframe zijn laboratoriumgereedschap en worden niet als een herhaalbaar matrixbedieningssysteem voorgesteld. Geen volledige lange matrix, ondersteuningsverdeling of aandrijfrouting is hiermee gekwalificeerd.

Tijdens de ontwikkeling werden werkelijke botsingen gevonden met de vaste schroefsteun, de voorste framedecksectoren en een aangrenzende vrouwelijke rotor. De huidige taps vrijgemaakte kolomvork, uitlopende bovenste vork, aangepaste frame-enveloppen en 0,90-mm hoge rugvrijloop beantwoorden die specifieke geometrische conflicten. De eindrapporten moeten nul onverwachte botsingen bevatten.

## Stijfheid: winst in hoogte, duidelijke beperking zijwaarts

De werkelijke doorsnede ter hoogte van de rotoruitsparing, 0,0001 mm naast de as om coplanaire meshartefacten te vermijden, geeft:

| Doorsnedegrootheid | E-299 | E-300 |
|---|---:|---:|
| Materiaaloppervlakte | 11,723 mm² | 7,089 mm² |
| Traagheidsmoment voor verticale buiging | 17,852 mm⁴ | 36,173 mm⁴ |
| Traagheidsmoment voor zijwaartse buiging | 8,650 mm⁴ | 0,869 mm⁴ |

De hogere doorsnede geeft lokaal **2,026×** zoveel geometrische weerstand tegen verticale buiging bij dezelfde elasticiteitsmodulus. De smalle rasterpassende rug maakt dezelfde doorsnede zijwaarts juist aanzienlijk zwakker. Het ontwerp mag daarom niet algemeen als stijver of sterker worden bestempeld. Draaiing van de open doorsnede, zijdelings wiebelen, laaghechting, kruip, spanningsconcentraties en de smalle rug vragen fysieke inspectie. Het volledige geprinte proefstuk bevat een brede externe peddel; die kwalificeert geen lange herhaalde selector. Een langere vrije overspanning blijft ondanks de hogere doorsnede ongunstig; doorbuiging groeit bij een puntlast als de derde macht van de lengte.

## Koppel, aandrukkracht en ontkoppelen

Voor een ideale 45°-conus met uniforme druk over radii 1,40–1,90 mm is de effectieve straal 1,6626 mm:

`T = μ × F_axiaal × 1,6626 / sin(45°) = μ × F_axiaal × 2,3513 Nmm`.

Bij **aangenomen**, niet gemeten `μ = 0,10 / 0,20 / 0,40` levert 1 N axiale kracht per koppeling respectievelijk ongeveer 0,235 / 0,470 / 0,941 Nmm. Twee koppelingen vragen samen circa tweemaal die axiale kracht plus verliezen in de flens-/vorkcontacten, DD-schuifpassing en geleidingen. Ook dat verlieskoppel is onbekend. De eigenaar rapporteert een vlot bewegende pin, geen gemeten benodigde schroefkoppel; daaruit kan geen voldoende slipmarge worden afgeleid.

**De bovenste flenswrijving kan de haalbaarheid bepalen.** Die rotor draait onder de volledige aandrukkracht tegen zijn kolomvork. Het belaste vlak is de lokale bovenzijde van de **onderste** vorkarm, `z = −0,24 mm`, na inversie aan de bovenzijde van de vrouwelijke flens. De uitgewerkte U-contactvorm heeft bij uniforme druk een effectieve straal van circa 1,819 mm; een grove volledige-annulusreferentie van 1,40–2,15 mm geeft 1,801 mm. Voor werkelijk nuttig schroefkoppel blijft dan hoogstens `F_axiaal × (2,351 μ_conus − 1,819 μ_bovenvork)` over, vóór verdere verliezen. Bij beide coëfficiënten 0,20 is dat slechts circa 0,106 Nmm per N. Het algemene krachtmodel gebruikt voorzichtig 1,85 mm en ongunstige gevoeligheden van 2,00 en 2,15 mm. Bij 0,20 op de conus en 0,30 op de vork is de schatting zelfs negatief: harder aandrukken verbetert de verhouding dan niet. Drukverdeling, statische/dynamische wrijving en werkelijke contactplaats zijn onbekend; dit is een gevoeligheidsberekening, geen voorspelde uitkomst. De onderste flenswrijving verhoogt bovendien het benodigde inputkoppel. Slip, moeilijk draaien onder druk en het verschil tussen ontlast en belast draaien moeten dus apart worden genoteerd.

Een centraal belaste starre rij kan twee contacthoogtes door hellen benaderen, zonder toegevoegde veren. Dit is uitsluitend een tweepuntsproef. Bij meer dan twee onafhankelijke hoogtes op een lange rij is voldoende druk op iedere conus niet opgelost. De gekozen brede 45°-hoek vermijdt volgens het ideale wigmodel zelfklemming zolang `μ < tan(45°) = 1`; geprinte ruwheid, vervorming, kleven en bramen kunnen toch blijven haken. Actief terugtrekken via de gevangen flenzen, ontlasten vóór ontkoppelen en werkelijk vrij draaien na beide ontkoppelroutes blijven verplichte fysieke controles.

## Assen en schroefsteun

De E-299-schroeven, pinnen en complete schroefprintboom blijven bytegelijk. De onafhankelijke meshcontrole vindt de eerste schroef/framecontacten ongeveer 0,147 mm omlaag en 0,230 mm omhoog; dit is nominale axiale speling, geen gemeten lagerkwaliteit. De inputsocket blijft 3,20 mm diep en de inputtip is ingekort naar 13,00 mm om bodemcontact bij de grotere rotorvangspeling te vermijden.

De onderste DD-inschakeling is ongeveer 1,72 mm in de nominale belaste tweepuntsstand. Bij twee contacthoogtes die overeenkomen met ±3° rijhelling is de kleine zijde circa 1,587 mm. Dat is geen universele ondergrens: op maximale ongebruikte rijslag, maximale rotorvangspeling en helling kan de geometrische inschakeling tot circa 0,877 mm dalen. Dat uiterste is geen beproefde toestand voor belast aandrijven. De 0,20 mm verdiepte blinde rotorboringen geven extra bodemruimte terwijl de bestaande schroeven intact blijven: circa 0,44 mm bij onderste rotor UIT op de lage vangspelingsgrens; circa 0,263 mm bij bovenste rotor UIT op de hoge vangspelingsgrens en de schroef volledig op zijn onderste framecontact. Dit zijn nominale combinaties vóór printfouten. Controleer vóór aandrijven de volledige selectieslag en actief terugtrekken; bodemen, sterk kantelen, beschadigde DD-vlakken of openende framevoegen zijn afkeur.

## Eindbeoordeling en stop

De eindgeometrie kan een zinvolle kleine fysieke proef rechtvaardigen als ook het definitieve X1C-project en de werkelijke slicerpaden worden goedgekeurd. Er is **geen fysieke GO** voor PLA-wrijving, beide contactdrukken, slipgrens, zijwaartse stijfheid, ontkoppelen of lange stangen. De proef moet juist die onzekerheid zichtbaar maken, met gewone PLA-vlakken en zonder fasezoeken of extra veren. Stop bij deze ene printproef; geen automatische vervolgontwerpen of duurcampagne.
