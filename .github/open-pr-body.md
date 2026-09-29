# DND-76: ultra-low-cost cell/mechanism primitives (<$250) — four divergent primitives + CAD

Adds `09-lowcost-alternative/primitives/`: four concrete cell-level / selection primitives that
attack the four S6-LC weak points named in [DND-76](/DND/issues/DND-76). **`08-current-design/` is
untouched.** This is an input to the [DND-71](/DND/issues/DND-71) synthesis, not a promotion.

**Evidence class:** CALCULATION over sourced FDM limits + CAD (real OpenSCAD). **No print, no
purchase, no measurement** ([DND-27](/DND/issues/DND-27)). **No board contact**
([DND-32](/DND/issues/DND-32)).

## Engineering question

[DND-71](/DND/issues/DND-71)'s candidate **S6-LC** (banked broadcast ratchet, per-bank threshold
mask, pawl-in-rack memory, 3 motors, ~$139.77) has four named weak points. Can **cell-level /
selection primitives** make it cheaper or more reliable — counting every component, with no
scaling hidden behind the words "selector" or "clutch"?

## Answer

**Yes — four primitives, all 100 % printed, adding zero bought selectors, zero bought clutches and
zero motors.** They turn tolerance-fragile *forces* into hard-stop *positions*, and the machine
still clears every gate: **13.0 s** full map (< 30 s), **$170.17 purchased** at worst-case optional
extras (< $250). The honest trade is a **correlated, silent error** if a whole comb or clutch
fails (bounded by 4 home sensors per bank, never per-cell feedback).

## What changed

- **`09-lowcost-alternative/primitives/primitives.py`** — analytic model:
  - **P1** friction-independent **bistable over-centre latch** (attacks #1 release-force spread).
    Hostile arithmetic: the S6-LC friction pawl's release force spans **0.79 → 1.78 N** (2.24×)
    across the sourced PLA μ band at the DND-48 bounding 3.27 N load → implied spread **19.1 %**
    vs the **9 %** break-even. The 0.90 mm (2-line) latch snap is **0.61 N** and stores state as a
    hard-stop position, so **μ leaves the stored state**.
  - **P2** **printed 4-plane louvre comb stack** as the mask medium (attacks #2). Screens five
    candidates and **rejects** paper punched cards, the single relative-shift comb (recorded as a
    failed idea), a bought 80-channel punch head ($38), and magnetic combs. Selected medium is
    **$0, 0 extra motors**; comb web **1.32 mm**, guide gap **0.20 mm** worst case. Decisive
    failure: a stuck comb mis-arms a **whole 80-cell band**, silently.
  - **P3** **relieved pocket throat + V-guide** at 3.60 mm body / 1.48 mm lane (attacks #3).
    Pawl throw **0.48 mm**, throat **30°** (< the 45° sourced limit), V-guide **9× margin**,
    pocket floor in compression **19×** the 3.27 N service load — **never a bending leaf**.
  - **P4** **single-actuator banked reset** (attacks #4): a reset bar rides the **common platen**
    (no second carriage, no extra motor) and 8 **printed one-way pawl clutches** free-wheel on the
    up-stroke. Reset **6.8 s**. A friction/detented slip-ring clutch is **rejected** for the same
    μ-spread reason as P1.
  - Full system accounting: all ten jobs, component counts, BOM delta, timing budget.
- **`09-lowcost-alternative/primitives/primitives_checks.py`** — **35 CI-style assertions**
  pinning every headline (baseline, each primitive, the system gates, the verdict).
- **`09-lowcost-alternative/primitives/scad/{s6lc_cell,mask_comb,reset_bar}.scad`** — real
  OpenSCAD for the cell, the comb bar and the reset bar.
- **`09-lowcost-alternative/primitives/tools/render_primitives_cad.py`** — renders with a **real**
  OpenSCAD and **fails hard** without one (no box-arithmetic meshes).
- **`09-lowcost-alternative/primitives/README.md`** — the full primitive write-up.
- **CI:** new `DND-76` check step (model + checks) in `engineering-checks`, and a new
  `lowcost-primitives-cad-render` job (hard-fails if OpenSCAD is missing).

## Evidence produced

| Check | Result |
|---|---|
| `primitives.py` | screen runs; **all 10 gates pass** |
| `primitives_checks.py` | **35 passed, 0 failed** |
| `render_primitives_cad.py` | **exit 2 without OpenSCAD** by design; CI job renders with it |
| System timing | **13.0 s** full map (margin 17.0 s, assumption-conditional) |
| System cost | **$170.17** worst case purchased; required delta **$0** |

## Assumptions

- Written dwell (0.50 s/bank) and platen stroke (0.55 s) are **stated assumptions**, the same class
  as S1's 25.20 s budget and S5-R's writer settle. **Not measured.**
- Print stiffness/modulus uses the sourced PLA midpoint (1500 MPa) and the sourced μ band.
- The common platen means the four broadcast strokes are paid **once**, not per bank; only the mask
  write is serial.

## What passed / what failed

- **Passed:** cell fit, comb printability, guide margin, compression load path, no-extra-motor,
  full-map < 30 s, cost < $250 worst case, friction-independent state.
- **Failed ideas recorded as evidence:** paper punched card; single relative-shift comb; bought
  80-channel punch head; magnetic printed comb; friction/slip-ring reset clutch.

## What remains uncertain / next test

- P1's worst-case snap-vs-comb margin (needs a coupon; forbidden under DND-27).
- P2's whole-comb failure is only detectable as a whole-comb failure (4 home sensors/bank).
- P3's as-printed V-guide wear and throat fusing are measurement-only.
- **Next:** hand the primitives to the [DND-71](/DND/issues/DND-71) synthesis and let the
  [Falsifier](/DND/issues/DND-78) attack the correlated-failure trade against the S6-LC baseline.

Closes [DND-76](/DND/issues/DND-76).
