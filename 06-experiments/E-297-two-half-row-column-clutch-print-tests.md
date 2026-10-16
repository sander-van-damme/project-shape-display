---
status: complete
builds-on: [E-295]
---

# E-297 — tweedelige rij-/kolomkoppeling met fysieke printproeven

**Eigenaarsopdracht, 16 oktober 2026.** Twee afzonderlijke axiaal bewegende koppelingshelften vormen één bidirectionele frontklauwkoppeling: rij omhoog, kolom omlaag. Hun gedeelde niet-roterende meenemers vangen elk een integrale flens tussen twee open kambladen en trekken ook actief terug. De architectuur blijft de oorspronkelijke gebruikersopdracht; E-296 is alleen als technische foutbron gelezen.

De 2×2-opstelling behoudt **5,08 mm pitch**, **4,4-mm pinnen** en de fysiek soepel bevonden E-295-draad met **0,175 mm radiale relief**. Twee brede klauwen per helft, een verschuifbaar double-D-profiel, afzonderlijke axiale schroefsteun en vaste geleidingen vormen de volledige krachtroute. Het pakket bevat echte printplaten en geconfigureerde Bambu-projecten; de uiteindelijke vrijgavestatus en controles staan in de afzonderlijke tests.

- [Test A — koppelingspassing, meenemers en twee identieke nominale sets](../owner-print-tests/2026-10-16-two-half-clutch-fit/test.md).
- [Test B — werkelijke 2×2-selectie en beweging in beide richtingen](../owner-print-tests/2026-10-16-two-half-clutch-matrix/test.md).
- [Printbare montagehandleiding en resultaatformulieren](../tools/curated-experiment-checks/E-297/print-and-assembly.pdf).
- [Technisch verslag](../tools/curated-experiment-checks/E-297/design-report.md), [tandkeuze en maatvoering](../tools/curated-experiment-checks/E-297/tooth-design.md).
- [Reproduceerbare CAD](../tools/curated-experiment-checks/E-297/cad/generate.py), [exacte overname van E-295-draad](../tools/curated-experiment-checks/E-297/validation/e295-source.json), [onafhankelijke geometriecontrole](../tools/curated-experiment-checks/E-297/independent-geometry.json).

**Aandrijving van de proef:** één afneembare handgreep draait beurtelings de vier inputassen **onder** de echte rij-/kolomkoppelingen. Iedere niet-geselecteerde input wordt eveneens gedraaid om de isolatie daadwerkelijk te toetsen. Dit is geen directe handaandrijving van vier schroeven als vervanging voor selectie, en geen kwalificatie van een gemeenschappelijke rotatiebus.

**Bewijsgrens:** berekening, CAD, echte slicerpaden en onafhankelijke ontwerpcontrole zijn geen fysieke werking. De eigenaar heeft deze nieuwe koppeling nog niet geprint of getest. Fasezoeken, wrijving, printspreiding, sterkte, axiale speling en buurisolatie blijven de expliciete testvragen. Geen nieuwe vervolgissues of automatische onderzoekscampagne.

**Oplevering:** Test A READY/P1 (20 delen, 44 min 08 s, 1,94 g); Test B READY/P2 na nominale passing in A (36 delen, 4 uur 29 min 43 s, 17,85 g). Dit zijn Bambu-ramingen. De onafhankelijke meshcontrole vond geen onverwachte botsing in 1.071 bemonsterde standen, inclusief 12 montagepaden. Werkelijke gecombineerde as-/rotorkanteling, laagsterkte en passing blijven fysiek te toetsen.
