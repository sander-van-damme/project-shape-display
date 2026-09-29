# DND-118: independent falsifier audit of the DND-115 state-encoding shutter

## What changed

- **New** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py` — a stdlib-only,
  default-deny checker (12 attacks, `--gate`) that recomputes every DND-115 number from the
  placed CAD constants and first principles. It imports **nothing** from `a1_writer_rate.py` and
  does **not** trust the CTO-authored `falsifier_dnd115_checks.py`.
- **New** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.md` — the audit register.
- **Corrected** the DND-115 section of `07-evidence-and-decisions/README.md` with the audit
  caveats and a new DND-118 entry.
- **New CI step** (`.github/workflows/ci.yml`) runs the audit as a **printed report** (no
  `--gate`) so `main` stays green while the correction is tracked.

## Engineering question

Does the DND-115 **state-encoding shutter** genuinely close the A1 read/verify axis at
CAD + calculation — i.e. do the decisive numbers (on/off return ratio, swept clearances, the
1.8 mm standoff revision) reproduce independently, and is the closure statement honest?

## Evidence produced (CALCULATION + CAD only)

**Reproduced from the placed CAD + first principles (no CTO summary imported):**

- Hidden occlusion **100%** of the 1.405 mm spot; visible clearance **0%**; on/off **7.72×**
  (gate 2×).
- Reflective target frame-fixed (**Δz = 0**); flap is an absorber (ρ = 0.05).
- Swept envelope: neighbour **0.280 mm**, own column **3.420 mm**, aperture **0.810 mm**.
- Claim 5 reproduces: 1.0 mm standoff infeasible (−0.190 mm worst case); 1.8 mm feasible
  (+0.610 mm).
- Printability: min feature 0.44 mm (1 line), committed STL watertight.
- **Angular robustness:** hidden coverage stays 1.000 for flap tilt 0–20°; visible state stays
  clear for crank 90–75° — the states are independent of the schematic linkage within a wide band.

**Falsified / downgraded (four FAILs; none a geometry collision):**

- **A5/A6 (crosstalk):** the ADR's "neighbour top is off-beam" is **false** — the coaxial 15°
  cone reaches the neighbour near edge by 0.231 mm. Including the state-invariant neighbour term
  drops the on/off ratio **7.72× → 6.37×** — **still above the 2× gate** — but the number was
  **reported and never gated** (`contrast_passes` ignores it).
- **A7 (framing):** "absorber Δz 0.55 mm inside ±1 mm DoF" is **vacuous** — the DoF budget is a
  *target* concept; the target is frame-fixed and the absorber term is 7.7× below the vane term.
- **A9 (method):** `shutter_tolerance_mc()` pins the aperture plane to the *nominal* vane top, so
  `aperture_clearance` can never fail. A corrected re-run with an explicit aperture tolerance
  (±0.10 / ±0.20 mm) still passes (+0.442 / +0.347 mm): the design survives, the as-written MC
  does not demonstrate it.

## Assumptions

Assumption-class, unmeasured (as in DND-115): flap reflectance 0.05, standoff 1.8 mm, aperture
0.44 mm, printed tolerances, LED/PD optical constants. Measurement-only (DND-27): linkage
force/friction/wear over 6,400 cycles. No print, purchase, or measurement; no board contact
(DND-32).

## Tests / gates run

- `python 07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py` → report, **NOT CLEAN**
  by design (4 fails, documented).
- `falsifier_dnd115_checks.py --gate` → exit 0; `falsifier_dnd114_checks.py --gate` → exit 0;
  `reliability_mask_checks.py` → 75/75; `a1_writer_rate.py` → exit 0.
- CI YAML validated; new step is report-only.

## What passed / failed

**Passed:** core mechanism geometry, contrast ratio, standoff revision, printability, angular
robustness. **Failed:** the crosstalk/off-beam wording and gating, the absorber-DoF framing, and
the MC aperture path.

## Remaining uncertain / next test

The mechanism **survives**; the **closure statement is over-claimed**. Recommended: a CTO
follow-up to correct/downgrade A5/A6/A7/A9 in the ADR and `a1_writer_rate.py` (no geometry
change), after which the report step can become a hard gate. No physical coupon is justified by
this audit alone; a single-cell A1 coupon with a real LED/PD pair is the cheapest experiment that
can falsify the assumption-class reflectance combination, and is a physical handoff (DND-27).
