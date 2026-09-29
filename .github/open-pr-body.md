# DND-122: independent re-verification of the DND-121/DND-119 shutter corrections (A5/A6/A7/A9)

## What changed

- **Falsifier checker** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py`:
  two further independent attacks added:
  - **A13 (`adr_numbers_match_model`)** — imports the model live and checks that the
    numbers the ADR/README quote match what the code produces (headline on/off and
    the ±0.20 mm reader clearance). Guards the DND-112/DND-111 defect class.
  - **A14 (`mc_onoff_gate_includes_crosstalk`)** — checks whether the tolerance MC's
    own on/off gate carries the in-cone term that `contrast_passes` carries.
- **Falsifier register** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.md`:
  table extended to A13/A14; new "DND-122 re-verification note".

## Engineering question

Were the DND-118 audit findings (A5/A6/A7/A9) **correctly and honestly** applied —
mechanism *and* the numbers cited to support it — and may the DND-115 read axis be
cited as closed?

## Findings

- **The corrections are on main via [DND-119](/DND/issues/DND-119) (PR #95), not the
  DND-121 branch the ticket named.** DND-121 (`cto/dnd121-shutter-framing` @
  `9841736`) is a **parallel, never-merged** correction; main's DND-119 is the live
  artifact and does the same work: crosstalk modelled + gated, "off-beam" wording
  corrected to weakly-in-cone, absorber-DoF claim downgraded, MC aperture plane
  de-tautologised.
- **A5/A6/A7/A9 — PASS** on main, independently re-verified (cone radius 1.286 mm vs
  1.055 mm offset → in-cone by 0.231 mm; term gate; MC aperture ±0.10/±0.20 mm).
- **A13 — PASS on main.** The model gives headline ideal **7.72×** and
  crosstalk-corrected **6.37×**; the ADR carries the explicit 6.37× gate row and
  `contrast_passes` requires `neighbour_crosstalk_gated` AND
  `on_off_return_ratio_with_crosstalk ≥ 2`. Accepted 3 µm rounding: ADR 0.325 mm vs
  re-run 0.322 mm for the ±0.20 mm reader clearance.
- **A13-style FAIL on the superseded DND-121 branch.** Its ADR types stale margins
  the code does not produce (neighbour sweep 0.255 vs 0.280; MC 0.093 / 0.441 /
  4.60× vs 0.084 / 0.434 / 4.48×). Since DND-121 need not merge, **close DND-121 as
  superseded by DND-119** rather than correcting its prose.
- **A14 — PASS with a noted consistency gap.** MC on/off is crosstalk-free (worst
  4.49×) while `contrast_passes` gates 4.04×; both > 2×. Optional hardening only.

## Gates run (all green)

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **CLEAN 14/14**
- `falsifier_dnd115_checks.py --gate` → **CLEAN 12/12**
- `falsifier_dnd114_checks.py --gate` → **CLEAN 7/7**
- `falsifier_dnd112_checks.py --gate` → **CLEAN 11/11**
- `reliability_mask_checks.py` → **78/78**

## Assumptions / uncertainty

- CALCULATION + CAD only. No print, no purchase, no measurement (DND-27). No board
  contact (DND-32). Nothing here is a physical validation.
- The ~4.6% in-cone crosstalk figure and the 6.37×/7.72× ratio pair rest on
  assumption-class optical constants; the mechanism and clearances are geometric.

## Next test

- Close [DND-121](/DND/issues/DND-121) as superseded by DND-119.
- Optional A14 hardening (add the crosstalk term to the MC gate).
- Physical coupon (linkage force/friction/wear + real reflectance) is the only route
  to retire the measurement-only residuals — a human/external handoff (DND-27).
