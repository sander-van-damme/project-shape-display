---
status: complete
builds-on: [E-129, E-130, E-134, E-138, D-002, M-004]
---

# Captive cam support leaves a backdrivable input; a dwell does not dissipate its energy

**Stop the tested travelling rocker and captive sliding cam as answers to passive
transfer arrest.** A finite groove can preserve loaded contact in both directions
and retain two heights at rest, but its moving input remains free. Even a flat
endpoint dwell does not stop input inertia. No mechanism here escapes the open
transfer coordinate, and no complete display is admitted. This rejects these
constructions under explicit bounds, not escapements generally or every bounded
outage motion. Stage 02 specifies no acceptable outage drop; none is invented.

Input main `7baed94`. Reproduce with Python 3 and NumPy:

```
python3 tools/curated-experiment-checks/E-139/support.py
```

Evidence: **finite offset-wall/roller geometry, contact-force calculations,
conservative constrained motion and deterministic dimensional scenarios**. No
qualified assembly CAD, impact simulation, process prior or physical measurement.
Self-review only. JSON is reproducible and is not retained.

## Search and causal comparison

Three independent strategies informed this bounded investigation: horological
rest/impulse faces; industrial walking-beam continuous load transfer; constraint
inversion from an open support to a two-sided groove. The first two are source-domain
searches; the third is geometric synthesis. These yield different contact arrangements,
not new physical principles. D-002/M-004 already identify escapement memory.

