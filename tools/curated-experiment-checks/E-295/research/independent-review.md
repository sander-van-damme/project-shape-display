# Onafhankelijke kritische beoordeling

Deze beoordeling probeert de voorstellen in E-295 te weerleggen op concrete geometrie, selectiviteit, ondersteuning en timing. Zij is geen fysieke goedkeuring. Reviewer werkte afzonderlijk van de CAD- en actuatieonderzoekers; bevindingen zijn rechtstreeks aan hen teruggekoppeld.

## Bewijsbasis en harde grenzen

- Het eigenaarrapport van 14 oktober toont vijf bruikbare **brede** handgedraaide draadparen. De 0,20-mm radiale CAD-speling voelde het best; 0,15 mm verschilde tussen drie nominale exemplaren. Geen van deze waarnemingen meet draaimoment, slijtage, houdkracht of de passing van een 4,4-mm pin.
- De historische compacte Trial 5-familie heeft positieve eigenaarervaring. De recente replica is door achtergebleven support **niet functioneel getest**. Beide feiten moeten naast elkaar blijven staan.
- Een doorlopende schroef en korte binnendraad blijven het werkingsprincipe. Een tegenvallende aandrijfkop verwerpt uitsluitend die koppeling, niet de schroefarchitectuur.

## Aanvallen op de aandrijfvoorstellen

### Onderzijdige XY-kop: kansrijk, maar aankoppeling is een echte mechanische stap

Een 2-mm inbuspunt heeft een omgeschreven straal van 1,155 mm. In een 3-mm AF ingangstrechter is de conservatieve eerste vangruimte slechts 1,5 − 1,155 = **0,345 mm**. Een 2,2-mm AF rechte zeskant geeft tegenover de 2-mm punt slechts **0,10 mm normale speling per vlak**. Verende laterale slag in de kop is geen vervanging voor die eerste vangruimte: de punt moet eerst binnen de trechter vallen. Scheefstand, printmaat, plaatdoorbuiging, assenregistratie en temperatuur nemen allemaal ruimte uit dezelfde marge.

De voorgestelde punt kan binnen 5,08-mm pitch blijven: bij een 4,4-mm buurcollar en 0,20-mm benaderfout resteert nominale afstand 5,08 − 2,2 − 1,155 − 0,20 = **1,525 mm** tot de buurcollar. Dit geldt alleen voor de uitstekende punt; grotere lagers, motor, vering en koppelbegrenzer moeten onder het vlak van alle andere koppen blijven.

Een ondersluitplaat met opening 3,6 mm laat een zeskanttrechter van 3 mm AF (3,464 mm over hoeken) slechts 0,068 mm radiaal vrij. Tegelijk moet die plaat de 4,4-mm collar axiaal vasthouden. Een ruimere opening vergroot de toegang en verkleint de dragende overlap. Het eerste demonstratiemodel moet deze twee functies werkelijk bevatten; alleen een vrijstaande schroef die met de kop mee omhoog komt bewijst geen bruikbare aandrijving.

Onbekende hoekstand is geen nul-tijdstap. Bij een zeshoek en 60 rpm ligt één theoretische 60°-zoekperiode al op 0,167 s; aanrijden, contact, zoeken, zakken, bevestigde krachtoverdracht en terugtrekken komen daarbij. Daarom blijven de tijdscenario's expliciet aannames tot de handproef en vervolgens een gemotoriseerde koppeling ze meten.

### Rijbank: complexiteit verplaatst naar enkele koppen, maar verdwijnt niet

Een rijbank met bijvoorbeeld 8–16 afzonderlijk inschuifbare punten kan de vaste onderdelen per schroef eenvoudig houden. Iedere actieve punt moet echter onafhankelijk terugtrekken terwijl de gemeenschappelijke roterende as blijft draaien. Dat vraagt per **kop**, niet per pin: axiale geleiding, een blijvende roterende verbinding, selectiemechanisme en veer/retourkracht. Motoren, actuatoren en servos moeten in de systeemrekening afzonderlijk zichtbaar blijven.

