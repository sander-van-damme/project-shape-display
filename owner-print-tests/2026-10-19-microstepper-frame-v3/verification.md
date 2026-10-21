# E-302 v3 — motorinterface en lange schroef/pin, 21 oktober 2026

**READY voor de fysieke proef met variant L.** Productie-CAD/STL gecorrigeerd;
nieuwe Bambu3MF opgeslagen, heropend, opnieuw gesliced en banen gecontroleerd. Geen fysieke passingstest uitgevoerd. Huidige uitbreiding bouwt op `66832d6`. De voorafgaande plaat en rapporten staan
in components/archive/2026-10-20-before-long-screw en
metadata/archive/before-long-screw. De eerdere verkeerd gespiegelde helften
blijven bewaard in de before-handedness-fix-archieven; gebruik die niet.

## Maatbasis en bronnen

[Eigenaarmetingen](../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md),
[machineleesbare registratie](metadata/owner-motor-measurements.json),
[PM08-2 PDF p.1](../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/historical/trial-0/micro-stepper-datasheet.pdf).
De PDF-foto en vooraanzichten tonen twee lipjes; hun precieze contour/dikte is
niet bemaat. PDF visueel gelezen, niet op schaal uitgemeten. OEM-identiteit
onbewezen. Meetlatwaarden zijn benaderingen; geen verzonnen fabricagetolerantie.

| Maat / referentievlak | Oude v3 | Technische bron | Eigenaar | Nieuwe ontwerpwaarde / status |
|---|---|---|---|---|
| HuisØ | Zitting8,2; controle8 | PDF tekst8, tekening8,2 max | circa8 | Zitting8,4; controle8 én8,2; 0,1 radiale ruimte bij8,2 |
| Huishoogte vanaf ondervlak | Zitting8,5; controle7,2 | PDF9,2 zonder boss | 9,2 | Volledig9,2-volume vanaf Z2 |
| Onder-/bovenvlak | Basis2; oud foto-top10,2 | PDF huislengte9,2 | vlakreferentie bij A–D | Basis2 behouden; top11,2 |
| Flens/lipjes | Ø11,5 pocket Z9,2–10,3 | Twee lipjes zichtbaar; contour onbemaat | twee bovenste lipjes circa1 | RuimteØ11,5 Z10–11,4; testvolumeØ10,2 ×1,2 tot11,2 is ontwerpenvelope, geen meting |
| BossØ / hoogte boven huis | Ø4 doorgang, geen solid | zichtbaar, onbemaat | ≈3 /0,25 | Volledig bossvolume; Ø4 doorgang; top11,45 |
| Kale asØ | oude bron1,5; geen solid | PDF0,8 | ≈0,8 | Ø0,8-volume |
| Asuiteinde | onbekend | PDF4,1±0,15 uitsteek, andere referentie/motor niet bewezen | ≈0,1 boven tandwiel | L-asuiteinde Z14,55; niet als nul genegeerd |
| Tandonderkant A | onbekend | niet afzonderlijk bemaat | K1,5 / L2 boven huis | L: Z13,2 |
| Tandbovenkant B | fototop14,2 | totale uitsteek is geen tandlengte | K2,75 / L3,25; typfout gecorrigeerd | L: Z14,45; K niet vrijgegeven |
| Tandlengte B−A | onbekend | onbemaat | afgeleid1,25 beide | L1,25 nominale overlapzone |
| Boss-top tot tandonderkant | onbekend | onbemaat | afgeleid1,75 voor L | L1,75 |
| TandØ / tanden / module / profiel | Geen tandmesh | Catalogus2,0 versus2,2 /9 /0,2; profiel onbekend | C paste | C-radiaalprofiel onveranderd; Ø2,2-envelope alleen vrijloopcontrole, geen echte tanden |
| PCB breedte | ruimte7 | PDF onbemaat | 6,5–7 variabel | ruimte8,5; modelbreedte7 |
| Motor+PCB diepte | oude ruimte X−8…−2,5 | onbemaat | circa10 | Model X−6…−2,5 bij huis tot+4; open zijde tot−9 |
| PCB hoogte vanaf ondervlak | oude ruimte2–10,5 absoluut | onbemaat | onder2 / boven6 | model Z4–8; brede ruimte Z2–10,01 |
| Lijm onder PCB | niet apart | onbemaat | varieert | Vrij tot motorsteun Z2; testblok Z2–4, breedte7,8 |
| Soldeer/draden | PCB-envelope gebruikt | vier draden, geen lokale buigradius | uitsteking varieert; kabels omhoog | Open kanaal X≤−4,2, breedte8,5 door gehele hoogte; testbundel X−7…−4,4, breedte8 |
| Ring | ID3,2/OD7/0,50 | bestaande component | behouden | Ringbodem12,4, ringtop12,9; pocketØ7,3 |
| C-profiel / inloop | Ø2,5; 3×R0,5 opR1,55; inloop0,50 | eigen CAD | radiaal passend | Radiaal onveranderd; inloop0,25 voor extra rechte overlap |
| Draad / proefslag | Ø3,2 /spoed3 /lengte16; slag3 | originele mesh | functioneel | Exacte meshes behouden; draad16 of48, slag3, pin18 of50 |
| Spacers / huisfixatie | 0,60/0,72/0,84 | eigen ontwerp | v3 niet gekwalificeerd | behouden, geen voorspanning bewezen; kies zonder asverschuiving of open naad |
| Print-/meetspeling | rotor0,2; lift0,3 | ontwerp, geen productiegegevens | meetlat beperkt | behouden; motor-/lijm-/kabelvariatie geen gemeten maximum |

