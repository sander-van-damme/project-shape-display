# Compacte passing — Bambu Studio-project

**Status:** READY · **Prioriteit:** P1 · **Beoordeeld:** 2026-10-15. Dit is de 3MF-uitvoering van [de bestaande compacte passingtest](../compact-screw-fit/test.md), dezelfde ene plaat. Fysieke passing is nog onbekend.

Open [**compact-five-pairs.3mf**](compact-five-pairs.3mf) in Bambu Studio als **project**, met de projectinstellingen. Het bestand bevat tien afzonderlijk benoemde delen, het volledige printer-/filament-/procesprofiel, de geslicede G-code en Bambu-previews. Je hoeft geen STL te importeren of CAD te compileren.

| In het project opgeslagen instelling | Exacte waarde |
|---|---|
| Slicer / printer | Bambu Studio **02.08.02.61**; **Bambu Lab X1 Carbon**, hardened-steel **0,4 mm**, Standard hotend |
| Filament | **Generic PLA**, 1,75 mm; dichtheid 1,24 g/cm³; flowratio **0,98**; max. volumestroom **12 mm³/s** |
| Temperatuur / plaat | Nozzle **220 °C** eerste en overige lagen; **Textured PEI Plate 55 °C** eerste en overige lagen |
| Koeling | Partfan **100%**, eerste laag uit; auxfan **0%**; korte-laagvertraging aan, **8 s**, minimum **10 mm/s** |
| Lagen / plaatsing | **0,12 mm**, ook eerste laag; **100% schaal**; per laag printen; bronoriëntatie behouden, complete plaat naar bedmidden verplaatst |
| Wanden / vulling | **Arachne**, **2 wanden**, **100% rectilinear** infill; 5 boven-/onderlagen, bovenschaaldikte 0,6 mm |
| Lijnbreedten | **0,45 mm** nominaal voor eerste laag, buiten-/binnenwand, top, infill en support; Arachne varieert de werkelijke breedte |
| Arachne-details | Minimale wandbreedte **85%** nozzle; minimale feature **25%**; overgangslengte **100%**, filtermarge **25%**, overgangshoek **10°**, verdeling **1** |
| Snelheden | Buiten-/binnen-/kleine wanden, gap fill en alle normale infill/top **30 mm/s**; kleine-perimeterdrempel **20 mm**; eerste laag en bruggen **20 mm/s**; overhangstappen **30/20/10/10 mm/s** |
| Reizen / acceleratie | Travel **150 mm/s**; model/travel maximaal **1000 mm/s²**; eerste-laagextrusie **500 mm/s²**. De officiële X1C-start-/eindbewegingen hebben hun eigen printerwaarden |
| Supports / bedhechting | **Supports uit; brim uit; skirt 0; raft 0; prime tower uit**. De bestaande 0,24-mm CAD-voetjes blijven behouden |
| Maatcorrecties | XY-contour **0**, XY-gat **0**, elephant foot **0 mm**; circle compensation uit; filamentkrimp **100%** |
| Overig | Arc fitting uit voor directe padcontrole; scarf seam uit; seam aligned; geen automatische oriëntatie of schaling |

**Varianten op dezelfde plaat:** pin 1–3 hebben **0,175 mm radiale CAD-relief**, pin 4 **0,15 mm**, pin 5 **0,20 mm**. De schroeven zijn functioneel gelijk. Dotlabels en de plaatindeling blijven behouden. Dit zijn geometrische spelingen, geen gemeten passingcorrecties. Wanddikten blijven 0,400–0,450 mm in de draadzone en 0,44 mm bovenaan.

**Bambu-raming uit de ingebedde G-code:** **1 uur 1 min 40 s totaal**, waarvan **50 min 25 s modelprinttijd**; **3,37 g / 1,128 m PLA**, **153 lagen**. De totale slicerraming bevat de X1C-start-/eindroutine; de werkelijke opwarm-, kalibratie-, purge- en printduur en het werkelijke verbruik zijn niet gemeten.

**Voor het printen:** controleer in de Preview dat alle tien delen op het bed staan, de vijf bovenbuizen een wand hebben en de boringen open zijn. Gebruik de ingestelde Textured PEI Plate en PLA. Wijzig je plaat, filament of profiel, slice dan opnieuw en controleer dezelfde plaatsen. Laat de dunne buitenvoetjes tijdens de passingtest zitten.

**Uitgevoerde controle:** echte Bambu-slice en Bambu-heropening/her-slice van het opgeslagen project zonder externe profielen; onafhankelijke controle van instellingen, behouden brongeometrie en alle 153 lagen. Zie [rapport](validation.json), [heropening](roundtrip.json), [herkomst](build-provenance.json) en [werkelijke padbeelden](toolpaths.png). De oorspronkelijke [STL](../compact-screw-fit/compact-five-pairs.stl) en CAD-bronnen zijn ongewijzigd.

Alle 495 gecontroleerde bovenbuis-/laagcombinaties vormen een gesloten wand; de centrale Ø1,2-mm doorgang blijft in alle 750 pin-/laagchecks vrij. Er zijn geen support-, brug- of overhangpaden en geen losse laagcomponenten zonder overlap met de vorige laag. In de onderste draadzone blijven lokale lijnonderbrekingen aanwezig: maximaal **0,224 mm** op een nominale wandmiddellijn bij pin 5, Z=0,48 mm ([detail](local-gap.png), [methode](local-gap.json)); dit is geen gemeten fysiek gat. Inspecteer die na het printen op gaatjes of zwakte. De padanalyse bewijst geen bedhechting, laagsterkte of draadpassing.

Volg [montage, vijf handcycli, stopcriteria en resultatenformulier](../compact-screw-fit/test.md#3-test-in-enkele-stappen--cto). Geen tang of draadnabewerking. Drie bruikbare nominale paren zijn de fysieke voorwaarde vóór de vierpins-proef; een slicercontrole vervangt die niet.

Controle gebeurde met de Bambu Studio-CLI en onafhankelijke inspectie van de daadwerkelijke G-code, inclusief visueel bekeken laagbeelden. Bambu-geometriepreviews zijn met software-rendering gegenereerd. Geen interactieve GUI-handcontrole, printerverbinding of fysieke print is uitgevoerd.

Voor onderhoud: [generator](../build-bambu-projects.py) gebruikt de officiële 02.08.02.61-resources en ongewijzigde STLs; [onafhankelijke padchecker](../validate-bambu-project.py) leest de ingebedde G-code en 3MF-transformaties. Versies en SHA-256-herkomst staan in `build-provenance.json`. Scratchuitvoer hoort in `work/`.
