---
status: complete
builds-on: [E-050, E-051, M-015, ADR-010, A-015, A-016, A-017, A-018, A-019, A-020, A-021, A-022, A-023]
---

# Cross-physics complete-machine screen

Broaden the discovery portfolio without choosing a product architecture. Retain
three priority investigations: magnetic command memory with mechanical power,
electroadhesive **low-force command** clutches with positive service support,
and common-pressure corrugated cells with mechanical latches. Binary structural
layers and microvolume phase-change collars remain distinct bounded reserves.
No candidate has passed a complete feasibility, sourcing or reliability gate.
A-015–A-023 define causal machines and their missing implementation evidence;
this result supplies the shared calculations and compact comparative landscape.

Input main `81c72cd`; Python standard library:
`python3 tools/curated-experiment-checks/E-063/landscape.py`.
Use `--all` for full generated populations/rejection reasons. JSON is reproducible
and not retained. Deterministic exhaustive grids, no random seed or invented
yield probabilities. Sources were accessed 2026-10-08. Evidence is literature,
analytical necessary bounds, abstract contact replay, and kinematic synthesis;
there are no physical measurements, qualified CAD or calibrated FDM priors.

## Landscape and decision

| Family | Repeated-site burden / changed principle | Evidence and dominant unknown | Disposition and next discriminator |
|---|---|---|---|
| Mechanical mask A-011 / load-grid A-012 | Physical information media and grounded support | Prior stiffness/isolation findings; inherited timing is not a new pass | Reference only; no protected status |
| Rack A-013 | Pawl, return, guide; many reusable positioning heads | E-059 priced servo route fails; support geometry/cost unresolved | Reference; do not deepen another pawl detail before new families |
| Shared shaft A-004/A-006; rotary A-005/DES-004 | Mechanical coupling or stepped support | Existing rejection/supersession retained | Negative/reference cases, no reopening from documentation age |
| XY magnetic writer ADR-010 | Passive latch; serial external writer | Rate was borrowed, not a magnetic measurement | Reference, not duplicated by A-016 |
| Hydraulic memory A-014 | 6,400 sliding seals/valves, fluid state | E-060–062 half-selection and rail support | Distinct reference; retain original gates |
| A-015 electroadhesion | Two command contacts/active circuits plus pawl/collet | Gap-sensitive ideal force; no complete HV-array cost | **Bounded → deeper selector study**, only low-force command role |
| A-016 magnetic toggle | Two flags, local flux returns, mechanical couplings | 5/9 threshold scenarios have a window; no field solution | **Bounded → deeper field/cost study**; reject overlapping half-select intervals |
| A-017 thermal unlock | ≥6,400 wires and 12,800 terminations plus flags | Serial schedule and long-wire price fail; shortest wire remains possible | **Bounded**, retain short-stroke alternative only; no row-serial development |
| A-018 phase-change collar | Cup/seal/heater/alloy and moving grip | Energy spans 100×; freeze support/cross-talk unproven | **Bounded reserve**, discriminate minimum load-bearing volume |
| A-019 temporal jamming | Many foil interfaces and retained wedges | Temporal capture shares the dual-clamp topology; vacuum alone lacks independent selection | **Bounded**, merge schedule research; no extra “architecture count” for timing alone |
| A-020 shared pressure | Bellows/spring/pawl; no cell valves or sliding seals | Flat sheet fails travel; corrugated sheet and pressure window open | **Bounded → deeper geometry study**, before pumps or printing |
| A-021 geometric amplification | ≥26 bars/site in best planar grid case | High reaction/assembly; 13+ stages and no pivot packaging | **Bounded/deprioritized**; stop planar-grid refinement, retain other topologies |
| A-022 structural bitplanes | Three full-load stages/site | 25 state transitions reachable; moving-layer drive access unresolved | **Bounded reserve**, solve offset-invariant coupling before claiming machine |
| A-023 sparse sheet | 81–324 jacks rather than 6,400 pins | Good smooth-hill interpolation; walls/steps/locality lost | **Counterfactual bounded; incompatible with current product**, no requirement change |

A-015/016/017 share elevator mechanics but change selection/state/wiring;
A-019 reuses capture timing with friction memory. A-020 recombines magnetic
selection with pressure; A-021/022 change structural memory. A-023 changes the
product degrees of freedom. Parameter populations are not new architectures.

## Shared loads, cost and support-transfer schedule

Keep the stage-02 field: 80² sites, 5.08-mm pitch, 40-mm travel, <30 s complete
update and unchanged-region support. Five heights 0/10/20/30/40 are a test
workload, not a requirement restricting eventual resolution. Unqualified force
scenarios are 0.05/0.2/1 N transient per pin and 1/10 N local service; 10 N at
every pin simultaneously is an intentionally severe sensitivity case, not a
required 64-kN tabletop capacity. Aggregate force is 320/1,280/6,400/64,000 N
and ideal 40-mm work 12.8/51.2/256/2,560 J. Moving frame, friction, acceleration,
return springs and drivetrain losses are additional. Separating latch release
(0.05 N scenario) from support does not make payload lifting free.

