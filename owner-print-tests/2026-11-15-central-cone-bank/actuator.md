# Afzonderlijke actuatorcoupon

Deze coupon is een concrete handmatige krachtsreferentie met twee zelfgewikkelde aantrekspoelen. Elektrisch schakelen onder belasting is **onbewezen**. De coupon is nog niet door deze subagent gesliced; de integrator beheert 3MF en READY/DRAFT-status.

## Geometrie en onderdelen

De cam verplaatst 10 mm tussen s=-5 (OFF) en s=+5 (ON). De follower stijgt 3 mm over een helling van 6 mm. Aan beide kanten ligt een vlakke dwell van 4 mm, waarop de reactiekracht via slider en vloer naar het frame loopt. De lichte metalen detent onthoudt de stand; hij draagt de verticale belasting niet.

Print één base, één slider, twee bobbins, één follower en één bridge. Alle STL-bestanden liggen al in hun printoriëntatie; de bridge ligt omgekeerd op zijn bovenbalk. `layout.json` geeft afmetingen en een mogelijke bedindeling. CAD: `actuator.scad`; export bijvoorbeeld `openscad -o slider.stl -D 'part="slider"' actuator.scad`.

Niet geprint:

- Twee rechte zachte stalen plungers Ø3×24 mm; glad laagkoolstofstaal, geen draadeind. De magnetische eigenschappen blijven onbekend.
- Twee M2×6 klemschroeven en twee M2×30 brugschroeven.
- Eén messing geleider/contactpen Ø2×25 mm, verticaal vast in de follower, **4mm uitstekend onder diens vlakke onderkant**.
- Circa 25 mm verenstaaldraad Ø0,35 mm, epoxy en tape.
- Circa 12,3 m geëmailleerde koperdraad Ø0,20 mm per spoel.
- Eén extra M3-moer en een brede metalen ring (bijvoorbeeldØ20) als licht laadplateau, aan het penbovenstuk vastgezet met epoxy; alternatief een krachtmeter.
- Bekende massa van 30–100 g of gemeten drukveer voor ongeveer 0,3–1 N belasting.
- Begrensde 5 V benchvoeding, twee geschikte MOSFET-kanalen met flyback, zekering en stroommeting.

## Montage

1. Plaats de slider op de vloer. Nominale zijspeling is 0,3 mm per kant, de vloerafstand 0,3 mm. De eindstops staan net buiten de bedoelde ±5 mm posities. Controleer eerst handmatig de volledige slag.
2. Leg de bobbins horizontaal met as in y: centers x=14, y=±27, z=8,5 mm. De 10,95 mm open cradles dragen de 10,8 mm flenzen. Zet de bobbins buiten de boring met tape of epoxy vast. Laat geen lijm in de plunjerboring komen.
3. Wikkel **567 windingen: 63 per laag ×9 lagen**, ongeveer 0,22 mm turnpitch. De vrije windinglengte tussen de flenzen is 14 mm; 72 windingen per laag passen daar niet. Berekende winding-OD is 8,76 mm. Verwacht ongeveer 12,3 m draad, R20≈6,8 Ω en 3,4 g koper per spoel; meet werkelijke winding en weerstand.
4. Plaats de plungers in de sliderclamps met lokale centers y=±21 mm. Hun binnenste uiteinden liggen bij y=±9 mm. Klem elk met één M2×6. As x=14, z=8,5 in de samenstelling. Beide plungers moeten over de hele 10 mm beweging vrij door de bobbins glijden.
5. Steek de 0,35 mm verendraad in het 0,55 mm ankergat bij x=-8, y=-15, z=4,5. Fixeer alleen de eerste 3 mm. Laat ongeveer 15 mm vrij langs +y en buig de laatste circa 3 mm naar +x, zodat de tip bij x≈-5,8, y=0 tegen de twee V-notches aan de sliderzijde loopt. De linkerrail heeft daar een uitsparing. Begin met slechts 0,1–0,3 mm voorspanning. De rechte-cantileverberekening geeft ongeveer 0,13 N/mm; de werkelijk gebogen draad/contactgeometrie wijkt daarvan af. Pas de buiging aan totdat beide dwells behouden blijven zonder grote klikkracht.
6. Schroef de bridge met twee M2×30 in de basepilots. De Ø2×25 messing pen wordt met epoxy in de follower vastgezet, met **4mm onderuitsteek**. Alleen de Ø2 penkop raakt de cam; de7-mm brede followerbodem mag niet op de cam rusten, anders overbrugt hij een stuk helling en wordt de lift kleiner dan3mm. De pen beweegt door de Ø3 brugboring. Het grote verschil is bewust voor deze krachtsproef. Breng de bekende last aan op het penbovenstuk boven de brug (bijvoorbeeld via een aan de laatste2,4mm pen vastgelijmde M3-moer met brede ring/laadplateau. Laat lijm buiten de brugboring en laat hem volledig uitharden; weeg het plateau mee en test eerst zonder toegevoegde massa) of meet de neerwaartse kracht met een krachtmeter. Meet of de follower beide camhoogtes volgt zonder te klemmen. Met4mm onderuitsteek blijft boven de hoge followerflens circa2,4mm ruimte tot de brug. Daar past geen willekeurige drukveer; gebruik een last boven de brug of een vooraf gemeten passende krachtfixture. De25mm pen blijft over de hele slag in de brugboring.

