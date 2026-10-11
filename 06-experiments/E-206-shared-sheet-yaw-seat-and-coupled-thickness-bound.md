---
status: complete
builds-on: [E-166, E-056, E-205]
---

# A rounded yaw seat clears the rear backing but exposes lip and stock conflicts

**Stop this short, uniform-sheet yaw-pawl construction under the tested bounds.**
Rotating a rounded heel sideways escapes E-166's rear-stop obstruction without
an axle or separately guided slider. The upper support lip instead intercepts
the twisting return strip: wide strips collide nominally; the narrow strip
collides at an adverse relative bank offset. Independently, the short strip's
release-stress ceiling conflicts with the toe's 10-N bending requirement, even
under deliberately generous material scenarios. This is not rejection of yaw
release, shared manufacture, lower loads, longer returns or reinforced toes.

Input main `01061a7`; LAB-333. Reproduce with
`python3 tools/curated-experiment-checks/E-206/yaw_seat.py` (Python + NumPy;
imports E-166). Evidence: generated finite sections/prisms, prescribed-motion
checks, unilateral static equilibrium, linear-elastic necessary conditions and
self-review. No fabricated CAD, physical measurements, calibrated process
priors, independent reviewer, purchase or print. JSON output is disposable.

## Changed physical combination and finite route

E-166's actual finite rear block, y=[−1,−.2], z=[11.8,12.8], intersects
**55/65** unloaded-release poses, first at 15.625% command. The source reconstructs
this from E-166's elastica, not its summary. Unloading does not remove the block.

Here z is upward; x crosses columns, y points toward the rack; all lengths mm.
A horizontal pawl has a circular heel radius .6 centered at (0,−.4), joined to
a rectangular nose x=[−.4,.4], y=[−.4,1.3], thickness t=.2. An integral vertical
return ribbon of width .4/.8/1.2 and the **same stock thickness** rises 12 mm
from the heel to a common grounded spine. A locally applied clockwise yaw of
65° swings the nose sideways; the ribbon twists about its vertical centerline.
The sheet-to-toe fold is an ideal connected right-angle joint; forming radius,
warping restraint and joint stress concentration are not credited as solved.

Ground consists of a lower ledge x=[−.6,.6], y=[−1.6,.3], z=[−.8,0]; an upper
heel lip x=[−.8,.8], y=[−1.6,−.7], z=[t,t+.8]; and a connected rear wall
x=[−.8,.8], y=[−1.6,−1.15], z=[−.8,t+13]. A top crossbar spans y=[−1.6,−.15],
z=[t+12,t+13] to connect the ribbon root to that wall. The .45-mm rear wall and
cantilever ledges have no qualified stiffness/creep result. Rack teeth occupy
x=[−.4,.4], y=[.6,1.7], thickness 2; the web occupies y=[1.7,2.2]. Five teeth
at 10-mm spacing encode 0/10/20/30/40 mm as in E-166, not a new height requirement.

The pawl/ground geometry has nominal touching contact at both horizontal seat
faces. With a hypothetical head carrying the rack and lifting it 1 mm, the
prescribed flat pawl can yaw and return without hitting its rear wall or teeth.
At 65°, actual nose/rack separating-line reserve is **.20437 mm** over 32 coherent
corners (pawl x/y, rack x/y and frame y each ±.05). Rack/seat contact width before
release remains ≥.7 mm. The open footprints exclude every intermediate rack
height, hence all 20 unequal height transitions. Ground also clears the entire
rack sweep. Pawl radial envelopes leave **1.48715 mm** between opposite adjacent
commands, including ±.05 x placement. Unchanged neighboring pawls need no common
release; their nominal contact points and positive vertical reactions persist
under these planar corners. This assumes rigid grounding, not zero vibration.

At 16/64/256 yaw subdivisions, 6,528/24,960/98,688 prism checks agree. The circular
heel uses a circumscribed 128-gon (radial overestimate <.00019 mm); its rotational
invariance and the neighbor-circle bound do not depend on angular sampling.
No complete swept-solid or compliant-motion certificate follows from samples.

