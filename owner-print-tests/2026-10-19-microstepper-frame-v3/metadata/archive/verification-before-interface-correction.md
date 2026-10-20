# E-302 v3 — maatcorrectie, 20 oktober 2026

**DRAFT/BLOCKED — niet printen.** Schone lokale branch bijgewerkt met fast-forward
naar `35720ba`. Alleen deze v3-map gewijzigd. De bestaande STL/3MF blijven
historisch bewijs; er is geen gecorrigeerd printpakket vrijgegeven.

## Actuele aanvulling na eigenaarmetingen en typcorrectie

A–D zijn nu benaderend gemeten: K A≈1,5/B≈2,75; L A≈2/B≈3,25;
beide C≈0,25 en D≈3 mm. Eigenaar bevestigt dat L **meer** dan3 mm is;
de eerdere tegenspraak is opgelost. Zie [centrale registratie](../../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md)
en [machineleesbare metingen](../../metadata/owner-motor-measurements.json).
Geen nieuwe meting van A–D nodig voor deze nominale herbeoordeling.

Met huisbasis Z2 en huistop Z11,2: K-tanden Z12,7–13,95;
L-tanden Z13,2–14,45; boss-top Z11,45. Bij de oude rotorpositie is de
rechte overlap bij lift0/0,3 voor K1,25/0,95 en voor L1,25/1,25 mm.
Tandtop/dakruimte is K4,25 en L3,75 mm, **alleen voor het tandwiel**;
een eventueel hoger asuiteinde is niet gemeten. Mond/bossruimte nominaal0,75 mm.
Dit kwalificeert geen toleranties of axiale belasting.

**Belangrijk ontwerpgevolg:** de hele rotor1 mm omhoog verplaatsen geeft
bij maximale lift K0 en L0,45 mm overlap. Beide halen dan de eerdere voorlopige
0,6-mm testgrens niet. Het huis/dekconflict moet dus worden opgelost met een
opnieuw berekende ring-/dek-/koppelingketen; niet door een blinde1-mm verschuiving.
Reproduceerbare berekening: `scripts/review_axial_measurements.py`, uitvoer
[axiale meetbeoordeling](../../metadata/axial-measurement-review.json).

**Taakstatus: nog niet afgerond.** Maatbasis en foutdetectie zijn bijgewerkt;
productie-CAD/STL/3MF nog niet gecorrigeerd. Er resteert geen blokkade door de
B-typfout. Werkelijke flens-/PCB-/soldeer-/draadenvelope en eventueel hoger
asuiteinde ontbreken. Die kunnen niet uit A–D worden afgeleid; een gesloten
motorhouder met onbemate uitsparingen is nog niet verantwoord vrij te geven.
De oude `motor-interface.json` en meshcontrole beschrijven de voorafgaande
bevroren audit; hun nulls zijn geen ontkenning van de nieuwe metingen.
Onderstaande oorspronkelijke tabel en audit blijven als gedateerd bewijs bewaard.

## Maatbasis vóór CAD-wijzigingen

Bronnen: [PM08-2 PDF, p.1](../../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/historical/trial-0/micro-stepper-datasheet.pdf)
(visueel gelezen, inclusief tekening), [bronvergelijking](../../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md),
eigenaarbericht 20 oktober, [fysieke resultaten](../../resultaten.md), bestaande CAD en scripts.
PDF is de beste technische referentie, maar geen bewijs van OEM-identiteit.
Geen maten uit fotoverhoudingen of CADforum afgeleid. Alle waarden in mm.