Een 4,0-mm cup bij 5,08-mm pitch heeft 1,08 mm nominale tussenruimte. Met twee tegengestelde positioneerfouten van 0,15 mm blijft 0,78 mm; niet genoeg om een conventioneel lager plus huls in dezelfde doorsnede te veronderstellen. De kop mag naar onderen en in rijrichting verbreden; de bovenzijde blijft maatkritisch.

Een loutere frictiecup is geen automatisch eenvoudige oplossing. Bij effectieve radius 1,36 mm, aangenomen wrijving 0,3 en 2 mN·m schroefmoment vraagt één cup ongeveer **4,9 N** aandrukkracht. Tachtig tegelijk leveren circa **392 N** aan de draagplaat. Dit is geen gemeten moment, maar toont waarom een positieve koppeling met begrenzing in de kop de voorkeur kan hebben boven onbegrensd harder aandrukken.

### Globale homing: een gemeenschappelijke koppelgrens begrenst niet elke pin

Een starre aandrijfas met één motorstroomlimiet kan niet alle verschillende hoogtes veilig tegen hun eindstop zetten: de eerste vastgelopen schroef kan de hele groep stoppen, of plaatselijk veel meer dan het veilige pinmoment ontvangen. Elke tegelijk actieve tak heeft een veilige slip- of ontkoppelweg nodig. Een rijbank hergebruikt deze voorzieningen; duizenden permanente slipkoppelingen zouden juist de herhaalde complexiteit verhogen.

Voor iedere actieve kop blijft het noodzakelijke venster **maximaal normaal loopmoment < minimaal slipmoment < minimaal schadelijk blokkeermoment** fysiek onbekend. De kleine passingtest mag dat venster niet uit handgevoel afleiden. Een eindstop moet vóór draaduitloop liggen; draad los laten draaien is geen homing die daarna vanzelf betrouwbaar omkeert.

### Ongekoppelde schroef: houdgedrag verdient een eenvoudige belastingswaarneming

Bij spoed 3 mm en benaderde flankdiameter 2,3 mm is de spoedhoek ongeveer 22,5°. Voor een ideaal 90°-V-profiel ligt de theoretische zelfremgrens rond μ ≈ tan(22,5°)·cos(45°) = **0,29**, vóór het effect van collar-/taatswrijving. Daarom is “een schroef houdt vanzelf” geen bewijs. Een lichte bekende last en kort kijken naar spontaan terugdraaien volstaan in deze fase; uitgebreide driftinstrumentatie is niet nodig.

## Compactheid, tops en geleiding

De compacte variant behoudt 4,4 mm buitenbreedte, terwijl een 3,2-mm buitendiameter met 0,20-mm radiale relief nog maximaal 0,40 mm wand op de vlakke zijde laat. De werkelijke facet- en slicergeometrie moet gecontroleerd worden; zo'n wand is ongeveer één extrusielijn. Meer walls instellen maakt een geometrisch dunne wand niet dikker.

Vierkante tops vergroten zonder de geleiding te wijzigen is onveilig. Een vierkante 4,4-mm pin in een 4,7-mm vierkant gat kan tot ongeveer 4,05° verdraaien. Een 4,88-mm top krijgt dan een geprojecteerde breedte van circa 5,21 mm, boven de pitch van 5,08 mm, nog zonder laterale speling. Daarom gebruikt de kleine demonstratie voorlopig dezelfde 4,4-mm vierkante top als het geleide lichaam. Dit is een geometrische correctie, geen voorkeur voor blijvend zichtbare brede voegen.

De eerste demonstratieschets had 4,7-mm gaten op slechts 6 mm afstand: 0,30-mm verschil in laterale positie gaf circa 2,86° mogelijke kanteling. Dit is naar aanleiding van de review gewijzigd naar **4,6-mm gaten en 10,2-mm afstand tussen de middelvlakken**. De maximale tophoogte inclusief 0,30-mm axiale collarspeling is 32,0 mm; het bovenste geleidemidden ligt op 24,8 mm, dus h = 7,2 mm.