At $250 shared reserve, $400/$500 permit $0.02344/$0.03906 for **all bought
local parts/site**; the reserve already exceeds $200. Reserve $150/$350 adds/
subtracts $0.015625/site. These are ceilings, not market floors. Unsourced
film/magnet/diaphragm cost floors are unknown, not zero. Supplies, drivers,
readers, harnesses, rails and fasteners must be allocated once. Two channels
or three bitplanes divide that allowance. At 10–30 s assembly/site, insertion/
inspection takes 17.8–53.3 hours before rework. A 100-mm, 2.4-mm-square solid
tail alone uses 3.69 litres/board before tops/supports; printed is not free.

**Full-field long-tail support sequence (distinct from E-051):** preposition
the unloaded elevator 0→40 mm. Grip changed nonzero pins, unload/release their
ground pawls, descend and deposit each pin at zero when elevator displacement
equals its old height. Ground support re-engages before moving grip releases.
At elevator zero, reacquire changed pins with nonzero targets, ascend and
transfer each to ground support at its target. Unchanged pins stay grounded.
Long tails allow grip at differing old heights; contact coverage/force are
unverified. Local updates may still require the complete shared stroke.

`move(d)=2 sqrt(d/a)` for triangular rest-to-rest travel, otherwise
`d/v+v/a`, with assumed v=100 mm/s and a=500 mm/s². Count preposition 40 mm,
eight stopped 10-mm legs, nine full-field contact events and 6 s for map
preparation, registration, scan, final settling and bounded recovery:
`T=move(40)+8 move(10)+9 dwell+6`.
At 0.02/0.2/1.4-s event dwell this is **9.043/10.663/21.463 s**. These are
conditional allocations, **not achieved times or universal lower bounds**.
Each dwell includes grip, unload microtravel, selector programming, relatch,
proof and reset; a one-second thermal pulse alone does not satisfy a 1.4-s
complete event. No substep may be silently overlapped on the common elevator.
A second full thermal command phase can exceed this budget. At 80 serial row
writes/event the available combined row interval is <29.36 ms before other
event work, so ordinary one-second SMA scanning is excluded.

Full-field parallel mechanics replace E-051's 40 stations with 6,400 couplers
and larger force/frame burden. The script replays 25 height pairs, unchanged
states and failed transfer guards. Failed acquisition keeps ground support;
failed deposition keeps moving support and stops. These commanded invariants
do not prove contact force, long-tail access or affordable grip geometry.

## Selector, thermal and pressure calculations

