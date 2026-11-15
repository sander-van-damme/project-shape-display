# Montage — DES-010, nog niet fysiek gebouwd

Alle coördinaten zijn mm; x loopt langs de twee uitgangen, y langs de rail, z omhoog. STL-bestanden liggen in printstand; dit zijn de **montage**datums. Gebruik het [bovenaanzicht](images/plan.svg) en de [doorsnede](images/section.svg). Bouw eerst zonder riem en zonder spanning. Verwijder eerst alle automatisch gegenereerde supports uit de open bankonderzijde (jackpockets; motorplaat is los en vlak geprint); boutkoppen moeten vrij in hun pockets bewegen. z=0 is de bovenkant van de houten verhogingen, niet de plank: reserveer onder de motor ≥45mm vrije ruimte en verzink boutkoppen waar nodig.

## Niet-geprinte onderdelen

| Onderdeel | Aantal / concrete maat |
|---|---|
| Centrale motor | 1 NEMA17, bodylengte≤40, front42,3 vierkant, bevestigingsharten31, shaftØ5, asuitsteek minstens12; omkeerbare stroombegrensde driver. Hergebruik Pico/TMC2208 kan mits motorstroom passend ingesteld. Geen microstepperØ8 in deze houder. |
| Riem | 1 ronde EPDM/NBR O-ring, Ø1 snoer, nominale binnendiameter32 als eerste referentie; motor sleuven laten spanning variëren. Geen GT2 bestellen. Grip/rek/levensduur onbekend. |
| Bankrail | 2 gladde stalen Ø3×120 stangen; 1 losse Ø3×15 indexpin |
| Vaste framebouten | 4 M3×40 door voeten/onderstrap/deck/bovenstrap + moeren en ringen; controleer werkelijke stapel vóór vastzetten |
| Binnenste stapel | 4 M3 draadeinden circa55, 24 M3 moeren en ringen; dubbele moeren onder/boven ieder guidevlak; vier geprinte 1,1-mm spacers |
| Handjacks | 2 M3×25 bouten, 10 gewone M3 moeren (2 captive,2 veerzetmoeren,4 bovenste contramoeren,2 reserve), kleine M3 ringen |
| Drukveren | 2 metalen, buitendiameter circa5, binnendiameter ≥3,4, vrije lengte circa6, solidheight<3; gemeten doelk≈0,2–0,4N/mm **meten**. Een penveer alleen gebruiken als hij echt past; niet op catalogusgevoel afstellen. |
| Motorafstandhouders | 4 metalen2,0-mm spacers (of4 gemeten0,5-mm M3-ringen per motorbout:16ringen totaal). Deze zijn noodzakelijk voor boss-/poelievrijloop. |
| Motorbevestiging | 4 M3×8 passend bij motorflens; 4 M3×8 voor losse motorplaat aan bank; 1 M3×6 radiale poelieschroef (2,5 pilot voorzichtig met hand tappen/inschroeven) |
| Onderplaat | Stijve plank circa150×150, plus **minstens45mm hoge stevige houten verhogingen** onder alle4 voeten en2 railblokken zodat de NEMA17 vrij onder de bank hangt; schroeven/klemmen voor voeten en railblokken. Onderdelen moeten op dezelfde vlakke basis staan. |
| Bovenkap bank | 2 M2×8 |
| Indexrail | 1 M3×20 met moer/ring aan voorste railblok |
| Elektrische coupon | Zie actuator.md: draad, tweeØ3×24 zachte-stalen plungers, twee M2×6, twee M2×30, Ø2×25 geleider, .35 verenstaaldraad, twee MOSFET/diodekanalen |

M3-draadeind voor de geleidingen is eenvoudig af te zagen; verwijder bramen buiten het model. Bevestiging aan een plank is deel van de opstelling: losse voeten zijn geen dragend frame. Voedingen/driver moeten aanwezig of apart verkregen zijn; niets werd aangeschaft.

## Eerst kleine passingen

