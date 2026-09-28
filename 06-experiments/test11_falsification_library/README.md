# Test11 — falsification library and shared isolation rig

**Status: analytical + CAD + protocol. Nothing is printed or measured.**
This test exists to be the project's adversarial layer: it tries to *kill*
survivors S1–S5 cheaply, and it defines the one physical protocol that
discriminates them.

## Engineering questions

1. For each survivor, what is the **cheapest experiment that can reject it**,
   with explicit pass/fail gates and cycle counts? (`falsification_register.csv`)
2. How much isolation is enough for a regional reveal, and does tile size
   change the answer? (`isolation_rig_protocol.md`, research question Q5)
3. Does per-cell unreliability make a 6400-cell board hopeless, and what does a
   small coupon actually prove? (`reliability.py`, `checks.py`)
4. Can the printed process hold the clearances every cell needs?
   (`CROSS-B` register row)

## What is in this folder

| Artifact | Type | Purpose |
|---|---|---|
| [`reliability.py`](reliability.py) | calculation | per-cell→board reliability, regional scaling, return margin, tolerance yield |
| [`checks.py`](checks.py) | regression | pins the project's own headline numbers so the adversarial story cannot drift |
| [`falsification_register.csv`](falsification_register.csv) | register | one row per claim: cheapest rejection test, gates, cycles, consequences |
| [`make_register.py`](make_register.py) | generator | keeps the register CSV valid and field-count checked |
| [`isolation_rig_protocol.md`](isolation_rig_protocol.md) | protocol | the buildable Q5 rig: layout, parts, procedure, gates |
| [`measurement_plan.md`](measurement_plan.md) | decision rules | turns peak motion / force / time into a mechanical GO-KILL-INCONCLUSIVE per survivor |
| [`isolation_rig_runner.py`](isolation_rig_runner.py) | runnable test | gate engine over the J2 table; `--selftest` exercises every gate with no hardware, `--validate` checks the schema |
| [`check_fixture.py`](check_fixture.py) | runnable test | fixture geometry gate: pitch, X1C bed fit, plate layout, protocol floors |
| [`j2_isolation_rig.scad`](j2_isolation_rig.scad) | CAD | holder, shared base rail, indicator bracket, miniature tray, one-plate print layout |
| [`printability_slice_check.py`](printability_slice_check.py) | slicer-level check | rasterised 0.20 mm slice simulation: per-layer wall thickness, overhangs, first-layer footprint, socket openness (needs numpy + scipy; not in stdlib-only CI) |
| [`PRINTABILITY_REPORT.md`](PRINTABILITY_REPORT.md) | report | [DND-16] J2 printability de-risk: verdict PRINT-READY PENDING HARDWARE |
| [`printability_slice_report.json`](printability_slice_report.json) | evidence | machine-readable output of the slice check over the DND-14 STL bundle |
| [`measurements/isolation.csv`](measurements/isolation.csv) | blank record | the J2 measurement table; ships header-only |

> **CAD render status (2026-09-28):** all six J2 parts were rendered to STL with
> OpenSCAD 2021.01; rendered bounding boxes match the declared geometry. A
> functional bug was found and fixed: the holder's fixture socket had been buried
> inside the frame's solid floor and is now a real open pocket.
> `check_fixture.py` now renders every part and probes the socket, so the bug
> cannot return silently. This is **CAD, not a print**.
>
> **Printability status (2026-09-28, [DND-16]):** a rasterised 0.20 mm slice
> simulation over the STL bundle finds no print-blocking feature: min real wall
> 2.0 mm, no sub-1.2 mm features, plate gaps 6.0 mm, bed fit 131.6 × 128.2 mm,
> socket open with a 2.0 mm floor and no internal bridge. Verdict
> **PRINT-READY PENDING HARDWARE**. Two non-blocking corrections: `chamfer_mm`
> is declared but unused, and the "no overhangs > 45°" claim does not hold for the
> indicator bracket's horizontal stem hole (self-supporting at Ø8.2 mm). This is
> a slice **calculation**, not a slicer binary and not a print. See
> [`PRINTABILITY_REPORT.md`](PRINTABILITY_REPORT.md).

## Core adversarial findings (calculation, not measurement)

### A 6-cell demo proves almost nothing

At an independent per-cell error rate of **0.01%**, the probability all 6400
cells are correct is only **52.7%**. At 0.001% it is 93.8%. A six-cell coupon is
99.94% perfect *even at the failing 0.01% rate*. Therefore:

- a clean six-cell reset is **not evidence** of board reliability;
- a 99% perfect-map goal needs **q ≤ 1.57×10⁻⁶** per cell, which needs about
  **1.91 million zero-failure independent trials** for a one-sided 95% bound;
- any survivor that cannot show counted failures at that scale must add
  **detection + bounded repair**, or it fails the product reliability gate.

These are exactly the figures already in
[Test09](../../06-experiments/test09_test08_validation/README.md); `checks.py`
re-derives them so they cannot be silently weakened.

### Regional updates are the real discriminator

