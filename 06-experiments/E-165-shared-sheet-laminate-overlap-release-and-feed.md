---
status: complete
builds-on: [A-019, E-164, E-148]
---

# Shared sheets reduce handling, but do not remove leaf feed or local clamps

**Retain removable assembly carriers; pause the high-interface straight-tip
laminate embodiment.** Common stationary combs permit independent heights. A
permanent rigid moving carrier does not. Two moving leaves/four interfaces have
a collision-free prescribed section; three or more need a changed exit shape.
Even the two-leaf case owes guided upward feed, return and independent clamping.
No complete architecture, process capability or fabrication is selected.

Input main `ac50711`; LAB-268. Reproduce with
`python3 tools/curated-experiment-checks/E-165/probe.py` (standard library;
JSON is disposable). Evidence: generated finite sections, analytical bounds and
self-review. Not equilibrium/contact simulation, fabrication CAD, measurements,
calibrated priors or independent review.

## Functional and assembly comparison

| Construction | Independent height / load path | Disposition |
|---|---|---|
| Permanent rigid moving sheet connecting a row | Forces equal displacement; ground clamps cannot restore missing freedoms | Only 2 of 8 three-cell 0/40-mm maps; reject this carrier, not compliant/slack alternatives |
| Slotted grounded comb sheets + independently attached moving leaves | Bottom runner tie → moving leaves in tension → friction → grounded comb fingers in tension → upper spine/frame | Geometric independence possible; retains every local clamp and leaf attachment |
| Same, moving leaves initially joined by removable cutting/assembly carrier | Attach tabs to individual runners, then remove bridges and verify separation | Fewer sheet placements; residual bridge couples cells, cutting access/debris and inspection are additional operations |
| Broad direct jaw / positive seat controls | Rigid runner → pads or engaged tooth → local frame | Avoid thin-leaf feed; jaw needs larger normal force, seat needs quantization and loaded transfer; neither is selected |

This is a manufacturing recombination of A-019, not a new friction principle.
The independent search axis was sheet connectivity versus assembly sequence.
Primary-source discrete clamping research confirms friction multiplication and
mechanical clamps: Zhou et al., [Discrete Layer Jamming for Safe Co-Robots,
2019, equations 4–6 and Table I](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/6/105859/files/2021/06/118_discrete_layer_jamming_for_safe_co-robots.pdf).
Their laser-cut ABS bending specimens use 70-mm width, 1.5875-mm thickness and
400-mm length. Their friction/modulus/test results are **not** priors for thin
foil, X1C PLA, linear feed or our dense array. Accessed 2026-10-11.
No landscape-saturation claim follows from this one topology investigation.

Complete-machine hypothesis retains A-019's local retained clamp command/wedge,
local reaction cheeks, clamp return/separation, grounded frame, and supported
release. H transported bidirectional heads capture/proof the runner, release its
clamp, position it, restore/proof support and withdraw. Unchanged clamps stay
engaged. A shared end-squeeze through the row cannot independently release one
stack; local stored clamp reactions remain necessary in this embodiment. Neither
sheet cutting nor a shared elevator supplies those functions. Head position is
not output/support verification. Failed proof inhibits withdrawal, reclamps and
allows one supported retry; failed retention needs a catch or module stop.
These mechanisms and the failure-safe sequence are obligations, not built hardware.

## Finite geometry and the exit collision

Coordinates: x across columns, y through the stack, z vertical, all in mm.
Pitch 5.08, finger width 2, contact patch z=[0,20], height h∈[0,40]. There are
n moving leaves alternating with n+1 grounded leaves, thickness t=.05 and
released face gap g=.1. Layer indices j=0…2n: even grounded, odd moving.

Moving leaf occupies z=[h−42,h+22]; its 2-mm-deep carrier lies below h−42.
Ground fingers extend z=0…64 to a common spine at z=64…66, above the entire
moving sweep. Thus 64-mm moving leaves retain the full 20-mm patch throughout
40-mm travel. Body/connector swept envelope is −44…66: **110 mm**, before
writer/surface/frame. A 2.8-mm-wide carrier leaves 2.28 mm between neighboring
carrier envelopes. Ground spines cross x only above all moving leaves.