1. Test rotor2,2 /2,3 /2,4 vierkante boring op dezelfde male-stift; nominale2,3 is herkenbaar aan bronbestandsnaam. Houd onderdelen per zakje gelabeld. Drie identieke nominale rotoren/stiften leveren printvariatie. Stift moet vrij axiaal schuiven terwijl rotor handmatig draait.
2. Test guide46/47/48 op één pin. **4,7 is de constructieve basis bij de nieuwe4,50-mm pin** (0,10 zijde,0,38 tussenwand).4,6/4,8 zijn alleen coupons: respectievelijk0,05/0,15 zijde en0,48/0,28 tussenwand en dus mogelijk onbruikbaar. Geen volledige alternatieve frames printen.
3. Knip eerst de externe stabilisatietorens van pinnen en koppelstiften los bij iedere dunne nek (16 per pin,12 per stift). Niet wrikken of draaien. Trim de resten vlak op de buitenvlakken en controleer de vierkante schuifpassing en guidepassing vóór montage. Laat de binnendraad ongemoeid. `pin.stl`/`male.stl` blijven de schone montage-referenties; de3MF gebruikt de `-supported` prints. Knip de vier externe steunnekken van iedere schroef los; niet wrikken aan de draad. Controleer **alle resten op de flank**. Steun zit uitsluitend buiten de schroef, nooit in de pin. Test vier paren handmatig vóór montage. Pin heeft40-mm lengte en6-mm functionele binnendraad.

## Vast raster

- Schroefcentra x=0/5,08; y=0/5,08. Onderkant cupz29; threadstartz37,2.
- Voeten: middens(-42,-5),(-42,10,08),(47,-5),(47,10,08), bovenz29,35. Hun STL-origin is een hoek: trek6 af van x/y. Zet ze op de plank vast.
- Onderstraps bij x=-42/47, lokale y=0, z29,35. Leg de drie onderste deckstrips op z31,35. Laat hun halve lagerboringen de vierØ2 halsjes omsluiten. FlensØ4,4 ligt tussen z34 en35. Bovenstraps z33,95 klemmen ook de middelste strip; vier buitenbouten door beide straps en voeten houden de delen bijeen. Alleen handvast, geen kromtrekken.
- Keeper z35,05, met4 geprinte spacers1,1 tussen de onderdeckbovenkant33,95 en keeperonderkant. Keeperboring3,5 gaat over de schroefdraad en geleidt het gladdeØ3,2 deel. Nominale flensfloat0,10 totaal: hij moet vrij draaien, niet tussen thrustvlakken klemmen. Shim keeper omhoog bij klemmen; noteer echte float. Grotere float vermindert dokprecisie.
- Binnenste boutcentra x=-8/13,08 en y=-5/10,08. Draadeinden houden keeper en guides bijeen; guides onderkantz50 en66. Borg elk vlak met moeren/ringen, zonder de dunne rasterwanden te belasten. Pinonderkant laagz40,2; bovenkant80,2. Slag0–8; stop op48,2 onderkant. Niet op mechanisch einde doorrijden. Vier pinnen zijn geen miniatuurplatform.

## Bank, jacks en riem

