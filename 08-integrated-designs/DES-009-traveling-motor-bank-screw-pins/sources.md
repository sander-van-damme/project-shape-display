# Bestanden en herkomst

[Terug naar DES-009](DES-009-traveling-motor-bank-screw-pins.md).

Bronstand **18 oktober 2026**, repositorybasis `84d265134fcb74266776f9f5d2cb7e0dea60a8ef` (actuele `origin/main` bij aanvang van consolidatie). De oudere lokale checkout `505bb91` is eerst bijgewerkt: de lange schroef en E-302-software in de drie nieuwere commits behoren dus tot dit overzicht.

## Dossierindeling en beheer

| Bestand/map | Herkomst / doel |
|---|---|
| [Hoofddocument](DES-009-traveling-motor-bank-screw-pins.md) | Nieuwe eigenaarsbeslissing en geconsolideerde architectuur; enige ID-dragende DES-009-tekst |
| [components.md](components.md) | Componenten, bronklassen, actuele Amazonextractie en motorvergelijking |
| [electronics.md](electronics.md) | Officiële documentatie, registerkaart, fysieke versus voorgestelde testconfiguratie |
| [experiments.md](experiments.md) | Concrete resultaten en directe oorspronkelijke CAD-/montage-/beeld-/3MF-links |
| [open-questions.md](open-questions.md) | Open ontwerpvragen; geen geactiveerde takenlijst |
| [sources.md](sources.md) | Dit herkomstoverzicht |
| [verification.md](verification.md) | Controleverslag voor links, bestanden, bewijsstatus en oorspronkelijke bytes |
| [historical/manifest.json](historical/manifest.json) | Per hersteld bestand: volledige commit, oorspronkelijk pad, Git-blob-ID, SHA-256 en bytes |
| `historical/trial-0/` | Drie oorspronkelijke motorreferenties; behouden submap `img/` houdt de originele afbeeldingslink werkend |
| `historical/trial-5/` | Eén oorspronkelijke compacte actuatorbron als genealogie, niet uitvoerbaar printpakket |

Actuele documenten worden gelinkt op hun oorspronkelijke locatie. Geen kopieën van actuele firmware, CAD, 3MF of proefresultaten; geen nieuwe binaries gegenereerd. Alleen de historische maatfoto is ook in E-301 aanwezig: de extra exacte kopie is nodig om het **ongewijzigde** herstelde `components.md` zelfstandig met zijn originele relatieve afbeelding te kunnen lezen.

## Herstel uit Git

Alle onderstaande bestanden zijn via `git show COMMIT:PATH` byte-exact teruggezet en tegen dezelfde Git-blob gecontroleerd. De oorspronkelijke documenten blijven ongewijzigd, inclusief onjuiste/oude claims. **Lees de actuele duiding in [componenten](components.md) en [elektronica](electronics.md) vóór gebruik.**

| Hersteld bestand | Oorspronkelijke locatie | Commit |
|---|---|---|
| [historical/trial-0/components.md](historical/trial-0/components.md) | `trial-0-pneumatic-multiplexer/docs/components.md` | `2d21eef7fdefdae75569a6eba02b95a143cacb6d` |
| [historical/trial-0/img/stepper-motor-dimensions.jpg](historical/trial-0/img/stepper-motor-dimensions.jpg) | `trial-0-pneumatic-multiplexer/docs/img/stepper-motor-dimensions.jpg` | `2d21eef7fdefdae75569a6eba02b95a143cacb6d` |
| [historical/trial-0/micro-stepper-datasheet.pdf](historical/trial-0/micro-stepper-datasheet.pdf) | `trial-0-pneumatic-multiplexer/docs/micro-stepper-datasheet.pdf` | `2d21eef7fdefdae75569a6eba02b95a143cacb6d` |
| [historical/trial-5/actuator.scad](historical/trial-5/actuator.scad) | `trial-5-grid-and-cubes-and-rod/actuator.scad` | `41484f96999847c139b9010e73009d73e9459c89` |

Het oude components-document bevat een dubbele B−-kleurtoewijzing, oude prijzen en verkoperclaims over de driver. Die zijn **geen actuele bedradingsinstructie, offerte of officiële IC-specificatie**. De PM08-PDF is een leveranciersdocument (Version 1.0) waarvan huis/as overeenkomen met de nieuwe eigenaarmetingen; zij bevestigt onze motoridentiteit niet. De Trial 5-bron heeft oude 30°-draad en `$slop=0.65` plus externe, niet vastgepinde BOSL2-includes. Zij is bewaard als referentie, niet gebouwd of geëxporteerd.

De maatfoto uit de gevraagde commit, de huidige [E-301-maatfoto](../../owner-print-tests/2026-10-17-microstepper-screw-pin/motor-dimensions-original.jpg) en Amazonafbeelding 4 hebben dezelfde SHA-256: `91b1daabccbcece63d11bcb0b190c2f7bcf23977b242e339027d56f075e935bd`. Dit bevestigt de herkomst van een catalogusbeeld, niet de fysieke afmetingen van de voorraad.

## Actuele originelen: centrale leesingangen

