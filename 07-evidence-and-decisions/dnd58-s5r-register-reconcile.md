# DND-58 — S5-R register reconciliation of the DND-55 rack + drive-rod corrections

- **Verdict:** The [DND-55](/DND/issues/DND-55) bank close-out produced two
  geometry corrections that land at the **register** level. Both are now folded
  into the register definition: the rack is re-dimensioned to **pitch 1.00 /
  tooth 0.50 mm** with a **1.00 mm per-stroke advance** (`RACK_STROKE_MM`), and
  the printed **3 × 2 drive-bar placeholder is replaced by a sourced steel rod
  d = 6 mm** (`BAR_D_MM`). The **full-map time is unchanged at 24.62 s** because
  the bank pass is *angular* — the rack's linear pitch does not enter the timing.
  Residual **R-DND55-4 is closed**; **R-DND54-4 is closed for the bank
  envelopes/pitch and sharpened to a sourced-steel-rod requirement.**
- **This is NOT a print and NOT physical validation** ([DND-27](/DND/issues/DND-27)).
  Evidence class is **CAD** (register unit cell + bank render, real OpenSCAD) and
  **CALCULATION** (geometry, torsion inheritance, timing).
- **Owner:** CTO. **Issue:** [DND-58](/DND/issues/DND-58), for
  [DND-55](/DND/issues/DND-55) (residual R-DND55-4) and [DND-54](/DND/issues/DND-54).
- **Inputs (imported, so nothing drifts):** `s5r_register.py` +
  `s5r_register.scad` (the register source of truth); the bank model
  `s5r_bank.py` / `s5r_bank.scad`; `tools/validate/analytic_printability.py`.
- **Evidence class:** CAD + CALCULATION. No purchase, no print, no measurement.

Run:

```text
cd 06-experiments/test12_winner_convergence
python s5r_register.py            # register model (rack stroke, timing, BOM), JSON
python s5r_register_checks.py     # regression + honesty gates (DND-58)
python s5r_bank.py && python s5r_bank_checks.py
python s5r_bom_ratify.py --selftest
python ../../tools/validate/analytic_printability.py s5r_register.scad
```

## 1. The question

[DND-55](/DND/issues/DND-55) CAD-modelled the R = 4 bank and returned two
corrections that were recorded in its ADR but **not yet applied to the DND-54
register model** (residual R-DND55-4): the rack pitch (0.60 → 1.00 mm) and the
drive-bar section (printed 3 × 2 → sourced steel rod). This ADR applies them and
records the consequences for the register's per-stroke advance, timing and BOM.

## 2. Rack re-dimension (correction (a))

The DND-54 rack (`RACK_TOOTH_PITCH = 0.60`, `RACK_TOOTH_HEIGHT = 0.45`) leaves a
**0.15 mm inter-tooth gap**, below one extrusion line (0.44 mm) — it would fuse
on a 0.4 mm nozzle. The register SCAD and model now carry **pitch 1.00 /
tooth 0.50 mm** (gap 0.50 mm ≥ 0.44 mm, printable). The per-stroke advance is
re-derived from the **pitch**:

| Quantity | DND-54 | DND-58 (reconciled) |
|---|---:|---:|
| `RACK_TOOTH_PITCH_MM` | 0.60 | **1.00** |
| `RACK_TOOTH_HEIGHT_MM` | 0.45 | **0.50** |
| inter-tooth gap | 0.15 (fuses) | **0.50** (printable) |
| `RACK_STROKE_MM` | `= tooth height = 0.45` | **`= pitch = 1.00`** |

The old code keyed the stroke to the tooth **height** (`RACK_STROKE_MM =
RACK_TOOTH_HEIGHT_MM = 0.45`); the corrected mechanism advances one tooth
**pitch** per stroke (1.00 mm). This is a register-level fix, not a re-closure of
the mechanism.

## 3. Timing is unchanged (why the pitch change does not move 24.62 s)

The pass is **angular**: the bank crank turns `LEVEL_ANGLE_DEG = 72°` per level,
independent of rack pitch. The select pass is `(LEVELS-1) × 72° = 288°` and the
reset pass `72°`; the writer-carriage stations and the group-index moves are
unchanged. `timing()` therefore still returns:

- `full_map_s5r_s = 24.615` (< 30 s, margin +5.385 s)
- `select_pass_s = 0.400`, `reset_pass_s = 0.100`, `per_group_s = 0.900`

`timing()` now also reports `rack_stroke_mm = 1.00` and
`crank_deg_per_level = 72` so the independence of the linear pitch from the
timing is auditable.

## 4. Drive-bar section (correction (b))

The DND-55 torsion calculation refuted the printed 3 × 2 placeholder bar (peak
tip skew **4.96 mm** vs the keeper gate/2 = **0.175 mm**, ~28×). Realistic
sections:

