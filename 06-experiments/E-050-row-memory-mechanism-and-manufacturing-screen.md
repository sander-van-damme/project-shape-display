---
status: complete
builds-on: [A-013, A-007, ADR-010, Q-012, E-015]
---

# Row memory: complete-machine necessary-condition screen

## Decision and method

Retain A-013 for bounded **head-cost and contact-geometry synthesis**, not product selection. No examined architecture passes all uncertainty bounds. The distinctive search is positive local rack memory with reusable parallel independent heads, compared with thread-angle memory and trapped-fluid memory. The geometry enumeration optimizes within one topology; it is not 243 new mechanisms.

Input main revision: `73ec9eb`. Inspected preserved checkpoint `5f30a98`: reused its finite schedule/scenario structure, not its results. Added acceleration, actual row-index travel, support transition checks, retention bounds, section geometry and cost sensitivity. This changes its optimistic rack time from 24 s to 29.350 s. No physical measurements, calibrated priors, quoted prices or validated CAD are used.

Executable source: `tools/curated-experiment-checks/E-050/row_screen.py`. Run with Python 3; standard library only. It prints all cases, survivors, failures and summary as JSON. Exhaustive enumeration, no random seed or probabilistic yield estimate. Reproducible output is deliberately not retained.

## Complete alternatives and unexplored boundaries

| Family | Selection, energy and state | Isolation, load, sensing and recovery | Full-scale burden / limitation |
|---|---|---|---|
| Rack A-013 | 80/160 independent linear grippers; individually retractable grounded pawls; tooth state | Only docked targets unlock; gripper carries load until pawl seats; encoder + optical/support read, retry while gripped | 6,400 racks/pawls/returns, ≥19,200 critical interfaces. 80/160 complete channels must fit budget and pitch. Section geometry only; full contact mechanism unresolved. |
| Screw A-007 control | Independent rotary sockets turn 3-mm mean-diameter screws, 1/2/4-mm lead; thread angle stores height | Nut/base carries load, threads must resist backdrive; height reader detects missed turns; re-dock/retry | 6,400 screws/nuts and ≥12,800 thread/socket interfaces. No automatic reopening of rejected A-007; high-lead timing needs a brake or substantiated friction. |
| Trapped-fluid docked piston | Shared pressure/return pump, independent head metering; normally closed mechanically dock-opened cell valves, no row/column sneak-flow matrix | Undocked valves isolate; fluid pressure supports piston. Height readback + closed-valve dwell; re-meter or stop leaking row | 6,400 piston seals and valve assemblies, ≥19,200 critical contacts; pressure source/common contamination faults. Printed sealing and drift unresolved. An added mechanical lock would change the family and must be counted. |

Each can command arbitrary five-state maps in its ideal state model; this does not establish physical reachability. Fluid timing uses an assumed piston speed and double-stroke refill/reset proxy, not a solved pressure network. Screw timing omits angular acceleration and is an optimistic rejection bound. Topologies not searched include magnetic writing, nested binary supports and pressure-driven mechanically latched cells. The generator cannot conclude they lose.

## Bounds and results

75 schedule cases = three families × five lane counts (8/16/40/80/160) × three scenarios, with three leads for screws. Distances mm, time s. Fast/central/slow assumptions: linear speed 400/200/80 mm/s; acceleration 20,000/5,000/1,000 mm/s²; spindle 6,000/3,000/1,000 rpm; contact 0.04/0.08/0.16 s; verification 0.01/0.02/0.04 s; minimum index 0.025/0.05/0.10 s; per-map overhead 2/4/8 s; 0/1/8 extra dwell retries. These are competing bounds, not confidence intervals. Overhead reserves homing, digital preparation, final settling and return registration; no external mask preparation is excluded.

Rest-to-rest motion: `2 sqrt(d/a)` below the triangular/trapezoidal crossover, otherwise `d/v+v/a`. Rack motion enumerates every unequal old/new pair among five states: home→old→new→home, stopping at each contact. The worst case is 40→20 mm (or its reverse), an 80-mm path with three motion segments; fluid uses a two-stroke proxy. Screw uses `40/lead*60/rpm`. Index time is at least physical lane-block travel using the same acceleration bound. Count stations as row groups × column groups, so a 160-head, two-row bank takes three stations for a 5×5 update. Partial-width row-wrap travel is omitted: those already-failing schedules are lower bounds. Jerk, carriage elasticity and read latency remain model discrepancy.

**64/75 timing cases fail; 11 survive timing alone:** rack 2, screw 7, fluid proxy 2. Rack fast 80-head = **29.350 s**, fast 160-head = **16.216 s**; central 160-head = **33.052 s**, failing strictly <30 s. Halving fast acceleration to 10,000 mm/s² makes 80-head time **35.206 s**. No central rack schedule passes. 160-head 5×5 regional times: **3.066/6.752/24.461 s**, conditional on independent channels and unchanged neighbors staying latched. Workload is a worst-case arbitrary map transition (every station can include a 40→20-mm cell), plus a contiguous 5×5 region. Flat unchanged maps require no cell motions; the fixed-overhead schedule is not a no-op estimate. Scattered changes may still require every row; local cost does not always scale with changed-cell count.

Square-thread self-locking requires `mu > lead/(pi*3)`, ignoring collar help. Thresholds 0.106/0.212/0.424; none survives the assumed friction interval 0.08–0.30 robustly. At 0.30, leads 1 and 2 may hold; 4 does not. Adding a brake invalidates the current interface/cost model. This supports retaining the A-007 rejection, not rejecting every screw machine.

