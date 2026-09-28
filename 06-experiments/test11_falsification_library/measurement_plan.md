# J2 measurement plan — turning motion and force into a go/kill decision

**Status: PROPOSED PLAN. Nothing here has been printed or measured.** Every
threshold is a decision rule, not a result. The plan's job is to make each
survivor's fate a *mechanical* output of the numbers, so no one can call a
survivor alive on a good-looking video.

Companions:

- [`isolation_rig_protocol.md`](isolation_rig_protocol.md) — how to build and
  run the rig (J2-0 … J2-4).
- [`isolation_rig_runner.py`](isolation_rig_runner.py) — the gate engine that
  consumes the filled `measurements/isolation.csv` and prints GO / KILL /
  INCONCLUSIVE per survivor. `--selftest` exercises every gate without
  hardware; `--validate` checks the table schema.
- [`j2_isolation_rig.scad`](j2_isolation_rig.scad) — the print-ready fixture.
- [`check_fixture.py`](check_fixture.py) — fixture geometry gate before printing.

## The four quantities that decide everything

Every survivor rises or falls on the same four measured quantities:

| # | Quantity | Symbol | Instrument | Why it decides the survivor |
|---|---|---|---|---|
| 1 | Peak neighbour vertical displacement during a target reset | `peak_vertical_mm` | 0.01 mm dial indicator + 240 fps camera | This *is* regional isolation. If the untouched loaded tile moves, "regional update" is a fiction. |
| 2 | Peak neighbour lateral displacement | `peak_lateral_mm` | second dial indicator on the tile edge | Lateral creep is how a jam propagates and how a miniature walks off its square. |
| 3 | Miniature base movement / tipping | `miniature_move_mm`, `miniature_tip_mm` | fixed-datum video | The product is played on: if the figure moves or tips, the display failed even if the tile did not. |
| 4 | Return/force margin at the cell | drag vs weight, selection/holding force | force gauge ≤ 1 mN, calibrated masses | A cell that cannot return is not a height memory; a gate that opens under tabletop load is not a gate. |

Plus the slow-burn quantities that only repeated cycling reveals: `seam_step_mm`
(adjacent height step), `cumulative_drift_mm` (100-cycle creep) and
`regional_clear_settle_s` (regional timing).

## Decision table (mirrors `isolation_rig_runner.py`)

Lower is better on every gate. `≤ pass` is GO, `> fail` is KILL, in between is
INCONCLUSIVE and must be reported as such — never rounded into a pass.

| Gate | Field | Pass | Fail | Units | Protocol step |
|---|---|---|---|---|---|
| Rig noise floor | `rig_noise_mm` | ≤ 0.02 | > 0.02 | mm | J2-0 |
| Neighbour peak vertical | `peak_vertical_mm` | ≤ 0.10 | > 0.25 | mm | J2-1 |
| Neighbour peak lateral | `peak_lateral_mm` | ≤ 0.10 | > 0.25 | mm | J2-1 |
| Miniature base movement | `miniature_move_mm` | ≤ 0.50 | > 0.50 | mm | J2-1 |
| Miniature tipping (edge lift) | `miniature_tip_mm` | ≤ 0.50 | > 0.50 | mm | J2-1 |
| Seam step at max adjacent height | `seam_step_mm` | ≤ 0.25 | > 0.50 | mm | J2-2 |
| Cumulative drift over 100 cycles | `cumulative_drift_mm` | ≤ 0.20 | > 0.50 | mm | J2-3 |
| Regional clear+settle (5×5) | `regional_clear_settle_s` | ≤ 3.0 | ≥ 26.251 | s | J2-4 |
| Regional clear+settle (10×10) | `regional_clear_settle_s` | ≤ 5.0 | ≥ 26.251 | s | J2-4 |
| Regional clear+settle (20×20) | `regional_clear_settle_s` | ≤ 8.0 | ≥ 26.251 | s | J2-4 |

Repetition guards (enforced by the runner; a fail here is INCONCLUSIVE, not GO):

- J2-1 peak gates need **≥ 10 repeats**; the **max**, not the mean, is scored.
- J2-3 drift needs **≥ 100 exchange cycles** to mean anything.
- J2-0 rig qualification must be on the table, or every survivor is
  INCONCLUSIVE (never GO).

The timing fail line is the modelled full-map time (26.251 s from Test09). A
"regional" update as slow as a full reset is a fail by definition.

