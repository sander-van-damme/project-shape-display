# E-300 reproduceren

Gebruik de Shape Display-repository met basiscommit `c341244ede59ce92ab63f8edd5bcb14907a87f6c`. Dit pakket voegt alleen E-300 en `owner-print-tests/2026-10-17-cone-friction-selector/` toe. De oude E-297-helper en exacte E-299-schroef/pin/steunmeshes worden alleen gelezen. De schroefgeometrie wordt niet opnieuw benaderd.

Voor printen is uitsluitend het meegeleverde, geconfigureerde `cone-friction-selector.3mf` nodig. Open als project in Bambu Studio; montage/test en het lege resultatenformulier zijn PDF's. Niet automatisch oriënteren of plaatsen.

Voor technische reproductie, vanaf de repositoryroot:

1. Python met CadQuery, numpy, trimesh, manifold3d, scipy, shapely, matplotlib en reportlab; de eigen bouwsessie gebruikte CadQuery 2.7.0 en Bambu Studio 02.08.02.61. Runtimes/downloads blijven buiten de repository en zitten niet in het pakket.
2. `python tools/curated-experiment-checks/E-300/cad/generate.py`
3. `python tools/curated-experiment-checks/E-300/review/geometry_review.py` en `python tools/curated-experiment-checks/E-300/review/array_review.py`
4. `python tools/curated-experiment-checks/E-300/analysis.py` en `python tools/curated-experiment-checks/E-300/analysis/thrust_face.py`
5. De Bambu-builder krijgt expliciet `--bambu`, `--resources`, `--scratch`, `--stl` en `--out`; zie `printing/build_project.py --help`. Gebruik de gegenereerde `owner-print-tests/2026-10-17-cone-friction-selector/cone-friction-selector.stl` en sla `cone-friction-selector.3mf` op. De builder sliceert, exporteert, heropent zonder externe profielen en sliceert opnieuw. Alle instellingen staan in het 3MF-archief en `bambu-settings.md`.
6. `printing/review_project.py`, `review_cones.py`, `review_selectors.py`, `review_braces.py` en `compare_reslice.py` controleren de concrete G-code, ook die van de heropende slice. Zie hun `--help`. De JSON-uitvoer bevat de beoordeelde 3MF-hash: verwissel geen oudere plaat met een nieuwe beoordeling.
7. `make_drawings.py`, `make_section.py` en `make_manual.py` maken illustraties/PDF's. `verify_delivery.py` controleert bronintegriteit en de definitieve oplevering; `./repo check` controleert repositorystructuur.

CAD en slicerpaden zijn geen fysieke resultaten. Alleen de eigenaar vult de resultaatvakken in. Geen vervolgprint of automatische taak is onderdeel van dit pakket.
