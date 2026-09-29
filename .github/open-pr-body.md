# DND-123: crosstalk normalisation corrected (6.37× → 5.95×); A13 now checks ADR internal consistency

## What changed

- **Model** `08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py`:
  `shutter_read_contrast()` now computes `bright`, `dark` and the neighbour crosstalk term with the
  **same area-weighted `A/d²` convention** (`A_vane = 0.44·1.60 = 0.704 mm²`). Previously the signal
  used the point return `r/g²` while the crosstalk used `r·A_incone/g_nb²`, mixing conventions and
  under-counting the crosstalk by `A_vane`. **No geometry change.**
- **ADR** `07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md`: the gated ratio is
  corrected to **5.95×**; the stale "0.068" crosstalk figure is corrected to 0.046 (4.6%).
- **Falsifier checker** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py`: A6 reports
  the corrected value; **A13 now parses the ADR's quoted crosstalk percentage and checks it is
  internally consistent with the quoted gated ratio** (`f ⇒ (1+f)/(1/R+f)`).
- **Register + READMEs**: new DND-123 sections; live headlines updated 6.37× → 5.95×.

## Engineering question

Was the DND-119 crosstalk-corrected on/off ratio (6.37×) arithmetically sound, or was it — like the
DND-112/DND-111 "number no artifact supports" class — a number whose internal arithmetic does not
reconcile?

## Findings

- **KO on the number (mechanism unaffected).** The ADR printed both "crosstalk **4.6%** of the vane
  return" and the gated ratio **6.37×**. These are mutually inconsistent: 4.6% implies **5.95×**;
  6.37× requires **3.25%**. The model's own function reported *two* crosstalk fractions
  (`neighbour_over_vane_term = 0.0325` vs `neighbour_crosstalk_ratio_physical = 0.046`).
- **Root cause.** `bright = r_vane/g_vane²` (point, no vane area) but
  `ct = r_vane·A_incone/g_nb²` (area-weighted). The mixed dividing normalisation discounts the
  crosstalk by `A_vane`.
- **The DND-121 branch made the opposite error** (`ct = frac·r_nb/g_nb²`, a dimensionless fraction
  times a point return → 7.41×). Neither 6.37× nor 7.41× is area-consistent.
- **The physics survives.** With a consistent convention the gated ratio is **5.95×**, ~3× above
  the 2× gate; `contrast_passes` stays TRUE. This is a margin correction, not a design failure.

## Evidence produced (CALCULATION only)

| Convention | crosstalk / vane | gated on/off |
|---|---:|---:|
| DND-119 as-written (mixed) | 3.25% | 6.37× |
| **DND-123 area-consistent (shipped)** | **4.6%** | **5.95×** |
| DND-121 branch (fraction × point) | 0.63% | 7.41× |

## Relationship to the DND-122 follow-up (already on main)

This branch is rebased on `a4338a7` (CTO's DND-122 follow-up: own-column clearance
3.41 → 3.42 mm, A13 extended to the swept clearances). The A13 extensions are
**merged in one checker**: the swept neighbour/own-column clearance checks from that
follow-up, plus the new crosstalk-percentage internal-consistency check here.

## Gates run (all green)

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **CLEAN 14/14** (A13 now also catches the
  percentage/ratio inconsistency; verified it FAILs the pre-DND-123 ADR text and a 6.37× tamper).
- `falsifier_dnd115_checks.py --gate` → **CLEAN 12/12**; `falsifier_dnd114_checks.py --gate` →
  **CLEAN 7/7**; `falsifier_dnd112_checks.py --gate` → **CLEAN 11/11**;
  `reliability_mask_checks.py` → **78/78**; `a1_writer_rate.py` exit 0.

## Assumptions / uncertainty

- CALCULATION only. No print, no purchase, no measurement (DND-27). No board contact (DND-32).
- The 4.6% crosstalk and the 5.95×/7.72× pair rest on assumption-class optical constants; the
  normalisation fix is pure arithmetic over the placed CAD geometry.

## Next test

- Physical single-cell A1 coupon (real LED/PD pair + linkage force/friction/wear) remains the only
  route to retire the assumption-class / measurement-only residuals — a human/external handoff
  (DND-27).
