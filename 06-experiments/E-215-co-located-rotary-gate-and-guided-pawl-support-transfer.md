---
status: complete
builds-on: [E-214, E-054, E-056, E-209, E-167, E-174, E-125, E-123]
---

# Turning the ground ring does not create accessible takeover

**Stop the constructed ring embodiment and straight rear-rod slider access.**
Co-location removes the remote eye but not the need for a second accessible
load face. Outer pickup intersects the locked ring; inward pickup meets the
lowest lug rather than the seated lug in four of five old states. The release
spanner also crosses lower lugs. These are scoped contact/access contradictions,
not bans on co-location, rotating supports, axial writing or sliding pawls.
No dimensional/material optimization, purchase or fabrication is justified.

Input main `e96a7d4`. Reproduce: `python tools/curated-experiment-checks/E-215/transfer.py`
(standard library). Evidence: finite rectangular/circular prisms, exact axial
unions, analytic contact/clipping bounds, sampled nominal ring motion and
necessary signed force/timing/cost calculations. **Self-review only**; no measured
priors, loaded-contact solution, actuator design, priced BOM or hardware evidence.
JSON is disposable. Ring-only motion below removes the failed writer explicitly.

## Functional combinations before probing

| Combination | Causal functions and disposition |
|---|---|
| Guided pawl control | Head captures/unloads column, translates shelf-guided pawl, writes height, reverses pawl, proves resident support and detaches. Reconstruct E-054/E-056; separate column restraint, retention and return remain owed. |
| Opposed dogs + axial cam sleeve | Writer takes load between two resident bearing pads; sleeve retracts/reinserts both dogs. Splits support/pickup faces but adds 12,800 dog slides and 6,400 sleeves; defer until access exists. No finite survivor. |
| Stationary column + turning ring | Resident ring carries paired lugs into ground; independent resident column guides remain after departure. Writer lifts column, lifts/turns ring, writes height, reverses and proves. Selected inversion of E-167: avoids cap rotation but adds ring bearings/release. |
| Rocking toe + inward pickup | Moving pickup toward support leaves E-214's miniature release and resident moment obligation. E-209 tails remain; no reduced-output credit. |

Search moves: invert moving/grounded members and split support/takeover patches.
This is functional recombination, not new physics or broad saturation. E-167/E-168
already study bayonet columns; E-123/E-174 expose capture crossing closed guides.
E-124/E-125's retained cup is not offered again. The new test is whether rotating
**the resident support**, while keeping the column still, opens the handoff.

## Direct guided-pawl reconstruction

Import E-054's actual generator and E-056's equilibrium source. At middle bound
e=.35, rack breadth 1.6, wall .4, shelf .8 and bearing .4 mm, reproduce footprint
4.89×5.00, stroke 1.22, unload .47, rail length 2.37 and vertical slot play .55.
Four shelves ground each pawl through two outer walls; favorable 10-N strip
bending demand 5.8594 MPa is not an allowable.

Original x coordinates: web starts .45, tooth ends 3.29, pawl spans 2.52…3.32.
A 1-mm rear nose, y=±.3, z=−1.5…−.5, follows the rear face to x=4.54…5.54.
The next continuous web starts 5.53: **.010-mm nominal penetration**, checked
by exact swept boxes. This stops that straight rod, not dogleg/vertical access.
A tensile coupling is unbuilt; granting one does not remove the collision.

E-056's edge-pressure case F=10, H=−.001, x=0, h=2 demands shelf reactions
**10.0025/−.0025 N**: a failed unilateral condition, not inevitable tipping.
Pawl shelves do not guide the column. No free column reaction, spring, positive
return or retention is borrowed from the writer or E-214.

## Ring construction and actual resident ground path

Units mm/N; z upward. Nonrotating shaft radius .6 carries five 4×.8×1.2 lugs,
undersides z=h−10.1j, j=0…4. Heights 0/10.1/20.2/30.3/40.4 span 40.4 nominal;
±.05 independent tooth-height errors leave ≥40.3 between extreme seats, but no
manufactured transfer pass follows. A 4.6-square cap lies at z=h+70…h+72.
Resolution, dimensions and loads are design scenarios, not product requirements.

Rotor: annulus R=1…2.2, z=−1.4…0, minus a **finite** 4.1×1.2 slot. End bridges
are .15 thick; an infinite slot would make disconnected halves. Locked slot runs
y, leaving opposite x lands under the lugs; a 90-degree turn aligns the slot with
them. Rotor bears across .15 radial overlap on a ground ledge R=2.05…2.5,
z=−1.8…−1.4. A 5-square deck with R=2.05 hole, z=−2.2…−1.8, joins the ledge to
four .4-square corner posts at |x|,|y|=2.1…2.5, reaching z=57.

