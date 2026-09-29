<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-13 A1 coupon A/B/C build-readiness — CAD-ready physical handoff package

> **Evidence class: CAD + CALCULATION only** (DND-27). This note designs the
> coupons; it prints, purchases, and measures nothing. Nothing here is
> physical validation. S5-R and S6-LC are untouched. All existing gates stay
> green (verified below).

## Context

[SHA-7](sha7-a1-promotion-decision.md) gated A1 (architecture PROMOTED, build
MEASUREMENT-GATED on coupon A); [SHA-9](sha9-a1-gate-residuals-regional.md)
retired R5 (8-head-minimum design rule) and half-retired R6 (rigid-body /
geometry analytic; elastic half open). R1–R4 plus the elastic half of R6 are
measurement-only and unretireable analytically under DND-27. No further
analysis retires them — but the coupons themselves can be designed now, so the
physical handoff is ready if DND-27 ever lifts. That is what this note does.

Gate script: `08-integrated-designs/a1-reliability-first/analysis/a1_coupon_readiness.py`
(`--gate`: 32/32). It asserts the kill lines reproduce from the record, the
coupon geometry fits the X1C bed at the provisional FDM rules, and the three
coupon SCAD files carry the handoff markers.

## Coupon A — single cell at true pitch (gates the build)

**Retires:** R1 (snap force) + R4 (read contrast). The build stays
MEASUREMENT-GATED until coupon A passes.

**Geometry deltas** (`scad/a1_coupon_a_single_cell.scad`; cell parts reused
unchanged from `a1_binary_latch_cell.scad`):

- Base plate 30 × 30 × 3.0 mm with a centred socket `BODY + 2·CLEAR`
  (3.60 + 0.40) placing one true-pitch cell station.
- Force-gauge mount post (Ø6 × 12 mm), axis on the latch toe contact line.
- Reader bracket holding the aperture plane at `Z_FLAG_TOP + 1.8 mm`
  (44.8 mm): the adopted DND-115 fixed standoff / 0.44 mm aperture.
- All new features observe the provisional rules (≥0.44 mm feature,
  ≥0.88 mm wall); the coupon fits the X1C 256 mm bed.

**Procedure + instruments:**

- Toggle-force: push-pull force gauge (0–20 N, ±0.05 N) on the writer
  contact; record peak snap force per toggle. Reader at the fixed standoff
  (630 nm LED + photodiode, 50 µs integration budget per DND-111).
- Read-contrast: 30 reads per state at the fixed standoff; compute on/off
  return ratio (ideal and crosstalk-corrected).

**Sample size / pass-fail:**

- Toggle: n = 30 snaps across ≥3 prints (10 each); **PASS iff sample mean
  ≤ 7.14 N** (R1 kill: writer 10 N usable can no longer toggle the worst
  cell of a ±40 % spread band above this mean) **and no single snap > 10 N**.
- Contrast: **PASS iff on/off ≥ 2×** both ideal and crosstalk-corrected
  (R4 kill: below 2× the reader cannot resolve one wrong cell in 6,400).

**Decision driven:** PASS lifts the build gate to coupon B; either kill
fails the program as drawn (redesign the writer force path or the
shutter/vane encoder, then re-coupon).

## Coupon B — 5×5 cycling rig, loaded untouched neighbour + miniature

**Retires:** R2 (hinge wear) + the elastic half of R6 (loaded-neighbour
motion, tip-over, wear drift). Geometry half of R6 is already analytic.

**Geometry deltas** (`scad/a1_coupon_b_5x5.scad`; 25 cells reused unchanged
at true 5.08 mm pitch, field 25.4 × 25.4 mm):

- Tile 40 × 40 × 3.0 mm with a 5×5 socket grid at true pitch.
- Centre cell (2,2) is the loaded untouched neighbour: dead-weight / spring
  seat applying the 3.27 N service load; miniature plinth (Ø30 × 2.0 mm)
  sized for a representative 28–35 mm figure base.
- Tile fits the X1C 256 mm bed.

**Procedure + instruments:**

- Cycle the 4 orthogonal neighbours of the loaded centre cell (toggle sweep
  equivalent to a 20×20 boundary reveal); the centre cell is never
  addressed. Dial indicator / LVDT (1 µm) on the centre column top for peak
  vertical/lateral motion and residual height error each 500 cycles, to
  5,000 cycles. Representative miniature stands on the centre cell
  throughout; note any tip-over. Inspect hinges for stall/fracture.

**Sample size / pass-fail:**

- One 5×5 tile (25 cells), 5,000 toggle cycles on the neighbour set.
- **PASS iff peak neighbour motion ≤ 0.10 mm** (Q5 proposal; modelled
  rigid-body is 0.00 mm), **no miniature tip-over**, **no hinge
  stall/fracture**, residual height error ≤ 0.10 mm.

**Decision driven:** PASS retires the elastic half of R6 and bounds R2 wear;
any kill drives a hinge/load-path redesign (larger pin, harder material, or
reduced service-load claim) and re-coupon.

## Coupon C — gantry registration over 406 mm (thermal/belt drift)

**Retires:** R3 (gantry registration over the full traverse).

**Geometry deltas** (`scad/a1_coupon_c_gantry.scad`; head aperture geometry
reused unchanged from `a1_reader_head.scad`):

- Spliced 406.4 mm reference rail: two 210 mm segments (each fits the 256 mm
  bed) + 40 × 20 × 3.0 mm splice plate with M3 holes.
- 9 measurement stations, every 10 cells (50.8 mm), with Ø3.2 mm datum
  sockets; head-carriage mock carries the 0.44 mm aperture bar.

**Procedure + instruments:**

- Command the carriage to each station, 3 full traverses; dial indicator /
  laser scale records positional repeatability vs commanded. Repeat after an
  ambient thermal soak (thermocouple logged) and under belt load vs
  unloaded (belt-stretch split). Calipers for splice datum check.

**Sample size / pass-fail:**

- 9 stations × 3 traverses × 2 thermal states.
- **PASS iff repeatability within ±0.264 mm** (secondary read concern) **and
  absolute drift < 2.54 mm** (half-pitch kill: at half-pitch drift the head
  addresses the wrong cell).

**Decision driven:** PASS retires R3; either kill drives a gantry redesign
(stiffer belt, thermal compensation, or shorter rail segments) and re-coupon.

## What stays open (stated, not hidden)

- Until a physical program runs these coupons, A1 remains architecture
  PROMOTED, build MEASUREMENT-GATED. This note changes no status; it makes
  the handoff ready.
- Residual uncertainty is unchanged from SHA-7/SHA-9: snap nominal 3.0 N is
  assumption-class; flap ρ ≈ 0.05 and aperture constants are
  assumption-class; hinge wear, registration, and elastic neighbour motion
  are measurement-only.

## Reproduce / verify

```bash
python 08-integrated-designs/a1-reliability-first/analysis/a1_coupon_readiness.py --gate   # 32/32 (new)
python 08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py --gate    # 13/13 (unchanged)
python 07-evidence-and-decisions/falsifier_sha7_a1_writepath_audit.py --gate               # 22/22 (unchanged)
python 07-evidence-and-decisions/falsifier_dnd112_checks.py --gate
python 07-evidence-and-decisions/falsifier_dnd114_checks.py --gate
python 07-evidence-and-decisions/falsifier_dnd115_checks.py --gate
git status --short  # S5-R (08-integrated-designs/s5r-*) and S6-LC untouched
```
