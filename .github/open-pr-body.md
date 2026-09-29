# DND-65: reconcile the assembly-manifest purchased BOM to the promoted S5-R model

Make the board-facing assembly manifest carry the **same purchased BOM as the promoted
model** ($404.60 delivered working, incl. the sourced steel drive rod), so a board member
generating a shopping list from the print/build package cannot under-buy or see a total
that contradicts the handoff headline.

**Evidence class:** documentation/gate reconcile over already-landed CAD / calculation /
sourced-listing work. **No print, no purchase, no measurement**
([DND-27](/DND/issues/DND-27)). **No board contact** ([DND-32](/DND/issues/DND-32)).

## Engineering question

`08-current-design/fabrication/manifests/assembly_manifest.md` §"Purchased BOM" was generated
verbatim from the **pre-DND-58 ratified CSV**
(`06-experiments/test12_winner_convergence/s5r_bom_ratified.csv`), which produced two real
inconsistencies:

1. **Total contradicted the handoff headline.** The table total was **$388.10 delivered**,
   labelled *"TOTAL (working scenario, sourced units)"*. But the promoted model
   `s5r_register.bom(rows_in_bank=4)` returns **`delivered_usd = $404.60`**. $388.10 is the
   *optimistic sourced-unit* variant (2 bank ICs, motor $12.39 / writer $2.20, no rod),
   mislabelled as "working".
2. **Missing purchased line.** No **sourced Ø6 mm steel drive-rod** row, though assembly
   step 3 requires the board to source one ([DND-58](/DND/issues/DND-58)).

**Answer:** the manifest + CSV now reconcile line-by-line to the promoted model.

## What changed

- **`s5r_bom_ratify.py::emit_bom_csv`** now emits the **WORKING** scenario at the DND-54
  allowance units ($12.00 motor / $2.50 writer) + the block's own priced channels + the
  DND-58 sourced steel rod. Delivered total reconciles to the model's
  `delivered_usd` (**$404.60**). Adds the **steel drive-rod line**; labels the optimistic
  **$387.18** as a non-working reference and records the superseded **$388.10** header as a
  mislabel. A `Q8` selftest re-reads the emitted CSV and asserts TOTAL == model
  `delivered_usd`, rod present, and scenario labels correct.
- **`gen_manifests.py::purchased_bom_md`** reads the promoted model `bom(4)` and presents
  the working figures + **$404.60** total + explicitly labelled non-working scenarios
  (optimistic $387.18, rod-unpriced $401.12, DND-54 claim $397.53).
- **`manifests/assembly_manifest.md`** regenerated: steel-rod line, working total $404.60,
  correct scenario labelling, DND-27 "purchases nothing" note kept.
- **`fab_package_checks.py`: new gate C8** — fails if the manifest/CSV BOM total contradicts
  the model's `delivered_usd`, if the steel-rod line is absent, or if **$388.10** is
  headlined as the working scenario. Verified to **FAIL** (exit 1) on a synthetic drift
  (rod line removed + total reverted to $388.10).
- **CI wiring needs no workflow-file change.** C8 lives in `fab_package_checks.py`, which the
  existing `ci.yml` `fab-package` step already runs (`gen_manifests.py` → `fab_package_checks.py`);
  the README coherence gate **R1–R6** (`tools/validate/readme_s5r_coherence.py`) is already
  wired into `engineering-checks` ([DND-64](/DND/issues/DND-64)). So the new gate runs
  unattended with no `.github/workflows/*` edit (which would have tripped GitHub's
  maintainer-approval gate for a PR changing workflow files).
- **READMEs** (`08-current-design/fabrication/README.md`, gate-count C1-C6 → C1-C8) and
  `s5r_bom_ratify_checks.py` updated for the new working CSV.

## Evidence produced

| Check | Result |
|---|---|
| `06-experiments/test12_winner_convergence/s5r_bom_ratify.py --selftest` | **OK** (incl. new Q8 CSV reconcile: $404.60 == model) |
| `06-experiments/test12_winner_convergence/s5r_bom_ratify_checks.py` | **OK** (11 tests) |
| `06-experiments/test12_winner_convergence/s5r_register_checks.py` | **OK** (20 tests) |
| `08-current-design/fabrication/tools/fab_package_checks.py` | **GATE: PASS** (C1–C8) |
| `tools/validate/readme_s5r_coherence.py` | **GATE: PASS** (R1–R6) |
| `tools/validate/analytic_printability.py` (`scad/s5r_parts.scad`) | **PASS** |
| C8 synthetic drift (rod removed + total $388.10) | **GATE: FAIL** (exit 1) — as required |

Promoted model constants pinned by C8: delivered **$404.60**, parts **$348.79**, steel rod
**$3.00 parts / $3.48 delivered**.

## Assumptions / limits

- Documentation + CI-gate reconcile over landed CAD/calc/sourced work; it changes no model
  constant, geometry, or sourced price. The manifest derives its total from
  `s5r_register.bom(4)`, so it tracks the model exactly.
- The "$388.10" and "$387.18" figures are related but distinct *optimistic* variants
  (2 bank ICs sourced-unit vs 1 shared bank IC); both are labelled as **not** the working
  scenario.
- Residual uncertainty is unchanged and remains **measurement-only** ([DND-27](/DND/issues/DND-27)).

## Most informative next test

None remaining for this issue. On close, [DND-57](/DND/issues/DND-57) auto-wakes the CEO for
the terminal S5-R call.
