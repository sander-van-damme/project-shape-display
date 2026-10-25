---
status: complete
builds-on: [E-295, E-296, E-297, E-298, E-299, E-300, E-302, E-303]
---

# E-305 — Permanent-magnet and reversible-electromagnet clutch

**Owner-commissioned investigation,25 October 2026.** Baseline1071f695b93951246a2865038e7fb9de9bdf2a05. DES-009 remains active and unchanged. Research, finite-geometry calculations, dimensioned concept CAD and one verified printable force fixture;**no new physical measurements**.

Numbering corrected to **E-305** after pulling `main` at `e130fcc02d31135fbf9022f84266a1d25e6fd000`. The existing [E-304 guided row/column study](E-304-guided-full-length-row-column-clutch.md) and its assets are preserved. This correction updates identifiers and the saved print profile; it adds no engineering result.

**Decision:** test one stationary140-turn air-core winding with a purchased axialØ3×2-mm N48 magnet. A single sliding conical carrier is the clearest static all-angle clutch concept. A straight-dog carrier remains a credible lower-holding-power alternative with conditional dynamic seating. Neither warrants adopting6,400 clutches.

## Deliverables

- [Concise decision report](../tools/curated-experiment-checks/E-305/decision.md): all owner questions and focused comparison with E-303, row/column couplings and DES-009.
- [Materials,stock prices and remagnetization](../tools/curated-experiment-checks/E-305/materials.md): NdFeB, ferrite, AlNiCo, SmCo and measured steel hysteresis; initial magnetization versus maintenance/reversal.
- [Engagement geometry and complete load paths](../tools/curated-experiment-checks/E-305/engagement.md): full angular-domain analysis, positive/friction/hybrid candidates, torque/release/obstruction and counted support.
- [Actuator,electronics and array accounting](../tools/curated-experiment-checks/E-305/actuator-and-array.md): force-position curves, core limitations, neighbors, addressing, power and component costs.
- [Reproducible calculations](../tools/curated-experiment-checks/E-305/analysis/model.py),[generated data](../tools/curated-experiment-checks/E-305/analysis/results/winding.json),[dimensioned section](../tools/curated-experiment-checks/E-305/images/concept-section.svg),[exploded assembly](../tools/curated-experiment-checks/E-305/images/concept-exploded.svg),[flux diagram](../tools/curated-experiment-checks/E-305/images/flux.svg),[parametric concept CAD](../tools/curated-experiment-checks/E-305/cad/concept.scad).
- [One illustrated force test](../owner-print-tests/2026-10-25-reversible-magnet-force/test.md): actual STLs, parametric CAD, genuine configured X1C Bambu3MF, low-voltage wiring, purchased-parts list and blank results. **6 parts /3.63 g /about 50 min.**
- [Provenance and verification](../tools/curated-experiment-checks/E-305/verification.md).

## Decision-changing findings

1. Finite air-coil/magnet calculation gives~30 mN at 0.3 A and~50 mN at 0.5 A across the proposed0.6-mm stroke. Axial magnet rotation preserves the ideal field geometry; current reversal changes force sign on this side of the coil center. A steel core can instead stay attractive at both polarities.
2. Ordinary steel can retain magnetization and some quenched steels can be rewritten at actuator-scale fields. Short open geometry and repeated reversal undermine treating it as a stable miniature permanent magnet. NdFeB/ferrite initial magnetizing fields are far beyond this winding; no magnetizing machine is proposed.
3. The continuous35° cone has no angular indexing barrier. At assumedμ0.25, the enlarged concept gives~0.0756 Nmm at 0.5 A/0.674 W;E-303 light/moderate provisional starting scenarios are0.0597/0.343 Nmm. **Actual screw torque remains unmeasured.** A seated straight-dog version could require much lower holding current but needs seating/release/overload evidence.
4. The explicit concept counts15 mechanical pieces/allocations including pin/screw/support/coil/retention, plus electronics. It needs continuous ON current and has no guaranteed loaded power-loss release. Independent screw support is preserved.
5. 14×14-mm housing/Ø13-mm gear/Ø10-mm cone do not fit5.08-mm pitch. Staggering alone leaves through-shaft collisions. Finite neighbor calculation gives~43.5 mN axial interaction for parallel3×2-mm magnets at 5.08-mm pitch with 0.6-mm vertical offset—comparable to actuation force.
6. Repeated component/electronics estimate~€7.4k–14.9k for 6,400, before shared infrastructure/labor. Full0.5-A activation is~4.3 kW copper alone. No complete-array cost or thermal advantage over E-303 is established.

**Continuation observation:** repeatable≥45 mN upward across the stroke at≤0.5 A, useful reverse force, ≤2 mN isolated OFF parasitic force, and acceptable pulse temperature. This would justify an owner decision about a cone torque test, not prove continuous duty or dense compatibility. The prepared test stops at force measurement; no elaborate clutch print precedes it.

The saved3MF was reopened in actual Bambu Studio 02.08.02.61 with a fresh data directory and resliced. Both archives passed actual path/bores/thin-wall checks. Ten numerical model checks passed. Repository check retains six pre-existing size findings; previous evidence files are unchanged.

**Stop condition reached:** one numbered investigation and one prepared physical validation. No purchases, issues, schedules, additional experiments or autonomous follow-up. Await explicit owner decision; DES-009 remains primary.
