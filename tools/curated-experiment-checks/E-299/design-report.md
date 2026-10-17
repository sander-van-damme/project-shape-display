# E-299 — kleine 1×2-proef na de fysieke E-298-feedback

17 oktober 2026. Bronnen: het volledige eigenaarsrapport in `owner-print-tests/2026-10-16-self-aligning-point-matrix/test.md` op commit `46a4117`, E-297/E-298 CAD, de compacte E-295-draad, projectmissie en huidige prototypeprioriteiten. De bronrapporten en bestaande printprojecten worden niet aangepast.

## Keuze en bewijsniveau

Eén gedeelde rij, twee onafhankelijk bediende kolommen en twee schroefpinnen op 5,08 mm raster. Dit is de kleinste opstelling die zowel een gedeelde selector als een niet-geselecteerde buur bevat. Een tweede rij zou meer onderdelen en montage vragen zonder de nu gemelde sluitingsproblemen beter te isoleren. Deze proef kwalificeert geen volledige 2×2-adressering of uiteindelijke transmissie.

De eigenaar observeerde twee afzonderlijke problemen: punt-op-puntblokkering en onvoldoende sluiting met licht verbogen selectoren. Vlotte beweging van één pin is positieve fysieke ervaring; buurgedrag en gelijktijdige selectie bleven onbekend. De exacte filamentsoort, werkelijk gebruikte oriëntaties en ontbrekende onderdelen zijn niet bekend. Automatisch oriënteren/plaatsen was gebruikt; de oude aanbevolen oriëntaties zijn dus geen betrouwbare reconstructie van die print.

## Koppeling en fasezoeken

Brede dragende honden vervangen de fragiele punt. De bovenste 0,24 mm van de twee 2,40-mm-hoge honden is afgeschuind; de wortelbreedte blijft 76°. De koppeling krijgt een grotere bruikbare rechte flankoverlap. Scherper printen is niet als oplossing voor iedere beginfase aangenomen: ook een ideale symmetrische punt heeft exact tegenover zijn tegenpunt geen gegarandeerde draairichting.

Daarom is **langzaam fasezoeken met de input onder lichte selectiedruk onderdeel van de bediening**. De gebruiker draait de input gecontroleerd totdat de selector zijn volledige eindstand haalt; pas daarna wordt aandrijfkoppel toegepast. Maximaal één volledige inputomwenteling per poging, terwijl de werkelijk zichtbare onderste rotor ten minste één hondenperiode van 180° moet bestrijken. Zo wordt DD-omkeerspeling niet verward met echte faseverandering. Niet door blokkering heen persen. Deze keuze behoudt rij-/kolomselectie en schroefaandrijving, maar geeft de vroegere eis van volledig passieve invang bij exact stilstaande inputs op. Zonder fasezoeken wordt apart gemeten; actieve hulp wordt nooit als passieve zelfuitlijning gerapporteerd.

Dit is een hypothese die de nieuwe fysieke test kan bevestigen of afwijzen. Er wordt geen reeds bewezen invang vanuit iedere fase geclaimd. De kleine handproef heeft afzonderlijke inputs; een toekomstige gedeelde aandrijving en haar timing zijn hier niet uitgewerkt.

## Sluiting en stevigheid

Beide selectors bewegen 3,00 mm. Onderste rotorbase: 8,00 UIT en 11,00 AAN; bovenste: 29,36 UIT en 26,36 AAN. Afstand tussen flensbuitenvlakken bij volledig selecteren: 15,36 mm. Tandwortelvlakken liggen dan 2,96 mm uiteen. Met twee tanden van 2,40 mm geeft dat 1,84 mm interdigitatie, 1,36 mm rechte flankoverlap en 0,56 mm tip-tot-tegenwortelruimte. Bij slechts één geselecteerde helft is er 1,16 mm tipvrijloop.

Deze waarden zijn nominale CAD-maten, geen gemeten printmaten. Twee vangspelingsbreedten van 0,24 mm geven maximaal ±0,24 mm relatieve afwijking rond hun midden. Daarnaast laten de vensters circa ±0,08 mm per selector toe. Samen kan de nominale tandafstand circa 0,40 mm variëren: ongeveer 0,96 mm rechte overlap en 0,16 mm tip-tot-wortelruimte blijven in de ongunstige berekende eindstanden over, vóór echte printfouten. Dat is een marge voor een handproef, geen gegarandeerde productietolerantie. Volledige eindstand wordt fysiek gecontroleerd; hard bodemcontact of openende framevoegen is afkeur.

