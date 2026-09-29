# DND-55 — S5-R R=4 multi-row bank assembly: bar torsion + comber/carriage envelopes

- **Verdict:** The R=4 bank's **assembly envelopes fit** (bar, reset comber and
  writer-carriage sweep all clear the columns in a real OpenSCAD render with
  empty interference queries), **but the DND-54 drive-bar section does not close
  the keeper gate on bar torsion, and the DND-54 rack geometry does not print.**
  Both are corrected here: the bar must be a **sourced steel rod (d = 5–6 mm)** or
  an Ø8 printed round bar (the printed 3×2 placeholder is **~20× over** the gate),
  and the rack tooth pitch must rise **0.60 → 1.00 mm** (tooth 0.45 → 0.50 mm) so
  the inter-tooth gap clears one extrusion line. Residual **R-DND54-4 is closed
  for the comber/carriage envelopes and for the pitch/Y lay-out, and sharpened
  for the bar** (a sourced-steel requirement, not a printed part).
- **This is NOT a print and NOT physical validation** ([DND-27](/DND/issues/DND-27)).
  Every figure is labelled CAD / CALCULATION / sourced / assumption. The bar
  torsion number is a **bound** whose dominant input (the reaction eccentricity)
  is an assumption the coupon would have measured.
- **Owner:** CTO. **Issue:** [DND-55](/DND/issues/DND-55), for
  [DND-54](/DND/issues/DND-54) (residual R-DND54-4).
- **Inputs (imported, so nothing drifts):** `s5r_register.py` (per-pawl force,
  pitch, keeper gate, motor class); the model is
  `06-experiments/test12_winner_convergence/{s5r_bank.py, s5r_bank_checks.py}`,
  CAD is `s5r_bank.scad`, printability is
  `tools/validate/analytic_printability.py` (bank branch).
- **Evidence class:** CAD (SCAD + real-OpenSCAD render + scoped interference
  queries) and CALCULATION (torsion / clearance over sourced material and FDM
  limits). No purchase, no print, no measurement.

Run:

```text
cd 06-experiments/test12_winner_convergence
python s5r_bank.py            # analytic model (torsion, envelopes), JSON
python s5r_bank_checks.py     # regression + honesty gates
python s5r_bank.py --cad      # real OpenSCAD render + interference queries
python ../../tools/validate/analytic_printability.py s5r_bank.scad
```

## 1. The question

[DND-54](/DND/issues/DND-54) promoted S5-R on a single-column unit cell and left
the *assembly-level* geometry of the **R = 4 bank** un-modelled (R-DND54-4):
bar torsion, the reset-comber envelope and the writer-carriage envelope. Those
are claims about geometry, so per [DND-27](/DND/issues/DND-27) they are closed by
**CAD + calculation**, not by a coupon. This ADR does exactly that and reports the
bar-torsion number against the keeper gate (**KEEPER_GATE_STEP = 0.35 mm**).

## 2. The bank, and why R = 4 is free in pitch

Rows run along Y; the in-row column pitch is 5.08 mm. The shared bar spans the
**80 columns in X (406.4 mm)** and **R = 4 rows in Y** (`s5r_bank.scad`). A single
bank pass writes R rows at once, so the map needs `ceil(80/R) = 20` groups instead
of 80 (the DND-54 result). The cross-row pitch is 5.08 mm and is **independent of
the in-row pitch**, so R = 4 adds depth in Y only: `pitch_penalty = 0.0`, and the
DND-54 per-cell fit (0.53 mm worst-case tip gap) is unchanged — verified in
`pitch_penalty_check()`.

## 3. Bar torsion — the number the issue asks for (CALCULATION)

The bar is driven from **both ends** (2 motors, DND-54) and resists 320 ganged
pawls. The pawl reaction is predominantly **axial**; a perfectly axial line of
action produces **no** torsion about the bar axis. Torsion appears only from the
reaction's **eccentricity `e`** from the bar shear centre (tooth-flank angle and
pawl-to-tooth contact offset). The repo has no measured contact data, so `e` is an
**assumption** — the model is therefore reported **parametrically**.

Model (Saint-Venant prismatic bar, symmetric end drives, linear torque build-up):

```
w_torque   = F_total * e / L                 [N·mm per mm]
twist(L/2) = w_torque * (L/2)^2 / (2 G J)    [rad]
skew       = twist(L/2) * r_tip              [mm, tangential at the rack]
G = E / (2 (1+nu));  J_rect = (a^3 b)/3 (1 - 0.630 a/b)
```

