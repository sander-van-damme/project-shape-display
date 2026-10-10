---
status: complete
builds-on: [ADR-019, A-013, E-092, E-079]
---

# Dry support: finite swing survives, gravity completion remains unearned

**Retain a positively driven crossbolt as the primary support comparator and a
powered pivot pawl as a distinct conditional alternative. Do not credit passive
gravity completion or a compact over-centre linkage as a retained command.**
This changes the next question from another passive return sweep to a finite
shared set/return coupling that stays selected through support proof. No complete
architecture, affordable selector or hardware is established.

Input main `0f5cec0`. Reproduce:
`python3 tools/curated-experiment-checks/E-115/dry_support.py`.
Deterministic standard-library geometry, inverse force bounds and abstract support
logic; no random seed, measurements, contact solver, process prior or CAD release.
The three support topologies are a translating crossbolt, rotating rigid pawl,
and a crossbolt driven by a two-link toggle. Parameter variants are not additional
architectures. E-092 remains the supported-transfer comparator; A-013's guide
and actuator exclusions and ADR-014/015's selector failures remain in force.

## Generated section and manufacturing bounds

Coordinates are mm: rack lip x=0, pocket depth 1.2, overall rack depth 1.6.
The selected pocket initially has ceiling z=0 and floor z=−h; a carrier lifts
the rack by u before withdrawal. Other pockets repeat at provisional 5-mm
vertical spacing through 40 mm. These are test geometries, not a required height
resolution. Out-of-plane guides and connection to the column are unqualified.

A pawl initially occupies x=−a…o, z=−t…0, with pivot (−a,−t/2). Generate
a={1,1.5,2}, overlap o={.4,.6,.8}, thickness t={.6,.8,1},
h={2,3,4}, and opening angle {45,60,75,90} degrees: 324 sections per bound.
A grounded stop under the negative-x part of the bar limits downward rotation;
upward rotation clears that face. A downward nose load rotates toward the stop,
rather than relying on gravity to carry service force. Stop/pivot strength,
clearance, wear, backlash and finite mounting geometry remain unresolved.

Independent relative pivot, length and thickness errors are bounded by ±e,
e={.05,.10,.20}; pocket height/depth and common lift error also use ±e.
Opening-angle endpoint error is ±2 degrees; the closed hard-stop angle is
assumed zero. The angular error scales with opening fraction. Initial stop tilt
is **not covered** and is an explicit next-model discrepancy. These are epistemic
scenarios, not calibrated X1C capabilities or probabilities. Shared absolute
translation cancels; coherent adverse bank-relative errors are allowed.

For each nominal angle, rotate the actual rectangle and clip against the rack
half-plane. Enclose dimensional and angle deviations with a conservative radius
`eta=3e+hypot(a+o+e,(t+e)/2)*2*pi/180`. A 96-step angular sweep adds
`eps=hypot(a+o,t/2)*theta/(2*96)`, the maximum point motion to the nearest
sample. Clip at x≥−eta−eps before expanding z/x extrema. This covers intermediate
points, including vertices entering the rack between samples. Require 0.05-mm
clearance to pocket floor, ceiling, back and withdrawn lip. A finite pivot-side
reserve .6 and rack depth 1.6 enter the lateral section check; complete bearing
and guide thickness are not thereby certified.

If the clipped swept body's vertical extrema are lo,hi, admissible commanded
lift is `hi+.05+e <= u <= lo+h−2e−.05`. Opening and closing use the same path.
Withdrawal clears the entire rack half-plane, allowing every intervening tooth
to pass during 40-mm translation. Reseat only at a valid target pocket, close
the pawl under carrier support, lower to the hard stop, prove support, and then
release the carrier. Carrier acquisition/packaging is still E-092's unresolved
machine boundary; this calculation does not instantiate it.

| e mm | Certified section passes / 324 | Passes below 90 degrees |
|---|---:|---:|
| .05 | 81 | 41 |
| .10 | 31 | 12 |
| .20 | 0 | 0 |

Failure of this conservative sufficient enclosure is **not** a necessary
impossibility certificate. Counts are search outcomes, not manufacturing yield.
The .10-mm witness a=1.5,o=.4,t=.6,h=4,angle=75° has u=1.7994…2.7660 mm,
.2976-mm withdrawal reserve and .2425-mm back reserve. Compare the rectangular
crossbolt o=.4,t=.6,h=3,stroke=.9: u=.15…2.05 mm at e=.10; at e=.20 it still
retains .05-mm withdrawal reserve. The crossbolt needs a guide and positive
drive; its rectangular sweep repeats E-092's principle rather than reopening
A-013's excluded complete head.

## Gravity and toggle discrimination

