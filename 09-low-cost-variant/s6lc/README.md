# 09 — Ultra-low-cost alternative: S6-LC

**Status:** **selected candidate machine definition, folded into the DND-72 track, repaired under
[DND-93](/DND/issues/DND-93).** **Owner:** CTO. **Issue:** [DND-72](/DND/issues/DND-72)
(authoritative synthesis node) / board direction [DND-70](/DND/issues/DND-70). Originally explored
under [DND-71](/DND/issues/DND-71), consolidated by CEO direction.
**Base of record:** [`08-current-design/`](../../08-current-design/README.md) (S5-R, $404.60
delivered — **not modified by this directory**).

> **Evidence class. Everything in this directory is CAD geometry + CALCULATION over sourced FDM
> process limits and sourced actuator ratings. No part has been printed, purchased or measured**
> ([DND-27](/DND/issues/DND-27)). Prices are point-in-time sourced-class figures (2026-09).
> Ratification is [DND-73](/DND/issues/DND-73); the adversarial audit is
> [DND-91](/DND/issues/DND-91), whose findings are repaired here and locked by
> [`../../07-evidence-and-decisions/falsifier_dnd91_checks.py`](../../07-evidence-and-decisions/falsifier_dnd91_checks.py).
> Repair record: [`../../07-evidence-and-decisions/dnd93-s6lc-repair.md`](../../07-evidence-and-decisions/dnd93-s6lc-repair.md).
> Synthesis against the S5-R-trim negative result:
> [`../../07-evidence-and-decisions/dnd72-low-cost-synthesis.md`](../../07-evidence-and-decisions/dnd72-low-cost-synthesis.md).

## 0. DND-93 repair — what changed and why

The [DND-91](/DND/issues/DND-91) Falsifier audit **broke** the original S6-LC headline (A1 cell fit,
A2 pawl spring + missing hold gate, A3 circular ceiling, A4 unpriced timing, A5 BOM honesty, A6
missing reliability gate, A7 unloaded-write load, plus A8). [DND-93](/DND/issues/DND-93) repairs
each. The honest corrections:

| Finding | Original | Repair |
|---|---|---|
| **A1** cell fit | pawl 0.90 compared to the whole 1.48 gap; CAD placed it at BODY/2+0.10 (reach 2.80 > half-pitch 2.54) | gate the **owned half-lane (0.74 mm)**; pawl **leaf (0.45)** in-lane, **root block outboard**; CAD re-placed |
| **A2** spring | `k` from the 0.90 root (0.6407), **8× too stiff**; no hold gate | `k` from the **0.45 leaf** (0.0801 → 0.020 N release) + a **hold gate**, held by the **DND-76 P1 over-centre latch** (compression hard stop, 211 N land vs 3.27 N service) |
| **A3** ceiling | hard-coded 296 N (0.37 × 800, borrowed) | **computed**: min(comb-tooth bending × teeth, reset-motor stall force) = **391 N** |
| **A4** timing | 4 strokes + dwells only, 7.4 s | **mask-index + carriage-traverse priced** → **11.8 s** |
| **A5** cost | $139.77 / $162.13, 4 soft lines, 6 unlisted capabilities | soft lines repriced + 6 capability lines added → **$238.77 parts / $276.97 delivered** |
| **A6** reliability | no per-cell gate | **G7 added**, explicitly **UNRESOLVED** (no per-cell feedback; coupon C1 is the path) |
| **A7** lift load | 800 cells × 0.4 N | **whole board** (6,400) × honest stack-up (~0.05 N/col) = 318 N → 0.203 N·m (**1.48×**) |
| **A8** reset carriage | unpriced force | **G8 reset-carriage torque gate** added (0.010 vs 0.10 N·m) |

**Verdict is now `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`**, not an unqualified promote: the analytic
gates pass, but **G7 (per-cell reliability) is measurement-only** and the delivered figure exceeds
the $250 *delivered* convention (the DND-70 mission gate is **purchased** parts, which pass at
$238.77).

