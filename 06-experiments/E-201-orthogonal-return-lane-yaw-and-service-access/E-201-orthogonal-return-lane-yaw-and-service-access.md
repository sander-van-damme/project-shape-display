---
status: complete
builds-on: [E-200, E-054, E-121]
---

# A side return lane clears the rack but expands guides and blocks extraction

**Retain the side lane as a nominal clearance escape; do not promote it to a
reliable return or individually serviceable assembly.** Moving E-200's leaf into
a separate y lane raises spring-to-neighbor-rack separation from .08 to .60 mm.
The required crossbar and grounded side guides introduce yaw sticking and reduce
frame-to-frame separation to .08 mm. A longer-guide holdout removes the specific
low-friction yaw witness, so the short-guide failure does not reject this family.
Straight slider extraction remains obstructed, even with generous disassembly.

Input main `ff9f972`; LAB-328. Reproduce:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-201/orthogonal.py`.
Python + NumPy; imports retained E-198/199/200 source. Evidence: generated finite
solids/envelopes, analytical bounds, linearized unilateral contact and self-review.
No physical measurements, calibrated manufacturing distributions, nonlinear
coupled contact/dynamics, hardware qualification or independent review. JSON is
reproducible and discarded. No fabrication or purchasing is justified.

## Construction and comparison

This is a routing/guide change within the shared-manufacture investigation,
not another independent fundamental search. E-054 already routes guides around
rack cheeks; E-121's local pull-pull route adds cord/sheave/preload obligations
and does not supply a simpler return here. The new construction moves the E-200
spring contact sideways while explicitly retaining its eccentric wrench.

Keep 5.08-mm pitch, five heights 0/10/20/30/40 mm, q=-.75…0 mm withdrawal,
E-198 rack and island, and E-200 leaf shape/button/lug/seat. Translate leaf and
root/spine to y=1.4…1.8 mm, centered at **e=1.6 mm**. Add an integral crossbar
x=[-1.75+q,-1.75+L+q], y=±2, z=[-2,0], initially L=.6 mm. Its rear face
receives the button. The original island remains y=±.2 and extends to x=.9+q.

Move posts to y=[-2.5,-2.1]/[2.1,2.5], extend their x range to [-2.5,.15],
and widen the three vertical-reaction bridges, stop and base to y=±2.5.
Side cheeks x=[-2.5,-1.75+L], y=[-2.1,-2]/[2,2.1], z=[-2,0] guide the
crossbar. A face-connectivity graph reaches every ground solid from the base.
Bonding/clamps and zero-play guide fits remain idealizations, not assembly designs.

| Combination | Changed causal obligation |
|---|---|
| Side-lane leaf + crossbar slider | Head captures/unloads rack, retracts slider, moves rack, releases leaf, seats and proves support. Leaf supplies force at y=1.6; separate side guides must react yaw. Adds a nonplanar slider and two guide faces/site. |
| E-200 coplanar force contact | Avoids this wide crossbar but has .02-mm actual rack intrusion at its stated ±.025-mm error corner. Its pitch-friction witnesses remain scoped to that guide/mass. |
| Carrier-assembled slider + powered bilateral reset | Avoids reliance on the leaf but needs finite head acquisition, positive state retention after departure, supported jam recovery and outage arrest. Centering its force does not by itself remove this side-guide's static wedging. No completed head is supplied here. |

Unchanged columns remain seated in the intended sequence. Failed seating/height
proof must retain the supported head, allow bounded supported recovery and inhibit
departure. Capture, transfer, false acceptance, readback, arrest and disturbance
are unresolved; positive ground support cannot be inferred from prescribed poses.

## Geometry and manufacturing bounds

At 4/16/64 subdivisions, 125/425/1,625 poses clear: withdrawal after .2-mm
unloading plus all twenty unequal height moves with the slider retracted.
Neighbor rack envelopes cover arbitrary heights; neighbor slider and spring
sweeps cover independent commands. Continuous checks use exact affine slider
unions and monotone leaf envelopes against the finite ground and adjacent solids.
The independent inclined-stem/crossbar separation bound is .038878 mm, inherited
from E-200's finite-nose construction. These bounds supplement discretization.

Spring/rack separation is now in y: **1.4-.8=.60 mm**, independent of the old
x near-collision. With four opposed bounded location/size contributions ±δ,
its conservative margin is `.60-4δ`: .50/.40/.20 mm at δ=.025/.05/.10.
But outer post edges are only **5.08-5=.08 mm** apart. Opposing face errors ±δ
leave `.08-2δ`: .03/-.02/-.12 mm for the same bounds. At δ=.05 the actual
rectangular neighboring posts interpenetrate by **2.438 mm³** (.02-mm width),
not merely overlapping swept boxes. These are explicit scenarios, not X1C or
sheet-cutting accuracy claims. Common absolute translation cancels; shared part
oversize closes gaps board-wide and does not average away.

Zero-play guides are not qualified fits. E-198's adverse gap/interference
problem remains; adding side guides adds another tolerance-sensitive pair.
A side gap g requires yaw of order `2g/L` before diagonal contact: .0167/.0833/
.1667 rad for g=.005/.025/.05 at L=.6. Those are geometric scales, **not** solved
finite-clearance poses; other contacts may intervene. Flatness, shrinkage, warp,
first layer, kerf/burrs, alignment, roughness/friction, creep, anisotropy, wear and
fatigue are uncalibrated. No manufacturing yield or board reliability is estimated.

## Compatible yaw witness and a nonfatal holdout

Represent each side cheek by two normal springs at the crossbar x endpoints,
y=±a (a=2), at the actual tip height. For lateral displacement u and yaw θ,
`Ni=max(-ki ni(u+xi θ),0)`; enumerate all 16 active sets, with independent
Coulomb tractions on the two sides. Coordinates xi are relative to the crossbar
center. Solve lateral force/moment balance affinely in total +y-side traction/H;
intersect activity and friction intervals. No imposed interference or arbitrary
normal preload is supplied. This is an endpoint compliance regularizer in the
rigid limit, not a measured distributed-pressure law.

At L=.6, e=1.6, μside=.2, a finite witness has opposing normals
**N/H=2.571429 each**, and x tractions **-.485714H / -.514286H**. Force and yaw
moment close with nonnegative normals and compatible rotation. An independent
equal-traction witness gives N/H=e/L and μ=L/(2e)=.1875.

The full independent 3D reconstruction applies these forces at E-200's actual
tip z, includes the enlarged slider's weight, and supplies compatible lower-left/
upper-front vertical reactions. Density .008 g/mm³ remains an explicit metal-like
assumption; union volume 6.512 mm³ gives W=.000511062 N. At q=0/-.3/-.75,
H=.000464300/.001160749/.002205424 N, and upper gravity reaction is
.00110119/.00148449/.00205943 N. All six force/moment residuals are <1e-9 in
N and N mm. Tip friction and vertical-guide friction are set to zero: the side
contacts alone supply a sticking witness. q=0 is the limit before the intentional
seat stop engages. A k=10^6 N/mm regularizer makes nominal yaw <1.9e-8 rad;
this stiffness is not assigned to printed hardware. Beam/pose coupling vanishes
in this ideal limit; finite stiffness, impact and return dynamics are not solved.

For this isolated side-guide model, force balance makes the two side normal sums
equal. Combining their moment arm with both traction bounds yields the exact
**infimum** `μ*=L/[2 max(a,|e|)]`. With |e|<a it is not attained: normals diverge
as μ approaches it from above. The code independently recovers feasibility at
1.01μ* and infeasibility at .99μ*. Thus μ*=.15 for e=0 and 1.6; a centered
force also admits sticking at μ=.2, with N/H=10 and opposed tractions -2H,+H.
This static friction-induced couple is not a prediction of a dynamically reached
jam. Increasing force alone scales the witness rather than removing it.

Bounds L=.5/.6/.7 and e=1.5/1.6/1.7 give μ*=.125/.15/.175. Unequal endpoint
stiffness ratios .1/10/1/.1 change displacement, not the finite μ=.2 equilibrium.
These nine geometry scenarios and two stiffness models are sensitivities, not
sampled cells or probability distributions.

**Changed-span holdout:** L=1.4 clears 125 poses and the same continuous envelopes,
while μ*=.35. This defeats any blanket claim that the side lane necessarily jams
at μ=.2. It does not prove return: pitch/roll friction, weight, guide errors,
finite compliance and tip traction must be coupled. No need to tune leaf modulus
or buy a friction measurement to discover this geometric escape.

## Service, scale and decision

Even grant complete removal of the local +y cheek/post and omit the head: straight
lateral extraction first hits the neighboring post after **.58 mm**. Grant removal
of that post too: the adjacent fully withdrawn slider is hit after **1.08 mm**;
at 1.09 mm there is .012 mm³ actual crossbar overlap. Both withdrawn is a legal
local state, sufficient to defeat universal direct extraction. Pure rearward
extraction meets the neighbor rack web after .38 mm; pure downward extraction
hits the lower support immediately. These finite witnesses reject these straight
paths, **not** all multiaxis disassembly or bank-cassette service. No removable
closure, carrier breakaway or safe column-support fixture is implemented.

Repeat 6,400 sliders/crossbars, leaves, sliding tip contacts, rack engagements and
seated stops; guide faces increase from 19,200 to **32,000**. The crossbar can be
integral, but is no longer a planar .4-mm sheet island: it needs a 3D part or an
attached feature with an unpriced manufacturing/assembly process. Forty-site
spring sheets still imply 160 placements, plus 160 hypothetical separate-slider
carrier batches and carrier removal. The short crossbar adds 27.648 cm³ of slider
material across 6,400 sites; L=1.4 adds 64.512 cm³. These volumes are geometry,
not print time, qualified material, scrap or assembly-cost estimates.

The full bought boundary remains `Cshared+Hheads*chead+6400*ccell<500 dollars`;
a hypothetical $250 reserve leaves <$0.03906/site. No quotes or cost pass.
The inherited unearned schedule `6+ceil(6400/Hheads)*s` is 26 s at 160 heads and
s=.5 s, but fails the strict <30-s target at s=.6 s. Capture, unloading, motion,
return, seating, readback, transport, preparation, settling and bounded recovery
all remain charged. Neither spring force nor a static equilibrium provides time.

**Disposition:** preserve the side-lane clearance and longer-guide holdout; stop
optimizing the short-guide passive-return package. It earns clearance, not an
assembly/service or full-machine win. Do not reject sliders, side lanes or force
contact generally. Next change the **retention/service architecture**: construct a
finite powered-reset interface and removable supported cassette together, using
longer side guides as an option. First reconstruct E-116's captured-transfer
failure; a fork, removable cover or stronger actuator must not be assumed to fix
acquisition, retained state or outage arrest. Reconsider if that construction
merely adds repeated precision channels without credible access or recovery.