## Kracht en elektrisch testen

Meet eerst met de hand de laterale schakelkracht bij 0,3 / 0,5 / 1 N verticale belasting, in beide richtingen. Zonder wrijving is de benodigde hellingkracht al 0,15 / 0,25 / 0,5 N. Werkelijke camwrijving, detent en plunjergeleiding verhogen die. Dit is waarom elektrisch succes niet vooraf kan worden beloofd.

Elke spoel trekt een eigen stalen plunjer naar zijn midden; links selecteert OFF, rechts ON. Het open magnetische retourpad heeft geen gekwalificeerd krachtmodel. De geometrie voorkomt de onrealistische aanname van sterke aantrekking over een vlakke 10 mm luchtspleet, maar garandeert geen bruikbare insertiekracht. Meet elke spoel ook los op verschillende insertiedieptes.

Gebruik één spoel tegelijk via een logic-MOSFET die daadwerkelijk op 3,3 V gate is gespecificeerd, met 100 Ω gateweerstand, 100 kΩ pulldown en eigen flybackdiode. Beide kanalen starten OFF. Gebruik een 5 V voeding begrensd op 0,5 A en aanvankelijk een serieweerstand van 10 Ω / 5 W. Die weerstand begrenst ook bij kortgesloten spoel tot maximaal 0,5 A. Meet werkelijke stroom; een spanningsinstelling is geen stroommeting. Geen voeding uit GPIO of USB.

Begin met maximaal 200 ms ON en minstens 5 s OFF. Bij 0,5 A is berekend koperverlies circa 1,7 W en warmte per 200 ms circa 0,34 J; adiabatische gemiddelde koperopwarming ongeveer 0,26 K per pulse. Dit is geen duty rating. Stop bij 45 °C, 10 °C temperatuurstijging, brandgeur, schuren of een losse kern. Maak pulses niet steeds langer om tekort aan kracht te verbergen.

Noteer windingen, R20, werkelijke I/V, pulseduur, verticale belasting, piek-handschakelkracht, volledige elektrische slag in beide richtingen (20 cycli), behoud van beide standen gedurende 10 min zonder stroom, temperatuur en schade. Bij onvolledige slag blijft de elektrische selectie onbewezen; de geïntegreerde handbank kan wel als mechanische referentie worden getest. Deze coupon kwalificeert geen bank van 80 kanalen.

## Uitgevoerde CAD-controles

Alle vijf part-exports zijn volgens OpenSCAD eenvoudige solids. Exacte OpenSCAD-intersecties tussen base en slider zijn leeg bij s=-5, -2,5, 0, +2,5 en +5 mm. Een aanvankelijke botsing van plunjerclamps tegen de eindstops is verholpen door die stops buiten de clamps te houden. De spoelas is naar z=8,5 gebracht zodat de flensonderkant 0,1 mm boven de basevloer ligt. Brugvoeten staan buiten de zijrails; de hoge follower heeft geometrisch ruimte onder de brug. Dit zijn CAD-controles, geen fysieke passing of slicercontrole.

**Integratiegrens:**3mm camlift is2,4mm park plus0,6mm extra. Een uiteindelijke elektrische carrier moet de drukveer intern voorgespannen gevangen houden, zoals de M3-jack met bovenstop dat doet;0,6mm compressie vanuit nul levert met een0,2–0,4N/mm veer slechts0,12–0,24N. De opgelegde0,3–1N followerlast meet schakelarbeid, geen reeds geïntegreerde voorspancartridge of positieve conusextractie. Daarom is deze coupon een afzonderlijke onzekerheidsproef.
