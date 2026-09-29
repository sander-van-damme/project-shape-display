# 09 — Ultra-low-cost S5-R variant (<$250 purchased): NEGATIVE RESULT + break-even

**Status: NEGATIVE RESULT.** The promoted S5-R machine cannot be brought under a
**$250 purchased** cost while every other mission requirement is unchanged. The
sub-$250 space for this architecture is **empty**, not merely thin. This
directory is the proof, the sourced cost ladder, the topology screen and the
**break-even number** — delivered exactly as [DND-72](/DND/issues/DND-72)
permits ("a negative result is a valid deliverable").

> **This does not touch `08-current-design/`.** S5-R remains the promoted
> machine at **$404.60 delivered / 24.615 s**. This subdirectory is a *separate*
> exploration of the <$250 question.

## Headline

| Quantity | Value | Class |
|---|---:|---|
| S5-R fixed no-channel base | **$218.70 parts → $253.69 delivered** | CALCULATION (inherited, sourced + allowances) |
| Base alone vs the $250 target | **101.5 % — exceeds it by $3.69** | CALCULATION |
| Purchased headroom left for actuators | **−$3.18 parts (negative)** | CALCULATION |
| Sub-$250 configurations in a 570-point sweep | **0** | CALCULATION |
| Cheapest requirement-preserving configuration | **R6-W20-M2, $345.90 delivered, 29.987 s** | CALCULATION |
| **Break-even (the honest floor)** | **~$346** | CALCULATION |
| Gap from target | **$95.90 (~$96)** | CALCULATION |

**Why:** the purchased base of the S5-R architecture — the bought non-actuator
lines (frame, lift/drive, supply, loom, fasteners, controller, PCB/passives
allowance) — **already costs $253.69 delivered with zero actuators**. Any
actuator only adds cost. So no actuator count can reach <$250, and the cheapest
configuration that still meets the mission's < 30 s full-map gate is **$345.90**.

## What is here

| File | Purpose |
|---|---|
| [`s5r_ultra.py`](s5r_ultra.py) | Analytic model: fixed-base proof, topology screen, exhaustive budget scan, relaxation ladder, verdict. Imports the promoted S5-R model so it cannot drift. |
| [`s5r_ultra_checks.py`](s5r_ultra_checks.py) | 19 CI-style assertions pinning every headline number. |
| [`scad/s5r_ultra_cell.scad`](scad/s5r_ultra_cell.scad) | The unit cell of the cheapest requirement-preserving point (R=6 bank cross-section + unchanged DND-59 cell). Real OpenSCAD. |
| [`stl/`](stl/) | Watertight renders (`cell`, `pawl`, `keeper`). |
| [`tools/render_lowcost_cad.py`](tools/render_lowcost_cad.py) | Renders + mesh-validates the parts with a real OpenSCAD, fails hard if OpenSCAD is missing. |

Run:

```bash
cd 06-experiments/test12_winner_convergence   # so the model imports resolve
PYTHONPATH=$PWD python ../../09-low-cost-variant/s5r_ultra.py
python 09-low-cost-variant/s5r_ultra_checks.py
python 09-low-cost-variant/tools/render_lowcost_cad.py
python tools/validate/analytic_printability.py \
  09-low-cost-variant/scad/s5r_ultra_cell.scad
```

## The cost ladder (sourced)

| Line | Parts | Delivered |
|---|---:|---:|
| Fixed no-channel base | $218.70 | $253.69 |
| + bank motors (2 × $12.00) | $24.00 | $27.84 |
| + writer solenoids (40 × $2.50) | $100.00 | $116.00 |
| + bank H-bridge ICs (2 × $0.7955) | $1.59 | $1.85 |
| + writer darlington chips (5 × $0.30) | $1.50 | $1.74 |
| + sourced steel drive rod | $3.00 | $3.48 |
| **= promoted S5-R** | **$348.79** | **$404.60** |

## Requirement preservation

The chosen point (the cheapest that preserves every requirement) is
**R6-W20-M2** (bank depth R=6, 20 writer solenoids, 2 bank motors):

| Requirement | Status | Class |
|---|---|---|
| 406.4 × 406.4 mm / 5.08 mm / 6,400 cells | preserved (geometry unchanged) | CAD |
| ≥ 40 mm travel | 41 mm platen stroke | CAD + calc |
| full-map < 30 s | **29.987 s** | CALCULATION (crank/settle-conditional) |
| regional updates | common platen ⇒ one stroke | CALCULATION |
| X1C-buildable | unit cell watertight, printability **PASS** | CAD + sourced limits |
| **purchased < $250** | **$345.90 — FAILS** | CALCULATION + sourced |

## Evidence discipline ([DND-27](/DND/issues/DND-27))

**No print, no purchase, no measurement.** Every claim above is CALCULATION
over sourced listings and stated allowances on the promoted S5-R model, or CAD
(real OpenSCAD). The one number that would overturn this verdict is recorded as
a falsifier: a **sourced, non-requirement-touching fixed-base reduction below
$215.52 parts** ($250 delivered). See
[`07-evidence-and-decisions/dnd72-low-cost-variant.md`](../07-evidence-and-decisions/dnd72-low-cost-variant.md).
