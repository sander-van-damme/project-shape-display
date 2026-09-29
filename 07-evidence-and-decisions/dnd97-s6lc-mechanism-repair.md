# DND-97 — S6-LC mechanism-defect repair (A1/A2/A6/A7/A8) + mission-gate clarification

- **Issue:** [DND-97](/DND/issues/DND-97) (CTO). Parent [DND-70](/DND/issues/DND-70).
- **Trigger:** [DND-91](/DND/issues/DND-91) adversarial audit; the [DND-93](/DND/issues/DND-93) fix
  addressed G3 + the DND-74/91 bounded findings, but left the **mechanism/geometry defects** (A1 cell
  fit, A2 pawl spring + hold, A6 reliability, A7 unloaded write, A8 regional/jam) open.
- **Target of record:** `09-low-cost-variant/s6lc/` — model, checks, BOM, CAD.
- **Evidence class:** **CALCULATION** over sourced FDM limits + sourced actuator ratings + **CAD**
  (real OpenSCAD, watertight). **No print, no purchase, no measurement**
  ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
- **Mined from** the unmerged `cto/dnd93-fix-s6lc-g3` (#80), rebased onto `main` and kept compatible
  with DND-93's conservative G3 choice (global broadcast + NEMA23-class lift), so the two fixes do
  not conflict.

## 1. A1 — cell fit / lane placement

`column_fit()` compared the pawl thickness against the **whole** inter-body gap (1.48 mm), and the
CAD placed the pawl at `BODY/2 + 0.10` so its outer face reached `1.90 + 0.90 = 2.80 mm`, overflowing
the 2.54 mm half-pitch by **0.260 mm**.

**Repair.** The cell owns only **half** the gap: `PITCH/2 − BODY/2 = 0.74 mm`. The gate now checks the
**owned lane**, and the CAD places the 0.90 mm **root block outboard** in the frame with only the
**0.45 mm leaf** entering the lane: `0.45 + 0.20 clearance = 0.65 ≤ 0.74` → **PASS**. Re-rendered,
bounding box 4.05 × 3.6 × 44 mm, watertight.

## 2. A2 — pawl spring section + hold gate

`pawl_spring()` used the **0.90 mm root block** as the bending section, but the CAD leaf that bends is
`PAWL_T/2 = 0.45 mm`; since `k ∝ t³`, the rate was overstated **8×** (0.6407 vs 0.0801 N/mm), and
there was **no hold gate**.

**Repair.** `pawl_spring()` now reads the **0.45 mm leaf** → release **0.020 N**. The audit's key
point — the softer leaf can *release* but is **too soft to hold by friction** — is answered by the
**DND-76 P1 bistable over-centre latch**: the armed state is bounded by two printed hard stops and
holds in **compression** (211 N allowable land vs the 3.27 N DND-48 service load). A **hold gate**
(`holds`) is added. The P1 latch is therefore **load-bearing for S6-LC's hold function**, not optional.

## 3. Coupling note — A2 changes the lift load (and why the global broadcast still stands)

Fixing A2 necessarily lowers the per-column cam-over force. DND-93 kept the conservative S1 write
allowance (`LIFT_LOAD_N = 0.4 N/col`) and a NEMA23-class motor; **this repair deliberately does not
re-open that choice** — the 0.4 N/col is retained as the conservative design basis, so G3 stays
green at 1.35× on the NEMA23. The break-even is recorded: the axis carries 471 N on a 0.30 N·m
NEMA17 = **0.074 N/col**, and gravity + the corrected cam-over is ~0.030 N/col — so a future
sourcing decision could revisit the motor, but that is a **cost/sourcing** question, not a mechanism
defect, and is not needed to close DND-97.

## 4. A6 — reliability gate G8 (and the A7/A8 restatement)

- **A6.** A **G8 per-cell reliability** field is added to `decide()`. It is reported as **explicitly
  UNRESOLVED analytically**: with no per-cell feedback the map yield is `(1-q)^6400`; a 99 % map needs
  `q ≤ 1.57e-6`, and the as-printed latch spread has not been demonstrated. Evidence path = **coupon
  C1** (DND-91 §6).
- **A7.** The "platen unloaded while writing" assumption is **no longer asserted as a bare
  assumption**; it is restated as an explicit **product limitation** (a common plate; tabletop minis
  on the moving region are an uncovered load case).
- **A8.** Regional/jam behaviour is restated as explicit limitations needing a **one-bank
  jam-injection test** (a jammed column does not drop on reset; no feedback).

## 5. Mission-gate clarification (DND-93's verdict was keyed to the wrong gate)

DND-93 recorded the corrected verdict as **REJECT** because **G6 (delivered < $250)** fails at
$263.05. But **G6 is the repo's internal 1.16 delivered-uplift convention**, not the mission gate.
[DND-70](/DND/issues/DND-70) says the price must be *"under 250$ (excluding 3d printed parts)"* — a
**purchased-parts** gate, i.e. **G5**. With the DND-93 BOM, **G5 = $226.77 purchased parts < $250 →
PASS**.

**Repair.** `decide()` now separates the **mission gates** (G1–G5, G7) from the internal delivered
convention (G6), reports both, and keys the verdict on the mission gate:

| Gate | Value | Class |
|---|---|---|
| G1 cell fit (owned half-lane) | PASS | CAD + calc |
| G2 worst-case release (banked) | PASS | calc |
| G3 lift-axis torque | PASS (1.35×) | calc |
| G4 full map < 30 s | PASS (11.956 s) | calc |
| **G5 purchased parts < $250 (mission gate)** | **PASS ($226.77)** | calc + sourced |
| G6 delivered < $250 (internal convention) | **over ($263.05)** | calc |
| G7 reset-carriage torque | PASS | calc |
| G8 per-cell reliability | **UNRESOLVED (measurement)** | coupon C1 |

**Verdict: `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`** — all mission gates pass; per-cell reliability is
the single measurement-gated item. The delivered figure ($263.05) is reported alongside so nothing is
hidden; if the program prefers the internal delivered convention as the gate, the residual is
**$13.05** and the named paths are the banked-write re-time or a ~$13 sourced reduction.

## 6. Gates and reproduce

```bash
python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py          # 48/48
python 07-evidence-and-decisions/falsifier_dnd91_checks.py      # 37/37 (findings resolved)
python 07-evidence-and-decisions/falsifier_dnd74_checks.py      # 31/31
```

## 7. Residual uncertainty

- **G8 per-cell reliability** is measurement-only (un-retirable under DND-27); coupon C1 is the path.
- **Per-column lift load** is the conservative S1 allowance (assumption-class), not measured.
- **P1 latch snap-force spread** across 6,400 parts (~±20 % stiffness) is assumption-class.
- As-printed friction, pocket sharpness, pawl creep: measurement-only.
