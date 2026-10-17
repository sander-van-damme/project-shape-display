# E-300 — CAD-maatvoering en montagegrenzen

Alle maten in mm; nominale CAD-geometrie, geen fysieke meetuitslagen. [Bron](generate.py), [parameters](parameters.json), [werkelijke meshdoorsneden](../drawings/section.png), [onafhankelijke controle](../review/geometry-review.json). Voer `python tools/curated-experiment-checks/E-300/cad/generate.py` uit vanuit de repository met CadQuery, NumPy, trimesh en manifold3d beschikbaar. De generator schrijft uitsluitend E-300 en de nieuwe gedateerde proefmap.

| Onderdeel / functie | Definitieve maat |
|---|---|
| Raster / kolomslag | 5,08 / 3,00 |
| Onderrotorbasis UIT / nominale AAN-contactpositie | Z 8,00 / 11,00 |
| Bovenrotorbasis UIT / nominale AAN-contactpositie | Z 29,36 / 26,36 |
| Flens | Ø4,30 × 0,72 |
| Mannetje, 45° flank | lokaal Z 6,20–6,70; R 1,90→1,40 |
| Cup, 45° binnenflank | lokaal Z 8,56–9,21; R 1,30→1,95 |
| Cup buitenmaat / minimale lip / rastervrijloop tussen cups | Ø4,70 / 0,40 / 0,38 |
| Flensbasisafstand bij flankcontact | 15,36 |
| Tipvrijloop / mondverlenging | 0,10 / 0,05 |
| Selector: onderblad / bovenblad / totale hoogte | 2,40 / 4,40 / 8,00 |
| Vanggroef / totale axiale flensspeling | 1,20 / 0,48 |
| Onderste U / bovenste U | Ø2,80 / Ø3,70 bij flensvlak, uitlopend tot Ø4,10 bovenaan |
| Hals / overgang naar Ø3,60 hub | R1,60 tot Z5,52; overgang Z5,52–5,72 |
| Kern: X-breedte per cel / Y-envelop | 4,60 / −2,77…+2,15 = 4,92 |
| Rug door vanggroef | Y −2,77…−2,31: 0,46 breed |
| Rug op bladhoogten | Y −2,77…−2,14: 0,63 breed |
| Bovenste rugvrijloop | Laatste 0,90 hoog: vrijloop vanaf Y−2,60; printhelling naar Y−2,14 |
| Inputsockets / inputtip / rotor-DD-blindbodem | 3,20 diep / Z13,00 / lokaal Z5,68 |
| Kolomhouder UIT / AAN | Z20,96–23,96 onder tab / Z29,04–32,04 boven tab |

## Krachtcontact en werkelijke slag

De nominale conusposities in `assembly-both-on.stl` tonen de flanken zonder aangedrukte vangspeling. Om kracht over te dragen neemt de rij eerst 0,24 onderrotorspeling op; de bovenrotor beweegt 0,24 naar boven tot zijn kolomvork, en de kolomselector 0,04 naar zijn bovenste houder. Nominaal eerste belast contact is daarom:

| Component | Z-basis |
|---|---:|
| Gedeelde rijselector | 11,52 |
| Beide onderste rotoren | 11,28 |
| Beide kolomselectors | 26,40 |
| Beide bovenste rotoren | 26,64 |

Deze toestand staat in `assembly-both-loaded.stl`. De handslag vanaf rij-UIT is circa **3,52**; de frame-envelop laat centraal **3,75** en kanteling ±3° vrij. De koppeling begrenst de echte beweging bij contact. 3,75 is geen voorgeschreven door te drukken eindstand. Een starre rij kan als geheel kantelen, maar buigen is geen geplande hoogtecompensatie. De concrete 0,10-mm-eenzijdige hoogteproef is afzonderlijk geometrisch gecontroleerd; willekeurige maatfouten zijn daarmee niet gekwalificeerd.

## DD-inschakeling: scenariogrenzen

Onderste nominale DD-overlap bij belast contact: **13,00−11,28 = 1,72**. Bij de gecontroleerde ±3°-hoogteverdeling verschuiven de rotorbasissen ±0,133: minimaal circa **1,59**. In de ongekoppelde, vlakke uiterste rijstand en op het dragende onderblad resteert **1,49**. Onbelaste rotoren mogen binnen hun vangspeling hoger staan: de conservatieve volledige vrijloopcombinatie geeft slechts circa **0,88** met maximale rijslag en lokale kantelverhoging. Niet gebruiken als belast aandrijfgeval; controleer zichtbaar vrije slag en werkelijk volledig contact voordat de input draait.