Gecombineerde verdraaiing/kanteling mag niet worden berekend door twee onafhankelijk onmogelijke maxima op te tellen. Bij yaw θ is de geprojecteerde breedte w = 4,4(cos θ + sin θ); de resterende laterale ruimte is 4,6 − w. De uiterste topzijde ligt op 4,6/2 + h(4,6 − w)/10,2 vanaf de celas. Het grootste bereik ontstaat bij θ = 0: minimale nominale buurafstand = 5,08 − 4,6 − 2·7,2·0,2/10,2 = **0,198 mm**, of circa 0,196 mm met een kleine extra sectieprojectie door kanteling. Yaw alleen geeft een grotere restafstand. Deze positieve nominale marge bewijst geen fysiek botsingsvrije array: bijvoorbeeld een 0,10-mm groter gat gecombineerd met een 0,05-mm smallere pin zou de rekenmarge al negatief maken. Zulke afwijkingen zijn gevoeligheidsscenario’s, geen gemeten printerspreiding. De demonstratie moet op uiterste standen naar contact, binden en buurbeweging kijken.

## Onafhankelijke printcontrole

De exact geleverde STL’s en echte PrusaSlicer 2.7.2-paden zijn afzonderlijk gecontroleerd; de uitvoer en het reproduceerbare profiel staan hieronder. De vergelijking gebruikt een 0,4-mm nozzle, 0,12-mm lagen en expliciete lijnbreedten. Het is geen gekwalificeerd Bambu-machineprofiel en de gegenereerde vergelijkings-G-code wordt niet aan de eigenaar als printprogramma geleverd.

Het controleprogramma reconstrueert extrusievoetafdrukken uit XY/E, kijkt naar alle lagen en meldt nieuw beginnende componenten zonder overlap met de vorige laag. Dat kan zwevende eilanden vinden. Het bewijst geen bedhechting, voldoende overlap bij zijdelingse krachten, thermische werking of fysieke draadpassing. Die beperkingen zijn onderdeel van het resultaat.


### Compacte plaat: controle afgerond, één READY-proef

- Exacte STL: `compact-five-pairs.stl`, SHA-256 `478d9087e4f566126f7ec21d8f4b9ac374546707f80fec7272b699bb4b83b56c`.
- Onafhankelijk geladen: **10 afzonderlijke gesloten lichamen**, correcte winding, 72 × 27 × 18,4 mm, 2.538,162 mm³ solid volume.
- Arachne: **153 lagen**, 42m11s / 3,17 g in het vergelijkingsprofiel. Nul support-, brug- of overhangrollen. Een extra slice met automatische supports aan gaf eveneens nul supportpaden. Dit is uitsluitend een diagnostische vergelijking; de eigenaar print met supports **uit**.
- Bij alle lagen is ieder extrusiecomponent groter dan 0,005 mm² verbonden met de vorige laag. Er zijn geen nieuw in de lucht beginnende onderdelen. De 12 × 12-mm buitenvoeten zijn daadwerkelijk op de eerste twee lagen aanwezig; het gat blijft open.
- Bij **750 pin/laagcombinaties** blijft de centrale cirkel van 0,60-mm radius vrij van gedeponeerd materiaal. Alle 495 onderzochte bovenbuis-secties (Z > 6,12 mm) hebben een gesloten wandlus in de gereconstrueerde extrusievoetafdruk.
- **Beperking gevonden:** bij dunne draadwanden onderin maakt Arachne soms kleine onderbrekingen bij de overgang van twee lijnen naar één lijn. In 110 onderzochte draadzone-secties is de nominale wandvoetafdruk lokaal niet geheel gesloten. De grootste gesommeerde onderbreking langs het gecontroleerde wandmidden is 0,255 mm; een detail toont twee kleine gaten rond een kort lijnstuk. Dat lijnstuk heeft wel steun op de vorige laag. Dit is een toolpathbevinding, geen gemeten gat in een fysieke print. Het handoffformulier vermeldt nu expliciet mogelijke kleine gaten/zwakke plekken, zonder deze met grote ontbrekende wanden of zwevende onderdelen te verwarren.
- Classic, 0,40-/0,42-mm lijnbreedte en verkorte Arachne-overgangen zijn gescreend; die elimineren deze onderbrekingen niet. De aanbevolen vergelijking blijft **Arachne / 0,45-mm nominale breedte**. De eigenaar moet de dunne draadzone na printen beoordelen. Het doel van de kleine plaat is juist de werkelijke werking en integriteit vaststellen; een verdere geometriewijziging vóór deze proef is niet bewezen nodig.