Let c run from 0 released to 1 packed. In the patch,
`y_j=(j−n)[t+(1−c)g]`; anchors retain `(j−n)(t+g)`.
Use `S(u)=3u²−2u³`, clamped to [0,1]. Ground fingers blend from packed positions
at z=20 to open positions at 64. Moving fingers blend from their bottom anchors
to packed positions at 0, then have **straight free upper tips**. Finite bodies
are width-2 extrusions with y-thickness t. These are a prescribed small-deflection
shape hypothesis; contact equilibrium is not imposed by naming them flexures.

At n=3, h=40, c=1, z=30, ground layer 4 has y=.063148009 and moving layer 5
y=.100000000. Their .05-mm-thick sections **overlap by .013148009 mm**.
The offending bodies share x and z: this is actual section penetration, not
bounding-box overlap. The same topology fails for n=6/12. As grounded inner
fingers spread toward anchors they enter outer moving tips. Refining 64/256/1024
samples gives maximum observed n=3 overlap .048828/.049654/.049933 mm; the
analytic z=30 witness establishes failure independently of the sampled maximum.

At n=1/2 the grounded outer leaves spread away from moving tips; the n=2 middle
grounded leaf stays centered. Ordering and finite thickness remain nonintersecting
for every c∈[0,1], h∈[0,40] in this prescribed section. The source explicitly
checks 64 combinations of three neighboring endpoint-height/clamp maps for n=2.
Moving carrier and common spine never meet. Intervals prove overlap for intermediate
heights; sampled maps alone do not. This is **rigid-frame geometry**, not proof of
neighbor immobility under clamp forces or of a realizable return trajectory.

Allowing the moving tips to bend/splay under extra contacts, guiding every layer,
using side-rooted combs or changing the leaf termination can remove the collision.
Those changes need a new contact/return construction; rejecting the prescribed
straight-tip branch does not reject laminar jamming. Merely adding interfaces to
the A-019 scalar force formula does not construct that exit.

## Feed, release and manufacturing bounds

Downward parked load puts both sets of leaves in tension in this routing. During
upward travel, however, a bottom attachment **pushes** its moving leaf against
residual drag. Downward runner load does not prevent this internal compression.
The first possible patch contact is 42 mm from the bottom attachment at h=0;
contact at the upper patch edge instead gives 62 mm, or 64 mm at the free tip.

For width w=2, `I=w*t³/12`, `Pcr=π²*E*I/(K*L)²`. E=2,000/200,000 MPa are
explicit polymer-like/metal-like scenarios, not measured material assignments.
K=.5/1/2 bounds alternate end restraint, without claiming a real end constraint.
Pinned sinusoidal imperfection e gives the reduced relation
`amplitude=e/(1−P/Pcr)`; demanding amplitude<g/2 gives
`P<Pcr*(1−2e/g)`. This is a pre-contact beam screen, not postbuckling capacity.
For K=1, L=42, g=.1, e=.01:

| E (MPa), t (mm) | Pcr per leaf | Clear-feed load per leaf | Equal drag allowance per face |
|---|---:|---:|---:|
| 2,000, .05 | .000233 N | .000187 N | .0000933 N |
| 200,000, .05 | .023313 N | .018650 N | .009325 N |
| 2,000, .4 | .119360 N | .095488 N | .047744 N |

Metal-like .05-mm Pcr falls to .010698/.010040 N at L=62/64. A .02-N-per-face
residual-drag scenario exceeds even the optimistic 42-mm metal-like bound;
zero drag does not. No real drag is measured. Guide confinement may stabilize
the leaf but adds contacts, drag and alignment, so it cannot be silently granted.
108 coherent corners vary E, t=.05/.1/.4, K, e=0/.01/.05 and g=.1/.2;
clear-feed thresholds span 0…47.744 N, demonstrating strong model dependence,
not yield or a material ranking. Initial curvature, end restraint and contact
location must be resolved together before claiming reliable feed.

The shortest lower flexure is 2 mm at h=40. In n=2 each moving leaf shifts .1 mm.
A fixed-guided beam approximation gives `strain_max=3*t*delta/a²` and
`Fend=E*w*t³*delta/a³`: .375% and .625 N per metal-like .05-mm leaf; 3% and
3.2 N per polymer-like .4-mm leaf. These are demands, not qualified elastic,
fatigue or creep limits. Longer flexures reduce strain but increase unsupported
feed length and depth. Force shunted into bending means outer squeeze is not
automatically equal pressure at every interface.