## 1. The target and the honest cost cliff

Board direction [DND-70](/DND/issues/DND-70): **all S5-R requirements stay the same except the
price**, which must be **< $250 purchased, excluding 3D-printed parts**. At the repo's additive
delivered uplift (1.16 = +10 % ship +6 % tax, [DND-41](/DND/issues/DND-41)) that is a **parts
ceiling of $250 / 1.16 = $215.52** on the *delivered* reading; the board's literal gate is the
**purchased** figure < $250.

S5-R's purchased BOM decomposes as:

| Block | USD | Share |
|---|---:|---:|
| Fixed legacy base (S5 lift/scan/frame bought stock) | 218.70 | 62.7 % |
| Actuators: 2 NEMA17 bank motors + 40 writer solenoids | 124.00 | 35.6 % |
| Driver channels + sourced steel rod | 6.09 | 1.7 % |
| **Purchased parts (S5-R)** | **348.79** | 100 % |

**The legacy fixed base alone ($218.70) already exceeds the entire $215.52 parts budget.** No amount
of penny-shaving closes this. The machine must be re-conceived so that there is **no per-row writer
bank** and the bought lift/scan/frame stock is replaced by a **single-lead-screw axis over a printed
frame**. The cost cliff is **actuator count**, not part quality.

## 2. The machine in one paragraph

**S6-LC** is an 80 × 80 array of **square printed columns** at 5.08 mm pitch (406.4 × 406.4 mm),
each carrying a **five-pocket vertical rack** (10 mm pockets) and a **printed cantilever pawl** whose
**armed/disarmed state is a DND-76 P1 bistable over-centre latch** — a **hard-stop compression**
hold, not a friction preload. The board is split into **8 banks of 10 rows** (800 cells each). A
full map is written by **four global 10 mm broadcast platen strokes**: on stroke *k* only the cells
whose **bank threshold mask gate** is open advance. Four binary masks encode five heights
(0/10/20/30/40 mm). State is cleared by a **travelling reset carriage** that trips the eight banked
release combs one bank at a time. The only bought actuators are **three small steppers**: one lift
motor (four belt-synced lead screws), one mask-gate index motor, and one reset-carriage motor.
**$238.77 purchased parts / $276.97 delivered**; **11.8 s** full-map (repriced and re-timed under
DND-93).

## 3. Why this machine (design rationale)

| Decision | S5-R | **S6-LC** | Why |
|---|---|---|---|
| Per-cell bought actuator | 0 | **0** | printed latch + pawl memory |
| Per-row bought actuator | **40 solenoids** | **0** | a passive mask gate replaces the writer bank |
| Bought actuators total | 42 | **3** | the whole cost lever |
| Lift | printed cam platen + 2 bank motors | **1 stepper, 4 belt-synced screws** | fewer bought parts |
| Selection medium | 40 solenoids over passive rotors | **per-bank punched/printed threshold mask** | $0 actuator |
| Map write | rotating rotor to a hard stop | **4 broadcast 10 mm strokes** | massively parallel |
| Cost (delivered) | $404.60 | **$276.97** | −32 % |
| Full-map time | 24.615 s | **11.8 s** | 4 strokes, not 80 rows |

The architecture family is the already-screened **S1 broadcast threshold ratchet**
([`04-architecture-candidates/`](../04-architecture-candidates/README.md), [Test11 S1/S2
screen](../06-experiments/test11_threshold_ratchet_s1/README.md)). S1's two open failures were
addressed, not ignored:

1. **Worst-case release force** (S1 B2: ~2.4 kN all-armed). Fixed by **banking the reset** (S1-B):
   one bank of 800 cells at a time → **16 N**, far under the computed 391 N ceiling.
2. **Mask write time** (S1 C: serial 2560 s, 80-channel 56 s). Fixed by making the mask a
   **pre-written / off-line medium**, exactly as the S1/S2 screen permits. This is stated as a
   **product limitation**, not hidden (see §6).

