---
status: complete
builds-on: [E-124, E-123, E-115]
---

# Closed jaw channels reject the compact layout before powered-transaction admission

**Reject the generated retained cup at the declared bounds;
no complete powered transaction is admitted.** Capped pins and closed return
channels replace E-124's floating upper contacts. The smallest generated housing
collides with its adjacent head by **0.009665 mm³** at e=.025/c=.005 mm, without
needing adverse face-size errors. This is new finite retention/drive-routing
geometry, not a repeat of the side-shoe acquisition failure.

The same geometry at **10.16-mm head spacing** clears the head-packing conflict,
but actual closing-wall contact exposes a second failure: channel play reduces
upper overlap to .023223 mm, and an allowed .025-mm inward foot-face error blocks
the rigid capture path at the foot side.
Thus the result does **not** exclude wider/staggered internal machinery or the
direct-head principle. That sparse layout is only a retained-joint component:
independent vertical power, positive drive arrest, powered ground-bolt set/reset,
retained selection and finite readback have not been implemented. Do not release
system timing/cost on this component. Close the bounded compact-head investigation
with a failed mechanical gate; retire its dependent complete-system evaluation.
Reopening requires changed channel/contact packaging or a sparse machine that
resolves loaded acquisition and supplies actual power/arrest/readback, not another
tolerance sweep of this section.

Input main `b0fe596`. Reproduce, using only Python's standard library:

```
python3 tools/curated-experiment-checks/E-125/retained.py
```

Evidence: generated finite polygon prisms, exact relative translational sweeps,
a pair-of-beams unilateral contact calculation, drive force-balance bounds and
support-state counterexamples. No sourced process distribution, material allowable,
physical measurement, qualified motor/sensor, manufacturing release or machine
performance claim. JSON is reproducible output and is not retained.

## Retained coupled stroke and routing

The original foot, stem and .4-mm horizontal/vertical motions remain. Each jaw
is now one rigid web/pad with two pins 2 mm apart. A stationary closed diagonal
slot constrains each pin; an outer translating plate has a closed horizontal
slot. After taking up channel play, lowering that common plate .4 mm produces .4 mm
inward/downward motion along the nominal guide direction. Reversing the plate
opens the jaws after traversing the opposite clearance faces. The two guide points constrain
in-plane rotation. Capped through-pins on **both** y faces resist axial escape;
there is no open-end return channel. This is a finite transmission from a shuttle
coordinate, **not an actuator or a power-loss latch**.

The generator includes four walls/end caps per slot, pin stems/caps, both jaw
webs, lower-pad pedestal, stationary plate bridges/tie and moving plate
bridges/tie. It replaces E-124's base rather than letting the descending rigid
webs cross it. Nominal self-collision is zero throughout acquisition and the
coupled stroke, including relative moving-body sweeps. Contacts with the foot
are intentional surface touches. A separate closure/take-up route is not ranked:
it would require its own complete routing and reset, beyond this one-topology
bound. No extra mechanism diversity is claimed for dimensional variants.

Generator: square-pin half-side {.1,.2,.3} mm × channel/plate wall {.2,.4,.6} mm;
cap lip .15 mm; fit gap `4e+.025`; e={.025,.05,.10}, c=.005. There are nine sections
per error bound. All fail the 5.08-mm adjacent-head enclosure. The lowest-error
smallest section has **.2-mm square pins and .2-mm walls**, a **5.002082×3.55-mm**
head envelope and only **.077918 mm** nominal x separation. These small features
are experimental even with the optional fine nozzle; no printable-strength credit
is used to accept them.

For an actual interference witness, put adjacent heads at h=40 with opposite
lower-guide endpoint errors ±.005 and opposing datum offsets ±.025 mm. Their
centre offsets are ±.046667 mm and rotations ±.000333333 rad. Intersect the
rotated generated bodies: the largest body-pair overlap is .009664997 mm³.
This is an attainable pose corner, not merely failure of a sufficient enclosure.
The witness uses no face growth. Larger generated housings cannot improve the
compact enclosure; this is not a continuous impossibility proof for all channel
shapes. Chamfered/curved channels and relocated joints were not generated.

Reusing the actual bodies at twice the head spacing removes this collision.
Nominal swept prisms over 40-mm travel also clear every adjacent column's
independently swept foot/stem. This sparse check does not include uncertain
loaded poses, a vertical drive, or transport/indexing between the two passes.
The smallest cap's projected vertical overhang over its shuttle opening is
.026777 mm after ±.025 face-size bounds alone: retention exists geometrically,
but cap bending, wear, misalignment and assembly remain unqualified.

The source also generates a **loaded closing-wall path** instead of pretending
that a pin in the middle of a clearance slot transfers force. At the lower
normal face of the diagonal guide, the jaw shifts outward/downward by
`gap/sqrt(2)=.088388 mm`. The horizontal shuttle's upper wall must take up
`gap+gap/sqrt(2)=.213388 mm` before bearing on the pin. Both actual wall-contact
coordinates are checked; the fixed-normal return deadband alone is .25 mm.
These allowances are distinct from the E-124 remote shaft guide half-play.

The nominal foot top is reached at q=.779029 of the original .4-mm stroke,
with only `.2-sqrt(2)*gap=.023223 mm` shoulder overlap. Exact sweeps to this
contact have zero internal/foot collision. Now shrink the foot's x faces by
.025 mm, with everything else unchanged. The jaw passes below the foot top
before reaching its side: the first side contact is at q=.783471. Advancing
another .01 in q produces **.000036971 mm³** prism intersection, rather than
upper seating. Thus wider head spacing alone does not rescue the generated
rigid transition under the declared error scenario. Elastic escape could change
this result, but is not established by the reduced contact model below; this is
not a universal physical-jam or material-strength claim.

