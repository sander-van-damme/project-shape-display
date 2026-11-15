---
status: active
builds-on: [DES-009, E-295, E-300, E-303, E-304, E-305]
---

# DES-010 — centrale motorbank met selecteerbare conussen

**Expliciete eigenaarsrichting, 15 november 2026; geen fysiek bewezen bank.** Eén omkeerbare centrale motor drijft twee aangrenzende uitgangen op een verrijdbare bank. Iedere uitgang heeft een eigen schuivende conuskop. Het vaste **2×2 raster op 5,08 mm pitch** behoudt de bestaande schroefwerking. De handmatige bank is de geïntegreerde mechanische referentie; een afzonderlijke elektromagnetische camcoupon meet de onzekere elektrische selectie. [DES-009](../DES-009-traveling-motor-bank-screw-pins/DES-009-traveling-motor-bank-screw-pins.md) blijft historische/technische basis.

**Bouwen begint bij het [printpakket](../../owner-print-tests/2026-11-15-central-cone-bank/test.md):** echte STL's, geconfigureerde Bambu-projecten, parametrische CAD, doorsneden, montage/BOM, resultaten en digitale verificatie. Geen fysieke proeven of aankopen.

## Bewijs en omvang

- E-301: één microstepper bewoog één schroefpin. Dit bewijst geen bank of automatische koppeling.
- E-295: compacte nominale 0,175-mm radiale CAD-relief voelde handmatig soepel. Dit is geen gemeten bedrijfsspeling of benodigd koppel.
- **Actuele eigenaarwaarneming A:** blokkering onderaan verdween na verwijderen van supportresten; pin liep daarna soepel. Het onderframe paste na hermontage minder goed. Thermische vervorming is vermoed, niet vastgesteld. Deze waarnemingen wegen zwaarder dan lege oude formulieren.
- Alle nieuwe kracht-, slip-, riem- en actuatorwaarden zijn berekeningen of proefinstellingen. Nieuwe fysieke werking blijft onbekend.

2×2 in plaats van 4×4 test met vier paren dezelfde nieuwe interfaces: twee werkelijk aangrenzende kanalen, parallel/afzonderlijk bewegen en een tweede rij bereiken. Proefslag **8 mm**, pinlengte40 mm; geen aanspraak op40-mm slag. Vier pinnen vullen geen D&D-vak van25,4 mm: speelbaarheid, dunne grensmuren en miniatuursteun zijn hiermee niet bewezen.

## Samenstelling en krachtroute

Rastercentra x=0/5,08 en y=0/5,08; z omhoog. Bestaande nominale Ø3,2/3-mm-spoedhelix en vrouwelijke draad worden uit de historische meshes behouden; geen herontworpen draad. Onderkant cupz29, gladde halsØ2 van31–34, flensØ4,4 van34–35, bovenhalsØ3,2 van35–37,2 en27-mm draad vanaf37,2. Onderdeck31,35–33,95 en keeper35,05–36,65 vangen de flens met nominale0,10 totale float. Drie deelbare onderste strips maken montage mogelijk; buitenste boven-/onderstraps klemmen ook de middelste strip. Geen per-displaypin bouten, veren of elektromagneten.

De vrouwelijke draad blijft exact gelijk; alleen de buitenwand wordt0,05mm per zijde verdikt van4,40 naar **4,50mm**, omdat de gerichte slicerproef daarmee alle330 gecontroleerde lagen sluit. Nieuwe buitenpassing fysiek onbekend. De pin wordt tegen rotatie gehouden door twee korte2-mm guidevlakken op z50/66, opening4,7. Tussenwanden0,38 mm zijn een te testen printdetail; coupons4,6/4,7/4,8 voorkomen hele alternatieve frames. Grotere openingen verminderen wandsterkte en kunnen de draadasuitlijning verslechteren. Pinonderkant laag40,2, hoog48,2; beide guides blijven volledig overlapt.

**Koppel:** motor → gemeenschappelijke riem → twee axiaal vaste rotoren → vierkante schuifstiften → conus → resident schroef → vrouwelijke draad/pin. **Permanente last:** pin → schroef → vaste flens → onderdeck → buitenste voeten/plank. Omgekeerde axiale kracht gaat via keeper. Bank/yoke levert alleen tijdelijke koppeldruk en draagt nooit stilzwijgend de permanente pinlast.