With `F_total = 80*4*0.0874 = 27.97 N`, `L = 406.4 mm`, `r_tip = 6 mm`, PLA
`E = 1500 MPa`, `nu = 0.35` (G = 555.6 MPa), and the **worst-case** `e = W/2`:

| Bar section | J (mm⁴) | G (MPa) | e (mm) | peak skew (mm) | vs gate/2 = 0.175 mm |
|---|---:|---:|---:|---:|:--:|
| printed PLA 3 × 2 (**DND-54 placeholder**) | 4.64 | 556 | 1.5 | **4.960** | **FAIL ~28×** |
| printed PLA 3 × 12 (on-edge) | 90.99 | 556 | 1.5 | 0.253 | FAIL (1.4×) |
| printed PLA round Ø8 | 402.1 | 556 | 4.0 | 0.153 | PASS (1.15×) |
| **sourced steel rod Ø5** | 61.36 | 76 923 | 2.5 | **0.0045** | PASS (~39×) |
| **sourced steel rod Ø6** | 127.2 | 76 923 | 3.0 | **0.0026** | PASS (~67×) |

**Decision-changing results.**

1. **The DND-54 placeholder bar (3 × 2 printed PLA) is refuted by ~28×** on
   torsion. It was never dimensioned for torsion.
2. **A printed PLA bar is marginal under the worst-case eccentricity.** Even a
   3 × 12 on-edge bar fails at `e = W/2 = 1.5 mm` (skew 0.253 mm > 0.175 mm); its
   break-even eccentricity is only **1.04 mm**, below the worst case. A printed
   Ø8 round bar passes (e = 4 mm, skew 0.153 mm) but with no margin.
3. **A sourced steel rod (d = 5–6 mm) makes torsion negligible** (≤ 0.005 mm,
   30–70× under the gate). The bar is a passive power-transmission member;
   sourcing **one rod** is not the K7 cliff (which was 80 *motors*). **Recommended
   fix: a Ø6 mm steel drive rod** (or, if the rod must be printed, an Ø8 round bar
   and a re-check of `e`).

The gate is the **half-gate bound**: if the peak tip skew is below
`KEEPER_GATE_STEP/2 = 0.175 mm`, no column can be written one level off. The
torsion number is a **bound**, not FEA; rack/bar attachment compliance and
multi-row load sharing are not modelled (§7).

## 4. Assembly envelopes (CAD) — do the comber and carriage fit?

`s5r_bank.scad` models the R = 4 bank (8 modelled columns at the real 5.08 mm
pitch, the racked bar, the reset comber and the writer-carriage **sweep
envelope**). A real OpenSCAD (2023.09.11) renders six parts and runs five scoped
interference queries; **all interference queries are EMPTY**:

| Query | Position | Expected | Result |
|---|---|---|---|
| `run_all_engaged` | every pawl on the rack | empty | **empty** |
| `selected_dropped_pawl` | one pawl held clear by its keeper | empty | **empty** |
| `comber_park` | comber parked below the pawl tips | empty | **empty** |
| `comber_trip` | comber swung up to the trip position | empty | **empty** |
| `writer_carriage_sweep` | carriage swept across the full X travel | empty | **empty** |

Analytic cross-check (`clearance_stack_up()`), mirrored from the SCAD datums:

| Envelope clearance | Value | Limit | Verdict |
|---|---:|---:|---|
| carriage nose to column top, **worst case** | 0.40 mm | > 0 | PASS |
| comber tine rides the X-gap between column stacks | 3.73 mm | > 0 | PASS |
| comber body clear of the modelled span (+X) | 33.02 mm | > 0 | PASS |
| carriage Y depth vs R = 4 bank span (18.24 mm) | 24 mm | ≥ span | PASS |
| cross-row free gap (ROW_PITCH − BAR_W), worst case | 1.88 mm | 0.20 mm | PASS |

**Verdict: the comber and writer-carriage envelopes fit the R = 4 bank**, and the
R = 4 lay-out adds no pitch penalty.

## 5. Sourced printability of the added parts (CALCULATION)

`analytic_printability.py` (bank branch) reads the SCAD constants and returns:

