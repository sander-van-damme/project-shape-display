---
status: complete
builds-on: [E-206, E-166, E-054, E-056]
---

# Thick toe on a shared bending comb cannot withdraw from its keyed seat

**Stop the tested monolithic, keyed-seat construction.** Separating section
thickness removes E-206's uniform-stock conflict without installing a toe insert:
a thick printed toe joins a thin bending leaf through a finite tapered collar.
The positive withdrawal keys then obstruct release. Across 16 explicit coherent
bank scenarios, the first sampled collision occurs after .02036–.18322 mm of
withdrawal, with the key still .11711–.24617 mm below the ledge surface.
Removing the keys clears the modeled release path but removes positive
withdrawal restraint. Neither construction earns a supported update sequence.
This does not reject thickened combs, flexures, alternate force/moment inputs,
rocking seats or longer torsion returns.

Input main `7183367`; LAB-334. Reproduce:
`python3 tools/curated-experiment-checks/E-207/keyed_toe.py` (Python + NumPy;
imports E-166). Evidence: finite prisms, quasistatic inextensible elastica,
compressive-reaction existence, bounded scenarios and self-review. No physical
measurements, fabrication CAD, process qualification, independent review,
purchase or printing. JSON output is reproducible and not retained.

## Construction and actual connection

Coordinates: x across cells, y toward the rack, z upward; dimensions mm.
The **single-material, monolithic comb** is deliberately different from
inserting 6,400 rigid toes into metal-sheet sockets. Its 40 toes and return leaves
would share a stationary spine across 203.2 mm; two combs per row give 160 comb
placements. That is an allocation, not a validated print layout or assembly time.
The source constructs the local root boundary and grounds it ideally; a shared
spine/clamp's flexibility and complete 40-finger solid are not modeled.

Each toe occupies x=[−1.5,1.5], y=[−1,1.6], z=[0,2]. An inset rack-contact pad
x=[−.4,.4], y=[.8,1.2], z=[2,3.4] bounds the service load location. The upward
cantilever leaf is .8 wide in x and .4 thick in y, centered at y=−.6, from
z=−12.2 to −.2. Its top finite face joins a tapered collar that widens from
.4 at z=−.2 to .8 at z=.4; the collar overlaps the toe. The source verifies
that both leaf-edge coordinates coincide with the collar's bottom face at
rest and two bent states. This is a continuous printed junction, not a pinned,
friction-fit, adhesive or zero-area connection. Treating the toe/collar as rigid
and the junction as perfectly clamped remains a constitutive approximation;
fillet stresses and effective flexible length are unqualified.

Two ground ledges outside the rack, x=[−1.7,−.85] and [.85,1.7], have their
upper face at z=0 and extend y=.4…1.7. Deep beams and rear walls connect them
to the root ledge without entering the rack's swept volume. They do not guide
the toe throughout withdrawal. Each toe wing has a downward key at y=.85…1.15,
depth .2; each ledge has a socket y=.75…1.25 with a floor at −.35. The .1-mm
end clearances allow small lost motion; the vertical socket walls then provide
**positive withdrawal restraint**, unlike a spring-only detent. No upper lip,
axle or second slider is used. The pad keeps vertical loads inside the ledge
support polygon; large lateral moments or upward extraction are not qualified.

A rigid five-tooth rack uses 10-mm spacing and 2-mm teeth, giving five selectable
heights over 40 mm, as in E-166. Tooth footprints are x=±.4, y=.6…1.7; the web
lies at y=1.7…2.2. This discretization is an embodiment, not a new requirement.

## Ground support, takeover and the blocked transition

At rest four admissible ledge contact points, x=±1.1 and y=.5/1.45, surround the
entire inset pad. Nonnegative reaction weights balance .1/1/10-N vertical loads
at all four pad corners, with force/moment residual <3e−15. Nominal support
margins are .7 mm in x and .25 mm in y. This is existence of compressive
reactions, not a pressure, shelf strength, friction or elastic-contact solution.
Unchanged neighboring toes retain these contacts; their solid envelopes are
unchanged. The 3.4-mm-wide local frames leave 1.68 mm between adjacent sites at
5.08-mm pitch. Common frame deflection and miniature disturbance are not solved.

