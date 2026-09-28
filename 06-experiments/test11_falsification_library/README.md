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
| [`j2_isolation_rig.scad`](j2_isolation_rig.scad) | CAD | holder, shared base rail, indicator bracket, miniature tray |
| [`measurements/isolation.csv`](measurements/isolation.csv) | blank record | the J2 measurement table; ships header-only |

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
```

Both use the Python standard library only. `checks.py` is part of the CI
`engineering-checks` workflow.

Optional CAD export needs OpenSCAD on PATH:

```bash
openscad -o /tmp/holder5.stl  -D tile=5  j2_isolation_rig.scad
openscad -o /tmp/holder10.stl -D tile=10 j2_isolation_rig.scad
openscad -o /tmp/rail.stl     -D part=\"base_rail\" j2_isolation_rig.scad
```

## Honesty statement

Every number in `reliability.py` is a **calculation from stated assumptions**.
The register's gates are **proposed thresholds**, not results. The J2 protocol
is **unbuilt**. A run of `checks.py` proves the arithmetic is self-consistent;
it proves nothing about hardware. The physical run is owned by the CTO.

## Next action

Hand the J2 rig print set and the S5/Test09 Stage A fixture to the CTO for
fabrication on the X1C, and run J2-0 (rig qualification) before any survivor.
See [`isolation_rig_protocol.md`](isolation_rig_protocol.md#what-to-hand-to-the-cto).