**The return ribbon breaks this apparent clearance success.** At the real
interior section z=t+.05, with linear prescribed twist from the grounded root,
both .8- and 1.2-mm ribbons intersect the upper lip already at nominal 65°.
The .4-mm ribbon clears nominally; its all-angle radial reserve to the lip is
only .07639 mm. Opposed ±.05-mm ribbon/frame y offsets produce a finite collision
in one of four coherent corners. The same bank bias can affect all 40 fingers;
this is not an independent-cell yield estimate. Moving the lip, narrowing the
ribbon or changing its attachment can reopen the question, but must preserve
upper-heel contact area and moment reaction. Removing the lip is not a repair.
An additional bending/warping escape is unmodeled, not ruled out by this
prescribed-twist collision.

## Load equilibrium and coupled stock thickness

For an adverse vertical tooth load W at y=1.3, admissible nominal contact points
are lower y=.2 and upper y=−.85, both on the generated bodies. Force and moment
balance give `Rlower=2.047619 W`, `Rupper=1.047619 W`. At 10 N the ledge therefore
carries **20.476 N upward**, and the upper lip **10.476 N downward**. The source
also checks shifted contact positions and residuals at the planar bank corners.
This is existence of rigid compressive reactions, not solved elastic pressures.
Compared with E-166, the ground can carry the peel moment; the thin nose still
must carry bending between the rack and the foremost lower support edge.

A rectangular, unreinforced nose section of width b requires
`t ≥ sqrt(6 W l/(b sigma))` to stay below a chosen elastic bending-stress ceiling.
Use b=.7/.9, adverse edge-load arm l=.9/1.1, and ribbon length L=11.5/12.5.
Edge loading is allowed by the actual finite contact; uniform pressure or moving
support under the rack would be different models. The full section moment is
accounted for; hidden ribs, laminates or a rigid toe insert are not granted.

