# E-302 — lange schroef met verwijderbare supports

De lange schroef heeft **48 mm schroefdraad en 50,4 mm totale lengte**, inclusief
de behouden vierkante voet. In de 3MF ligt zij horizontaal: de as ligt 5 mm boven
het bed, de totale printhoogte is slechts 10 mm. Normale supports lopen vanaf de
plaat onder de draad. Zo ontstaat geen vrijstaande schroefkolom van 50 mm.

![Werkelijke banen van schroef en supports](long-screw-review.png)

## Opgeslagen instellingen

Alleen object `10-screw-50-supported` krijgt supports. De andere negen objecten
hebben expliciet `enable_support=0`, zodat pinboringen en koppelingen vrij blijven.
De globale instelling staat eveneens uit; de **objectinstelling** schakelt de
supports voor de lange schroef in. Zie [opgeslagen objectinstellingen](saved-object-settings.json).

| Instelling lange schroef | Waarde |
|---|---|
| Type / stijl / plaatsing | Normal(auto), snug, alleen vanaf bouwplaat |
| Supporthoek / kleine overhangen verwijderen | 45° / uit |
| Bovenste / onderste Z-afstand | 0,24 / 0,24 mm |
| XY-afstand | 0,35 mm |
| Bovenste interface | 2 lagen, rectilinear, tussenruimte 0,2 mm |
| Basispatroon tussenruimte | 2 mm |
| Support / interfacesnelheid | 20 / 15 mm/s |
| Brim lange schroef | Buitenom, 3 mm, afstand 0,12 mm |

De schroef behoudt het bestaande draadprofiel; alleen de lengte en printoriëntatie
zijn gewijzigd. Model-laaghoogte 0,12 mm, PLA, X1 Carbon met 0,4-mm nozzle.

## Controle van de echte slice

Bambu Studio **02.08.02.61** heeft de opgeslagen 3MF zelfstandig heropend en opnieuw
gesliced zonder externe profielen. Globale en objectinstellingen bleven gelijk.
`review_long_screw.py` controleerde beide G-codes; de onderstaande resultaten zijn
voor beide gelijk.

| Controle | Resultaat |
|---|---|
| Hoogste schroeflaag | Z 9,96 mm; CAD-hoogte 10 mm |
| Supportbanen / interfacebanen | 4.776 / 2.387 |
| Support buiten het lange-schroefgebied | Geen |
| Support vanaf bouwplaat | Vanaf Z 0,12 mm; eerste nominale footprint 320,02 mm² |
| Supportinterface, projectie langs draad | Plaat-X 10,737–58,395 mm; draad X 10,4–58,4 mm |
| Lengtedekking in stroken van 0,1 mm | 477 / 480 stroken, 99,375%; grootste ongedekte reeks 0,3 mm bij de voet |
| Nieuwe model-eilandjes boven support | Alle 16; verticale opening 0,24–0,36 mm door laagafronding |
| Nieuwe model-eilandjes zonder onderliggende support | Geen |

Deze controle gebruikt nominale extrusiebreedtes. Lengtedekking betekent dat
supportinterface onder die X-strook aanwezig is; het is geen claim dat ieder punt
van de schroef over het hele oppervlak wordt gedragen. De bovenste draadlagen
bouwen verder op de schroef zelf. De negen andere onderdelen behouden de bestaande
laagcontactcontrole; pinnen en koppelingen bevatten geen slicersupport.

De complete plaat wordt geschat op **14,13 g PLA en 4u17m16s**; de heropende slice
schat 4u17m34s. Geen fysieke print, passing, stijfheid of supportverwijdering getest.

## Verwijderen en testen

Laat de plaat afkoelen en neem schroef en supports samen van de flexplaat. Ondersteun
de schroef vlak bij de plaats waar je support losmaakt. Pel de support in kleine
stukjes van de onderzijde; buig niet aan de hele lange schroef. Verwijder ook de
brim rond de voet, maar behoud de functionele vierkante voet zelf.

De support raakt de buitenste schroefdraad. Controleer die onderzijde op PLA-resten,
afgebroken draadtoppen en littekens. Draai de schroef **eerst met de hand** door de
50-mm pin over het bruikbare draadtraject. Stop bij klemmen of beschadiging; laat
de motor de verbinding niet forceren. Noteer schoonmaaktijd en beschadiging in het
resultatenformulier. Verwijderbaarheid en draadkwaliteit blijven fysieke testpunten.

De 50-mm vrouwelijke pin staat nog op haar bestaande brede voet; daar zitten geen
supports in de boring. De lange schroef krijgt de hier getoonde steunconstructie.

Bewijs: [eerste slice](long-screw-review.json),
[heropende slice](long-screw-review-reopened.json),
[bouw en roundtrip](microstepper-frame-v2-build.json).
