# E-300 — twee pinnen, conische wrijving en een stijvere rij

**Status:** DEFERRED — 25 oktober 2026: het huidige eigenaarsverzoek geeft voorrang aan het [minimale schroefframe en de buurgeleidingsproef](../2026-10-25-minimal-friction-screw-frame/test.md). Bestaande CAD, slicercontrole en resultaten blijven behouden; dit is geen nieuwe mechanische afkeur.
**Prioriteit:** geen; het eerdere printaanbod is geparkeerd om binnen maximaal drie READY-printjobs te blijven. Geen vervolgwerk ingepland.
**Datum:** 17 oktober 2026.  
**Bron:** [ontwerp en krachtbalans](../../tools/curated-experiment-checks/E-300/design-report.md), voortbouwend op E-299 op `main`. E-299 en bestaande resultaten zijn ongewijzigd.

## Eén beslissing

Kunnen twee gewone geprinte PLA-conussen bij **stilstaande inputs** volledig sluiten en onder dezelfde gedeelde rijdruk beide pinnen soepel omhoog en omlaag aandrijven? De proef onderzoekt tegelijk de sterkere uitsparingen, kleine hoogteverschillen, herkenbare slip en loskomen. Er zijn geen tanden, veren, coatings of mechanismen per pin toegevoegd.

**Stop:** hard klemmen, zichtbaar buigen, beschadigde draad/cup, openende framevoeg, buurcontact, te zware handdruk of pin buiten de veilige band. Geen tang op bewegende delen, motor of boormachine. Een mislukking niet oplossen met fasezoeken, schuren of extra kracht.

## Print en voorbereiding

Open **[cone-friction-selector.3mf](cone-friction-selector.3mf) als project**, met de opgeslagen X1 Carbon/0,4-mm/PLA-instellingen. Gebruik aanwezige gewone PLA en noteer het exacte type. **Behoud de vaste plaatsing en oriëntatie; gebruik geen automatische plaatsing of oriëntatie.** **Slicerraming: 3 uur 47 min 48 s totaal / 10,48 g PLA** (geen werkelijke printmeting). Instellingen en controles staan in [bambu-settings.md](bambu-settings.md).

Eén plaat: twee framehelften, één gedeelde rij met centrale drukpaddle, twee kolomselectors, twee mannelijke conussen, twee vrouwelijke cups, twee inputassen, één sleutel, twee grote kolomhouders, twee pinnen en één gesteund schroefboompje met twee schroeven. De mannelijke helften zijn laag en hebben een vlakke top; de vrouwelijke hebben een zichtbaar komvormige opening. Er is geen losse rijhouder. **17 printobjecten, 18 mechanische onderdelen** nadat beide schroeven uit het steunframe zijn gehaald.

Oriëntatie: frames op hun deelvlak, rij op haar rug met ontworpen schuine verstevigingen, kolommen op hun brede achterste greepvlak, conussen/cups met de flens op het bed en contactvlak omhoog, pinnen met gesloten top op het bed, schroeven rechtop in hun steunframe. Geen brim of slicersupport in functionele gaten. De steunen rond de schroeven zijn meegetekende modellen en moeten worden verwijderd.

**Controle:** onafhankelijke CAD-controle van 8.451 booleans / 213 poses en 1.620 rasterbuurposes, inclusief belaste sluiting en een concrete 0,10-mm verschilpose. In de definitieve slicerpaden zijn geen losse eilanden bij pinnen, rotoren of selectoren; beide kolommen hebben geen vrije brug-/overhangsegmenten. De rij heeft maximaal 1,81 mm vrije baan, de framebruggen circa 21,98 mm. Alle twintig schroefsteunverbindingen zijn aanwezig; cups zijn open en rotorhalzen blijven gesloten. De dunne behouden pinbinnendraad heeft nog lokale wandonderbrekingen in de nominale paden: inspecteer werkelijk geprinte gaten, scheuren en draadscherfjes. Het gesteunde schroefboompje is geen bewezen bedhechting of verwijderbaarheid. Geen fysieke passing, sterkte of grip is hiermee bewezen.

Verder nodig: gewone tape, pen/liniaal en een reeds aanwezig fijn kniptangetje. Een bestaande keukenweegschaal en schuifmaat zijn nuttig maar niet verplicht. Zonder krachtmeting blijft de druk kwalitatief en wordt geen Newtonwaarde ingevuld.

## Montage — eerst los passen, dan inleggen

