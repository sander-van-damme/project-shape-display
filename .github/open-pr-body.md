# DND-55 — S5-R R=4 multi-row bank assembly: bar torsion + comber/carriage envelopes

## What changed

Closes residual **R-DND54-4**: the multi-row (R = 4) bank geometry that
[DND-54] left as an assertion. Uses only the evidence classes [DND-27] permits —
**CAD + CALCULATION; no print, no purchase, no measurement**.

- `06-experiments/test12_winner_convergence/s5r_bank.py` — bank model: parametric bar
  torsion, candidate sections, clearance stack-ups, envelope fit, CAD harness, decision.
- `s5r_bank_checks.py` — 16 regression + honesty gates (CI).
- `s5r_bank.scad` — R = 4 bank CAD: columns + racked bar + reset comber + writer-carriage
  sweep envelope, with scoped interference queries.
- `07-evidence-and-decisions/dnd55-s5r-bank-assembly.md` — the ADR.
- `06-experiments/test12_winner_convergence/README.md`, `08-current-design/README.md` — folded in.
- `tools/validate/analytic_printability.py` gains a bank-assembly branch;
  `validate_geometry.py` and `render_winner_cad.py` render the bank parts;
  `.github/workflows/ci.yml` runs the model checks, printability and CAD render.

> Branched from `main` (DND-54 already merged).

## The call

Does the R = 4 bank close at the assembly level — bar torsion inside the 0.35 mm keeper
gate, and the reset-comber / writer-carriage envelopes fitting — without a coupon?

## Result — the torsion number and the envelopes

**Bar torsion (CALCULATION).** Driven from both ends, resisting 320 ganged pawls. The
reaction is modelled as an eccentric axial line (eccentricity `e` = an assumption; the
coupon that would measure tooth contact is forbidden). Peak tip skew at mid-span:

| Bar section | J (mm⁴) | G (MPa) | e (mm) | skew (mm) | vs gate/2 = 0.175 |
|---|---:|---:|---:|---:|:--:|
| printed PLA 3 × 2 (**DND-54 placeholder**) | 4.64 | 556 | 1.5 | **4.96** | **FAIL ~28×** |
| printed PLA 3 × 12 (on-edge) | 90.99 | 556 | 1.5 | 0.253 | FAIL (1.4×) |
| printed PLA round Ø8 | 402.1 | 556 | 4.0 | 0.153 | PASS |
| **sourced steel rod Ø5** | 61.4 | 76 923 | 2.5 | **0.0045** | PASS (~39×) |
| **sourced steel rod Ø6** | 127.2 | 76 923 | 3.0 | **0.0026** | PASS (~67×) |

**Fix: a sourced Ø6 mm steel drive rod** (or an Ø8 printed round bar, re-checking `e`).
The 3 × 2 placeholder bar is refuted by ~28×.

**Assembly envelopes (CAD).** Real OpenSCAD renders six parts; **all five scoped
interference queries are EMPTY** — `run_all_engaged`, `selected_dropped_pawl`,
`comber_park`, `comber_trip`, `writer_carriage_sweep`. Carriage-to-column clearance is
**0.40 mm worst case**; the comber tine rides a **3.73 mm** X-gap between column stacks;
**R = 4 adds no pitch penalty** (0.0 mm).

**Printability (CALCULATION).** PASS after one correction: the DND-54 rack
(pitch 0.60 / tooth 0.45) leaves a **0.15 mm inter-tooth gap that fuses** at a 0.4 mm
nozzle; re-dimensioned to **pitch 1.00 / tooth 0.50 mm** (gap 0.50 mm). Comber tine
0.60 → 0.90 mm (1 → 2 lines).

## Verdict

R-DND54-4 **closed for the comber/carriage envelopes and the pitch/Y lay-out**, and
**sharpened for the bar** (a sourced-rod requirement, not a printed part). Not a
print-ready claim, not board contact.

## Assumptions / what passed / what is uncertain

- **Passed:** 16 new checks, the geometry harness, the winner-CAD render, and the full
  test12 suite (all green).
- **Assumed:** the reaction eccentricity `e` (dominant input; steel makes it irrelevant),
  Poisson 0.35, carriage/comber datums.
- **Uncertain:** the bar model is a Saint-Venant bound, not FEA; the CAD is a reduced
  8-column model (80-column length covered analytically); as-printed friction/wear/creep
  remain measurement-only.

## Most informative next test

Reconcile the register's per-stroke advance to the corrected **1.00 mm rack pitch**
(R-DND55-4), and cost/source the Ø6 mm steel rod in the bank BOM.

[DND-27]: /DND/issues/DND-27
[DND-54]: /DND/issues/DND-54