Twee korte rotorjournalsØ4 draaien in4,3 boringen; bovenste lagerkap is afneembaar voor rotorinbouw. Vierkante stift2,0 in nominale2,3 boring schuift axiaal. Een gevorkte cage vangt deØ4,2 collar; drukveer via onafhankelijke M3-jack op y+18/+25 levert ON-druk, contramoeren trekken de vork positief terug. De metalen veer draagt de ingestelde druk; de gebruiker hoeft die niet met een magneet te blijven leveren.

**Volledig park is2,4 mm retractie.** Conushoogte1,386; alleen1,2 mm contactverlies laat de tip nog in de cup. Bij2,4 retractie is nominale tipruimte1,014 mm onder de cup. Dit is vóór float, printafwijking, scheefstand en vuil; visueel controleren vóór reizen. Railindex heeft twee gaten op5,08 mm afstand; motor uit, beide volledig park, dan pas indexpin uit. Er is geen automatische reisinterlock.

TweeØ3×120 rails, handmatige indexering, één NEMA17 op een los vlak geprinte motorplaat met sleuven en een losse rotorlagersluiting maken de proef demontabel. NEMA17 hangt onder de bank: minimaal45 mm vrije ruimte op stevige verhogingen. Capbevestiging M2 kop≤Ø3,8 zonder grote ringen; grotere koppen kunnen de teruggetrokken vork raken. Exacte boutlengten, montagecoördinaten en voorraadlijst staan uitsluitend in assembly.md van het printpakket.

## Gemeenschappelijke transmissie: keuze

| Optie | Beoordeling bij5,08 pitch |
|---|---|
| Gemeenschappelijke tandriem | GT2-16T steekdiameter10,19 en grotere flenzen passen niet naast elkaar. Z-staggering alleen lost botsing met de doorlopende naburige assen niet op. Een offsetoverbrenging voegt onderdelen toe. Positieve grip en omkeerbaarheid zijn aantrekkelijk, maar deze gangbare geometrie is geen bouwbare directe bank. |
| Horizontale as + kegel-/kroonwielen | Een metalen as is sterk en schaalbaar. Haakse uitgangenØ4,6 vragen echter zeer fijne tanden, uitlijning en bidirectionele reactielagering. Printen met0,4-nozzle is onzeker; grotere wielen hebben opnieuw asinterferentie. Meer componenten/assemblage dan de kleine proef rechtvaardigt. |
| **Gladde ronde frictieriem, gekozen** | Eén driehoek rond beide kleine eindrotoren en motor geeft werkelijke omwikkeling, geen tandfase en weinig onderdelen. Omkeerbaar, verwisselbaar en eenvoudig te printen; wel riemrek, tracking, glijwrijving en lagerverlies te meten. Geen gekwalificeerde positieve transmissie. |

TrommelsØ4,6 metØ4,9 lippen enØ1 ronde elastomeerriem geven ongeveer5,6 effectieve diameter. MotorpoelieØ10,6; hart(2,54,−35), uitsluitend y−35..−39 instelbaar. Begin met O-ring32-mm binnendiameter/1-mm snoer en minimale bruikbare spanning. De flenslip is slechts0,15 mm: tracking is uitdrukkelijk een fysieke beslisvraag. Vergroot voorspanning niet om binding te maskeren.

Scenario0,3 Nmm per uitgang: bij effectieve straal2,8 is spanningstoename circa0,107 N. Contactboog rond95° en aangenomen μ=.3 geeft capstanverhouding exp(μθ)≈1,65. Dit is geen gemeten materiaalgegeven of voltooide motorkoppelberekening. Radiale riemlast en droge journalwrijving kunnen vergelijkbaar zijn met het schroefkoppel. Meet lege bankverliezen en bus-slip; **riem moet meer koppel leveren dan de conusslipgrens** voordat conusslip als bescherming mag worden geclaimd. Krachtige motor kan slechte passingen verbergen en beschadigen.

### Uitbreiding naar80–100

Een rechte riem langs80 collineaire trommels heeft vrijwel nul binnenwrap. De concrete vervolggeometrie is **twee interleaved decks**, elk40 uitgangen op10,16-mm onderlinge afstand, met backside-idlers bij de tussenliggende x-posities en y≈−6. Kleine rotoren kunnen in z verspringen zonder de GT2-doorasbotsing. Bij referentie-steekstraal2,6 zijn lokale interne raaklijnlengte5,897 en boog/doorasspeling circa0,56 mm berekend; dit is nog geen vrijgave voor de hier gewijzigde effectieve2,8-mm straal of volledige lus.