- Achterste railblok oorsprong(-36,-70,0), voorste(-36,35,0). Stangen opx=-28/33,z6; zet uiteinden ongeveer y=-72..48. Houd blokken evenwijdig, leg bank vóór vastzetten over de stangen. Bank STL staat3mm lager dan montagestand: monteer met onderkantz3.
- Rotors STL op(x0 of5,08,y0,z12); korteØ4 journals draaien in4,3 bores. De trommel staat z14..18. Schuif beide rotoren in de onderste shelf, plaats de losse bovenkap opz18,2 en zet hem op de buitenposten vast met2 M2×8 in1,6 pilots, kopdiameter≤3,8mm en **geen grotere ringen**. Eerst met hand voorvormen; niet aandraaien tot de kap kromtrekt. Controleer vrije rotatie en axiale float vóór de stiften worden geplaatst.
- Male STL met stiftvoet op z11 bij ON (conusbasis29); OFF schuift2,4 omlaag. Vork printstand terugdraaien: eerst z−2,45, dan −90° om y; zet lokale conusdatumz29. Beide vorken wijzen naar+y: kanaal0 gebruikt `yoke` (reach18), kanaal1 `yoke-long` (reach25). Vorkopening3,2 om vierkante stift; collar gevangen tussen vorkvloer en bovenlip. Trek handmatig: de bovenlip moet de collar echt neerhalen.
- Iedere jack loopt op y=+18/+25, x=0/5,08. M3 moer in bankhex, bout vanonder. Op bout boven captive moer: instelmoer, ring0,5mm, drukveer, vorkgat, ring en2 contramoeren. Beide jacks staan buiten riem en vast raster. Start de onderkant van de veerzetmoer op **minstensz17,0** in ON, ringbovenkant circa19,9: tot de vorkonderkant24,3 blijft circa4,4mm veerruimte. Een vrije6mm veer wordt dan ongeveer1,6mm ingedrukt; kracht meten. De optionele geprinte veerzetter kost1,2mm ruimte en is alleen nuttig als de gekozen veer dat toelaat. De onderkant moet na2,4mm retractie≥14,6 blijven en de bankpad (top14) vrijlaten. Verstel de zetmoer omhoog voor meer druk en controleer altijd resterende ruimte tot solidheight. De veer drukt de vork omhoog; contramoeren boven vork trekken hem positief terug bij terugdraaien. Stel bovenstop en veerzetmoer afzonderlijk af: ON-veercompressie meten, OFF minimaal2,4mm conusretractie. De vork mag niet op de bovenste rotorshelf rusten. Geen elektrische selectie op deze bank claimen.
- Monteer eerst de losse `motorplate` op bankdatumz9 met4 M3×8 bijx−23,46/28,54 en y−52/−18 in2,5-mm pilots. Vorm de PLA-schroefdraad met de hand, trek niet door tot het plastic dol draait. De plaat wordt vlak geprint en vervangt de onbetrouwbare43-mm motorbrug. Plaats vier2,0-mm metalen spacers tussen motorflens en onderzijde van de motorplaat; motorfrontz7, boss topz9, poeliehub begintz10. **Zonder deze spacers botsen motorboss en poeliehub.** De motoras blijft op dezelfde x/y, riemvlakz16. Motor onder die plaat, ascentrum(2,54,-35). Sleuven lopen uitsluitend van y−35 naar−39; poelietrommelz14..18, dus poelie-STL origin opz10 (lokale shaftboss0..4/trommel4..8). Zet motoras vast met radiale M3. O-ring rond beide kleine drums en motorpoelie, met zo weinig rek als bruikbaar. Flenslip slechts0,15mm: tracking is een expliciete proef. Laat riem vrij van vaste schroeven en vorken.
- Indexrail oorsprong(41,5,19,14), schroef aan voorblok op(38,39). Indexpin valt bijbanky0 of5,08 door rail en banktab. Draai motor uit, parkeer beide conussen volledig, controleer lucht onder **alle**cups, verwijder indexpin, verschuif5,08, plaats pin terug. Geen mechanisch automatisch reisinterlock aanwezig; de volgorde is handmatig.

Controleer opnieuw vrije rotatie met gesloten frame, beide rijen en beide selectiestanden. De bank draagt nooit de permanente pinlast. Zonder bank moet iedere schroef gevangen blijven. Als pin terugloopt: noteer OFF-retentie als mislukt; krachtigere koppeling lost die houdvraag niet op.

De pinbinnendraad is historisch exact behouden; uitsluitend de buitenwand is0,05mm per zijde verdikt van4,40 naar4,50mm om daadwerkelijk gesloten slicerbanen te verkrijgen. De buitenpassing is daardoor nieuw en moet met de coupons worden gecontroleerd. Nominale buurafstand is0,58mm.

De cirkeluitsparing in de lange vork geeft de moeren/ring van het andere kanaal vrijloop bij onafhankelijke ON/OFF-standen. Niet met een grotere ring danØ7 vervangen.

Geen speciale korte veer of koploze jack nodig: de twee naar+y versprongen jacks laten gewone M3-bouten en circa6-mm metalen veren toe. Een zelfgemaakte veer mag, mits maat/kracht/solidheight gemeten zijn.
