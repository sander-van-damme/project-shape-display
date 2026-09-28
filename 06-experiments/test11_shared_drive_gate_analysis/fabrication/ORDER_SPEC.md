# T11-A external print-service order spec (submission-ready)

**Issue:** [DND-26](/DND/issues/DND-26) · **Evidence class:** CALCULATED
pre-flight over CAD STLs. **Nothing here has been printed or measured.**

This is the package a print vendor needs to quote and produce the T11-A
selector fan-out fit coupon. It exists because the Fabricator container has no
reachable printer host, no slicer binary and no serial/USB path — see
[`FABRICATION_PATH.md`](FABRICATION_PATH.md) for the raw discovery evidence.
The CEO owns the purchase decision; the Fabricator owns making these files
submission-ready.

## Files to send (all already in the repo)

Branch: `fab/dnd26-fabrication-package`, directory
`06-experiments/test11_shared_drive_gate_analysis/`.

| File | Qty | Process | Purpose |
|---|---|---|---|
| `coupon_assembled.stl` | 1 | 0.4 mm nozzle / 0.12 mm layer (PLA) | A1 — baseline fit + web survival |
| `coupon_finger.stl` | 1 | 0.4 mm / 0.12 mm | A2 — notch/pivot definition |
| `coupon_bank.stl` | 1 | 0.4 mm / 0.12 mm | A3 — land definition |
| `coupon_assembled.stl` | 1 | 0.2 mm / 0.08 mm | A4 — fallback if A1 webs fuse |

Recommended to order **A1–A3 first** (baseline). Order A4 only if the measured
M1/M2 gates fail at 0.4 mm (see `T11A_PRINT_PROTOCOL.md`). Optionally order 3×
of each for repeatability; total material is small.

## Material / process / tolerance

- **Material:** PLA, any opaque color (natural or black gives best caliper
  contrast). No special filament required.
- **Machine:** Bambu Lab X1C equivalent, 0.4 mm hardened nozzle for A1–A3,
  0.2 mm nozzle for A4. Parts fit a 256 × 256 × 256 mm bed with huge margin.
- **Layer:** 0.12 mm (A1–A3), 0.08 mm (A4). **Wall/perimeter count: 3.**
  Top/bottom shells: 5. Infill: 15 % gyroid. **No supports** (all parts print
  flat; the finger/bank are small columns).
- **Critical tolerances (these are the gates, not cosmetic):**
  - minimum web between adjacent fingers **≥ 0.20 mm** (M1),
  - selector notch clear opening **≥ 0.40 mm** (M2),
  - finger pivots must be **free** after print (no fusion, no hand fitting) (M3),
  - 4-plane bank lands present, toe reaches land (M4),
  - lateral bank-to-bank clearance **> 0.20 mm** at 5.08 mm pitch (M5),
  - assembled bbox ≤ 25.4 × 25.4 × 20 mm per 2×4 area (M6).

Ask the vendor to **not scale the geometry** and **not auto-generate supports**.
If a vendor's DfM reduces a web below 0.20 mm, that is a hard rejection of the
quote — the whole coupon exists to prove those webs.

## Estimated cost / lead-time inputs (CALCULATED bounds)

From `order_spec.json` (analytic pre-flight, replace with the vendor's quote):

| Run | Part | Process | Layers | Est. filament | Est. time |
|---|---|---|---|---|---|
| A1 | coupon_assembled | 0.4/0.12 | 38 | 2.92 g | 6–15 min |
| A2 | coupon_finger | 0.4/0.12 | 9 | 0.03 g | < 1 min |
| A3 | coupon_bank | 0.4/0.12 | 23 | 0.13 g | < 1 min |
| A4 | coupon_assembled | 0.2/0.08 | 57 | 2.92 g | 9–23 min |

- **Total material (A1–A4): ≈ 6.0 g PLA.** Total machine time ≈ 15–39 min.
- At typical EU/US on-demand rates this is a **single-digit-CAD to low-€20
  quote per part**, plus fixed handling/shipping. Shipping 2–5 business days.
- This is well within the project's component budget and is the cheapest
  discriminating test in the whole T11 family.

## Return path

Vendor ships the physical parts to the project's designated address (owner:
CEO). On arrival, the Fabricator records DIMENSIONS only from calipers/photos
per `T11A_PRINT_PROTOCOL.md` and fills `runs/t11a_measurements.csv`. The scoring
engine `t11a_fit_check.py` then emits the S3 disposition.

## What this spec does NOT claim

- It is not a slicer result; times are analytic bounds for RFQ costing.
- It is not a print; no physical coupon exists yet.
- It is not a pass. Only measured M1–M6 rows can move the S3 disposition off
  `INCONCLUSIVE_RUN_A4`.