1. Laat afkoelen en inspecteer alle delen. Knip de schroefsteunverbindingen aan de **staanderkant** los, van boven naar beneden; steun de schroef vlak naast de verbinding. Knip de voet bij de 1,00-mm-overgang onder de DD-staart los, zonder de eigenlijke staart meer dan 0,10 mm in te korten. Verwijder alleen los steunmateriaal. Stop als een draadkruin loskomt, een schroef buigt of een steunbult de passing blokkeert.
2. Test beide pin/schroefparen buiten het frame enkele slagen op en neer. Controleer iedere rotor op haar DD-as: axiaal schuiven én meedraaien moeten soepel gaan. Plaats een selector zijwaarts om een flens: smalle U-opening aan de aszijde, brede opening aan de halszijde. De flens zit gevangen tussen de twee hoge bladen. Niet spreiden of uitboren.
3. Leg de achterste framehelft plat, deelvlak omhoog. Leg beide inputassen onderin, dikke bus naar beneden. Schuif op iedere input een **mannelijke** conus, contactvlak omhoog. Vang beide flenzen in de gedeelde rij; de centrale paddle gaat door het achtervenster.
4. Schroef iedere pin op haar schroef, pinonderkant circa 5,25 mm boven het begin van de buitendraad. Schuif een **vrouwelijke cup** op de neergaande schroefstaart, opening omlaag. Vang iedere cupflens in één kolomselector. Leg beide complete combinaties in het frame: schroefkraag op haar conische steun, pin in beide vierkante geleidingen, kolomtabs naar de voorkant.
5. Leg de voorste framehelft erop en sluit alleen de externe voegen met kleine stukjes tape. Houd geleidingen, vensters en bewegende delen vrij. A=links en B=rechts vanaf de zijde met de twee kolomtabs. Steek de sleutel van onderen circa 3 mm in een inputbus.
6. Zet de pinbovenkanten rond 4 mm boven het hoogste framevlak. Blijf tijdens de proef tussen **2,5 en 5,5 mm**; stel uitsluitend met ontkoppelde, ontlaste delen terug. Controleer eerst alle slagen zonder conuscontact. De hogere bladen mogen nergens het frame raken. Controleer volledige terugtrekking op bodemcontact in de DD-sockets; de diepere boring is geen garantie voor echte passing. De nominale rij-handbeweging tot eerste belast contact is circa **3,52 mm**, inclusief vang- en houderspeling; het is geen harde eindstop. De kolommen bewegen nominaal 3,00 mm.

**Kolom UIT:** omhoog, grote houder **onder** de tab. **Kolom AAN:** omlaag, houder **boven** de tab. Plaats een houder alleen als hij zonder wrikken past. De houders dragen de reactie van de conusdruk. **Rij UIT:** actief omlaag trekken. **Rij AAN:** uitsluitend centraal op de brede paddle omhoog drukken en die druk tijdens het draaien vasthouden. De rij mag beperkt links/rechts kantelen; niet één uiteinde apart omhoogduwen. Een vaste rij-eindstop is geen krachtinstelling.

## Korte proef