Tel ongeveer80 rotoren en78 idlers, twee riemen, lagering en een samengestelde motorpoelie. Volledige retourroute, belt-kruisingen, spanning over400 mm, framebuiging, slijtage, verliezen en alle gelijktijdige lasten zijn nog uit te werken. De huidige twee-uitgangsproef kwalificeert die bank niet. Bij onvoldoende grip moet de distributie worden aangepast vóór80 kanalen worden gebouwd. Breder bepaalt parallelle kanaaltelling; langer kan via de rail. Modulaire banken kunnen later identiek/vervangbaar zijn; multi-bankplanning is geen onderdeel van deze proef.

Bij80 gelijktijdige uitgangen en aangenomen0,3 Nmm elk is de nuttige som24 Nmm. De verhouding5,8/2,8 vraagt aan de motor circa50 Nmm vóór lager-/idlerverliezen. De bijbehorende som van riemspanningsverschillen is circa8,6 N, veel groter dan de kleine proef. Een NEMA17 is een plausibele klasse, geen bewezen voldoende koppel bij snelheid. Controleer vooral de laatste zwaarbelaste journals, asbuiging en slijtage; alleen laag motorkoppel begroten is onvoldoende.

## Conus en krachten

Herbruik E-300/E-304: halve hoek30°, contactstralen1,1–1,9, contacthoogte1,386 mm, oppervlak15,08 mm² en effectieve straal1,50 bij uniforme slijtage/1,536 bij uniforme druk. Eerst PLA/PLA; rubber verhoogt wrijving én risico op vastkleven en verhindert een eerlijke eerste vergelijking.

`T_conus ≈ μc F R_eff/sin30° ≈3 μc F Nmm`.

De gekozen bovenkeeper heeft een thrustannulus r1,75–2,20, effectieve straal **1,984mm**; neem niet de kleinere E-304-pad over. Screening: `T_nuttig≈F(3μc−1,984μ_thrust−k_zijdelings)`. Bij aangenomen .25/.20/.10 geeft dit .253F Nmm: het historische .343-Nmm scenario zou **1,35N** vragen, buiten de eerste1,2-N grens. Bij μc=.30 daalt dat naar circa.85N. Dit scenario is geen gemeten schroefvraag. Stop bij onvoldoende beweging; niet druk blijven verhogen. De inputcollar (effectieve straal1,86) belast apart de motor met wrijving. Berekening/sensitiviteit: `scripts/calculate.py` in het pakket.45° vraagt nog meer druk;30° blijft de eerste laagkrachtproef.

Veerdruk instelbaar circa0,3–1,2 N, beginnen laag; **meten** met schaal tegen compressie.1 N is geen bewezen vereiste. Nominale gemiddelde contactdruk bij1 N≈.133 MPa; printtrappen dragen lokaal meer. Cupopening heeft slechts0,4-mm radiale wand, dus slicerbanen én fysieke schade controleren. Tolerantie, excentriciteit, plaattwist en slijtage kunnen grip in beide richtingen veranderen.

μ<tan30° bewijst geen release: trappen, vuil en adhesie kunnen klemmen. Positieve collar-extractie, onderbroken rotatie bij eerste instelling, vaste axiale vangst en volledige parkcontrole zijn noodzakelijk. Geen tandfase nodig, in tegenstelling tot een dog-clutch die niet vanzelf onder willekeurige relatieve hoek kan insteken.

**Bescherming vereist** normaal bedrijfskoppel < gemeten conusslip < schadelijk koppel; alle drie onbekend. Blokkering kan ook hals, cup, key, keeper of bank beschadigen; externe pinimpact loopt buiten de sliproute. Riemslip of motorstapverlies mag niet als conusslip worden geregistreerd. Hoogtebehoud zonder bank blijft expliciet open:3-mm spoed is niet vanzelf zelfremmend. Test OFF-drift; sterker aanklemmen lost dit niet op.

## Elektrische selectie: concrete onzekerheidsproef

| Variant | Keuze/gevolg |
|---|---|
| Zelfgewikkeld + mechanisch bistabiel | Gekozen coupon: twee tegenovergestelde inschuifplunjers, cam10-mm slag/3-mm lift, vlakke dwells en metalen draaddetent. Dwell draagt veerlast stroomloos, coil betaalt wel de schakelarbeid. Geen bewezen bistabiliteit of krachtmarge. |
| Permanente magnetische latch | Mogelijk één coil/H-brug, maar losbreken, OFF-restkracht en buren onbekend. E-305/E-241's negatieve kracht- en uitleesresultaten blijven relevant;80 bankactuatoren veranderen de aantallen, niet de fysica. |
| Spring-return solenoïde | Eenvoudig, maar continue stroom/verwarming. Historische5V/1,1A referentie geeft440W bij80 ON. Retourveer is alleen fail-release als zij werkelijk positief kan lostrekken. |
| Commerciële latch | Historische Olimex circa€2,50,5-mm slag,8×10,3×16,3 lichaam is referentie, geen actuele prijs/voorraad/krachtbewijs. H-brug/mount/bedrading meerekenen. Kan goedkoper totaal zijn dan handwikkelen. |

