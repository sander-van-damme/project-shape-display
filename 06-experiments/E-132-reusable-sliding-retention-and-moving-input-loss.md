---
status: complete
builds-on: [E-131, E-129, E-125, E-127, E-128]
---

# Reusable friction heads fail moving arrest or dense routing in this comparison

**Stop the solid rotating-screw head and counterbalanced permanent-pad head under
the stated bounds.** Reuse reduces screw inventory, but rotor energy remains when
low load weakens frictional arrest. Pad drag is inadequate at opposite spring/load
corners. A new transverse-pin route clears two adjacent outputs but intersects a
third unchanged row. Failures apply to these embodiments, not all screws or friction
materials. No complete machine is admitted; no printing or purchase is justified.

Input main `b790ab9`. Reproduce: `python3 tools/curated-experiment-checks/E-132/heads.py`.
Standard library; JSON is reproducible and not retained. Evidence: finite rigid
output/contact prisms, conservative drive envelopes, analytical dynamics and
numerical consistency checks. No complete drive CAD, qualified capture/controller,
process prior, physical measurement or independent review.

## Causal machines and support continuity

Both writers translate a grounded assembly 4 mm laterally to insert a rigid pin
through a moving column eye. Its upper face lifts the eye; the opposite wall
provides finite bilateral containment with backlash. A separate stationary pin
supports nine column positions 0–40 mm at 5-mm intervals while the writer is absent.
These are test levels, not a new product-resolution requirement.

- **Screw:** an antirotating nut/carriage moves on a continuously engaged square
  thread; thrust bearings/frame ground the screw. Rotation changes height, and
  thread friction supplies conditional retention. Bearings, antirotation rails,
  motor and lateral writer arrest are unbuilt, not supplied by freezing the input.
- **Pads:** the carriage joins a rail between two permanent opposing pads. Ground-
  backed compression springs apply normal force; an upward constant-force spring
  assists a bilateral drive. Pad reactions and spring anchor return load to ground.
  Drive, coil, lateral arrest and frame connections remain unbuilt; reflected drive
  inertia is a bounded variable.

Centered writer-pin insertion leaves stationary support intact. Raising .25 mm
reaches the eye ceiling; another .25-mm lift unloads the stationary pin before its
4-mm withdrawal. Reverse these contacts at a target indexed position. Raising,
reversal and loaded lowering retain the same load-bearing eye-ceiling/pin pair
while column reaction stays positive. No brake or thread releases. The lower eye
wall contains upward escape only after clearance take-up; no zero-backlash coupling
is claimed. Failed insertion must retain stationary support; failed handback must
retain the writer. Actual actuators, horizontal loss retention, proof sensors and
fault guards are unresolved. False capture/stop readback can release sole support.

The vertical counterexamples **grant** intact coupling and ideal guides to test
whether even that favorable subsystem arrests; these grants do not admit the
machine. Moving loss sets motor torque to zero and allows input motion. Electrical
shorting, motor detent and bearing friction receive no credit.

## Finite access: isolated pair clears, dense replication fails

The source constructs solid prisms in mm: 4.6-mm square tops at (0,0) and (5.08,0),
2.4×2.4-mm stems spanning z=h−76 to h, and nine through-x 1.5×1.5-mm holes centered
at local z=−30.25−5i. A stationary 1×1-mm pin at z=−30 bears on the selected hole's
upper face. Its actuator/retention housing is not generated.

First output: elbow z=h+[−72.5,−71.5], y=0 to −8. Eye spans x=±1.2, y=−8±1.5,
z=h−74±1.5, with a through-x square hole of half-side .75. Four actual walls are
generated. A 4×1×1-mm writer pin goes from x=[−6,−2] to [−2,2], then rises .25 mm
to ceiling contact. Connected root/arm reach a drive at (−10,−8). Mirroring x/y
about (2.54,0) puts the second drive at (15.08,8), spending internal area rather
than forcing a 12-mm screw under a 5.08-mm top.

Screw: 12-mm mean diameter, .5-mm lead, .25-mm square tooth width/depth,
5.875-mm solid core radius, 70-mm length (z=−82 to −12). Major-diameter routing
envelope is 12.25 mm; nut envelope 16×16×6 mm. Helix, running clearance, thrust
bearings and strength are analytical abstractions, not meshed threads. The .25-mm
printed features are unqualified on the specified X1C/nozzles.

Pad alternative: 4×4×90-mm rail, local z=[−89,1]; fixed 4×10-mm pads at
y=[−11,−10]/[−6,−5], z=[−47,−37]. The arm exits in x between them. Explicit
4-mm spring spaces and backing blocks react outward in y. Rail/pad overlap persists
through 40 mm plus .5-mm transfer allowance. Spaces do not establish spring force;
coil, guides and lateral carriage are not detailed.

