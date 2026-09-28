# T11-A run records

This directory holds the **dated, human-entered** T11-A print/measurement records.
It is deliberately separate from any generated `results/` output: these rows are
the only place a real instrument reading may live, and a row is invalid unless a
physical coupon was printed and measured.

## Files

| File | Purpose |
|---|---|
| `t11a_measurements.csv` | one row per print run (A1-A4, repeats appended). Blank until printed. |
| `t11a_<YYYY-MM-DD>_<run>.md` | optional per-run narrative: photos, slicer project, anomalies |

## How to fill and score

1. Print A1-A3 on 0.4 mm / 0.12 mm PLA; print A4 on 0.2 mm / 0.08 mm only if A1
   webs fuse. Record `slicer_project`, `filament_lot`, `nozzle_mm`, `layer_mm`.
2. Measure M1-M6 exactly as in `../T11A_PRINT_PROTOCOL.md`, with instrument id
   and uncertainty. Convert booleans to `yes`/`no` in `M3_pivot` and
   `M4_land_present`.
3. Score the table with the fit-check engine:

   ```bash
   python ../t11a_fit_check.py --validate
   python ../t11a_fit_check.py --input t11a_measurements.csv
   python ../t11a_fit_check.py --input t11a_measurements.csv --json
   ```

   The engine applies the M1-M6 pass/kill gates and the protocol decision tree
   across the 0.4 mm baseline and the 0.2 mm fallback, emitting one of:
   `S3_DENSITY_PRINTABLE`, `S3_REQUIRES_FINE_NOZZLE`,
   `REJECT_S3_4ROW_DROP_TO_2_3`, or `INCONCLUSIVE_RUN_A4`.

## Status

**No row is filled. Nothing has been printed.** The coupon STLs and this scaffold
are a fabrication package; there is no physical T11-A measurement yet. Do not
infer a pass from the calculated `--predict` values (M1 web ~0.47 mm, M5 ~3.48 mm)
— those are geometry, not print results.