| Bronfamilie | Canonieke ingang / wat hieruit is overgenomen |
|---|---|
| E-295 | [Experiment](../../06-experiments/E-295-compact-screw-drive-development.md), [compacte geometrie](../../tools/curated-experiment-checks/E-295/research/compact-geometry.md), [latere fysieke passing](../../owner-print-tests/2026-10-15-compact-screw-fit/test.md): 4,4/5,08-mm basis, draad en relief, vijf handcycli |
| E-297 en verwante alternatieven | [Experiment](../../06-experiments/E-297-two-half-row-column-clutch-print-tests.md); alle zes selector-/koppelingspakketten staan in de [experimentenkaart](experiments.md). Ontwerpstatus en gedeeltelijke negatieve E-298-observaties blijven gescheiden |
| E-301 | [Experiment](../../06-experiments/E-301-pico-w-motorcontroller.md), [leidend fysiek verslag](../../owner-print-tests/2026-10-17-microstepper-screw-pin/pico/resultaten.md), [motorbronketen](../../owner-print-tests/2026-10-17-microstepper-screw-pin/sources.md): huidige elektrische proef en motorpinbewijs |
| E-302 | [Experiment](../../06-experiments/E-302-improved-microstepper-test-frame.md), [mechanische bronnen](../../owner-print-tests/2026-10-18-microstepper-frame-v2/sources.md), [softwarehandleiding](../../owner-print-tests/2026-10-18-microstepper-frame-v2/software/handleiding.md): laatste CAD-/print-/softwarestand zonder nieuwe fysieke claim |
| Missie en prioriteiten | [Missie](../../01-project-description/shape-display-mission.md), [prioriteiten](../../02-design-criteria/current-prototype-priorities.md): D&D, eenvoudige mechanica, zuinig leren; DES-009 vult hun eerdere open architectuurkeuze in |
| Historische DES | [DES-007](../DES-007-radial-pinch-belt-row-head/DES-007-radial-pinch-belt-row-head.md), [DES-008](../DES-008-positive-latch-shared-lift/DES-008-positive-latch-shared-lift.md): behouden vergelijkingen, geen actieve bankarchitectuur |

Alle relevante eigenaarpakketten van **15 t/m 18 oktober** zijn in [experiments.md](experiments.md) geïndexeerd, inclusief printprojecten en montagebeelden. Lege resultatenformulieren blijven leeg; aanwezige CAD-/slicerbeelden worden niet als proefopnamen aangeduid.

## Externe bronnen en rechten

| Bron | Klasse / versie / behandeling |
|---|---|
| [Abovehill B08346RFVZ](https://www.amazon.com/Abovehill-Stepper-2-Phase-4-Wire-Connection/dp/B08346RFVZ) | Verkoper, live gelezen 18 oktober 2026; geen versie of OEM-identificatie. Volledige relevante extractie en vier geïnspecteerde productafbeeldingslinks in [components.md](components.md) |
| [TMC2208/2 & TMC2224 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf) | Officiële TRINAMIC/ADI bron, rev.1.13, 25 mei 2022; rechtstreeks opgehaald/gecontroleerd. Specs, pagina's en registers in [electronics.md](electronics.md) |
| Raspberry Pi Pico W datasheet/pinout | Officiële fabrikantlinks in [electronics.md](electronics.md); HTTP403 bij deze broncontrole, revisie niet opnieuw vastgesteld. Geen ongelezen versie verzonnen |
| MicroPython, TI TPS3808 en FYSETC-modulehandleiding | Softwareproject-, fabrikant- en modulevergelijkingsbronnen; doel en revisiebeperkingen in [electronics.md](electronics.md) |
| Historische PM08-PDF | Reeds bestaand repositoryreferentiebestand exact hersteld op eigenaarsverzoek. Beste technische referentie voor huis/as; geen bevestigde OEM-datasheet van de gebruikte motor |

Geen expliciete herdistributietoestemming gevonden voor nieuw verzamelde externe PDFs of verkoopbeelden. Daarom stabiele bronlinks met vastgestelde versie waar beschikbaar; tijdelijke downloads zijn alleen gebruikt voor broncontrole en staan niet in dit dossier. De herstelde historische binaries zijn ongewijzigd; hun aanwezigheid is geen nieuwe licentieclaim.

## Zoekbereik en bewuste uitsluitingen

Gericht gezocht met `git log --all`, `git ls-tree`, `git show` en pad-/inhoudszoekopdrachten in huidige bestanden en geschiedenis. Onderzocht: trial-0, trial-5, de vroegere `img/`, `images/`, `docs/PM08-2-8mm-Micro-Stepper-Motor-datasheet.pdf` en latere `tests/`, `experiments/`, `06-experiments/test00...` en `06-experiments/legacy/test00...`-verhuizingen. De volledige repositorygeschiedenis is beschikbaar; dit was geen nieuwe brede architectuurstudie.

`trial-0-pneumatic-multiplexer/docs/multiplexing-layout.ods` en `shape-display-dev.odt` zijn inhoudelijk uit Git gescreend. Ze bevatten oude multiplex-/pneumatische planning en brede architectuurdoelen, geen aanvullende actuele motorspecificaties of motorbankbewijs. Samen met de oude Pythonbesturing en requirements bewust niet hersteld. Ze blijven bereikbaar in commit `2d21eef7fdefdae75569a6eba02b95a143cacb6d`. Er is geen volledig oud ontwerp teruggezet.

**Niet gevonden/bevestigd:** een sluitende OEM-datasheet voor de werkelijke circa Ø8 × 9,2-mm motor, afzonderlijke in de repository opgeslagen eigenaarsfoto's van beide gebruikte varianten, connectorfamilie/steek/pinout, eigen windingweerstandsmetingen en nauwkeurige toleranties van beide motoren. Dit zijn informatiehiaten; alle hierboven geselecteerde historische bestanden konden uit Git worden hersteld. Catalogusfoto's mogen deze hiaten niet als eigen meetgegevens invullen.

**Maatupdate 20 oktober:** [eigenaarmetingen K/L, A–D](motor-variants-limits.md#1a-eigen-motorpaar--benaderende-eigenaarmetingen-20-oktober-2026) zijn de actuele mechanische basis; oudere Amazon-maten zijn geen maatwaarheid.
