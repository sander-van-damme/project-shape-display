# E-303 — Individually selectable friction clutches: feasibility and one finite test

**Owner-commissioned investigation, 23 October 2026.** Repository baseline `c06a663` matched fetched `origin/main` before changes. This result is analytical research, conceptual CAD and a passive print-test package; **no new physical measurements**. DES-009 remains the active development direction. Completion here means the assigned investigation and handoff are complete, not that a clutch has passed.

**Recommendation:** screen candidate A's friction interface first, using measured external normal force. Keep B as a material/contact research alternative and C as a mechanical fallback. No investigated family currently justifies a 6,400-cell build or displacing the traveling motor bank. The hoped-for simple, standard-washer, zero-additional-motion clutch is not established: separating terrain load from clutch pressure requires an explicit compliant force path, and that function must be counted.

## Reading route

| Deliverable | Contents |
|---|---|
| [Owner decision summary](decision-summary.md) | Seven requested decisions, next physical test and stopping point |
| [All-family comparison](comparison.md) | A–H operation, counts, cost, torque/power evidence, failure modes and recommendation |
| [A, C and D engineering](research-electromagnetic.md) | Complete magnetic/axial paths, stationary coil, PCB limits, compliance and fallback mechanisms |
| [B1/B2 engineering and primary research](research-electrostatic.md) | Actual 20-mm research, floating-electrode physics, materials, rotating electrical interfaces and limitations |
| [E–H assessment](sources-rejected-families.md) | Hysteresis, EPM/AlNiCo, MR fluid and powder; evidence for rejecting/deferring them |
| [Calculations and reproduction](calculations.md) | Equations, assumptions, tests and interpretation |
| [Generated tables and plots](analysis/results/tables.md) | Readable results; underlying CSVs preserve scenario detail |
| [Electrical selection](addressing.md) | Matrix counterexamples, local latches, low-voltage circuit, HV channel comparison and full power accounting |
| [Materials, suppliers and cost](components-and-costs.md) | Checked catalogue dimensions/prices, quantity tiers, manufacturing categories and honest exclusions |
| [A drawing](concepts/a-magnetic-concept.svg) / [B drawing](concepts/B-floating-electrode.svg) | Dimensioned sections, top views, exploded stacks, supports, materials and electrical/magnetic paths |
| [Passive physical test](../../../owner-print-tests/2026-10-23-clutch-friction-screen/test.md) | One configured X1C plate, STL/CAD, assembly, measurement procedure and blank results |
| [Verification](../../../tools/curated-experiment-checks/E-303/verification.md) / [technical review](review.md) | Actual completed checks, remaining limitations and review resolutions |

## Question and finite method

Can predominantly printed components and ordinary purchased metal/film/electronics provide independently selectable torque at a 5.08-mm pitch with very few moving functions? Compare all eight families; calculate useful upper bounds and failure sensitivities for A/B; expose their real supports and interfaces in CAD; prepare one low-energy friction test. Do not design a complete shared transmission, launch follow-on experiments or infer performance from CAD.

The decision gates are: adequate torque in both directions, sufficiently small OFF drag, independent axial support, retained height, tolerable heat, repeatable assembly and credible per-pin cost. Low component count matters before peak torque. A larger actuator is not a solution until its **entire envelope**, surrounding shafts, wires and supports can coexist in the array.

## Repository evidence retained

