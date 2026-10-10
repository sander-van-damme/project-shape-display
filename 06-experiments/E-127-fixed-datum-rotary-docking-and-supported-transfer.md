---
status: complete
builds-on: [E-126, A-025]
---

# Fixed-datum rotary access needs phase registration, routed shafts and real arrest

**Reject the tested six-dog rigid shared drive and same-tier two-lane straight
shaft layout. Retain matched lock/dock indexing as a conditional recombination,
not an admitted machine.** The generated single-head mesh/transfer has a nominal
powered support path; it has no continuous passive arrest while moving. Stop
timing/BOM refinement and fabrication for this embodiment. A smaller or rerouted
pinion, an independently phased head, or an actually arrested indexed bus changes
the case; neither these failures nor an 8-mm gear diameter rejects A-025 generally.

Input main `7f969cc`. Reproduce using Python 3 and NumPy:

```
python3 tools/curated-experiment-checks/E-127/rotary_transfer.py
```

Optional `--svg PATH` renders the same generated profiles. JSON/SVG are
reproducible output and are not retained. Evidence is **finite rigid cross-sections,
prismatic axial intervals, kinematic contact replay and calculations**; not full
assembly CAD, contact dynamics, manufacturing yield or physical measurements.

## Constructed mechanism and gear control

Coordinates: rack motion z, pinion axis y, radial mesh direction x. Generate an
18-tooth, module .4-mm, 20° involute pinion: pitch radius 3.6, tip radius 4.0,
root radius 3.1 mm. Flanks join radially below the base circle; there is no root
fillet or strength credit. Rack tooth flanks are straight, addendum .4, dedendum
.5 mm, with .10-mm total tangential thinning. Its backing is .8 mm thick;
56-mm finite rack extends from z=−48+h to 8+h, retaining engagement throughout
h=0…40 mm. Top pitch stays 5.08 mm. Larger internals are expressly allowed.

