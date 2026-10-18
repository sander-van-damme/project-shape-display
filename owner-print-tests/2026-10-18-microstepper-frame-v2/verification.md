# E-302 — verificatie revisie 2, 18 oktober 2026

Geen fysieke print, pasproef of motorproef uitgevoerd. READY betekent dat het
gevraagde digitale printpakket gecontroleerd is, niet dat fysieke succescriteria
al zijn behaald.

| Controle | Uitkomst / bewijs |
|---|---|
| Remote | Eerste versie basis0383489; revisie op eigenaarfeedback vanaf3d554a3; remote opgehaald, geen andere wijzigingen |
| Meshes | Acht bronnen gesloten, consistent georiënteerd, één lichaam per STL; plaat10 lichamen |
| CAD-review | Drie kopvarianten ×25 standen; 50-mm pin,3-mm slag, geen nominale botsing houder/frame, houder/schroef, schroef/frame of pin/frame |
| Motorsteun | Aanvullende veren buiten de PCB-opening; meer cilindrische steun boven/onder; nominale0,1-mm veerinterferentie, geen gemeten klemkracht |
| PCB-uitsparing | Complementaire helften; volledige ruimte X−8…−2,5,Y±3,5,Z2…10,5 vrij in gemonteerde CAD |
| Toegevoegde pinnen | Twee bestaande schroeven +18-mm pin ongewijzigd;50-mm pin behoudt onderste18 mm en6-mm draad |
| Axiaal | Bestaande ring/dek/keeper behouden; nominale onderschouderruimte0,49 mm, keeper0,3 mm; diepe ribben zonder axiale tandwielstop |
| Officiële Bambu Studio | Versie02.08.02.61; bouw/slice en zelfstandige heropening/reslice beide exit0 |
| Instellingen | Printer X1 Carbon/nozzle0,4, PLA en proces opgeslagen; geen verschillen na heropening |
| Toolpathlobben | Alle4 koppelingen, ieder64 rechte boringlagen; alle3 lobben aanwezig, centrale radius0,80 mm open, beide slices |
| Kleinste lobe-uitsteking | A0,235; N1 circa0,195; N2 circa0,199; C0,146 mm, berekend uit nominale extrusievoetafdruk |
| Ondersteuning | Alle10 onderdelen zonder nieuwe ongeankerde eilanden boven0,005 mm²; geen slicersupports |
| Frameveerbrug | Eerste bruglaagZ4,08,3 X-brugbanen met beide einden ondersteund; vrije span9,98 mm |
| Vierkante holte kop | Dakbrug maximaal10,38 mm met ondersteunde uiteinden; fysieke doorhang onbekend |
| Afbeeldingen | Montage, plaat, echte rib-toolpaths en eerste veerbruglaag visueel bekeken |
| Lange print |417 lagen tot slicerZ50,04;366 bovenlagen gesloten contour, kernradius0,60 vrij, geen nieuwe ongeankerde eilanden; voet12 mm behouden |
| Fysiek | Onbekend: PCB-envelope, motorstabiliteit, montagekracht, tandpassing, slip, tweede motorhoogte, slijtage |

**Bambu-check is uitgevoerd via de officiële Bambu Studio CLI-engine**, met
heropening van het uiteindelijke project zonder externe profielen. Geen interactieve
GUI-inspectie geclaimd. De afbeeldingen zijn uit werkelijke G-code gemaakt.
De twee slices hebben gelijk opgeslagen instellingen maar kleine verschillen in
banen; beide zijn apart gecontroleerd. Zie `microstepper-frame-v2-build.json`
voor hashes en roundtrip, `saved-settings.json` voor alle waarden.

De herziene oorspronkelijke slice schat13,62 g en4u06m54s totaal (model3u51m15s).
De zelfstandige heropening schat eveneens13,62 g en4u06m42s totaal.
Schattingen zijn geen fysieke waarnemingen. Niet alle CAD-contouren worden exact
gevolgd: de gemeten nominale ribtipradius in de slice is A0,962–0,986,
N1 1,007–1,032,N2 1,007–1,028,C1,054–1,081 mm. Daarom worden drie kleine
passingsvarianten en twee identieke nominale koppen geleverd.

Zie ook [lange pin: printstabiliteit en grenzen](pin-print-verification.md).

![Werkelijke ribbanen](lobe-review-original.png)
![Eerste veerbruglaag met vorige laag grijs](support-review.png)

## Reproductie

Eigenaar: open de meegeleverde3MF; onderstaande stappen zijn alleen voor engineering.
Python: numpy,trimesh,manifold3d,scipy,shapely,matplotlib,networkx. OpenSCAD voor gewijzigde CAD.
Vanuit repositoryroot:

```sh
python owner-print-tests/2026-10-18-microstepper-frame-v2/generate.py
python owner-print-tests/2026-10-18-microstepper-frame-v2/review_geometry.py
python tools/curated-experiment-checks/E-299/printing/build_project.py \
  --bambu /pad/naar/bambu-studio --resources /pad/naar/resources \
  --scratch work/e302-revision/slice \
  --stl owner-print-tests/2026-10-18-microstepper-frame-v2/microstepper-frame-v2.stl \
  --out owner-print-tests/2026-10-18-microstepper-frame-v2/microstepper-frame-v2.3mf \
  --name 'E-302 revision 2 PCB recess and 50mm pin X1C PLA'
```

`review_lobes.py PROJECT OUT.json`, `review_support.py PROJECT OUT.json`
en `review_pins.py PROJECT OUT.json`
controleren zowel de opgeslagen als de door de bouwer heropende3MF. De scripts
gebruiken de bestaande `owner-print-tests/validate-bambu-project.py` G-codelezer.
`drawings.py` reproduceert montageafbeeldingen. `review_geometry.py` gebruikt
de meegeleverde schroef/pin-STLs en vergelijkt die met de E-301-bronnen.
`review_dimensions.py` documenteert de voorwaardelijke tandprofielcontrole;
`review_archive.py` vergelijkt alle10 meshes met de opgeslagen3MF en controleert
rapporthashes. De repo is de volledige reproductiebron.

Officiële Bambu AppImage:
<https://github.com/bambulab/BambuStudio/releases/download/v02.08.02.61/BambuStudio_ubuntu24.04-v02.08.02.61-20260820225108.AppImage>.
SHA256 `d501b103fac5424513ec0e8d6bc145fb30719de2c7d94d7320d723740c81a7fd`
gecontroleerd vóór gebruik. Ontbrekende runtimebibliotheken via ondertekende
Debian-APT-metadata lokaal uitgepakt; geen TLS/signatuurcontrole uitgeschakeld.

Repositorycheck: bestaande grootteoverschrijdingen in E-266/E-283/E-286/E-288/E-293
en beide AGENTS-bestanden; geen van die bestanden gewijzigd. Geen nieuw E-302
structuurprobleem. Tijdelijke tools blijven buiten de oplevering.

## Historie van deze correctie

Commit3d554a3 bevatte de eerste E-302-plaat zonder schroeven/pinnen en met twee
kleinere zijvensters. Na eigenaarfeedback vervangen door deze revisie met één
gezamenlijke uitsparing, complementaire helften, meer cilindersteun en volledige
schroef/pin-testonderdelen. Oude bestanden en meetclaims zijn geen actuele
printinstructies; de eerste versie blijft in Git-historie. De koppelingmaten
bleven behouden na bron- en voorwaardelijke profielcontrole; A blijft marginaal.
