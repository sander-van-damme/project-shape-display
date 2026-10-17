# Verificatie en technische reproductie

Uitgevoerd op 17 oktober 2026. Geen motor, printer of Uno fysiek aangesloten.

| Controle | Resultaat |
|---|---|
| Vier CAD-bronnen / vijf printobjecten | Gesloten, consistent georiënteerde meshes; één lichaam per bron |
| Mechanische CAD | 41 standen over 3 mm, maximale nominale botsing 0 mm³ tussen pin/schroef/houder/frame |
| Draad versus oorspronkelijk 0,175-paar | Volumesymmetrisch verschil circa 0,000012 mm³ schroef / 0,000019 mm³ pin; float32-exportverschil, geen functioneel herontwerp |
| Officiële Bambu Studio 02.08.02.61 | Nieuw project gesliced/opgeslagen, returncode 0 |
| Datzelfde project zelfstandig heropenen en reslicen | Returncode 0; alle projectinstellingen identiek; 10,43 g in beide slices |
| Onafhankelijke baancontrole, beide slices | Alle vijf objecten aanwezig vanaf laag 1; geen nieuw los component >0,005 mm²; geen slicersupports; open pinholte en motor-/geleidingsenvelop gecontroleerd |
| Dunne pinwand | 23 draadlagen met lokale nominale onderbrekingen; bovenste buis gesloten; geen claim dat onderwand gesloten/sterk is |
| Bruggen | Houder maximaal 10,38 mm vrije middellijn; frame 6,98 mm; fysieke doorhang onbekend |
| Uno-programma | AVR-core 1.8.8 + TMCStepper 0.7.3 gecompileerd: **11922 bytes flash, 484 bytes statisch RAM** |
| Reisgrenzen | `test_motion.cpp` geslaagd; beide grenzen, weigerende overschrijdingen, herhaalde cycli, nulafstand, NaN, oneindig en losse-motorstanden |
| Repositorycontrole `./repo check` | Mislukt door bestaande grootteoverschrijdingen in E-266/E-283/E-286/E-288/E-293 en beide AGENTS.md-bestanden; die bestanden zijn niet gewijzigd |
| Fysieke passing, UART, fasestroom, motorvermogen, betrouwbaarheid | Niet uitgevoerd; invullen in `test.md` |

De slice/meshtests beschrijven nominale geometrie en paden, geen echte beads,
bedhechting, motorkoppel of fysieke veiligheidstest. De bedradings-SVG en
mechanische SVG zijn gerenderd en visueel bekeken. De baanbeelden zijn uit
echte Bambu-G-code opgebouwd. Geen interactieve Bambu-GUI-inspectie geclaimd.
Headless Wayland/GLFW- en ZFiller-meldingen staan beschreven in `bambu-settings.md`.

## Reproductie voor een engineer

**Voor de eigenaar is dit niet nodig: open de meegeleverde 3MF rechtstreeks.**
Werk vanuit de repositoryroot. Tijdelijke tools/logs blijven buiten de checkout.
Python-vereisten: numpy, trimesh, manifold3d, scipy, shapely, matplotlib;
optioneel cairosvg om de meegeleverde SVG's te renderen.

BOSL2 is vastgezet op `136e6367e65d52196a3ea51d03156f8b622c60fc`.
`rig.scad` hergebruikt het naastliggende E-295 `thread-kernel.scad` uit de repo.
CAD genereren:

```sh
python owner-print-tests/2026-10-17-microstepper-screw-pin/generate.py \
  --bosl2 /pad/naar/BOSL2 --scratch /tmp/microstepper-cad
```

Download de officiële Bambu AppImage van
<https://github.com/bambulab/BambuStudio/releases/download/v02.08.02.61/BambuStudio_ubuntu24.04-v02.08.02.61-20260820225108.AppImage>.
Controleer SHA-256 **d501b103fac5424513ec0e8d6bc145fb30719de2c7d94d7320d723740c81a7fd**
vóór gebruik. Op deze machine waren extra WebKit/JavaScriptCore-runtimebibliotheken
nodig; die zijn via ondertekende Debian-APT-indexen opgehaald, gecontroleerd en
uitsluitend lokaal uitgepakt. Geen checksum/TLS/signatuurcontrole uitgezet.

De generieke bestaande projectbouwer is alleen hergebruikt; aan E-299 is geen
CAD of ontwikkelwerk toegevoegd. Geef een werkend Bambu-executable/launcherscript
en zijn officiële `resources`-map mee:

```sh
python tools/curated-experiment-checks/E-299/printing/build_project.py \
  --bambu /pad/naar/bambu-studio --resources /pad/naar/resources \
  --scratch /tmp/microstepper-slice \
  --stl owner-print-tests/2026-10-17-microstepper-screw-pin/microstepper-rig.stl \
  --out owner-print-tests/2026-10-17-microstepper-screw-pin/microstepper-rig.3mf \
  --name 'Single microstepper screw pin 0.12 X1C PLA'
python owner-print-tests/2026-10-17-microstepper-screw-pin/validate.py \
  --resliced /tmp/microstepper-slice/reopen/microstepper-rig.3mf
```

De bouwer voert ook de zelfstandige heropening/reslice uit. `saved-settings.json`
is de volledige export van de daadwerkelijk opgeslagen settings. `geometry-validation.json`,
`slicer-review.json`, `layout.json` en `microstepper-rig-build.json` bewaren
de uitvoer, profielherkomst, hashes en scope. De objectnamen zijn via de layout
aan de vijf meshes gekoppeld; geen automatische herschikking/orientatie.

Softwarecheck vanuit deze testmap:

```sh
arduino-cli compile --fqbn arduino:avr:uno --warnings all controller
g++ -std=c++11 -Wall -Wextra -pedantic test_motion.cpp -o /tmp/test-motion
/tmp/test-motion
```

Arduino CLI 1.5.2-rc.1 is gebruikt. De laatste compilatie eindigde met code 0;
het firmwaregedrag op hardware is daarmee niet bewezen. De reisgrenstest gebruikt
dezelfde header als de Uno-firmware; hij vervangt geen UART-/elektronicatest.

Geen fysieke resultaten ingevuld, geen nieuwe onderzoeksopdracht of vervolgarchitectuur.
