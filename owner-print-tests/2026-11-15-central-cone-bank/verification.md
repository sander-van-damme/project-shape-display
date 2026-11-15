# Digitale verificatie — 15 november 2026

**Geen nieuwe fysieke proef uitgevoerd.** Dit dossier onderscheidt nominale geometrie, berekening, echte sliceruitvoer en eigenaarwaarnemingen. READY betekent voorbereid voor de beschreven kleine printproeven; het betekent geen bewezen mechanische bank of elektrisch werkende selector.

## Geometrie en montage

`metadata/geometry-review.json` bevat 611 nominale botsingscontroles plus vier positieve contactproeven van de permanente schroefvangst. Gecontroleerd: beide kanalen onafhankelijk ON/OFF, volledige parkstand2,4mm en extra2,7mm, beide rijposities en tussenposities, rotor-/kapinbouw, geleiders, pinverplaatsing0–8mm met correcte helixfase, riemvolume, NEMA17-body/boss/as op beide toegelaten motorposities, jackbouten/moeren/ringen/veerenveloppen, beide vorken met verschillende standen, voeten/straps/rails/index. Alle60 objecten liggen op het bed binnen256×256, zonder mesh-overlap. Alle componentmeshes zijn gesloten en consistent gewonden; `metadata/meshes.json` geeft maten, volume en hashes.

De ondersteuning is meer dan een plaatje zonder botsingen: schroef0,06mm omlaag raakt de onderste steun,0,06 omhoog raakt keeper; de nominale0,10mm float wordt dus werkelijk begrensd. Dit beoordeelt geen plaatbuiging of sterkte. De werkende schroefhelix is geometrisch gelijk aan A; de vrouwelijke geometrie binnen de historische4,4-mm buitencontour verschilt **0,0mm³**. Alleen buitenwandverdikking naar4,50mm is nieuw. Pinbuitenpassing met4,70 guide blijft fysiek onbekend.

`verify_actuator.py` controleert met OpenSCAD/CGAL tien slider/base/bridge-posities. De Ø2 contactpen steekt4mm onder de followerbody uit en volgt beide dwells zonder de helling met de brede body te overbruggen; berekende lift3mm. De camcoupon blijft een afzonderlijke kracht-/schakelproef. Geen gemeten coilkracht, bistabiliteit, warmtegedrag of volledige elektrische bankwerking. Exacte winding, drivers en grenzen staan in actuator.md.

Montagevoorwaarden uit de controle: beide jacks naar+y op18/25; lange vork heeft een vrijloopuitsparing voor de andere jack; onderkant bewegende veerzetmoer in ON≥z17; circa6mm vrije veerlengte/4,4mm werkende lengte, kracht en solidheight meten; motorflens op2-mm metalen spacers (frontz7/bosstop9, poeliehubonder10); capkoppen≤Ø3,8 zonder grote ringen; motorcentra uitsluitend y−35..−39; motorruimte≥45mm onder datum0. Een niet gemodelleerde ring, grotere motor of gewijzigde montagehoogte is niet automatisch gecontroleerd.

## Werkelijke Bambu-projecten

Officiële **Bambu Studio02.08.02.61**, X1 Carbon0,4, Generic PLA, Textured PEI. `build_projects.py` maakt benoemde objecten, laadt echte printer-/filament-/procesprofielen, slaat3MF met G-code op en **heropent/reslicet zonder externe profielen** in een nieuwe data-directory. Alle opgeslagen instellingen en objectoverrides zijn gelijk gebleven. G-codevolgorde kan bij heropening verschillen; beide archives worden afzonderlijk beoordeeld. Dit was CLI-heropening in de echte Bambu-engine, geen handmatige GUI-bediening of fysieke printerverbinding.

| Job | Eerste slice | PLA | Functie |
|---|---:|---:|---|
| P1 actuator |5u07m12s |16,56g | Zelfstandige passingplaat: één4,50-pin, drie nominale rotor/stiftparen, toleranties en complete actuatorcoupon |
| P2 mechanical |16u36m17s |65,78g | Complete2×2 bank/frame met twee functionele uitgangen |

Schattingen, geen werkelijke printtijden. Totaal circa82,34g PLA. De langzaam geprinte schroeven/pinnen en conservatieve kleine-perimetersnelheden verklaren de relatief lange tijd; grotere stevige delen hebben apart30/40/60mm/s buiten/binnen/infill, met behoud van15/20 voor kritische onderdelen. Exacte heropende tijden en hashes staan in `*-build.json` en `*-slice-review-reopened.json`.

Opgeslagen proces: laag/eerste laag0,12/0,12; Arachne, twee wanden, lijnbreedte0,45/minimum75%, featureminimum10%; gyroid25%,5boven/5onder; kritische pin/schroef/stift100% infill en3mm lokale brim; overige brim uit; geen raft; per laag printen; contour/gat/elephant-footcompensatie0. Buiten15/binnen20/brug15/eerste laag15/infill40mm/s; acceleratie1000, buiten/eerste laag500. Nozzle220°C, bed55°C, fan100% na eerste laag, laagvertraging8s/minimum10mm/s. Alle waarden staan in de projectprofielen, niet alleen in deze tekst.

### Supports en werkelijke draadpaden