Coupon: twee bobbins met boring3,65/flens10,8/windinglengte14. **567 windingenØ0,20 Cu per coil**,63×9; berekend circa12,3 m/6,8Ω en1,7W bij0,5A. Er is geen gesloten stalen retourpad, dus geen verantwoorde krachtvoorspelling. Meet plunjerkracht bij begin/midden/eind én camkracht onder0,3–1 N. Een mechanische latch levert geen gratis schakelenergie; ongekwalificeerde PLA-klikveren worden vermeden.

[Concrete montage en elektrische proef](../../owner-print-tests/2026-11-15-central-cone-bank/actuator.md): twee MOSFET/diodekanalen,5V bench≤0,5A, aanvankelijk10Ω/5W serie, maximaal200ms puls/5s pauze; stoppen bij45°C of10°C stijging. Polariteit omkeren maakt staal niet afstotend. Bistabiliteit kan ON na stroomuitval vasthouden: handmatig volledig park vóór reizen.

Een3-mm cam reserveert slechts0,6mm extra boven2,4mm park. Dat is niet genoeg om een slappe veer vanuit nul tot1N te comprimeren. De bankjacks houden de veer daarom al voorgespannen tussen zetmoer en bovenstop; een toekomstige elektrische carrier moet die voorspanning gevangen houden. De coupon meet de vereiste schakelarbeid onder opgelegde last, maar bewijst die carrier/extractie niet.

De afzonderlijke coupon is bewust de toegestane stopgrens voor deze nog onvoldoende onderbouwde selectie. Hij is **geen drop-in elektrische bank**. FlensØ10,8 vereist minstens drie y-lanes bij5,08 pitch; de36×82-mm krachtcoupon kwalificeert die packaging niet. De handmatige bank blijft de fysiek te bouwen referentie.

## Kosten en maakbaarheid

Alle bedragen zijn **begrotingsaannamen**, geen offertes of actuele materiaalprijzen. Geen aanschaf uitgevoerd. Kleine proef motor/driver€15–35, voeding€10–20, riem€1–3, veren/bevestiging€12–25, rails€4–10, verhogingen€0–10, PLA€2–6, elektrische coupon€8–20: **circa€55–130**, exclusief arbeid, verzending en meetgereedschap. Dit is een complete materiaalraming voor de kleine opstelling; hergebruik verlaagt hem. Exacte slicermassa in verificatielog.

| Toekomstige bank, zonder vast raster/arbeid | Commerciële latch | Zelfbouw dubbelspoel |
|---|---:|---:|
|80 kanalen incl driver/mount/connectors |€320–560 |€320–640 |
|Motor/rail/voeding/communicatie |€70–160 |€70–160 |
|Transmissie/lagers/frame reservering |€40–120 |€40–120 |
|**Eén bank** |**€430–840** |**€430–920** |
|**Twee banken** |**€860–1.680** |**€860–1.840** |

De80-route kan de transmissiereservering ongeldig maken. Eén euro per kanaal is€80, maar tien minuten minder assemblage bespaart13,3 uur.160 zelfgewikkelde coils vragen circa1.968 m draad en320 aansluitingen; alleen vijf minuten wikkelen per coil is13,3 uur. Geen actuele draadprijs vastgesteld. Twintig gelijktijdige .5A-pulsen geven circa34W/10A koperlast,80 circa136W/40A; geen totale voedingsspecificatie. Gespreid pulsen vraagt gemeten schakeltijden. Twee banken herhalen hardware, niet het vaste raster. Duizenden resident schroef-/pinparen zijn buiten deze bankraming.

## Controle en stopconditie

Nominale mesh-/bewegingscontrole, werkelijke slicerpaden en fysieke waarnemingen worden afzonderlijk gelogd in het [pakket](../../owner-print-tests/2026-11-15-central-cone-bank/verification.md). Het pakket bevat reproduceerbare bronnen en echte STL/3MF, montage, BOM, korte test en leeg resultatenformulier. Digitale passing bewijst geen printfit, slip, retentie of elektrische selectie. Stop bij deze geïntegreerde referentie plus kleine elektrische krachtproef; geen80-kanaalbouw of autonoom vervolg.
