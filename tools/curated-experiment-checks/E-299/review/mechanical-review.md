# Onafhankelijke mechanische beoordeling E-299

Beoordelaar: afzonderlijke Codex-subagent. Dit verslag is CAD-/analysebewijs; er zijn geen nieuwe fysieke uitslagen.

## Keuzes vooraf

De volledige eigenaarsfeedback van E-298 is gelezen, inclusief de aanvullende montage- en modulevoorstellen. De beperkte eigenaarstest toont afzonderlijk onvoldoende sluiting door selectorvervorming/slag en blokkering bij punt-op-punt. Scherpere identieke statische punten geven geen garantie tegen een dode symmetrische fase. Daarom is een begrensde inputfasezoekbeweging onder lichte selectiedruk een bewust, expliciet compromis. Zij telt niet als passieve zelfuitlijning met stilstaande inputs.

Een 1×2-coupon is de kleinste zinnige vervolgstap die een gedeelde selector én een onaangedreven buur bevat. Een 1×1-coupon kan die vraag niet beantwoorden; een 2×2 voegt voor deze sluitings-/printproef onnodig veel delen toe.

Een vaste centrale staaf vraagt een doorgaand gat in de huidige DD-aandrijving. Bij 1,60-mm flats en een 1,00-mm boring blijft slechts 0,30-mm wand over. Dat is voor de 0,4-mm nozzle geen robuuste aandrijving. Deze richting vereist een andere schroef-/asfamilie en is nu niet geïmplementeerd. Het montagevoordeel van modulariteit wordt beperkt toegepast door de test als kleine losse cassette op te bouwen; een schaalbaar moduleslot wordt niet voor deze proef ontwikkeld.

## Onafhankelijke historische integriteit

`history_integrity.py` vergelijkt iedere bestaande tracked file met commit `46a4117d5bbed2c5fc0669be62e27b7c1233a7e2`, inclusief SHA-256 van ieder bestand. De uitvoer staat in `history-integrity.json`. De definitieve uitvoering moet nul gewijzigde historische bestanden melden.

## Definitieve geometriecontrole

De definitieve `geometry_review.py` gebruikt de werkelijk geëxporteerde, gesloten STL-meshes en echte Manifold-booleans. De uitvoer staat in `geometry-review.json`, met SHA-256 van de gecontroleerde CAD-meshes.

- **7.180 doorsnedeberekeningen, 173 eindige poses, nul onverwachte doorsneden. Er zijn geen contactparen uitgesloten**, ook de echte schroef-/pindraad niet.
- Alle acht binaire rij-/kolomstanden, inclusief de drie grote houders op hun correcte zijde van de tabs.
- 31 standen per bewegingspad: alle drie selectors samen, alleen de rij, en beide kolommen met tegengestelde beweging. Houders van bewegende selectors zijn daarvoor verwijderd.
- 32 aandrijfstanden: alle acht selectiemaskers met inputs op −90°, −45°, +45° en +90°. Geselecteerde schroeven en pinnen volgen de werkelijke 3-mm lead; ongekozen outputs blijven op hun plaats. Dit controleert geometrische vrijloop en is geen dynamische voorspelling van buurisolatie.
- 31 standen van de montage van de twee voorgemonteerde framehelften, langs Y van 15 mm afstand naar gesloten, in stappen van 0,5 mm.
- De volledige 3-mm translatie-enveloppen van de drie selectoronderdelen zijn bovendien met een conservatieve Minkowski-som gecontroleerd tegen de werkelijke beide framehelften. De positieve marge van 0,00001 mm rond die enveloppen introduceert geen doorsnede. Deze specifieke selector/framecontrole is continu; overige genoemde controles bemonsteren eindige poses.
- Negen voorgeschreven fasezoekstanden tonen de geometrische route uit tand-op-tand: bij inputhoek 0° stopt de beschikbare kolominschuiving rond 38,7% van de slag; bij 76° kan de volledige slag worden bereikt. Dit is nadrukkelijk een opgelegde contactvrije route met inputrotatie, geen simulatie van wrijving, krachten of spontaan meedraaien.

### Axiale steun en DD-inschakeling

De nominale tandwortelafstand bij volledig kiezen is 2,96 mm. Daaruit volgen 1,84-mm interdigitatie, 1,36-mm rechte flankoverlap en 0,56-mm tandtip-/bodemvrijloop. De flensbuitenvlakafstand is 15,36 mm. Bij slechts één gekozen selector blijft nominale tipvrijloop 1,16 mm. De 0,24-mm flensvangspeling per helft kan samen 0,24 mm afwijking van de relatieve rotorstand geven; de CAD-getallen zijn geen gekwalificeerde printtoleranties.