## Eén expliciete axiale keten

Z0 framebodem → motorsteun2 → huisbovenkant11,2 → boss11,45.
Vrije motorruimte tot11,4 → draagdek tot ringbodem12,4 → ringtop/rotormond12,9.
De uitsparing oversnijdt bij het dek0,01 mm voor booleans: minimale restdikte
circa0,99 mm, geen onbedoeld0,5-mm dek. Ring ondersteunt de rotor buiten Ø4.

L-tanden13,2–14,45; asuiteinde14,55. Rechte ribben conservatief13,15–18,9;
bij0,30 lift13,45–19,2. Overlap L bij rust1,25 en bij maximale lift1,00 mm.
Dakruimte boven as4,35 mm; mond boven boss1,45 mm; ringbodem boven boss0,95 mm.
De oude voorlopige minimale overlap0,6 wordt nominaal gehaald. Een uitdrukkelijk
**aangenomen** gevoeligheid van tandtop−0,2 / tandonderkant+0,2 geeft0,80 mm;
dit is geen bewezen meettolerantie of koppelkwalificatie.

K geeft met deze geometrie bij maximale lift slechts0,50 mm: **niet vrijgegeven**.
Een blinde1-mm verhoging van de oude rotor gaf L0,45 / K0 mm. Daarom gekozen:
ring/rotor+0,7 en inloop0,50→0,25, geen automatische koppelinginkorting met2 mm.
De functionele ribvorm en draad zijn behouden; alleen de axiale inloop is aangepast.

RotorØ7, bodylengte12 en bestaande draadlengte16 behouden; extra lange
uitvoering heeft48 mm draad. Schouder24,9; bovenstop25,2; korte draad24,9–40,9,
lange draad24,9–72,9. Totale rotorlengtes28 en60 mm. De lange uitvoering
is gecontroleerd met pin50; korte met pin18 en50. Bovenste rotorgeleiding, pinbescherming en bovenste uitlijnpunt
schuiven samen0,7 omhoog. Onderbouwhoogte40,7; centrale geleiding nu32,7–72,7 met4,8-mm vierkant gat.
Pinonderkant27,9–30,9;18-mm pinbovenkant45,9–48,9 blijft binnen geleiding.
50-mm pinbovenkant77,9–80,9, uitsteek5,2–8,2; volledige proefslag blijft3 mm.
Het vierkante bovendeel is4,4 mm breed:0,2 mm nominale speling per kant.
Extra elastiekgroef bij67,7; geen nieuwe motor-/draadarchitectuur.

