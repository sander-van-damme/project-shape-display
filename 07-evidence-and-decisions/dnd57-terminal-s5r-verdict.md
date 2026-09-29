# DND-57 — CEO terminal S5-R verdict: SUCCESS (trigger 1) — board handoff

- **DECISION (rev 6, 2026-09-29 03:0x): SUCCESS — trigger 1 fired.** S5-R is a **buildable
  shape display**, and the repository now contains a **complete, coherent, slicer-ready
  fabrication package** the board can physically print. Every mission requirement is met on its
  labelled evidence class (CAD / CALCULATION / sourced), and the only remaining uncertainty is the
  **measurement-only residue** that the board's own first print retires by design
  ([DND-27](/DND/issues/DND-27)). This is the **first permitted board contact**
  ([DND-32](/DND/issues/DND-32)); the handoff approval is linked on this issue.
- **Handoff package (on `main`):** `08-current-design/` — one coherent S5-R definition + the
  `fabrication/` printable part set. Commits: fabrication package `b1d6659` (DND-61), README
  reconcile `9130730` (DND-64).
- **Owner:** CEO. **Issue:** [DND-57](/DND/issues/DND-57), for [DND-54](/DND/issues/DND-54) and
  the mission goal.
- **Decision history:** rev 1–2 NEXT AVENUE (DND-58) · rev 3 (DND-60) · rev 4 (DND-61) · rev 5
  (DND-64) · **rev 6 SUCCESS**.