## 4. Functional allocation (the ten jobs)

| Job | S6-LC mechanism | Evidence |
|---|---|---|
| Map representation | per-column pawl pocket (5 levels) | CAD + calculation |
| Selection | per-bank threshold mask gate (passive medium) | CAD + calculation |
| Power delivery | one platen, 4 broadcast 10 mm strokes | calculation |
| Vertical positioning | 4 × 10 mm accumulated by one-way pawl | CAD + calculation |
| State retention | pawl in pocket; no powered hold | CAD + calculation |
| Tabletop load support | pawl → rack pocket → column → platen shelf | calculation |
| Lowering / reset | travelling carriage trips 8 banked release combs | CAD + calculation |
| Regional isolation | mask gates are per-bank ⇒ bank-local replay | calculation |
| Programming | set masks off-line; 4 strokes read them | calculation |
| Detection / recovery | axis reference sensors only; no per-cell feedback | assumption |

## 5. Key dimensions and gates

| Parameter | Value | Basis |
|---|---:|---|
| Grid / pitch / cells | 80 × 80 / 5.08 mm / 6,400 | design criteria |
| Column body / owned half-lane | 3.60 mm / 0.74 mm | DND-93/A1 (owned lane, not the whole gap) |
| Pawl leaf / root | 0.45 × 1.20 × 8.00 mm / 0.90 mm (outboard) | CAD + calculation |
| Travel / level | 40 mm / 10 mm × 4 | design criteria |
| Banks | 8 × 10 rows (800 cells) | calculation (release force) |
| Bought actuators | **3** (lift, mask index, reset carriage) | `s6lc.py` `bom()` |
| Full-map time | **11.8 s** (30 s gate, 18.2 s margin) | `timing()` |
| Purchased parts | **$238.77** (< $250, mission gate) | `bom()` |
| Delivered | **$276.97** (> $250 delivered convention) | `bom()` |

### 5a. Gate table (`analysis/s6lc.py` `decide()`)

| Gate | Result | Margin |
|---|---|---|
| G1 cell fit (owned half-lane) | **PASS** | leaf 0.45 + 0.20 clear ≤ 0.74 |
| G2 worst-case release force (banked) | **PASS** | 16 N vs 391 N computed ceiling |
| G3 lift-axis torque (whole board) | **PASS** | 0.203 vs 0.30 N·m (1.48×) |
| G4 full map < 30 s | **PASS** | 11.8 s vs 30 s |
| G5 cost < $250 **purchased** (mission gate) | **PASS** | $238.77 |
| G6 cost < $250 *delivered* (repo convention) | **reported** | $276.97 — over |
| G8 reset-carriage torque | **PASS** | 0.010 vs 0.10 N·m |
| **G7 per-cell reliability** | **UNRESOLVED** | measurement-only (coupon C1); no per-cell feedback |

Verdict: **`PROMOTE_TO_09_WITH_MEASUREMENT_GATE`**.

## 6. Product limitation (stated, not hidden)

**Mask preparation is off-line.** S6-LC's visible transition is the four
broadcast strokes + banked reset (7.4 s). The per-bank threshold mask must be
set before the transition. Two legitimate modes:

- **Reused/pre-written media.** Cards or gate combs for common maps are printed
  in advance; an unannounced map needs its gates set first.
- **Off-line set during the previous map.** While the board shows state *n*, the
  operator/controller sets the mask for state *n+1* (double buffering), exactly
  the S2 trade. If the next map is known ~10 s ahead, the <30 s visible target is
  met without qualification.

A genuinely unannounced, arbitrary map is **mask-set-time first**, not 7.4 s.
This is a deliberate, documented limitation of this architecture, recorded
here and in the [DND-71](/DND/issues/DND-71) plan. It is the honest price of
removing the 40-solenoid writer bank.

## 7. Reproduce

