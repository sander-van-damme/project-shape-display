# Test 13 — Convergence Step 6: load, structure and power (DND-43)

**Question.** Does the shared-lift structure of the surviving field carry the whole moving
mass and hold its flatness, does the lift motor have a real torque-speed margin, and what
happens on a power cut — modelled for the **S5 winner** and screened for the **S3 / S4**
family, which share the same common lift?

**Evidence class.** CALCULATION / SIMULATION over sourced material and drive figures and
stated assumptions. **Nothing here is a print and nothing here is a physical measurement**
([DND-27](/DND/issues/DND-27)). This is the analytic/simulation artefact the convergence
plan calls for at Step 6
([`07-evidence-and-decisions/convergence-plan.md`](../../07-evidence-and-decisions/convergence-plan.md) §3 Step 6).

Run:

```text
python model.py     # prints the Step-6 stack-up
python checks.py    # regression + honesty gates (findings encoded, incl. failures)
```

## 1. What the earlier model missed

Test08/Test09 model the platen/frame as a **monolithic** beam with the full 406.4 mm span
or **203.2 mm** as a free span, loaded by `5 w L^4 / 384 E I`. That is optimistic in one
specific, load-path-relevant way: **the field exceeds the 256 mm X1C bed, so it is printed as
cartridges and bolted at splices.** A bolted splice at midspan is a stiffness
discontinuity, and midspan is exactly where the moment (and curvature) peak. This Step adds
the splice term and reports the support spacing the flatness budget actually allows.

## 2. Moving mass and lift force (calculated)

| Quantity | Value | Basis |
|---|---:|---|
| Column mass, each | **2.178 g** | 4.68 mm square × 80.2 mm solid, PLA 1.24 g/cm³ (Test08 geometry) |
| 6,400 columns total | **13.94 kg** | calculated |
| Dummy platen (modelled) | **4.0 kg** | mid of the Test09 2–6 kg band |
| Moving mass | **17.94 kg** | calculated |
| Lift accel | 0.20 m/s² | Test09 `lift_accel_mm_s2` |
| Guide drag | 6,400 × 0.015 N | Test09 `guide_drag` + drag band |
| **Total lift force** | **275.6 N** | weight(1.02 g) + drag |

## 3. Structure — spliced, not monolithic (calculated)

Rails: **8 × 20 × 30 mm hollow tube, 2 mm wall** (Test09 coupon section),
`I = 21,565 mm⁴` each. Load distributed equally.

| Case | Soft printed E = 700 MPa | Bulk E = 2500 MPa | Gate |
|---|---:|---:|---:|
| **Unsupported 401.3 mm span**, monolithic | **1.921 mm** | 0.538 mm | 0.25 mm → **FAIL** |
| Spliced @ 203.2 mm support spacing | **0.514 mm** | 0.144 mm | **FAIL at soft E** / pass at bulk E |
| Spliced @ 101.6 mm support spacing | **0.097 mm** | 0.027 mm | pass |

**Finding S-1 (support spacing):** at the *soft printed* modulus the 203.2 mm spacing
assumed in [`08-current-design`](../../08-current-design/README.md) §6 does **not** meet the
0.25 mm flatness gate once the splice is modelled (`0.514 mm > 0.25 mm`). The largest
spliced span that meets the gate at soft E is **151.4 mm**. The design lever is therefore
either (a) support spacing **≤ ~150 mm** (i.e. the 406.4 mm axis is split into **3
cartridges/axis**, not 2), or (b) raise the as-printed rail modulus toward the bulk PLA
value (stiffer geometry / higher infill / fibre), for which 203.2 mm passes with 0.144 mm.

**Finding S-2 (the splice is real):** on the same 203.2 mm span the spliced model gives
0.514 mm vs the monolithic 0.249 mm — a **2.1×** penalty. A plain `5wL⁴/384EI` number is
not a safe structural proxy for a bolted cartridge frame, so future structure claims must
name the splice stiffness assumption (here `k = 0.25`, **not measured** — the dominant
unknown of this Step).

## 4. Lift drive — torque-speed margin (calculated) — **FAILS at the baseline**

T8 lead-screw, 4 screws, η = 0.30, sourced $18 planetary NEMA17 allowance, representative
running torque **0.30 N·m** on a 24 V bus (assumption; the unit is not sample-verified).