Fluid 3-mm bore at assumed 10 N/cell requires **1.415 MPa**. Allowing 0.1-mm drift over a four-hour session requires leakage below **4.91×10⁻⁵ mm³/s per cell**. Both load and drift limits are research assumptions, not product requirements. No leakage prior supports a pass. At 80 simultaneously moving pistons and 400 mm/s, ideal flow is 226,195 mm³/s and ideal hydraulic power 320 W at that load; losses add. Flow and power hardware are not free within the reserve. Stop timing refinement until retention and sealing are credible.

## Manufacturing, geometry and whole-board uncertainty

243 rack section cases enumerate overlap 0.6/0.9/1.2 mm, tooth thickness 1/1.5/2 mm, three error envelopes, modulus 500/1,500/3,000 N/mm² and loads 1/10/100 N. Rigid cross-section model: 2.4-mm rack web, 0.8-mm support wall, 1-mm cantilever reach, 2.4-mm tooth width, 10-mm tooth spacing. Check residual overlap ≥0.4 mm, lateral envelope ≤5.08 mm, section stress ≤8 N/mm² and deflection ≤0.1 mm. Limits and moduli are explicit scenario bounds, not PLA strength/stiffness evidence or qualified X1C dimensions.

Adverse relative error sums print-wide bias + regional warp/alignment + local fit: tight 0.05+0.05+0.05=0.15 mm; middle 0.10+0.10+0.15=0.35 mm; wide 0.20+0.20+0.20=0.60 mm. Common terms apply to every affected cell, not independent draws. Hole shrinkage, wall variation, layer quantization and roughness are aggregated into fit/section uncertainty; first-layer interference must be excluded from future working faces. No fatigue, creep or wear distribution is invented. The modulus/stress envelope only screens initial elastic behavior and cannot certify long-term support.

48/243 sections pass: tight 36, middle 12, wide **0**. None robustly passes all bounds at 10 N; none carries 100 N under the section stress limit. A representative middle-error survivor is overlap 0.9 mm/tooth 2 mm at 10 N: residual overlap 0.55 mm, envelope 4.80 mm, stress 6.25 MPa and deflection 0.00417 mm at E=500 MPa. Independent bound: overlap≥0.4+error and overlap≤1.88−2error imply error≤0.4933 mm for *any* overlap in this single-plane section. Therefore the wide-envelope failure is not merely coarse grid spacing. Wider staggered internal latches escape this constraint and remain open.

This is generated 2D support-section evaluation, **not** swept-volume/contact CAD. The 25 old/new state transitions check ideal support order latch→latch+grip→grip→grip+latch→latch and ≤80-mm path. They do not verify that geometry can execute that order. Base-grid deflection, seam preload, buckling, impacts and neighboring-column friction are excluded and require later models. E-015's 100-N incidental load is retained as sensitivity, not imposed as a new mandatory per-cell requirement.

False acceptance matters independently of retry: per-cell rates 10⁻³/10⁻⁴/10⁻⁵ imply expected 6.4/0.64/0.064 missed cells per board by linearity, without independence assumptions. A single shared reader/registration failure can misaccept an entire 80-cell row. No distribution or board reliability is claimed. Retries cannot repair a common bias; sustained faults stop the affected bank, so successful-update times exclude unrecovered faults.

## Cost, manufacture and conditional frontier

54 budget scenarios enumerate common-hardware reserves $150/250/350, 80/160 heads at $1/3/6 per **complete** channel, and $0/0.02/0.05 purchased parts per cell. Ten combinations are ≤$500; these are budget feasibility cases, not costed products. Reserve must cover frame, guides, transport, drivers/control, supply, wiring, sensors, fasteners and pump where applicable. At $250 reserve and free cell hardware, 80-head allowance is $3.125 each; 160-head allowance $1.5625. A $0.05 cell part alone adds $320. Any omitted item reduces these allowances.

A solid 2.4×2.4×60-mm column allocation is 2.212 litres for 6,400 columns before tops, racks, pawls, guides or grid. At assumed deposited rates 5–15 mm³/s, that allocation alone is 41–123 print hours; infill, orientation, waste, travel and reprints are unresolved. If per-cell insertion/inspection consumes 10–30 seconds, assembly alone is 18–53 hours. These sensitivity estimates penalize apparently free printed parts. All architectures need modular construction for X1C build volume, accessible underside repair and full 40-mm travel plus support/head depth; no compactness claim is established.

Conditional frontier: 80 rack heads trade lower channel cost for fragile timing; 160 buy timing margin only in the fast scenario. Screw has faster favorable motion but weaker bounded retention. Fluid offers shared energy but unbounded leakage, pressure and sealing burden. There is **no demonstrated feasible Pareto set** across hard constraints; cost-envelope feasibility does not erase missing geometry/retention evidence.

## Verification and next decision

Executed source assertions check zero-distance and triangular/trapezoidal motion limits, a separate hand-computed full-row timing expression, regional station counts, all 25 state transitions and absence of 100-N section survivors. Analytical overlap feasibility independently explains the wide-error result. This is self-review, not independent validation. No convergence claim is needed for exact finite enumeration; continuous geometry optima outside enumerated bounds remain open.

Next: resolve complete head cost and generated contact transitions before further timing optimization. Compare staggered wider supports and shared-elevator grippers only if selection, energy, isolation and reset are explicitly implemented. Stop expensive head embodiments outside the budget envelope; reopen failed sections with wider internal support or tighter evidence-backed bounds. No print request: current failures are architectural/model questions, not yet a decision-relevant calibration opportunity.