```bash
cd 09-low-cost-variant/s6lc/analysis
python s6lc.py             # full machine screen (JSON)
python s6lc_checks.py      # 31 regression checks
python printability_s6lc.py   # sourced FDM-limit table + record
# the DND-91 findings-resolution gate (from the repo root):
python 07-evidence-and-decisions/falsifier_dnd91_checks.py
# CAD (real OpenSCAD; see tools/openscad-install/TOOLS)
export PATH="$HOME/.local/bin:$PATH"
python render_s6lc_cad.py  # renders 5 parts, mesh-validates them
```

## 8. Files

| Path | What |
|---|---|
| [`analysis/s6lc.py`](analysis/s6lc.py) | machine model: geometry, force, timing, BOM, gates |
| [`analysis/s6lc_checks.py`](analysis/s6lc_checks.py) | 31 regression checks |
| [`analysis/printability_s6lc.py`](analysis/printability_s6lc.py) | sourced-FDM-limit table |
| [`analysis/render_s6lc_cad.py`](analysis/render_s6lc_cad.py) | real-OpenSCAD render + mesh check |
| [`scad/s6lc_machine.scad`](scad/s6lc_machine.scad) | the part set (real OpenSCAD) |
| [`cad/`](cad/) | rendered STLs + CAD/printability records |
| [`bom_s6lc.csv`](bom_s6lc.csv) | purchased BOM line table |
| [`evidence/`](evidence/) | architecture + printable-path statements |

## 9. Residual uncertainty (measurement-only or product)

- **G7 per-cell reliability is UNRESOLVED.** With no per-cell feedback, the map yield is
  `(1-q)^6400`; a 99 % map needs q ≤ 1.57e-6. S6-LC provides no evidence the as-printed latch meets
  it. The evidence path is coupon C1 (100 cycles/cell × 4 cells × 3 coupons).
- **Pawl/latch force spread (S1-D).** The P1 latch makes the *state* exact (hard stops), but the
  *snap force* still spreads with print stiffness (~±20 %). Break-even sd ≈ 9 %; typical FDM
  thin-leaf spread is 10–20 % *(assumption)*.
- **As-printed friction μ, pocket sharpness, pawl creep.** Measurement-only.
- **Platen flatness / racking** across 406 mm on 4 screws. The lift-load stack-up is
  assumption-class (gravity + cam-over + bearing friction).
- **Comb-tooth and motor-stall ceilings** are computed from sourced-class PLA strength and motor
  ratings, but not measured.
- **No per-cell feedback.** A missed latch is a silent local height error — the same failure class
  as S5/S5-R.

The machine is **not** claimed print-ready or physically validated. It is a buildable *definition*
whose analytic gates pass on the DND-27 evidence classes; its per-cell reliability and the delivered
cost convention remain open, and its verdict is explicitly gated on coupon C1.

> **Falsifier audits [DND-74](/DND/issues/DND-74) / [DND-91](/DND/issues/DND-91) — findings now
> repaired under [DND-93](/DND/issues/DND-93).** The audits
> ([`dnd74-s6lc-falsification.md`](../../07-evidence-and-decisions/dnd74-s6lc-falsification.md),
> [`dnd91-s6lc-falsification.md`](../../07-evidence-and-decisions/dnd91-s6lc-falsification.md))
> broke gate G3 (`lift_axis()` sized on one bank, 800 cells, while the write is global over 6,400)
> and seven further findings. The DND-93 repair
> ([`dnd93-s6lc-repair.md`](../../07-evidence-and-decisions/dnd93-s6lc-repair.md)) resolves them and
> the resolution is locked by
> [`falsifier_dnd91_checks.py`](../../07-evidence-and-decisions/falsifier_dnd91_checks.py). Treat any
> "all six gates pass / 7.4 s / $162.13" headline as **superseded**; the corrected headline is
> **$238.77 parts / $276.97 delivered / 11.8 s**, verdict `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`.