| Lead | Screw total torque | Worst-screw (2× unbalance bound) | Running margin | Hold margin | Screw rpm @ 35 mm/s |
|---|---:|---:|---:|---:|---:|
| 8 mm (Test09 baseline) | 1.170 N·m | 0.585 N·m | **0.51×** FAIL | 0.68× FAIL | 262 |
| 4 mm | 0.585 N·m | 0.292 N·m | **1.03×** FAIL (<1.5) | 1.37× | 525 |
| **2 mm** | 0.292 N·m | 0.146 N·m | **2.05×** PASS | 2.74× | 1050 |

**Finding P-1 (recovery lever):** the Test09 8 mm lead cannot be lifted by the sourced
motor allowance — margin **0.51×**. Dropping the lead is the cheap fix: **2 mm lead**
gives 2.05× running margin at 1050 rpm, inside a 1200 rpm small-bearing bound. This is a
*motor-allowance* finding, not a physical one; the alternative lever is a larger/more
expensive motor. The design must **not** carry the 8 mm lead into the BOM without a
re-sized motor.

**Finding P-2 (power cut):** at 8 mm lead the lead angle is `atan(8/(π·8)) = 17.66°`, so
`tan λ = 0.318 > μ ≈ 0.15` — **the screw is not self-locking**. A power cut at the top of a
stroke back-drives the 17.94 kg platen under gravity. The 1 mm unload clearance buys only
**~14 ms** before the column toes would land on the rotors (impact 0.140 m/s). A
**friction brake or a platen detent is therefore required** to hold the platen on power
loss; the 26.25 s timing budget does not currently include a power-cut recovery step.

## 5. Terrain patch load (calculated)

A miniature loads only the raised hard stops, so the frame sees a local patch, not the whole
platen. A 20 %-of-map patch at the 1 N service load gives **11.31 MPa** rib bending stress
vs the 45 MPa PLA yield (ratio 0.25) — **not a frame killer** at the product service load.
This deliberately does **not** cover the 5 N abuse screen (a handling screen, not a gate).

## 6. Disposition for the S3 / S4 / S5 family

All three survivors share a **common lift**, so structure/power is a **family** question.
Step 6 therefore does **not** kill S3/S4/S5 as architectures; it kills or bounds concrete
design *details* and hands the winner a corrected specification:

| Candidate | Step-6 effect | Status after Step 6 |
|---|---|---|
| **S5** (winner) | Forces two spec changes: support spacing ≤ ~150 mm (or stiffer rail) and lift lead ≤ 2 mm (or bigger motor); adds a mandatory power-cut brake/detent. | stays the winner, **with a corrected structure/drive spec** |
| **S3** (multi-row head) | Same lift/structure findings apply; S3 additionally carries a **moving head** (~1.2 kg assumed) on long rails, worsening the rail-mass and motor sizing. The pivot-clearance gate is now analytically `S3_DENSITY_PRINTABLE` ([PR #30](https://github.com/sander-van-damme/project-shape-display/pull/30), [DND-4](/DND/issues/DND-4)). | still **killed on cost/printability**, not on structure; Step 6 does not revive it |
| **S4** (shared-bus tiles) | Tile-local lifts avoid the single large platen, but the same splice/modulus and lead-screw rules apply per tile group; the bus-backlash gate from [DND-4](/DND/issues/DND-4) still binds. | stays **parked** |

**Nothing in Step 6 kills a survivor on structural grounds.** The Step's output is a
**corrected specification** for the winner and two inherited rules (spliced spacing,
torque-speed) for any sibling that keeps a common lift.

## 7. Residual uncertainty / risk register additions

| id | Risk | Class | Status |
|---|---|---|---|
| R5 | Splice stiffness ratio `k = 0.25` is **assumed**, not measured | assumption | open — drives the ≤150 mm spacing finding; a higher `k` relaxes it to 203.2 mm |
| R6 | As-printed rail modulus (700 vs 2500 MPa) spans the pass/fail line at 203.2 mm | assumption | open — same class as the existing printed-process risks |
| R7 | Sourced lift motor torque at speed (0.30 N·m) is representative, not sample-verified | assumption | open — Step 6 shows the whole drive sizing depends on it |
| R8 | Power-cut brake/detent is **not** in the current BOM or timing model | calculation + assumption | open — new required item surfaced by Step 6 |

## 8. Links

- Plan: [`07-evidence-and-decisions/convergence-plan.md`](../../07-evidence-and-decisions/convergence-plan.md) §3 Step 6.
- Winner: [`08-current-design`](../../08-current-design/README.md) (S5) — §6 support/frame text is superseded by Finding S-1.
- S3 gate: [PR #30](https://github.com/sander-van-damme/project-shape-display/pull/30), [DND-4](/DND/issues/DND-4).
- Source issue: [DND-43](/DND/issues/DND-43); parent convergence [DND-35](/DND/issues/DND-35).
