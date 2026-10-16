# Onafhankelijke geometriecontrole — E-297

Deze controle importeert geen geometriegenerator of eerder berekende botsingsuitslag. Het script leest de werkelijk geëxporteerde onderdeelmeshes, plaatst die opnieuw volgens afzonderlijk vastgelegde coördinaten en berekent doorsnedevolumes. De hashes staan in `independent-geometry.json`. Het resultaat is geometrisch bewijs binnen de vermelde aannamen, geen fysieke passing-, wrijvings-, sterkte- of betrouwbaarheidstest.

Reproduceren vanuit de repositoryroot met Python 3, NumPy, Trimesh en Manifold3D:

```sh
python tools/curated-experiment-checks/E-297/independent_geometry.py
```

`--skip-mesh` voert alleen de analytische controles uit en is geen complete verificatie. De bronbestanden en uitslagen zijn bedoeld voor engineeringreproductie; de eigenaar print de afzonderlijk geleverde Bambu-projecten.

## Axiale selectie

De rij en kolom bewegen ieder 2,40 mm. De afstand tussen tandtips in rust is 3,36 mm. Per cel geldt dus `tipafstand = 3,36 − 2,40 × (rijfractie + kolomfractie)`.

| Rij | Kolom | Tipafstand | Geometrische toestand |
|---|---|---:|---|
| 0 | 0 | 3,36 mm | Vrij |
| 1 | 0 | 0,96 mm | Vrij |
| 0 | 1 | 0,96 mm | Vrij |
| 1 | 1 | −1,44 mm | 1,44 mm tandinterdigitatie |

De twee afgeschuinde tipzones van elk 0,24 mm worden **beide** afgetrokken. De rechte dragende flankoverlap is daardoor nominaal 0,96 mm. De vrije afstand van tandtip tot tegenoverliggende tandwortel is eveneens 0,96 mm. Met een totale ongunstige axiale foutstapel van maximaal 0,72 mm blijft voor enkeleselectie, rechte flankoverlap en wortelvrijloop telkens 0,24 mm over. Dit is een acceptatiebudget, geen gemeten X1C-nauwkeurigheid. De rotor ligt in het CAD midden in de 0,24-mm capture-speling: ±0,12 mm per helft, samen maximaal ±0,24 mm tandafstandsfout. De gekozen budgetverdeling is 0,24 mm capture, 0,24 mm gezamenlijke stop-/Z-positioneerfout en 0,24 mm resterende reserve. Het script vermeldt aanvullend de volledige 0,48-mm verplaatsing tussen tegengestelde belaste capturestanden; dat is geen extra fout bovenop de gecentreerde ±0,24 mm.

Alle zestien rij-/kolomschakelstanden geven de verwachte cartesische AND-selectie. Alle 256 overgangen tussen deze standen zijn bovendien op een route gecontroleerd die eerst volledig opent en vervolgens de nieuwe selectie maakt. De analytische afstanden zijn monotoon over iedere deelbeweging. De meshcontrole bemonstert daarnaast alle 32 unieke schakelranden op drie tussenposities.

Twee deels bewogen selectoren **kunnen** al contact maken zodra hun gezamenlijke sluiting 3,36 mm bereikt. Het mechanisme is een AND-selectie voor de twee eindstanden; het is geen digitale vergrendeling die alle tussenstanden uitsluit. Stop de draai-input, ontlast torsie en open de oude selectie volledig voordat een nieuw adres wordt ingesteld. Tijdens het eerste deel van deselectie bestaat nog flankoverlap.

## Draaimoment, fase en omkeerspeling

De twee klauwen per helft beslaan ieder 76°. De ideale volledig zittende fase ligt rond 90°, met een geometrisch venster van 76° tot 104° en dus 28° vrije omkeerspeling. Chamfers vergroten alleen het eerste invanggebied. Zij bewijzen geen vanzelfsprekende fase-invang onder belasting. Gedwongen sluiting bij tand-op-tandfase geeft aantoonbaar een positief botsingsvolume; deze negatieve controle hoort te falen.