**Heruitgave op eigenaarsverzoek:** vier externe bedtorens met diagonale armen stabiliseren iedere40-mm pin en iedere dunne koppelstift. Alleen breeknekken van0,46×0,60×0,24mm raken de buitenvlakken. Pin:16 contacten op8/17/26/35mm; stift:12 contacten op6/10,2/14,4mm. De maximale afstand tussen contacten is9mm respectievelijk6mm. De bestaande schroefsteunen blijven behouden. Automatische supports blijven uit in de binnendraden; deze stabilisatoren zijn echte modelgeometrie in deSTL/3MF, ook als de G-code daarvoor geen Support-rol vermeldt. Een brim ondersteunt de voet maar verhindert hoge zijwaartse wobble niet.

`cad/stability.scad` en `verify_stability.py` controleren één verbonden solid, bedvoeten en gedeponeerde contactnekken; cleanpart-materiaal en pinholte blijven behouden. Dit bewijst geen fysieke printstabiliteit, lossnijdbaarheid of krasvrije buitenpassing. Inspecteer de print en verwijder alle nekrestjes vóór guide-/keypassing. Verscheidene buitenste supportvoeten delen een brim; de afzonderlijke modeldelen botsen niet.

Automatische supports staan **alleen voor bank aan**, normal(auto), vanaf bouwplaat. De aanvankelijke43-mm motorbrug bleek ondanks automatische supports onvoldoende ondersteund. Daarom is de motorplaat afgesplitst, vlak geprint en met4 M3×8 aan de bank bevestigd. Alleen de bereikbare onderzijde van jackpockets krijgt nog supports. Verwijderen via de open onderkant. Geen supports in pinbinnendraden, schroefdraad of koppelingen. De vier externe schroefsteunen zijn echte meegeprinte geometrie; clip alle nekresten weg zoals de eigenaarervaring met A vereist.

`review_toolpaths.py` beoordeelt echte gedeponeerde footprints: pinwandlussen/open bores, cupwanden, rotorboringen, centrale guidewebs en laagverbindingen. Supportlagen hebben eigen tussenhoogten; de model-eilandcontrole vergelijkt modellagen onderling en telt supportpatronen apart. Alleen nul eilandmeldingen is geen bewijs dat een lange brug printbaar is. `verify_supports.py` controleert daarom afzonderlijk echte supports onder de bank, vrij van andere objecten, en neemt de werkelijke bridge-beadhoogte plus0,15mm spleet mee bij de ondersupportcontrole. De resterende maximale vrije bankspan in die controle is3,58mm in beide archives.

De oude4,40-pin had plaatselijke open wandlussen. Een naadgap0%-proef en Classic-proef losten dat niet op. De gekozen buitenverdikking0,05mm per zijde sluit de gecontroleerde wandlussen, met behoud van exact dezelfde binnendraad. Zie `pin-profile-trials.json` en de werkelijke doorsneden `images/critical-pin-paths.svg`. De4,70-guides hebben doorlopende kruisribben en open gaten; ook de tolerantiecoupons zijn afzonderlijk bekeken. Dit beoordeelt deposited-bead-geometrie, geen fysieke laaghechting of printsterkte.

`verify_delivery.py` vergelijkt alle vier originele/heropende archives met de echte STL-platen: facettelling, bidirectionele vertexafstand én windingsgetrouwe driehoekvergelijking. Het maximum staat in `archive-geometry-review.json`. SVG-doorsnede, schema en pinpadfiguur zijn gerenderd en visueel gecontroleerd. OpenSCAD kan de assembly-branche parsen; geen gemeten of fysiek gebouwde assemblage geclaimd.

## Grenzen en reproduceerbaarheid

Nog onbekend: geprinte passing, framehermontage, supportverwijderbaarheid, thermische vervorming, benodigde schroefkracht, OFF-hoogtebehoud, riemgrip/tracking, werkelijke conusslip en extractiekracht, veerconstante, langdurige creep/slijtage en coilkracht/temperatuur. Slip is geen volledige beveiliging. De80-kanaalroute is een lokale geometrische verkenning, geen gecontroleerde complete bank.

Broncommit en bibliotheekversies: `metadata/provenance.json`. CAD/scripts gebruiken relatieve repositorybronnen; Bambu-runtime en tijdelijke sliceprojecten horen buiten de levering. Vanaf de repositoryroot:

```sh
python owner-print-tests/2026-11-15-central-cone-bank/scripts/generate.py
python owner-print-tests/2026-11-15-central-cone-bank/scripts/verify_geometry.py
python owner-print-tests/2026-11-15-central-cone-bank/scripts/verify_actuator.py --scratch /path/to/work/actuator-check
python owner-print-tests/2026-11-15-central-cone-bank/scripts/build_projects.py --bambu /path/to/bambu-wrapper --resources /path/to/resources --scratch /path/to/work/slice-P1 --plate actuator
python owner-print-tests/2026-11-15-central-cone-bank/scripts/build_projects.py --bambu /path/to/bambu-wrapper --resources /path/to/resources --scratch /path/to/work/slice-P2 --plate mechanical
```

Daarna per origineel/heropend project `review_toolpaths.py PROJECT OUT.json --layout metadata/layout.json --plate JOB`; voor mechanical ook `verify_supports.py`. Pythonbenodigdheden en versies staan in provenance; OpenSCAD en officiële Bambu Studio vereist. Alleen de geleverde parameterstand is gecontroleerd. Aanpassen vereist regenereren en opnieuw controleren.

Repositorycheck wordt vergeleken met een pristine documentkopie van de broncommit. Zes historische groottebevindingen blijven behouden: E-266/E-283/E-286/E-288/E-293 en owner-print-tests/AGENTS.md; geen historische experimenten herschreven om die op te ruimen. `git diff --check` moet schoon zijn. Eindmanifest in `metadata/delivery-checks.json`.
