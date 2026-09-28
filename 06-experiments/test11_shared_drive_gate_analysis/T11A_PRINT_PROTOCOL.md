# T11-A — selector fan-out fit coupon: print and measurement protocol

**Purpose.** The cheapest test that can reject S3. It answers one question: can
four independently rockable selector fingers and a 4-plane cam bank fit inside
one 5.08 mm cell band and print cleanly on the Bambu Lab X1C?

**This has not been printed.** Everything below is a protocol. Fill the record
with measured numbers or leave it blank; do not infer a pass from CAD.

> **Status (DND-21).** The print/measure half of this protocol cannot be executed
> by any agent in this company: there is no 3D printer, slicer host, or
> fabrication bridge reachable from the agent runtime. What ships here is the
> complete, runnable **fabrication + scoring package** (STLs, run-record schema,
> gate engine). A physical A1–A4 print and caliper/microscope pass M1–M6 is still
> required to move S3 off `INCONCLUSIVE`; the gate engine will score it the moment
> the rows are entered.
>
> **Status update (DND-4, analytic).** Under board policy [DND-27](/DND/issues/DND-27)
> the physical pass cannot be run, so the analytic gate in
> [`analytic/`](analytic/README.md) is used instead. The pivot was changed from a
> printed-in-place boss (**no** designed clearance — M3 unresolvable) to a
> **designed journal fit** with `PIVOT_CLR = 0.20 mm` per side
> (`PIVOT_SOCKET_D = 1.20 mm`), so M3 is now an analytic quantity. Feeding the
> analytic record to `t11a_fit_check.py` returns **`S3_DENSITY_PRINTABLE`** on
> the 0.4 mm baseline with the explicit *analytic screen, not a print* warning.
> M1/M5/M6 are analytic passes; M4 land-reach is the remaining thin term
> (−0.05 mm worst case). This is still **not** a printed or measured result.

## Files

| File | What it is |
|---|---|
| `selector_fanout_coupon.scad` | readable parametric source (needs OpenSCAD) |
| `make_coupon_stl.py` | stdlib-only binary-STL generator for the same geometry |
| `verify_coupon_stl.py` | mesh/bounds check (not a slicer check) |
| `coupon_assembled.stl` | 2 columns × 4 rows frame + banks + fingers |
| `coupon_finger.stl` | one finger (notch present) |
| `coupon_bank.stl` | one 4-plane cam bank |
| `coupon_base.stl` | the open frame plate |

Regenerate:

```bash
python make_coupon_stl.py --part assembled
python verify_coupon_stl.py
```

**Run record and scoring.** Fill the dated table in
[`runs/t11a_measurements.csv`](runs/t11a_measurements.csv) (one row per print run)
and score it with the fit-check engine, which applies M1–M6 and the decision tree
below mechanically:

```bash
python t11a_fit_check.py --validate
python t11a_fit_check.py --input runs/t11a_measurements.csv
python t11a_fit_check.py --predict    # CALCULATED expected M1/M2/M5, not measured
python t11a_fit_check.py --selftest    # SYNTHETIC: exercises every gate branch
```

`runs/` holds human-entered measurements only; it is separate from any generated
`results/`. The engine emits one of `S3_DENSITY_PRINTABLE`,
`S3_REQUIRES_FINE_NOZZLE`, `REJECT_S3_4ROW_DROP_TO_2_3`, `INCONCLUSIVE_RUN_A4`.

## Print matrix

Print each part, then repeat the critical one at the finer nozzle. Record the
slicer project, filament lot and nozzle for every print.

| Run | Part | Nozzle | Layer | Goal |
|---|---|---|---|---|
| A1 | `coupon_assembled` | 0.4 mm | 0.12 mm | baseline fit + web survival |
| A2 | `coupon_finger` | 0.4 mm | 0.12 mm | notch/pivot definition |
| A3 | `coupon_bank` | 0.4 mm | 0.12 mm | land definition |
| A4 | `coupon_assembled` | 0.2 mm | 0.08 mm | fallback if A1 webs fuse |

Print the assembled coupon in the orientation implied by the STL (fingers
standing, pivot boss horizontal). Inspect actual sliced wall paths: a missing web
fails even if the STL is valid.

## Measurements

Instruments: caliper/micrometer resolving 0.01 mm, optical microscope or phone
macro for webs, 0.01 g balance (optional), and a straight edge.

| ID | Measurement | Pass | Kill |
|---|---|---|---|
| M1 | minimum web between adjacent fingers over all 4 rows | ≥ 0.20 mm | < 0.20 mm on any row |
| M2 | selector notch present and open (engaged fingers) | clear opening ≥ 0.40 mm | fused or < 0.40 mm on 0.4 mm nozzle; retry A4 |
| M3 | finger pivot free play after print, no hand fitting | rotates/bears under finger force | any fused pivot |
| M4 | bank land height vs finger toe (nominal 0.5 mm land) | toe reaches land across 4 rows | land missing or displaced > 0.2 mm |
| M5 | lateral clearance between bank OD and neighbour bank | > 0.20 mm | collision at 5.08 mm pitch |
| M6 | assembled bbox | ≤ 25.4 × 25.4 × 20 mm per 2×4 area | exceeds |

## Decision

- **PASS** (all M1–M6): S3 density is printable; proceed to T11-B (loaded
  engage/write/disengage dwell) before any head CAD or drive purchase.
- **FAIL on M1/M2 at 0.4 mm, pass at 0.2 mm:** S3 requires the 0.2 mm nozzle and
  loses process margin; document as a design constraint and re-run the timing
  with the slower fine-nozzle print cost.
- **FAIL at both nozzles:** reject S3 at 4 rows/station. Drop to 2–3 rows and
  re-pay the timing (see `model.py` station budget: 27 or 40 stations).

## Record

Copy this block into a dated run directory; keep raw photos and slicer projects.

```text
run_id, part, nozzle_mm, layer_mm, filament_lot, M1_web_mm, M2_notch_mm,
M3_pivot, M4_land_mm, M5_clearance_mm, M6_bbox_mm, verdict, operator, date
```