The finite takeover control is a C jaw entering from +x. Lower/upper 1-mm-thick
fingers occupy y=1.35…1.65, x=−.35….8, at z=2.4…3.4 and 5.4…6.4; a spine at
x=.55….8 connects them outside the rack. The inset pad provides lower-finger
clearance above the main toe. The model checks 33 acquisition and 33 .8-mm-lift
poses against the toe, frame and rack. Touching jaw faces idealize closed fit;
a closing drive, retention and force limiting remain explicit head obligations.
For a planar load at y=.8…1.2, lower contact at y=1.4 and upper at 1.6 require
lower reactions 2W…4W and opposing upper reactions W…3W. Thus the 10-N screen
can require **40 N upward plus 30 N downward** from the head. Roll accommodation,
registration error and jaw compliance are not proven. In the rigid model a
continuous load share between seated toe and closed jaw is possible; after
lifting, only the jaw carries the selected rack. This is a nominal takeover
control, not a complete qualified writer.

Next apply a moment-free rearward transverse force at the leaf endpoint, while
the jaw keeps the rack .8 mm raised. This is the specified release input; an
actual opening-tool contact and actuator would still be required. The leaf
bends backward, the toe pitches nose-up, and the endpoint falls slightly.
The intended sequence is withdraw → move rack → return toe → lower and prove
support → open jaw. **It stops during withdraw:** the keys meet the rear socket
walls before lifting out. Increasing force after first contact is not the
simulated path; it would require contact-induced deformation/stress analysis.
No normal reseating, recovery or dock completion is claimed.

| Segments / command subdivisions | First sampled withdrawal collision (mm) | Key bottom at that pose (mm) | Keyless open rack gap (mm) |
|---|---:|---:|---:|
| 32 / 32 | .127454 | −.177706 | .406683 |
| 64 / 64 | .106235 | −.181308 | .406932 |
| 128 / 128 | .106246 | −.181307 | .406994 |

These are sampled event brackets, not precise onset estimates. Command runs
from zero to `q=|H| L²/EI=.34`. A small-angle independent check explains the
failure: key rise per endpoint withdrawal is initially `3a/(2L)` with a=1.45,
only .174… .189 for L=11.5…12.5. End-play clearance of order .1 mm therefore
buys only order .02 mm of lift, much less than the .15… .25-mm key depth.
This local linear check is not a global swept-volume certificate.

The **keyless control** clears the ledges in every sampled phase and all 16
corners. At nominal dimensions the leaf, lifted rack and acquired jaw also
clear throughout; open toe/rack y projections are disjoint. Projection exclusion
covers all 20 unequal height transitions for the toe alone, not the moving jaw.
Its reversed free path is likewise clear. It cannot establish supported
reseating of the keyed device, or replace positive retention with an assumed
small spring force. Finite convex contact tests distinguish touching from
penetration; E-166 derivative, equilibrium and small-load checks are rerun.
The centerline integration is independently reconstructed and checked against
the solved endpoint. No stochastic seed, yield estimate or reliability claim.

## Manufacturing and constitutive bounds

Sixteen deterministic bank corners combine L=11.5/12.5, nominal socket end play
.07/.13, relative socket translation ±.05 and key depth .15/.25. Relative rear
clearance is therefore .02… .18. Each corner stays fixed through its entire
sequence and may apply to all 40 fingers; shared batch offsets can affect many
banks. Socket floors retain .15 clearance in these favorable corners. This
purposefully isolates release after an initially valid fit. Common translation
cancels; opposed toe/seat bias does not. All 16 corners obstruct keyed release.
These are **labelled bounds, not sourced X1C distributions or statistical yield**.
Nominal leaf/frame/jaw checks are not extrapolated to full-body corner robustness.

