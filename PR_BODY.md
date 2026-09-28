# DND-26 — T11-A fabrication path + submission-ready external order package

Fabricator deliverable for [DND-26](/DND/issues/DND-26). Stacked on the T11-A
gate-engine branch (`feat/dnd21-t11a-fit-verdict`); review the last commit only.

## What changed

Adds `06-experiments/test11_shared_drive_gate_analysis/fabrication/`:

- `order_spec.py` — stdlib-only mesh/watertight/bed pre-flight plus an analytic
  RFQ estimator (layers, filament mass, print-time band). Not a slicer.
- `order_spec.json` — generated machine-readable spec for the four T11-A runs.
- `ORDER_SPEC.md` — vendor-ready process, quantity, and **tolerance** spec
  (the M1–M6 gates are the tolerances; no auto-supports, no rescaling).
- `FABRICATION_PATH.md` — the live probe evidence: no printer host, no slicer
  binary, no serial/USB, no reachable print service. Chosen path = external
  print service; purchase decision escalated to the CEO.
- `MEASUREMENT_RUNBOOK.md` — instrument session that turns a returned print into
  measured rows for `runs/t11a_measurements.csv`, then `t11a_fit_check.py`.

## Why this is the right increment

The issue's Step 1 asked to re-verify reachability (done, evidence committed) and
Step 2 named external print-service sourcing as the fallback when no host exists.
This PR makes the package submission-ready so the only remaining step is a spend
authorization that only the CEO can give.

## Evidence class

**CALCULATED.** No part is printed or measured by these files. The blank
`runs/t11a_measurements.csv` still scores `INCONCLUSIVE_RUN_A4`, which is the
correct, honest state until physical parts are measured.

## Verification

```bash
python3 06-experiments/test11_shared_drive_gate_analysis/fabrication/order_spec.py --validate
python3 06-experiments/test11_shared_drive_gate_analysis/fabrication/order_spec.py --write
python3 06-experiments/test11_shared_drive_gate_analysis/t11a_fit_check.py --validate
```

All three pass; `--validate` reports watertight meshes and X1C bed fit.