1. **Stilstaand sluiten.** Zet beide kolommen AAN en houd beide inputs stil. Begin met gescheiden helften en verschillende zichtbare beginhoeken, bijvoorbeeld A circa 0° en B circa 70°. Druk de rij centraal rustig omhoog. Beide cups moeten hun conus omvatten, zonder bodemcontact, framecontact of zichtbare buiging. Markeer/meet de twee sluitposities; alleen het bereiken van een vensterrand bewijst geen contact. Selecteren mag geen bedoelde schroefrotatie of pinverplaatsing vragen. Noteer elke beweging of speling apart.
2. **Grip bij dezelfde druk.** Houd de rijdruk aan. Draai input A en vervolgens B elk maximaal 1/4 omwenteling heen en terug, zonder de rij of een individuele cup tussendoor bij te stellen. Beide outputs moeten volgen; 1/4 schroefomwenteling geeft theoretisch 0,75 mm. Herhaal sluiten bij twee andere willekeurige hoekparen. Eerst sluiten, dan draaien; iedere hulp tijdens sluiten apart als mislukte/onduidelijke poging noteren.
3. **Druk en slip.** Begin telkens licht en verhoog alleen binnen comfortabele handdruk. Vergelijk beide pinnen bij dezelfde druk in beide richtingen. Voor een korte herkenbare slipproef mag een zichtbaar bovenrotorlichaam met een zacht vingercontact licht worden afgeremd terwijl de input voorzichtig beweegt. Raak geen draad/contactvlak aan, druk niet op de pin en gebruik geen gereedschap. Zodra input en onderste rotor draaien terwijl de bovenrotor stil blijft, is slip zichtbaar; stop meteen. DD-speling of een doorslippende sleutel is geen conusslip. Kan dit niet veilig worden waargenomen, vul slipgrens **onbekend** in; forceer geen blokkade.
4. **Kleine hoogteverschillen.** Controleer of de rij vrij een kleine helling kan aannemen en beide pinnen blijven volgen. Alleen na een goede nominale proef: desgewenst één gemeten dun laagje tape op het statische bovenste contactvlak van één kolomhouder aanbrengen, ver van de rotoren. Monteer de houder opnieuw zonder wrikken; noteer de werkelijke dikte en nieuwe kolompositie. Dit verandert één sluitniveau. Herhaal één gezamenlijke sluit-/gripproef zonder individuele hulp en verwijder de tape daarna. Geen bekende shimdikte of nieuwe positie: noteer een kwalitatieve proef, geen gekwantificeerd vereffenbereik.
5. **Selectie en buur.** Controleer de acht standen hieronder. Stop beide inputs vóór iedere wijziging; rij eerst terug, kolommen instellen/borgen, rij sluiten bij stilstaande inputs. Draai beide inputs afzonderlijk zacht heen en terug. Alleen de geselecteerde pinnen mogen bewegen. Doe bij alleen A en alleen B elk drie korte op/neercycli. Een kantelstop bij één geselecteerde pin is geen bewijs van tweepuntsvereffening.
6. **Loskomen.** Na een korte aandrijfslag torsie ontlasten en alleen de rij volledig terugtrekken. Draai de input zacht: output blijft stil. Sluit opnieuw en trek nu alleen de betreffende kolom terug; herhaal na de andere draairichting. Noteer plakken, extra terugtrekkracht en meegesleepte output. Inspecteer cup, flens, uitsparingen, sleutelbus en draad. Stop hier.

| Rij | Kolom A | Kolom B | Verwacht gekoppeld |
|---|---|---|---|
| UIT | UIT | UIT | geen |
| UIT | AAN | UIT | geen |
| UIT | UIT | AAN | geen |
| UIT | AAN | AAN | geen |
| AAN | UIT | UIT | geen |
| AAN | AAN | UIT | A |
| AAN | UIT | AAN | B |
| AAN | AAN | AAN | A en B |

**Optionele krachtmeting:** ondersteun uitsluitend de centrale rijpaddle via een stevig bestaand blokje op een keukenweegschaal, buiten de frameomtrek. Houd frame en inputs vrij van weegschaal/blok. Druk het frame langzaam omlaag zodat de weegschaal de rij omhoog belast; houd kanteling en zijwaartse belasting klein. Noteer de onbelaste uitgangslezing en trek die af. `F_rij≈0,00981×Δgram N`. Beproef hoogstens circa 50/100/200/300 gram extra (0,5/1/2/3 N), stop eerder bij buigen/klemmen. Zonder stabiele vrije krachtweg is de lezing ongeldig. Deze meting omvat geleidingswrijving en zegt niet dat iedere cel de helft krijgt. Noteer de laagste druk waarbij **beide** pinnen volgen, en de druk bij zichtbare slip. Een getal zonder meetopstelling is geen meting. Zonder koppelmeter blijft de slipgrens een gripwaarneming bij bekende rijdruk, geen gemeten koppel in Nmm.

## Resultaat en grens

Vul [resultaten.md](resultaten.md) in. Praktisch positief: complete bruikbare print, eenvoudige montage, sluiting zonder draaien bij alle geteste hoeken, beide pinnen onder dezelfde lichte druk in beide richtingen aangedreven, geen zichtbare buiging/buurbeweging en beide ontkoppelroutes werken. Onvoldoende grip, klemmen of één droog blijvend contact is een waardevolle negatieve uitkomst.

De echte aandrukkracht, slipkoppel, lange stangen en meer dan twee gelijktijdige contacten zijn pas bewezen voor zover ze werkelijk gemeten zijn. De beperkte kantelrij kan geen willekeurige hoogtefouten van veel koppelingen vereffenen. Er zijn nog geen fysieke resultaten; na deze ene oplevering volgt geen automatische vervolgopdracht.
