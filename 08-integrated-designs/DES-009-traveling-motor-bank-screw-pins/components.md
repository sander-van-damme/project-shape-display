# Componenten en motoridentiteit

[Terug naar DES-009](DES-009-traveling-motor-bank-screw-pins.md) · [Elektronica](electronics.md) · [Bestanden en herkomst](sources.md)

Broncontrole: **18 oktober 2026**. Onderscheid hieronder: **CAD** is nominale geometrie; **verkoper** is ongeverifieerde productinformatie; **eigenaar** is een fysieke waarneming of gerapporteerde meting; **fabrikant** is documentatie van het geïdentificeerde component. Een passende catalogusfoto identificeert nog niet de volledige motorpartij.

## Actuele mechanische basis

| Component | Voorlopige specificatie | Bron en begrenzing |
|---|---|---|
| Geleide, niet-roterende pin | 4,4 × 4,4 mm; holte boven draad 3,52 mm vierkant; onderste 6 mm binnendraad | [E-295](../../06-experiments/E-295-compact-screw-drive-development.md), CAD plus positieve handmatige passing; geen gemeten draagvermogen |
| Raster | 5,08 mm pitch, vijf pinnen per 25,4-mm D&D-vak; nominale voeg 0,68 mm tussen 4,4-mm pinnen | [Vierpinproef](../../owner-print-tests/2026-10-15-four-pin-screw-demo/test.md); geen vrijwel gesloten groot terreinoppervlak bewezen |
| Schroef | Buitendiameter 3,2 mm; spoed 3 mm; draaddiepte 0,9 mm; profielhoek 90° | [Compacte passing](../../owner-print-tests/2026-10-15-compact-screw-fit/test.md); spoed is geen gemeten verplaatsing van de huidige gemotoriseerde proef |
| Nominale draadpassing | Radiale relief 0,175 mm; vergelijkingsvarianten 0,15 en 0,20 mm | Drie nominale paren fysiek soepel bevonden; CAD-relief is geen gemeten fysieke speling |
| Proefpin | E-301 18 mm; E-302 ook 50 mm buitenhoogte | [E-302 maatbronnen](../../owner-print-tests/2026-10-18-microstepper-frame-v2/sources.md): onderste 18 mm behouden, frame houdt nominale 3-mm proefslag; **50 mm pinhoogte is geen 50 mm slag** |
| Microstappenmotor | Eigenaar meet circa Ø8 × 9,2 mm; as circa Ø0,8 mm, vier draden, klein tandwiel en zijprintje | Circa **200 exemplaren** volgens [eigenaarverslag](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md); niet individueel gemeten/gekarakteriseerd |
| Tijdelijke aandrijfkoppeling | Ducttape in geslaagde éénmotorproef; E-302 onderzoekt opsteekkoppelingen | Ducttape bewees beweging, geen automatische ontkoppeling of reproduceerbare bankkoppeling; siliconenslang niet als werkelijk gebruikt bevestigd |
| Controller/driver | Raspberry Pi Pico W + witte Silent2208/TMC2208 V1.2-module | Huidige fysiek werkende testbasis; exacte modulefabrikant niet vastgesteld. [Elektronica](electronics.md) bevat fabrikantbronnen, firmware, UART/registers, stroominstellingen en werkelijke EN/VIO-bedrading |

**Motorbankgeometrie staat open:** Ø8-mm motorhuizen passen niet naast elkaar op 5,08-mm hartafstand in één rechte rij. Zijprintje, flens, koppeling en bedrading nemen extra ruimte in. De bankindeling en aandrijflijnen zijn nog niet gekozen of fysiek bewezen.

## Amazonlisting B08346RFVZ