**Electroadhesion:** 36 cases: film 10/25/50 µm, air gap 0/5/20 µm,
200/500 V, friction 0.2/0.5, relative permittivity 3, area 40 mm².
Ideal series-gap pressure `epsilon0/2 [V/(g+t/3)]²`; friction force is `mu*p*A`.
Range 0.00105–1.992 N; 12 cases reach 0.05 N, one reaches 1 N, none 10 N.
This optimistic area/friction model omits peeling, roughness distribution,
polarization and leakage; the 0-gap limit is an ideal closing-gap limit, not
qualified contact. Ideal dielectric field spans up to 50 MV/m, with no accepted
breakdown margin. Shared contamination/batch film thickness can degrade every
site together. Passive half-voltage friction would remain one-quarter nominal,
not zero; the candidate charges active isolation/retention hardware instead.
[Rauf and Follmer](https://arxiv.org/abs/2412.16803) demonstrate rapid release
in carefully driven electroadhesive clutches and explain why ideal electrostatic
dynamics alone are inadequate. Their timing is not transferred to dirty printed
pin guides. Low-force command plus mechanical collet is the next mutation.

**Magnetic coincidence:** ideal normalized full/half fields 2/1, relative
field error e=0.05/0.15/0.25 and threshold spread d=0.05/0.15/0.30 require
`(1+e)/(1-d) < threshold < 2(1-e)/(1+d)`. Five of nine windows survive;
e=d=0.15 gives 1.353–1.478, while d=0.30 has none. This necessary condition
must include neighboring pulses, remanence/current droop and batch/local gap
errors. A-016 adds ideal air-gap force/ampere-turn bounds, not a field solution.
[Flip-latch Braille work](https://ieeexplore.ieee.org/document/8952768/) is a
mechanism lead from its accessible indexed abstract; no numerical capability
is borrowed. Full crossed-flux geometry is the next gate.

**Thermal release:** A-017 records sourced wire energy/cost floors. Short
release travel must still clear the correlated geometric error envelope;
E-050's dimensional bounds are not SMA strain distributions.

**Phase change:** 27 cases with volume 0.5/2/10 mm³, effective heat
0.2/0.5/1 J/mm³ and site-to-sink conductance 0.002/0.02/0.2 W/K. Material
properties are deliberately labelled bounds; no alloy is assigned invented
precision. Board heat is 0.64–64 kJ. With at most 20 K driving temperature,
`Q/(20G)` gives optimistic cooling bounds 0.025–250 s, ignoring approach to
ambient and supercooling. A representative 2-mm³, 0.5-J/mm³ collar gives
6.4 kJ, >213 W average rejection at 30 s, and ≥2.5 s cooling at G=0.02 W/K.
Warming/moving/re-freezing again increases map heat and time. Thus heat alone
does not reject every microcollar; large/poorly cooled embodiments fail.
Diffusion distance `sqrt(alpha*t)` at 30 s for assumed alpha=0.1/10/100 mm²/s
is 1.73/17.3/54.8 mm: a metallic cooling bridge can couple many pitches. This
is a length scale, not a neighbor-temperature prediction. No uniform thermal
independence or qualified long-term collar strength follows.

**Jamming and pressure:** A-019 derives 25 ideal friction interfaces for 10 N;
A-020 derives 28.3 kPa for 0.2 N at a 3-mm bore, 1.81 litres displacement and
4.67 kN plenum-cover reaction. The executable reproduces these bounds and the
694% taut-sheet extension failure. Corrugations change the geometry and remain
unresolved; pressure area does not supply independent site selection.

## Structural synthesis and fidelity counterfactual

Scissor synthesis generates 1,944 cases over 3/4/5-mm bar lengths, lower
angles 10/20/30°, upper angles 65/75/85°, 1–24 stages and error envelopes
0.15/0.35/0.60 mm. Width/travel equations and witness are emitted by the source. Reject
1,781 cases; tight/middle/wide envelopes retain 96/37/30 with minimum 13/17/17
stages. Virtual work independently gives the low-angle force ratio n cot(angle).
Straight-link swept width is checked, not finite-width joints, contact or
bistability. No survivor is qualified geometry; stop this planar grid.

Binary layers require 19,200 stage sites. All 25 clear-before-set transitions
reach their endpoints without exceeding the larger endpoint; some descend
below both. Six ideal stroke passes take ~2.57 s before addressing, support
transfer, rail access, homing/readback and settling. A-022 specifies those
missing paths; bit reachability does not establish drive accessibility.

Sparse comparison uses bilinear interpolation at node spacings 1/2/5/10 cells,
all paired x/y offsets (not independent phases), and fixed edge nodes: 72 deterministic workload cases. Inputs:
smooth `20+10 cos(2πx/79)cos(2πy/79)` mm hill; x=39 single-cell 40-mm wall;
x≥40 step; and 0/40-mm checkerboard. This samples prescribed heights at jacks;
it is neither optimal least squares nor a physically solved membrane. The
adversarial null-space wall and continuous slope limitation survive that
qualification; RMS values are only for this reconstruction method.

| Node spacing | Actuators including edges | Hill RMS mm | Wall RMS mm | Step RMS mm | Checker RMS mm |
|---|---:|---:|---:|---:|---:|
| 5.08 mm | 6,400 | 0 | 0 | 0 | 0 |
| 10.16 mm | 1,681 | 0.0189 | 3.16–4.47 | 2.24 | 28.28 |
| 25.4 mm | 289–324 | 0.125–0.129 | 4.47–6.93 | 2.83–4.90 | 21.30–21.49 |
| 50.8 mm | 81–100 | 0.449–0.504 | 4.47–10.68 | 4.12–7.55 | 27.25–28.28 |

Global RMS hides lost walls: maximum error reaches 40 mm. Coarse grids lose
narrow walls/pits and create slopes under miniature bases; changed-node influence
extends two node intervals per axis before elastic nonlocality. A-023 states
D&D stability, fog-of-war, cost and repair implications. Smooth terrain is a
credible separate product opportunity, not authorization to replace independent
columns. No actuator-rate, sag or lifetime claim comes from interpolation.

## Uncertainty, verification and stopping rule

Geometric error uses E-050's labelled tight/middle/wide sums of batch bias,
spatial alignment/warp and local fit. No scenario is an X1C accuracy prior.
Layer quantization, wall error, hole shrinkage and first-layer interference
must enter detailed geometry; thin foil and bellows require different processes.
Friction/thermal/magnetic extremes are epistemic scenarios applied coherently
across the board, not 6,400 independent random draws. PLA orientation, creep,
fatigue and wear remain unbounded failure modes, so no service-life/yield
ranking is asserted. Optimistic nominal survivors can fail a shared bad batch.

All dense candidates require underside readback plus support proof; the 6-s
schedule reserve is not a reader implementation. Occlusion and scanner access
remain gates. At assumed per-site false acceptance 10⁻³/10⁻⁴/10⁻⁵, expected
misses are 6.4/0.64/0.064 without independence; shared registration error can
corrupt rows. Persistent faults stop modules, outside successful-update timing.
Retries cannot repair common bias.

Self-review checks zero/crossover motion limits, an electrostatic hand case,
dense-grid exact reconstruction, endpoint reach and support guards. Closed
forms need no time-step convergence. No contact/mesh or independent validation
is claimed. Run repository checks and inspect the full diff before integration.

Stop this first-order campaign after the initial screen of every requested
family. ADR-012 records continuation/rejection conditions. No feasible Pareto
winner, hardware release or print proposal follows from these necessary bounds.