| Section | peak skew | vs 0.175 mm |
|---|---:|---|
| printed PLA 3 × 2 (placeholder) | 4.96 mm | **FAIL ~28×** |
| printed PLA 3 × 12 (on-edge) | 0.253 mm | FAIL (1.4×) |
| printed PLA round Ø8 | 0.153 mm | PASS (1.15×) |
| **sourced steel rod Ø6 (chosen)** | **0.0026 mm** | **PASS ~67×** |

**Adopted: sourced steel drive rod Ø6 mm.** The register model declares
`BAR_D_MM = 6.0`, `BAR_MATERIAL = "sourced steel rod"`; `s5r_register.scad`
renders the bar as a round rod (replacing the 3 × 2 rectangle). An Ø8 printed
round bar is the fallback if the rod must be printed, with a re-check of the
reaction eccentricity `e` (R-DND55-1).

## 5. BOM delta

| Line | Parts | Delivered (×1.16) |
|---|---:|---:|
| DND-54 channels-unpriced claim | $342.70 | $397.53 |
| + block's own channels (DND-56) | $345.79 | $401.12 |
| **+ sourced steel rod Ø6 (DND-58)** | **$348.79** | **$404.60** |

The honest working total moves **$401.12 → $404.60 delivered** (margin
**$95.40** vs the $500 ceiling). Both earlier figures are retained as model
fields (`delivered_claim_usd` $397.53, `delivered_no_rod_usd` $401.12) so the
DND-54 and DND-56 records still reproduce, and `s5r_bom_ratify.py --selftest`
reconciles the rod-aware total. The rod is a **single commodity line** (6 mm ×
406.4 mm ground rod, $3.00 sourced-class allowance) and is a passive
power-transmission member — sourcing one rod is not the K7 cliff (which was about
80 *motors*).

## 6. Verification run

| Check | Result |
|---|---|
| `s5r_register_checks.py` (18 gates, incl. DND-58 rack/rod/BOM) | **OK** |
| `s5r_bank_checks.py` (16 gates) | **OK** |
| `s5r_bom_ratify.py --selftest` (DND-56 + rod reconcile) | **OK** |
| `s5r_bom_ratify_checks.py` (11 gates) | **OK** |
| register `analytic_printability.py` | PASS (keeper RISK closed by [DND-59](/DND/issues/DND-59)) |
| `s5r_bank.py --cad` (6 positives + 5 interference queries) | all PASS/empty |
| `tools/validate/validate_geometry.py` (real OpenSCAD, mesh) | HARNESS OK |

## 7. What this does and does not claim

- **Does:** reconcile the register rack to the corrected pitch and per-stroke
  advance; adopt and price the sourced steel rod; show the timing is unaffected;
  re-run the register/bank/printability/geometry harnesses; close R-DND55-4.
- **Does not:** claim a printed or measured part, a qualified rod, or retire any
  measurement-only residual. R-DND55-1 (reaction eccentricity `e`) remains an
  assumption for a *printed* bar and is made irrelevant by the steel rod.

## 8. Residual uncertainty / risk register

| id | Residual | Class | Status |
|---|---|---|---|
| R-DND55-4 | Corrected rack stroke changes the DND-54 per-stroke advance | CAD/calc | **closed (this ADR)** |
| R-DND54-4 | Multi-row bar drive torsion / envelopes | CAD/calc | **closed for envelopes/pitch; sharpened to sourced-rod** |
| R-DND55-1 | Bar-torsion eccentricity `e` | assumption | open for a printed bar; **closed for the steel rod ([DND-59](/DND/issues/DND-59))** |
| R-DND54-1/2 | As-printed friction / gate sharpness / creep | measurement-only | open — unmeasurable under [DND-27](/DND/issues/DND-27) |
| R-DND54-KEEPER | Keeper leaf 1-line printability RISK | CAD/calc | **closed ([DND-59](/DND/issues/DND-59))**: 2 lines + compression shoulder |

## 9. Decision and next actions

1. **Adopt the reconciled register:** rack pitch 1.00 / tooth 0.50 mm,
   `RACK_STROKE_MM = 1.00`, sourced steel drive rod Ø6 (`BAR_D_MM = 6.0`), BOM
   **$404.60 delivered working**.
2. **Close R-DND55-4**; keep R-DND54-4 closed for envelopes/pitch and sharpened to
   the sourced-rod requirement; retain R-DND55-1 as the printed-bar fallback
   assumption.
3. **Do NOT contact the board.** This is an internal CAD/calc reconciliation; the
   board trigger is a buildable print-ready machine. State that boundary plainly.

## 10. Evidence classes used

| Class | Where |
|---|---|
| CAD | `s5r_register.scad` (unit cell + round rod); `s5r_bank.scad`; real-OpenSCAD render + interference queries |
| CALCULATION | torsion inheritance (DND-55), timing (`timing()`), printability (FDM limits) |
| sourced | FDM process limits (`tools/fdm-limits`), steel/PLA moduli (DND-55) |
| **NOT** | print, measurement, purchase |