De verkorte schroefstaart is onafhankelijk opnieuw gecontroleerd: de werkelijke vaste framevlakken begrenzen de schroef rond −0,1484 mm en +0,2300 mm axiale beweging. De onderste conische steun neemt het neerwaartse gewicht op; de bovenste borgplaat begrenst opwaarts verschuiven. Dit betekent circa 0,3784-mm nominale axiale vrijheid, geen spelingsvrije lagering.

Na het zetten op de onderste conische steun blijft circa **0,302-mm eindvrijloop** tussen schroefstaart en de gesloten bodem van de bovenrotor in UIT. Een eerdere versie had daar circa 0,052 mm; de staart is daarom 0,25 mm ingekort terwijl de wereldpositie van schroefdraad en steunkraag gelijk bleef. De bovenste DD-inschakeling is bij AAN 2,03 mm nominaal; bij de maximale opwaartse schroefbeweging blijft circa 1,80 mm, vóór vangspeling en printfouten. De onderste DD-inschakeling is bij AAN 2,20 mm nominaal; circa 2,00 mm wanneer de inputbus op de onderste steun ligt. Dat is geschikt om deze kleine handproef te onderzoeken, geen sterktekwalificatie voor motorbelasting.

Een conservatieve stapeling van onafhankelijke CAD-uitersten verlaagt de bovenste AAN-DD-inschakeling verder: 2,03 − 0,23 (opwaartse schroefvrijheid) − 0,12 (rotorvangspeling) − 0,08 (tab/houdervrijheid) = **1,60 mm vóór printfouten**. Voor de onderste AAN-verbinding resteert met neerwaarts gezette input en +0,20 mm rotor-/tabafwijking circa 1,80 mm. De bovengenoemde 0,302-mm zittende staart/bodemvrijloop wordt in UIT bij +0,20-mm rotor-/tabafwijking circa **0,102 mm vóór printfouten**. Dit zijn bewuste kleine marges voor een lichte zichtbare handproef: controleer afzonderlijke soepele schuifbeweging en dat de schroef op haar vaste steun blijft, vóór sluiten/aandrijven. Geen motorbelasting of hogere belasting kwalificeren; CAD geeft geen positief printfoutenbudget voor willekeurige productievariatie.

De rotorhalzen zijn verlengd zodat 1,60-mm selectorbladen hun volledige slag halen. Bij de onafhankelijke controle zijn echte botsingen tussen kolomselector en beide vaste geleidings-/steunplaten, en tussen houders en frame/buurhouder, ontdekt en vóór de einduitvoer in CAD opgelost. Die oude negatieve controles zijn geen fysieke resultaten.

### Printsteun en montage

De definitieve `screw-tree.stl` is één verbonden, gesloten lichaam. Beide schroeven staan op brede, onderling verbonden voeten; vier stijve staanders en twee zijverbindingen per schroef op meerdere hoogtes vervangen de eerdere ongestabiliseerde slanke print. De verbindingen zitten op de schroefkraag en op berekende draadkruinen. De draadverbindingen zijn 0,50 mm breed en 0,36 mm hoog, met nominale radiale ingreep 0,14 mm. Bij losmaken kunnen littekens ontstaan: dit blijft een expliciete vraag van de fysieke test. De onafhankelijke slicercontrole moet bevestigen dat deze verbindingen werkelijk geëxtrudeerd worden. CAD-verbondenheid alleen is daarvoor onvoldoende.

De vaste centrale staaf en uitgebreid modulair docking zijn terecht uitgesteld. De nieuwe tweedelige inlegconstructie en drie grote herbruikbare houders leveren al montagewinst zonder extra kleine stops. Tape houdt alleen de vaste buitenvoeg; geen tape op schuif- of draaivlakken.

### Review van de testinstructies

`test.md` benoemt het juiste materiaal, vaste printoriëntaties, uitschakelen van automatische oriëntatie/plaatsing, afzonderlijke passing buiten het frame, zorgvuldige steunverwijdering, beide ontkoppelroutes, acht maskers, zichtbare volledige sluiting en de veilige hoogteband van 2,5–5,5 mm. De eindstanden worden vóór aandrijven geborgd. Fasezoeken en passieve uitlijning worden afzonderlijk geregistreerd; nieuwe fysieke uitkomsten blijven onbekend. Er zijn geen verdere geometrische blockers gevonden.

**Grenzen:** geen gemeten printsterkte, wrijving, selectorstijfheid, bedhechting of verwijderbaarheid van brugjes. Geen bewijs dat willekeurige fysieke fases altijd met lichte handkracht invangen. Geen productie- of arraykwalificatie. De eigenaarstest beslist juist deze resterende vragen.

De slicerreview meldt werkelijk geëxtrudeerde verbindingen voor alle twintig steunbrugjes. De framehelften bevatten echter bruggen van circa 22 mm: doorzakking blijft fysiek onbekend. Inspecteer die framebruggen vóór montage; een doorhangende brug die geleiding of de framevoeg beïnvloedt is afkeur. Dit is vastgelegde printonzekerheid, geen gemeten mislukking.
