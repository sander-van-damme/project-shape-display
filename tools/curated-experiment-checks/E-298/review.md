# Onafhankelijke mechanische beoordeling — E-298

16 oktober 2026. Afzonderlijke reviewer; geen fysieke print of werking uitgevoerd. Gelezen: repository- en printtestinstructies, missie/prioriteiten, E-297-tandontwerp, actuele CAD en onafhankelijke E-297-review. Deze review beperkt zich tot de gevraagde twee punten en twee holtes op twee afzonderlijk axiaal bewegende helften. E-297 en historische printtests blijven bewijsstukken, geen bestanden om bij deze opdracht te corrigeren.

## Wat zelfuitlijning werkelijk vereist

De axiale kracht kan alleen rotatie veroorzaken wanneer de gezamenlijke contactgeometrie bij de huidige fase een tangentiële component heeft, en die component de wrijving en het benodigde schroefkoppel overwint. Een helling op één losse tand bewijst dat niet: beide tegenoverliggende punten kunnen tegelijk contact maken en elkaars tangentiële momenten opheffen. Voor identieke tegenoverliggende hoogtevelden is de minimale niet-botsende basisafstand de bovengrens van de som van beide oppervlakken, met de juiste spiegeling van de bovenhelft. De helling van die **gezamenlijke contactomhullende** is relevant.

Een kleine asymmetrie kan de plaats en aard van een symmetrisch contact veranderen; zij levert geen algemene garantie tegen alle dode fases. Iedere periodieke contactomhullende behoudt een hoogste stand. Een ideale scherpe top kan daar instabiel zijn, maar exact contact kan zonder verstoring blijven staan. Werkelijke vlakke FDM-toppen, afronding, laagtrappen en statische wrijving kunnen juist een eindig stilstandsgebied maken. De proef moet daarom precies punt-op-punt én kleine afwijkingen naar beide kanten bevatten. De uitkomst “draait na een zetje” wordt apart genoteerd van zelfstandig invangen onder uitsluitend axiale druk.

## Gemeenschappelijke stijve selectoren

Verschillende beginfases zijn geometrisch verenigbaar als iedere bovenste schroef zelfstandig mag indexeren en de helften hun gezamenlijke eindstand kunnen bereiken. De eigenaar staat die beperkte pinverplaatsing uitdrukkelijk toe. Daardoor is er een bruikbare testhypothese zonder motorisch fasezoeken.

Er is echter geen individuele veer of slagcompensatie: de eerste cel die vastloopt kan de hele stijve rij- of kolomstaaf tegenhouden. Een soepel paar omzeilt een vastgelopen buur niet. Ook reeds gezette cellen moeten voldoende axiale wortelvrijloop houden terwijl andere cellen nog roteren. Test B moet dus verschillende fases **tegelijk** selecteren, de inputs tijdens selectie niet afzonderlijk verdraaien, en de eindstand van alle koppelingen vaststellen. Een zichtbaar bewegende pin alleen is geen bewijs van volledige aangrijping. Meer handkracht of elastisch buigen van de selector mag een blokkering niet als succes verbergen.

## Dragende flanken en axiale marge

De nieuwe lange punthellingen kosten rechte flanklengte. Bij oorspronkelijke E-297-penetratie 1,44 mm en twee even lange tophellingen met hoogte h is de rechte overlap `1,44 − 2h`. Voor h=0,48 mm is dat 0,48 mm; voor h=0,60 mm slechts 0,24 mm. Het oude expliciete ±0,72-mm E-297-ontwerpbudget kan daarom **niet** als bewezen of behouden tolerantieclaim worden overgenomen: de ongunstige stand heeft dan geen rechte overlap meer. Werkelijke printmaten, vangspeling en selectorzetting moeten worden gemeten.

Bij gedeeltelijke zetting dragen de hellingen het koppel en kunnen beide draairichtingen een axiale uitloopkracht geven. De positieve axiale vangst voorkomt niet vanzelf vervorming, slijtage of een openbuigende selector. Volledige zetting en voldoende rechte flank zijn vereist voordat de test bidirectionele overdracht beoordeelt. Ontkoppelen gebeurt met stilstaande input en ontlaste torsie.

## Printbaarheid en bewijsgrens

Een CAD-punt kleiner dan één extrusielijn is geen geprint punt met dezelfde maat. De opgeslagen Bambu Studio-toolpaths moeten aantonen welke bovenlagen werkelijk aanwezig zijn, hoe breed de overblijvende kroon is en of beide punten verbonden blijven met hun tandvoet. De afmeting uit CAD en de geplande slicervorm worden afzonderlijk gerapporteerd. Alleen een fysieke print bepaalt werkelijke apexradius, beschadiging, wrijving en herhaalbaarheid. Identieke herhalingen op Test A zijn daarvoor essentieel.

De bestaande soepele E-295-draad is positief eigenaarbewijs voor die draad. Zij bewijst geen lage indexeerkracht bij iedere belasting, geen zelfremming en geen automatische puntkoppeling. Met 3-mm lead geldt voor werkelijk gemeten outputrotatie Δθ: `Δz = 3 Δθ / 360` mm, met teken volgens draairichting. Noteer rotatie en pinverplaatsing tijdens het **selecteren**, los van de daaropvolgende aangedreven slag.

