# J2 analytic isolation gate (DND-28)

**This directory replaces the physical J2 isolation-rig run of
[DND-14](/DND/issues/DND-14) with analytic + simulation evidence.** No physical
print tests are performed (board policy [DND-27](/DND/issues/DND-27)).

## What is here

| File | Type | Purpose |
|---|---|---|
| `j2_analytic_gate.py` | calculation + simulation | Shared-rail coupling bound, stiction/friction bound, isolation ratio, fixture fit stack-up, analytic run-record emitter |
| `runs/isolation_analytic.csv` | **analytic run record** | Three rows (5×5 / 10×10 / 20×20) in the exact `measurements/isolation.csv` schema, with `evidence=CALCULATION` |

## How it is consumed

The existing CI-tested gate engine reads the analytic record directly:

```bash
python ../isolation_rig_runner.py --validate
python ../isolation_rig_runner.py --input runs/isolation_analytic.csv
python j2_analytic_gate.py --report      # full analysis
python j2_analytic_gate.py --selftest    # asserts the analysis is sane
python j2_analytic_gate.py --emit-record # regenerate the record
```

The engine reads the `evidence` column, waives the "≥10 repeats" measurement
guard for a deterministic analytic bound (stating so in the gate note), and
labels the outcome `analytic bound, NOT a measurement`.

## The isolation concept, analytically

The two tile holders are mechanically independent except through the shared
rigid base rail. That gives two coupling paths, both bounded here:

1. **Structural (rail bending).** A clamped-clamped beam model of the 12 mm rail
   puts the neighbour-tile deflection from a 1 N target actuation at
   **0.0006 mm (5×5), 0.003 mm (10×10), 0.017 mm (20×20)** for the conservative
   simply-supported bound — all far below the 0.10 mm peak gate. The
   clamped-clamped value is ~4x smaller.
2. **Stiction / friction.** A loaded neighbour column is held by Coulomb
   friction. At μ=0.35 (assumed) the force to start sliding is **0.18 N (5×5),
   0.71 N (10×10), 2.84 N (20×20)** ballpark, orders of magnitude above the
   rail-transmitted shear. Isolation ratio (40 mm target stroke / rail-bound
   neighbour motion) is **>10⁴**.

**Fixture fit stack-up** (Monte Carlo, 200k): the 10×10 holder (62.80 mm nominal,
62.90 mm worst case) fits the X1C 256 mm bed; the two-holder pair + seam is
reachable; the fixture socket and ≥2 mm holder wall pass at 1.0000.

## Claim dispositions — analysis vs still-measurement

| Quantity | J2 step | Retired by | Note |
|---|---|---|---|
| rig noise floor | J2-0 | **measurement** | property of the built rig; not analytically derivable. Record left blank → engine returns `INCONCLUSIVE`. |
| peak vertical / lateral | J2-1 | analysis (bound) | rail-only coupling path; bound ≪ gate |
| miniature move / tip | J2-1 | analysis (bound) | rail end-rotation bound |
| seam step | J2-2 | analysis | geometry + load-fit; analytically computable |
| cumulative drift (100 cyc) | J2-3 | **measurement** | wear/dust/tribology; cannot be bounded tightly |
| regional clear+settle | J2-4 | analysis (screen) | `reliability.py` timing model, perfect-scaling benefit of the doubt |
| stiction release force | J2-1 | **measurement** | tribology |

## Engine verdict

`isolation_rig_runner.py` returns **INCONCLUSIVE** for each tile: every
analytically boundable gate passes, but **J2-0 rig qualification is missing** by
design. That is the honest result: the isolation *concept* is analytically
sound, but the rig's own noise floor (and creep) are physical facts an analysis
cannot supply.

## Residual uncertainty (vs a physical rig)

This is **not a measurement**. The bounds assume rigid holders and isotropic PLA
(FDM is anisotropic); they cannot see stiction release, wear, dust, creep, or
the real rig noise floor. See `../PRINTABILITY_REPORT.md` and
`../check_fixture.py` for the fixture mesh/render validation (OpenSCAD render
runs in the CI `j2-cad-render` job; reported `SKIP` in environments without
OpenSCAD).