The standard no-undercut inequality `z ≥ 2/sin²(20°)=17.0973` motivates 18 teeth;
E-126's 3-mm pitch diameter is not inherited as a printable standard gear.
KG Stock Gears' *Technical Data*, §1.8 p.28 and §1.9 Table 15 p.36, supplies
the standard undercut and rack-contact formulas:
[manufacturer technical reference](https://www.kggear.co.jp/en/wp-content/themes/bizvektor-global-edition/pdf/TechnicalData_KGSTOCKGEARS.pdf),
downloaded and text-extracted 2026-10-10. The independent ideal contact-path
calculation gives ratio **1.75529**. Neither
formula establishes tooth strength, wear or actual printed involute accuracy.

At each of 321 phases over a tooth period, check generated gear vertices **and
edge crossings of rack-face corners**. These cover the minima of the
piecewise-linear gap along each polygon edge. Taking up .05-mm rack backlash
gives maximum residual x-gap **.0001410 / .00000884 / .000000539 mm** at
32/128/512 flank segments, with no detected penetration. This converges toward
the ideal tangency; it is not a continuous-phase interval proof. Repetition and
the finite rack ends cover 40-mm reach without inventing a new tooth phase.

Error cases are explicitly labelled bounds, **not X1C priors**. At 161 phases,
common rack-center error {−.10,0,+.10} mm crosses tooth halfwidth growth
{0,.025,.05} mm. Center −.10 plus growth .025 produces **.03140-mm maximum
penetration**; −.10 plus .05 produces .1000 mm. A common rail/print bias can
therefore jam an entire lane; no independent-cell averaging or board-yield claim.

## Arbitrary-angle docking versus matched indexing

Generate axial rectangular dogs centered at radius 2.6 mm: .6 radial × .5
tangential × .8 axial mm. Socket cavities are .8 × .8 × 1.0 mm in a radius-3.4-mm
disk. Convex corner containment checks every dog against its rotated socket.
Straight axial insertion/withdrawal preserves that section; no chamfer or
elastic alignment is assumed. Socket floors leave .2-mm axial clearance.

Six equally spaced dogs give an insertion half-window **2.97155°**, modulo 60°.
Two ground-locked shafts separated by 30° have disjoint engagement intervals:
`2 × 2.97155° < 30°`. A 721-angle scan independently finds no common fit.
This rejects **simultaneous fixed-phase engagement through this rigid six-dog
bank**, even with perfect manufacture. A single independently rotating head can
phase itself while the ground bolt holds. Sequential acquisition with disengaged
free sleeves, friction clutches or independent motors adds physical channels;
it is not represented by the ideal common coupling in E-126.

Recombination: use **twelve dogs and twelve ground-lock slots**, registered to
one angular datum. All nominal parked states then have the same dock pattern.
Their loaded-seat offset is common and must also be included in head phase.
The resulting height step is **1.88496 mm**, and 22 steps span **41.4690 mm**.
This is a possible discrete terrain alphabet, not a new product resolution
requirement, arbitrary continuous height, or an approved performance tradeoff.

For that twelve-dog joint, enumerate 16 corners at each error e: common head
x/z offsets ±e, dog edge growth ±e, socket edge shrink ±e. All twelve dog
orientations are checked. Worst margins:

| e, mm | 0 | .025 | .050 | .100 |
|---|---:|---:|---:|---:|
| Insertion margin, mm | .1000 | .01585 | −.06830 | −.23660 |

The .025-mm case has little reserve and omits angular registration error,
warp, axial tilt and burrs; it is not manufacturing acceptance. Common translation
acts coherently across a dock bank. Larger cavities trade interference against
backlash and thinner material; this run does not optimize a failed fit.

## Supported handover and the power-loss hole

Generate a radius-3.4-mm ground collar with twelve radial open slots, root x=2.4
and tangential width .9 mm. A .5-mm-wide bolt inserts its nose to x=2.6 and
extends to 4.4 mm; retraction to nose x=3.5 clears the collar. Intersect the bolt
with the **actual polygonal circular collar**, then test containment in a slot.
This avoids assigning load support at a corner outside the disk. Full-seat
half-window is **3.38885°**; 256/1024/4096 disk segments change it by less than
.0000014°. The grounded bolt guide must resist torque into the frame; guide
stiffness, return spring and actuation hardware are not constructed or qualified.

Replay ten local states: ground seated → dock inserted unloaded → drive flank
contact → lift inside ground-slot clearance → retract ground bolt → rotate →
insert target bolt → lower onto ground flank → unload dock → undock. Actual
fit/contact conditions distinguish **inserted** from **load-bearing**. Powered
support exists in every nominal state if the head is a torque-holding drive;
the constant relative dock angle preserves contact during motion. Ground seating
requires **.21293-mm rack motion** from slot center before ground contact carries
load. Thus a bolt-position indication alone does not prove that load transferred.
The trace is a single-head kinematic construction, not a synchronized bank controller.

At 15° mid-step the full bolt cannot enter. A spring-return bolt pressed against
the unbroken circular rim has a radial normal and supplies **no positive resisting
torque** in the frictionless model. Power loss there therefore has no demonstrated
passive load path. The full-insertion-blocked arc corresponds to **1.45910 mm**
of rack travel per index. Partial edge capture can begin earlier than full seating;
that number is not a predicted free-fall distance or a proof that every point in
the arc lacks all partial contact.

Even granting instantaneous return and successful arrest at the next slot, the
supremum distance to its loaded flank approaches one **1.88496-mm** step.
For downward force scenarios 1/3.27/10 N this releases up to **1.885/6.164/18.850 mJ**
before arrest, excluding drive inertia and initial kinetic energy. These are
conditional work calculations, not measured impacts, safe drops, or guaranteed
upper bounds with a real delayed spring. A missed/bounced slot can travel farther.
Required drive torque is 3.6/11.772/36 N·mm before friction/inertia. No material
allowable, fatigue, creep or contact-stress acceptance is assigned.

The e=.025/.05/.10 edge-growth, slot-shrink and tangential-offset corners leave
centered bolt margins .125/.050/−.100 mm. Housing runout, shrinkage, first-layer
effects, layer quantization and wear can enter those aggregate bounds; no claim
is made that the bounds cover the actual process. Spring dynamics and friction
need independent evidence if a revised mechanism survives kinematics. A real
shared fail-safe brake could preserve the docked load path; it must hold every
selected channel through disengagement/recovery and does not appear for free.

## Staggering does not automatically clear the shafts

The 8-mm gear envelope exceeds 5.08-mm pitch; that alone is **not a rejection**.
Test alternating axial gear/rack lanes. Gear disks in each lane are then spaced
10.16 mm. However, a straight radius-.8-mm shaft crossing the other lane
intersects the adjacent full-travel rack backing at x=[−.98,−.18] mm:
**.62-mm radial penetration** at shaft height. The backing spans that height at
every h=0…40 in this same-tier construction. This is an exact circle/rectangle
intersection, not an envelope-only alleged collision. Vertical tiers, opposite
access directions, smaller gears or offset transmissions change the layout and
are unbuilt; the finding rejects this two-lane straight-through routing only.

The local axial stack reserves rear bearing y=[−1.2,−.2], gear [0,1.2], collar
[1.4,2.6], front bearing [2.8,3.8], socket disk [4,5.2], docked head [5.2,7.2] mm.
It is not a tileable 5.08-mm-depth assembly. Bearings are nominal radius-.95 bores
around the .8 shaft: adverse bore/shaft radial errors and eccentricity each e
leave `.15−3e` gap, zero at e=.05 mm. Guides, bearing housing load paths, bolt
retractors and travelling-head access still need finite construction.

## Decision, full-board implications and next discriminator

Repeated inventory remains 6,400 racks, pinion/shaft assemblies, ground bolts,
ground return elements and dock patterns, plus 12,800 bearing surfaces. These
are functional counts; integral printing may combine parts but not remove their
fits, wear, inspection or repairs. An open ground bolt plus falsely reported
dock/lock seating can release a cell; common head-registration or reader bias can
affect a bank. Commanded actuator position and motor angle cannot independently
verify load support or rack height. Retain the head and stop locally on failed
proof; actual sensing, false acceptance and bounded recovery remain unimplemented.

No completed-cell rate, <$500 machine cost, local-disturbance acceptance or
reliability follows. In particular **do not reuse E-126's six-second reserve**.
Continuous pocketed feed was not promoted as a control: no simpler supported
exchange is supplied here, and E-126 preserves its distinct inventory/feed issues.

Reopen only with a changed **complete joint topology**: routed stationary access
and a load path arrested throughout handover, plus either independent phase
acquisition or a matched indexed bank. The useful next comparison is continuous
independent phase capture versus matched stop-at-index coupling with shared
arrest; the latter eliminates a phase search but changes motion scheduling.
First demonstrate two different retained heights, selective release and power
loss with finite contacts; stop if it simply relocates an ideal clutch/brake.
Do not expand gear-width/tolerance sweeps or print the present embodiment.

Self-review only: involute contact-path cross-check; profile and circular-rim
convergence; analytic disjoint phase intervals; zero-error symmetry; explicit
common-error counterexamples; ten-state contact replay; independent exact
circle/backing intersection. No independent external validation or hardware claim.