For relative anchor/slot bias b and per-surface departure bound r, released
clearance is at least `g−2r−b`. At g=.1, (r,b)=(.01,.02)/(.03,.04)/(.05,.05)
gives .06/0/−.05 mm; g=.2 with (.03,.04) gives .10 mm. Opposed bow/slot offsets
can repeat coherently over a printed module. Four-gap n=2 closure stroke may
need .56/.80/1.00/1.20 mm respectively, not nominal .40 mm. Uniform translation
cancels; relative layer pitch/warp does not. An outer open gap alone cannot prove
that internal leaves separated. Cut-foil burrs, residual curvature, roughness,
contamination and adhesive contacts are separate from X1C hole shrinkage,
first-layer/XY bias, frame warp, layer quantization and assembly error. No .05-mm
printed leaf is proposed. Printed .4-mm flexures still owe orientation-dependent
strength, interlayer integrity, creep, fatigue and wear; no distribution or
lifetime is inferred from these bounds.

## Board accounting and decision

With ideal equal transmitted N at all four n=2 interfaces,
`Fhold=4*mu*N`. At 10-N load and mu=.05/.2/.4, N=50/12.5/6.25 N and mean
pressure on 40 mm²=1.25/.3125/.15625 MPa. At 1 N these fall tenfold. Loads and
friction are scenarios, not stage-02 requirements. A two-pad jaw needs twice N
under the same equal-pressure assumption, while avoiding foil feed. Elastic
shunts, pressure nonuniformity, unloading and clamp creep reduce the ideal credit.

A 40-column tile is 203.2 mm wide before fixtures. Two tiles/row ×80 rows gives
160 tiles. n=2 uses **480 stationary comb sheets +320 temporary moving-carrier
sheets**, versus 32,000 separately handled leaves: a potential 40× reduction in
sheet-placement count, **not measured assembly time**. It still has 12,800 moving
leaf attachments, 25,600 friction interfaces, 6,400 independently retained clamps,
returns, commands and local reaction paths. Removing each of 320 row carriers
must leave 12,800 independently moving tabs; residual bridges are common faults.
Controls can also use carrier-assisted assembly, so this advantage is not exclusive.

Allocated rectangle stock area is 10.859 m² before nesting/reuse, cutting kerf,
spares or scrap, using 66/68-mm stationary/moving blanks. With hypothetical $250
reserved elsewhere, **all stock alone** must cost <$23.02/m² if all remaining
hardware is free. Joint budget is `Cshared+H*chead+6400*ccell<500`; no quote or
BOM pass. The .05-mm stack plus two assumed .8-mm cheeks occupies 2.25 mm in y;
this is an allocation, not constructed jaws, flags or loaded printed walls.

Common frame is a correlated uncertainty: a simply supported 5×10-mm beam with
assumed E=2,000 MPa, carrying 10 N per 5.08 mm, gives linear deflection diagnostics
52.44/.2048/.005244 mm for support spacing 203.2/50.8/20.32 mm. The first is outside
small-deflection validity and is not a physical prediction. It exposes why rigid
spines need distributed backing. No new disturbance tolerance is introduced;
adding backing adds assembly and does not remove total load into the base.

E-148's optimistic `T=6+ceil(6400/H)*service` requires H=121/137/149 at
service=.45/.50/.55 s for strict <30 s, including only the assumed 6-s shared
allowance. Laminate feed/release/proof time has not earned those allowances or
parallelism. Preparation, registration, transport, readback, one bounded retry
and settling remain in the budget. Readback must detect support loss and internal
bridges; assumed per-cell false acceptance p gives 6,400p expected misses without
independence, not a validated rate. No regional, cost or reliability pass.

**Stop** detailing the tested high-interface straight-tip construction. Retain
common fixed sheets/removable carriers as an assembly tool and n=1/2 as conditional
geometric controls. Reopen laminate development with a finite supported upward-feed
and layer-separation construction that retains its normal-force advantage over a
broad jaw; include moving-tip splay if using more interfaces. No print request:
these geometric/guide obligations precede informative material calibration.
Next portfolio question: can a shared-sheet assembly method improve a positive
load stop without needing a compressively fed foil? Cross-check A-010 and existing
seat-array work first; if duplicated, reopen a different functional combination
rather than optimize laminate friction again.

Self-review: analytic collision reconstruction, interval endpoint/continuous
ordering checks, released limit, 64 neighbor maps, Euler Rayleigh-quotient
quadrature, t³ scaling, imperfection boundary, fixed-guided energy/force identity,
sampling sensitivity and integer timing. These verify the stated reduced models;
nonlinear contact, root/frame compliance and actual manufactured return are absent.
