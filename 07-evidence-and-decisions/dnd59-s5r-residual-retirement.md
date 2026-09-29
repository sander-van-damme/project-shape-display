# DND-59 — S5-R residual retirement: the last agent-reachable residuals

- **Verdict:** All five agent-reachable S5-R residuals are **retired or bounded
  on the evidence classes DND-27 allows**. The keeper is re-profiled to **2
  extrusion lines** (printability RISK -> PASS) with its *holding* function moved
  to a **hard printed shoulder in compression**; the writer force is re-derived
  **bottom-up** and cleared by the sourced actuator class; the missed-set
  reliability requirement is derived (**q <= 1.57e-6** per keeper for a 99 % map)
  and the agent-reachable levers (verify+retry, redundancy) are quantified; the
  crank-speed break-even is re-derived and the sourced motor class clears it; and
  the bar eccentricity `e` is shown **genuinely irrelevant for the sourced steel
  rod**. What remains is **measurement-only** and is listed explicitly.
- **This is NOT a print and NOT physical validation** ([DND-27](/DND/issues/DND-27)).
  Evidence class is **CAD** (SCAD geometry), **CALCULATION** (statics, reliability,
  tolerance Monte-Carlo) and **sourced listings** (published actuator specs). No
  print, no purchase, no measurement.
- **Owner:** CTO. **Issue:** [DND-59](/DND/issues/DND-59), for
  [DND-57](/DND/issues/DND-57) (the CEO terminal call).
- **Inputs (imported, so nothing drifts):** `s5r_register.py` + `s5r_register.scad`
  (register source of truth), `s5r_bank.py` (torsion model), and
  `tools/validate/analytic_printability.py`. New model:
  `06-experiments/test12_winner_convergence/{s5r_residuals.py,
  s5r_residuals_checks.py}`.

Run:

```text
cd 06-experiments/test12_winner_convergence
python s5r_register.py && python s5r_register_checks.py
python s5r_bank.py && python s5r_bank_checks.py
python s5r_residuals.py            # the residual retirement model, JSON
python s5r_residuals_checks.py     # regression + honesty gates
python ../../tools/validate/analytic_printability.py s5r_register.scad
```

## 1. The question

[DND-57](/DND/issues/DND-57) found S5-R clears every mission requirement on its
labelled evidence class **except buildability**, and split the remaining
residuals into **agent-reachable** (this issue) and **measurement-only**
(forbidden under [DND-27](/DND/issues/DND-27)). This ADR retires the
agent-reachable set.

## 2. R-DND54-KEEPER — keeper-leaf printability (RISK -> PASS)

**The DND-54 problem.** The keeper leaf was **0.45 mm = 1 extrusion line**
(limit 0.88 mm) — a print **RISK**, accepted. Worse, its *hold* was a
bending-spring force `k * over_centre_offset`, which is **tolerance-fragile**: the
offset (+/-0.10 mm per printed face) can print to zero, giving a non-holding
keeper. A Monte-Carlo over the sourced print tolerance shows the bending-only
hold fails in a meaningful fraction of builds (reported by
`keeper_tolerance_mc()`).

**The re-profile (two coupled fixes).**

1. **Hold by a hard printed shoulder in compression.** The pawl's push-out
   (0.0374 N) plus a 0.05 N seating preload is carried by a **0.90 x 0.70 mm
   printed shoulder** in compression. Over the sourced printed-PLA compression
   yield band (20–45 MPa) that is **144–324x** the load. The hold therefore no
   longer depends on any tolerance-critical offset — the print-accuracy
   Monte-Carlo does not apply to the holding function.
2. **2-line leaf.** The snap/release leaf is re-profiled to **0.90 mm = 2 lines**
   (PASS) and **4.00 mm long** so the snap strain stays low (0.51 % at the 0.06 mm
   over-centre offset).

**The geometry coupling (why the keeper moves to Y).** Thickening the keeper in
the pitch direction (X) would consume the free band: the X-band then holds
pawl 0.90 + keeper 0.90 + over-centre 0.06 = 1.86 mm in a 2.08 mm band, leaving a
worst-case gap of **0.02 mm < 0.20 mm** — a FAIL. The keeper is therefore
re-profiled into the **row direction (Y), beside the pawl**: the X-band then
holds only the pawl (gap 0.98 mm) and the Y-band holds pawl + keeper = 1.60 mm
(gap **0.28 mm**). Both axes clear the 0.20 mm requirement.

| Axis | Stack | Free band | Worst-case gap | Verdict |
|---|---:|---:|---:|---|
| X (pitch) | 0.90 (pawl) | 2.08 | 0.98 mm | PASS |
| Y (row) | 1.60 (pawl+keeper) | 2.08 | **0.28 mm** | PASS |

`analytic_printability.py` (register branch, now two-axis) returns **PASS** for
the register (was RISK); the keeper leaf reads 0.90 mm / 0.88 mm PASS and the new
shoulder reads 0.50 mm / 0.44 mm PASS.

## 3. R-DND54-6 — writer/solenoid force, bottom-up

**The DND-54 problem.** No listing published a force; the >= 1.2 N target was an
assertion.

**Bottom-up derivation.** The writer has two duties, priced separately:

```
required = leaf_trip  + gate_detent + nose_friction
         = k * over_centre  + preload  + mu * pawl_normal
         = 2.990 * 0.06     + 0.05     + 0.35 * 0.0374
         = 0.1794           + 0.05     + 0.0131  = 0.2425 N
```