A separate assumed E=700/2200 MPa, t=.35/.45 and L=11.5/12.5 screen gives
.00435… .03436 N for the unobstructed q=.34 motion. Nominal .4-mm leaf maximum
outer-fiber strain is .56018%. Neither is a material allowable or a force claim
once keys contact. Toe transverse simply supported strip bending at a 2.2-mm
span, thickness 2 and effective breadth .4/1 gives **8.25…20.625 MPa at 10 N**
(.825…2.0625 at 1 N). The .32-mm² pad additionally sees average compression
31.25 MPa at 10 N. Thus rigidity is not free: even illustrative 8/40-MPa ceilings
change the apparent service margin. Thin ledges, collar stress concentrations,
creep and layer direction remain unsolved. Loads are comparison scenarios,
not established tabletop requirements.

For the 1-mm jaw, a favorable .3-mm-wide strip with .55-mm lever and 40-N lower
reaction already gives `6Fl/(bt²)=440 MPa`; a real metal head, broader bearing,
revised contact or lower load needs justification and cost. The printed toe is
not itself a complete writer. These favorable rigid-body assumptions cannot
remove the key collision; they also cannot prove any survivor's strength.

Baseline fabrication is X1C/PLA/.4-mm nozzle; .2-mm nozzle is optional. A .4-mm
return can be a single-extrusion feature, and a thick toe on an upright thin
leaf creates support/orientation issues. Neck wall bias, layer quantization,
first-layer changes, warp, roughness, interlayer strength, fatigue, creep, wear
and spine/clamp misalignment are uncalibrated. The model grants a stress-free
initial seat and rigid root rather than inventing a distribution for those
unknowns. Printing is not justified to rediscover the finite obstruction.

## Burden, alternatives and decision

| Construction | Repeated/assembly burden | Disposition |
|---|---|---|
| This thick monolithic comb | 160 possible comb placements; 6,400 toes, collars and bending necks; 12,800 keys/socket fits; zero separate toe inserts, folds, pins or bearings | No extra full-stroke guide, but positive keys block release |
| E-054/E-056 slider | 6,400 separate pawls and guided fits; 25,600 shelf faces, plus return/stops/head | Service-support comparator; its retention and moving fit are not magically solved |
| E-206 longer torsion control | 160 possible sheet placements; 6,400 toe folds/torsion necks and rotary seat fits | Favorable 10-N stock bound needs about 20–22 mm at 65°; lip, seat fit and positive yaw restraint remain open |

The comb still needs distributed grounding and accessible module attachment;
an allocation of two clamp rails and four fasteners per comb means 320 rails
and 640 fasteners, **not constructed/qualified clamp geometry or a quote**.
A bad neck can force replacement/support of 40 cells. No 40× assembly-time
claim follows from placement counts, and there is no credible current savings
from adding a second local guide merely to unlock these keys.

Complete-machine obligations remain
`Cshared + H*chead + 6400*ccell < $500`, preferably below $200–400. Allocating
$250 elsewhere leaves <$0.03906 per purchased resident bundle; shared clamps,
actuators, capture/opening tools, motors, sensors, guides, wiring and supplies
all count. With an illustrative 6-s map overhead, H=40/80/160 simultaneous heads
permit strict service slots <.15/.30/.60 s. Acquisition, close/lift, release,
40-mm height motion, return/reseat, support proof, withdrawal, transport,
settling and bounded retry must all fit. No timing or cost pass is claimed.
A one-cell update need only address one leaf in principle; jaw transport,
readback false acceptance and bank disturbance remain unbuilt. Failed proof
must retain head support; closed-looking keys alone are insufficient evidence.

**Next changed physical axis:** change release kinematics/positive retention
at the load seat, rather than adding toe inserts or extending a translation
guide. Test a rocking seat or localized curved flexure that produces initial
key lift with little withdrawal, including the required force/moment input and
support polygon. Alternatively revisit longer torsion returns if a finite lip
and positive yaw restraint can be supplied. The failed straight-cantilever path
must not be reused as though unloading solved its key interference. This is one
local topology probe; no new fundamental principle or search saturation is
claimed. Stop detailed head recovery and print preparation for this embodiment.