## From a survivor's verdict to the board (the reliability bridge)

A coupon verdict is *not* a board verdict. `reliability.py` and the runner's
`reliability_consequence()` convert counted failures into the board-level claim:

- q = failures / operations counted per channel;
- a **zero-failure** run reports the one-sided 95% upper bound
  `q ≤ 1 − 0.05^(1/n)`, which for n = 10 000 is ≈ 3.0×10⁻⁴;
- `P(perfect 6400-cell map) = (1 − q)⁶⁴⁰⁰`;
- the 99%-perfect-map budget is **q ≤ 1.57×10⁻⁶**, requiring ≈ **3.27×10⁴**
  zero-failure independent trials for a 95% one-sided bound;
- Test09's headline **≈ 1.91×10⁶** trials corresponds to the much tighter
  per-update rate q ≈ 2.69×10⁻⁸ that also survives *correlated* faults before
  the map is drawn — it is not the same q as the 1.57×10⁻⁶ budget above
  (see `checks.py::test_zero_failure_trials_formula`).

Worked consequences (CALCULATED, from `reliability.py`):

| Counted run | q used | P(perfect 6400-cell map) | Verdict |
|---|---|---|---|
| 6 cells, 1 clean reset | — | ~100% | **proves nothing** |
| 10 000 ops, 0 failures | 3.0×10⁻⁴ (95% bound) | 14.7% | still far from safe |
| 100 000 ops, 0 failures | 3.0×10⁻⁵ (95% bound) | 82.5% | approaching |
| 1 000 000 ops, 0 failures | 3.0×10⁻⁶ (95% bound) | 98.1% | near budget |
| 100 000 ops, 10 failures | 1.0×10⁻⁴ | 52.7% | **KILL** |

Rule: a survivor may only be called board-safe if its counted run bounds q at
or below 1.57×10⁻⁶, *or* it ships detection + bounded repair that converts
silent faults into repairable ones. A clean six-cell demo cannot do either.

## Per-survivor go/kill consequence

| Survivor | Cheapest test | GO means | KILL means |
|---|---|---|---|
| S1 threshold/ratchet | 2×5 strip, 500 cycles, J2 isolation | survives to a 10×10 coupon; mask writing becomes the next gate | rejected as a cell-density family |
| S2 planar tiles | 5×5 four-plane stack; J2 swap | survives to a 10×10 tile with a real writer | rejected as planar-memory family |
| S3 multi-row DMA | 2×4 head, 256 masks, one shared drive | survives to a larger head coupon; repriced BOM | rejected; shared-motion local-selection narrowed |
| S4 shared-bus tiles | two 2×4 tiles on one bus + forced jam | survives to a longer bus coupon | rejected; correlated-fault risk confirmed |
| S5 rotary stops | Test09 Stage A→B, J2 isolation | passive mechanism qualified; proceed to Stage C | rejected as specified geometry; do not buy 80 motors |

## Exact run record

Copy `measurements/isolation.csv` into a dated directory (never overwrite the
shipped blank). One row per timed reset/cycle sequence. Field meanings are in
the protocol; the runner reads these numeric fields:

`rig_noise_mm`, `peak_vertical_mm`, `peak_lateral_mm`, `miniature_move_mm`,
`miniature_tip_mm`, `seam_step_mm`, `cumulative_drift_mm`, `cycles`,
`regional_clear_settle_s`, plus `survivor`, `fixture_id`, `tile_size`.

Run the gates:

```bash
python isolation_rig_runner.py --input runs/2026-09-28/isolation.csv
python isolation_rig_runner.py --input runs/2026-09-28/isolation.csv --json
```

## What an agent cannot do here

Nothing in this plan can be *measured* by an agent in this environment: it needs
a printed rig, two 0.01 mm dial indicators, a ≤ 1 mN force gauge, calibrated
masses and a real miniature. The agent deliverable is the protocol, the fixture,
the runner and these decision rules. **The physical run is owned by the CTO** and
is the single highest-value missing evidence in the project.

## Honesty statement

- The gates are proposed thresholds, NOT results.
- `check_fixture.py` passing means the *declared geometry* is self-consistent
  and bed-fit; it is not a print or a CAD render (OpenSCAD is absent here, so
  the SCAD parse step reports SKIPPED).
- `isolation_rig_runner.py` passing its self-test means the gate engine works,
  using SYNTHETIC rows. It is not evidence about any survivor.