De DD-profielen zijn vormsluitend in beide draairichtingen voor alle geleverde toleranties. Het mannelijke profiel is Ø2,20 / vlakmaat 1,60 mm. De testreliefs zijn 0,12 / 0,15 / 0,20 mm per zijde. Bij de ruimste variant is de ideale verschilmaat tussen mannelijke omcirkel en vrouwelijke vlakmaat nog 0,20 mm; onafhankelijke ongunstige maatfouten van elk 0,10 mm kunnen dat verschil geheel opeten. De analyse gebruikt geen veronderstelde normale verdeling van printfouten.

Voor de nominale relief geeft iedere DD ongeveer 26,14° potentiële vrije omkeerspeling. De twee schuivende DD-verbindingen plus klauwen leveren samen ongeveer 80,28°; inclusief de uitneembare handsleutel en haar extra DD-verbinding is dat ongeveer 106,41°. Bij 3 mm schroefspoed vertegenwoordigt dit ongeveer 0,887 mm hoogteverschil tussen ideale aandrijffasen, exclusief draadspeling en vervorming. Het is een geometrische bovengrens voor speling in deze verbindingen, geen gemeten vrije slag. Verwacht daarom geen onmiddellijke pinbeweging na een kleine draairichtingswissel.

## Schroef, ondersteuning en pinnen

De oorspronkelijke E-295-draadmeshes zijn daadwerkelijk meegenomen. Positieve CAD-rotatie van de schroef om +Z vraagt **negatieve** pinverplaatsing van 3 mm per omwenteling. De juiste combinatie is in beide richtingen over ±360° en ±3 mm gecontroleerd; het omgekeerde verplaatsingsteken levert een duidelijke botsing als negatieve controle.

De schroef rust op een vaste conische schouder aan de onderste plaat en wordt boven de flens tegen oplichten begrensd. De inputas heeft een onderste steun, een opgesloten kraag en een langer bovenjournaal. Beide assen hebben nominaal 0,24 mm axiale vrije slag. Deze slag kan een kleine pinhoogtesprong geven. Zij wordt niet automatisch bij het tandafstandbudget opgeteld: zolang de schuifprofielen vrij blijven, liggen de rotoren axiaal aan hun eigen selectoren.

De blinde DD-gaten zijn 5,48 mm diep. De nominale insteeklengte is 4,92 mm in rust en 2,52 mm geselecteerd; er blijft in rust 0,56 mm ruimte voor de astip. Na 0,24 mm asbeweging en 0,12 mm rotor-capturebeweging blijft 0,20 mm dakvrijloop over. Een aanvullende ongunstige selector-stopverschuiving van 0,12 mm verkleint dit tot slechts **0,08 mm vóór verdere printafwijking**. Het 0,72-mm tandbudget kwalificeert dus niet automatisch de blinde dakvrijloop. De output houdt bij de ongunstigste gecontroleerde combinatie minimaal 2,16 mm DD-overlap bij de gecontroleerde as- en capturebeweging, of 2,04 mm met nog 0,12 mm ongunstige selector-stopfout. Deze nominale vrijloop is bedoeld om een verborgen axiale krachtroute naar de selector te voorkomen; daadwerkelijk vrij schuiven en afwezigheid van dakcontact moeten fysiek worden vastgesteld.

De 4,40-mm vierkante pinnen hebben twee 4,60-mm geleidingen op Z=42,0–43,2 en 51,2–52,4 mm. Beide grijpen over de volledige ±3-mm testslag aan. Een conservatieve ideale kantelberekening, inclusief 0,24 mm output-asverplaatsing, laat slechts **0,1275 mm** gezamenlijke buurreserve aan de hoogste pinpunten over. Gatvergroting, frame-uitlijnfouten en buiging verbruiken deze reserve. Dit vraagt een daadwerkelijke buurvrijloopproef; een coaxiale CAD-stand is hiervoor geen productiegarantie.

## Werkelijke meshes en bewust afgekeurde geometrie