| Feature | Value | Limit | Verdict |
|---|---:|---:|---|
| drive bar width (BAR_W) | 3.00 mm | 0.88 mm | PASS |
| drive bar height (BAR_H) | 12.00 mm | 0.88 mm | PASS |
| rack tooth height | 0.50 mm | 0.44 mm | PASS |
| **rack tooth gap** (pitch − tooth) | **0.50 mm** | 0.44 mm | **PASS** (fixed) |
| reset-comber tine thickness | 0.90 mm | 0.88 mm | PASS |
| writer-carriage wall | 1.20 mm | 0.88 mm | PASS |
| cross-row free gap, worst case | 1.88 mm | 0.20 mm | PASS |

**DND-55 printability correction to DND-54.** The DND-54 rack
(`RACK_TOOTH_PITCH = 0.60`, `RACK_TOOTH_HEIGHT = 0.45`) leaves a
**0.15 mm inter-tooth gap**, which is **below the one extrusion line (0.44 mm)**
and would **fuse** on a 0.4 mm nozzle — the rack would not print as teeth. The
rack is re-dimensioned to **pitch 1.00 mm / tooth 0.50 mm** (gap 0.50 mm), and the
comber tine is thickened 0.60 → 0.90 mm (1 line → 2 lines). The bank now returns
**PASS**. The register's per-stroke advance therefore becomes **1.00 mm** (one
tooth) instead of 0.60 mm; that is a DND-54 rack-level change, recorded here.

## 6. What this does and does not claim

- **Does:** model the R = 4 bank as CAD; verify the comber/carriage envelopes with
  empty interference queries; give the bar-torsion number vs the 0.35 mm gate;
  refute the placeholder bar section; and name the corrected rack/tooth geometry.
- **Does not:** claim a printed or measured part, a qualified steel rod, an FEA of
  the bar, or the full 80-column (320-body) render. The reduced 8-column model is
  the CAD witness; the 80-column length is covered by the uniform-pitch argument,
  not by a 320-solid CSG render.

## 7. Residual uncertainty / risk register

| id | Residual | Class | Status |
|---|---|---|---|
| R-DND55-1 | Bar-torsion **eccentricity `e`** (tooth-flank contact offset) | assumption | **open** — dominant input; e = W/2 worst case; measured only by a coupon ([DND-27](/DND/issues/DND-27)). Steel rod makes it irrelevant |
| R-DND55-2 | Bar torsion model (Saint-Venant bound, no FEA, no attachments) | calculation | open — a bound, not FEA |
| R-DND55-3 | Reduced (8-column) CAD vs full 80-column torso | CAD | analytic uniform-pitch argument; not a 320-body render |
| R-DND55-4 | Corrected rack stroke 1.00 mm changes the DND-54 per-stroke advance | CAD/calc | **closed ([DND-58](/DND/issues/DND-58))** — register reconciled to pitch 1.00 / tooth 0.50, `RACK_STROKE_MM = 1.00`; timing unchanged (angular pass) |
| R-DND55-5 | As-printed friction, wear, creep (K2/K11 class) | measurement-only | open — unchanged by this closure |

## 8. Decision and next actions

1. **Adopt a sourced Ø6 mm steel drive rod** for the R = 4 bank (torsion ≤ 0.003 mm,
   ~67× under the gate). If the rod must be printed, use an Ø8 round bar and
   re-check `e`; **do not use the 3 × 2 placeholder section**.
2. **Re-dimension the rack to pitch 1.00 mm / tooth 0.50 mm** and reconcile the
   register's per-stroke advance (1.00 mm) — R-DND55-4. **Done: [DND-58](/DND/issues/DND-58)**
   (`RACK_STROKE_MM = 1.00`; timing unchanged because the pass is angular).
3. **Update the DND-54 residual R-DND54-4:** comber/carriage envelopes and the
   pitch/Y lay-out are **closed** (CAD); the bar is **sharpened to a sourced-rod
   requirement**.
4. **Do NOT contact the board.** The board trigger is a buildable print-ready
   machine; this is an internal CAD/calc closure. State that boundary plainly.

## 9. Evidence classes used

| Class | Where |
|---|---|
| CAD | `s5r_bank.scad`; real-OpenSCAD render + interference queries (`s5r_bank.py --cad`) |
| CALCULATION | bar torsion (`bar_torsion`), envelopes (`clearance_stack_up`), printability (bank branch) |
| sourced | material moduli (PLA 1500 MPa, steel 200 GPa), FDM limits (`tools/fdm-limits`) |
| assumption | reaction eccentricity `e`; Poisson 0.35; carriage/comber datums |
| **NOT** | print, measurement, purchase |
