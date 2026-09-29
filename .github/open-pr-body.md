# DND-93: fix S6-LC lift-axis G3 (global board) + honest allowances — G6 now fails

**Follows the DND-74/DND-91 falsification audit.** DND-74 (superseded by DND-91) broke **G3**:
`analysis/s6lc.py:lift_axis()` sized the platen torque on one bank (**800 cells**) while the
mechanism writes the **whole 6,400-cell board** in one global stroke (only the reset is banked).
This PR fixes G3, fixes the audit's bounded findings in the same pass, and re-runs the gate.

**Evidence class:** CALCULATION over sourced FDM limits + sourced actuator ratings, plus CAD
geometry. **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)). No board
contact ([DND-32](/DND/issues/DND-32)).

## Engineering question

Can S6-LC's lift axis be sized honestly for the architecture as described, and does the corrected
machine still close the < $250 delivered gate?

## Answer

**G3 is fixed and passes — but the honest BOM now breaks G6 (delivered cost). Corrected verdict:
REJECT.**

- **Branch chosen (DND-74 branch 1): keep the global broadcast.** `lift_axis()` now carries all
  **6,400 cells**: `0.4 N × 6400 = 2,560 N → 1.6297 N·m`; four belt-synced screws share it. A
  **NEMA23-class motor (2.2 N·m, ~$30)** is required — the old 0.30 N·m NEMA17 passed only on the
  1/8 load. **G3: 1.35× PASS.**
- **Bounded findings fixed:** the circular **296 N ceiling** is replaced by an independent
  **comb-tooth bending limit (413 N)**; a **reset-carriage torque gate (G7)** is added (0.082 N·m
  vs 0.16 N·m, 1.96×); the **mask-index (1.0 s)** and **carriage-traverse (3.556 s)** timing terms
  are priced → full map **11.96 s** (< 30 s, G4 PASS).
- **Cost:** add the six honest allowances (**+$69**) and re-price the lift motor (**+$18**) →
  parts **$226.77**, delivered **$263.05**. **G6 (< $250) FAILS by $13.05.** The model reports the
  miss rather than hiding it.
- **Branch 2 (bank the write)** was evaluated analytically and does **not** rescue it cheaply: it
  fits 30 s only at **~40 mm/s = 1,200 rpm** on a 2 mm lead (unmodelled torque/wear), abandoning
  the "4 broadcast strokes" premise and returning to ~$242 delivered (only $7.83 headroom).

## Corrected gate table

| Gate | Old | Corrected |
|---|---|---|
| G1 cell fit | PASS | PASS |
| G2 release (banked) | PASS vs 296 N | **PASS** vs **413 N** (independent) |
| G3 lift-axis torque | PASS (1/8 load) | **PASS** 1.63 N·m vs 2.2 N·m |
| G4 full map < 30 s | 7.4 s | **PASS** 11.96 s |
| G5 cost < $250 parts | PASS $139.77 | **PASS** $226.77 |
| G6 cost < $250 delivered | PASS $162.13 | **FAIL $263.05** |
| G7 reset carriage (new) | — | **PASS** 0.082 vs 0.16 N·m |

## Still open (not this issue's scope)

A1 cell-fit overflow (0.260 mm into the neighbour band), A2 pawl-spring section (8×, no hold-force
gate), A6 absent reliability gate, A7 unloaded-write assumption, A8 regional/jam — all remain
listed in `decide()["residual_uncertainty"]` and locked open in the re-baselined falsifier gate.

## Checks run

- `python 09-low-cost-variant/s6lc/analysis/s6lc.py` — corrected screen.
- `python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py` — **40/40** (corrected result locked).
- `python 07-evidence-and-decisions/falsifier_dnd91_checks.py` — **40/40** (re-baselined; fixed
  items corrected, open attacks remain open).
- `s5r_ultra_checks.py`, DND-76 primitives, DND-75 divergence gates — still green.

## Artifacts

- `07-evidence-and-decisions/dnd93-s6lc-g3-fix.md` — full report.
- `07-evidence-and-decisions/falsifier_dnd91_checks.py` — re-baselined 40-check gate.
- `09-low-cost-variant/s6lc/` — corrected model, checks, BOM CSV, README, rationale.
- `.github/workflows/ci.yml` — step comments updated (S6-LC gate, DND-91 audit gate).

## Residual uncertainty / next test

The cheapest deciding experiment is non-physical (DND-27): a **cost/mechanism trade study** — shed
≥ $13 delivered without dropping a capability, or re-design the write for banking at a platen speed
that still fits 30 s and re-time/re-cost it. A1/A2/A6/A7/A8 are a separate mechanism-fix track and
must be resolved before S6-LC is called buildable.
