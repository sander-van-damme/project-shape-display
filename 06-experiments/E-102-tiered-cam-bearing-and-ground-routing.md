---
status: complete
builds-on: [E-101, E-100, E-062]
---

# Tiered cam routing escapes shaft collisions but fails follower stiffness

**Retain four-phase axial routing as a partial geometric result; reject its
slender follower fork under the inherited 500…3000-MPa uncertainty range.**
Two shaft tiers alone are insufficient: the two-phase layout has an
actual cam-web collision. Four axial phases remove that witness and clear the
checked support envelopes. This is new routing evidence, not a complete
selector, bidirectional valve or hardware pass. Stop free-post refinement and
shaft-phase simulation of that embodiment. Stiffer followers and a grounded
frame/return design are required before contact/dynamic analysis.

Input main `c64de1f`. Replay:
`python3 tools/curated-experiment-checks/E-102/tiered_support.py`.
Evidence: finite swept envelopes, exact solid collision intervals and linear
elastic calculations; self-review only. No physical measurements, sourced
manufacturing prior, CAD export, contact solver or print request. All dimensions
and E values are explicit design/scenario bounds inherited or changed from
E-100/E-101; none is qualified X1C capability. No probabilistic yield follows.

## Generated routing and changed search rule

At 5.08-mm pitch, alternate parallel 3-mm shafts between z=10 and 18 mm.
The E-101 captured cam package has outer radius 6.6 mm, 1.2-mm axial thickness,
1.2-mm pin, .2-mm groove clearance, .6-mm webs and 2.5-mm lift. Neighboring
shaft-to-cam radial clearance becomes **1.376624 mm**; same-tier shafts, two
pitches apart, clear cams by **2.060 mm**. This escapes E-101's continuous
coplanar-shaft collision, rather than just renaming that geometry.

Generate two routing rules, not a diameter sweep. Support repeat is eight
cells (40.64 mm); axial cam stations are `(0.5+8*(lane mod n)/n)*pitch` modulo
that repeat, for n=2 and 4. The two-phase rule leaves same-tier disks in the
same axial plane. At a common intermediate −90° rotation their high and low
outer dwell webs overlap by **.540 mm** along the line of centers. The source
intersects actual annular-material intervals, not only bounding disks. Concurrent
column transitions can encounter this state. Alternating heights by themselves
therefore do not establish a usable array.

The four-phase rule separates these disks axially. A nine-lane, three-station
patch generates cam envelopes, two finite bearing housings per cam, bearing
ground necks, two follower fork cheeks and a bridge per cam. Bearings sit
5.08 mm either side of the cam; housing outer size is 1.2×5.2×5.2 mm
(3-mm shaft, .2-mm diametral clearance, 1-mm walls). Fork cheeks are .6×1.2 mm
in section, straddle the disk with .2-mm axial side gaps, and reach a rail
attachment at z=30…32.5 mm. Upper crossed-family bearing necks, 1.6×1.2 mm,
are placed halfway between lower shafts; their maximum envelope reaches
55.4 mm above ground. Narrow necks deliberately replace E-101's broad posts.

**13,392** shaft/foreign-ground-neck checks, **324** disk-pair checks and
**20,736** foreign-component box checks pass for the four-phase rule. Minimum
reported sufficient separating gap is **1.140 mm**, exceeding two opposing
.1-mm envelope expansions. Solid swept cylinders enclose cams; boxes enclose
fork motion over a prescribed −.2…2.7-mm stroke envelope. These selected
checks cover continuous motion inside that envelope; groove-rise contact has
not established that the actual mechanism stays inside it. Intentional own-shaft/bearing, pin/groove and
fork/rail contacts are excluded and are **not** validated by the clearance run.
No claim of complete all-part collision clearance is made: upper cam/rail
assemblies, edge drives, frame ties, actual groove-rise contact, pin bending,
beam retention/anti-yaw, valve/manifold and assembly access remain ungenerated.
The periodic patch does not qualify finite bank boundaries.

## Crossed riser cannot inherit its original position

E-101's 1.6-mm-square straight row riser at the diagonal beam endpoint is only
`5.08−2 sqrt(2)=2.251573 mm` from the nearest continuous upper shaft axis.
A 3-mm shaft intersects it by **.048427 mm**, independently of axial disk
staggering or shaft tier height. The riser must cross that shaft elevation.
Moving its center **.288427 mm** into the exact inter-shaft corridor leaves
.240 mm nominal side clearance and only **.040 mm** after opposing .1-mm
expansions. This is an inverse placement bound, not a generated bent riser or
returned beam. The offset pad, compression/buckling and return linkage still
need geometry. It is not valid to transfer E-101's beam-contact pass unchanged.