Two annular column guides (bore radius .65, outer 2.2) occupy z=43.5…44.5 and
55.5…56.5. Bridges x=±2.5, |y|=1.5…2.5 join them to the posts. Full-motion lug
envelope ends at 43.1, including 1.5 unload; lowest cap begins 70. Generated
conservative envelopes clear the posts/bridges; nominal connectivity is checked.
Thus departure retains explicit column → guide → bridge/post → deck reactions,
in addition to lug → rotor → ledge → deck. No loaded attitude, angular retention,
shaft buckling, frame stiffness or bearing capacity is established.

For downward F at transverse yL and horizontal H at z=70, necessary guide
reactions obey `q44+q56=−H`, `44q44+56q56=−F*yL−70H`. F=.1/1/10, yL=−1/0/1 and
H=−.05/0/.05 require signed magnitudes up to .941667 N; opposite signs require
opposite sleeve walls. These are allocations, not solved contact poses. Higher
caps and loaded guide take-up require more analysis. Circular guides do not
silently provide yaw control. Raised rotor keys/keepers and positive return are
unbuilt. Access fails even granting ideal indexing/retention, so these missing
features cannot repair the tested routes.

## Manufactured acquisition and release falsifiers

**Outer takeover:** pads x=±(1.25…1.85), y=±.3 must reach lug underside z=0;
stems beneath them intersect rotor z=−1.4…0. Finite intersection persists in
**32/32 corners at each e=.01/.025/.05**, varying pad x/y position, size, rotor
aperture and slot width independently by ±e. All old states present the same
seat plane. Opening the gate first leaves no vertical contact before pickup:
this is unsupported transfer, not an admissible sequence.

**Inward escape:** pads x=±(.68….88), y=±.15 nominally fit inside R=1 and outside
the shaft. An axial stem from below all lugs first meets j=4 at
**−40.4/−30.3/−20.2/−10.1/0** across old states. Exact sweeps intersect 4/3/2/1/0
intervening lugs before reaching the seated-lug datum. Calling bottom-lug pickup
co-location restores remote, variable-height capture. Retractable fingers require
a new retained bidirectional construction. The .12-mm² combined nominal pad area
would demand 83.33 MPa mean pressure at 10 N, not a material allowable/failure.

**Ground crossing:** nominal lug corner radius 2.039608 leaves only **.010392 mm**
to the ledge hole. Rebuilt lug x/y placement, half-size and aperture edges at ±e
cause actual annular-prism crossing in **8/16, 12/16, 12/16** cases at
.01/.025/.05. This persists with an oracle writer. Widening needs changed ring
bearing support; the result does not reject all rotary supports.

**Release:** four .25-square posts at (±1.3,±1.3) nominally enter proposed .30-square,
.30-deep underside pockets. Pocket sidewalls permit signed torque, but posts only
push axially. The analytic pocket section is separate from the conservative
uncut ring used for collision tests; pockets do not remove the pickup witness.
Circular ledge clearance is .034746 mm; square-post width ceiling at these centers
is **.299138 mm**. Coherent +e placement/+e face bias with −e aperture recession
collides even at e=.01; insertion half-margin `.025−4e` is negative. The supposed
coarse release recreates miniature precision.

At 45 degrees the carrier-connected post stems themselves intersect **4/3/2/1/0
lower lugs** across old states: a diagonal post reaches x≈1.838, y=0, below the
unloaded seated lug. Source clips the rotated finite square against each lug.
The ring clears; its transmission does not. A short side-entering spanner needs
a newly opened ground route. Blind pockets also cannot pull the rotor back down:
a 1-g rotor against .020-N upward drag requires −.01019 N from its underside tool
at zero acceleration. This is its own deterministic return bound, not measured
mass/drag or E-209's rocking model.

## Reach, support proof and uncertainty

Removing the writer, all **20 unequal height pairs** clear nominal ring, ledge
and upper guides through lift 1.5, ring lift .4, turn, height move, reverse turn,
ring lower and reseat. At 8/32/128 subdivisions, **6,300/23,100/90,300 lug poses**
clear. Continuous limits close sampling gaps: during turns seated lug bottom 1.5
exceeds rotor top ≤.4, next lower lug top ≤−7.4; during translation all lugs fit the
open slot. All 25 pairs include five unchanged states. These are necessary
ring-only kinematics; **no nontrivial manufactured supported transaction passes**.

Unchanged cells keep their own rings/guides. Nominal 5-mm frame width leaves .08
between cells; four adverse face/registration terms give gaps .04/−.02/−.12 at
those e values. No full-density manufactured packing or regional-disturbance
pass. Common bank/batch bias and warp need not average away. Misfit cases are
bounds, not X1C priors, independent samples or yield estimates.

