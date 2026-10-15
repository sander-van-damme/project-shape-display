# Printtest — vijf compacte schroefstaafjes van 4,4 mm

> **Fysiek resultaat (eigenaarrapportage 2026-10-15):** alle vijf compacte paren starten zonder kracht en voltooien vijf handcycli. De drie identieke 0,175-mm-paren voelen alle drie "supersoepel" met heel weinig benodigde kracht. Zie [resultaten en interpretatie](#4-mijn-resultaten--sander-eigenaarrapportage-2026-10-15).

> **Bambu-oplevering (2026-10-15):** de originele X1 Carbon/0,4-mm/PLA-3MF is volgens de eigenaar zonder wijzigingen geprint. Het opgeslagen profiel en de slicerpadvalidatie staan in [bambu-settings.md](bambu-settings.md). Werkelijke printerinstellingen zijn niet afzonderlijk uit de machine geverifieerd.

> **Printsteunen:** de dunne externe voetjes waren bewust in de CAD geïntegreerd voor bedhechting (niet door de slicer gegenereerde supports of brim). De eigenaar vond het verwijderen lastig; dit is een open vraag voor maakbaarheid en assemblage, ook al werkt de draadpassing.

**Status:** COMPLETED  
**Prioriteit:** afgerond (voorheen P1)  
**Laatst beoordeeld:** 2026-10-15  
**Reden:** de eigenaar heeft alle vijf compacte schroef-pinparen fysiek getest; de drie identieke nominale 0,175-mm-paren voldeden alle aan de handmatige passing- en vijfcycli-eis. Ontwerp van printvoetjes en onafhankelijke aandrijving blijven onbewezen.

**Technische bron:** [E-295 — compacte geometrie en bewijs](../../tools/curated-experiment-checks/E-295/research/compact-geometry.md), voortbouwend op [short-thread-fit](../2026-10-14-short-thread-fit/test.md) en het originele Trial 5.

## 1. Waarom deze test? — CTO

**Vraag:** kunnen 4,4-mm vierkante pinnen met 6 mm binnendraad onderaan even prettig heen en terug bewegen als de eerdere brede testmoeren, zonder binnendraad-supports of schuren? Drie nominale exemplaren tonen eventuele printspreiding.

**Vooraf vastgelegde beslisregel:** drie bruikbare nominale paren rechtvaardigen een kleine onafhankelijke bewegingsdemonstratie. Wisselende nominale resultaten vragen eerst verklaring; alleen succes van de ruimste variant is geen bewijs voor betrouwbare productie. De plaat bewijst geen 40-mm slag, draagkracht of levensduur.

**Afkeur/stop:** harde blokkade, scheuren, loskomende lagen, scheefgeprinte schroef of functionele draad die gevijld/gesneden moet worden. Geen tang, boormachine of krachtproef; stop zodra het blokkeert. Een mislukte variant is een bruikbaar resultaat, geen reden om haar passend te forceren.

## 2. Printklaar — CTO

| Bestand / verwijzing | Inhoud | Herkenning |
|---|---|---|
| [**Bambu Studio-project**](compact-five-pairs.3mf) | Compleet X1C/0,4/PLA-project met opgeslagen instellingen en geslicede paden | Zie [exact profiel en Bambu-controle](bambu-settings.md) |
| [**compact-five-pairs.stl**](compact-five-pairs.stl) | Complete plaat: vijf schroeven en vijf holle pinnen, tien losse delen | 1–5 stippen op beide voeten; behoud de plaatvolgorde |
| [plate-preview.png](plate-preview.png) | Afbeelding van exact dezelfde STL | Geen montagepositie: alle delen staan apart op het bed |
| [coupon.scad](coupon.scad), [thread-kernel.scad](thread-kernel.scad), [generate.py](generate.py) | Reproduceerbare bron; pinned BOSL2 vermeld in bron | **Niet nodig om te printen** |
| [geometry-validation.json](geometry-validation.json) | Maatvoering, mesh-, volume- en passingchecks | CAD-bewijs, geen fysieke test |

- **Printjobs:** één plaat; geen extra kopieën of brede moeren nodig.
- **Varianten:** 1, 2, 3 identiek: **0,175 mm radiale CAD-relief**; 4: **0,15 mm**; 5: **0,20 mm**. Alle buitenschroeven zijn functioneel identiek. Dit is geen gemeten printercorrectie. Minimale wand bij de drie toleranties: 0,425/0,450/0,400 mm; bovenholtewand 0,44 mm.
- **Geometrie:** buitenschroef d 3,2 mm, spoed 3, diepte 0,9, 90°-profiel uit de recente geslaagde test; draad 16 mm boven een 10 × 10 × 2,4-mm handgreep. Pin 4,4 × 4,4 × 18 mm, binnendraad onderste 6 mm, overige holte 3,52-mm vierkant; bovenkant open voor inspectie. Buitenvoet 12 × 12 × 0,24 mm, geen support in het gat. Hele plaat **72 × 27 × 18,4 mm**.
- **Materiaal/printer:** gewone PLA die je al hebt; Bambu Lab X1 Carbon, **0,4-mm nozzle**, schaal 100%. Geen aankoop nodig.
- **Slicer:** Bambu Studio met **Arachne-wandgenerator**; laaghoogte én eerste laag **0,12 mm**. Twee wanden, 100% infill voor de kleine massieve delen. Nominale lijnbreedte 0,45 mm; laat Arachne dunne wanden variabel vullen. Buitenste/kleine perimeters maximaal 30 mm/s; eerste laag 20 mm/s; acceleratie maximaal 1000 mm/s². Opgeslagen PLA-profiel: 220 °C nozzle, 55 °C Textured PEI Plate, flowratio 0,98, partfan 100% na de eerste laag, auxfan 0%; korte-laagvertraging aan (8 s, minimaal 10 mm/s). Geen XY-/gat- of elephant-foot-compensatie toevoegen voor deze vergelijking; noteer aanwezige compensaties.
- **Oriëntatie:** rechtop zoals geleverd; niet automatisch draaien. Print per laag, niet object-na-object. Alle tien delen moeten het bed raken.
- **Supports/brim:** **alle supports UIT, automatisch brim UIT, geen raft.** De ontworpen 0,24-mm pinvoet is al de buitenbrim. Er hoeft niets uit het gat te worden verwijderd. Laat de voet tijdens de passingtest zitten; dit voorkomt beschadiging van de dunne wand bij losknippen.
- **Preview:** controleer dat de bovenste vierkante buiswanden aanwezig zijn, alle schroefdraden worden geprint en alle vijf binnengaten open blijven. Geen enkel supportpad hoort in de holte. In de onderste draadzone blijven lokale Arachne-lijnonderbrekingen; de Bambu-padcontrole vindt maximaal circa 0,224 mm langs een nominale wandmiddellijn (geen gemeten fysiek gat): die zijn op de vorige laag ondersteund, maar kunnen kleine gaatjes of zwakke plekken geven. Inspecteer en noteer die na het printen; geen draad nabewerken. Ontbreekt een groot wanddeel of begint een eiland zonder ondersteuning, print dan niet met dat profiel en bewaar de preview. De meegeleverde bron hoeft niet opnieuw geëxporteerd te worden.
- **Bambu Studio 02.08.02.61:** **1 uur 1 min 40 s totaal geraamd / 3,37 g / 1,128 m PLA**, waarvan 50 min 25 s modelprinttijd; 153 lagen. De raming komt uit de daadwerkelijk meegeleverde X1C-G-code met officiële startprocedure, niet uit een fysieke print. Werkelijke opwarm-/kalibratietijd, purge en verbruik kunnen afwijken. Het eerdere PrusaSlicer-resultaat (42 min / 3,17 g) blijft uitsluitend een historische vergelijking. Zie [Bambu-validatie](bambu-settings.md).
- **Extra:** handen en liefst een gewone liniaal. Bewaarde onderdelen van short-thread-fit zijn optioneel voor vergelijking, geen nieuwe brede print.
- **Eerdere CAD-/PrusaSlicer-controle:** 2026-10-15: tien gesloten afzonderlijke meshes; 305 coaxiale montagestanden zonder CAD-botsing. Exacte plaat met supports uit én aan gesliced: geen support-, brug- of overhangpaden. Onafhankelijke controle van 153 lagen: geen nieuw los deel zonder overlap met de vorige laag. De bovenste buiswand is doorlopend in de paden; onderin blijven de genoemde kleine lijnonderbrekingen. Dat onderbouwt de ontworpen korte print, maar bewijst geen fysieke hechting, laagsterkte of passing. Zie [exacte sliceruitvoer en profiel](../../tools/curated-experiment-checks/E-295/validation/compact-arachne.json), [laagbeelden](../../tools/curated-experiment-checks/E-295/validation/compact-toolpaths.png) en [detail van een lokale lijnonderbreking](../../tools/curated-experiment-checks/E-295/validation/compact-local-bead-gap.png).

**Historische printinstructie (proef inmiddels afgerond):** open [**compact-five-pairs.3mf**](compact-five-pairs.3mf) als **project** in Bambu Studio en behoud het meegeleverde profiel. Het oorspronkelijke STL blijft beschikbaar. Je hoeft geen CAD of Python te compileren. Deze proef is vrijblijvend, zonder deadline. De bestaande grote test is afgerond; deze plaat stelt de nieuwe vraag naar compactheid.

## 3. Test in enkele stappen — CTO

1. Laat afkoelen en neem alle delen rustig van de plaat. Houd paren 1–5 bij elkaar. **Laat de brede dunne pinvoetjes zitten.** Kijk door de open buis en noteer losse voet, scheefstand, ontbrekende draad, gaten, scheuren of stringing. Alleen loshangende draadjes verwijderen; geen draad bijschuren of uitboren. Noteer iedere nabewerking.
2. Houd de pin bij haar printvoet, zodat je de dunne buis niet samenknijpt. Steek de schroefpunt vanaf de voetkant recht in de binnendraad. Draai voorzichtig; even terugdraaien om de draadstart te vinden mag. Niet drukken of een verkeerde draadstart doordraaien.
3. Draai tot de vrije axiale afstand tussen **bovenkant schroefhandgreep en onderkant pinvoet ongeveer 6 mm** is. De schroef steekt dan circa 10 mm in de pin. Draai één omwenteling uit tot ongeveer 9 mm afstand, en terug. Dat is circa 3-mm beweging met de volledige 6-mm binnendraad nog in aangrijping. Draai niet tegen de voet en niet bijna volledig los. Herhaal **vijfmaal heen en terug**. Houd de pin tegen rotatie en draai de schroef: zo blijft het gekozen schroef-staafprincipe zichtbaar.
4. Noteer per paar start, soepel/lichte weerstand/stroef/vast, voelbare speling en schade. Bij verschillen tussen 1–3: probeer pin 1 op schroef 2 en 3. Zo wordt zichtbaar of weerstand vooral met de pin of de schroef meeverhuist. Geen belastings- of breuktest.
5. **Optioneel, als de oude onderdelen bewaard zijn:** probeer compacte pin 5 op dezelfde oude schroef waarop de brede 0,20-mm moer zo soepel liep. Vergelijk ook die brede moer op diezelfde schroef. Noteer richting en gevoel. De draadprofielen zijn nominale matches; de contactlengtes 6 tegenover 10 mm en handgrepen verschillen, dus dit is een nuttige kwalitatieve vergelijking, geen wrijvingsmeting of bewijs dat alleen de compactheid een verschil veroorzaakt.

**Succes:** alle drie nominale paren starten zonder kracht, bewegen vijfmaal heen/terug op volle draadgrijping en blijven intact zonder nabewerking van de draad. Voelbare variatie mag worden gerapporteerd; zij wordt niet gemiddeld weggeschreven. “Even soepel als het oude paar 5” is een waarneming, geen gemeten motorbelasting.

**Onbekend:** gesloten top, externe geleiding, buurbeweging, belasting, zelfremming, lange-schroefstabiliteit, 40-mm slag, snelheid, slijtage en opbrengst van duizenden onderdelen. De tijdelijke 12-mm pinvoeten passen niet in het raster. Eventueel **na** alle passingtesten alleen aan de buitenkant vlak afknippen is een afzonderlijke observatie over verwijderbaarheid; trimmen is niet nodig voor deze proef en succes ervan wordt niet verondersteld.

## 4. Mijn resultaten — Sander (eigenaarrapportage 2026-10-15)

**Testdatum:** 15 oktober 2026 (datum zoals door eigenaar opgegeven).  
**Printer / PLA / nozzle / laaghoogte / wandgenerator:** eigenaar meldt *"Originele 3MF zonder wijzigingen"*. Het opgeslagen project is ingesteld op Bambu Lab X1 Carbon, Generic PLA, 0,4-mm nozzle, 0,12-mm lagen, Arachne, twee wanden. Dit zijn bevestigde gebruikte **projectkeuzes volgens de eigenaar**, geen afzonderlijk nagemeten machine-instellingen of filamentidentificatie.  
**XY-/gat-/elephant-footcompensatie:** originele 3MF niet aangepast; daarin staan alle drie op 0 mm.  
**Werkelijke printtijd / materiaal:** niet gerapporteerd (de raming in §2 is geen meting).  
**Print gelukt?** [x] ja [ ] deels [ ] nee.  
**Handtest:** volgens de eigenaar starten alle vijf paren zonder kracht en voltooiden ze alle vijf de voorgeschreven heen-en-terugcycli. Exacte draaikracht, voelbare speling en gemeten verplaatsing zijn niet afzonderlijk gekwantificeerd.

| Paar | Radiale CAD-relief | Print intact / functionele opening? | Start zonder kracht? | Vijf handcycli? | Gevoel en opmerkingen van eigenaar |
|---|---:|---|---|---|---|
| 1 — nominaal | 0,175 mm | Ja / draad kan starten | Ja | Ja | "Supersoepel, heel weinig kracht nodig." |
| 2 — nominaal | 0,175 mm | Ja / draad kan starten | Ja | Ja | "Supersoepel, heel weinig kracht nodig." |
| 3 — nominaal | 0,175 mm | Ja / draad kan starten | Ja | Ja | "Supersoepel, heel weinig kracht nodig." |
| 4 — krapper | 0,15 mm | Ja / draad kan starten | Ja | Ja | In het begin stroef; na enkele omwentelingen soepel met lichte weerstand. |
| 5 — ruimer | 0,20 mm | Ja / draad kan starten | Ja | Ja | Heel soepel; volgens eigenaar mogelijk nog net soepeler dan 1–3, maar moeilijk te onderscheiden. |

**Printschade / draadnabewerking:** alle paren als print-intact gerapporteerd; geen draadschade of draadnabewerking gemeld. Draadnabewerking is niet apart uitgevraagd; laat "niet gemeld" niet doorgaan voor een afzonderlijk gecontroleerd nulresultaat. Visuele gatencontrole en axiale speling zijn niet afzonderlijk gerapporteerd.  
**Kruisproef pin 1 op schroef 2/3:** niet gerapporteerd; geen merkbare onderlinge verschillen bij 1–3 waarvoor foutlokalisatie nodig zou zijn.  
**Vergelijking met bewaarde brede test:** geen nieuwe kruisproef gerapporteerd. In de [eerdere brede test](../2026-10-14-short-thread-fit/test.md) voelde 0,20 mm het soepelst, terwijl de drie nominale 0,15-mm-paren meer uiteenliepen. De nieuwe compacte test gebruikt andere nominale speling, pinvorm, ingrijplengte en printprofiel; oorzaken zijn dus niet geïsoleerd.  
**Bedhechting / verwijderbaarheid van de pinvoeten:** eigenaar meldt dat de printer voetjes onder de pinnen heeft geprint voor bedhechting, maar dat die lastig te verwijderen zijn. Technisch zijn dit de **in de CAD ontworpen externe voetjes van 12 × 12 × 0,24 mm**, geen automatisch gegenereerde slicer-brim of supports. Of ze allemaal verwijderd zijn, hoeveel kracht dit vraagt en of verwijderen de dunne wand kan beschadigen, is niet gemeten of afzonderlijk gerapporteerd.  
**Suggestie eigenaar:** bij een volgende uitvoering mogelijk de schroefdraad bovenaan printen zodat het voetprobleem verandert/verdwijnt. **Nog geen ontwerpbesluit:** omgekeerd oriënteren kan de bedhechting, wandstabiliteit, draadkwaliteit of noodzaak van buitenste steun veranderen. Vergelijk dit later met eenvoudig afneembare externe steunen, zonder nu extra printtests te starten.  
**Foto / video:** niet aangeleverd.

## 5. Interpretatie en vervolg — CTO (na eigenaarresultaat 2026-10-15)

**Fysiek handpassingsresultaat: GO.** Vijf van vijf compacte paren starten zonder kracht en maken vijf heen-en-terugcycli; de drie identieke nominale 0,175-mm-paren zijn volgens de eigenaar alle drie uitzonderlijk soepel, met weinig handkracht. De vooraf vastgelegde drempel voor doorgaan naar een kleine **onafhankelijk bewegende vierpins-demonstratie** is daarmee op deze ene printplaat gehaald. Dit is sterk positief bewijs dat de recente draadgeometrie ook in 4,4-mm vierkante pinnen handmatig functioneert, anders dan de eerdere 10,3-mm brede moeren die nog niet binnen het raster pasten.

**Voorlopige tolerantiekeuze voor een eventuele vierpins-proef: 0,175 mm radiale CAD-relief.** Drie identieke exemplaren zijn goed en onderling consistent. 0,15 mm vraagt aanvankelijk merkbaar meer kracht en lijkt tijdens gebruik in te lopen; mogelijk spelen oppervlakteruwheid of micro-onregelmatigheden mee, maar dit is niet gemeten. 0,20 mm voelt mogelijk een fractie soepeler, maar de eigenaar kan dat niet duidelijk onderscheiden. Een grotere relief kan ook meer speling veroorzaken. Daarom is **0,175 mm de praktische eerste kandidaat**, geen definitief productieoptimum. De drie identieke samples geven een gunstig signaal voor reproduceerbaarheid **binnen één printplaat**, niet over printers, batches of duizenden pinnen.

**Nieuw maakbaarheidspunt: tijdelijke voetjes.** Het verwijderen van de CAD-bedhechtingsvoetjes is lastig. Dit doet niets af aan het geteste schroefcontact, maar is relevant voor dunne wanden, mogelijke beschadiging bij nabewerking en montage van duizenden pinnen. Het idee om de draad bij het printen bovenaan te plaatsen is een ontwerpoptie, niet automatisch een betere oriëntatie. Evalueer voet-/brimontwerp en printoriëntatie pas gericht in het ontwerp van een eventuele vervolgproef; dwing of snijd bij deze proef geen voetjes weg om extra succes te claimen.

**Grenzen van het bewijs:** geen gemeten motorkoppel, backlash, axiale houdkracht, slip/zelfremming, last van een miniatuur, onafhankelijke buurbeweging, aan-/ontkoppeling van een aandrijfkop, lange schroeven/40-mm slag, uithouding of productieopbrengst. De rapportage verifieert de opgegeven onveranderde 3MF, maar de werkelijke instellingen en printtijd zijn niet uit de printer uitgelezen.

**Besluit en stopconditie:** status **COMPLETED** voor deze passingvraag. De reeds uitgewerkte [vierpins-demonstratie](../2026-10-15-four-pin-screw-demo/test.md) is technisch de logische volgende *keuzemogelijkheid* met de 0,175-mm-variant; zij is hiermee niet automatisch geprint, geactiveerd of gevalideerd. Geen nieuwe printopdracht of bredere serie zonder expliciet eigenaarsbesluit.
