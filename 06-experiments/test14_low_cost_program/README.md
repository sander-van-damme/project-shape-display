# test14 — low-cost program: S6-LC selection + S5-R-trim negative result

> **Provenance / experiment stage.** This package is the exploratory low-cost program
> (computations, screens, checks, CAD). The **selected S6-LC machine** is an integrated design and
> now lives at [`08-integrated-designs/s6lc-low-cost/`](../../08-integrated-designs/s6lc-low-cost/README.md);
> this directory retains its supporting negative results, divergent concepts, primitives and
> sourcing work. Originally the top-level `09-low-cost-variant/` stage, retired by
> [DND-117](/DND/issues/DND-117).

**Status: SYNTHESIS — one architecture selected.** Two questions were asked under
[DND-70](/DND/issues/DND-70)/[DND-72](/DND/issues/DND-72) and are reconciled here:

1. **Can the S5-R architecture be trimmed under $250?** **No.** The fixed no-channel
   base ($218.70 parts → $253.69 delivered) alone exceeds the $215.52 parts budget;
   the requirement-preserving break-even is **$345.90 delivered**. Proof + 19 checks:
   [`s5r_ultra.py`](s5r_ultra.py), [`s5r_ultra_checks.py`](s5r_ultra_checks.py).
2. **Is there a *different* architecture under $250 that keeps every mission
   requirement?** **Yes — [S6-LC](../../08-integrated-designs/s6lc-low-cost/README.md).** A **$139.77 parts / $162.13
   delivered / 7.4 s** machine that removes the per-row bought actuator entirely.

> **This does not touch `08-integrated-designs/s5r-shared-drive-register/`.** S5-R remains the promoted machine at
> **$404.60 delivered / 24.615 s**. This directory is a *separate* exploration of the
> <$250 question. Full reconciliation: [`../07-evidence-and-decisions/dnd72-low-cost-synthesis.md`](../../07-evidence-and-decisions/dnd72-low-cost-synthesis.md).

## Selected machine — [S6-LC](../../08-integrated-designs/s6lc-low-cost/README.md)

Family = the screened **S1 broadcast threshold ratchet**; height held by a passive printed
pawl (no per-cell/per-row bought actuator); selection by an off-line **punched-card per-bank
mask gate**; lift by **one** lead-screw stepper. Run:
`python 08-integrated-designs/s6lc-low-cost/analysis/s6lc_checks.py` → **29/29 pass**.

| Quantity | Value | Class |
|---|---:|---|
| Purchased parts (excl. printed) | **$139.77** | CALCULATION + sourced |
| Delivered (×1.16) | **$162.13** (margin $87.87) | CALCULATION |
| Full-map reconfiguration | **7.4 s** (margin 22.6 s) | CALCULATION |
| Bought actuators | **3 steppers** (vs S5-R's 42) | CAD + sourced |
| Travel | 50 mm (5 × 10 mm) | CAD + CALC |
| Gates G1–G6 | **all pass** | CALCULATION |

The single architectural lever is **actuator count**: the S5-R fixed base is a *consequence* of
the 40-solenoid writer bank and the 2-motor bank drive. Change the family and the base vanishes.

## The negative result (why a trim cannot work)

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
| [`s6lc/`](../../08-integrated-designs/s6lc-low-cost/README.md) | **Selected machine S6-LC** — model, 29 checks, BOM (`bom_s6lc.csv`), real-OpenSCAD CAD + renders, evidence notes. |
| [`divergent/`](divergent/README.md) | **DND-75 inventor divergence** — A1 single-shaft cam ($67.63), A2 hand-crank/tape ($49.76), A3 S1-B banked broadcast ($114.02); 18 checks + printability. Alternatives to S6-LC, folded in. |
| [`primitives/`](primitives/README.md) | **DND-76 cell/mechanism primitives** (supporting, formerly the retired `09-lowcost-alternative/primitives/` root) — P1 bistable latch, P2 printed louvre comb, P3 pocket/guide, P4 single-actuator reset; 35 checks + real-OpenSCAD CAD. Inputs to the synthesis; no architecture promoted. |
| [`reliability_sourcing/`](reliability_sourcing/cost_envelope_dnd104.md) | **DND-109 reliability-first cost/printability envelope** — sourced-class prices, 3 scenarios + per-cell sensitivity, media/consumable flags, PROVISIONAL vs sourced FDM rules, assembly/reliability scaling for the DND-104 mechanism classes. Gate: `cost_envelope_checks.py`. |
| [`s5r_ultra.py`](s5r_ultra.py) | Negative-result proof: fixed-base floor, topology screen, exhaustive budget scan, relaxation ladder, verdict. Imports the promoted S5-R model so it cannot drift. |
| [`s5r_ultra_checks.py`](s5r_ultra_checks.py) | 19 CI-style assertions pinning every negative-result headline number. |
| [`scad/s5r_ultra_cell.scad`](scad/s5r_ultra_cell.scad) | The unit cell of the cheapest requirement-preserving S5-R trim point (R=6 bank cross-section + unchanged DND-59 cell). Real OpenSCAD. |
| [`stl/`](stl/) | Watertight renders (`cell`, `pawl`, `keeper`). |
| [`tools/render_lowcost_cad.py`](tools/render_lowcost_cad.py) | Renders + mesh-validates the parts with a real OpenSCAD, fails hard if OpenSCAD is missing. |

Run:

```bash
python 08-integrated-designs/s6lc-low-cost/analysis/s6lc_checks.py       # 29/29 — selected machine
python 06-experiments/test14_low_cost_program/s5r_ultra_checks.py               # 19/19 — negative result
python 06-experiments/test14_low_cost_program/reliability_sourcing/cost_envelope_checks.py  # DND-109 envelope gate
python 06-experiments/test14_low_cost_program/tools/render_lowcost_cad.py
python tools/validate/analytic_printability.py \
  06-experiments/test14_low_cost_program/scad/s5r_ultra_cell.scad
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
[`07-evidence-and-decisions/dnd72-low-cost-variant.md`](../../07-evidence-and-decisions/dnd72-low-cost-variant.md).