Exact full-stroke swept boxes give **zero cross-site intersection** for the isolated
pair, including insertion and transfer allowance. Pin/eye insertion and loaded
take-up pass exact translational sweeps and 16/64/256-step holdouts. The separate
ground pin clears all nine seats and unloaded withdrawal. These are geometry
results, not force-qualified capture or a complete self-collision audit.

Two explicit witnesses stop extrapolation:

- Pin growth e, hole-face shrink e and vertical registration e leave centered-entry
  margin `.25−3e`: .175/.100/−.050 mm at e=.025/.05/.10. At e=.10 the pin intersects
  the upper wall by **.144 mm³**. Smaller bounds leave entry clearance only.
- An unchanged third output at (0,−5.08), h=0, intersects the first output's elbow
  at h=20 by **5.76 mm³** (largest single prism 3.60 mm³). This is actual solid
  overlap; stationary support does not remove it. Tiers or different routing are
  unconstructed alternatives. The pair is not a passed dense-board layout.

## Thread stationary hold versus rotor-energy loss

Let r=.006 m, lead l=.0005 m, k=l/(2π), s=k/r=.0132629; W is constant net downward
load, m physical translating mass, J rotor inertia, μ Coulomb friction. Positive
motor torque T drives the chosen direction. Force and rotor balance give:

```
c_up = r(μ+s)/(1−μs)             c_down = r(μ−s)/(1+μs)
steady raising torque = W*c_up   steady lowering torque = W*c_down
upward acceleration   = k(T−W*c_up)/(J+m*k*c_up)
downward acceleration = k(T−W*c_down)/(J−m*k*c_down)
```

Dynamic axial thread force is W+m*a_up or W−m*a_down, **not frozen at W**. The
source verifies positive reaction/denominator in every case and does not continue
lost-flank/singular solutions. At μ=0, gravity accelerates equivalent mass
`m+J/k²`. Independent friction-work/kinetic/potential-energy balance is checked.

At μs=.05, s<μs: stationary self-locking has margin. Kinetic μ=.02 still requires
positive lowering torque, but that does not ensure rapid arrest. At μ<s it
backdrives. High kinetic scenarios presume μs at least as high; no material pair
is qualified. Density **scenario** 1000 kg/m³ gives core-only
`J=ρπR⁴L/2=1.309934e−7 kg m²`, already **20.6856 kg** reflected to the output.
Density 1300 and added rotor inertia {0,1e−7,1e−6} increase it. These are bounded
structural/drive choices, not measured filament density or sourced motors. Hollow
screws/rotating nuts are different embodiments.

With W=1 N, m=.05 kg, μk=.02 and minimum core-only inertia, motor-off downward
acceleration is **−.0245800 m/s²**. From 100 mm/s, an infinite thread would coast
**203.417 mm**. At h=20, the finite nut loses full thread-length coverage after
25.25 mm and all axial overlap after 31.25 mm (including .25-mm pin take-up).
Thus 203 mm is a counterfactual stopping calculation, not a valid trajectory after disengagement. An unmodeled end impact
is not recovery. Raising from that speed coasts 41.479 mm and also needs endpoint
handling. No invented allowable-drop criterion rejects these finite-stroke failures.

| μk | Down coast at 1 N | Down coast at 10 N |
|---|---:|---:|
| .02 | 203.417 mm | 20.342 mm |
| .05 | 37.115 mm | 3.711 mm |
| .10 | 15.586 mm | 1.559 mm |
| .30 | 4.553 mm | .455 mm |

Rows use .05-kg translator, minimum inertia and 100 mm/s. Low load reduces holding
friction while rotor energy remains. **432 deterministic cases** cover W={1,10},
m={.05,.5} kg (discard m*g>W), ρ={1000,1300}, three added inertias,
μk={.02,.05,.1,.3}, v={.05,.1,.3} m/s, both directions. Unconstrained coast spans
.0576–16,373.8 mm: sensitivity, not predicted physical falls or a yield distribution.

100 mm/s needs **12,000 rpm**. At W=10 N, μ=.3, steady raising torque is
.018871 N m and thread heat **22.714 W/head** (3.63 kW at 160 simultaneous heads).
3 m/s² adds .004938 N m of core acceleration torque. Critical speed, temperature,
wear, contact stress, actual motors and nut lifetime remain unqualified.

