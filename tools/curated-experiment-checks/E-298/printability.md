# E-298 — X1 Carbon: scherpe punten versus werkelijk geslicete toppen

De twee projecten zijn echte Bambu Studio 02.08.02.61-projecten met afzonderlijke onderdelen, vaste oriëntatie, opgeslagen X1 Carbon/0,4-mm nozzle/Generic PLA-profielen en gegenereerde G-code. Beide zijn zonder externe profielen opnieuw geopend en geslicet. Er is geen fysieke print uitgevoerd. De CLI-heropening is geen interactieve GUI-controle. De headless OpenGL/GLEW-thumbnailrenderer faalde; de losse `toolpaths.png`, `point-toolpaths.png` en `critical-toolpaths.png` tonen echte geslicete banen in plaats van een gerenderde Bambu-thumbnail. Dit verhindert de configuratie, G-code of heropening niet.

## Profiel en herkomst

Basis: het bestaande, door de eigenaar ongewijzigd geprinte E-295 compact-project. E-298 wijzigt alleen nieuwe projecten: 0,08-mm lagen, eerste laag 0,12 mm; Arachne minimum wall width 75% en minimum feature size 10%. De 0,45-mm aanbevolen normale lijnbreedten, twee wanden, 100% infill, conservatieve snelheden/versnellingen, temperaturen en koeling blijven uit dat profiel. Test A heeft geen brim; Test B een buitenbrim van 3 mm met 0-mm afstand. Geen supports, geen raft. Alle exacte opgeslagen waarden staan per test in `bambu-settings.md` en `slicer-review.json`. Geen E-295/E-297-bestand is aangepast.

