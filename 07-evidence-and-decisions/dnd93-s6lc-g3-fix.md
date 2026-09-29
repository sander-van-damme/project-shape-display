# DND-93 — S6-LC lift-axis (G3) fix and re-run of the low-cost gate

- **Issue:** [DND-93](/DND/issues/DND-93) (CTO). Parent [DND-70](/DND/issues/DND-70).
- **Trigger:** [DND-74](/DND/issues/DND-74) falsified **G3** of S6-LC: `lift_axis()` sized the
  platen torque on one bank (800 cells) while the mechanism writes the **whole 6,400-cell
  board** in one global stroke. Superseding audit [DND-91](/DND/issues/DND-91) confirmed the
  break and added bounded findings.
- **Evidence class:** **CALCULATION** over sourced FDM limits + sourced actuator ratings; CAD
  geometry from `scad/s6lc_machine.scad`. No print, no purchase, no measurement ([DND-27](/DND/issues/DND-27)).
- **Branch:** `cto/dnd93-fix-g3` from `origin/main` (`4164730`).
- **Gates re-run:** `analysis/s6lc_checks.py` (40 checks) and
  `07-evidence-and-decisions/falsifier_dnd91_checks.py` (40 checks, re-baselined).

## Headline

**The G3 fix is correct and passes — but fixing G3 honestly breaks the cost gate.**
Keeping the global broadcast (DND-74 branch 1) requires a **NEMA23-class lift motor**; together
with the **six honest BOM allowances** the delivered cost rises to **$263.05**, **$13.05 over the
$250 gate**. Corrected verdict: **REJECT** (G6). S6-LC's "all gates pass / $162.13 / 7.4 s"
headline is retired; the machine survives as a *definition* whose cost must drop ~$13 or whose
write must be banked (branch 2) and re-timed.

## 1. Branch chosen: DND-74 branch 1 (keep the global broadcast)

The architecture's whole premise is a **broadcast** write: one platen, **four global 10 mm
strokes**, mask-gated per bank; only the **reset** is banked. Branch 1 preserves that premise and
sizes the lift for the real load. Branch 2 (bank the write) changes the timing model and the
"4 strokes" claim and is evaluated in §4.

### The corrected lift axis

The four screws are belt-synchronised at 1:1, so the single lift motor supplies the **sum** of the
four per-screw torques = the total global torque (belt losses ignored → optimistic).

| Load model | Force | Torque (lead 2 mm, η 0.5) | vs 2.2 N·m motor |
|---|---:|---:|---|
| old, as coded (800 cells) | 320 N | 0.204 N·m | 1.47× vs **0.30** (wrong input) |
| **corrected global (6,400 × 0.4 N)** | **2,560 N** | **1.6297 N·m** | **1.35× PASS** |
| per screw (shared) | 640 N | 0.4074 N·m | — |

`lift_axis()` now returns `cells_lifted = 6400`, `load_n = 2560`, `torque_needed_nm = 1.6297`,
`motor_torque_nm = 2.2` (sourced-class NEMA23, ~$30-40), `margin = 1.35`, `passes = True`.
The old **0.30 N·m NEMA17** cannot carry it; the old gate passed only on the 1/8 load.

## 2. The bounded findings from the audit, fixed in the same pass

| Finding (audit) | Fix | Result |
|---|---|---|
| **Six honest allowances missing** (A1/A5) | Added `allowance`-class lines: mask index mechanism $15, carriage rail $20, thrust bearings $18, homing switches $3, cable chain $8, power protection $5 = **+$69** | Parts **$226.77** → delivered **$263.05** |
| **Cost gate must be re-stated** | `delivered margin >= $50` check retired; G6 now honestly **fails** at $263.05. The model *reports* the miss instead of hiding it. | **G6 FAIL** |
| **Circular "296 N ceiling"** (A3) | Replaced with a **comb-tooth bending limit**: PLA tooth 1.6 × 0.88 × 1.0 mm, σ_allow = 50 MPa / SF 2 = 25 MPa → 5.163 N/tooth × 80 teeth = **413.0 N** | Banked 128.2 N < 413 N → **3.22× PASS** |
| **Reset-carriage torque ungated** (A5) | New `reset_carriage_axis()` gate: 128.2 N through the 2 mm screw = **0.0816 N·m** vs a $8 42 mm small stepper (**0.16 N·m**) | **1.96× PASS** (new gate G7) |
| **Mask-index timing absent** (A4/A6) | Added `MASK_INDEX_S = 0.25 s` × 4 strokes = 1.0 s, and `CARRIAGE_TRAVERSE_S` for the 7 bank gaps (50.8 mm @ 100 mm/s = 3.556 s) | Full map **11.956 s** < 30 s, margin 18.04 s → **G4 PASS** |

