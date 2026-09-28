# Test11 — selector fan-out coupon at final 5.08 mm pitch (S3/S4)

**Question:** can the S3/S4 shared-drive family get 320–400 *printable* per-column
selectors — a latch that clicks one level per shared stroke and holds the load
passively — or does the 5.08 mm pitch kill every pitch-resident selector?

**Answer so far: the printed latch body survives, but the *command gate* is the
killer at this pitch, and Test07's linear release blade cannot be re-pitched.**
Three calculated checks fail (see `results_summary.csv`). This is a design
result, not a bug: it is the cheapest possible rejection before any CAD/BOM.

This experiment combines two things that already exist in the repo:

- **Test07's sliding-gate latch** (`06-experiments/legacy/test07_5x5_grid/grid.scad`):
  a printable sawtooth rack + spring-returned blade that gains **one 5 mm tooth
  per push** and holds the miniature load. That is functionally a shared-drive
  selector, but at **8.5 mm pitch** and with no electronic gate.
- **Test09's driver + witness harness** (`06-experiments/test09_test08_validation/`):
  the motor/detent/coupling bench, the 5 N retaining-face abuse gate, and the
  blank `measurements/` registers. Test09 already flagged that *Test07's whole-row
  moving comb cannot preserve independent per-cell state*, which is exactly the
  gap a per-column selector must fill.

## Reproduce

Python 3.11+, standard library only:

```bash
python 06-experiments/test11_selector_coupon/coupon_geometry.py   # JSON model
python 06-experiments/test11_selector_coupon/checks.py            # PASS/FAIL gates
```

OpenSCAD 2021.01 (`openscad` on PATH) for the coupon STLs/renders:

```bash
openscad -o results/t11_cluster.stl   -D 'part="grid"'     06-experiments/test11_selector_coupon/selector_coupon.scad
openscad -o results/t11_carriers.stl  -D 'part="carriers"' 06-experiments/test11_selector_coupon/selector_coupon.scad
openscad -o results/t11_gate.stl      -D 'part="gate"'     06-experiments/test11_selector_coupon/selector_coupon.scad
openscad -o results/t11_plate.stl     -D 'part="plate"'    06-experiments/test11_selector_coupon/selector_coupon.scad
openscad -o results/t11_assembly.stl  -D 'part="assembly"' 06-experiments/test11_selector_coupon/selector_coupon.scad
```

`results/` is gitignored (Test09 convention). OpenSCAD success is not slicer,
fabrication, collision or physical validation.

## What is actually new here

Test09's multi-row screen said the shared family is conditional on a selector
below **$0.54** each including driver, and Test10 said bought selectors at scale
are hopeless. Test11 is the first artifact that pushes a *specific existing
printable latch* down to the final pitch and asks the three questions that decide
the family:

1. **Row-band budget.** At 5.08 mm pitch the inter-cell band is
   `5.08 − 4.68 − 2×0.10 = 0.20 mm` (Test09's body and clearance unchanged).
   A linear gate must slide the full row pitch (5.08 mm) to make one continuous
   slot channel, so Test07's linear blade is geometrically impossible. A
   printable slot plus two printable walls needs **1.60 mm**, roughly **8×**
   the whole band. → **FAIL**: linear gate blocked.

2. **Rotary gate reaches into the neighbour.** A one-blade rotary gate centred
   on the cell (Test07's finger is 1.2 mm long, advancing at radius 2.54 mm)
   sweeps out to `2.54 + 1.2 = 3.74 mm` from the cell centre. The neighbour
   channel begins at `2.54 − 0.10 = 2.44 mm`. The blade crosses **1.10 mm** into
   an occupied cell. → **FAIL**: any printed rotary gate must be axis-centred
   (drum gate) or non-contacting (magnetic), or the pitch must grow.

3. **One-per-column electronic gate bus.**
   If the gate is a small rotary actuator on a commanded 2-wire bus, a
   one-per-column gate at 5 ms toggle needs `80×(80/80)×5 ms + 80×79×50 µs
   ≈ 0.72 s` to address all 80 columns — more than the 0.60 s dwell, and 80
   gates draw **7.2 A** if energised together. → **FAIL**: address needs a
   *loaded* mechanical register banked per row, or an address protocol with a
   shorter toggle, or fewer columns per drive.

**What *does* pass:** the shared stroke is only **25% of 40 mm** (one tooth
pitch per level, 4 strokes), independent of column count — Test09's shared-stroke
assumption is structurally sound. The latch tooth shear area (`0.50 × 1.20 =
0.60 mm²`) gives **8.3 MPa** at the 5 N abuse gate, below ideal PLA shear yield,
but edge stress concentration and creep are unmodelled. And the actual engaged
overlap is **0.80 mm, not the intended 0.90 mm** because the 0.40 mm tooth-tip
recess eats 11% of it — engagement must be a designed *and measured* value.

## Coupon artifacts

| Part | File (after OpenSCAD) | Purpose |
|---|---|---|
| `grid` | cluster block | The 2×4 final-pitch lattice that holds carriers and the per-column gate slot. Print this first to see whether the band prints at all. |
| `carriers` | 8 interchangeable carriers | Printable sawtooth-rack columns; measure tooth pitch and land. |
| `gate` | sliding gate piece | Test07's blade re-derived for the thin band; the geometry under test. |
| `plate` | retention tile | Separate 5-level latch-tooth abuse coupon; push calibrated rods through the bores to measure slip/break/permanent set at 5 N. |
| `assembly` | cluster + carriers + gates | Engaged bench view; carriers must be printed separately so pitch is testable. |

## Physical-print plan (CAD, not yet printed)

- **Printer / material / orientation:** Bambu X1C, PLA baseline (PETG for the
  gate wear face), 0.4 mm nozzle, 0.12 mm layers. `grid` prints flat on its
  base; carriers print upright; the `plate` tile prints flat. Repeat the
  decisive fit on 0.2 mm nozzle / 0.08 mm layers.
- **Dimensions to measure:** actual inter-cell wall band, gate-slot opening,
  tooth pitch/land, actual engaged overlap (should be 0.80 mm nominal), and the
  force to slip the latch tooth at 5 N.
- **The measurement that closes the biggest assumption:** with the cluster
  printed, push a carrier up one level and load the engaged tooth to 5 N; if the
  tooth slips or the gate deflects before 5 N, the "0.6 mm² shear area" number is
  wrong and the whole passive-load-path claim for S3 fails at final pitch.
- **The single biggest unproven assumption this coupon retires:** *that a
  load-bearing latch can be printed in the 0.20 mm inter-cell band at 5.08 mm
  pitch.* The analytical answer is currently "not with a linear gate, and only
  with an axis-centred rotary gate" — the print is what turns that into evidence.

## Labeled evidence

| Claim | Label |
|---|---|
| 5.08 mm pitch, 4.68 mm body, 0.10 mm/side clearance, 40 mm stroke, 5 levels | **assumption** (from Test09 params) |
| inter-cell band 0.20 mm; slot+walls 1.60 mm; blade overreach 1.10 mm | **calculation** |
| shared stroke = 25% of 40 mm; 4 strokes | **calculation** |
| 0.80 mm actual overlap; 8.3 MPa shear at 5 N | **calculation** |
| 0.716 s / 7.2 A gate bus; $160 for 400 gates | **calculation / assumption** |
| X1C 256 mm, PLA, 0.4/0.2 mm nozzle | **sourced** (Test09 F1) |
| any printed part, force, overlap or slip measurement | **NOT MEASURED** |

## Consequence for the S3/S4 family

- The **passive latch body** is not the blocker; the **command gate** is.
  S3/S4 must fund either (a) a tiny *loaded mechanical register* per row so
  address energy is amortised (8–10 gates per 80-column row ⇒ 0.02 s class
  toggles are unnecessary), (b) an axis-centred **drum gate** at slight pitch
  growth, or (c) a **contactless** gate.
- **Test07 cannot be scaled to final pitch by parameter change alone.** Its
  linear release blade is re-pitch-blocked; a new gate topology is mandatory.
- **Next cheapest test after this coupon:** a 2×4 *axis-centred drum gate* strip
  printed at 5.08 mm pitch with the Test09 driver, measuring per-column toggle
  force, loaded dwell, leakage between adjacent columns, and whether a bank of
  8 gates on one drive can toggle within a fraction of the 0.60 s dwell.

## Scope / non-goals

This coupon does **not** include the command gate, the moving drive bar, the
46.4 mm vertical stroke, the platen, or the full row band. It isolates one
decisive subsystem. It is not a build authorization and does not change S3/S4's
"drop until quantified" status in `04-architecture-candidates/`.