- **Decision (rev 4, 2026-09-29 01:2x):** **NEXT NAMED AVENUE — [DND-61](/DND/issues/DND-61)** — the
  **last** one before a SUCCESS handoff. After [DND-60](/DND/issues/DND-60) closed, the S5-R
  machine is a **complete, coherent printable package** (14 parts / 25,661 pieces, manifests,
  printability PASS, CI coherence gate), and the only unretired uncertainty is **measurement-only**
  (the board's own build/measure). **But** the package is **not yet slicer-ready**: two structural
  tiles (`cell_cartridge`, `platen_module`) are **reduced witness blocks**, not the true full-tile
  geometry, so the board cannot directly slice and print the real structural parts. Completing the
  full-tile geometry is bounded agent-reachable CAD work. When DND-61 closes and every part is a
  true printable part (or a documented sub-tile set), the honest call becomes **SUCCESS -> board
  handoff (trigger 1)**. **No board contact yet** ([DND-32](/DND/issues/DND-32)).
- **Decision (rev 3, 2026-09-29 01:1x):** **NEXT NAMED AVENUE — [DND-60](/DND/issues/DND-60).**
  After [DND-59](/DND/issues/DND-59) closed, every **analysis** residual on S5-R is retired or
  bounded agent-side, and the only residue left is **measurement-only** (un-retirable under
  [DND-27](/DND/issues/DND-27)). But `08-current-design/` is still a **definition**, not a
  **printable package** — there is no complete STL set or assembly/print manifest for the full
  machine. Producing that package is agent-reachable CAD work and is the last avenue between the
  machine definition and the board's SUCCESS trigger. **No board contact**
  ([DND-32](/DND/issues/DND-32)).
- **Decision (rev 2, 2026-09-29 01:0x):** **NEXT NAMED AVENUE — still.** After
  [DND-58](/DND/issues/DND-58) closed (rack 1.00 mm pitch + sourced steel rod folded in;
  **$404.60 delivered**, 24.62 s), S5-R is **still not print-ready** and the program is **still
  not an exhausted dead end**. The remaining residuals split cleanly into **agent-reachable**
  (now owned by [DND-59](/DND/issues/DND-59)) and **measurement-only** (un-retirable under
  [DND-27](/DND/issues/DND-27)). **No board contact** ([DND-32](/DND/issues/DND-32)).
- **Decision (rev 1):** **NEXT NAMED AVENUE** — the [DND-58](/DND/issues/DND-58) reconcile.
- **Owner:** CEO. **Issue:** [DND-57](/DND/issues/DND-57), for [DND-54](/DND/issues/DND-54) and
  the mission goal.
- **Triggered by:** `issue_blockers_resolved` — the two remaining residuals
  [DND-55](/DND/issues/DND-55) (Fabricator) and [DND-56](/DND/issues/DND-56) (CostManufacturing)
  both reached `done`.
- **Evidence class:** this is a **decision record over** CAD / CALCULATION / sourced work
  produced by DND-54/55/56. No print, no purchase, no measurement
  ([DND-27](/DND/issues/DND-27)).

## 1. The question

After [DND-55](/DND/issues/DND-55) + [DND-56](/DND/issues/DND-56) closed, is the post-K7
successor program ([DND-52](/DND/issues/DND-52) → [DND-54](/DND/issues/DND-54)) a **print-ready
machine to hand the board** (trigger 1), an **agent-reachable next avenue**, or an **exhausted
failure** (trigger 2)?

## 2. Board-trigger test against the mission requirements

| Requirement | S5-R as defined | Class | Meets? |
|---|---|---|---|
| ~400 × 400 mm | 406.4 × 406.4 mm (modular for the 256 mm X1C bed) | design + CAD | yes |
| ~5.08 mm pitch | 5.08 mm, unchanged from S5 | CAD | yes |
| ~6,400 cells | 80 × 80 = 6,400 | design | yes |
| ≥ 40 mm travel | 41 mm platen stroke (40 + 1 unload) | CAD + calc | yes |
| full-map reconfig < 30 s | **24.62 s** @ R=4 (G6) | **calc** — conditional | yes, conditionally |
| regional updates | 1 row ~3.9 s, 10 rows ~6.3 s, 80 rows ~24.7 s | calc | yes |
| purchased cost < $500 | **$401.12 delivered working** ($387.18–$421.51 band) | **sourced** — ratified | yes |
| **buildable (print-ready)** | **no** — [DND-58](/DND/issues/DND-58) open; R-DND54-1/-2/-5 measurement-gated | — | **no** |

Every headline clears on its labelled evidence class **except buildability**. The gap is not a
single killer; it is a short, named residue plus one open reconcile.

## 3. What DND-55 and DND-56 actually changed

- **DND-55 (Fabricator)** closed residual **R-DND54-4** (multi-row bar assembly): real-OpenSCAD
  R=4 bank render, **5/5 interference queries empty**, printability PASS; bar torsion closed by
  calculation — the printed placeholder bar **fails ~28×** at the mid-span gate, a **sourced
  Ø6 steel rod passes ~67×**. PR #55, 9/9 CI green.
- **DND-56 (CostManufacturing)** ratified the DND-54 BOM: **$397.53 reproduces exactly** (no
  driver double-count); one material finding — the register block's own channels were unpriced —
  gives the honest working total **$401.12 delivered** (still under $500). Folded into the ADR
  and model by [DND-54](/DND/issues/DND-54) (channels now explicit in `s5r_register.bom()`).
- DND-55 opened a **new residual (R-DND55-4)**: the corrected rack pitch (0.60 → 1.00 mm) changes
  the register's per-stroke advance and must be reconciled into the register definition;
  **DND-58** owns exactly this (rack pitch + steel drive rod). It is `in_progress`, assigned to
  the CTO, and is the concrete next avenue.

## 4. Why not SUCCESS

A SUCCESS handoff requires a **buildable** machine ready for the board to physically print.
S5-R is still:
- internally inconsistent at the register level until [DND-58](/DND/issues/DND-58) folds the
  corrected rack pitch + steel rod in;
- carrying measurement-gated residuals that cannot be retired under DND-27 — as-printed
  pawl/keeper friction μ and gate/tip sharpness (R-DND54-1, K2 class), printed-leaf creep
  (R-DND54-2, K11 class), and silent-row-error with no per-cell feedback (R-DND54-5, R1 class);
- conditional on an assumed crank speed (R-DND54-3, 720 °/s) for the 24.62 s timing.

Presenting this as print-ready would violate the evidence-discipline rule (never present
analytical work as physical validation).

## 5. Why not exhausted FAILURE

No residual is a proven, decisive killer. Every remaining quantity is reduced to a single named
physical or geometric question, and at least one — the register reconcile — is **agent-reachable
right now** with no print and no purchase. The cost basis is **ratified, not refuted**
($401.12 < $500), and the mechanism clears every analytic gate with margin. This is the opposite
of a dead end.

## 6. Disposition and next action

- **Determination: NEXT NAMED AVENUE — [DND-58](/DND/issues/DND-58)** (CTO): reconcile the 1.00 mm
  rack pitch + sourced steel drive rod into the register, re-run checks, keep CI green. On its
  close, the residual set is re-tested against the trigger.
- **DND-57** is held `in_review`/blocked-by DND-58 semantics via a first-class blocker so the CEO
  is auto-woken (`issue_blockers_resolved`) for the next terminal call. No board contact.
- **No new board-facing interaction** is created ([DND-32](/DND/issues/DND-32)).
- Engineering artifacts: this record, plus the DND-54/55/56 branches already merged to `main`.

---

## Rev 2 (2026-09-29) — re-trigger after DND-58 closed: still NEXT NAMED AVENUE

`issue_blockers_resolved` fired when [DND-58](/DND/issues/DND-58) reached `done`. Re-tested the
board trigger against the requirements with the reconciled model (verified on `main` `e0bb09d`).

### What DND-58 changed
- Rack pitch corrected to **1.00 / 0.50 mm** (printable gap); per-stroke advance `RACK_STROKE_MM = 1.00`.
- Printed 3 × 2 placeholder bar replaced by a **sourced steel rod Ø6 mm**.
- Timing **unchanged at 24.62 s** (the bank pass is angular; linear pitch does not enter it).
- BOM: +$3.48 delivered for the rod → **$404.60 delivered working** (margin $95.40).
- **R-DND55-4 closed**; **R-DND54-4 closed** for bank envelopes/pitch; R-DND55-1 irrelevant for the
  chosen steel rod.

### Board-trigger test (rev 2)

| Requirement | S5-R | Class | Meets? |
|---|---|---|---|
| ~400 × 400 mm | 406.4 × 406.4 | design/CAD | yes |
| ~5.08 mm pitch | unchanged | CAD | yes |
| ~6,400 cells | 80 × 80 | design | yes |
| ≥ 40 mm travel | 41 mm stroke | CAD/calc | yes |
| full-map < 30 s | **24.62 s** | calc (conditional on crank/settle) | yes |
| regional updates | 3.9–24.7 s | calc | yes |
| purchased < $500 | **$404.60 delivered** | sourced | yes |
| **buildable / print-ready** | agent-reachable residuals (DND-59) + measurement-only residue | — | **no** |

### Why still not SUCCESS
S5-R is internally consistent now, but three **agent-reachable** residuals remain open on the
promoted machine, and the rest are measurement-only:
- **Keeper-leaf printability RISK** — 0.45 mm = 1 extrusion line (limit 0.88 mm), *accepted* today.
- **R-DND54-6** — writer/solenoid force (N) is not published by any listing; the ≥1.2 N target is unconfirmed.
- **R-DND54-5** — missed keeper set = silent row error; no quantified reliability bound for a 99 % map.
- **R-DND54-3** — crank speed (720 °/s) and writer settle (0.05 s) are assumptions (break-even 468 °/s / 0.084 s).
- **R-DND55-1** — to be confirmed irrelevant for the sourced rod.

None of these requires a print or a purchase; each is reachable with CAD / calculation / sourced
listings. They are consolidated into **[DND-59](/DND/issues/DND-59)** (CTO).

### Why still not exhausted FAILURE
No residual is a proven, decisive killer; the cost basis is sourced and clears with $95.40 margin;
and DND-59 is a live, agent-reachable avenue. A dead end is not proven.

### Disposition (rev 2)
- **Determination: NEXT NAMED AVENUE — [DND-59](/DND/issues/DND-59)** (CTO). On its close, the CEO
  is auto-woken again for the final terminal call.
- **Measurement-only residue** (un-retirable under DND-27), to be reported in any final package:
  R-DND54-1/-2 (as-printed μ, gate/tip sharpness, leaf creep) and the R1-class per-cell error rate.
- **DND-57 re-blocked on DND-59** (first-class) for the wake path. **No board contact.**

---

## Rev 3 (2026-09-29) — after DND-59: NEXT NAMED AVENUE = the printable fabrication package

`issue_children_completed` fired when [DND-59](/DND/issues/DND-59) (the consolidated
agent-reachable residual retirement) reached `done`. Re-tested the board trigger on `main`
`eef0d44`.

### What DND-59 changed
All agent-reachable S5-R **analysis** residuals are now retired or bounded:
- **R-DND54-KEEPER closed** — keeper re-profiled 0.45 → **0.90 mm (2 lines)**, hold moved to a
  **hard compression shoulder** (144–324×), printability RISK → **PASS**. DND-59 also found a real
  hidden failure mode: the old bending-spring hold was tolerance-fragile (a 200k-sample Monte-Carlo
  over sourced print tolerance shows it can print to zero hold) — the compression shoulder removes
  that dependence.
- **R-DND54-6 closed agent-side** — writer force re-derived bottom-up (0.2425 N); sourced 5 V push
  solenoid class (1.20 N) clears 4.95×.
- **R-DND54-5 bounded** — 99 % map needs per-keeper q ≤ 1.57e-6; per-group verify+retry relaxes
  2–10×, writer redundancy ~798×.
- **R-DND54-3 bounded** — break-evens 468 °/s / 0.084 s; sourced NEMA17 class clears (2.15× torque).
- **R-DND55-1 closed** for the sourced steel rod (33× inside gate at extreme e).

**The only residue left is measurement-only** (R-DND54-1/-2, the as-printed q, the loaded NEMA17
curve) — un-retirable under DND-27.

### The remaining gap: definition vs printable package
`08-current-design/` is a **machine definition (README)**, and every CAD artifact to date is a
unit cell, bank, or coupon. There is **no complete printable part set, no print manifest, and no
assembly manifest** for the full machine. "Ready for the board to physically print" requires
exactly that package. Building it is agent-reachable CAD work (real OpenSCAD + sourced FDM limits),
with no print and no purchase.

### Board-trigger test (rev 3)
All mission requirements still clear on their labelled class — 406.4 × 406.4 mm, 5.08 mm, 6,400
cells, 41 mm stroke, 24.62 s calc, regional bounded, **$404.60 sourced** — **except the
buildable/print-ready package**, which does not yet exist.

### Disposition (rev 3)
- **Determination: NEXT NAMED AVENUE — [DND-60](/DND/issues/DND-60)** (Fabricator, with CTO
  integration): the complete printable S5-R fabrication package (STL set + print manifest +
  assembly manifest + printability pass + CI coherence gate).
- **Measurement-only residue** (un-retirable under DND-27), to be reported in the final package
  for the board's own build/measure: R-DND54-1/-2, the as-printed per-set q, the loaded NEMA17
  speed/torque curve.
- **DND-57 re-blocked on DND-60** (first-class) for the wake path. **No board contact.**

---

## Rev 4 (2026-09-29) — after DND-60: SUCCESS is one bounded step away (full-tile geometry)

`issue_children_completed` fired when [DND-60](/DND/issues/DND-60) (the printable fabrication
package) reached `done`. Verified on `main` (`70566f1`), including a first-hand run of the
package coherence gate (**PASS**).

### What DND-60 achieved
- A **complete real-OpenSCAD printed-part set**: 14 distinct parts / 25,661 pieces.
- **14 watertight, bed-fitting STLs**; full-set printability **PASS** (no FAIL, no RISK) against the
  sourced FDM limits; DND-59 keeper (0.90 mm / 2 lines) and DND-58 rack (1.00 / 0.50 mm) carried forward.
- **Print manifest** (qty / material / nozzle+layer / orientation / sourced limit / est. mass+time)
  and **assembly manifest** (exploded order + fasteners + ratified **$404.60 delivered** BOM).
- **CI coherence gate** (`fab_package_checks.py`, C1–C6) that pins the package to the promoted model.
- `08-current-design/README.md` §6a "How to print and build" + measurement-only residue pointer.

### The honest remaining gap — not yet slicer-ready
The package's STLs are **CAD witnesses**. Two structural tiles are **reduced witness blocks**:
- `cell_cartridge.stl` = an **8×8 witness** of the true **27×27, 137.16 × 137.16 mm cartridge**;
- `platen_module.stl` = a **27×27 witness** of the platen tile.

A board member cannot slice these and print the **real** structural parts. Completing the full-tile
geometry (or a documented sub-tile print set with joint/assembly spec) is bounded, agent-reachable
CAD work — no print, no purchase.

### Why this is not yet SUCCESS
The board trigger is "a buildable shape display **ready for the board to physically print**." A
package whose structural tiles are periodicity witnesses is not yet directly printable. Declaring
SUCCESS now would overstate the package.

### Why this is not an exhausted FAILURE
The remaining gap is one bounded CAD task with a clear owner and path; no killer is proven.

### Disposition (rev 4)
- **Determination: NEXT NAMED AVENUE — [DND-61](/DND/issues/DND-61)** (Fabricator): full-tile
  geometry for every witness-block part, or a documented sub-tile print route, with the coherence
  gate extended to fail on un-documented witnesses. **This is the last avenue before SUCCESS.**
- On DND-61 close, if every part is a true printable part / documented sub-tile set, the CEO call is
  the **SUCCESS handoff to the board (trigger 1)**.
- **Measurement-only residue** (the board's build/measure): as-printed PLA–PLA μ / scallop+tip
  sharpness (K2), leaf creep/fatigue (K11), as-printed per-set keeper reliability q (R1), loaded
  NEMA17 torque-speed (K6). Un-retirable under DND-27.
- **DND-57 re-blocked on DND-61** (first-class) for the wake path. **No board contact yet.**

---

## Rev 5 (2026-09-29) — after DND-61 + DND-62: package slicer-ready; final doc reconcile (DND-64)

`issue_blockers_resolved` fired when [DND-61](/DND/issues/DND-61) (full-tile geometry) and
[DND-62](/DND/issues/DND-62) (CTO recovery/merge) closed. Verified on `main` `b1d6659`,
first-hand.

### Package is now slicer-ready
- `cell_cartridge` renders the **true 27×27 / 137.16 × 137.16 × 14 mm** full-tile solid (67,488 tris);
  the DND-60 8×8 witness is gone. `platen_module` confirmed full 137.16 × 137.16 × 7 mm (its DND-60
  "witness" label was a documentation error).
- `fab_package_checks.py` **GATE PASS (C1–C7)** run locally on `main`; C7 fails any committed STL
  whose bbox ≠ its declared real envelope, or a reduced witness without a documented sub-tile route.
- `analytic_printability.py --fail-on-design-fail` **VERDICT PASS** (every critical feature clears
  the sourced FDM limits; no FAIL, no RISK). Documented 3×3 sub-tile fallback for beds < 137.16 mm.

### The final gap — the source-of-truth README describes the wrong machine
`08-current-design/README.md` is **internally inconsistent**:
- **Header + §1 "Machine in one paragraph"** describe the **incumbent S5** (full-width **80-channel
  programming head**, **80 bought PM steppers**), not the promoted **S5-R** (shared-drive register,
  **2 bank motors + 40 writer solenoids**, R=4 bank).
- **§2** compares S5 ($482.95/$501.51), not S5-R ($404.60).
- **§7** is the **old S5 K-register (K1–K12)**, not the S5-R register; it still lists K7 as the
  binding residual, whereas S5-R retires the 80-motor cliff.
- Only **§6a** and the fabrication package are S5-R-correct.

A board member opening the source of truth first sees the **superseded** machine. That is a handoff
defect: the README must lead with the machine we are handing over. The fabrication package itself is
correct (S5-R: 40 writer stations, 2 bank motors, R=4) — this is a documentation-coherence gap, not
a geometry gap.

### Why not SUCCESS yet
The board trigger requires a package the board can act on. A package fronted by a README that
describes a different, superseded machine is not a clean handoff.

### Why not exhausted FAILURE
The remaining item is one bounded documentation reconcile with a clear owner; no killer proven.

### Disposition (rev 5)
- **Determination: NEXT NAMED AVENUE — [DND-64](/DND/issues/DND-64)** (CTO): reconcile
  `08-current-design/README.md` to a single, coherent **S5-R** description (header → §1 → §2 → §7 →
  §6a), with the legacy S5 K-register relocated and labelled, plus a CI coherence check against the
  promoted model. **This is the last item before the SUCCESS handoff.**
- On DND-64 close, with a coherent README and the slicer-ready package, the CEO call is the
  **SUCCESS handoff to the board (trigger 1)**.
- **Measurement-only residue** (the board's build/measure): as-printed PLA–PLA μ / scallop+tip
  sharpness (K2), leaf creep/fatigue (K11), per-set keeper reliability q (R1), loaded NEMA17
  torque-speed (K6) — named in `fabrication/README.md` §5.
- **DND-57 re-blocked on DND-64** (first-class). **No board contact yet.**

---

## Rev 6 (2026-09-29) — SUCCESS: board-trigger 1 fired

`issue_children_completed` fired when [DND-64](/DND/issues/DND-64) (README reconcile) reached
`done`. Verified on `main` (`9130730`) first-hand: ran the README-coherence gate, the fabrication
package gate, the printability check and the register/residual checks — all **PASS**.

### Board-trigger test (final)

| Requirement | S5-R | Evidence class | Meets? |
|---|---|---|---|
| ~400 × 400 mm | 406.4 × 406.4 mm | model / CAD | yes |
| ~5.08 mm pitch | 5.08 mm | CAD | yes |
| ~6,400 cells | 80 × 80 | design | yes |
| ≥ 40 mm travel | 41 mm platen stroke | CAD + calc | yes |
| full-map reconfig < 30 s | **24.615 s** (`clears_30s`, margin 5.385 s) | calc | yes |
| regional updates | 3.9–24.7 s | calc | yes |
| purchased cost < $500 | **$404.60 delivered** (ratified; margin $95.40) | sourced | yes |
| **buildable / printable** | **complete slicer-ready package** (14 parts / 25,661 pieces, all full-size; C1–C7 PASS; printability PASS) | CAD + sourced | **yes** |

### What was verified on `main` (`9130730`), first-hand
- `tools/validate/readme_s5r_coherence.py` → **GATE PASS (R1–R6)**; `08-current-design/README.md`
  describes **one** machine consistently (S5-R); incumbent S5 is labelled superseded; the S5-R
  residual register is live; the legacy K-register is in a labelled appendix.
- `08-current-design/fabrication/tools/fab_package_checks.py` → **GATE PASS (C1–C7)**; no reduced
  witness blocks; `cell_cartridge` is the true 27×27 / 137.16 mm part.
- `tools/validate/analytic_printability.py … --fail-on-design-fail` → **VERDICT PASS**.
- `s5r_register_checks.py` **20 OK**; `s5r_residuals_checks.py` **12 OK**.
- Promoted model: `full_map_s5r_s = 24.615`, `delivered_usd = 404.60`, `clears = true`.

### The handoff content (what the board prints)
- **Print manifest:** `fabrication/manifests/print_manifest.md` — per part: qty, PLA, nozzle/layer,
  orientation, supports, sourced FDM limit, est. mass/time. Every critical feature PASSES.
- **Assembly manifest:** `fabrication/manifests/assembly_manifest.md` — exploded ordering,
  fasteners, and the ratified **$404.60 delivered** purchased BOM.
- **Part set:** `fabrication/stl/` (14 STLs) from `fabrication/scad/s5r_parts.scad`.
- **Sub-tile fallback:** a documented 3×3 `cell_cartridge_tile` route (45.72 mm) if the board's bed
  is under 137.16 mm; not required on a 256 mm X1C.

### The measurement-only residue (open by design; the board's print retires it)
As-printed PLA–PLA friction μ and scallop/tip sharpness (K2 class); printed-leaf creep/fatigue (K11
class); as-printed per-set keeper reliability q (R1 class, requirement bounded at q ≤ 1.57e-6); the
loaded NEMA17 torque-speed curve (K6 class). Named in `fabrication/README.md` §5 and the README §7
S5-R register. **No claim of physical validation is made anywhere.**

### Disposition (rev 6)
- **SUCCESS — trigger 1.** Board approval [4ffbf3b7](/DND/approvals/4ffbf3b7-c706-432c-bcd4-8a729eea06e9)
  linked on this issue; DND-57 → `in_review`, owner = board (print & physically verify).
- Team on standby to turn around printability/assembly feedback.
- **This is the first and only permitted board contact** ([DND-32](/DND/issues/DND-32)).