Bewijs: [Arachne-resultaat](../validation/compact-arachne.json), [Classic-vergelijking](../validation/compact-classic.json), [supports-aan-diagnose](../validation/compact-support-on.json), [wandcontrole](../validation/compact-wall-review.json), [laagbeelden](../validation/compact-toolpaths.png), [lokale lijnonderbreking](../validation/compact-local-bead-gap.png).

### Vierpins-demonstratie: alle drie varianten gesliced, DEFERRED

Alle drie complete variantplaten zijn afzonderlijk geladen en gesliced met **3-mm uitsluitend externe brim, brimafstand 0, supports uit, Arachne en 0,12-mm lagen**. Iedere plaat heeft 12 gesloten lichamen, 60 × 65 × 24 mm en 200 lagen. Alle nieuw gedeponeerde componenten hebben overlap met de vorige laag; dit sluit lokale bruggen en hun beperkingen niet uit.

| Radiale relief | Exacte SHA-256 van STL | Vergelijking tijd / massa |
|---|---|---|
| 0,15 mm | `4198ca22483ab9a370b7006f3647f5ec6994f48a7f45e19903aa80f91f563142` | 1h42m06s / 9,39 g |
| 0,175 mm | `9c6cb2402bd494cf028ec13353b2a0ca2df32d3ac5e6938b8c4240670fb763cc` | 1h42m03s / 9,38 g |
| 0,20 mm | `ad53ba20d710ee06724462af2f314526140c9d88975454c4b375db76a51d3981` | 1h42m05s / 9,37 g |

De brim geeft de 4,4-mm voet van de staafjes/schroeven circa 10,4 mm totale bedbreedte; de grote zijwand van de liggende kooi steunt rechtstreeks op het bed. Dat is een werkelijke bedsteun in de paden, geen voorspelling van PLA-hechting of bewijs van stabiel printen bij een bepaalde nozzle-zijkracht. De 18–21,5-mm fijne onderdelen blijven korte proeven.

**De slicer geeft wel waarschuwingen:** “Floating bridge anchors, Loose extrusions, Long bridging extrusions.” Die zijn niet verborgen. De zijwaarts geprinte kooi bevat een daklijn van 18,34 mm die tussendoor op het middelste geleidevlak steunt; de grootste werkelijk vrije centrumlijnspan boven de vorige laag is **8,98 mm**, niet 18,34 mm. Andere vrije spans zijn 4,20 mm bij de geleidegaten, 2,64 mm in de top-infill van de pin, 3,10 mm bij de top-overhangperimeter en 2,22 mm bij de hex-socketroof.

Sommige brug-infill begint op een **eerder in dezelfde laag geprinte brugperimeter**, niet rechtstreeks op de vorige laag; de grootste eindpuntafstand tot vorige-laagmateriaal is 1,515 mm bij het kooidak. Er zijn dus reële brugankers die steun van eerder gedeponeerde bruglijnen nodig hebben. Daarom is “alle paden volledig ondersteund” onjuist. Het ontwerp vermijdt supportmateriaal in draad en socket, maar brugdoorhang en kleine geleideopeningen moeten fysiek worden beoordeeld. De test blijft DEFERRED, met expliciete preview- en stopinstructies; geen directe tweede actieve printopdracht en geen automatische inschakeling van supports.

Bewijs: [0,15](../validation/demo-015.json), [0,175](../validation/demo-0175.json), [0,20](../validation/demo-020.json), [slicerwaarschuwingen](../validation/demo-slicer-warnings.txt), [brugdetails](../validation/demo-bridge-details.json), [laagbeelden](../validation/demo-toolpaths.png).