Selectorbladen worden 1,60 mm in plaats van 0,96 mm dik, met een doorlopende diepe rug. De smalle rotorhals wordt verlengd zodat het dikkere bovenblad niet tegen de conus loopt. Het doel is minder verbuiging en meer bruikbare sluiting; de echte stijfheid blijft te testen. Grote, herkenbare eindstandhouders vervangen de oude losse microblokjes. De houders moeten ook het uit elkaar drukken van de helften tijdens aandrijven tegengaan.

## Montage en modulariteit

Een tweedelig frame splitst door beide aslijnen. Onderdelen worden vanaf één open zijde in hun halve zittingen gelegd en door de tweede helft gevangen. De framehelften kunnen bij montage plat liggen; de schroef/pinparen worden vooraf buiten het frame samengesteld. Het mechanisme blijft zichtbaar. Tape sluit alleen de externe framevoegen, buiten de bewegende delen; geen kleine boutjes of aankopen.

Een vaste centrale staaf wordt voor deze proef niet ingevoerd. In de bestaande DD-as met 1,60-mm-flats laat zelfs een 1,00-mm-boring slechts 0,30 mm wand over bij de flats, minder dan één normale nozzlelijn. De schroef, lagering en uitlijning zouden fundamenteel moeten veranderen. Dat vergroot nu de onzekerheid.

De 1×2-opstelling is als zelfstandig demonteerbaar teststuk te behandelen. Er komt geen extra dockingframe, moduleconnector of 4-/16-pinsysteem: dat zou extra breedte en een nieuwe tolerantiestapel introduceren voordat de koppeling en selector werken. Vervangbaarheid binnen dit kleine frame is wel concreet te beoordelen.

## Printontwerp

De printplaat krijgt vaste oriëntaties en ruime onderlinge afstanden; niet opnieuw automatisch oriënteren of plaatsen. Alle onderdelen staan binnen het X1C-bed. Framehelften liggen op hun deelvlak, de rijselector op haar volle rug en kolomselectors op hun brede zijvlak en rotoren op hun flens. Pinnen staan met gesloten top op het bed; hun binnendraad wordt zonder supports geprint. De diepere inputsocket zit in een verdikte bus; niet in de dunne DD-schacht uitgeboord. De inputstaart eindigt op 13,20 mm, zodat zij de blinde rotorboring UIT niet raakt. De schroefstaart begint op 24,33 mm; de draad blijft op 34,16–50,16 mm. Deze inkorting voorkomt bodemcontact na het circa 0,15 mm zakken van de schroef op haar conische steun. DD-inschakeling is daardoor korter: 2,03 mm nominaal AAN, en ongeveer 1,60 mm in de conservatieve combinatie van opwaartse schroefspeling, rotorvangspeling en tabspeling, vóór printfouten. De zittende schroef heeft circa 0,30 mm nominale eindvrijloop in de bovenrotor UIT; in de conservatieve spelingscombinatie resteert circa 0,10 mm. Daarom eerst buiten het frame schuiven en in het frame steun en vrije slag controleren; geen motorbelasting. Draad en conische steun zijn niet ingekort.

De twee schroeven krijgen een ontworpen stabilisatieframe met brede bedvoeten, staanders en kleine verbreekbare verbindingen. Dit volgt het concrete eigenaarsvoorstel. De verbindingen beperken de vrijstaande lengte al tijdens het opbouwen, in plaats van pas na het bereiken van een bovenbrug. De aansluitingen worden in de echte CAD- en slicerdoorsneden gecontroleerd. De afbreekbaarheid en eventuele draadschade zijn nog onbekend en horen bij de afkeurcriteria. Geen slicersupport in de pinboringen. Een CAD-steunframe is geen bewezen bedhechting of gegarandeerd succesvolle print.

Het pakket telt 18 printobjecten en 19 bruikbare mechanische onderdelen, met een voetafdruk van 136,32 × 70,00 mm en een hoogte van 27,71 mm. Bambu Studio 02.08.02.61 raamt 3 uur 33 min 55 s en 9,37 g PLA. De definitieve steunlocaties en werkelijk opgeslagen slicerinstellingen staan in het nieuwe testpakket. Alle twintig steunverbindingen zijn in de werkelijke paden aanwezig. De circa 22-mm framebruggen en lokale draadwandonderbrekingen tot circa 0,208 mm blijven fysieke inspectiepunten; de behouden draad wordt niet als bewezen sterk gepresenteerd. Sliceruitvoer en geometrische controles worden afzonderlijk van het nog lege fysieke resultatenformulier bewaard.

## Stop

De oplevering eindigt bij één gecontroleerd X1C-project, montage/testinstructies en een leeg resultatenformulier. Geen nieuwe issues, automatische vervolgexperimenten, printopdrachten of aanschaffen. Niet-uitgevoerde fysieke tests blijven onbekend.