Bovenste nominale overlap bij belast contact: **26,64−24,33 = 2,31**. De combinatie AAN, −0,24 rotorvangspeling en +0,230 schroefaxiaalspeling geeft circa **1,56**. UIT met +0,24 rotorvangspeling en een 0,147 neergezakte schroef houdt circa **0,26** tussen DD-staart en blindbodem over. Dit is een CAD-marge vóór printfouten; eerst vrij schuiven en steun controleren. Niets tegen een eindstop forceren.

## Raster en proefgereedschap

De herhaalbare kern wordt als `row-selector-core` en `column-selector-core` geëxporteerd, maar wordt niet apart geprint. Zijn Y-envelop van 4,92 laat 0,16 tot een naastgelegen selector en 0,16 tot de naburige Ø4,30-flens. De 0,90-mm-rugvrijloop met afgenomen YZ-printhelling voorkomt cupcontact bij onafhankelijke selectie en vangspeling. De onafhankelijke controle onderzoekt buurkernen en rotoren op het 5,08-raster.

De verticale traagheidsmaat bij de uitsparing is afzonderlijk gecontroleerd: 17,852→36,173 mm⁴, circa **2,03× E-299**. Dat geldt alleen voor buiging in de selectierichting. De laterale traagheidsmaat daalt tot circa 10% door de smalle rasterrug; zijwaartse buiging en torsie zijn dus belangrijke proefpunten.

De grote centrale rijpaddle, diagonale printvleugels, eindarmen, lange kolomhendels en frame zijn **externe bediening van deze 1×2-proef**. Zij worden niet binnen een grotere matrix herhaald. Een lange rij vraagt externe bediening en ondersteuning; de proef bewijst geen willekeurig aantal gelijktijdige contacten. Een starre balk met één kantelvrijheid kan twee verschillende hoogten opvangen; meer contacthoogten zijn niet opgelost.

## Onderdelen en oriëntatie

Eén plaat bevat **17 printobjecten**: twee framehelften, één rijselector, twee kolomselectors, twee mannelijke rotoren, twee cups, twee inputassen, één sleutel, twee kolomhouders, twee pinnen en één gezamenlijke schroefprintboom. Na losmaken van de twee schroeven zijn dat **18 mechanische onderdelen**; geen rijhouder of losse onderdelen per koppeling.

Framehelften liggen op hun deelvlak; rijselector op de achterkant van de paddle, gesteund door integrale bijna-45°-vleugels; kolomselectors op de brede achterkant van hun hendel; rotoren op hun flens met de cupmond omhoog. Pinnen hebben de gesloten top op het bed. De 0,65-mm-brede schuine schouders op de kolomhendel laten de kern zonder losse eilanden uit de smallere steel groeien. De ondersteunde schroefboom, schroeven en pinnen zijn byte-identiek aan E-299. Niet automatisch heroriënteren.

Monteer de onderste rij met inputs en mannetjes in één open framehelft, en leg de vooraf geschroefde pinparen met cups en kolomselectors in diezelfde open framehelft. Schuif geen flens door een kleinere gesloten boring. Sluit de framevoeg extern met tape. Zet een kolom UIT met zijn houder onder de tab; AAN met dezelfde houder boven de tab. De rij wordt centraal met de hand belast; houd haar niet op een vaste hoogte vast. De vergrote selector-envelop laat voorste secties van de rotorgeleidingen over; DD-assen en deze gedeeltelijke geleidingen begeleiden de rotoren. Wiebelen, vensterwrijving en excentrisch handkoppel blijven fysieke controlepunten.

De conische geometrie bevat geen hoekafhankelijke tanden. Werkelijke PLA-wrijving, benodigde aandrukkracht, grip in beide richtingen, drag van stilstaande vorken tegen draaiende flenzen, slip en loskomen zijn nog **onbekend**. Selecteer eerst met stilstaande inputs en draai pas na volledig contact. De conus is geen bewezen oplossing voor deze krachten.