The proof table derives actual support by lowering a finite lug .001 into the
gate pose: closed geometry contacts; open geometry does not. Independently
varying reported state reveals unsupported departure on false “locked” acceptance.
Likewise, bottom-lug force cannot prove the requested contact identity. Require
actual height, capture, resident reseating and head unloading before departure;
failed proof must retain last support and stop. Sensors and axis arrest remain
unbuilt. Unknown false-accept p implies 6,400p expected misses without iid assumptions.

Push-only inward capture also fails signed descent: `N=m(g−a)−D`; at m=.005 kg,
D=.060 N, a=0, N=−.01095 N. Source covers two masses, three drag and acceleration
bounds. Hole shrink, first layer/layer quantization, warp, roughness, anisotropy,
wear, fatigue, creep and elastic model discrepancy are uncalibrated; no force
command supplies missing contact. Refining those priors cannot remove the
present geometric contradictions.

## Complete-machine obligations and conditional allocations

| Obligation | Guided-pawl control | Ring proposal |
|---|---|---|
| Residents | 6,400 pawl fits; 25,600 shelves; 32,000 teeth; column guidance/retention/return still owed | 6,400 rotary/axial bearing sites; 32,000 lugs; 12,800 column-guide stations; 25,600 proposed tiny release pockets; angular retention/return still owed |
| Outputs H=40/80/160 | ≥162/322/642: height, height capture, pawl stroke/coupling, shared XY | ≥202/402/802: height/capture, ring axial/angle/return capture, shared XY |
| Assembly | Pawl installation/retention and frame registration | Captured rotor, shaft through two guides, frame registration |

These are complete proposed functional inventories, **not implemented drives**
or one motor/output. Count positive ring-return capture despite its absence from
the tested posts. Coupling functions can lower counts only after construction.
One 10-second operation/site costs 17.78 h; three cost 53.33 h. Print time, scrap,
material mass and assembly yield are unestimated; integrated printing does not
remove joints. Modules are required by the 256-mm bed. At 10 N/head aligned frame
reactions are 400/800/1,600 N before inertia.

Assumed completed head widths 5/8/12 mm require cell strides 1/2/3 and 80/40/27
heads/row. Required rows for H=40/80/160 are **1/1/2**, **1/2/4**, **2/3/6**,
respectively. This is envelope packing, not motor/cable CAD. The 5-mm frame
already fails the e=.025 packing corner; sparse writers do not relax resident pitch.

Six seconds map overhead leaves strict **.15/.30/.60-s** slots. Granting unbuilt
fixed-datum capture, charge two 1.5-mm unload/reseat strokes, |target−old| plus
capture's return to datum, two .4-mm ring lift/lower strokes and two 90-degree turns.
Rest-to-rest triangular scenarios: linear a=1,000/5,000/20,000 mm/s²; angular
alpha=7,200/28,800/115,200 degree/s²; auxiliary .08/.16/.32 s for capture,
registration, settling, proof and bounded retry. No velocity limit is favorable.
Full 40.4-mm excursion maximizes this itinerary. Slots span **.424111…1.806123 s**;
**0/27, 0/27, 3/27** fit H=40/80/160. Common transport/home/preparation is charged
to 6 s, whose adequacy is unproved. This is capacity sensitivity, not performance
credit for collided hardware. The stopped slider earns no new timing pass.

Purchased bound: `Cshared+H*chead+6400*ccell < $500`. With $250 elsewhere and free
resident purchases, head allowances are **<$6.25/$3.125/$1.5625**; at $400 they
are <$3.75/$1.875/$.9375. The reserve already misses the $200 ideal band.
$.01/.02/.04 per resident consumes $64/$128/$256; the last leaves no positive head
budget under $500. Source tabulates all bands: allocations, not quotes or
family-wide cost rejections.

If rocking remains, E-209 still carries **2.247/3.188%** root-error strain,
**3.44/4.31%** tensile-edge strain and **7.56/14.80-N** force tails. Pickup
relocation does not erase them. Ring/slider instead owe their own return,
capture, arrest and wear evidence; no free spring is credited.

## Decision and next discriminator

Stop ring-pocket/ledge tuning: it cannot remove the lower-lug and signed-capture
obligations. Next change **access topology**: construct a permanently open side
portal with separate resident bearing and writer capture faces. Reconstruct
E-123/E-174's closed-guide obstruction; include the portal's missing structural
reaction, unchanged-neighbor stock and actual ground attachment. No alternative
is yet accepted. Reopen the ring only with finite takeover/release routes that
avoid the lug train and establish positive supported departure.

Self-review checks inherited generator/reactions, touch/hole/connected-rim
predicates, exact axial sweeps, rotated spanner intersection, force/moment
residuals, nominal ground connectivity, continuous kinematic limits, subdivision
holdouts and strict timing arithmetic. These verify reduced models only.