## Coupled contact, rather than summed free deflection

The reduced solve uses relative lateral translation, rotation and axial position.
Column/head Euler–Bernoulli compliance is combined with their **opposite**
overhang orientations: upper-column and lower-head cross-compliances have
opposite signs. Column I=1.2⁴/12 and head I=2⁴/12 mm⁴; guide spacing 30 mm,
overhangs 45−h and h+10. These shafts are structural scenarios, not an assembled
powered carriage. The unlocked column has **no fictitious axial ground spring**.

This is an optimistic fully closed interface comparator; it does not repair the
failed loaded-wall acquisition path. Enumerate all active sets of five compliant
unilateral contacts: centred lower
pad, two upper shoulder nodes and two web-side nodes. Solve equilibrium with
nonnegative reactions and compatible active/inactive gaps. Individual guide
endpoint offsets, lateral warp, differential upper-face seating and closure
preload enter the same solve. Vertical reaction balance is independently checked;
symmetry is a zero-asymmetry limiting case, not a force-balance assumption.

Bounds (not priors): E={500,2000,100000} N/mm²; contact stiffness
k={10,100,1000} N/mm; h={0,20,40}; c={.005,.025}; all 16 correlated/adverse guide
corners; lateral warp ±.025; closure interference {−.025,.01,.05}; differential
upper seating {−.05,0,.05} mm. Signed travel loads are −.13405 N upward-driving
resistance and +.01095 N downward-driving resistance, from E-124's labelled
5-g/.060-N scenario. Each E/k combination evaluates 3,456 cases: **31,104
scenarios**, not samples from a population or estimates of yield.

At E=2000, k=100, h=20, zero guide/warp error and .01-mm interference, the
symmetric calculation gives .703017 N lower and .296983 N at each upper node.
With .05-mm differential seating, its mathematical continuation gives upper
forces .150218/.443749 N and relative pose x=−.215724 mm, angle=.026147 rad.
Transforming the **finite shoulder** leaves only .015307 mm projected overlap;
one assumed upper contact node has left the pad. **That continuation is invalid
as a real contact solution**; it is not an actual clamp displacement, load tail
or proof of jamming. The executable reports such invalid nodes separately.

Changing stiffness changes the active contacts and invalidity counts substantially.
Even within small-angle limits, fixed contact nodes can cease to represent the
finite foot. This rules out using symmetry or this reduced model alone to admit
loaded capture. Moving-edge/contact-surface refinement would be required for a
changed-layout admission, but cannot rescue the independently demonstrated compact
housing collision. Stop higher fidelity here. Friction, 3D torsion, guide edge
contact, pin/cap bending, strength, layer anisotropy, creep and lifetime remain
outside the solve; no reaction above is a rated load.

## Power, ground support and fault boundary

The square-thread analytical comparator exposes a separate support obligation:
for mean diameter d, lead l, slope s=l/(πd), the torque needed to oppose lowering
is `T=F d/2 (s−mu)/(1+mu s)`. Positive T means a brake is required. The source
checks d={1.2,2,3}, l={.25,.5,1} mm at explicit mu={0,.05,.1} scenarios. These
are **not generated screws or sourced friction values**. With a 5-g gravity load,
zero guide drag, d=1.2, l=.5 and mu=.1, T=.000947706 N mm: an unbraked axis can
back-drive despite positive jaw attachment. Some larger/finer threads self-lock
at mu=.05; the result does not reject all screws. All positive-lead threads
back-drive in the frictionless limit. A retained command or motor de-energisation
is not a positive stop.

A finite comparator adds a .6-mm-thick ground bolt, .4-mm engagement, .9-mm
withdrawal, four guide walls and a connected rack with nine 3-mm-high pockets at
5-mm pitch. Seated contact and insertion after .8-mm unload are collision-free.
At h=2.5 between indexed seats, reinsertion intersects rack material by **.032 mm³**.
A discrete ground bolt therefore cannot be silently credited as an immediate
power-loss arrest at every travel height. Its set/reset actuator and integration
with the head are absent and receive no grant.

The executable enumerates idle → acquisition → clamp → unload → unlock → upward
or downward travel → reseat → proof → withdrawal → command reset. Fault witnesses
separate actual support from reported support: missed capture with false readback,
common false ground/height acceptance, command cleared on reseat, mixed reset,
jam and power loss while unlocked. Even ideal retained command memory cannot
repair loss of the carrier support path. A powered jam stop must retain support
and selection; no recovery is qualified. **These are transaction requirements and
counterexamples, not implemented controllers, output readers or safe-stop hardware.**
No actuator/sensor budget, reliability probability, reset success or timing is
inferred from them.

Self-review: finite interior collision witness, exact relative sweep versus
8/32/128-step holdouts, finite arbitrary-neighbour-height sweep, independent
assembled beam-element stiffness versus analytical compliance, reciprocity,
zero-load/symmetric limits, active-set residuals, vertical force balance and
frictionless screw work conservation. E-123's pad drag, e=.10 compact packing,
closed-guide rack collision and E-124's tilted side-shoe failure remain executable.
There is no independent external validation. No print or purchase is justified
by this rejected compact mechanism; no missing physical qualification is being
turned into a new blocking task.
