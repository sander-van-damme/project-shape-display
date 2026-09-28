# Test11: falsification library + shared isolation rig (S1–S5 rejection tests)

Adversarial layer for the shape-display survivors. Delivers the evidence matrix
update, a per-survivor cheapest-rejection register, the reliability arithmetic,
the architecture-agnostic Q5 regional-isolation rig the project was missing, and
a slicer-level printability de-risking of the J2 rig before its first print.
**No physical evidence is claimed** — everything here is analytical, CAD, or
protocol.

## Engineering question

For each serious candidate (S1–S5): what is the *cheapest experiment that can
reject it*, with explicit gates, and can a small coupon even distinguish a good
architecture from a bad one? Plus: how much isolation does a regional reveal
need, and does tile size change the answer?

## What changed

- **`06-experiments/test11_falsification_library/`** (new)
  - `falsification_register.csv` — one row per claim: cheapest rejection test,
    gates, cycle counts, pass/fail consequences (S1-A/B … S5-A/B + CROSS-A–D).
  - `reliability.py`, `checks.py` — per-cell → 6400-cell map probability,
    regional scaling, return margin, tolerance yield; 19 CI-pinned regressions.
  - `isolation_rig_protocol.md`, `measurement_plan.md`,
    `isolation_rig_runner.py`, `check_fixture.py`, `j2_isolation_rig.scad`,
    `measurements/isolation.csv` — the Q5 rig, its gate engine and fixture gate.
  - `make_register.py` — regenerates the register and checks field counts.
  - `printability_slice_check.py`, `PRINTABILITY_REPORT.md`,
    `printability_slice_report.json` — slicer-level printability analysis of the
    J2 STL bundle ([DND-16](/DND/issues/DND-16), inputs from [DND-14](/DND/issues/DND-14)):
    mesh health, wall thickness, overhangs, plate layout, socket-pocket
    openness. Reproduces all six parts from the STL; verdict
    **PRINT-READY PENDING HARDWARE**, two non-blocking SCAD corrections (C1 dead
    `chamfer_mm`, C2 over-broad "no overhang" claim).
- **`07-evidence-and-decisions/README.md`** — adversarial survivor status table.
- **`06-experiments/README.md`**, **`.github/workflows/ci.yml`** — index + CI.
- **`.github/workflows/open-pr.yml`**, **`.github/PR_BODY.md`** — credential-free
  PR opener (workflow-scoped `GITHUB_TOKEN`, `pull-requests: write`).

## Evidence produced (labelled)

- **CALCULATED:** at 0.01 %/cell error, P(all 6400 correct) = **52.7 %**; at
  0.001 % → 93.8 %; a 99 % map needs q ≤ 1.57e-6 (~1.91 M zero-failure trials).
  A six-cell coupon is 99.94 % perfect *even at the failing rate* — a clean small
  demo cannot promote an architecture.
- **CALCULATED:** solid 2.069 g column = 20.29 mN gravity vs 5 mN assumed drag →
  only **15.29 mN** headroom; hollow 0.997 g is already below the 2× rule.
- **CAD + PROTOCOL:** J2 rig with measured gates (neighbour peak ≤ 0.10 mm, no
  miniature tip, seam ≤ 0.25 mm, 100-cycle drift ≤ 0.20 mm); fixture geometry
  gate passes (5.08 mm pitch, X1C single-plate fit).
- **CAD ANALYSIS:** every J2 part is manifold/watertight; minimum real wall
  2.0 mm (≥ 3×0.4 mm); single-plate layout 131.6 × 128.2 mm fits the X1C; the
  holder socket is a real open pocket with no internal bridge. The only >45°
  overhangs are the indicator-bracket stem-hole crown (self-supporting at 0.20 mm).
- **NOT STARTED:** every survivor's physical gate. S5's 5 N abuse gate remains
  unpassed even in the ideal model.

## Scope note

This branch also carries the [DND-16](/DND/issues/DND-16) slicer-level
printability report (commit `4cad1ca`), by the same author, because both are
Test11 evidence artifacts for the same J2 rig. The CTO owns the physical print
([DND-14](/DND/issues/DND-14)).

## Passed / failed

- `checks.py`: 19/19 pass. `isolation_rig_runner.py --validate/--selftest`: pass
  (gate engine fires PASS/KILL/INCONCLUSIVE on synthetic rows). `check_fixture.py`:
  PASS (SCAD render step reports SKIPPED — no OpenSCAD in the agent env).
- All wired into the `engineering-checks` CI workflow.

## Assumptions / limits

- No printed or measured evidence exists. The register gates and measurement
  plan thresholds are proposed, not results. The runner/fixture tests prove the
  *machinery* is self-consistent, not that any survivor passes.
- Physical build/measure is owned by the CTO (Bambu X1C, PLA).

## Remaining uncertainty / next test

- Which survivor survives the J2 neighbour-disturbance gate — the single
  discriminator for S1/S2/S4.
- Hand the J2 print set (`part = "plate"`) and the S5/Test09 Stage A fixture to
  the CTO, run J2-0 rig qualification, then feed the dated run into
  `isolation_rig_runner.py --input` for GO/KILL calls.

## Related

- Source issue: [DND-5](/DND/issues/DND-5)
- Goal: [DND-1](/DND/issues/DND-1)