## Vrijgave van het experiment

Test A is de kleine beslissende proef. Test B is een concrete, vooraf voorbereide integratieproef die pas zinvol wordt nadat A zelfstandig invangt, volledig zet en beide richtingen draagt zonder puntbeschadiging. CAD en echte slicerpaden kunnen deze fysieke voorwaarden niet invullen. Een negatieve uitkomst is bruikbaar en leidt binnen deze opdracht niet tot veren, een derde selector of een andere architectuur.

## Afzonderlijk uitgevoerde controles

De reviewer controleerde de nieuwe reactiekam die tijdens selectie de vier bestaande inputs tegen verder meedraaien opvangt, met de hieronder gekwantificeerde DD-speling. In alle 16 binaire selectietoestanden zijn 112 werkelijk overlappende bounding-boxparen booleaans onderzocht: geen interferentie van de kam met de nominale assemblage. De tijdelijke kam komt onder de bestaande inputassen; zij is geen nieuwe selector of aandrijfarchitectuur en wordt verwijderd voor de overdrachtstest. De hergebruikte frame-, selector-, as-, schroef-, pin- en hulpmiddelbestanden zijn in 31 gevallen byte-identiek aan E-297. Bron en uitkomst: [independent_review.py](independent_review.py), [independent-review.json](independent-review.json). Dit is geen continue tolerantie- of montagekrachtgarantie.

Alle drie nieuwe STEP-rotoren zijn afzonderlijk als geldige BREP-solids geopend. De oorspronkelijke omhullende blijft nominaal behouden; de nieuwe sectoren hebben een andere polygonale discretisatie. Een exacte booleaanse deelverzameling van de oude rotor is daarom niet bewezen en wordt niet gebruikt als vervanging voor controle van de nieuwe geometrie.

## Nieuwe Bambu-archieven

De aparte [archiefcontrole](independent_review_archives.py) opent beide ZIP-projecten, controleert ZIP-integriteit en vergelijkt de ingesloten objectmeshes met de nieuwe plaat-STL's. Test A bevat 18 gesloten objecten; Test B 37. Volumes, gesorteerde afmetingen en aantallen facetten komen binnen exportafronding overeen; de grootste maatverschillen zijn circa 0,000016 mm. Dit bevestigt dat de onderzochte brononderdelen in de nieuwe projecten zitten. Daarnaast zijn opgeslagen X1 Carbon/0,4-mm-nozzle/PLA, 0,08-mm lagen, 0,12-mm eerste laag, Arachne en twee wanden afzonderlijk gecontroleerd. Beide projecten bevatten echte G-code met overeenkomende MD5. Dit vervangt niet de volledige procescontrole, controle van werkelijk geëxtrudeerde puntlagen en heropenen/opnieuw slicen. Zie [A-resultaat](independent-review-archive-geometry-A.json), [B-resultaat](independent-review-archive-geometry-B.json) en de afzonderlijke printbaarheidsrapportage.

Het verworpen eerste CAD-topvlak van 0,16 mm is in de slicer niet intact behouden. De geleverde CAD gebruikt daarom een kroon van circa 0,30 × 0,30 mm; dat is een productiecompromis, geen claim dat de printer een perfect scherpe punt maakt. De onafhankelijke echte STL-contactomhullende bevestigt voor de bemonsterde fases een topcontactplateau; de asymmetrische variant verschuift het plateau en verwijdert het niet. Daarom blijft Test B een voorwaardelijke diagnostische proef, ook wanneer de bestanden correct slice- en printbaar zijn.

## Reactieplaat houdt de input niet spelingsvrij vast

De nominale DD-pen is Ø2,20 mm met vlakmaat 1,60 mm; de socket Ø2,50 mm met vlakmaat 1,90 mm. Voor concentrische ideale profielen is de totale vrije omkeerhoek per verbinding `2[asin(0,95/1,10) − asin(0,80/1,10)] = 26,138°`, dus ±13,069° vanuit het midden. De keten **reactieplaat → inputas → onderste rotor** bevat twee zulke verbindingen: maximaal 52,276° totale omkeerhoek, of ±26,138° vanuit twee gecentreerde profielen. Dat is aanzienlijk naast de berekende puntcontactplateaus. Werkelijke excentriciteit, printmaat en vervorming kunnen hiervan afwijken; dit is geen gemeten bovengrens.

De reactieplaat verhindert dus onbeperkt meedraaien, maar bewijst geen strikt stilstaande inputas of onderste rotor. Markeer en observeer bij de zelfuitlijnproef de onderste rotor, input en bovenste rotor/schroef afzonderlijk. Beweging die alleen beschikbare DD-speling verbruikt kan uit een dode fase ontsnappen zonder dat de schroef dezelfde hoek draait. Registreer dit als passieve spelingsopname, niet als motorisch fasezoeken, en evenmin als bewijs van zelfuitlijning bij volledig star vastgehouden onderhelften. Test A heeft dezelfde observatie nodig: een stilgehouden handasvoet laat nog de DD-speling van haar rotor toe. Ook tussen bovenrotor en schroef zit één DD-verbinding; de rotorhoek hoeft daarom niet onmiddellijk in pinhoogte omgezet te worden.
