# DND-64: reconcile 08-current-design README to the promoted S5-R machine

Make `08-current-design/README.md` describe **one machine consistently — the promoted
S5-R** — so a board reader opening the engineering source of truth meets the printable
machine we are handing over, not the superseded incumbent S5.

**Evidence class:** documentation reconcile over already-landed CAD / calculation /
sourced-listing work. **No print, no purchase, no measurement**
([DND-27](/DND/issues/DND-27)). **No board contact**
([DND-32](/DND/issues/DND-32)).

## Engineering question

The fabrication package is S5-R and coherent (C1–C7 PASS on `main` `b1d6659`), and §6a
points at it — but the top-level README was internally inconsistent: the header + §1 still
described the incumbent S5 (**full-width 80-channel head of 80 bought PM steppers**), §2
compared the incumbent-S5 cost ($482.95), and §7 was still the old **S5 K1–K12 register**
with K7 as the binding residual. Which machine does the source of truth actually define?

**Answer:** now unambiguously S5-R, from header → §1 → §2 → §5 → §6 → §7 → §9.

## What changed

- **Header/status + §1** describe **S5-R**: shared-drive programmable rotary register,
  R = 4 bank, **2 bank motors + 40 writer solenoids**, **24.615 s**, **$404.60 delivered**.
  Incumbent S5 is labelled the superseded bought-motor fallback (K7 refuted, DND-49).
- **§2** comparison table is S5-R; the incumbent-S5 comparison moves to a labelled **§2a**.
- **§4/§5** key dimensions and purchased BOM are S5-R (`s5r_register.bom()`); the incumbent
  S5 BOM/cost table moves to a labelled **§5a** (kept, not deleted).
- **§6** makes the **fabrication package (§6a)** the visible "what to print" entry point;
  the old S5 coupon/harness route becomes a labelled legacy **§6b**.
- **§7** is now the **live S5-R residual register** (consolidated DND-59 R-DND54-* /
  R-DND55-* with closed/bounded/measurement-only status). The **K1–K12 / R1–R8 register is
  relocated to a labelled `Appendix A`** (not deleted).
- **§8/§9** next-actions and final verdict are S5-R; the legacy S5 verdict is in Appendix A.
- **New CI gate** `tools/validate/readme_s5r_coherence.py` (checks R1–R6) fails if the
  README's promoted-machine headline (machine name, actuator count, full-map time,
  delivered cost) contradicts the promoted model `s5r_register.py`, or if the incumbent S5
  is presented as the current machine / live register. Wired into `ci.yml`
  (`engineering-checks`) so this cannot drift again.

## Evidence produced

| Check | Result |
|---|---|
| `tools/validate/readme_s5r_coherence.py` | **GATE: PASS** (R1–R6) |
| `08-current-design/fabrication/tools/fab_package_checks.py` | **GATE: PASS** (C1–C7) |
| `06-experiments/test12_winner_convergence/s5r_register_checks.py` | **OK** (20 tests) |
| `06-experiments/test12_winner_convergence/s5r_residuals_checks.py` | **OK** (12 tests) |
| In-document anchors / local file links | all resolve |

Promoted model constants pinned in the gate: actuators **42** (2 + 40), full map
**24.615 s**, delivered **$404.60**.

## Assumptions / limits

- This is a documentation change plus a CI check; it does not change any model constant,
  geometry or BOM.
- The README headline is checked against `s5r_register.py`; the gate reads the model's JSON
  output, so it tracks the model exactly.
- Residual uncertainty is unchanged and remains **measurement-only** ([DND-27](/DND/issues/DND-27)).

## Most informative next test

None remaining for this issue. The README is coherent with the promoted machine and the
package is slicer-ready; on close, [DND-57](/DND/issues/DND-57) auto-wakes the CEO for the
terminal call.