[Abovehill — 10 pair 8mm Micro Stepper Motor 2-Phase 4-Wire DC 5-6V with Connection line +gear](https://www.amazon.com/Abovehill-Stepper-2-Phase-4-Wire-Connection/dp/B08346RFVZ) was bereikbaar en is inclusief alle vier primaire productbeelden onderzocht. Dit zijn **verkoperspecificaties, geen bevestigde OEM-datasheet**.

| Gegeven | Verkopersopgave | Betekenis voor onze motoren |
|---|---|---|
| Huis | Ø8 mm, hoogte 8,2 mm | Weersproken door eigenaarmeting: huis 9,2 mm; zie [actuele maatbasis](motor-variants-limits.md) |
| Type | Twee fasen, vier draden | Bipolaire toepassing; werkelijke windingparen identificeren |
| Faseweerstand | **39,2 Ω** | Historische tabel rondt af op 40 Ω; geen windingmeting aan de gebruikte motoren |
| Spanning | Geschat 5–6 V | Listing zegt “Estimated phase voltage”; geen vastgestelde nominale rating |
| Stroom | Circa 0,12 A; bij 6 V “short-circuit current” 0,14 A | Methode, temperatuur en toegestane bedrijfsduur ontbreken; geen gemeten stroom of gegarandeerde veilige limiet |
| Asdiameter | 1,5 mm | Weersproken door eigenaarmeting: kale as circa Ø0,8 mm |
| Lange uitvoering | Asuitsteking 4 mm | Blauw A+, zwart A−, rood B+, wit B− volgens verkoper |
| Korte uitvoering | Asuitsteking 3,5 mm | Paars A+, geel B−, oranje B+, groen B− volgens verkoper: **B− dubbel, A− ontbreekt** |
| Tandwiel | Ø2,2 mm, 9 tanden, module 0,2; “copper gear” | Messingkleurig op foto; materiaal, tandlengte, drukhoek en toleranties niet vastgesteld |
| Frontgaten | 6 mm hartafstand op maatfoto | Geen bevestigde schroefdraad of volledige flensmaat |
| Kabel/connector | Geen familie, steek of pinout genoemd | Foto's tonen twee motoren met acht draden naar één wit connectorhuis en elders losse krimpcontacten |
| Verpakking | Tien paren / twintig motoren; beide asuitvoeringen | Geen bewijs dat alle eigenaarsmotoren uit dezelfde partij komen |
| Overige catalogusvelden | 2000 rpm; 0,48″W × 0,31″H; 2,04 ounces; materiaal “Copper” | Context en testcondities ontbreken; niet gebruiken als motorsnelheidslimiet, individuele massa of montage-envelop |

### Productbeelden en vergelijking

De vierde productafbeelding is **byte-identiek** aan de [historische maatfoto](historical/trial-0/img/stepper-motor-dimensions.jpg) en de [actuele E-301-kopie](../../owner-print-tests/2026-10-17-microstepper-screw-pin/motor-dimensions-original.jpg). SHA-256: `91b1daabccbcece63d11bcb0b190c2f7bcf23977b242e339027d56f075e935bd`. Het betreft dezelfde catalogusfoto, geen onafhankelijke eigen meting. Voor de overige verkoopbeelden is geen herdistributielicentie gevonden; gebruik deze directe bronlinks.

| Beeld | Inhoud |
|---|---|
| [1 — tien paren](https://m.media-amazon.com/images/I/61Mrx175NvL._AC_SL1100_.jpg) | Tien tweemotorbundels met gezamenlijke witte connectorhuizen |
| [2 — kabelboom en aanzichten](https://m.media-amazon.com/images/I/61xvpzCIshL._AC_SL1100_.jpg) | Motorpaar vanuit verschillende hoeken; zijprintje/afdekking en twee uitstekkingen |
| [3 — beide asuitvoeringen](https://m.media-amazon.com/images/I/71I80J53Y5L._AC_SL1100_.jpg) | Paars/geel/oranje/groen gelabeld 3,5 mm; blauw/zwart/rood/wit gelabeld 4 mm; losse krimpcontacten |
| [4 — oorspronkelijke maatfoto](https://m.media-amazon.com/images/I/61mi2Nqb-gL._AC_SL1100_.jpg) | Ø8 × 8,2 mm, 4-mm totale uitsteking, Ø2,2-mm tandwiel met negen tanden/module 0,2 en frontgaten 6 mm uiteen |

De eigenaar meldt daadwerkelijk twee varianten met verschillend uitstekende tandwielen en een klein zijprintje, passend bij deze familie. E-302 vermeldt dat een derde getoonde motorfoto dezelfde motor vanuit een andere hoek is, geen derde type. Afzonderlijke foto's van de gebruikte exemplaren zijn in de huidige E-301/E-302-mappen niet opgeslagen; de visuele vergelijking blijft dus beperkt tot catalogusbeeld plus vastgelegde eigenaarbeschrijving.

**Tegenstrijdigheden blijven zichtbaar:**

- De korte kleurregel bevat zowel in de live listing als [oude componententabel](historical/trial-0/components.md) twee B−-draden. Niet stil corrigeren; werkelijk windingparen bepalen.
- De maatfoto toont de paars/geel/oranje/groene uitvoering met **4 mm** uitsteking, terwijl tekst en beeld 3 die kleurset aan **3,5 mm** koppelen. Beide uitvoeringen zijn inmiddels benaderend gemeten: zie [K/L en A–D](motor-variants-limits.md#1a-eigen-motorpaar--benaderende-eigenaarmetingen-20-oktober-2026). Geen kleurtoewijzing aan K/L bewezen. De pijl van 4 mm betreft totale as+tandwieluitsteking boven het huis, **niet de tandlengte**.
- De stroomcijfers sluiten niet exact op 39,2 Ω aan: `5/39,2 ≈ 0,128 A`, `6/39,2 ≈ 0,153 A`. Dit zijn Ohm-berekeningen; geen gemeten motorstroom of bevestiging van de verkooplimieten.
- De eigenaar beschrijft een **zeer kleine vierpolige connector**, kleiner dan GPIO-Dupont. Verkoopfoto's tonen een gezamenlijk connectorhuis voor een paar. Familie, steek en pinout blijven onbekend; geen JST-identificatie uit uiterlijk afleiden.

## PM08-PDF: beste technische referentie, identiteit onbewezen

[PM08-2 / PM08-02, Tempero Systems, versie 1.0](historical/trial-0/micro-stepper-datasheet.pdf), twee pagina's zonder zichtbare documentdatum, is hersteld als **historisch leveranciersdocument met onbevestigde type-identiteit**. Tempero is niet als de OEM van onze partij vastgesteld.

De PDF noemt Ø8 mm, **9,2-mm huis en Ø0,8-mm as**: die passen bij de
inmiddels ontvangen eigenaarmetingen. De eerdere kwalificatie “afwijkend type”
op basis van de Amazon-maten is achterhaald. PM08-2/PM08-02 is een aannemelijke
familie, geen bewezen OEM-identiteit. Elektrische ratings en twintig stappen per
omwenteling blijven geen eigen metingen. Gebruik de [actuele motorregistratie](motor-variants-limits.md)
voor bronverschillen, twee gemeten tandwieluitstekingen en resterende onzekerheid.

## Historische geometrie en bronklassen

De [oorspronkelijke Trial 5-CAD](historical/trial-5/actuator.scad) verklaart de compacte pinfamilie: 4,4-mm buitenbreedte, 0,44-mm wand, 50,8-mm pin, Ø3,2-mm schroef en 3-mm spoed. Maar deze oude versie gebruikt **30° profiel, 10-mm binnendraad, `$slop=0.65` en niet vastgepinde BOSL2-includes**. Het is genealogie, geen vervanging voor de recente E-295-basis met 90° profiel en 6-mm draad. De exacte vroeger succesvolle variant/libraryversie is onbekend; de [Trial 5-replica van 14 oktober](../../owner-print-tests/2026-10-14-trial5-short-replica/test.md) is wegens supports niet functioneel getest.

Voor Pico W en TMC2208 verwijst [electronics.md](electronics.md) naar officiële fabrikantdocumentatie. Voor deze microstappenmotor is **geen passend, bevestigd fabrikantdocument gevonden**. De motorverkooptekst en PM08-PDF blijven daarvan gescheiden. Werkelijke fysieke waarnemingen en multimetermetingen staan in het [E-301-resultaatverslag](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md); commits, herstelhashes en bestandsinventaris staan in [sources.md](sources.md).
