# DND-4: designed pivot clearance closes the S3 selector fan-out gate analytically

## What changed

- `06-experiments/test11_shared_drive_gate_analysis/selector_fanout_coupon.scad`:
  the finger pivot is redesigned from a printed-in-place boss to a **designed
  journal fit**. Added `PIVOT_CLR = 0.20 mm/side`, `PIVOT_SOCKET_D = 1.20 mm`,
  and cut base socket bores so each finger boss journals in a defined socket.
- `.../make_coupon_stl.py`: parity update — emits the socket-post marker at the
  design diameter (this stdlib generator has no boolean kernel).
- `.../analytic/t11a_analytic_gate.py`: models the boss and socket as separate
  tolerance contributors; **M3 (pivot free) is now a designed fit** and is
  reported `yes`/`no` instead of left blank. Adds `ANALYTIC_PASS_DIMENSIONAL_M3_RESOLVED`
  and `ANALYTIC_FAIL_PIVOT_INTERFERENCE` verdicts.
- Regenerated: `analytic/runs/t11a_analytic_measurements.csv`, the coupon STLs.
- Docs: `04-architecture-candidates/README.md`, the T11-A `README.md`,
  `T11A_PRINT_PROTOCOL.md`, `analytic/README.md`, `rejection_tests.json`.

## Engineering question

Can the S3 selector fan-out gate (T11-A) reach a real disposition
**analytically**, under board policy [DND-27] (no physical print test), instead
of stalling on an unmodelled slicer unknown?

Previously: M3 was unmodelled because the pivot printed in place with no designed
clearance, so `t11a_fit_check.py` returned `INCONCLUSIVE_RUN_A4`.

## Evidence produced (calculated / CAD — no physical measurement claimed)

- The designed journal clearance gives a **0.40 mm diametral free play**.
- Worst case (boss high, socket low, ±0.06 each) leaves **+0.08 mm** margin over
  the 0.20 mm free-gap floor.
- Monte Carlo (200k, sigma = half_range/√3): M3 pass fraction **0.99998** (the
  tail is normal-distribution beyond the bounded ±0.06 tolerance, not a design
  boundary).
- Feeding the analytic record to the CI-tested engine now returns
  **`S3_DENSITY_PRINTABLE`** on the `A1-ANALYTIC` 0.4 mm baseline row, with the
  explicit `[ANALYTIC SCREEN, NOT A PRINT]` warning. M1/M2/M5/M6 analytic PASS.

## Reproduce

```bash
cd 06-experiments/test11_shared_drive_gate_analysis
python model.py && python checks.py && python coupon_geometry.py
python make_coupon_stl.py && python verify_coupon_stl.py
python t11a_fit_check.py --selftest && python t11a_fit_check.py --validate
python analytic/t11a_analytic_gate.py --selftest
python analytic/t11a_analytic_gate.py --emit-record
python t11a_fit_check.py --input analytic/runs/t11a_analytic_measurements.csv
```

## Passed / failed

- PASS (local): the whole CI-run script set for this folder, including the new
  analytic gate selftest and the engine on the analytic record.
- Remaining thin term: **M4 land reach** is −0.05 mm worst case (the ±0.20 mm
  protocol window is itself the bound); MC pass fraction 0.9083. This is
  unchanged by the pivot work and is the next analytic item.

## Assumptions

- FDM tolerance for the boss and socket bores: ±0.06 mm half-range (FDM XY class).
- Free-gap floor 0.20 mm at 0.4 mm nozzle, 0.15 mm at 0.2 mm (assumption).
- `PIVOT_CLR` is a CAD-set dimension; 0.40 mm diametral also clears the 0.4 mm
  slot rule.

## What remains uncertain / next test

- This is **not a print**. The model cannot see fusion, stringing, layer
  adhesion, elephant-foot, warp, or how the printed boss/socket pair deviates
  from the modelled tolerance class. That stays a **permanent qualitative risk**
  per ADR-001 §5.2.
- Next analytic step: close the M4 land-reach term, then T11-B loaded dwell.

## Links

- Source issue: DND-4 (S3/S4 family; Step-4 selector/register fan-out gate).
- Policy: [DND-27] no physical print tests; analytic/simulation/CAD only.
- Convergence: ADR-001 / convergence-plan §3 Step 4.
