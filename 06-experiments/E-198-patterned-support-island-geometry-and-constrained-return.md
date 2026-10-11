---
status: complete
builds-on: [E-166, E-054, E-056, E-165]
---

# Backed sheet islands exchange separate springs for constrained-return friction

**Retain patterned sheets as an assembly option; stop the flat-seat, straight-leaf
passive-return embodiment.** In the stated metal-like bounds, axial tension
created by preventing leaf shortening presses the island into its guide. Even
an optimistic return-force bound cannot overcome μ=.05 from rest anywhere in
the tested stroke. Folded suspensions, shaped release seats or powered bilateral
reset are different mechanisms; none is supplied by this result. No machine,
material, print process or fabrication is selected.

Input main `ceafa81`; LAB-325. Reproduce with
`python3 tools/curated-experiment-checks/E-198/islands.py` (Python + NumPy).
Evidence: finite solid/envelope generation, analytical beam/contact bounds,
nonlinear compatibility solve and self-review. No physical measurements,
calibrated distributions, full CAD/contact simulation or independent review.
Output JSON is reproducible and not retained.

## Search and causal comparison

The axis is **sharing manufacture while separating spring and service-load
paths**. E-165 already tested laminate carriers; E-166 tested formed load-bearing
comb hooks; E-054/056 tested backed rigid sliders. This is their manufacturing
recombination, not a new retention principle or a landscape search count.
The independent source analogy is MEMS suspension/layout synthesis:
[CMU's microresonator synthesis work](https://research.ece.cmu.edu/~mems/projects/memsyn/ressyn/)
constructs shuttles and folded-beam suspensions from physical layout parameters.
It supplies an architectural analogy, **not** dimensions, friction, material
properties or scaling evidence for this machine. Accessed 2026-10-11.

| Combination | Complete causal hypothesis and discriminator |
|---|---|
| Integral straight-leaf island + grounded seats | Shared sheet supplies independent return leaves and rigid lock islands; seats take rack load. Direct head captures/unloads rack, pushes island out, moves rack, releases island, seats/proves and withdraws. Flat backing couples axial stretch to friction: fails guaranteed passive return in the stated cases. |
| Integral folded suspension + same seats | Floating turnaround can accommodate leaf shortening while island stays level; removes the specific straight-leaf compatibility constraint. Extra flexures/links, finite travel, frame and neighbor clearance remain unconstructed. |
| E-166 formed comb hook | Fewer guide contacts, but the service load bends/peels the return finger; known thin-hook runoff and backing obstruction remain. |
| Carrier-assembled rigid slider + independent return | E-054/056 grounded support control; separates spring sizing from support. Temporary carrier can share placement too, so assembly advantage is not exclusive to integral flexures. Retains separation, guide, spring and proof operations. |

All use five rack levels 0/10/20/30/40 mm in this comparison. Independent
bidirectional heads provide motion/energy and local lock opening; spring return
is supposed to restore the positive ground seat. Unchanged cells remain seated.
Failed output/support proof must retain the head, permit one supported retry,
then stop the affected module. Head acquisition, writer geometry, drive/brake,
reader, false acceptance and outage arrest remain unresolved, not free functions.
A returning spring alone cannot arrest a moving column between teeth.

## Connected finite geometry

Coordinates mm: x along release, y through sheet, z up. Pitch 5.08 both axes.
At q=0 the island occupies x=[−1.75,.9], y=±.2, z=[−2,0]. Command q∈[−.75,0]
translates x only. Rack web is x=[1.2,2.2], y=±.8, z=[h−42,h+2]; five teeth
extend to x=.4 at z=h−40+10j…h−39+10j. At each parked h one tooth underside
rests at z=0, with .5-mm island overlap. Full withdrawal leaves .25-mm clearance.

Two in-plane leaves attach at x=−1.45/−.65, z=−2 and end at grounded z=−43:
L=41, in-plane width w=.1, sheet thickness t=.4. Roots are .2 mm to the right
of attachment positions, providing .2-mm engagement preload. A row spine spans
x below the **entire** rack sweep at z=−45…−43. A shorter spine crossing the
rack lanes at z=−15 would obstruct arbitrary heights; long leaves are not granted
free inter-row routing. The tested common spine is a connected bottom route.

Lower guide bridge: x=[−.25,.15], z=[−2.5,−2]. Upper front/rear bridges:
x=[−.25,.15]/[−1.7,−1.4], z=[0,.4]. All span y=±1.4. Side posts occupy
y=[−1.4,−1]/[1,1.4], x=[−1.7,.15], z=[−46,0], joined by a base z=[−47,−46].
A spine foot connects the sheet to that base. Thus the load reactions have actual
routes around the leaves and rack. The front upper face allows the opposite
moment sense during unloaded spring return; a rear upper face alone is not a
complete bilateral guide. These are nominal **zero-play** faces with ideal
rigidity, not a manufacturable exact-fit claim.

The source checks 125/425/1,625 rack/island poses at 4/16/64 subdivisions:
release/reinsert after .2-mm rack unloading, and all 20 unequal height moves
while retracted. Adjacent rack swept envelopes, leaf segment envelopes, frame
solids and eight three-island release patterns are checked. No positive-volume
unintended collision is found. Intended root bonds and touching guide faces are
allowed. Continuous separation follows monotone x bounds: withdrawn tip≤.15,
rack starts .4; neighbor web ends −2.88 while the island starts no farther left
than −2.5; leaf/bridge x or y intervals separate except intended end bonds.
Interior leaf axial displacement and cross-section rotation cannot close those
lateral gaps in the stated beam law. No physical neighbor-disturbance claim.

The leaf centerline is a constitutive shape; the island/guide state is prescribed.
Quasistatic service support and head takeover are not established by these poses.
For a service-only contact control, downward F at x=.6, lower reaction at x=0,
upper rear at x=−1.55 gives Rupper=.3871F, Rlower=1.3871F. At F=10 N, spreading
these over their entire .12/.16-mm² sheet-edge patches still gives mean
32.3/86.7 MPa; the rack/island .2-mm² overlap gives 50 MPa. Loads .1/1/10 N
are comparison scenarios, not requirements. These are demands, not allowables;
real leaf end moments, contact localization and printed-seat creep remain open.

## Why the backing changes return

Two end-parallel beams with transverse displacement d=.2−q are constrained to
retain projected height L by the flat lower seat and ideal guide. A free beam
would shorten; suppressing that shortening generates tensile force. Use small-
slope extensible Euler–Bernoulli (von Karman) theory, A=tw, I=tw³/12, per beam:

`EI v'''' − N v'' = 0`,
`N = EA/(2L) ∫(v')² dz`,
`v(0)=v'(0)=v'(L)=0`, `v(L)=d`.

For a=L sqrt(N/EI)/2,
`v'=C[1−cosh(2a(z/L−1/2))/cosh(a)]`,
`C=d/[L(1−tanh(a)/a)]`,
`N=EA C²[1+sech²(a)/2−3tanh(a)/(2a)]/2`.
Bisection solves compatibility. Horizontal end force is H=NC; the reported
H and N below sum both leaves. E=200,000 MPa is an explicit metal-like scenario.

| d mm | Return H N | Downward leaf reaction N | H/N | Peak total strain |
|---:|---:|---:|---:|---:|
| .20 | .001709 | .21821 | .007834 | .00632% |
| .50 | .018529 | 1.28016 | .014474 | .03042% |
| .95 | .113207 | 4.47437 | .025301 | .10125% |

These are elastic-model demands, not strength/fatigue acceptance. The vertical
reaction presses the island into the lower guide. Total absolute guide normal
force is **at least N**, even granting all balancing moments with no additional
friction. Thus `H−μN` is an optimistic bound on quasistatic return margin after
the column is unloaded. With μ=.05 it is −.00920/−.04548/−.11051 N at the three
poses. A stationary island can remain stuck throughout this stroke; μ=.01 still
prevents guaranteed completion near engagement. μ=0 passes this necessary force
check. No friction value is asserted as measured or universal. Inertia or
externally forced return is a different trajectory, not passive completion proof.

A free-shortening cubic model instead predicts only .002205 N at d=.95 and
relative downward motion `.6(.95²−.2²)/41 = .012622 mm` from the parked pose.
That motion penetrates the lower shelf by .002020 mm³ in the explicit finite
section. Ignoring shortening or granting a perfectly free vertical end while
retaining a flat support seat gives inconsistent physics. Adding only an upper
guide clearance does not remove the lower obstruction. A relieved seat, a
separate lift-before-retract operation or folded suspension may remove it but
requires changed geometry and timing.

Self-review: numerical integration reconstructs compatibility with relative
errors 1.50e−5/5.94e−8/2.32e−10 at 64/256/1,024 intervals. The exact arclength
increment differs from the small-slope value by .0151% at maximum stroke.
The infinitesimal force matches `2Etw³d/L³`; end displacement, touching/penetrating
solid controls and service-only force/moment balances are checked independently.
The derivative of independently integrated strain energy matches end force
within 1e−4 relative at all three reported strokes.
Maximum slope is below .026 nominally. This validates numerical implementation
within the reduced model, not plate torsion, root stresses or contact compliance.

## Manufacturing uncertainty and board consequences

Sixty-four coherent corner scenarios vary E=160,000/220,000 MPa,
w=.08/.12, t=.35/.45, L=40/42, preload=.15/.25 and stroke=.7/.8 mm. Each scans
65 stroke positions. These are epistemic bounds, **not** process distributions,
independent cells or a joint geometry-qualified population. Near-engagement H/N
ranges .00595–.00982; maximum-stroke H/N .02189–.02889. All tested poses permit
sticking at μ=.05; every corner loses completion margin at μ=.01. Peak H spans
.0417–.2472 N, N spans 1.904–8.556 N and peak strain .0765–.1310%. E and stock
thickness change forces but cancel from the friction ratio for this beam law.

An off-geometry polymer-like E=2,000, w=.4, t=.8 control gives H/N=.03850/.03415
at d=.2/.95; widening the leaf changes the ratio, not just stiffness. This is
not a printed survivor or evidence for X1C capability. Finite width packing,
layer orientation, creep and endurance would need new construction/evidence.

Nominal guide height equals island height. Independently bounded top/bottom
surface errors ±e give slot-minus-island gap in [−4e,+4e]: already ±.10 mm at
e=.025. Negative gap means interference; positive gap permits rotation/contact
redistribution outside this fixed-guide model. Relative seat/root bias and sheet
flatness can similarly create or remove axial preload. Common translation cancels;
common relative bias does not average away across 6,400 cells. Kerf, burrs,
residual sheet stress, root radius, out-of-plane buckling, roughness, wear and
forming/cutting yield are unqualified. Printed guide shrinkage, first layer,
warp, anisotropic stiffness/interlayer strength, creep and assembly alignment
remain separate. The .1-mm leaf width is a cut-sheet hypothesis, not a PLA print.

Forty-cell, 203.2-mm-wide ×45-mm-high blanks imply **160 placements** and
1.46304 m² allocated stock, before fixtures, cutting/nesting waste and spares.
This can replace 6,400 individually placed island/return assemblies, but retains
**12,800 leaves, 6,400 rack engagements, 19,200 guide faces and 12,800 side posts**
(the posts may be integral with printed frames). It is placement accounting,
not measured assembly time. One cracked leaf may require replacing a 40-cell
sheet with all its columns independently supported. The common root and guide
frames retain correlated bias/load faults. No free per-cell replacement or
measured printing time/material/scrap advantage is claimed.

The complete bought constraint remains `Cshared+H*chead+6400*ccell<500`.
With a hypothetical $250 reserved elsewhere, resident bought items alone have
<$0.03906/site, or stock alone <$170.88/m² if all other resident operations and
items were free. These are ceilings, not supplier quotes. Stock processing,
heads, readers, wiring, power, brakes, guides and fixtures must also be charged.
At assumed `T=6+ceil(6400/H)*s`, H=160 and s=.5 gives 26 s; s=.6 gives exactly
30 s and fails the strict requirement. The full service slot must include
capture, unloading, release, bidirectional travel, reset, seating and proof;
the 6-s allowance must pay preparation, registration, transport, settling and
bounded retry. Neither slot is earned here. No full/local update-time pass.

**Decision and reopening:** stop optimizing the tested straight-leaf/flat-seat
passive-return package. Do not print a friction coupon: the ideal construction
already needs a different seat/suspension and unqualified sheet manufacture.
Next discriminate a finite folded suspension with a floating turnaround against
a carrier-assembled rigid slider; include root connectivity, bottom-seat contact,
local reset and replacement. Stop that extension if it merely moves the same
constrained-shortening reaction into another hidden guide or increases assembly
without a compensating function. The wider manufacturing axis remains open;
these results do not favor a complete architecture by documentation volume.
