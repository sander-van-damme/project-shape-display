# Test B — 2×2 met gelijktijdige zelfuitlijning

**Status:** DEFERRED  
**Prioriteit:** geen; alleen na kansrijke A1 én A2 uit [Test A](../2026-10-16-self-aligning-point-fit/test.md)  
**Laatst beoordeeld:** 2026-10-16  
**Reden:** het concrete printproject is voorbereid; de gekozen puntvorm is nog niet fysiek getest. E-297 en zijn bestaande READY-tests blijven volledig ongewijzigd.  
**Technische bron:** [E-298](../../06-experiments/E-298-self-aligning-point-clutch.md).

## 1. Vraag en stopconditie

Kunnen twee of vier koppelingen met verschillende outputfases door één gedeelde selectieslag volledig aangrijpen, terwijl alle inputassen stilstaan? De schroeven mogen daarbij draaien en de pinhoogtes mogen veranderen. Eén verkeerd gefaseerde koppeling die de hele selector tegenhoudt is een negatieve uitkomst, geen reden om harder te drukken of verborgen fasehulp te geven.

Deze proef behoudt de twee axiaal bewegende helften, rij omhoog / kolom omlaag, 5,08-mm raster en succesvolle E-295-draad met 0,175-mm relief. Er zijn geen veren of extra selectoren. De inputreactieplaat is uitsluitend een verwijderbare proefhulp onder het frame.

**Stop** bij hard blokkeren, openende framevoeg, buigende rail, puntbeschadiging, pin-/buurcontact, onvoldoende draadinschakeling of uit elkaar klimmen onder koppel. Geen tang of boormachine. Een blokkade niet oplossen met een verdraaiing en vervolgens als zelfuitlijning noteren.

## 2. Printklaar project

[**point-matrix.3mf**](point-matrix.3mf) — één geconfigureerd X1 Carbon-project. **37 delen:** drie framedelen, vier gedeelde selectors, acht A/point48-rotoren, vier inputassen, vier integrale schroeven, vier pinnen, één handgreep, acht stopstukjes en één vierpuntsreactieplaat. Alle functionele draad zit werkelijk in de meshes. Het STEP-aanbod bevat de puntrotoren en andere CAD-onderdelen; de schroef/pin-STL's behouden de originele functionele draad.

[Onderdelenkaart/manifest](layout.json) · [maatvoering en montage](../../tools/curated-experiment-checks/E-298/cad/cad-guide.md) · [gecontroleerde Bambu-instellingen, tijd en materiaal](bambu-settings.md).

**Slicerraming:** 6 uur 41 min 51 s totaal / 18,28 g PLA; modelprinttijd 6 uur 28 min 34 s.

Open als project en behoud instellingen en oriëntatie. Buitenframes liggen op de buitenwand, middenframe op het deelvlak; selectors op hun rug; rotoren met punten omhoog. Pinnen staan met gesloten top op het bed, schroeven op hun DD-staart. De buitenbrim ondersteunt bedhechting en moet weg van de functionele oppervlakken worden verwijderd. Supports blijven uit; geen support in draad of socket. Let bij de slanke schroeven op loskomen/wiebelen tijdens printen; slicerpaden kwalificeren bedhechting niet fysiek.

**Wat de paden nog niet bewijzen:** de dunne binnendraad heeft lokale onderbrekingen in de geplande wanddoorsnede (35–37 van 76 gecontroleerde draadlagen; grootste gemeten middellijnonderbreking circa 0,199 mm). De volle pinbuis en rotorhalzen blijven in de gecontroleerde paden gesloten. Inspecteer de draad dus op scheuren, lekke wand en schade; echte passing en sterkte zijn onbekend. Dit is geen nieuwe positieve of negatieve fysieke draadtest.

**Verder nodig:** enkele stukjes gewone tape voor de externe framevoegen, pen/liniaal, eventueel aanwezige schuifmaat en camera. Geen aanvullende hardware of aankopen.

![Onderdelenkaart](../../tools/curated-experiment-checks/E-298/drawings/plate-matrix.png)

## 3. Montage

