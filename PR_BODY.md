# DND-21 — runnable T11-A fit-coupon gate engine + run-record scaffold

Stacked on the Test11 branch (`feat/test11-shared-drive-invention`, PR #12).
Review the **last commit only** (`797eb31`); the base commits belong to Test11.

## What changed

- Adds `06-experiments/test11_shared_drive_gate_analysis/t11a_fit_check.py`:
  the executable half of `T11A_PRINT_PROTOCOL.md`. Reads the run record, applies
  the M1–M6 pass/kill gates, and resolves the protocol decision tree across the
  0.4 mm baseline and the 0.2 mm fallback.
- Adds `runs/t11a_measurements.csv` (dated, human-entered; blank until printed)
  and `runs/README.md` (how to fill and score).
- Wires the engine's `--selftest`, `--validate` and `--predict` into CI.
- Updates the T11-A protocol and the experiment READMEs; records the blocker
  plainly instead of implying a print happened.

## Engineering question

DND-21 asks to **print and measure** the T11-A coupon. Can the agent fleet do
that, and if not, what is the most useful thing to ship instead?

## Evidence produced

- **Blocker (first-class):** no agent runtime reaches a 3D printer, slicer host,
  or fabrication bridge. The A1–A4 print and caliper/microscope M1–M6 pass are
  not executable here. This is the same wall documented for the sibling J2 rig
  task DND-14.
- **Shipped instead:** a gate engine that mechanically applies the protocol the
  moment a real measured row is entered, so the only remaining work is the
  physical print — no hand-scoring, no ambiguity.
  - `--selftest`: 12/12 synthetic branch checks pass (all-pass, coarse-web kill,
    fine-nozzle rescue, reject-both, inconclusive, notch fail, fused pivot,
    bank collision, bbox over, missing fields, packed bbox).
  - `--predict` (CALCULATED, not measured): M1 web 0.47 mm, M2 notch 0.55 mm,
    M5 clearance 3.48 mm, bbox 10.16 × 20.32 × 5.06 mm.
  - `--validate`: runs/ schema check.

Evidence labels: **CALCULATED + SYNTHETIC only.** No printed or measured T11-A
result exists. This change does **not** move S3 off INCONCLUSIVE.

## Passed / failed

- PASS: engine self-test, schema validation, all existing Test11 checks + STL
  verification, CI steps.
- Not attempted: the physical print and M1–M6 measurement (no hardware).

## Assumptions

- Gate thresholds and the decision tree are taken verbatim from
  `T11A_PRINT_PROTOCOL.md` (M1 web ≥0.20; M2 notch ≥0.40; M3 free pivot; M4 land
  0.5±0.2 mm; M5 clearance >0.20; M6 ≤25.4×25.4×20 mm).
- Station counts for the 2–3-row fallback (27/40) come from `model.py`.

## What remains uncertain / next test

- The physical A1–A4 print and M1–M6 measurement, followed by
  `python t11a_fit_check.py --input runs/t11a_measurements.csv`.
- If a printer becomes reachable, this is the first print to run; if not, the
  board must decide whether to accept a fabricated coupon from an external
  service or keep S3 gated on unprinted geometry.

## Links

- Source issue: DND-21
- Depends on: Test11 branch / PR #12 (DND-12)
- Sibling (same blocker): DND-14