### Timingreview en gevolgen

De onafhankelijke review vond dat een axiaal geselecteerde rijbank voor gemengde op/neerbeweging niet alle punten eenmaal kan aankoppelen en daarna slechts de motorrichting omkeren: de punten voor de andere richting moeten nog vrij staan en vervolgens opnieuw fasezoeken/aankoppelen. De bijgewerkte systeemstudie rekent daarom **een aankoppelhandeling per richtingspass**.

Ook is 0,05 s ontkoppelvertraging bij 600 rpm en 3 mm spoed gelijk aan **1,5 mm** doorgaande verplaatsing; 0,15 s volledige terugtrekking is 4,5 mm. Voorspelbare vertraging is eventueel te compenseren, maar koppeling onder belasting kan haken of slijten. De systeemstudie bevat nu een afzonderlijk conservatiever scenario: de bus stopt bij iedere gewenste hoogte, de bereikte kop(pen) trekken terug en de resterende koppen starten opnieuw. Alleen de gunstige continu-doordraaiende procesondergrens tonen zou het onopgeloste selectiemechanisme verhullen.

### Reproductie

Het [vergelijkingsprofiel](../validation/comparison-012.ini) gebruikt 0,4-mm nozzle, 0,12-mm eerste/overige lagen, 0,45-mm nominale lijnen, twee wanden, 100% infill, 30 mm/s buiten-/kleine perimeters en 1.000 mm/s² acceleratie. Het bevat geen gekwalificeerde X1C-startcode. Printtijd is exclusief echte machinevoorbereiding en standaard PLA-laagkoeling kan langer duren.

Vanuit de repositoryroot, met een beschikbare PrusaSlicer 2.7.2:

```sh
prusa-slicer --load tools/curated-experiment-checks/E-295/validation/comparison-012.ini --threads 2 --perimeter-generator arachne --export-gcode --output work/compact-comparison.gcode owner-print-tests/compact-screw-fit/compact-five-pairs.stl
python tools/curated-experiment-checks/E-295/independent_toolpath_review.py --stl owner-print-tests/compact-screw-fit/compact-five-pairs.stl --gcode work/compact-comparison.gcode --output work/compact-review
python tools/curated-experiment-checks/E-295/compact_wall_review.py --gcode work/compact-comparison.gcode --output work/compact-wall-review.json
```

Voor een demoplaat voeg je `--brim-width 3 --brim-type outer_only` toe; controleer de bruggen met [bridge_review.py](../bridge_review.py). De audit gebruikt numpy, trimesh, shapely en matplotlib. De gegenereerde G-code blijft in `work/` en is uitsluitend berekeningsinvoer, geen geleverde machinecode. Alle vastgelegde STL-hashes horen bij de exacte geleverde meshes; genereren of herschrijven vereist een nieuwe vergelijking.

De bewaarde JSON-bestanden bevatten compacte samenvattingen en de zwaarste bruggevallen per laag/rol. Volledige laag- en segmentrecords worden door bovenstaande controles in `work/` gereproduceerd; [summarize_validation.py](../summarize_validation.py) maakt daaruit de opgeslagen samenvattingen. Zo blijven de belangrijke fouten en hashes controleerbaar zonder ruwe scratchuitvoer in de repository.

### Integratiecontrole

De hoofdagent heeft de compacte CAD opnieuw uit bron gegenereerd (305 montagestanden plus zes kruiscontroles), de drie demo's opnieuw op 150 montagestanden gecontroleerd en de timing-JSON onafhankelijk gereproduceerd. Alle lokale documentlinks en de zes opgeslagen slicercontroles matchen de definitieve STL-hashes. `git diff --cached --check` is schoon. `./repo check` op een schone export van de voorgestelde wijzigingen geeft exact dezelfde vijf bestaande omvangsmeldingen als uitgangscommit `117549a`: E-266, E-283, E-286, E-288 en E-293. Er zijn geen nieuwe structuurmeldingen; die historische documenten zijn buiten deze opdracht niet herschreven.