For power-loss-safe lowering confined to [0,40] without endpoint impacts,
`v(h)≤sqrt(2*a_stop*h)`. Even granting instantaneous powered acceleration, no motor
inertia and zero reset travel, integrating dh/v(h) gives **≥1.80407 s/descent**
at the adverse light-load/minimum-inertia corner. A full-travel speed ceiling
44.344 mm/s alone is insufficient: speed must fall with remaining stroke. With
E-131's unvalidated .05-s/site and 6-s/map allowances, integer batches need
**≥534 channels** for strict <30 s. At $250 shared reserve, $400/$500 leave
**$.281/$.468 per head**, even with free cell hardware (160 heads: $.938/$1.563).
These are conditional bounds for this schedule, not achieved times, prices or a
cost-impossibility proof. Extra endpoint travel/different rotors change the bound.

## Counterbalanced pads: lower heat, no low-friction arrest

C=5.5 N ±20%, W∈[1,10] N, 100-N nominal preload per pad ±20%: residual can be
±5.6 N. At μs=.05, minimum preload gives 8 N static drag and 2.4 N margin.
Moving drag is `Dk=2*μk*N`; downward acceleration is `(W−C−Dk)/M_eff`. Reverse
residual sign for upward motion. M_eff includes reflected drive/coil inertia.

At μk=.02 and N=80 N, Dk=3.2 N. W=10/C=4.4 gives **2.4 N downward accelerating
force** during lowering; W=1/C=6.6 gives **2.4 N upward** during raising. At
M_eff=.5 kg each accelerates at 4.8 m/s² along travel and cannot arrest before
finite travel ends. If μs is also .02, stationary retention fails. Inertia changes
acceleration magnitude, not its sign.

At favorable μk=.05/minimum preload, adverse-residual stops from 100 mm/s are
.104/1.042/10.417 mm for M_eff=.05/.5/5 kg. The source covers **432** deterministic
load/spring/preload/friction/mass/direction cases. Friction and reflected inertia
change ranking; these are not device predictions. Zero kinetic margin at μ=.02
and −20% preload would need **175 N nominal per pad**, with no stopping reserve;
do not tune to that threshold. Existing high bound N=120, μ=.3 gives 72 N drag,
**7.2 W/head** at 100 mm/s (1.152 kW/160), up to **77.6 N** steady drive force,
and 2–3 MPa pad pressure across preload bounds. Coil hysteresis/fatigue, frame
compliance, pad wear/creep and heat rejection are unqualified.

## Limits, disposition and next action

All load/friction/density/inertia/preload values are engineering scenarios, not
product requirements or sourced process distributions. ±e is an adverse geometry
box. Common friction, spring force, preload loss and registration can affect a
bank; no independent-cell averaging or yield follows. Constant Coulomb friction
omits velocity dependence and stick-slip. Layer steps, hole bias, first layers,
warp, anisotropic stiffness, bearing drag, creep and fatigue remain unbounded.

Functional repetition remains 6,400 guided/slotted stems, eyes/elbows and ground
pins with actuation/retention, plus head drives, lateral carriages, readers and
frames. Reuse removes one inventory burden, not local stop/assembly/repair costs.
Neither input angle nor pin position proves supported height. False acceptance
can release multiple outputs; recovery and completion timing remain unimplemented.

**Stop both embodiments**, not their entire principles. Screw reopening requires
changed rotating inertia/kinematics, verified kinetic dissipation and dense routing;
static self-locking is insufficient. Pad reopening needs a supported load/energy
path beyond its adverse friction dependence, not exact balance or more nominal
preload. A-007 remains rejected. No brake/dog-fit sweep or full-machine optimization.

**Next: EXPLORE structural state retention**, storing height in stable load-bearing
geometry instead of arresting an unlocked output with a travelling friction head.
Search nonplanar multistable shells/distributed elastic structures against discrete
solid-stop control. A-021/E-063's planar scissors and singular reaction remain
negative controls; renaming a link stack is not novelty. First discriminate loaded
energy barriers, collapse paths, state reach, manufacturing bias and 40-mm dense
routing. Reject unspecified latches or unsupported snap transitions. CTO owns this
bounded exploration; no architecture is selected.

Primary source checks, 2026-10-10: [Roton backdriving](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/)
supports positive lowering torque for a self-locking screw, not instantaneous rotor
arrest; its bronze coefficient is not transferred. [Roton screw speed](https://www.roton.com/screw-university/types-of-screws/power-screws/speed-for-power-screws/)
identifies sliding loss as heat. Numerical results above are our calculations.

Self-review: force/rotor residuals, positive flank reaction, frictionless limit and
friction-work energy balance; exact coast versus 64/256/1024-step Euler position
integration (errors reduce 4×); continuous contact sweeps versus three refinements;
full-stroke pair separation, actual third-row intersection and integer scheduling.
No independent external validation or physical qualification.
