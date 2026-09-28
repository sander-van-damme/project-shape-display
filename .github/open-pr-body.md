# DND-43: convergence Step 6 — load, structure and power (spliced beam + drive + power-cut)

## What changed

- **New experiment** `06-experiments/test13_step6_load_structure_power/`:
  - `model.py` — analytic/simulation Step-6 model: spliced full-span beam + dummy
    platen at modelled column mass; lift torque-speed margin; flatness support
    spacing; power-cut behaviour; terrain patch load.
  - `checks.py` — CI regression + honesty gates (the failing lift gate is
    encoded as a green check so a reader cannot mistake the Step for all-pass).
  - `README.md` — the disposition for S3 / S4 / S5.
- `06-experiments/README.md` — index + reproduce line for Test13 (and Test12).
- `07-evidence-and-decisions/README.md` — evidence-matrix row + findings summary.
- `07-evidence-and-decisions/convergence-plan.md` — Step-6 closure note.
- `08-current-design/README.md` — §6 support-spacing text, BOM lift-screw note,
  risk register R5–R8, and next actions updated with the Step-6 corrections.
- `.github/workflows/ci.yml` — runs `test13/checks.py` and `test13/model.py`.

## Engineering question

Does the shared-lift structure of the surviving field carry the whole moving
mass and hold its flatness, does the lift motor have a real torque-speed margin,
and what happens on a power cut — modelled for the **S5 winner** and screened
for the **S3 / S4** family, which share the same common lift?
(Convergence plan §3, Step 6.)

## Evidence produced (calculated / simulated — no print, no measurement, DND-27)

All 8 rails 20×30×2 mm hollow tube, `I = 21,565 mm⁴`. Splice modelled as a
midspan plug with stiffness ratio `k = 0.25` (assumed, not measured).

**Moving mass / force**
- Column 2.178 g each; 6,400 columns 13.94 kg; +4 kg platen → 17.94 kg.
- Total lift force **275.6 N** (weight with 0.2 m/s² accel + guide drag).

**Structure / flatness**
| Case | E=700 MPa | E=2500 MPa | Gate 0.25 mm |
|---|---:|---:|---|
| Unsupported 401.3 mm, monolithic | 1.921 mm | 0.538 mm | FAIL |
| Spliced @ 203.2 mm | **0.514 mm** | 0.144 mm | FAIL (soft) / pass (bulk) |
| Spliced @ 101.6 mm | 0.097 mm | 0.027 mm | pass |
- Max spliced span at soft E = **151.4 mm**.
- Spliced vs monolithic on the same span = **2.1×** — the splice term matters.

**Lift torque-speed** (T8, 4 screws, η=0.30, motor 0.30 N·m running allowance)
| Lead | Worst-screw torque | Running margin |
|---|---:|---:|
| 8 mm (Test09) | 0.585 N·m | **0.51×** FAIL |
| 4 mm | 0.292 N·m | 1.03× FAIL |
| 2 mm | 0.146 N·m | **2.05×** PASS @1050 rpm |

**Power cut**: 8 mm lead angle 17.66°, `tan λ = 0.318 > μ ≈ 0.15` → **not
self-locking**. 1 mm unload clearance buys ~14 ms before toe impact. A
friction brake / platen detent is required.

**Terrain load**: 20 %-map patch at 1 N/cell → 11.31 MPa rib stress vs 45 MPa
PLA yield — not a frame killer at the service load.

## Disposition

Step 6 **kills no survivor**. It corrects the winner spec and adds two shared
rules:

- **S5** stays the winner, with: support spacing ≤ ~150 mm (3 cartridges/axis)
  or a stiffer rail; lift lead ≤ 2 mm or a larger motor; a mandatory power-cut
  brake/detent.
- **S3** gets the same lift rules; still killed on cost/printability (the
  pivot-clearance gate is now analytically `S3_DENSITY_PRINTABLE`, PR #30).
- **S4** gets the same rules per tile group; still parked on bus backlash.

## Passed / failed

- PASS (local): the entire CI script set, including the new Test13 checks.
- FAIL (design, by design): the 8 mm lead torque-speed gate — recorded as
  evidence, not hidden.

## Assumptions / what remains uncertain

- Splice stiffness ratio `k = 0.25` is **assumed** and is the dominant unknown
  (R5). A higher `k` relaxes the spacing to 203.2 mm.
- As-printed rail modulus (700 vs 2500 MPa) spans the pass/fail line (R6).
- Sourced lift-motor torque at speed (0.30 N·m) is representative, not
  sample-verified (R7).
- The power-cut brake/detent is not yet in the BOM or the timing budget (R8).

## Next test

Fold the brake/detent and the re-sized lead into the winner BOM + timing
budget, and update the CAD support layout to 3 cartridges/axis (CostMfg /
Fabricator follow-up).

## Links

- Source issue: [DND-43](/DND/issues/DND-43); parent [DND-35](/DND/issues/DND-35).
- Policy: [DND-27](/DND/issues/DND-27) (no print); [DND-19](/DND/issues/DND-19) (agent merge).
- Prerequisite landed: [PR #30](https://github.com/sander-van-damme/project-shape-display/pull/30) (S3 pivot clearance) merged to `main`.