De nominale controle omvat 403 matrixposities met alle selectors, beide rotoren per cel, beide assen, pinnen en de drie echte framedelen. Daarin zitten alle 16 selectiemaskers, niet-cardinale rotorfasen, tussenstanden, ±3-mm draadbeweging, de volledige capture-spelingshoeken en beide axiale asposities. Daarnaast zijn twaalf daadwerkelijke montagepaden in 668 posities met maximaal 0,25 mm translatiestap gecontroleerd. De montage begint met het middendeel van het frame: eerst de achterste rij losse assen/rotoren vanaf hun eigen X-zijde, dan haar vork vanaf −Y; daarna de voorste rij. Beide vorken worden eerst vanaf X=−40 mm op een vrije positie 6 mm achter hun doelrij gebracht. Vervolgens komen de vooraf samengestelde bovenste kolommen vanaf hun eigen X-zijde en sluiten de buitenste framedelen. Er wordt geen onderdeel door een te klein gesloten geleidingsgat gestoken. Op de definitieve meshes zijn dit samen **1.071 posities en 7.653 echte doorsnedeberekeningen, zonder onverwacht doorsnedevolume**. De laatste JSON bevat de actuele hashes, aantallen doorsnedeberekeningen en eventuele afwijkingen. Volumes groter dan 0,00001 mm³ gelden als botsing; zuiver vlakcontact mag bestaan.

Een eerdere rotor met Ø4,30-mm bovenlichaam is bewust verworpen. Met een geometrisch toegestane helling van 3,2° en 0,05 mm zijdelingse verschuiving bleven selector en verticale inputas vrij, terwijl twee buurrotoren elkaar ongeveer 0,03514 mm³ doordrongen. Dit negatieve resultaat is bewaard in `validation/rejected-wide-rotor-tilt.json`. De huidige rotor heeft boven de captureflens Ø3,60 mm en twee nieuwe vaste ronde framegeleidingen van Ø4,00 mm, één op ieder rotorhoogteniveau. Het lichaam is verlengd zodat die vaste geleidingen gedurende de volledige selectieslag op cilindrisch materiaal blijven aangrijpen. Een vrije captureflens alleen werd dus niet als voldoende uitlijning aangenomen.

De aanvullende kantelcontrole staat in `independent_tilt.py` / `independent-tilt.json`: 39.000 kandidaten voor selectorfractie 0 / 0,5 / 1, acht kantelrichtingen, hoeken tot 20°, dertien laterale posities, vijf Z-posities en selectorverschuiving −0,2 / 0 / +0,2 mm. 7.741 combinaties passen binnen de werkelijke ronde framegeleiding en de werkelijke tweestationsvork. Een volledig ronde buitenomtrek omvat alle rotatiefasen van de tanden.

Bij volledige selectie bedraagt het grootste conservatieve halve ruimtebeslag 2,43546 mm; bij halve selectie 2,49827 mm. Beide blijven in deze bemonstering onder de halve pitch van 2,54 mm. In de OFF-stand laat de ruimere verzameling zonder asbeperking een flensbereik van 2,61228 mm toe. Die betreffende standen botsen met de nominale verticale inputas; de grootste OFF-stand die óók met die verticale as vrij blijft, reikt 2,29741 mm. **De gecombineerde kanteling van inputas en rotor, plus werkelijke printfouten, is daarmee niet volledig gekwalificeerd.** De fysieke proef moet buurcontact en meeslepen in alle selectiestanden daadwerkelijk controleren. Dit is een afgebakende resterende onzekerheid, geen bewezen botsing van het definitieve mechanisme en evenmin een bewijs dat iedere mogelijke vrije stand veilig is.

De brede kantelzoektocht ging vooraf aan uitsluitend langere handgrepen en bredere, ver van de rotoren gelegen framespines. Daarna zijn 25 grensgevallen opnieuw tegen de definitieve meshes gecontroleerd; de JSON bewaart zowel de oorspronkelijke zoekhashes als de definitieve hashes van deze lokale hercontrole. De bewering is dus bewust een eindige geometrische controle met hercontrole van de gewijzigde delen, geen volledige continue tolerantieanalyse.

De rotor wordt tijdens gebruik door de vaste ronde framegeleiding beperkt. De kale rotor/coupon buiten dat frame heeft deze beperking niet. Geen van deze berekeningen bewijst automatische fase-invang, voldoende laagsterkte, lage wrijving, zelfremming, frame-uitlijning of de afwezigheid van buurbeweging in een werkelijke print.