For the pivot witness, assume a uniform 2-mm-wide bar, density .001… .0014 g/mm³,
bearing radius .4 mm, Coulomb coefficient .1… .5 and worst opening angle 77°.
These are deliberately labelled physical scenarios, not sourced PLA properties.
With no residual service load, maximum extra resisting pivot torque is
`mg[(L/2)cos(theta)−mu*r]`: **0.0000003065…0.000005439 N mm**,
equivalent to **0.161…2.863 microN** at its 1.9-mm tip. A finite burr/side-contact
drag above that bound prevents slow return; no inertial arrival credit is taken.
The geometric best-at-90° sections cannot guarantee gravitational closure under
±2° error. Larger counterweights, changed pivots or powered closing are changed
mechanisms to evaluate, not implicit fixes. Nothing here proves actual friction
exceeds the bound, but gravity alone earns no completion guarantee.

The toggle places its output joint .8 mm behind the crossbolt tip. Two links
have independently varying lengths L±e; knee moves from +b through zero to −K.
Generate L={1,1.2,1.4,1.6}, b={.2,.3,.4}, K={.7,.9,1.1,1.3},
o={.4,.6,.8}: 144 choices/bound. Invalid reach domains are rejected.
Output span is `sqrt(L1²−k²)+sqrt(L2²−k²)`. Crossing zero **extends** the
bolt before retracting it; the pocket must contain this overshoot. Monotonic
separable terms give extrema at both-short or both-long link corners, including
independent local deviations and correlated batch bias.

Include .3-mm joint radial envelopes and the rack in the lateral extent,
`1.6−(o−e)+.8+max(closed_span)+.3`. The full knee envelope includes +b and −K;
.4-mm link bodies must occupy separate lateral planes at their joints. Those
planes, pin shoulders, output guide and mounting are not a completed assembly.
Only **5/144, 0/144, 0/144** pass these necessary section gates at e=.05/.10/.20.
The tight witness L=1.2,b=.2,K=.9,o=.4 has .0550-mm forward overshoot,
≥.6165-mm retraction and 4.8319-mm lateral extent. Finite guided assembly can
only consume more space. Wider-error grid failures do not reject all linkages.

Over-centre geometry with an unloaded output has no restoring energy by itself.
A closed stop does not ensure the knee remains there against reverse disturbance.
Adding a spring/detent, captive cam or grounded keeper needs an actual reset and
energy path; E-079's passive-seating failure is not repaired by naming a toggle.
Stop nominal refinement of this compact toggle; a staggered/relocated linkage
could reopen with changed packaging and explicit retention.

## Retention, full-board consequence and next gate

Represent (retained command, ground support, carrier support). A supported
transaction needs:
`(1,1,0) -> (1,1,1) -> (1,0,1) -> (1,1,1) -> (1,1,0) -> (0,1,0)`.
Motion occurs while carrier support is present. A direct complement
`ground=not command` fails four states. Clearing selection on ground reseat
loses the command before selective carrier withdrawal. This is a concrete
logical exclusion of direct coupling, not an information-theoretic lower bound
or an implemented decoder. A common phase cam may supply the extra sequencing
state, but must permit outputs to remain supported after command reset.
An unselected cell must stay in ground-only support through every common phase.
A falsely accepted ground proof produces (1,0,0) regardless of a correct command
read. Mechanical interlocks and reader false acceptance remain open.

At 6,400 sites, one ground support plus one retained command already repeats
12,800 moving/retaining elements, before acquisition, followers, guides and
sensors. The toggle adds two links and three pivot interfaces per support
(12,800 links/19,200 interfaces if used everywhere). One bought item per cell
at a $250 shared reserve allows <$0.0391/item under the $500 cap. A hypothetical
80-row/80-data addressing scheme still has 160 logical lines plus shared drives;
no physical selector, purchased channel count or price follows from that count.
No time pass follows from small release stroke: the approximately 200-mm
shared-motion example in E-092 and ADR-017's grouping failures remain relevant.

**Next:** implement one finite positively captured set/return coupling, compare
crossbolt and powered-pawl outputs, and keep a command through reseat/proof/reset.
A row-local or transported route must avoid blocked rigid-ram conflict, positively
withdraw before address changes, and count real channels. Stop if it merely
recreates E-079's passive ramp or ADR-015's excluded writer. No print is proposed;
the unresolved discrimination is mechanism completeness, not a fitted tolerance.

Verification is self-review: angular enclosures versus 4,096-step holdouts and
32/64/128-step bounds, manufactured-vertex holdouts, independent unequal-link
closure/interior extrema, exact rectangle crossbolt limits and support-state
fault witnesses. No force dynamics, stiffness, proof sensor, process reliability,
durability, full 3D collision acceptance or physical qualification is claimed.