Officiële gepinde bron: [Bambu PrintConfig.cpp](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.cpp#L6417), regels 6417–6440. Deze beschrijft expliciet dat features onder minimum feature size wegvallen; overblijvende dunne features worden verbreed tot minimum wall width. Beide percentages gelden ten opzichte van de nozzle. Bron-SHA256: `d4e96aaca40b0698de720537ba0d2af46efbb576e183507c763c0654e394e99c`. Standaard 25%/85% betekent 0,10/0,34 mm bij deze nozzle. E-298 10%/75% betekent 0,04/0,30 mm; dit zijn slicergrenzen, geen bewezen fysieke maatnauwkeurigheid.

Gepinde [Ubuntu 24.04 AppImage](https://github.com/bambulab/BambuStudio/releases/download/v02.08.02.61/BambuStudio_ubuntu24.04-v02.08.02.61-20260820225108.AppImage), SHA256 `d501b103fac5424513ec0e8d6bc145fb30719de2c7d94d7320d723740c81a7fd`. Pakketten/runtimes staan uitsluitend onder work. Bronprofielbestanden en hashes staan in de twee `point-*-build.json`-bestanden.

## Waarom geen mathematisch naaldpuntje

Een 0,16 × 0,16-mm CAD-kroon met 0,60-mm taper gaf een echte Bambu-slicerfout: lege lagen tussen 8,28 en 8,60 mm; zie `printing/rejected-016-tip-result.json`. Dit verworpen bestand is geen printaanbod. De definitieve CAD-kroon is 0,30 mm radiaal en ongeveer 0,30 mm tangentieel. Ook die volledige kroon wordt niet behouden: de punt wordt door de discrete lagen en korte Arachne-banen afgerond en afgekapt.

| Geometrie | CAD-top | Laatste extrusielaag | Ontbrekende top | Laatste nominale bead-footprint per punt, ongeveer |
|---|---:|---:|---:|---|
| point48, A en matrix | 8,60 mm | 8,44 mm | 0,16 mm | 0,70 mm radiaal × 0,98 mm tangentieel |
| point60, A | 8,60 mm | 8,36 mm | 0,24 mm | 0,74 × 1,05 mm |
| point60skew, A | 8,60 mm | 8,36 mm | 0,24 mm | 0,74 × 1,05 mm, gedraaid |

Deze footprints zijn buffers rond G-code-centerlijnen met de geslicete lijnbreedte, geen gemeten materiaaldoorsneden. Per punt en laag zijn breedten, oppervlakte, vorige-laagoverlap en bounds vastgelegd in `point-paths.json`. Alle twaalf testhelften en acht matrixhelften hebben twee laatste-laagcomponenten met overlap op de voorgaande laag. Vier identieke exemplaren van iedere A-variant tonen in deze controle dezelfde laatste hoogte; hun fysieke printvariatie is onbekend.

Het eindigt dus in een klein afgerond topvlak, niet in een exact punt of alleen een lange mesrand. De brede top maakt een punt-op-puntvlakcontact mogelijk en vergroot de onbekende fysieke dode zone. De skew-variant breekt geometrische symmetrie maar bewijst niet dat zo'n vlakcontact altijd losloopt. Dit is een belangrijke uitkomst van de printvoorbereiding, niet een verborgen tolerantie. De lagere effectieve tiphoogte verkleint de geleidingshelling; de rechte dragende flanken onder de taper blijven aanwezig. Hun lastcapaciteit is niet gemeten.

Een kleinere nozzle kan theoretisch kleinere banen leveren; een officiële X1-series 0,2-mm hotend bestaat, maar is niet gekozen of aangeschaft. De geleverde projecten zijn voor de huidige 0,4-mm configuratie. De beste scherpte binnen deze beperkte vergeleken CAD-/profielkandidaten is niet bewezen het globale optimum van alle X1C-processen.

## Betekenis van de controles

De onafhankelijke archivecontrole vergelijkt getransformeerde meshvertices en georiënteerde facetten met de STL. De G-codecontrole onderzoekt alle extrusielagen op losse componenten zonder overlap, booropeningen, nekwanden en schroef/pin-banen. Dit toont geplande materiaalbanen, geen hechting of fysieke sterkte. Een vrij centraal schijfje r=0,60 mm is een verstoppingsscreen; het bewijst niet de hele DD-/schroefdraadpassing.

Test B bevat slanke verticale schroeven met externe brim. Ondersteuning staat uit zodat interne schroefholtes niet worden volgeprint. Brim-contact wordt afzonderlijk gecontroleerd. Verwijder de buitenbrim voorzichtig volgens de montage-instructies; geen ondersteuningsmateriaal uit functionele draad snijden. De koeling, brugkwaliteit en stabiliteit van de slanke onderdelen moeten fysiek blijken. De status van B blijft uitgesteld tot A zinvol positief resultaat geeft.

Herproduceer met `printing/build-project.py --help`, de gepinde executable/resources en tijdelijke scratchmap. Het script bewaart en heropent het project. Daarna `validate-project.py`, `critical-paths.py --dog-root 6.2`, `point-paths.py` en `compare-reslice.py`. Geen upload, netwerkprinteractie of printopdracht is uitgevoerd.

## Vastgelegde resultaten van de definitieve projecten

- A: 18 meshonderdelen; modeltijd 44m34s, totale schatting 57m52s, 1,62 g. B: 37 onderdelen; modeltijd 6h28m34s, totale schatting 6h41m51s, 18,28 g.
- Beide: bronfacetten inclusief winding behouden; nul losse extrusielaagcomponenten zonder overlap met de voorgaande laag. Dit omvat de puntlagen. Grootste vrije bridge/overhang-centerline A 1,459 mm, B 5,120 mm; grootste ankerafstand respectievelijk 0,453/0,950 mm. Dit zijn inspectiesignalen, geen gemeten brugkwaliteit.
- Alle twintig koppelinghelften: 66 gescreende centrale boorlagen per helft vrij op r=0,60 mm; 14 neklagen gesloten, nul gaten in de nominale middenwandlijn.
- Vier matrixpinnen: gewone buiszone 134 lagen per pin gesloten. In de draadzone zijn **35–37 van 76** lagen per pin niet volledig gesloten volgens nominale bead-footprints, maximale middenwandonderbreking **0,199 mm**. Dit bestaande dunwandige geometrieprobleem wordt niet als geslaagd weggepoetst. Interlaagbinding en de succesvolle E-295-draad geven reden om fysiek te testen, maar bewijzen hier geen sterkte of sluitende wand.
- Vier schroeven: elk 197 onderzochte draadlagen met één verbonden materiaalcomponent, minimale dekking van de centrale r=0,45-mm schijf circa 85,0%; werkende crest-radius minimaal 1,591 mm. De eindaanloop is smaller. Alle vier eerste lagen hebben echt brim-contact met 0-mm nominale spleet.
- Heropening: instellingen exact gelijk, geometrische extrusievolgorde niet byte-identiek. Grootste symmetrische footprintverschil per laag A **1,476%**; B **6,160%** bij z=23,08 mm (1,029 mm² op 16,709 mm² oorspronkelijke oppervlakte). Dit is meer dan uitsluitend tekstuele afronding: de hergeslicete draadzone is daarom apart gecontroleerd. De oorspronkelijke G-code is ingebed; wie opnieuw slicet, produceert mogelijk andere lokale banen. Geen van beide is fysiek gekwalificeerd.

De hergeslicete B-kritieke controle (`reopened-critical-paths.json`) behoudt vrije boorscreens, gesloten nekwanden en gewone buiswanden; de draadzone heeft 36–38/76 open-footprintlagen per pin met maximaal dezelfde 0,199-mm middenwandonderbreking. Alle vier schroeven behouden één verbonden component in 197 draadlagen en minimaal circa 85,0% kerndekking. Zo is de reslicevariatie begrensd op deze gecontroleerde kenmerken; zij verdwijnt niet door heropening.
