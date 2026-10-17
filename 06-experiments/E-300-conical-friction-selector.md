---
status: complete
builds-on: [E-299, E-298, E-295]
---

# E-300 — conische wrijving en hogere selectoren, één tweepinsproef

**Eigenaarsopdracht, 17 oktober 2026.** Basis: E-299 op `main`, commit `c341244ede59ce92ab63f8edd5bcb14907a87f6c`, plus het volledige fysieke eigenaarsrapport inclusief de latere stopblok-/uitsparingsfeedback. Historische experimenten, resultaten en printprojecten blijven ongewijzigd.

## Concrete keuze

Twee pinnen op 5,08 mm, één centraal belaste gedeelde rij en twee kolommen. Gewone PLA-conussen met halve hoek 45° en contactring straal 1,40–1,90 mm vervangen de tanden. Eerst sluiten met stilstaande inputs, pas daarna draaien. Geen fasezoeken, veren, coating of mechanisme per pin. De schroef, pin en complete E-299-schroefprintsteun blijven bytegelijk. Splitframe, diepe sleutelbus en grote kolomhouders blijven; de vaste rijhouder vervalt omdat een vaste afstand geen betrouwbare conusdruk instelt.

Hogere vangbladen (2,40/4,40 mm), een 8,00-mm profiel, doorlopende smalle rug en uitlopende U-vrijloop versterken de gemelde zwakke uitsparing. De echte meshdoorsnede geeft circa **2,03× verticaal buigtraagheidsmoment** tegenover E-299; zijdelingse stijfheid neemt juist af. Een smallere actieve doorsnede voorkomt nominale botsing met rasterburen. Het hogere profiel vraagt langere rotorhalzen en aangepaste framevrijloop. Dit zijn getoetste CAD-keuzes, geen gemeten fysieke sterkte.

De rij kan beperkt kantelen om twee contacthoogten op te nemen. De proef heeft centrale handdruk, geen automatische voorspanning. De nominale handslag tot eerste belast contact is circa **3,52 mm**, inclusief vang-/houderspeling. Een concrete 0,10-mm verschilpose is geometrisch gecontroleerd. Meer dan twee willekeurige contacthoogten op een lange stijve rij worden hiermee niet opgelost.

## Haalbaarheid en fysieke vraag

De conus kent geometrisch geen tandfase. Wel remt de onder druk draaiende rotorflens tegen haar stilstaande selector. Het model `T_schroef ≈ F_cel(2,3513 μ_conus − 1,85 μ_thrust) Nmm` laat zien dat deze remwrijving veel grip kan verbruiken. Bij aangenomen gelijke μ=0,25 en 0,10 Nmm benodigd schroefkoppel zou ongeveer **1,60 N totale rijdruk** nodig zijn voor twee pinnen. μ, schroefkoppel, echte lastverdeling en slipkoppel zijn ongemeten. Bij ongunstige wrijvingsverhouding helpt meer druk niet. De vlotte eigenaarservaring maakt één kleine fysieke proef zinvol, maar bewijst geen lage aandrukkracht.

De print moet sluiten vanuit verschillende stilstaande hoeken, beide pinnen bij dezelfde druk aandrijven, herkenbaar kunnen slippen en via rij én kolom betrouwbaar lossen. Ook steunverwijdering, volledige slag, lokale buiging, zijdelings wrikken en buurisolatie worden vastgelegd. Geen langdurige of zware belasting; stop bij klemmen, schade, buigen of frameopening.

## Oplevering en bewijsniveau

- [Eén gedateerde test met geconfigureerd X1 Carbon/0,4-mm/PLA-project](../owner-print-tests/2026-10-17-cone-friction-selector/test.md), vaste oriëntatie, supports en slicerpaden gecontroleerd; slicerraming **3 u 47 min 48 s / 10,48 g PLA**, geen nieuwe fysieke resultaten.
- [Ontwerp en kracht-/tolerantieargumentatie](../tools/curated-experiment-checks/E-300/design-report.md), [reproduceerbare CAD](../tools/curated-experiment-checks/E-300/cad/generate.py) en [CAD-maatvoering](../tools/curated-experiment-checks/E-300/cad/cad-guide.md).
- [Onafhankelijke mechanische beoordeling](../tools/curated-experiment-checks/E-300/review/mechanical-review.md), inclusief belaste sluiting, ontkoppelslagen, rotatie, concrete shimpose en actieve rasterkernen. Externe proefgrepen en paddle zijn geen uitgewerkte routering voor een volledig display.
- [Opgeslagen instellingen en slicerbewijs](../owner-print-tests/2026-10-17-cone-friction-selector/bambu-settings.md), [korte montage/test-PDF](../owner-print-tests/2026-10-17-cone-friction-selector/montage-en-test.pdf) en [leeg resultatenformulier](../owner-print-tests/2026-10-17-cone-friction-selector/resultaten.md).

**Stopconditie:** één zinvolle fysieke proef opgeleverd; geen aankopen, extra prints, automatische vervolgtaak of nieuwe fysieke claim. Passing, benodigde kracht, grip/slip, werkelijke gelijktijdige drukverdeling en ontkoppeling blijven onbekend tot de eigenaar die test.