1. Laat de plaat afkoelen. Verwijder buitenbrim en losse stringing; geen functionele delen schuren of uitboren. Controleer de punten, acht rotorhalzen, DD-boringen, draad en framewebben. Bewaar de reactieplaat apart tot het frame gemonteerd is.
2. Begin met het **middenframe**, beide aslijnen aan de open zijvlakken bereikbaar. Monteer eerst de achterste rij inputs en onderste rotoren, vanaf hun open zijkanten in de halve zittingen. Breng haar rijselector via een open zijkant vóór de flenzen en schuif vervolgens met de U-monden eerst om beide flenzen. Smalle opening naar de as, brede naar de hals. Herhaal voor de voorste rij. Sluit nog geen buitenframe.
3. Schroef buiten het frame iedere pin op zijn schroef; de eerste middenstand ligt met de pinonderkant circa 5,25 mm boven het begin van de buitendraad. Zet de bovenrotoren op de neergaande DD-staarten, punten omlaag. Vang per kolom beide flenzen in één kolomselector en leg die complete kolom vanaf haar eigen open zijkant in het middenframe. Lijn kragen, conische schroefsteun, rotorlichamen en vierkante pinnen met hun geleidingen uit.
4. Controleer alle selectortabs in hun vensters. Schuif de buitenframes zijwaarts over de registratiepennen en sluit de externe voegen met kleine stukjes tape op voet en bovenrand. Geen kraag wordt door een kleinere gesloten boring geperst. Een openende voeg is een stopreden.
5. **Rij UIT:** beneden, zonder stopstukjes. **Rij AAN:** omhoog, één stopstuk onder iedere eindtab. **Kolom UIT:** omhoog, één stopstuk onder iedere eindtab. **Kolom AAN:** beneden, stopstukjes weg. Beweeg beide uiteinden samen; de gevangen flenzen verzorgen actief terugtrekken.
6. Controleer iedere rotorhelft op de volledige slag van 2,40 mm, bij nog gescheiden punten. Een selector mag de axiaal gesteunde schroef niet als geheel meesleuren. Noteer klemmen in DD/geleiding afzonderlijk van puntcontact. Breng de pinnen rond **4 mm boven het hoogste framevlak**. De eerste proef blijft in de band circa **2,5–5,5 mm**; houd ook rekening met hoogteverandering tijdens selecteren. Niet tegen een eindstop nulstellen.
7. Plaats de reactieplaat van onderen, alle selectors UIT. De vier DD-pennen steken via de openingen in de vier inputsockets. Stel de **inputassen alleen tijdens deze voorbereiding** met de hand gelijk zodat de hulp past; forceer niet. De bovenkant van haar brede voet hoort circa 0,20 mm onder de framebodem te blijven. Ondersteun de plaat tijdens de proef en houd frame en plaat tegen meedraaien. Zij mag geen selectorkracht of output ondersteunen. Geen tape bij roterende delen. Na deze voorbereiding blijven alle inputs tijdens iedere zelfuitlijnpoging onaangeraakt.

**De reactieplaat is geen spelingsvrije fixatie.** De nominale DD-passing laat per verbinding circa 26,14° totale omkeerspeling toe. Via reactieplaat → input → onderrotor zijn dat twee verbindingen: samen maximaal circa 52,28° volledige spelingbreedte (±26,14° rond het midden), vóór printfouten. Markeer daarom ook de onderrotor en waar zichtbaar de input; film hun beweging naast de bovenrotor/schroef. Niet handmatig verdraaien blijft verplicht. Passief opnemen van DD-speling is een afzonderlijke mechanische uitkomst, geen bewijs dat de onderhelft exact stil bleef. De bovenrotor kan eveneens eerst zijn DD-speling opnemen voordat de schroef draait.

De nominale volledig geselecteerde flensbuitenvlakken staan 15,76 mm uiteen; tandwortelvlakken 3,36 mm. A heeft daar slechts 0,48 mm rechte overlap. Het oude E-297-tolerantiebudget garandeert dat nieuwe contact niet. Observeer daarom werkelijk volledige slag aan beide uiteinden en meet waar mogelijk de rotorflensafstand. Een extra afstand van 0,24 mm verbruikt al de helft van de nominale rechte overlap; onbekende maatvoering blijft een onzekerheid.

## 4. Proef met verschillende fases