Krachtpad: pin → draad/rotor → bestaande ring → draagdek → frame.
Opwaartse last via rotorschouder/bovenstop. Geen bedoeld axiaal contact met
boss/as/tandwiel; fysieke klemming of wrijving blijft te controleren.

## Correctie van de handigheid

De vorige digitale assemblage gebruikte `back.apply_scale([1,-1,1])`.
Dat maakte een spiegelbeeld van het geprinte onderdeel en verborg de fout.
De nieuwe back-STL is in de CAD in X gespiegeld vóór de printoriëntatie.
Montage van beide werkelijk geleverde meshes gebruikt nu uitsluitend translatie
plus rotatie90° rond X en voor back180° rond Z, determinant+1.
De oude back-STL met dezelfde fysieke rotaties geeft38,444 mm³ botsing en wordt
expliciet afgekeurd; het nieuwe paar sluit zonder betekenisvolle overlap.
Pennen/gaten en PCB-/kabeluitsparingen liggen nu aan de juiste gezamenlijke zijde.
De nieuwe lange framehelften zijn samen te vervangen. Drie elastieken, inclusief
één bovenaan, houden het splitvlak dicht; daadwerkelijke rechtstand en schuifwrijving
over de40-mm geleiding blijven fysiek te beoordelen.

## Uitgevoerde geometriecontrole

`review_geometry.py` toetst de nieuw gegenereerde meshes met een **9,2-mm huis**,
boss, kale as tot boven de tanden, flensenvelope, PCB, lijm-/kabelenvelopes en
conservatieve cilindrische tandwielomtrek. Dit is een volledig samengesteld
ruimte-model met expliciete aannamen, geen bewezen OEM-contour of tandprofiel.

- Beide helften: huisØ8 enØ8,2 vrij; oude botsing13,196 mm³ per helft opgelost.
- PCB, lijmruimte, voorgeschreven kabelroute, flens, boss en as: geen significante
  frame-/ring-/rotorbotsing. Kabelroute **buiten** de ring; niet willekeurig langs as.
- 722 standen per combinatie: korte rotor/pin18, korte rotor/pin50 en
  lange rotor/pin50: rotatie0–360° per graad, gekoppeld
  aan3-mm slag, op lift0 en0,3. Daarnaast een continu4,4-mm vierkant sweepvolume
  door de geleiding voor het hele tussenliggende lengtebereik18–50: geen botsing.
  Rotor/frame circa1,7e−14 mm³; pin/frame en rotor/pin nul. Discrete sampling,
  geen analytisch continu bewijs; ronde bodyvrijloop is rotatie-invariant.
- Opnieuw geëxporteerde framehelften en korte rotor verschillen geometrisch
  niet van66832d6 (symmetrisch verschil0; zie metadata/preserved-parts-review.json).
- Originele korte draad symmetrisch verschil1,36e−5 mm³; lange48-mm draad
  2,53e−5 mm³ tegenover de oorspronkelijke v2-mesh, onder meshgrens1e−4.
  Korte/lange koppelingbody verschil1,19e−7 mm³: dezelfde dragende geometrie.
  Zijsteunen worden vóór montage verwijderd en zitten niet in de assemblagecheck.
- Ring/frame nul; ring/rotor4,91e−6 mm³ (meshprecisie). Contactprobes0,001 mm
  bevestigen circa25,91 mm² onderste en30,41 mm² bovenste draagvlak.
- Bovenstop vrij bij0,30; contact bij0,31 (0,24608 mm³). Helften onderling vrij.
- Spacers: nominale huisinterferentie0 /0,05250 /0,97794 mm³. Geen veerkracht
  berekend, geen garantie van gecentreerde as bij vastklemmen.