| Afmeting / referentie | Bestaande v3 CAD/controle | PM08-2 PDF / aanvullende bron | Eigenaar | Ontwerpbesluit / betrouwbaarheid |
|---|---|---|---|---|
| Metalen huis Ø | Zitting 8,2; controle 8 | Tekst 8; tekening Ø8,2 Max | circa 8 | Nominaal 8; toets ook 8,2-envelope. Zitting is geen huismeting; benodigde printspeling nog niet vrijgegeven |
| Huishoogte vanaf onderste metaalvlak | Zitting Z2–10,5 (8,5); controle 7,2 | 9,2 exclusief bearing sleeve | 9,2 | **9,2**, hoge bewijskracht; meettolerantie onbekend |
| Onder-/bovenvlak | Basis Z2; oude foto rekende top Z10,2 | Huishoogte 9,2; geen volledig gedimensioneerde zijaanzichtketen | Geen afzonderlijke vlakmeting | Basis voorlopig behouden Z2 → top **Z11,2**; bevestig dat ondervlak vlak draagt |
| Flens, huisovergangen | Ø11,5-ruimte Z9,2–10,3 | Foto toont flens, 2×M1,2; Ø8,2 Max in vooraanzicht, geen volledige flensdikte/contour | onbekend | Onbekend; Ø11,5 is ontworpen ruimte, geen motorafmeting |
| Boss / bearing sleeve | Ø4 doorgang Z10,49–11,96 | Zichtbaar, onbemaat | onbekend | Ø en hoogte boven metalen bovenvlak onbekend; essentieel voor ring/dek |
| Kale as Ø | Niet apart gemodelleerd; oude bron 1,5 | Tekst 0,8 | circa 0,8 | **0,8** nominale referentie; geen tolerantie bekend |
| Kale aslengte / uiteinde | Niet gemodelleerd | Tekst 4 met ambigu 'above the belt gear'; tekening 4,1±0,15 vanaf voorvlak tot uiteinde | onbekend | Geen bewezen kale asuitsteek; niet gelijkstellen aan tandlengte |
| Tandwiel buiten-Ø | Geen werkelijk tandwiel; C-boring 2,5 / tips Ø2,1 | PDF onbemaat; bronoverzicht Tempero 2,0 versus Amazon 2,2 | C paste goed | Geen definitieve tand-Ø; bewezen C-profiel behouden |
| Tanden / module / profiel | Drie ribben, geen geconjugeerd tandprofiel | PDF niet gespecificeerd; catalogus 9 / 0,2; drukhoek/tandcorrectie onbekend | niet gemeten | 9 / 0,2 uitsluitend hypothese; geen involuut verzinnen |
| Tandlengte / onder- en bovenkant | Fototop Z14,2; onderkant onbekend | 4,1±0,15 totale uitsteking, geen tandonderkant | twee verschillende uitvoeringen | **Onbekend per gekozen motor**; cruciaal voor overlap en dakruimte |
| Afstand tandonderkant–boss | Niet bepaald | Onbemaat | onbekend | Onbekend; geen vaste 2-mm inkorting gerechtvaardigd |
| PCB positie/breedte/dikte/hoogte | Ruimte X−8…−2,5, Y±3,5, Z2…10,5 | PCB zichtbaar maar onbemaat; 33±5° is tekeninghoek, geen envelopemaat | klein zijprintje | Alle uiterste grenzen t.o.v. as en ondervlak onbekend |
| Soldeer/kabels | Zelfde lege ruimte als PCB, geen afzonderlijk model | Vier draden; 160±5 / 18±3 kabelmaten, geen lokale buigradius | vier draden | Lokale uitsteking en vrije draaduittrede onbekend; kabellengte lost dat niet op |
| Productietoleranties | Geen motorstacktoleranties | Ø8,2 Max; uitsteek ±0,15; geen volledige stapeling | meetmethode onbekend | Niet overzetten naar eigen motor als bewezen tolerantie |
| Printpassing | Huis nominaal 0,10 radiaal; rotor 0,20; ring 0,15; axiaal 0,30 | n.v.t. | C past; huisfixatie eerder onvoldoende | Ontwerpspelingen, geen gemeten printpassing. Ø8,2 huis heeft nul nominale ruimte in Ø8,2 zitting |
| Spacers | 0,60/0,72/0,84; tangentbreedte 8,20/8,08/7,96 | n.v.t. | niet gekwalificeerd | 0,72 raakt het gecentreerde Ø8-huis al licht; 0,84 klemt sterker; mogelijke zijdelingse verplaatsing is geen gevalideerde uitlijning. Geen voorspanning bewezen |
| Ring / rotor / draad | ID3,2 OD7 dikte0,50; rotor Ø7; draad Ø3,2 spoed3 lengte16 | n.v.t. | bestaande ring en passende draad/C | Behouden; geen onnodige geometriewijziging |

