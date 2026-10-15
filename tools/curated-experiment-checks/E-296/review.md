# Onafhankelijke mechanische review — E-296

Review door een afzonderlijke Codex-subagent, 15 oktober 2026. Gelezen: actuele criteria, E-295, selectief E-076–083/E-118, de uiteindelijke `generate.py`, `validation.py` en de onafhankelijke geometrieanalyse. Dit is een kritische ontwerp- en bronreview, geen fysieke kwalificatie of vermoeiingsberekening.

## Oordeel

De enkele huls met **rijveer, positieve rijterugtrekking en omhoog vrijgevend kolomplafond** is een verdedigbare voorkeur voor één kleine precisieproef. Het plafond geeft een werkelijke geometrische permissie; de lokale veer laat halfgeselecteerde en tijdelijk fasegeblokkeerde cellen wachten terwijl de rij haar slag afmaakt. Dit verschilt wezenlijk van twee tegengestelde krachten op één starre huls. Die oorspronkelijke krachtbalans alleen bewijst geen EN.

De twee seriële koppelingen blijven een concrete reserve, maar zijn niet noodzakelijk om de logica te repareren: de gewijzigde enkele huls levert die functie met minder lokale rotoren en koppelinterfaces. Het huidige mechanisme is **geen aangetoonde goedkope FDM-oplossing op 6.400 plekken**. De voorkeur geldt voor de eerste fysiek te falsifiëren topologie, onder de hieronder genoemde precisie- en montagevoorwaarden.

## Positieve logica en vrijgave

Met rijslag `R`, plafondslag `C` en hulsverplaatsing `q` gelden de twee positieve grenzen `q ≤ R + 0,20` en `q ≤ C`. De veer probeert de hoogste toegestane stand te bereiken. Voor eindstanden 0/1,40 mm:

| R | C | q maximaal | Outputtipgap / overlap |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0,60 mm vrij |
| 1,40 | 0 | 0 | 0,60 mm vrij |
| 0 | 1,40 | 0,20 | 0,40 mm vrij |
| 1,40 | 1,40 | 1,40 | 0,80 mm totale overlap |

Na de vergrote 0,375-mm vangmond resteert bij volledig zetten **0,425 mm rechte outputflank**; de afschuining mag niet als volle dragende flank worden geteld. Bij 30° faseverschil stopt gecentreerde geometrie op `q = 0,91077 mm`, zodat de lokale veer nog plaats heeft en de rij niet op deze cel hoeft te stoppen. Rij vrijgeven trekt via de integrale onderflens terug; kolom vrijgeven duwt met het plafond terug. Voor beide routes blijft werkelijk ontlasten vóór uitschuiven vereist.

Een willekeurige gelijktijdige adresovergang is niet geïsoleerd. Bij `R=1,40(1−t)` en `C=1,40t` geeft de overgang 10→01 op `t=4/7` een maximum `q=0,80`, dus **0,20 mm onbedoeld tipcontact**, ondanks twee ontkoppelde eindstanden. Daarom: input stoppen en torque ontlasten → rijen positief terug → kolommen wijzigen → gewenste rij(en) heffen → licht fase zoeken en volledig zetten → draaien. De eerste proef gebruikt deze zichtbare handvolgorde. Twee rijen en twee kolommen tegelijk kiezen koppelt alle vier kruispunten; een diagonaal vergt twee passes.

## Bevindingen die tijdens review zijn hersteld

- De eerste custom C-clip vereiste een niet uitgewerkte elastische montage en liet slechts circa 0,274 mm wand bij de groef/zeshoekhoek. De uiteindelijke huls heeft een **integrale onderflens Ø3,40**. Twee rijhelften worden eromheen gemonteerd en buiten het pinveld aan beide uiteinden vastgezet. Er is geen verborgen clip meer nodig.
- Een dunne horizontale kam in een hoge verticale sleuf bood onvoldoende kantelgeleiding. De uiteindelijke rij- en kolomkammen hebben aan beide uiteinden **3-mm-hoge shoes** met eindige geleidingen. De aanvankelijke vrij uitkragende-bladclaim vervalt.
- Ø2,20-boringen om Ø2,00-journals gaven te veel ongecontroleerde asbeweging. De huidige precisiehypothese gebruikt Ø2,02-boringen en 4-mm-landlengte. Dat is geen bewijs dat de gemonteerde assen voldoende samenvallen; die voorwaarde blijft te meten.
- De pin-enveloppe is verlengd tot z=15…45 met gesloten dak vanaf 44,6; de schroef eindigt op 36,2. Er zijn twee vaste geleidingsvlakken op 19…21 en 29…31. De huidige reservering is voor een kleine ±1,5-mm-demonstratieslag, geen gekwalificeerde 40-mm-slag. Functionele draadgeometrie blijft de E-295-bron.

## Resterende voorwaarden met besliswaarde

**Precisie en kanteling.** AF1,95 om AF1,80 geeft nominaal 0,075 mm halve vlakspeling; deze speling is geen volledige budgettoekenning aan elke fout afzonderlijk. Asregistratie, journalspeling, neusoverhang, hulshelling, rondloop, ruwheid en kamgeleiding gebruiken hetzelfde invang-/zetbudget. Een vrij zwevende huls kan enige excentriciteit delen tussen beide hexen; 0,075 mm is daarom geen universele onmogelijkheidgrens. De onafhankelijke analyse stelt een meetbare voorwaarde aan de hubassen en berekent daarvoor geometrische reserve. De vangmond toont een beschikbaar pad, niet dat wrijving het fysiek zal volgen.

