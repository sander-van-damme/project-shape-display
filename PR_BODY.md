# Test11 — S3/S4 printable selector fan-out coupon at final 5.08 mm pitch

## What changed
- Adds `06-experiments/test11_selector_coupon/`: stdlib analytical model, seven
  falsifiable PASS/FAIL gates, an OpenSCAD 2x4 latch cluster at final 5.08 mm pitch,
  a measurement register (blank), and a results summary.
- Updates `04-architecture-candidates/README.md`, `05-research-questions/README.md`,
  `07-evidence-and-decisions/README.md` with the calculated selector-fan-out bounds.
- Adds `.github/workflows/open-pr.yml` (reusable Actions-token PR opener).

## Engineering question
Can the S3/S4 shared-drive family get 320–400 *printable* per-column selectors —
a latch that clicks one level per shared stroke and holds load passively — at the
final 5.08 mm pitch, or does the pitch kill every pitch-resident selector?

## Evidence produced (calculated / CAD only — no physical measurement claimed)
- `coupon_geometry.py`: JSON model of row-band budget, radial blade overreach,
  shared-stroke partition, actual tooth overlap, retaining-face shear, per-column
  gate-bus timing/current.
- `checks.py`: 7 gates; **4 PASS, 3 FAIL**.
  - PASS: printable wall band; shared stroke = 25% of 40 mm (4 strokes, independent
    of column count); actual engaged tooth overlap 0.80 mm; retaining-face shear
    8.3 MPa at 5 N abuse gate (PLA shear yield ~30–40 MPa ideal, edge stress
    concentration unmodelled).
  - FAIL: linear gate slot+walls need 1.60 mm vs 0.20 mm available band;
    one-blade rotary gate crosses 1.10 mm into the neighbour channel;
    one-per-column gate bus needs 0.72 s / 7.2 A vs the 0.60 s dwell.
- `selector_coupon.scad`: 2x4 latch cluster, interchangeable carriers, sliding gate,
  separate 5 N retention abuse tile.

## Assumptions
- Test09 body/clearance geometry (4.68 mm body, 0.10 mm clearance) unchanged.
- 80 columns per drive head; 5 ms solenoid/rotary gate toggle; 50 µs command pulse.
- 5 N retaining-face abuse load; PLA shear yield ~30–40 MPa ideal.
- Existing A_* constants in `coupon_geometry.py`; all listed in the JSON output.

## What ran
```
python 06-experiments/test11_selector_coupon/coupon_geometry.py   # exit 0
python 06-experiments/test11_selector_coupon/checks.py            # exit 0, 3/7 FAIL
```
OpenSCAD rendering is documented but not required for the checks.

## What passed / failed
- Passed: the printable latch body itself survives at pitch; the shared-stroke
  concept is structurally sound (25% of 40 mm, column-count-independent).
- Failed: the *command gate* at pitch. The linear and single-blade rotary gates are
  geometrically blocked; a one-per-column electronic gate bus misses the dwell and
  exceeds the current budget.

## What remains uncertain
- No physical measurement: `measurements/*.csv` registers are blank. Printed latch
  tooth engagement, creep, and edge stress concentration are analytic only.
- Survivor direction: an **axis-centred drum gate**, a magnetic/non-contacting gate,
  or a loaded mechanical register banked per row with a shorter protocol.
- OpenSCAD success is not slicer/fabrication/collision/physical validation.

## Next test
Cheapest rejection next: print the 2x4 `selector_coupon.scad` cluster and the 5 N
abuse tile, then measure (a) engaged tooth overlap under load, (b) whether an
axis-centred drum gate can be printed within the 0.20 mm band budget, and
(c) gate-bus timing/current with a real 5 ms actuator.
