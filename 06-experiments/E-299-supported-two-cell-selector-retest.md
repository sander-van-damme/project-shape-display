---
status: complete
builds-on: [E-298, E-297, E-295]
---

# E-299 — ondersteunde schroeven en stevige selectie in een 1×2-proef

**Eigenaarsopdracht, 17 oktober 2026.** Verwerkt de volledige fysieke E-298-feedback inclusief de aanvullende montage-/modulevoorstellen, opgehaald met `git pull` op commit `46a4117`. Bestaande experimenten, resultaten en printprojecten zijn ongewijzigd.

## Concrete oplevering

Eén [gedateerde fysieke test](../owner-print-tests/2026-10-17-two-cell-supported-selector/test.md) met een [geconfigureerde X1 Carbon/0,4-mm/PLA-3MF](../owner-print-tests/2026-10-17-two-cell-supported-selector/two-cell-selector.3mf). Eén gedeelde rij, twee afzonderlijke kolommen, twee echte E-295-schroefpinnen op 5,08-mm raster. Achttien printobjecten worden negentien mechanische onderdelen nadat twee schroeven van hun gezamenlijke printsteun zijn losgemaakt. Slicer: **3 u 33 min 55 s / 9,37 g PLA**, geen fysieke raming uit een werkelijk uitgevoerde print.

Brede afgeschuinde honden, stijvere 1,60-mm selectorbladen en 3,00-mm slag vervangen de kwetsbare punt en krappe sluiting. Nominaal 1,36-mm rechte flankoverlap en 0,56-mm tip/bodemvrijloop; de volledige tolerantiestapel is niet fysiek gekwalificeerd. Drie grote eindstandhouders vervangen de acht miniblokjes. Een tweedelig inlegframe en 3,2-mm diepe inputsockets vereenvoudigen montage/bediening. De schroeven hebben brede voeten en twintig kleine steunverbindingen op berekende draadkruinen en kragen; verwijderbaarheid en draadschade moeten fysiek worden beoordeeld.

**Bewust compromis:** begrensd langzaam inputfasezoeken onder lichte selectiedruk is onderdeel van de bediening. Statische identieke punten kunnen exacte symmetrie niet gegarandeerd doorbreken. Dit is daarom geen claim van passieve zelfuitlijning met stilstaande inputs of reeds bewezen invang vanuit iedere fase. De test vergelijkt beide handelingen afzonderlijk. Een centrale vaste staaf en uitgebreid modulair docking zijn onderzocht en uitgesteld wegens te dunne DD-wanden en extra toleranties; het kleine inlegframe levert nu een concrete montageverbetering.

## Controle en bewijsgrens

- [Ontwerpkeuzes en compromissen](../tools/curated-experiment-checks/E-299/design-report.md), [parametrische CAD](../tools/curated-experiment-checks/E-299/cad/generate.py), [onderdelen en maatvoering](../tools/curated-experiment-checks/E-299/cad/parameters.json).
- [Onafhankelijke geometriecontrole](../tools/curated-experiment-checks/E-299/review/mechanical-review.md): 7.180 booleans, 173 poses, nul onverwachte botsingen; geen paren uitgesloten. Acht maskers, slagen, tweerichtingsaandrijving, montagepad en voorgeschreven fasezoekroute; tevens continue selector/frame-enveloppen.
- [Opgeslagen Bambu-instellingen en heropen/slice-controle](../owner-print-tests/2026-10-17-two-cell-supported-selector/bambu-settings.md): Bambu Studio 02.08.02.61, twee succesvolle slices, instellingen behouden. Werkelijke extrusiepaden, open boringen, rotorhalzen, tanden, bedcontact en alle twintig steunverbindingen onderzocht. Framebruggen en dunne draadwanden blijven expliciete fysieke inspectiepunten.
- [Montage/testinstructies](../owner-print-tests/2026-10-17-two-cell-supported-selector/test.md), [resultatenformulier](../owner-print-tests/2026-10-17-two-cell-supported-selector/resultaten.md).
- [Historische integriteit](../tools/curated-experiment-checks/E-299/review/history-integrity.json): alle 1.257 bestaande tracked bestanden SHA-256 gelijk aan de opgehaalde broncommit.

**Resultaat:** een nieuwe afgebakende, gecontroleerde fysieke testprint is klaar; geen nieuwe fysieke uitslagen. Werkelijke passing, invang, stijfheid, steunverwijdering, buurisolatie en montagegemak zijn nog onbekend. Geen motorbelasting, volledige matrixkwalificatie, arraybetrouwbaarheid, levensduur, aankopen, nieuwe issues of automatische vervolgexperimenten. Stop bij deze oplevering.