1. Label van boven gezien A=R1/C1, B=R1/C2, C=R2/C1, D=R2/C2. Markeer zichtbare schroef-/rotorstand en een framereferentie. Noteer de resolutie van hoogte en draaihoek. Controleer met alles UIT op zelfstandig teruglopen; dat is een afzonderlijke observatie.
2. Stel bij gescheiden helften de **outputs** bewust op verschillende beginfases. Dit mag door een zichtbare schroefkraag/rotor voorzichtig te draaien terwijl de inputs vaststaan. Houd de pin in zijn geleiding en middenbereik. Noteer de werkelijk ingestelde fases en beginhoogtes; de DD-speling maakt “ongeveer 30°” geen exacte meting. Doe dit vóór de poging, nooit tijdens het sluiten. Nulfase betekent tandvoet tegenover tandvoet, 90° betekent tandvoet tegenover holte.
3. Begin met één rij/twee kolommen: bijvoorbeeld A circa 30°, B circa 60°. Zet beide kolommen omlaag, til de gedeelde rij rustig en gelijkmatig omhoog en observeer of beide outputs **zelf** draaien en alle helften volledig zetten. Geen input verdraaien, output aanraken of rail buigen. Onderbreek meteen als één cel blokkeert. Noteer ook een reeds deels gezette buur. Probeer dezelfde toestand daarna met omgekeerde inschakelvolgorde: rij eerst omhoog, kolommen daarna omlaag.
4. Herhaal voor één kolom/twee rijen met verschillende fases. Probeer daarna alle vier, bijvoorbeeld 30°/60°/120°/150°. Sluit de echte gedeelde staven zonder per pin te helpen. “Gelijktijdig geselecteerd” betekent dat meerdere verschillende fases tijdens dezelfde gemeenschappelijke slag moeten invangen; het achteraf afzonderlijk helpen telt niet.
5. Voer bewust één ongunstige cel in: A circa 0° of ±5° en de overige circa 30°/60°/120°. Noteer of A de hele rij/kolom stopt, of andere outputs al bewogen, en of de selector zijn eindstand haalt. De berekende eindige kroon heeft rond punt-op-punt een dode zone. Een gevonden blokkade is waardevol bewijs; niet forceren. Een aparte poging na terugtrekken en een kleine hoekcorrectie wordt als **geholpen herstart** geregistreerd, niet als geslaagde oorspronkelijke poging.
6. Meet per pin de hoogte en schroefhoek direct vóór en na selecteren, vóór enige aandrijfbeweging. Met 3-mm spoed is 30° rotatie theoretisch 0,25 mm hoogteverandering. Registreer teken en werkelijk gemeten waarde; speling en teruglopen kunnen verschillen veroorzaken. Observeer niet-geselecteerde buren afzonderlijk. Toegestane indexeerbeweging van een geselecteerde pin is geen ongewenste selectie van een buur.
7. Alleen na volledige zetting: leg de bijbehorende stopstukjes onder de hoge selectoren, ontlast de reactieplaat en trek haar recht omlaag weg. Draai met de bestaande losse handgreep iedere input om beurten een kleine slag beide kanten op. Houd de pinhoogtes in de genoemde band. Dit test koppeloverdracht en isolatie, geen gedeelde motor/transmissie.
8. Controleer de vier celtoestanden 00/10/01/11 en de 16 maskers hieronder. In iedere stand worden alle vier inputs met de hand gedraaid; alleen de geselecteerde schroeven mogen worden meegenomen. Bij adreswisselen: input stoppen/ontlasten, rijen terug, gewenste kolommen instellen, zelfuitlijnen met stilstaande inputs, volledige zetting controleren. Als een fase blokkeert, noteer de onuitgevoerde aandrijfproef in plaats van fasehulp te verzwijgen.
9. Test na beide draairichtingen de twee ontkoppelroutes: eerst alleen rij terug, in een nieuwe cyclus alleen kolom terug. Ontlast torsie vóór terugtrekken. Controleer dat draaien van die input daarna de output niet meeneemt. Eindig met inspectie van alle punten; geen duurtest of zwaardere belastingcampagne.

## 5. Resultaten — nog niet uitgevoerd

Datum / 3MF / eventuele profielwijzigingen: ______  A1/A2 vooraf geslaagd?: ______  Filament: ______  Tijd/massa: ______  Nabewerking/schade: ______  Hoogte-/hoekresolutie: ______

| Poging | Beginfases A/B/C/D | Selectie + inschakelvolgorde | Input/onderrotor: draaiing of speling? | Alle helften volledig gezet zonder hulp? | Geblokkeerde cel / rail / hulp / krachtgevoel |
|---|---|---|---|---|---|
| Rij, twee fases | | | | | |
| Kolom, twee fases | | | | | |
| Alle vier, vier fases | | | | | |
| Eén dode fase | | | | | |
| Omgekeerde volgorde | | | | | |

| Poging / pin | Hoogte vóór (mm) | Hoogte na selecteren (mm) | Δh (mm) | Zelf gedraaide hoek / richting | Niet-geselecteerde buur bewoog? |
|---|---|---|---|---|---|
| / A | | | | | |
| / B | | | | | |
| / C | | | | | |
| / D | | | | | |

`10` betekent eerste rij/kolom, `01` tweede. Vul alleen uitgevoerde proeven in.

| R1R2 | C1C2 | Verwacht gekoppeld | Werkelijk / volledige zetting / blokkade / buren |
|---|---|---|---|
| 00 | 00 | geen | |
| 00 | 10 | geen | |
| 00 | 01 | geen | |
| 00 | 11 | geen | |
| 10 | 00 | geen | |
| 10 | 10 | A | |
| 10 | 01 | B | |
| 10 | 11 | A, B | |
| 01 | 00 | geen | |
| 01 | 10 | C | |
| 01 | 01 | D | |
| 01 | 11 | C, D | |
| 11 | 00 | geen | |
| 11 | 10 | A, C | |
| 11 | 01 | B, D | |
| 11 | 11 | A, B, C, D | |

Bidirectioneel gedragen?: ______  Rij trekt los?: ______  Kolom trekt los?: ______  Punten vóór/na intact?: ______  Teruglopen bij loslaten?: ______

## 6. Interpretatie na feedback

Nog geen fysieke resultaten. GO voor een volgende stap is hier niet vooraf ingevuld. De proef kan zelfstandig invangen buiten dode fases aantonen, of juist laten zien dat één fase de hele selector blokkeert. Zij kwalificeert geen automatische invang vanuit iedere fase, productieopbrengst, levensduur, 40-mm slag of gemeenschappelijke motortransmissie. Stop na deze concrete proef; er is geen automatische vervolgopdracht.