For release, the Saint-Venant rectangular-strip solution gives
`tau_peak = G theta k(w,t)/L`, with w=.4 and k computed by a converged rectangular
stress-function series. In the thin limit k→t. The
[MIT structural-mechanics notes, Unit 11](https://ocw.mit.edu/courses/16-20-structural-mechanics-fall-2002/15610a00dfce40d899a2ea0cbe414e57_unit11.pdf)
provide the isotropic stress-function/membrane formulation and narrow-strip
limit; accessed 2026-10-11. A separately implemented finite-difference Poisson
solve checks the series at w=.4,t=.2: 16/32/64 thickness cells differ by
−.1725/−.0432/−.0108%; the series gives k=.186012 mm. Thin-strip and axis-swap
limits are also checked. Finite twist, end warping restraint, residual forming
strain and nonlinear ribbon behavior remain model discrepancy.

These are **alternative scenario ceilings**, not sourced stock grades or PLA
allowables. In particular, equal bending/shear ceilings deliberately favor the
metal-like cases; they are not a consistent ductile-yield qualification.

| G / bending ceiling / shear ceiling (MPa) | 10-N toe minimum t (mm) | 65° return maximum t (mm) | 1-N thickness-interval survivors / 8 corners |
|---|---|---|---|
| 77,000 / 400 / 400 | .3873–.4855 | .05266–.05724 | 0 |
| 60,000 / 800 / 800, deliberately favorable | .2739–.3433 | .13747–.15069 | 8 |
| 700 / 40 / 20, polymer-like | 1.2247–1.5353 | .4 search cap | 2 |

All **24 ten-newton corners fail**; 72 total load/material/geometry cases cover
.1/1/10 N. At .1 N all thickness intervals survive, and the favorable 1-N case
retains only six of eight intervals after a coherent ±.02-mm stock tolerance.
These counts concern necessary stress inequalities only: the ribbon/lip collision,
seat fit, fatigue, printing and support transfer are not cleared by them.

The 65° command is not the reason for the ten-newton rejection: the worst planar
corner needs ≥**51.9167°** merely to clear the finite nose, with zero reserve.
Even there, the most favorable 10-N section requires L≥**15.596 mm**, beyond
12.5. At 65°, favorable length requirements are **19.527–21.784 mm**. Longer
ribbons are therefore a genuine reopening condition, not a forbidden family;
no compactness requirement forbids them. Their cap interference and manufactured
seating would still need reconstruction. Thicker formed/reinforced toes with
separate thin returns instead remove the shared-thickness conflict directly.

Vertical fit is an additional unresolved repeated interface. With zero nominal
seat gap, roof/floor errors ±.05 and stock error ±.02 give gaps **−.12…+.12 mm**;
four of eight corners interfere. Adding .15 nominal clearance gives .03… .27,
which permits unloaded pitch and changes service seating and yaw paths. The flat
prescribed path does not certify those poses. No X1C tolerance distribution,
roughness/friction, anisotropy, first-layer error, warp, creep, fatigue, wear or
forming quality is calibrated here. Bounds may correlate across a whole comb.

## Machine obligations, comparison and disposition

| Construction | Repeated hardware/contact burden | Consequential result |
|---|---|---|
| E-166 unbacked comb | 6,400 formed hooks/elastic returns; 160 sheet placements | Thin nominal metal-like hook runs off near 1.758 N; rear stop blocks release |
| E-054/E-056 side-wing slider | 6,400 separate pawls/guide fits; four shelf faces per site plus return/retention | Ground support comparator, with pressure/fit and writer obligations |
| This integral yaw sheet | 6,400 toes, folds and torsion necks; upper/lower contacts and rear backing per site; 160 possible sheet placements | Avoids an axle and full-stroke sliding guide, but creates rotary heel fit and the two failures above |

Forty fingers across 203.2 mm could share one comb; two per row ×80 rows gives
160 placements and .48768 m² at an assumed 15-mm blank height, before cutting,
forming, fixtures and rejects. These are allocation counts, not a validated
flat pattern, print time, assembly time or procurement quote. A comb fault can
require supporting and replacing 40 sites. The 40× placement reduction versus
loose hooks does not remove 6,400 precision folds, seat fits or wear cycles.

Selection still requires a transported locally addressed head, bidirectional
rack capture, unload stroke, yaw tool, local force limiting, held-open return,
height drive, actual support proof and withdrawal. **That head is not built by
this experiment.** The finite path assumes its reaction only to identify a
necessary-condition failure; it is not a supported-handoff demonstration.
Unchanged sites stay seated. The changed rack must remain captured through
opening, all height motion, reseating and load proof. Failed closure/proof keeps
the head engaged; a bounded supported retry precedes a module stop. Power loss
or loss of yaw command during travel can drive a tooth into the returning toe;
passive return is not qualified arrest. Side loads may yaw the pawl against its
spring; no positive yaw lock or favorable friction has been supplied. A sensor
reading closed angle cannot prove seat load transfer, and false acceptance is
unbounded; assumed per-site p implies 6,400p expected missed supports regardless
of independence. Rescue/dock construction remains downstream of normal takeover.

With the inherited illustrative 6-s per-map overhead, H=40/80/160 concurrent
heads have strict service-slot ceilings **.15/.30/.60 s** for <30 s. Every action
above, registration, transport, settling, verification and bounded retry must
fit; no timing pass. A one-cell update needs one selected head in principle,
but acquisition is not implemented. Purchased cost still requires
`Cshared + H*chead + 6400*ccell < $500`; $250 elsewhere leaves <$0.03906 per
resident bundle. No priced BOM, complete machine, regional-disturbance or
reliability pass follows.

**Decision / next physical axis:** retain rounded yaw bypass as geometric
knowledge; stop this short uniform-sheet construction and detailed recovery
work on it. Next separate a rigid service toe from a bending return sheet,
constructing the attachment and supported reseating without a hidden pivot,
loose pin or second precision channel. Compare the added joints/placements
against the existing slider before deeper development. A longer torsion ribbon
is an alternative if its finite lip clearance and controlled seating can beat
that burden. This local topology probe and source check do not establish broad
search saturation. No fabrication is informative for the demonstrated clashes.