The product requirement is that an untouched, loaded region is not disturbed.
S1, S2 and S4 all **assume** this. The register's `S2-B`, `S4-A` and `CROSS-D`
rows and the J2 rig turn it into a measured gate: peak neighbour motion
≤ 0.10 mm, miniature not moved/tilted, seam ≤ 0.25 mm, cumulative drift over
100 cycles ≤ 0.20 mm. The protocol gives regional timing the benefit of the
doubt (perfect proportional scaling) before any measurement.

### Return margin is thin and unmeasured

At Test09's assumed inputs, a solid 2.069 g column has 20.29 mN of gravity
against an assumed 5 mN drag — a 4.06× ratio, but only **15.29 mN** of headroom
before the column stops returning. A hollow 0.997 g column is already below the
project's own 2× rule. Dust, warping and lateral load are unmodeled. The
`CROSS-C` contamination challenge is the cheapest way to find out.

### Process variation is a board-level gate

A 99.99% per-cell pass *still* loses ~47% of boards at 6400 cells
(`board_yield`). The three-batch, centre-and-corner coupon gate (`CROSS-B`) is
the only way to bound the real print sigma; a nominal CAD clearance is not
evidence.

## Verdicts recorded by this test

- **S1–S4**: no survivor is killed by this analytical work alone, because all
  of them are unbuilt. Each now has a named cheapest rejection test and explicit
  gates. Their evidence status is `NOT_STARTED`.
- **S5**: already the most specified, and already has Test09's Stage A–E plan.
  This test does not duplicate it; it adds the reliability and isolation framing
  Test09's physical plan lacks. The cam-buckling 5 N abuse gate remains **not
  passed** even in the ideal model (Test08: ~4.96 N).
- **No candidate is promoted** to [`08-current-design/`](../../08-current-design/).

## Reproduce

```bash
python 06-experiments/test11_falsification_library/checks.py
python 06-experiments/test11_falsification_library/make_register.py
# runnable protocol-and-fixture tests (no hardware required):
python 06-experiments/test11_falsification_library/isolation_rig_runner.py --validate
python 06-experiments/test11_falsification_library/isolation_rig_runner.py --selftest
python 06-experiments/test11_falsification_library/check_fixture.py
# score a real measurement table once a run exists:
python 06-experiments/test11_falsification_library/isolation_rig_runner.py \
    --input 06-experiments/test11_falsification_library/measurements/isolation.csv
```

All use the Python standard library only. `checks.py`, the runner's
`--validate`/`--selftest` modes and `check_fixture.py` are part of the CI
`engineering-checks` workflow. The runner's `--selftest` prints `SYNTHETIC`
rows: it proves the gate engine works, not that any survivor passes.

Optional CAD export needs OpenSCAD on PATH (absent in this agent environment,
so the fixture's parse/render step reports SKIPPED, never passed):

```bash
openscad -o /tmp/holder5.stl  -D tile=5  j2_isolation_rig.scad
openscad -o /tmp/holder10.stl -D tile=10 j2_isolation_rig.scad
openscad -o /tmp/rail.stl     -D part=\"base_rail\" j2_isolation_rig.scad
openscad -o /tmp/plate.stl    -D part=\"plate\" j2_isolation_rig.scad
```

## What the runnable tests do and do not prove

- `isolation_rig_runner.py --validate` checks the shipped measurement table has
  every field the gates read.
- `isolation_rig_runner.py --selftest` feeds **SYNTHETIC** rows through the
  engine and asserts each gate fires PASS/FAIL/INCONCLUSIVE as designed. It
  proves the gate engine is wired correctly. It is **not** a pass for any
  survivor.
- `check_fixture.py` checks the fixture's declared geometry (5.08 mm pitch,
  X1C bed fit, plate layout, protocol feature floors) and, when OpenSCAD is on
  PATH, renders every part and probes the holder's fixture socket for exposure.
  It is a **calculation + CAD render**, not a print.
- `isolation_rig_runner.py --input <run>.csv` is the only mode that scores
  MEASURED rows; it prints GO / KILL / INCONCLUSIVE per survivor and exits
  non-zero if anything is KILLed.

## Honesty statement

Every number in `reliability.py` is a **calculation from stated assumptions**.
The register's gates and the measurement plan's decision table are **proposed
thresholds**, not results. The J2 protocol and fixture are **unbuilt**. The
runner and fixture checks prove the *machinery* is self-consistent and that a
protocol can be applied mechanically; they prove nothing about hardware. The
physical run is owned by the CTO.

## Next action

Hand the J2 rig print set (`part = "plate"`) and the S5/Test09 Stage A fixture
to the CTO for fabrication on the X1C, run J2-0 (rig qualification) before any
survivor, then feed the dated run into
[`isolation_rig_runner.py`](isolation_rig_runner.py) to get the go/kill calls.
See [`isolation_rig_protocol.md`](isolation_rig_protocol.md#what-to-hand-to-the-cto)
and [`measurement_plan.md`](measurement_plan.md).