## Eén axiale keten en gevolgen

Vast framevlak Z0 → motorsteun Z2 → metalen bovenvlak **Z11,2**.
Vanaf dat bovenvlak: boss-top `11,2+h`, tandonderkant `b=11,2+g0`,
tandbovenkant `t=11,2+g1`, hoogste as/tandpunt `u=11,2+max(s,g1)`.
`h,g0,g1,s` zijn onbekend en staan als null in [motor-interface.json](../../metadata/motor-interface.json).
De PDF-uitsteek zou, *indien dezelfde referentie en motor*, een top Z15,15–15,45
geven. Dit is geen vastgestelde t voor de eigen motor, noch een tandlengte.

Bestaande vaste keten: draagdek Z10,5–11,95; ringbodem Z11,7; ringtop en
rotormond Z12,2; rechte C-ribben Z12,7–18,2; holtedak Z18,2;
rotorschouder Z24,2; bovenstop Z24,5; draad Z24,2–40,2.
Bij oplichting `l∈[0;0,3]`: mond `12,2+l`, ribben `[12,7+l;18,2+l]`.

- **Zeker fout:** het volledige huis doorkruist het draagdek van Z10,5 tot 11,2.
  De lagere Ø11,5-uitsparing stopt al op Z10,3. Beide helften moeten worden herzien.
- Huisruimte moet minstens Z11,2 bereiken, plus gekozen montage-/printspeling;
  flens- en PCB-ruimte moeten aan echte referentievlakken worden gekoppeld.
- Overlap is `max(0,min(t,18,2+l)-max(b,12,7+l))`. Voorlopige oude testgrens
  0,6 aan beide liftuiteinden blijft een hypothese, geen koppelkwalificatie.
  Dakvrijloop vereist `18,2-u ≥ 0,5`; boss/mond vereist een afzonderlijke radiale
  én axiale toets. Zonder g0/g1/h/s is inkorting met 2 mm **niet goedgekeurd**.
- De ring ondersteunt de rotor, het dek ondersteunt de ring. Het dek heeft Ø4
  gat: onderste ringsteun is de annulus R2–3,5, circa25,92 mm² (vóór toleranties),
  niet de volledige ring tot R1,6. Bovenzijde draagt op de rotorannulus vanaf R1,6.
  Motor/boss/tand/as mogen geen parallel axiaal draagpunt worden.
- Deck/ring/rotor niet automatisch 1 mm optillen: dat verschuift ook schouder,
  bovenstop, draad en pinbereik. Eerst gekozen motorstack sluiten; alternatief
  lokaal dek aanpassen vereist genoeg restdikte, eveneens nog niet vrijgegeven.
- Huidige pinonderkant Z27,2–30,2, bovenkant Z45,2–48,2; 3 mm slag = één
  omwenteling bij spoed3. Elke latere rotorverplaatsing vereist hercontrole van
  geleiding, zes mm draadaangrijping, aanslagen en beide slaguiteinden.

## CAD-besluit en digitale verificatie

Productie-CAD, bestaande meshes en 3MF bewust bevroren als **ongeldig oud ontwerp**
tot de essentiële motorstack bekend is. Geen schijnbaar definitieve nieuwe STL.
C-ribben, originele draadmesh, ronde rotor, stijve helften, pennen, elastieken en
ring behouden. De generator en projectbouwer blokkeren uitvoer zolang de maatbasis
BLOCKED is. De correctie zit nu in maatbasis, detectie en vrijgavestatus, nog niet
in een vrijgegeven nieuwe mechanische uitvoering.

