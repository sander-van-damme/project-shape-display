# Fabricator measurement runbook — turning a printed coupon into measured rows

**Owner:** Fabricator · **Issue:** [DND-26](/DND/issues/DND-26) ·
**Engine:** `../t11a_fit_check.py` · **Protocol:** `../T11A_PRINT_PROTOCOL.md`

This runbook is what the Fabricator executes the moment physical parts exist
(printer host comes online, or external-service parts arrive from the CEO's
order). It exists so that a measurement session is mechanical and the S3
disposition is an output of instrument readings, never an inference from CAD.

## Instrument kit (record the ids in the CSV)

- caliper/micrometer resolving 0.01 mm (serial number as `instrument_ids`),
- phone macro or optical microscope for the M1 webs / M2 notch (photo id),
- straight edge for M6,
- optional 0.01 g balance.

## Session steps

1. **Photograph and label** each returned part with run id (A1–A4) before
   touching it.
2. **M1 — min web** between adjacent fingers over all 4 rows. Record the single
   **worst** (minimum) reading in mm.
3. **M2 — notch clear opening** on an engaged finger; if fused or < 0.40 mm on
   the 0.4 mm nozzle part, the protocol says retry with A4 (0.2 mm).
4. **M3 — pivot free?** Gently actuate; record `yes` if it rotates/bears under
   finger force without hand fitting, `no` if fused.
5. **M4 — land** height vs finger toe (nominal 0.5 mm). Record `M4_land_mm` and
   `M4_land_present` (`yes`/`no`).
6. **M5 — bank-to-bank clearance** at 5.08 mm pitch. Record the measured gap.
7. **M6 — assembled bbox** x/y/z per 2×4 area; pass if ≤ 25.4 × 25.4 × 20 mm.
8. **Then fill** `runs/t11a_measurements.csv` — one row per printed run. Convert
   booleans to `yes`/`no`. Keep raw photos and the slicer project alongside.

## Scoring

```bash
python3 ../t11a_fit_check.py --validate
python3 ../t11a_fit_check.py --input runs/t11a_measurements.csv
python3 ../t11a_fit_check.py --input runs/t11a_measurements.csv --json
```

The engine emits one of `S3_DENSITY_PRINTABLE`, `S3_REQUIRES_FINE_NOZZLE`,
`REJECT_S3_4ROW_DROP_TO_2_3`, or `INCONCLUSIVE_RUN_A4`. Commit the filled CSV +
photos on a branch and open a PR; report the disposition on DND-26.

## Evidence discipline (non-negotiable)

- A blank/partial row scores `INCONCLUSIVE` — never a pass. Do not hand-edit a
  row to force a disposition.
- Analytical values (`--predict`: web ≈ 0.47 mm, clearance ≈ 3.48 mm) are
  **CALCULATED**, not measured, and may not be copied into the CSV.
- Record failed prints and failed measurements as evidence, not as omissions.
- A submitted order is not a measured part until parts arrive and are measured.
