# DND-93: fix S6-LC lift-axis G3 + all DND-91/DND-74 falsifier findings

**Repairs the selected S6-LC machine** (`09-low-cost-variant/s6lc/`) against the
[DND-91](/DND/issues/DND-91) and [DND-74](/DND/issues/DND-74) adversarial audits. The audits broke
gate G3 (lift axis) and seven further findings; this PR fixes each and converts both falsifier gates
into **findings-resolution gates** so the fixes cannot drift back.

**Evidence class:** CALCULATION over sourced FDM limits + sourced actuator ratings + CAD (real
OpenSCAD). **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)). **No board
contact** ([DND-32](/DND/issues/DND-32)). `08-current-design/` untouched.

## Engineering question

Can S6-LC's lift axis (G3) and the DND-91/DND-74 findings be resolved without relaxing the mission
requirements, and does the corrected machine still meet the <$250-purchased / <30 s / 40 mm gates?

## Answer

**Yes for the analytic gates; two honest caveats remain.**

- **G3 — keep the global broadcast, re-derive the load.** The audit's 2,560 N bound combined the
  correct column count (6,400) with the *stale pre-A2* per-column load (0.4 N). After the A2 pawl
  correction the true lift load is gravity + cam-over + bearing friction ≈ **0.05 N/col**, so the
  whole board is **318.8 N → 0.203 N·m → 1.48×** on the 0.30 N·m NEMA17 — **no reduction, no
  banking**, preserving the fast 4-stroke timing. Branches (A) upsize-the-axis and (B) bank-the-write
  are evaluated and rejected in the ADR (A needs ~3,000 rpm; B re-times to 44 s).
- **A1** owned-half-lane cell fit + outboard root (CAD re-placed).
- **A2** pawl `k` from the 0.45 leaf (8× correction) + a **hold gate** backed by the DND-76 **P1
  over-centre latch** (compression hard stop).
- **A3** circular 296 N → computed `min(tooth bending × teeth, motor stall) = 391 N`.
- **A4** mask-index + carriage-traverse priced → **11.8 s**.
- **A5** soft lines repriced + six unlisted capabilities added → **$238.77 parts / $276.97 delivered**.
- **A6** **G7** per-cell reliability added, explicitly **UNRESOLVED** (coupon C1 is the path).
- **A7** whole-board lift load (§G3).
- **A8** **G8** reset-carriage torque gate added.

**Verdict: `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`.**

## What changed

- `09-low-cost-variant/s6lc/analysis/s6lc.py` — corrected geometry, spring, hold, ceiling, lift load,
  timing, BOM, gates (G7/G8 added).
- `analysis/s6lc_checks.py` — **31/31**; `bom_s6lc.csv` regenerated; CAD re-placed + re-rendered
  (watertight); `scad/s6lc_machine.scad` pawl root outboard.
- `07-evidence-and-decisions/falsifier_dnd91_checks.py` — rewritten as a findings-resolution gate
  (**39/39**); `falsifier_dnd74_checks.py` likewise (**23/23**).
- New ADR `07-evidence-and-decisions/dnd93-s6lc-repair.md`; README + audit banners updated; CI steps
  updated.

## Evidence produced

| Check | Result |
|---|---|
| `s6lc/analysis/s6lc_checks.py` | **31/31** |
| `falsifier_dnd91_checks.py` (resolution) | **39/39** |
| `falsifier_dnd74_checks.py` (resolution) | **23/23** |
| `s5r_ultra_checks.py` (DND-72 control) | 19/19 |
| `primitives_checks.py` / divergent runner | pass / exit 0 |
| `readme_s5r_coherence.py` | GATE PASS |
| CAD render `render_s6lc_cad.py` | 5 parts watertight |

## Assumptions / limits

- The lift load is an **assumption-class stack-up** (gravity + cam-over + bearing friction); the
  break-even is ~0.044 N/col friction.
- **G7 reliability is measurement-only** and unresolved; **G9-note:** delivered $276.97 exceeds the
  $250 *delivered* convention while purchased $238.77 passes the DND-70 mission gate.

## Most informative next test

The **coupon C1** (unit-cell pitch/latch/hold/engage coupon, DND-91 §6), then sourced ratification of
the new BOM lines. Physical build is gated by DND-27 (routed via the CTO).