## Schedule-conditioned load path rejects the slender fork

Keep the E-061 schedule: only one row is selected at a time. A row support
serving eight selected cells carries **9.512389 N**. An upper column support
carries eight .1-N preloads plus at most one selected endpoint, hence only
**1.889049 N**. Applying the dense row load to every upper column support
would overstate the failure. Loss of preload contact or support-load
redistribution invalidates these assumed equal-span reactions.

The lower row fork at shaft z=10 has two .6×1.2-mm cheeks between pin center
z=12.8 and rail attachment z=30: **17.2-mm constant loaded length** while both
ends rise together. Give them equal sharing and ideally fixed ends as an
optimistic case. Weak I=.0216 mm⁴ per cheek. Pair Euler capacity is
`8*pi²*E*I/L²` for fixed-fixed ends, one quarter for pinned ends; axial loss
is `F*L/(2*E*A)`. At full selected row load:

| E, MPa | Fork pair fixed capacity, N | Fork axial loss, mm | Local shaft sag, mm |
|---:|---:|---:|---:|
| 500 | 2.882416 | .227240 | .104545 |
| 1500 | 8.647247 | .075747 | .034848 |
| 3000 | 17.294493 | .037873 | .017424 |

At 500 and 1500 MPa even optimistic fixed-end capacity is below 9.512389 N.
At 500 MPa the formal axial loss alone exceeds E-061's entire .2-mm allowance;
post-buckling behavior is not predicted by that linear calculation. Contact
against the cam could restrain a buckled cheek but introduces rubbing/binding;
it is not an accepted substitute for the intended free-clearance support. At 3000
MPa pinned ends still fail (4.323623 N). The thin cheeks are therefore rejected
across this uncertainty set. They are design allocations, not unavoidable cam
features: shorter, wider, braced or guided followers could escape. Merely
staggering the shafts does not establish a load-carrying selector.

Shaft sag uses a simply supported 3-mm solid shaft between bearings 10.16 mm
apart, loaded at midspan. It is a local comparison, not torsional-phase
prediction; shaft continuity can change it. In the sparse upper column,
55.4-mm-long 1.6×1.2-mm ground necks have pair pinned/fixed capacities
.740905/2.963621 N at 500 MPa against 1.889049 N, axial loss .054507 mm and
shaft sag .020761 mm. Thus the upper ground return is **restraint-sensitive,
not conclusively overloaded under ideal fixed ends**. At 1500 MPa its pinned
capacity is 2.222716 N, before imperfections. Lower z=18 row bearing necks
have 15.4-mm length and .076297-mm axial loss at 500 MPa; they belong to a
shorter-fork station and must not be combined with the other tier's longest
fork as though they were the same assembly.

At 500 MPa the long fork's ideal fixed unsupported length would have to fall
below **9.468081 mm** just to reach unit buckling load ratio. Bracing alone
does not remove its axial shortening. Reopening requires a changed loaded
section/path and generated guide/frame restraint. Whole-line modulus, fit and
frame errors are correlated. Creep, crookedness, unequal sharing, contact and
housing flexibility remain outside this calculation; no material value or
production yield is inferred. The periodic interior density already implies
about **1,600 cams and 3,200 bearing interfaces/ground necks** for 160 lines,
before boundary support, segmentation, beam contacts, valves or drive/readback.
No complete cost or timing benefit is established.

## Decision boundary and next discriminator

This routing study expands the surviving geometric search space but rejects
its slender follower under dense selected-row load. Continue LAB-206 task 1
with one bounded frame/return synthesis: use the four-phase lanes, generate a
stiff follower/grounded braced load path and rerouted retained beam, charge its bending/axial/contact losses,
and test half-selection across the changed reset envelope. Do not spend on
loaded shaft-phase/dynamics until that geometry survives. A decisive frame or
return contradiction should trigger a campaign comparison against the direct
head and supported ramp alternatives, not another free-post/diameter sweep.
Valve and full-system tasks remain dependent; no fabrication or purchase.

Self-review checks actual web intersection, a deliberate cylinder collision,
continuous sufficient envelope separation, an independent Rayleigh energy
reconstruction of fixed-fixed buckling, and modulus scaling. The Euler model
has no discretization; it is not an independent hardware validation. Groove
curvature, friction, phase/unwinding, beam preload, load redistribution, repeated
wear, full-board boundaries and production fit remain outside this result.