| Existing evidence | Consequence for this work |
|---|---|
| [E-295](../../../06-experiments/E-295-compact-screw-drive-development.md): 4.4-mm pin, nominal 3.2-mm screw, 3-mm lead, 90° profile, 0.9-mm radial thread depth, 6-mm internal engagement | Reuse these dimensions. Nominal radial relief 0.175 mm is CAD geometry, not measured running clearance. The scenario mean thread diameter 2.3 mm is a geometric approximation, swept over 2.0–2.8 mm. |
| E-295 owner report: five compact pairs hand-cycled; three nominal pairs described as very smooth | Qualitative evidence only. It does not provide a torque, friction coefficient or production yield. |
| [E-301](../../../06-experiments/E-301-pico-w-motorcontroller.md): one screw pin moved up/down under motor power | Stronger evidence than a hand fit, still no calibrated torque, load, speed or efficiency. |
| [E-302](../../../06-experiments/E-302-improved-microstepper-test-frame.md): revised frame/CAD/software and later fit feedback | Binding, supports and motor mounting remain real design issues. No new quantitative clutch or screw measurements are invented. |
| [E-296](../../../06-experiments/E-296-compact-matrix-clutch-selection.md), [E-297](../../../06-experiments/E-297-two-half-row-column-clutch-print-tests.md), [E-298](../../../06-experiments/E-298-self-aligning-point-clutch.md), [E-299](../../../06-experiments/E-299-supported-two-cell-selector-retest.md) | Phase alignment, selector strength, positive return, supported screw loads and incomplete matrix selection are relevant failure lessons, not an active task queue. |
| [E-300](../../../06-experiments/E-300-conical-friction-selector.md): contact torque competed with a loaded stationary selector surface | Account for every stationary rubbing interface. Output-side drag reduces useful screw torque; input-side drag increases shared-drive torque/heat. Do not subtract input bearing friction from a prescribed input contact capacity as if it were on the output. |

The active [DES-009 dossier](../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/DES-009-traveling-motor-bank-screw-pins.md) and its component documentation remain unchanged. No functional screw thread is reinvented in this investigation; the passive fixture deliberately isolates friction and does not print another screw.

## Quantitative result that changes the decision

All values below are **conditional estimates**, not measured Shape Display torque. `1 N mm = 1 mN m`.

| Screen | Result | Meaning |
|---|---|---|
| Light screw scenario: 0.05-N weight, 0.01-N guide resistance, assumed thread μ running/start 0.10/0.15 | About **0.053 / 0.060 N mm** running/starting | Even a very light mechanism needs nonzero torque; actual minimum breakaway must be measured. |
| Moderate scenario: 0.2-N weight, 0.05-N guide resistance, assumed μ 0.20/0.30 | About **0.277 / 0.343 N mm** | A clutch sized from only the easiest hand-fit observation could fail useful operation. |
| Loaded/imperfect guide: 1 N plus 0.2-N guide resistance | About **1.63 / 2.20 N mm** | Guide friction, tilt and plastic distortion may dominate; the lumped parasitic term is only a scenario. |
| 4.7-mm annular friction interface, ri 1.1 mm, assumed μk 0.3 | **0.185 N** normal force for 0.10 N mm; **0.926 N** for 0.50 N mm | Modest-looking torque demands substantial controllable pressure at this radius. |
| Standard-part A reference, two 80-turn coils, two 0.10-mm pole gaps and assumed steel/contact reluctance | At 0.4 A: **0.10 N mm ideal ceiling**, **0.55 W** copper loss | Before leakage, unknown material B–H behavior or flexure restoring force. Copper-only initial adiabatic heating is about **13 K/s**; this is not a continuously rated design. |
| B2 floating split electrode, 4.7-mm envelope, 80% active annulus, 12-µm PET, 300 V, assumed μ 0.3 | Ideal gap-closing torque **0.043 / 0.0077 / 0.0010 N mm** at 0 / 5 / 20 µm gap | Zero-gap is a mathematical contact limit. Plain film on FDM cannot be credited with it without measurement. B1 at the same voltage gives four times this ideal value, with a powered output connection. |
| Continuous coils at 0.01–0.5 W each | **64–3,200 W** for 6,400 active channels | Neither 10 mW nor simultaneous full-array operation is an established specification. |

The model includes lowering and backdrive. For the nominal mean thread geometry, `tan(lead angle)≈0.415`; the V-thread friction correction makes the approximate thread-only self-lock threshold μ≈0.294. Actual collars, guides and static friction change that threshold. The light scenario can backdrive. An unpowered slipping clutch does not independently prove height retention.

### Friction needs a window, not one attractive number

