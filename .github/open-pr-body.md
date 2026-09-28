# DND-28: re-scope T11-A + J2 physical gates to analytic/simulation gates

Supersedes [DND-21](/DND/issues/DND-21) and [DND-14](/DND/issues/DND-14).

## What changed

The physical print/measure gates of the T11-A S3 selector fan-out coupon and the
J2 isolation rig can no longer be executed (board policy [DND-27](/DND/issues/DND-27):
no physical print tests). This PR replaces them with the strongest
**non-physical** evidence gates that can still reject the candidate
architectures, and teaches the existing CI-tested gate engines to consume
analytic input without ever presenting it as physical validation.

### A — T11-A selector fan-out (`06-experiments/test11_shared_drive_gate_analysis/analytic/`)

- **Analytic printability gate** against *sourced* FDM process limits
  (`sourced fact` vs `assumption` labelled per value): min vertical wall
  ~1.05× nozzle (0.42 / 0.21 mm), min slot ~1× nozzle (0.40 / 0.20 mm), plus
  assumed free-gap and pivot-definition floors.
- **Interference/tolerance stack-up**: worst-case and Monte Carlo (200k draws,
  sigma = half_range/√3) for min web, pivot free play, land reach, lateral
  clearance and bbox, with a margin distribution.
- **CAD/mesh validation**: `verify_coupon_stl.py` retained and extended to
  render the SCAD with OpenSCAD when present (SKIP otherwise).
- **Dated analytic run record** in the exact `t11a_fit_check.py` schema with an
  `evidence=CALCULATION` column.

### B — J2 isolation rig (`06-experiments/test11_falsification_library/analytic/`)

- **Kinematic/force analysis**: clamped/simply-supported rail-beam bound for
  target→neighbour coupling; Coulomb stiction bound; isolation ratio (all with
  units and stated assumptions).
- **Fixture fit stack-up**: Monte Carlo over declared fit tolerances, plus the
  existing `check_fixture.py` mesh/render gate.
- **Claim disposition table**: which protocol claims now rest on analysis vs
  which still require measurement.
- **Dated analytic run record** in the `measurements/isolation.csv` schema with
  an `evidence=CALCULATION` column.

### Engine + CI changes

- `t11a_fit_check.py` and `isolation_rig_runner.py` read an optional `evidence`
  column; a non-measured row is never reported as `MEASURED`, and the
  measurement repeat guard is waived only for a deterministic analytic bound
  (stated in the gate note).
- CI (`engineering-checks`) regenerates and consumes both analytic run records
  end-to-end.

## Engineering question addressed

Can the S3 4-row selector fan-out be rejected, and can the J2 isolation concept
be supported, **without a physical coupon** — and if not, precisely which claims
remain physical?

## Evidence produced

- `analytic/runs/t11a_analytic_measurements.csv` → engine disposition
  `INCONCLUSIVE_RUN_A4` (analytic warning).
- `analytic/runs/isolation_analytic.csv` → engine per-tile `INCONCLUSIVE`
  (J2-0 rig noise unmeasured by design).

## Findings (calculation/simulation, **not** measurement)

- **M1 min web worst-case margin +0.11 mm** — positive but thin; the web is the
  tight feature, not the notch.
- **M3 pivot free play is not analytically decidable**: the coupon prints its
  pivot in place with **no designed radial clearance**, so the record leaves
  `M3_pivot` blank and the engine returns `INCONCLUSIVE` rather than a false
  pass or kill. Adding an explicit designed clearance is the cheapest way to
  make this analytic.
- **J2 rail-coupled neighbour bound is 0.017 mm max (20×20) vs the 0.10 mm
  gate**; stiction (0.18–2.84 N) dominates rail shear. The isolation *concept*
  is analytically sound.
- **Still measurement-required:** J2-0 rig noise floor, J2-3 cumulative creep,
  and the stiction release force. These cannot be retired analytically.

## Assumptions made explicit

- FDM limits: wall ≈1 extrusion width, slot ≈1 nozzle diameter (slicer
  convention); free-gap 0.20 mm and pivot-definition 0.40 mm are **assumptions**.
- Tolerance inputs: ±0.08 mm XY, ±0.06 mm hole, ±0.05 mm shrink, ±0.20 mm land
  window; normal with sigma = half_range/√3.
- Rail model: isotropic PLA E=2500 MPa, rigid holders, rectangular section.
- Stiction: μ=0.35 dry PLA–PLA.

## What passed / failed

- Analytic selftests for both packages: PASS.
- Both analytic records consumed by their gate engines: PASS.
- All pre-existing `engineering-checks` scripts: PASS locally.
- M3 unresolved and J2-0/J2-3 measurement-required: reported as such, not papered
  over.

## What remains uncertain

Anything a physical coupon would show: fusion, stringing, layer adhesion,
elephant-foot, warp; and for J2, the rig noise floor, creep and stiction
release.

## Most informative next test

Add an explicit **designed radial clearance** to the S3 pivot in
`selector_fanout_coupon.scad`, then re-run the analytic stack-up. That converts
M3 from unmodelled to analytic and lets the T11-A decision tree reach a real
disposition without a print.