**Montage en dunne vlakken.** Ø3,40-onderflens door veer-ID3,50 laat slechts 0,050 mm radiale montageruimte; echte veerovaliteit en diameter-/draadvariatie zijn relevant. De terugtrekring ID3,20 vangt die flens over 0,100 mm nominale radiale overlap. Beide waarden vereisen het gekozen precisieproces en controle na montage. De hulswand bij de doorgaande zeshoekhoek is circa 0,374 mm. De splitnaden, uitwendige klemmen, verbinding met shoes en gesplitste lagerplaten moeten positief worden vastgezet; de CAD reserveert hun volumes maar werkt bevestigingsgaten en voorspanning niet productierijp uit. Niet op wrijving van losse helften vertrouwen.

**Fase en lage belasting.** De berekende veerconstante is 0,062385 N/mm bij aangenomen staal-G=79.000 N/mm²; normale voorspanning 0,019714 N, maximale geblokkeerde kracht 0,107053 N en kracht bij gecentreerde 30°-wachtstand circa 0,050235 N. Dat laatste kan de lichte schroef via tip-/afschuiningscontact al laten meedraaien zonder volledig zetten. Alleen langzaam draaien garandeert dan geen fase-invang. Omgekeerd kan iets meer glijwrijving dan de kleine normale voorspanning de huls vóór haar eindstand laten hangen. Juist de supersoepele recente schroefparen moeten daarom ook **onbelast** worden getest; een belaste succesproef alleen mist deze foutwijze. Miki Pulley beschrijft zowel tipcontact/drag turning als mislukte stationary engagement: [catalogus pp. 374–375](https://www.mikipulley-us.com/documents/Catalog/Catalog_Tooth_Clutch.pdf). Dit is mechanische precedentkennis, geen miniatuurrating.

**Ontkoppelen onder torque.** Rechte flanken voorkomen geen schuifwrijving. Een belaste schroef en een gestopte bus kunnen nog flankkracht vasthouden; stilstand is niet hetzelfde als nul torque. De positieve rij- en kolomroute moeten na ontlasten de huls geheel terugbrengen, ook na beide draairichtingen. De springspecificatie of een CAD-eindstand bewijst die terugkeer niet. Geen claim over snel ontkoppelen tijdens doorlopende busrotatie.

**Krachten en fanout.** Twee geblokkeerde cellen vragen ideaal circa 0,214 N; een 80-celrij circa **8,56 N**, plus glijwrijving en eigen gewicht. Alle 6.400 normale voorspanningen samen zijn circa 126 N interne belasting tussen selectors en frame. Deze belastingen worden niet gemiddeld over onafhankelijke cellen. De 0,30-mm kam en 0,80-mm bruggen zijn geen aangetoonde 400-mm-vrije overspanning; langere rijen vragen een gesteunde rail of andere eindige constructie. De kleine proef kwalificeert dat niet.

**Permanente rotatie en buren.** Iedere huls draait ook ontkoppeld; flens-/veer-/plafondcontacten blijven slijtage- en sleepinterfaces. Met slechts een illustratieve μ=0,2 en effectieve dakringstraal 1,69 mm is de normale contactsleep circa 0,0067 Nmm/cel. Bij 6.400 cellen en 600 rpm zou dat ongeveer 2,7 W zijn, exclusief journals; het is geen gemeten waarde of motorontwerp. De onbedoelde-pinroute is vooral spleetsluiting door slingering, kanteling of vervorming, plus afzonderlijke terugdrijving van een niet zelfremmende schroef. Markeer schroefrotatie én pinhoogte om die oorzaken te onderscheiden.

**Volledige krachtroute.** Axiale schroeflast loopt via outputcollars naar het frame, ook wanneer de huls open is. De schroef/pin zijn in deze CAD gelabelde enveloppen; de outputpost en schroef zijn geen gekwalificeerde materiaalverbinding doordat hun CAD-vlakken raken. Een fysieke proef moet een integraal vervaardigde output/schroef of een aantoonbare torque-/axiale verbinding toepassen. De recent 5/5 handpassende E-295-draadparen leveren daarvoor positieve draadpassingsevidentie, geen reeds gekwalificeerde precisiehead-joint.

## Eén fysieke beslisproef

Bouw één 2×2-selectielaag op 5,08 mm met vier werkelijk geleide 4,40-mm-pinnen, gemarkeerde schroefkoppen en langzaam handbediende gedeelde input. Stel eerst na montage minstens 0,15 mm zichtbare/gemeten vrije outputgap vast in elke halfselectie. Gebruik de bewezen E-295-draadpassing; kwalificeer de head/schroefverbinding in dezelfde proef.

Test per cel beide draairichtingen, alle drie uitstanden, rij-eerst en kolom-eerst inschakelen, vrijgeven via elk afzonderlijk commando en de veilige tweepassige diagonaal. Zet doelbewust één van twee geselecteerde outputs 30° uit fase: de andere moet kunnen zetten terwijl de eerste veer wacht. Herhaal dit met onbelaste lichte output en met een kleine genoemde pinlast. Bekijk volledige seating, niet alleen toevallige meedraaiing. Doe bijvoorbeeld twintig cycli per cel en noteer handhulp, vastlopen, slijtage, terugtrekkracht en beweging van de drie niet geselecteerde schroeven apart.

Stop bij false engagement, groeiende beschadiging, niet volledig ontkoppelen of buurschroefrotatie boven de zichtbare meetresolutie. Deze proef beslist of de MIN-huls de voorkeur houdt; zij bewijst geen arraylevensduur, serieopbrengst of 40-mm-werking. Meer simulatie van onbekende wrijving heeft vóór die proef weinig extra besliswaarde.