The gate travel (0.35 mm) does **not** bend the leaf — the keeper nose slides
along the gate, so only a small translating detent is charged. Against the
**sourced actuator class** (small 5 V open-frame push solenoid, published force
1.20 N, $2.50 sourced-class allowance) the margin is **4.95x**. The bottom-up
figure replaces the bare assertion; the residual is that a **published-force
listing of this class is a purchase-time confirmation** (DND-27 forbids buying
it now).

## 4. R-DND54-5 — missed keeper set = silent row error

**The requirement.** With no per-cell feedback (R1 unchanged), a full map of
6,400 keepers is correct only if every keeper sets correctly:

```
P(full map correct) = p_set^(ROWS*COLS)  =>  q = 1 - p_set <= 1.57e-6
```

for a **99 %** full map. That is the bare, binding number.

**Agent-reachable levers (quantified).** Each lever relaxes the required
per-keeper failure rate `q`:

| Architecture | required q | q vs bare | class |
|---|---:|---:|---|
| bare (one set, no feedback) | 1.57e-6 | 1.00 | — |
| per-group verify+retry, catch 50 % | 3.14e-6 | **2.0x looser** | firmware + kinematics |
| per-group verify+retry, catch 90 % | 1.57e-5 | **10x looser** | firmware + kinematics |
| writer redundancy 2x | 1.25e-3 | **798x looser** | mechanism |

So a **per-group verification pass is a real, agent-reachable lever** that
loosens the per-set requirement 2–10x, and a redundant second set loosens it
~800x. The as-printed `q` itself remains **measurement-only**; this ADR bounds
the requirement and the levers, not a measured `q`.

## 5. R-DND54-3 — crank speed / writer settle

The break-even is re-derived from the model: **min crank 468.0 deg/s** (chosen
720 -> **1.54x**) and **max writer settle 0.0837 s** (chosen 0.05 -> **1.67x**).
The required per-motor torque at the chosen bank load is **0.1398 N·m**; the
sourced NEMA17 class (0.30 N·m holding) gives **2.15x**. The chosen **720 deg/s
is inside the sourced motor class** (>= 1800 deg/s class figure). The *loaded*
speed/torque curve remains **measurement-only**.

## 6. R-DND55-1 — bar reaction eccentricity `e`

For the chosen **sourced steel rod d = 6 mm** the peak tip skew is **0.0052 mm**
at an *extreme* eccentricity `e` = the pinion radius (6 mm) — **33x inside** the
gate/2 = 0.175 mm bound; the break-even e is **~201 mm**, far beyond any physical
tooth-contact offset. **R-DND55-1 is closed for the chosen design:** the
eccentricity is irrelevant for the steel rod (it remains an assumption only for
the printed-bar fallback).

## 7. Consolidated residual table (S5-R)

| Residual | Status | Evidence class |
|---|---|---|
| R-DND54-KEEPER (keeper leaf 1 line RISK) | **closed** — re-profiled to 2 lines; hold is a compression shoulder | CAD + CALCULATION |
| R-DND54-6 (writer force unconfirmed) | **closed agent-side** — bottom-up 0.2425 N, sourced class 1.20 N clears 4.95x | CALCULATION + sourced |
| R-DND54-5 (missed set = silent error) | **bounded agent-side** — q <= 1.57e-6; verify/redundancy levers quantified; measured q is the residue | CALCULATION |
| R-DND54-3 (crank 720 deg/s, settle 0.05 s) | **bounded agent-side** — break-evens re-derived; sourced class clears | CALCULATION + sourced |
| R-DND55-1 (bar eccentricity e) | **closed for the steel rod** | CALCULATION |
| R-DND54-4 (multi-row bar/envelopes) | closed for envelopes/pitch ([DND-55](/DND/issues/DND-55)); sourced-rod requirement ([DND-58](/DND/issues/DND-58)) | CAD + CALCULATION |
| R-DND55-4 (rack reconcile) | closed ([DND-58](/DND/issues/DND-58)) | CAD + CALCULATION |
| R-DND54-1 (as-printed friction mu, gate/tip sharpness) | **measurement-only** (un-retirable under DND-27) | — |
| R-DND54-2 (printed-leaf creep/fatigue) | **measurement-only** (un-retirable under DND-27) | — |
| R-DND54-5-q (as-printed per-set q) | **measurement-only** (requirement bounded here) | — |
| R-DND54-3-curve (loaded NEMA17 curve) | **measurement-only** | — |

## 8. What this does and does not claim

- **Does:** retire the keeper RISK by a real re-profile (2 lines + compression
  hold), with the geometry coupling resolved by moving the keeper to the row
  axis; derive the writer force bottom-up and clear it against a sourced actuator
  class; derive the reliability requirement and quantify the agent-reachable
  levers; re-derive the crank break-evens; and close the bar-eccentricity
  residual for the steel rod.
- **Does not:** claim a printed or measured part, a qualified rod, or a measured
  per-set reliability/friction/creep. The **measurement-only** residue is listed
  in §7 and is unchanged.

## 9. Evidence classes used

| Class | Where |
|---|---|
| CAD | `s5r_register.scad` (keeper re-profile + shoulder) and its real-OpenSCAD render |
| CALCULATION | keeper statics + tolerance MC, writer bottom-up, reliability model, crank break-evens, torsion inheritance |
| sourced | printed-PLA compression yield / modulus, FDM 2-line wall limit, actuator class specs |
| **NOT** | print, measurement, purchase |
