# Test09 — falsifiable validation of Test08

**Decision: Test08 is better defined and weaker as a near-term build candidate;
it is not fundamentally disproved. Do not build an 80-channel head yet.** Its
conditional timing is reproduced, but the legacy notch cannot establish a full
missed-step correction, full-scale structure is unresolved, and realistic
purchased allowances exceed $500. No physical measurement has been made.

The smallest decision sequence is **process fits → six passive cells → one
driven retained rotor → eight simultaneous channels → representative lift**.
A failure stops the dependent stages. Begin by printing PLA clearance/web
coupons on the actual X1C; do not buy eighty motors or print 6400 parts.

## Reproduce from repository root

Python 3.11+, standard library only; no package installation for this workflow:

```text
python 06-experiments/test09_test08_validation/run.py
python 06-experiments/test09_test08_validation/run.py --render
```

The second command also needs **OpenSCAD 2021.01** on PATH (`openscad.com` on
Windows). It exports STLs and renders, checks bounding boxes against 256 mm,
rejects compiler warnings/errors and runs the scoped historical contact checks.
It may take several minutes. `--cad` omits PNG rendering. OpenSCAD success is
not slicer, fabrication, whole-assembly collision or physical validation.

Individual commands are `analyze.py`, `checks.py`, `qualify.py`, and
`cad_check.py --render` in this folder. `run.py` repeats analysis and verifies
byte-identical analytical output. The workflow relies on the preserved Test08
`params.json`, `analysis.py` (mass/cross-check only) and `coupon.scad` within this
repository; no historical generated results are needed. `cad_check.py` creates
a local generated snapshot so it never changes historical source or results.
During coupon-only iteration, `cad_check.py --render --coupons-only` reruns the
new exports into `cad_coupons.json` without repeating unchanged historical
contact checks. Run the complete command for a fresh checkout.

## Evidence and next actions

| Artifact | Purpose |
|---|---|
| [uncertainties.csv](uncertainties.csv) | 31 hypotheses, current assumptions/evidence, test methods, pass/fail thresholds and architecture consequences |
| [engineering.md](engineering.md) | Historical source audit, geometry, return, detent, structural, timing and reliability interpretation |
| [params.json](params.json), [analyze.py](analyze.py) | Reproducible analytical model and joint sensitivity sweep |
| [coupons.scad](coupons.scad), [cad_check.py](cad_check.py) | Fit/wall/hole/slot, replaceable detent, one-motor bench parts and spliced beam specimens; historical passive geometry exports |
| [physical-plan.md](physical-plan.md) | Ordered A–E fabrication, instruments, counts, acceptance/stop gates and exact bench assembly |
| [measurements/](measurements/) and [qualify.py](qualify.py) | Blank physical records and conservative measured-input timing replay; currently `NOT_MEASURED` |
| [bom.csv](bom.csv), [sources.md](sources.md) | Current price evidence, speculative targets, allowances, missing delivered quotes and contingency |
| [multirow.md](multirow.md), [multirow_bom.csv](multirow_bom.csv) | Separate 1–5-row independent/shared-motion screen and later selector test |

`results/` is already gitignored by the repository. It contains a 540-case
timing sweep, 36 map transitions, ordered worst schedule, 60 multi-row cases,
fit/level/detent/structure/lift/reliability tables, input hashes, measurement
gate and CAD records/STLs/PNGs. These are reproducible calculations, not records
of fabricated parts. Keep future physical records outside `results/`.

## Findings at the committed defaults

- Independent timing: **26.251 s**, only **0.749 s** to the ≤27 s engineering
  target. No measured operating region exists. Inspection/recovery can consume
  that margin immediately.
- Legacy notch point-follower capture envelope: **±8.72°**, smaller than an
  18° missed step. The new broad detent's restoring torque is only **0.00298
  mN m** in the ideal leaf model; friction and seating remain unverified.
- Four/five levels remain geometrically plausible; six has almost no angular
  reserve and does not align with full steps. Eight or more fail this toe width.
- Full-width illustrative box beams sag **0.799 mm** at the stated load/modulus;
  closer support is needed. Splice compliance, racking and brake remain gates.
- Purchased estimates with contingency: **$411.60 optimistic / $1089.65
  realistic allowance / $5993.85 conservative retail**. Only the speculative
  combination fits; no matched delivered BOM qualifies.
- Four/five-row shared motion has a **conditional** timing window, but needs
  complete selectors below roughly **$0.54/$0.43** each. Retain a later 2×4
  dynamically selected latch coupon, not a full travelling head.

## Exact next print

Start with `results/fit_tile_0.05.stl`, `fit_tile_0.1.stl`,
`fit_tile_0.15.stl`, `walls.stl`, `bushings.stl` and `slider.stl`, PLA/X1C,
0.4 mm nozzle/0.12 mm layers. Repeat critical failures on 0.2 mm/0.08 mm;
inspect actual sliced walls. Then make 30 winning interchangeable cell sets
across three batches and test measured drag against half measured weight.
Stage A failure is useful evidence; no quantity is marked passing by simulation.