- Tandcilinder/rib-intersectie circa0,04544 mm³ is **bedoelde** benadering van de
  passende getande interface; geen botsingsvrije tandmesh geclaimd. Vrijloop van
  boss/as/rotor en fysieke tandoverlap zijn verschillende bewijsvragen.

Alle nieuwe STLs zijn gesloten en elk één verbonden lichaam. De rapporten onderscheiden digitale vrijgave van fysieke passing. Rapporten: [geometrie](metadata/motor-interface-review.json),
[axiale keten](metadata/axial-measurement-review.json), [meshes](metadata/geometry.json).

## Slicer, reproductie en grenzen

Nieuwe STL-export: `python scripts/generate.py` vanuit deze map.
Geometrie: `python scripts/review_geometry.py` (exit0 bij READY).
Axiaal: `python scripts/review_axial_measurements.py`.
Python numpy/trimesh/manifold3d; OpenSCAD2021.01; originele v2-meshbron behouden.

Oude3MF staat in components/archive/2026-10-19. De nieuwe primaire levering is
[microstepper-frame-v3.3mf](microstepper-frame-v3.3mf).

**Bambu Studio02.08.02.61 CLI**, officiële Ubuntu22.04-AppImage; lokaal uitgepakt,
ontbrekende runtimebibliotheken uit ondertekende Debian-APT-snapshot. Geen GUI-sessie.
SHA256 en runtimebron staan in metadata/provenance.json. Project heropend zonder
externe profielen en opnieuw gesliced, exit0; geen gewijzigde globale instellingen
of objectoverrides. Nieuwe banen bekeken in images/toolpaths.png.

- X1 Carbon/0,4 nozzle, Generic PLA, Textured PEI, nozzle220/bed55°C.
- Laag/eerste laag0,12; Arachne, 2 wanden, nominale lijnbreedte0,45;
  min bead75%, min feature10%, 100% zigzag-infill.
- Buitenwand/kleine omtrek/eerste laag/brug15 mm/s, binnenwand20;
  acceleratie default/binnen1000, buiten/eerste500 mm/s².
  Infill/bovenvlak30 mm/s; lange schroef inclusief torens maximaal30 mm/s,
  1000 mm/s² in de werkelijke banen.
- Automatische supports uit, raft0, per laag. Korte rotor buitenbrim2 mm;
  lange rotor met meegetekende zijsteunen buitenbrim3 mm, beide gap0,12;
  XY/gat/elephant-footcompensatie0. Fan100% na eerste laag, hulpfan0,
  minimum laagtijd8s. Effectieve instellingen in metadata/saved-settings.json.
- **4u59m21 totaal /4u43m41 modeltijd,16,61g /5,56747m PLA**; heropening
  geeft4u59m26 totaal /4u43m47 modeltijd,16,61g /5,56745m. Slices zijn niet
  byte-identiek; instellingen/objectoverrides blijven gelijk en beide banen
  zijn afzonderlijk gecontroleerd. Geen werkelijke printtijd of materiaalmeting.
- Meshafwijking3MF/STL maximaal0,000011193 mm. Tien objecten; geen ongeankerde
  eilanden >0,005 mm². Maximale verankerde brug2,452 mm.
- C-profiel op47 rechte lagen van beide rotoren gecontroleerd, min ribcontrast0,1497 mm;
  centrale radius0,8 open. Draad128 lagen verbonden, vijf volledige gangen.
- Korte pin150 lagen;50-mm pin417 lagen. Centrale radius0,6 vrij;
  lange bovenwand366 lagen gesloten, maximaal15 mm/s en500 mm/s².
  Voet12×12×0,24 mm, circa137,14 mm² bedcontact. Uitlijnpenkernen doorlopend;
  ronde/sleufgaten op de **gespiegelde printposities** vrij. De lange guide-opening
  en beide wanden zijn in werkelijke banen afzonderlijk gecontroleerd.
  Spacers5/6/6/7 lagen.
