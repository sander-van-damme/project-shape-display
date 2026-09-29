# DND-54 — S5-R register analytic + CAD dropout-latch model (promote S5-R)

## What changed

Defines the **S5-R shared-drive programmable register** concretely and decides it
using only the evidence classes [DND-27] permits — **CAD + CALCULATION; no print, no
purchase, no measurement**.

- `06-experiments/test12_winner_convergence/s5r_register.py` — mechanism definition +
  static/kinematic model (cell fit, neighbour cross-talk, writer force, bank drive
  force, service-load inheritance, endurance, timing, BOM, sensitivity, verdict).
- `s5r_register_checks.py` — 15 regression + honesty gates (CI).
- `s5r_register.scad` — CAD unit cell (housing, rotor, printed pawl, over-centre
  keeper, toothed drive bar).
- `07-evidence-and-decisions/dnd54-s5r-register-latch.md` — the ADR.
- `08-current-design/README.md` and the DND-52 ADR updated to promote S5-R.
- `tools/validate/analytic_printability.py` gains a register-cell branch;
  `validate_geometry.py` and `render_winner_cad.py` render the register cell;
  `.github/workflows/ci.yml` runs the model checks, the printability table and the CAD
  render.

## Engineering question addressed

Does S5-R's decisive quantity — **selective dropout / re-engage of a bank of rotors
at 5.08 mm pitch** — close analytically, so that the program's only
cost+time-viable pivot can be machine-defined without the coupon that DND-27 forbids?

## The DND-54 correction to DND-52

DND-52's option-1 timing replaced the whole 80-column step time with a token
"20 stations × 0.3 s" and did not model a per-row cycle. Counted honestly, a
**single-row** bank (R=1) needs 80 groups and is **≥36 s even at an aggressive
3 rev/s crank**. The real lever is that the bank bar can span **R rows in depth at
no pitch penalty** (row pitch is independent of the in-row column pitch), so one
bank pass writes R rows at once.

## Result — all seven analytic gates pass at R=4

| Gate | Value | Limit | Margin |
|---|---|---:|---:|
| cell fit (worst case) | stack 1.55 mm | ≤ 2.08 mm | 0.53 mm |
| neighbour cross-talk | 0 N (a dropped pawl carries no rack force) | — | gap 0.33 mm |
| writer release force | 0.066 N | 1.20 N | 18× |
| bank drive force | 46.6 N | 100 N (2 motors) | 2.15× |
| latch vs service load | 0 N added | inherits K1 | unchanged |
| full-map time | **24.62 s** | < 30 s | +5.39 s |
| delivered cost | **$397.53** | ≤ $500 | −$102.47 |

Cycle life is reported ("≥1e6, order unknown", DND-46 FDM basis) on the same terms
as every other printed leaf.

## Evidence produced

- **CALCULATION** over sourced FDM limits (`tools/fdm-limits`) and sourced actuator
  ratings; every figure labelled sourced/assumed/calculated/endurance.
- **CAD**: `s5r_register.scad` renders with real OpenSCAD into four watertight STLs;
  the sourced printability gate returns PASS/PASS/RISK/PASS/PASS/PASS — the single
  RISK is the 0.45 mm keeper leaf (1 extrusion line), an **accepted** risk for a
  lightly-loaded bistable latch, stated not hidden.
- **Sensitivity** (break-even): crank 468 °/s, writer settle 0.084 s, fit tolerance
  ±0.365 mm, single-motor bank margin 1.07× (→ use two motors).

## Assumptions / what passed / what is uncertain

- **Passed:** all seven gates; the DND-54 sensitivity table; 15 new checks green and
  the existing test12 suite unchanged.
- **Assumed:** crank 720 °/s and writer settle 0.05 s (the time gate is conditional
  exactly as S5's K6 is conditional on its dwell); wheel/solenoid prices are
  point-in-time.
- **Uncertain (stated, not retired):** as-printed pawl/keeper friction μ, gate/tip
  sharpness, leaf creep (K2/K11 class), and the full multi-row (R=4) bar assembly
  (torsion, reset-comber and writer-carriage envelopes) — the last is the next
  **no-coupon** CAD test.

## Verdict

**PROMOTE S5-R (R=4) to a machine-definition candidate** alongside the incumbent S5;
S5 remains a nominal fallback only (refuted on the order-tier motor price). This is
**not** a print-ready claim and **not** board contact — the board trigger is a
buildable print-ready machine, which the measurement-gated residuals still block.

## Most informative next test

A **multi-row (R=4) bar-assembly CAD** — the only unit-cell-external geometry not
yet modelled — checking bar torsion, the reset-comber envelope and the writer
carriage envelope. Analytic/CAD only; no coupon.

[DND-27]: /DND/issues/DND-27