`review_geometry.py` gebruikt het volledige **9,2-mm cilindervolume vanaf Z2**,
met nominale Ø8 en aanvullende Ø8,2-envelope. Onbemate flens/boss/PCB/tanden
worden expliciet als ontbrekend gemeld, nooit als vrijloop-pass. Daardoor is dit
nog geen volledig OEM-motormodel; het volume dat zeker aanwezig is bewijst al de fout.
Rapport [motor-interface-review.json](../../metadata/motor-interface-review.json) bevat
beide helften afzonderlijk, motor/rotor/ring, oude PCB-envelope, spacers, rotatie
per graad over360° bij lift0 en0,3, gekoppelde volledige3-mm slag, aanslag en
ringcontact. Sampling is geen analytisch bewijs tussen standen. Cylindrische
rotor-framevrijloop is bovendien rotatie-invariant; thread/pin blijft een meshcheck.
Een BLOCKED-uitvoer eindigt met exit2, ook als niet-motorgerelateerde toetsen slagen.

Oude `cad-review.json`, slicerrapporten, illustraties en provenance zijn uitsluitend
bewijs voor 19 oktober. Oude slice: Bambu02.08.02.61, circa3u05 /10,70g.
**Geen nieuwe slice/heropening uitgevoerd:** onbekende motorstack blokkeert een
verantwoord nieuw printpakket reeds vóór slicing. Oude baancontrole bewijst geen
gecorrigeerde passing. Printer blijft beoogd X1C/0,4/PLA.

Niet digitaal bewezen: werkelijke PCB-/draad-/tandvrijloop, fysieke tandoverlap,
printkrimp, wrijving, ribflexibiliteit, voorspanning, slijtage of aslast onder belasting.
Geen fysieke bewegingstest uitgevoerd.

## Uitgevoerde resultaten

- Huis Ø8 ×9,2: **13,1961 mm³ botsing per helft**; Ø8,2-envelope:
  **14,1623 mm³ per helft**. Huistop expliciet Z11,2.
- 722 standen (361 hoeken ×2 liftstanden): grootste rotor/frame-overlap
  1,3e−14 mm³; pin/frame en rotor/pin nul. Numerieke grens 1e−4 mm³.
- Framehelften onderling nul; originele draad symmetrisch verschil
  6,79e−6 mm³. Geen functionele draadwijziging.
- Ring/frame nul; ring/rotor 2,46e−6 mm³ (meshprecisie). Contactprobes
  van0,001 mm geven onderaan0,025918 en bovenaan0,030404 mm³:
  effectief contact circa25,92 en30,40 mm². Bovenstop vrij op0,30 mm,
  op0,31 mm aantoonbaar contact (0,24613 mm³).
- Spacers0,60/0,72/0,84: huisinterferentie0 /0,05250 /0,97794 mm³
  bij gecentreerd Ø8-huis. Dit betreft radiaal contact, geen voorspankracht.
- Oude PCB-testvolume vrij, **werkelijk PCB onbekend**. Gear/boss/asvrijloop
  onbekend; geen claim van bewezen onbelaste motoras.
- Python-compilatie geslaagd. Beide exportcommando's stoppen vóór schrijven
  met expliciete BLOCKED-melding. Geometriecontrole exit2 zoals bedoeld.
- `git diff --check`: geslaagd. `./repo check`: exit1 wegens bestaande
  grootteoverschrijdingen E-266/E-283/E-286/E-288/E-293 en
  owner-print-tests/AGENTS.md; geen daarvan gewijzigd.

## Resterende meetinformatie

A–D niet opnieuw gevraagd. Voor één gekozen uitvoering resteert de envelope
van flens/lipjes en PCB inclusief soldeer/draaduittrede: uiterste breedte/diepte
t.o.v. de as en onder-/bovenhoogte vanaf het metalen ondervlak. Geef ook aan
of de as boven het tandwiel uitsteekt (zo ja, hoeveel). Dit bepaalt of het
frame kan sluiten en of er ongewenst axiaal contact ontstaat.
