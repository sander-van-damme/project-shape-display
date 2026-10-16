---
status: complete
builds-on: [E-297, E-295]
---

# E-298 — zelfuitlijnende puntkoppeling binnen de tweedelige matrix

**Eigenaarsopdracht, 16 oktober 2026.** Nieuwe puntgeometrie op de twee afzonderlijk axiaal bewegende helften van E-297. Rij omhoog, kolom omlaag; geen veren, extra selectoren of gewijzigde aandrijfarchitectuur. E-297 en alle bestaande printtests blijven volledig ongewijzigd. De compacte E-295-draad met 0,175-mm relief is exact behouden.

Iedere identieke rotorhelft heeft twee tegenoverliggende punten en twee open complementaire holtes. De punten lopen zowel radiaal als omtreksgewijs toe; brede wortelflanken dragen na volledige zetting koppel in beide richtingen. Drie varianten vergelijken 0,48- en 0,60-mm punthelling en een 12° verschoven apex. Test A bevat twee identieke paren per variant. Test B gebruikt de kortere helling met meer rechte flankoverlap, in de bestaande 5,08-mm 2×2-matrix.

## Concrete uitkomst

Het principe is kansrijk als beperkte fysieke proef, maar **zelfuitlijning vanuit iedere beginfase is niet aangetoond**. De ideale én daadwerkelijke meshcontactberekening vinden een punt-op-puntplateau. Asymmetrie verschuift die dode fase; zij verwijdert haar niet. Eén geblokkeerd paar kan nog steeds de hele stijve rij-/kolomselector tegenhouden. De outputschroeven mogen onafhankelijk draaien: daarmee is verschillende beginfase op zichzelf geen geometrische onmogelijkheid, zolang ieder contact werkelijk kan afglijden.

De oorspronkelijke CAD-kroon van 0,16 mm verdween in de echte slicerpaden. De definitieve 0,30-mm CAD-kroon is een printbaarheidscompromis; ook daar wordt de bovenkant deels afgekapt en aanzienlijk breder afgezet. **Een minuscule CAD-punt is geen bewezen even scherpe X1C-print.** De uiteindelijke extrusiepaden, inclusief de negatieve eerdere slice, staan in het printbaarheidsverslag. De fysieke puntsterkte, wrijving en schade blijven onbekend.

De nieuwe hellingen kosten rechte flank: nominale overlap **0,48 mm** voor A, **0,24 mm** voor B/C. Het oude ±0,72-mm E-297-ontwerpbudget garandeert die nieuwe overlap niet. De nominale enkel-selectievrijloop blijft 0,96 mm. Alle zestien nominale selectorstanden passen in de daadwerkelijke 2×2-meshcontrole; dat bewijst geen continu tolerantie- of fysiek werkingsvenster. Een afzonderlijk voorgeschreven pad met vier verschillende outputfases is bovendien in achttien complete matrixposities botsingsvrij; de bijbehorende rotatie is voorgeschreven, niet door een krachtsimulatie voorspeld.

## Oplevering

- [Test A — 18 delen, drie vormen en identieke herhalingen](../owner-print-tests/2026-10-16-self-aligning-point-fit/test.md), [X1C-project](../owner-print-tests/2026-10-16-self-aligning-point-fit/point-fit.3mf).
- [Test B — 37 delen, geïntegreerde 2×2](../owner-print-tests/2026-10-16-self-aligning-point-matrix/test.md), [X1C-project](../owner-print-tests/2026-10-16-self-aligning-point-matrix/point-matrix.3mf). **DEFERRED** tot kansrijke fysieke A-uitkomst; bestand vooraf concreet voorbereid.
- [Technisch verslag](../tools/curated-experiment-checks/E-298/design-report.md), [contactberekening](../tools/curated-experiment-checks/E-298/contact-analysis.md), [onafhankelijke review](../tools/curated-experiment-checks/E-298/review.md).
- [Parametrische CAD, maatvoering en montage](../tools/curated-experiment-checks/E-298/cad/cad-guide.md), [generator](../tools/curated-experiment-checks/E-298/cad/generate.py), [printbaarheid en echte slicercontrole](../tools/curated-experiment-checks/E-298/printability.md).
- [Printbare instructies en resultaatformulieren](../tools/curated-experiment-checks/E-298/print-and-assembly.pdf), [pakketcontrole](../tools/curated-experiment-checks/E-298/validation/delivery-integrity.json).

De hoofdproef houdt alle vier inputs stil met een verwijderbare reactiehulp en sluit meerdere koppelingen met verschillende outputfases via dezelfde staven. Handmatig fasezoeken telt niet als zelfuitlijning. De toegestane pinverplaatsing wordt vóór/na selecteren geregistreerd: bij 3-mm lead is 30° schroefrotatie 0,25 mm. Daarna worden volledige zetting, beide koppeldraairichtingen, beide terugtrekroutes en niet-geselecteerde buren afzonderlijk gecontroleerd.

**Bewijsniveau:** analyse, CAD en werkelijke slicerpaden; geen fysieke puntkoppelingsuitslagen. De positieve E-295-handpassing kwalificeert alleen die eerdere draadproef. Stop bij deze nieuwe ontwerpen en twee afgebakende printtests: geen nieuwe issues, merge of automatische vervolgcampagne.