## 3. Corrected gate table (honest)

| Gate | Old | **Corrected** | Margin |
|---|---|---|---|
| G1 cell fit | PASS | PASS | lane budget (but see §5 A1 — placement overflow still open) |
| G2 release (banked) | PASS vs 296 N | **PASS** | 128.2 N vs **413 N** (independent) |
| G3 lift-axis torque | PASS (1/8 load) | **PASS** | 1.6297 N·m vs 2.2 N·m (1.35×) |
| G4 full map < 30 s | 7.4 s | **PASS** | 11.956 s vs 30 s |
| G5 cost < $250 parts | PASS $139.77 | **PASS** | $226.77 |
| G6 cost < $250 delivered | PASS $162.13 | **FAIL** | **$263.05, over by $13.05** |
| G7 reset carriage (new) | — | **PASS** | 0.0816 N·m vs 0.16 N·m (1.96×) |

**Verdict: REJECT** (G6). G3, G4, G7 and the re-based G2 now pass on corrected arithmetic; the
program gate that fails is the delivered price.

## 4. The alternative branch (bank the write) does not rescue it cheaply

DND-74 branch 2 keeps the $12 NEMA17 (`lift_axis` on 800 cells is then correct) but serialises the
write into **8 banks × 4 strokes = 32 strokes**. Analytic re-run:

| Platen speed | Armed (32 strokes) | + mask + traverse + reset | Full map | < 30 s |
|---:|---:|---:|---:|---|
| 20 mm/s | 27.20 s | +9.56 s | 36.76 s | **FAIL** |
| 30 mm/s | 21.87 s | +9.56 s | 31.42 s | **FAIL** |
| **40 mm/s** | 19.20 s | +9.56 s | **28.76 s** | PASS (marginal) |

Branch 2 only fits the 30 s budget at **~40 mm/s** = **1,200 rpm on a 2 mm lead screw**, which
raises its own (unmodelled) torque/speed and wear questions, and abandons the "4 broadcast strokes /
7.4 s" premise. Cost would return to ~$242 delivered (under $250 but only $7.83 headroom).
**Neither branch closes comfortably**; branch 1 is $13 over delivered, branch 2 is timing-marginal
at 3× the screw speed. S6-LC is **not decision-ready**.

## 5. What is still open (not fixed here — separate defect class)

The DND-91 audited defects below are **geometry/mechanism** defects, out of this issue's
"lift-axis + bounded findings" scope. They remain listed in `decide()["residual_uncertainty"]` and
locked open in the re-baselined falsifier gate:

- **A1 — cell fit / lane placement.** The CAD pawl reaches 2.80 mm from the centreline vs a
  2.54 mm half-pitch → **overflows the neighbour band by 0.260 mm**. G1 checks a budget, not
  placement. This must be fixed before any full-machine build.
- **A2 — pawl spring section.** `pawl_spring()` uses the 0.90 mm root block, not the 0.45 mm CAD
  leaf → spring rate overstated **8×**; true release ~0.020 N; **no hold-force gate exists**.
- **A6 — per-cell reliability.** No per-cell feedback; at q = 1e-4, P(all 6,400 correct) = 52.7 %.
  The program reliability gate is still absent.
- **A7 — unloaded-write assumption** contradicts tabletop-in-play updates.
- **A8 — regional/jam behaviour** asserted, not modelled.

## 6. Reproduce

```bash
python 09-low-cost-variant/s6lc/analysis/s6lc.py            # full corrected screen
python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py     # 40 checks (corrected result locked)
python 07-evidence-and-decisions/falsifier_dnd91_checks.py  # 40 adversarial checks (re-baselined)
```

## 7. Most informative next step

The cheapest test that would decide S6-LC's fate is **not physical** (DND-27): it is a **cost-and-
mechanism trade study** — the two remaining paths to close are (i) shed ≥$13 delivered from the
honest BOM without dropping a required capability, or (ii) redesign the write for banking at a
platen speed that still fits 30 s, re-timing and re-costing it. Both are calculation/CAD tasks.
The A1/A2/A6/A7/A8 mechanism defects are a separate fix track and must be resolved before the
machine is called buildable.
