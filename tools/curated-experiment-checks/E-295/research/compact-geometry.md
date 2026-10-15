# Compacte schroefstaafjes: herkomst, keuze en begrensde proef

Onderdeel van [E-295](../../../../06-experiments/E-295-compact-screw-drive-development.md), 15 oktober 2026. **Uitkomst is CAD plus sliceronderzoek; deze nieuwe onderdelen zijn niet fysiek getest.** De expliciete vraag is of het aantoonbaar bewegende 90°-draadprofiel ook past in een slanke vierkante pin, zonder interne supports. De onderbouwde volgende stap is één kleine vergelijkingsplaat, geen serieproductie.

## Wat het bestaande bewijs wel en niet zegt

| Bron | Vastgesteld / gerapporteerd | Open beperking |
|---|---|---|
| [short-thread-fit](../../../../owner-print-tests/2026-10-14-short-thread-fit/test.md), eigenaar 2026-10-14 | Vijf 3,2-mm schroeven met 10,3-mm moeren doorliepen vijf handcycli zonder schade/nabewerking. 0,10 mm radiaal zeer stroef; drie 0,15 mm licht stroef tot vrij soepel; 0,20 mm uitstekend soepel. | Kwalitatieve waarneming, geen gemeten koppel/last. Werkelijke printinstellingen onbekend. Breedte past niet in 5,08-mm raster. |
| Origineel [Trial 5 actuator.scad, commit 41484f9](https://github.com/sander-van-damme/project-shape-display/blob/41484f96999847c139b9010e73009d73e9459c89/trial-5-grid-and-cubes-and-rod/actuator.scad) | CAD: 4,4-mm vierkant, 0,44-mm wand, 50,8-mm buis, 10-mm binnendraad; buitendraad d 3,2 / diepte 0,9 / spoed 3 / profiel 30°. Interne nominale d 3,4 / diepte 1,35; globale `$slop=.65`. | De eigenaar herinnert zich goed werkende historische prints. Exacte succesvolle variant, BOSL2-versie en printprofiel zijn niet teruggevonden. De huidige BOSL2-uitleg van de oude slop mag daarom niet als fysieke mislukking worden gepresenteerd. |
| Origineel [Trial 5 frame.scad](https://github.com/sander-van-damme/project-shape-display/blob/41484f96999847c139b9010e73009d73e9459c89/trial-5-grid-and-cubes-and-rod/frame.scad) | Opening 4,64 + wand 0,44 = **5,08-mm pitch**; 0,12 mm nominale ruimte per zijde voor 4,4-mm pin. | Lange rastergeleiding, doorbuiging en werkelijk geprinte passing zijn hier niet opnieuw gekwalificeerd. |
| [Verkorte Trial 5-replica](../../../../owner-print-tests/2026-10-14-trial5-short-replica/test.md) | Supports vulden het binnengat; eigenaar verwijderde ze niet. | Geen geldig draadpassingresultaat. Geen reden om compacte schroeven af te wijzen. |

De recentere E-281-schroef heeft **dezelfde nominale buitendiameter, diepte en spoed** als de historische buitenschroef. Het relevante verschil is vooral de 90°-flank en de expliciete overeenkomstige uitsnijding voor de moer, niet een grotere schroef. De brede 10,3-mm moer is dus geen geometrische noodzaak van deze schroef.

## Ontwerp van de eerste plaat

De [bron en STL](../../../../owner-print-tests/2026-10-15-compact-screw-fit/test.md) gebruiken exact het E-281-schroefprofiel via BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`, met `$slop=0` en een expliciete diametervergroting voor de vrouwelijke uitsnijding. Geen interpretatie van een verborgen bibliotheekcompensatie.

| Parameter | Nieuwe proef | Reden / grens |
|---|---:|---|
| Schroef grootste diameter / kerndiameter | 3,2 / 1,4 mm | Profiel uit geslaagde korte test behouden; dunne lange kern blijft een risico. |
| Spoed = lead / aantal starts | 3 mm / 1 | Snelheid en aantallen omwentelingen direct vergelijkbaar. |
| Radiale draaddiepte / ingesloten profielhoek | 0,9 mm / 90° | 45°-flanken in langsdoorsnede, printbaar zonder steile horizontale lip. |
| Draadlengte boven handgreep | 16 mm | Kleine proef; geen claim over 50-mm ongestutte schroef. |
| Vierkante pin / totale pinlengte | 4,4 × 4,4 / 18 mm | Slanke functionele doorsnede uit Trial 5; korte herhaalbare handproef. |
| Binnendraad onderaan / bovenholte | 6 mm / 3,52-mm vierkant | Twee volle spoeden, korte contactzone; 0,44-mm buiswand. |
| Variants | 1–3: 0,175; 4: 0,15; 5: 0,20 mm radiaal | Drie identieke nominale exemplaren, twee betekenisvolle grenzen binnen de eerder bruikbare band. 0,175 is **nieuw en onbewezen**. |
| Kleinste wand aan draadwortel | 0,425 / 0,450 / 0,400 mm | `(4,4 − (3,2 + 2×relief))/2`; kritisch voor 0,4-mm nozzle, daarom echte padeninspectie. |
| Geïntegreerde printvoet pin | 12 × 12 × 0,24 mm | Twee lagen van 0,12 mm, uitsluitend buiten de draadopening. Tijdelijke testhulp, **geen onderdeel dat in het raster past**. |
| Permanente handgreep schroef | 10 × 10 × 2,4 mm | Alleen coupon; geen kandidaat voor de duizenden aandrijfinterfaces. |

De oude 0,10-mm speling wordt niet opnieuw getest: zij was onaangenaam stroef. 0,20 mm wordt niet blind vastgelegd, want een d 3,6-uitsnijding laat slechts 0,40 mm materiaal over. 0,175 is een tussenwaarde die iets meer wand overlaat; de herhalingen testen spreiding. Radiale relief is de radiusvergroting van het overeenkomstige snijprofiel, dus de diameter groeit met tweemaal die waarde; het is geen toegestane excentriciteit. De nominale radiale overlap van de tanden daalt van `.9−.15=.75` tot `.9−.20=.70 mm`. Bij deze 45°-flanken voorspelt ideale vormgeometrie circa `2×relief` axiale vrije beweging, dus 0,30–0,40 mm vóór oppervlakte- en geleidingseffecten. Dit is geen gemeten backlash.

**Wat is verbeterd in CAD:** functionele buitenbreedte van 10,3 naar 4,4 mm, korte vrouwelijke draad alleen onderaan, een inspecteerbare open holte en een ontworpen buitenvoet die geen verwijdering uit de binnendraad vraagt. **Wat nog niet is verbeterd in bewijs:** wrijving, structurele sterkte, printopbrengst, levensduur en motorvermogen. Binnendraadlengte 6 versus 10 mm en laaghoogte 0,12 versus het eerdere aanbevolen 0,20-profiel zijn bijkomende verschillen; een beter handgevoel kan dus niet uitsluitend aan compactheid of tolerantie worden toegeschreven.

## Waarom deze printoriëntatie

Rechtop blijft de schroefas parallel met Z. De 90°-flank vraagt bij 0,12-mm laaghoogte nominaal 0,12 mm horizontale aangroei; bij het historische 30°-profiel zou dat ongeveer `.12/tan(15°)=.448 mm` zijn. Dat verklaart een aannemelijk printvoordeel zonder het historische fysieke succes te ontkennen. Dit is een doorsnedeberekening, geen vervanging van inspectie van de helixpaden.

Een liggende vierkante buis heeft goede bedsteun, maar de bovenzijde van de **interne helix** vraagt bruggen/overhangen boven een nauwe opening. Automatische supports geven opnieuw het concrete verwijderprobleem van de replica. Een gedeelde lange steunbrug helpt de buitenas, maar maakt dat interne contact niet bereikbaar. Een gesplitste moer/buis maakt montage en herhaalde onderdelen ingewikkelder. Daarom worden die opties voor deze kleine passantest niet gekozen. Voor langere productieassen blijven een liggende as met verwijderbaar extern kamframe, een grotere kern met minder draaddiepte of een ondersteund rechtop printframe serieuze vervolgmogelijkheden binnen hetzelfde schroefprincipe; hier worden ze niet als extra printjobs opgestart.

De 12-mm voet is een ontworpen buitenbrim. Zij blijft tijdens de handtest zitten. Dit vermijdt dat afbreken van een support een 0,40-mm functionele wand beschadigt vóór de passing wordt gemeten. De buis heeft hoogte/breedte 4,09; de schroefdraad is 16 mm hoog boven een 10-mm brede stijve voet. Dit is veel minder veeleisend dan een 50-mm vrije kern, maar hechting, koeling, kromtrekken en voetflexibiliteit moeten nog fysiek worden waargenomen. Slicen zonder supportpaden bewijst geen betrouwbare bedhechting.

## Van proef naar een terreinpin

- De coupon is bovenaan **open** voor inspectie en eenvoudig handmatig vergelijken. Een volledig terrein heeft gesloten vierkante toppen nodig. Bij pitch 5,08 geeft top 4,88 een spleet 0,20 mm en circa 92,3% nominale oppervlaktebedekking; top 4,4 geeft 0,68 mm en 75,0%. Een integraal kapje op de proef/demo is een mogelijke productievariant, geen excuus voor een grover raster.
- Zo'n brede top beperkt toegestane rotatie. Een top 4,88 past tussen buren bij gelijke hoogte slechts zolang `4,88(cosθ+sinθ)<5,08`, ongeveer **2,4°** zonder extra spelingreserve. Gebruik daarom externe rastergeleiding; onderling klemmen is onvoldoende onafhankelijk zodra buurhoogtes uiteenlopen. Een kapje lost de antirotatie niet op.
- De vierkante holte 3,52 geeft de schroefcrest 3,2 nominale ruimte. De buitendraad loopt door; uitsluitend het onderste moerdeel draagt axiale draadlast. Geen nauwkeurige losse moer of vergrendeling op iedere pin toegevoegd.
- d 1,4-kern maakt lange FDM-schroeven gevoelig voor zijdelingse belasting en torsie. De korte proef meet geen 40-mm slag of draagkracht. Draadschouders, geleidende plaat, axiale schroefopsluiting en een koppelbegrensde gedeelde kop moeten de belasting ordelijk opnemen; de moer mag niet tegen een eindstop worden aangedraaid.
- De kern heeft slechts 1,54 mm² minimale doorsnede. Een langere vrije as wordt snel gevoeliger voor knik (`Pcrit∝1/L²`); schroefribben en echte steuncondities beïnvloeden de waarde, daarom geen fictieve draaglast op basis van een kale kerncilinder. Torsiespanning stijgt sterk bij deze kleine kerndiameter, en FDM-laagverbindingen zijn geen isotroop massief materiaal. De 0,40–0,45-mm moerwand kan bij forceren, scheve insteek of zijdelingse druk opensplijten. PLA kan onder langdurige last kruipen. De 6-mm moer heeft minder belastingsverdeling dan de historische 10 mm en een hoger risico bij gedeeltelijk uitschroeven. De eerdere eigenaarwaarneming van een gebroken staafje nabij bijna volledig uitschroeven blijft relevant: de proef blijft daarom ruim volledig ingeschroefd. Geen tang of gemotoriseerde breekproef.
- Bij gemiddelde draaddiameter ongeveer 2,3 mm is de leadhoek `atan(3/(π×2,3))≈22,6°`. Zelfremming is dus **niet gegarandeerd**, zeker niet wanneer 0,20 mm bijzonder soepel blijkt. Houdgedrag moet fysiek worden getest; een globale rem of schroefzijdige houdwrijving kan daarvoor geschikter zijn dan extra mechaniek in de bewegende pin.
- Groot aantal onderdelen: print pas grotere batches na de drie identieke coupons. Tel afkeur, bedplaatsen, labels, trimwerk, assemblage en inspectie mee. Deze kleine ontworpen voeten mogen niet ongezien naar duizenden onderdelen worden gekopieerd.

## Reproduceerbare checks en stopconditie

`generate.py` exporteert de originele CAD, controleert tien gesloten meshes, maatvoering, volume en 305 coaxiale schroefstanden met nul CAD-overlap. Een bewust verkeerde fase geeft 6,472 mm³ overlap, zodat de toets ook daadwerkelijk een verkeerde montage detecteert. Zes aanvullende kruismontages met de bestaande brede onderdelen van paar 5 tonen nul CAD-overlap: oude schroef met nieuwe compacte pin en nieuwe schroef met oude brede moer. Binary-STL-export liet 88 geometrisch ontaarde sliverdriehoeken achter; alleen die zijn verwijderd, geen gaten gevuld en geen passing aangepast. De exacte hash en softwareversies staan in [geometry-validation.json](../../../../owner-print-tests/2026-10-15-compact-screw-fit/geometry-validation.json). De onafhankelijke slicercontrole, gebruikte instellingen en echte paden staan in het testpakket/review; geen meegeleverde G-code uitvoeren.

De stopconditie voor dit werk is dit printpakket plus de aansluitende kleine demonstratie en actuatievergelijking. Fysiek: drie nominale exemplaren moeten zonder draadnabewerking vijf heen/terugcycli met volledige 6-mm draadgrijping kunnen uitvoeren. Als die sterk uiteenlopen of slechts de ruime variant werkt, eerst eigenaarresultaten interpreteren; geen automatische grotere batch of nieuwe campagne. Als bewaarde brede onderdelen beschikbaar zijn, vergelijk op dezelfde oude schroef om printer- en schroefvariatie zichtbaar te maken; verschillend contactoppervlak blijft een confound. Geen feedback is geen resultaat.