- Geen automatische supportbanen;945 brimsegmenten op de eerste laag:
  258 rond korte rotor,687 rond lange rotor/torenvoeten. Geen pinbrim.
  Meegetekende zijsteunen worden als modelbanen geprint; ze zijn expliciet
  gecontroleerd en zijn niet afwezig omdat de slicer nul supportbanen rapporteert.
  Zie metadata/brim-review.json.
- Zoals bij de oude draad: lokale interne spleetjes blijven in de baanvoetafdruk;
  minimum dekking binnenR0,50 circa83%. Geen volledig massieve kern of sterkteclaim.

### Lange schroef: verbindingen en verwijderbaarheid

`rotor-long.stl` is de schone60-mm assemblagemesh. `rotor-long-supported.stl`
voegt twee3×3-mm torens toe op4×8×0,48-mm voeten, met schuine armen en acht
nekjes0,85×0,45×0,24 mm. Elke zijde heeft vier contacten op12-mm afstand:
links Z19,56/31,56/43,56/55,56; rechts Z21/33/45/57 vanaf de printplaat.
Dit hergebruikt het v2-steunconcept met contacthoogten9,6 mm verhoogd voor
de geïntegreerde12-mm body tegenover de oorspronkelijke2,4-mm voet.
Alleen kleine draadtopgebieden worden geraakt; er is geen supportmantel of
support in de C-holte of pinboring. De onderste12-mm body blijft ongewijzigd.

Beide werkelijke slices:500 lagen tot60 mm;16 gangen behouden, doorlopende
centrale buitencontour, alle acht nekjes op twee lagen aanwezig. Elke schuine
arm is via laagoverlap naar zijn toren gevolgd; geen onverwachte verbindingen
of los beginnende eilanden. Torens doorlopend tot57,12 mm. Nominale banen
bewijzen geen materiaalsterkte of printstabiliteit. De massieve nekjes hebben
geen vrijgavegap: afzonderlijk afknippen volgens assembly.md; verwijderkracht,
resterende littekens en soepele passing zijn nog onbekend. De eerdere slecht
geprinte horizontale lange schroef blijft negatieve fysieke evidence.

Rapporten: metadata/long-screw-review.json en long-screw-review-reopened.json;
pincontrole: metadata/pin-review.json en pin-review-reopened.json.
De50-mm pin krijgt geen zijsteunen; zijn12-mm voet blijft zitten. Verhouding
hoogte/bovenbreedte11,36: bedhechting, wiebelen en nozzlecontact blijven fysiek
te beoordelen. Er wordt geen bewezen stabiliteit afgeleid uit nul supportbanen.

De PCB-uitsparing sluit aan op de flensuitsparing: een klein ongeankerd randje
uit de eerste conceptslice is verwijderd. Alleen de uiteindelijke plaat is READY.
Slicerrapporten: metadata/slice-review.json en slice-review-reopened.json.
Reproduceer met scripts/build_project.py --bambu PATH --resources PATH
--scratch work/PATH --stl components/microstepper-frame-v3.stl
--out microstepper-frame-v3.3mf; voer daarna review_slice.py, review_long_screw.py en review_pins.py uit
voor beide archieven; review_brim.py ontvangt beide archieven tegelijk.
`cad/long-screw-supported.scad` bevat de meegetekende nekjes/torens;
generate.py gebruikt de bestaande v2 pin50- en lange draadmesh zonder herschalen.

Geen fysieke passing, wrijving, koppel, ribflexibiliteit, maatafwijking, slijtage
of duurbetrouwbaarheid bewezen. Geen nieuwe meetvraag: de eigenaargegevens
volstaan voor deze nominale correctie; lijm/kabelvariatie en printpassing later
fysiek controleren. `git diff --check` geslaagd; `./repo check` behoudt de zes
bestaande groottewaarschuwingen buiten deze map.