- [WO2017013611A1](https://patents.google.com/patent/WO2017013611A1/en)
  describes additional pallet rest formations and equilibrium positions. It does
  not establish an arbitrary interrupted loaded transfer for our display.
- [US4151907A](https://patents.google.com/patent/US4151907A)
  describes a grooved positive-motion cam and separate followers/linkages giving
  walking beams their transverse and longitudinal motions. It motivates captive
  construction, not an unpowered brake claim. Sources accessed 2026-10-10.

| Topology | Selection, motion, retention and grounded load | Verification/recovery and disposition |
|---|---|---|
| Travelling pivoted pallet | Select a column with a local rocker/head; its nose lifts a guided platform. The ground pivot takes force; a drive must take moment. Angular seats limit travel. | Top/seat proof required; the upper stop cannot resist gravity's moment. Fails even high-state retention without another support. |
| Captive/conjugate cam | A selected guided plate moves horizontally beneath a column's roller; lower wall supports downward load, upper wall contains opposite travel after clearance. Flat dwells store two levels at rest; grounded slide bearings take vertical force. | Read roller height and plate position; free input backdrives on the rise. Finite end stops bound geometric travel but do not qualify impact or recovery. |
| Fixed-slot control E-129 | Select and drive indexed shaft; ground bolts hold slot flanks at rest. | Two staggered full-insertion windows do not overlap; .516622-mm rack-equivalent gap. Identical-phase slots both release for motion. No new control result claimed. |

The rocker changes E-129's fixed bolt into a moving support but repeats E-130's
missing carrier restraint. The groove removes open follower separation; it does
not remove E-134's free phase. Stop before detailing a latch/reset that would
silently supply a free brake. No saturation claim for the whole design landscape.

## Actual sections and signed contact path

Rocker: grounded axis at (x,z)=(0,0), 4-mm arm, .2-mm arm capsule radius and
.4-mm circular nose centered at `(4 cos(theta),4 sin(theta))`. A horizontal
platform spans x=[3,4.5] mm, thickness .6 mm; its bottom stays tangent to the nose
for theta=0…pi/6, lifting **2 mm**. Grounded platform guides constrain lateral
motion. A radius-.15 lug at radius 1 contacts equal ground tips at angles
`−delta` and `pi/6+delta`, `delta=2 asin(.15)`, in a separate axial layer.
Exact circle gaps are nonnegative throughout. The upper tip pushes toward
**decreasing** theta, as gravity does; it cannot retain the high state.
Gravity torque is **3.464–4 N mm per N of load**. Stop this construction here.
The arm/seat attachment strength and axial webs are not qualified.

Cam coordinates: u increases as the plate translates globally by x=−u; the roller
axis remains at global x=0. Pitch curve `(u,h(u))`, in mm:

```
h=0                    for u<=2
h=1-cos(pi*(u-2)/4)     for 2<u<6
h=2                    for u>=6
n=(-h',1)/sqrt(1+h'^2)
lower=(u,h)-(.4+c)n; upper=(u,h)+(.4+c)n
```

Use roller radius .4 mm, nominal radial clearance c=.1 mm. Generate both finite
walls for u=−1…9, then join their vertices with straight edges. Lower material
extends to z=−1.5; upper material to z=3.5; both occupy axial y=[−.6,.6] mm and
join via a rear plate y=[.6,1.2]. Thus the two walls are one translating assembly,
not independently frozen rails. A tab at local x=[10,11], y=[1.4,2.4], z=[−1,0]
connects through a neck x=[10,11], y=[1.2,1.4] and bridge x=[8.5,11],
y=[.6,1.2], both at z=[−1,0]. Ground stop blocks have
x=[1,2] and [11,12], with the tab's y/z interval: their gaps are **8−u and u**.
Prism intersections check stop clearance against the tab, neck, bridge, rear plate
and conservative main-body box throughout the stroke. These stops bound u=0…8;
capacity, rebound and bridge strength remain unqualified.

For each phase, find the minimum roller-center height clearing **all lower-wall
segments and vertices**, and the maximum height clearing the upper wall by
reflection. Segment tangencies are evaluated only if the contact lies on the
segment. Vertex tangencies are also included; bounding-box clearance is not
substituted for roller/wall contact. The active lower contact defines the loaded
path; the upper-minus-lower center interval tests actual fit.

The two flat retained levels are −.1 and 1.9 mm relative to the cam datum. Translate
two independent copies to obtain **12→14→12 and 32→34→32 mm**. Raising and lowering
traverse the same loaded lower wall; no follower spring or reversal to an unloaded
path is granted. At u=4, loaded height is **.872864 mm**, remaining vertical fit
**.254273 mm**, and positive contact normal **1.271006 F**. From zero speed within
either dwell the load has a vertical ground reaction through the slide bearings;
the horizontal input is neutral, not position-restored. Holding the motor angle
is never assumed.

For 32/128/512 subdivisions (161/641/2561 vertices per wall), 257/1025/4097 unique
phases are checked; rigid translation gives the two height cycles and reversing
sample order gives signed paths. Independent zero-clearance
height error against the analytic pitch law falls **3.75286e−4 → 2.34687e−5 →
1.46685e−6 mm**. Signed force-work error at 1 N falls **5.507e−4 → 6.047e−5 →
3.073e−6 N mm**; reverse work has the opposite sign. These checks establish a
convergent section model, not a continuous-phase proof or a manufactured fit.

## Ground reactions, free input and dwell crossing

Let g(u) be the actual loaded roller-center path. Virtual work gives the input
load `Q_u=−F g'(u)`. At the finite-wall midpoint it is **−.784510 F N**. Column
and slide guides react transverse forces but do no work along the allowed motion.
Adding an ideal conjugate contact does not fix this: the two zero-clearance
constraint rows are `[-h',1]` and `[h',−1]`, rank **one**, with allowed tangent
`[1,h']`. Opposing normals cannot supply the missing generalized reaction.
This argument applies to these rigid lossless smooth branches; friction, a grounded
spring or a switching latch changes the force/topology model and must be explicit.

To test whether an endpoint dwell itself arrests motion, use an independent,
smooth zero-clearance limit with input free. Release at u=4 from rest. Set input
reflected mass m_c={.005,.02,.1} kg, output mass m_o=.01 kg and total downward
force F={.2,1,10} N. These are sensitivity scenarios, not service requirements.
With h and u in metres, conservation and the constrained equation give:

```
K=.5*(m_c+m_o*h'^2)*u_dot^2 = F*(h(4)-h(u))
(m_c+m_o*h'^2)*u_ddot = -F*h' - m_o*h'*h''*u_dot^2
N=(F+m_o*(h''*u_dot^2+h'*u_ddot))*sqrt(1+h'^2)
```

Check 2,001 phases of the descending half-rise for each scenario. **N stays
positive**, so this witness does not require contact separation or an upper-wall
impact. Energy residual is <2e−18 J. At the low dwell, output velocity vanishes
but input velocity does not. For F=1 N, m_c=.02 kg, the input reaches **.316228 m/s**,
crosses the 2-mm dwell in **6.3246 ms**, and arrives at the positive input stop
with **1 mJ**. Across the scenarios stop energy is .2–10 mJ. This is a conservative
witness, not a prediction of real stop impact, dissipation or settling.

The finite c=.1 geometry has .972864-mm descent from the midpoint to its low dwell;
the independent zero-clearance witness has 1 mm. Do not mix their numerical paths.
The finite cam's rigid end stops bound a full stroke to 2 mm of height change
while intact; they do not establish acceptable outage behavior. Removing those
stops for a repeating staircase removes that bound. Extending the dwell delays
impact but supplies no energy sink. A 1-N counterbalance only replaces F by F−1:
at F=.2/1/10 the midpoint generalized forces become +.6283/0/−7.0686 N. Exact
balance is neutral and repeats E-131, not retention under uncertain load.

## Coherent manufacturing bounds and neighbor obstruction

No calibrated X1C distribution is available. Cross the signs of roller-radius
bias, lower and upper inward wall offsets, and relative vertical wall misalignment,
each ±e and coherent across a head/bank. Recompute contacts at 97 phases for all
16 corners at each nonzero e:

| e, mm | Worst vertical fit, mm | Corners with interference |
|---:|---:|---:|
| 0 | .199981 | 0/1 |
| .025 | .074980 | 0/16 |
| .050 | −.050041 | 1/16 |
| .100 | −.354272 | 4/16 |

These are bounded scenarios, **not probabilities, yields or process acceptance**.
At flat dwell the adverse interval is exactly `.2−5e`; the .05-mm interference
therefore has an independent geometric check. A shared error does not average
away over cells. Hole/roller bias, wall thickness, differential warp, assembly
alignment and layer effects motivate these bounds but do not calibrate them.
Friction, roughness, contact compliance, orientation strength, creep, wear and
fatigue remain unresolved. Adding friction to cure backdrive needs the static,
kinetic and moving-inertia evidence missing in E-131/E-132.

Test a second roller at x=5.08 in the same engagement plane. With the selected
cam at u=0, a neighbor 20 mm above or below clears this local plate. An unchanged
neighbor at the **same retained height** has center z=−.1 while the actual lower
wall requires center z>=**1.636924 mm**: the disk intersects solid material.
Thus two unequal retained heights alone give a misleading isolation pass.
This rejects same-tier arbitrary-map replication of the generated plate. Staggered
planes, routing or a new pickup joint are unbuilt alternatives, not prohibited by
the 5.08-mm top pitch. Assume 4.8-mm tops; their .28-mm gaps are not a surface test.

## Full-display screen and decision

A direct 40-mm cam with the same peak slope stretches the rise to 80 mm: **84-mm
input stroke, 86-mm main plate width** before tab/drive hardware. It stores continuous
positions only with another restraint; two endpoint dwells alone provide two
levels. Twenty reindexed 2-mm cycles would instead need real support handback,
reset, indexing and retention after every step; that mechanism is absent.
Neither extrapolation is admitted merely because the section passes contact.

A resident version repeats 6,400 roller axes, 12,800 cam wall surfaces, 6,400 input
slides and column guides, plus selection/drive, end stops and height/seat readback.
Shared heads reduce cam inventory but reintroduce capture, service retention and
routing. Printed integration does not remove wear fits, assembly or repair access.
With a **hypothetical** $250 shared allowance, the $500 ceiling leaves <$.039063/site
before allocating any further heads; this is a budget inequality, not a sourced BOM.

For comparison only, grant a complete 2-mm cycle t including lift, handback, reset
and local settling; .05 s/site capture/proof; and 6 s/map preparation, registration,
transport overhead, final proof, bounded retry and settling. All 6,400 sites change
40 mm. `T=6+ceil(6400/H)*(.05+20t)` gives:

| Assumed complete cycle | T at 80 heads | Minimum H for <30 s | Per-head allowance with free cells/$250 elsewhere |
|---:|---:|---:|---:|
| 10 ms | 26 s | 68 | $3.676 |
| 50 ms | 90 s | 291 | $.859 |
| 100 ms | 170 s | 582 | $.430 |

These deliberately optimistic schedules do not invent the missing reset or prove
that sensing/retry fits the allocations. All-raising 1-N field work is at least
256 J. Unchanged columns need independent service supports and collision-free
access. Commanded plate position is not proof of actual top height, loaded seating or
intact groove. False acceptance/common registration faults are unquantified;
failed handback must retain capture, and recovery after interruption needs a real
arrest and proof. No bought-cost, throughput, durability or hardware pass follows.

**Close this finite branch; do not optimize its clearances or print it.** Reopen
only with an explicit grounded reaction or energy sink that changes input-loss
behavior and a route clearing arbitrary unchanged heights. The new evidence is
the generated captive path, rank/force witness, dwell coast-through and coherent
fit/neighbor counterexamples; the missing-carrier-restraint conclusion is consistent
with earlier controls, not claimed as a novel discovery.

**Switch the next search axis to load-responsive dissipation.** A targeted hoist
search found a screw-actuated friction stack with a grounded ratchet reaction:
[US3399867A](https://patents.google.com/patent/US3399867A/en) describes a Weston
brake with screw-related discs controlling lifting/lowering. [Harrington's product
description](https://harringtonhoists.com/accolift-electric-chain-hoists/accolift-low-headroom-hoists)
explicitly pairs its Weston brake with a motor disc brake. This supplies a new
recombination lead, **not proof that a scaled standalone brake arrests our free
input**. Compare its load-responsive clamping and overhauling-lowering branch
against E-129's released roller and E-132's permanent pads. First construct the
thread/axial/friction/ratchet reactions, including free input, low load and preload;
stop if it needs a hidden motor brake, absent return or uncontrolled release gap.
No fresh broad search, detailed machine, purchase or staffing is justified yet.