Measure `maximum required start torque < minimum ON capacity`, and `maximum OFF transmitted torque < minimum nonselected breakaway torque`, with a margin chosen from actual variation. Also measure useful running torque during slip, both directions, warm behavior and worn behavior. A high ON/OFF ratio alone is insufficient if the OFF torque still moves an almost unloaded screw.

For a 4.7-mm annulus, only 0.02 N residual preload at assumed μ=0.3 gives about 0.0108 N mm OFF drag. Surface wear can polish contact or create debris, adhesive transfer and residual attraction; its direction is unknown. Terrain load must go through the screw's independent thrust support so a pressed pin does not directly increase friction pressure. But those supports introduce their own drag and clearance.

Slipping limits torque only while it actually slips. Under the simplified raising relation, `F≈2πηT/lead`; at T=1 N mm and assumed efficiency 0.1–0.7, that is about 0.21–1.47 N, before guide losses. Static friction, stick-slip, inertia, jamming and pinch geometry prevent interpreting it as a finger-safety guarantee. The 5/20-N obstruction scenarios are calculation probes, **not owner finger tests**. Use weights or a gentle fixture stop.

Slip heat is mechanical power `T·Δω`. At 0.1 N mm and 600-rpm relative slip it is 6.28 mW per contact, or 40.2 W if all 6,400 slip. That heat is additional to winding and electronics losses. Engaged co-rotation has no ideal interfacial slip loss, although bearings and winding losses remain. No measured lifetime is claimed.

## Pitch and staggering: what actually fits

At 5.08-mm pitch, bare 4.7-mm discs leave 0.38 mm between adjacent envelopes; 5.0-mm discs leave just 0.08 mm. Assuming a **0.30-mm total clearance allowance**, the largest one-plane envelope is 4.78 mm. This allowance is a screening assumption, not an X1C tolerance guarantee.

With two checkerboard heights the nearest equal-height neighbor is diagonal: `sqrt(2)·5.08 = 7.184 mm`, so the same allowance permits about 6.884 mm. A 7-mm envelope has only 0.184-mm clearance. With four heights assigned by a 2×2 pattern, the nearest equal-height neighbor is 10.16 mm away; a 10-mm envelope leaves 0.16 mm, below the same allowance.

Different-height discs need enough vertical separation for their **full swept thickness and supports**. More critically, a neighboring 3.2-mm screw shaft crossing the clutch plane gives radial clearance `5.08 − D/2 − 1.6`: −0.02 mm at D=7 and −1.52 mm at D=10. Staggering discs alone therefore does not clear continuous neighboring shafts. Even a 2-mm journal only permits D≤7.56 mm with 0.30-mm radial allowance. The A complete reference package is larger still; B's brushes/supports also extend beyond its bare disc. No pitch-compatible integrated A/B unit is demonstrated.

Larger diameter is useful in a principle fixture to make tiny torques easier to measure. It is not automatically necessary or sufficient in the final architecture: a measured extremely low screw torque could reopen a small geometry, while larger magnetic poles and contacts could still make assembly worse. This is why the finite physical test compares small and large contact areas before investing in actuator refinement.

## Physical test and stop condition

The [one passive fixture](../../../owner-print-tests/2026-10-23-clutch-friction-screen/test.md) uses interchangeable 4.7-/10-mm contact rings, measured normal loads and a torque lever. It asks whether inexpensive surfaces offer a repeatable friction/drag window, continue slipping with output restrained, and survive a short wear screen. Nominal duplicates and clearance variants expose print variation. It does not measure electromagnetic force, electrostatic attraction, screw torque, automatic selection or full-array behavior.

The print handoff records actual Bambu settings, slice/reopen evidence, estimates and status. Three older READY jobs already exist; this package does not silently retire them or add a fourth READY queue entry. An owner can choose the delivered test without this investigation creating reminders or a future work chain.

Further attention away from DES-009 would require a supported screw moving under measured load, measured OFF isolation and height retention, repeatable bidirectional torque/slip after wear, a complete pitch/shaft clearance solution, and a sourced/assembled cost and thermal budget substantially better than the traveling bank. None of those system-level gates is passed here. **Stop after this handoff and await an explicit owner decision.**

