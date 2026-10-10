---
status: complete
builds-on: [E-127, A-025]
---

# Docking phase freedom does not remove the weakest load-transfer joint

**Reject the tested 20-N single-face friction dock under the low-friction load
scenario; independently phasing a sleeve merely moves the same friction cut
upstream. Matched-index dogs remove that cut, but no two-site complete machine
is admitted.** Outward-facing pinions give a new locally clear shaft route;
repeating it at the same depth causes actual core interference. A released
spring brake has a finite unsupported interval. Continuous drag closes that
interval conditionally, at an explicit force/heat cost. Stop before schedule,
BOM or fabrication; this is a contact/geometry counterexample result.

Input main `3c26e91`. Run:

```
python3 tools/curated-experiment-checks/E-128/docking_arrest.py
```

Python 3/NumPy; imports E-127's retained polygon/gear source. Output is disposable
JSON. Evidence: generated rigid sections, contact-state replay, analytical force
bounds and an isolated spring-pad calculation. No assembly CAD, measured friction,
process prior, dynamic arrest qualification or reliability estimate. Self-review
only. Positive indexed contacts inherit E-127's nominal geometry and its failures;
no tolerance improvement is claimed.

## Distinct joint and load-path combinations

| Route | Acquisition and torque path while ground bolt is open | Extra physical obligations | Disposition |
|---|---|---|---|
| Continuous face | rack/pinion → clamped annular face → head gear → shared translating drive rack → frame brake | Axial clamp spring, thrust reaction, release actuator; surface traction | Finite pressure-independent slip counterexample below |
| Independent phase sleeve | rack/pinion → locally phased positive nose → freely rotating sleeve → friction clutch → shared rack/brake | Sleeve bearing, phase actuator/readback, proximal clutch and clamp; cannot leave sleeve free during takeover | Same series torque cut; relocation alone is stopped, not credited as a new solution |
| Matched indexed | rack/pinion → twelve dogs registered to ground slots → head gear → shared rack/brake | Axial keeper/return, independently retractable head, ground-bolt release; stop-at-index sequencing | Nominal static contact chain only; fit errors and common arrest unresolved |
| Indexed plus permanent drag | same dogs; opposing preloaded pads always touch shared rack | Two pad springs/reactions, motor must overcome drag; wear/thermal service | Removes brake closure gap in model, with force/energy penalty; no full assembly admission |

A direct independently powered keyed head is the control: one phasing motor and
arrest per active head eliminates the proximal phase clutch, but does not establish
cost or routing. Positive nose plus an unbuilt ideal sleeve lock is not a survivor.
These are functional recombinations, not claims of new clutch physics. Earlier
M-008 already describes common-shaft selectable clutches. Novel discrimination
here is the phase-acquisition/arrest series cut and the outward routing failure.

## Finite two-height access and selective transfer

Keep E-127's 18-tooth module-.4 pinion, 3.6-mm pitch radius, 56-mm finite rack,
40-mm motion and actual ground-slot/dog polygons. Top centers are x=0 and 5.08;
pinion axes move **outward** to x=−3.6 and 8.68, with the right mesh mirrored.
Both shafts point along y instead of crossing the neighbor's rack lane. This
changes the route, not the dimensions of the rejected straight-through bank.
Racks occupy y=[0,1.2]; their backing x intervals are [.5,1.3] and [3.78,4.58].
Radius-.8 shafts occupy y=[−1.2,7.2], z=0. Exact circle/backing clearance is
**3.30 mm** at either height endpoint and throughout travel: every rack spans
z=0 for every h in [0,40]. Actual generated gear polygons are separated by
**4.35877 mm** in x. The 20.28-mm internal width exceeds the two tops' 10.16 mm;
this is permissible locally, not evidence of tileability.

Inherited axial stack: collar y=[1.4,2.6], bearing [2.8,3.8], docking disk
[4,5.2]. The proposed head gears occupy [6,7.2], sliding outward 1.5 mm to
[7.5,8.7] to disengage the .8-mm dogs. A shared toothed bar at y=[6,9.2],
z=[3.2,4.9] remains engaged with either axial head position; no telescoping
spline is silently added. A 70-mm finite toothed length covers the two head axes
and ±20-mm command travel with gear-radius end allowances. This is a routed
access construction; frame housings, head bearings, rack-drive mesh under error,
actuator bodies and wiring are not packed/qualified. The scalar length allowance
is not a tooth-contact validation. The failure conclusions do not require these
missing elements to succeed. Mirrored site meshes require opposite command
signs for equal height changes; a shared rack cannot lift both together as drawn.

Replay selected height **9.21185 mm** and unselected **28.06141 mm**, then lift
the selected site one 1.88496-mm index. Both start seated on ground-slot flanks.
Selected dock enters → head takes its loaded flank → lift .21293 mm to unload
the bolt → retract bolt → rotate through half-index → insert target bolt → lower
onto ground flank → unload and withdraw head. The other head stays withdrawn and
its ground bolt loaded throughout. Contact membership comes from the actual
polygons, including E-127's load-seat offset, not an inserted=loaded boolean.
The script distinguishes grounded support, indexed support and friction capacity.
Unselected height is kinematically constant; vibration/elastic disturbance is
not assessed. This is selective one-site motion in a two-height assembly, not a
parallel scheduling demonstration.

Ground-bolt return needs a spring and its release needs an actuator per addressed
head/site interface. Model a 2-N return-force scenario (not a designed spring),
plus guide friction. A properly successful takeover unloads its contact first.
If the face slips, that unloading cannot be asserted: even a straight slot needs
at least `mu_bolt F R/3.4` radial pull, **1.04 N** at F=3.27 N, mu_bolt=.3,
before the return force and guide losses. Pulling harder does not create support.
The matched head also needs axial retention during power loss: a normally engaged
spring with a thrust stop is proposed, not a qualified keeper. A released inactive
head may spring into a misphased socket on outage; its ground bolt must remain
engaged. Recovery must rephase with that bolt carrying load. No omission earns
support credit and no full survivor follows from the nominal trace.

## Pressure-independent friction counterexample

The generated single contact face is an annulus ri=1.6, ro=3.4 mm. For uniform
pressure its mean torque arm is
`2(ro³−ri³)/(3(ro²−ri²)) = 2.608 mm`; uniform wear gives 2.5 mm. Integrating
16/64/256/1024 radial strips converges to the former, within 0.000001 mm at the
finest setting. More decisively, **any nonnegative pressure distribution**,
including concentrated edge contact from misalignment, obeys `T ≤ mu N ro`.
This independently checks the reduced model without assuming full face contact.

At F=3.27 N, demand is **11.772 N·mm**. With N=20 N and mu=.1, uniform-pressure
capacity is **5.216 N·mm** and even all pressure at the outer edge supplies only
**6.8 N·mm**. The dock slips despite an arbitrarily strong grounded upstream
brake. Four replay states lose static support: unloading lift, bolt out,
half-index motion, and target bolt inserted but not seated. The independent
sleeve-plus-friction-clutch variant inherits this result for the same radius and
preload. It does not inherit it if it supplies a materially different positive
proximal lock; that lock then needs finite construction.

At mu=.3 and N=20 N the face capacity is 15.648 N·mm: the nominal 3.27-N case
passes this necessary static condition. Thus this is **not** rejection of all
friction coupling. At mu=.1, supporting 3.27 N needs at least **34.6235 N** axial
force even at the outer edge, or **45.1380 N** under uniform pressure. For 10 N,
these rise to 105.882/138.037 N per selected interface. Thrust bearings, clamp
springs, frame bending, release loads and synchronous bank reactions must carry
those forces; a stronger brake cannot substitute for them. Two friction faces,
a cone, greater radius or local positive capture changes the mechanism and has
its own release/packing obligations.

The executable crosses mu={.05,.1,.2,.3}, N={10,20,40} N and F={1,3.27,10} N:
36 explicit scenarios, no probabilities. Same low mu on both heads represents
common surface/material contamination; one low head is a local defect. Shared
preload loss is another bank fault. Pressure shape is model uncertainty, not a
random cell variable. X1C friction, creep, roughness, warp and spring relaxation
are **uncalibrated**; none of these bounds is a claimed manufacturing tolerance.
E-127's common ±.05-mm dog-fit failure still applies to matched indexing.

## A real passive-brake contact changes the comparison

Use a linear brake on the shared drive rack; each grounded pad has a 4×10-mm
contact face. At normal N=100 N **per face**, two opposing pads and mu=.1 supply
20 N tangential capacity. At the 3.6-mm head pitch radius this statically supports
two 10-N site loads only at equality, with no margin. A one-face fault halves it;
mu=.05 halves it. The frame must react 100 N from each pad. Pad spring, guide,
release coil/cam and adjustment remain required parts, not implicit free arrest.

For a released brake, model a single 20-g pressure plate traversing a .2-mm gap
under stiffness 2 N/mm and initial force 100.4 N, leaving the same 100 N
at contact as the drag case. Solve
`m x'' = F0 − kx`, x(0)=x'(0)=0. First contact is
`acos(1−kg/F0)/sqrt(k/m)` = **.28237 ms**. Time steps .1/.01/.001 ms converge
to that analytical value within .002 ms. This is an intentionally favorable
undamped, no-coil-delay calculation; full holding force appearing instantaneously
at first contact is also favorable. Before then the finite separated faces exert
**zero** brake friction. Gaps .1/.2/.4 mm give .19983/.28237/.39867 ms.
These are bounded design examples, not predictions of a purchased brake.

At downward speed 300 mm/s, the .2-mm case moves **.08471 mm** before contact
if velocity remains constant, or .08510 mm in a gravity-only point-mass example.
Neither value is a final stopping distance: brake force rise, drivetrain inertia,
external force and bounce are missing. At rest an overhauling load likewise has
no brake reaction during closure; its motion depends on reflected inertia.
The opened ground bolt cannot be credited as an instantaneous fallback.
A spring-applied brake is therefore not *continuous support* merely because it
is normally closed; bounded stopping may still be acceptable after a separately
defined displacement/impact criterion and a complete dynamic model.

For context only, [Miki Pulley's manufacturer description](https://www.mikipulley.co.jp/en/electromagnetic-clutches-brakes/offbrakes/braking)
(accessed 2026-10-10) distinguishes spring-applied emergency braking from free
rotation while energized. Its listed compact braking range is .12–2 N·m with
37–75-mm outer diameters. Those devices are references, not a selected BOM or
sources for the tiny pad's spring/friction values. Manufacturer ratings do not
transfer to a printed brake.

Leaving both pads continuously applied avoids the closure gap, provided dynamic
friction exceeds overhauling force and the drive remains connected. The 20-N
example dissipates **6 W at 300 mm/s**, whether moving one or both sites. More
generally permanently opposing 160 simultaneous 10-N downward loads at that speed
requires at least **480 W** drag dissipation at equality, before any force margin.
This is an instantaneous workload bound, not a whole-map energy or cooling design;
it falls with selected load/speed. Permanent drag has no powered release, but
still has two preload elements, wear adjustment and ground reaction. It exchanges
closure uncertainty for friction/heat/drive-force uncertainty, not free safety.

## Disposition and reopening

Naively repeat the outward pair at x+10.16 mm: adjacent pinion centers are only
**2.12 mm** apart. Their root disks (radius 3.1 mm, solid beneath teeth) overlap
by **4.08 mm**. This is actual material interference at equal z/y, independent
of tooth phase and tolerance. It rejects same-tier replication, not staggered
or expanded-depth access. It is distinct from E-127's shaft/backing collision.

At 6,400 cells, the stationary inventory still includes 6,400 racks, pinions,
ground stops/return elements, docking faces and at least 12,800 bearing surfaces.
Active heads add sliding rotary bearings, axial retention/release and ground-bolt
actuation. The independent sleeve adds one bearing, phase channel and proximal
clutch per head; the matched head avoids that clutch but retains discrete-phase
fit and command restrictions. A shared brake adds a correlated failure boundary;
a local friction slip can defeat its protection of one cell. No purchased-cost,
<30-s completion, repairability or production-reliability acceptance is inferred.

Stop the compact single-face/20-N route under the stated adverse scenario and
stop the free-sleeve relabeling. Keep matched positive transfer and independently
powered heads as comparisons, **not selected architectures**. No complete schedule,
BOM or print request. Reopen friction docking only with a changed positive capture
or explicit clamp/reaction geometry meeting low-traction bounds. Reopen matched
bank work only with routable replication and an arrest path whose gaps/dynamics
are explicit. A useful new axis is a load-energized no-back joint with input-only
release: it could remove permanent drag, but must demonstrate finite contacts in
both directions rather than rename an ideal brake. Explore that topology before
optimizing today's annulus, spring delay or gear sizes.

Verification/recovery remains a gate: drive angle does not detect local face slip;
bolt insertion does not prove ground load transfer. Actual height and supported
handover must be checked independently. Retain the dock on disagreement, keep
other bolts closed and stop locally. Reader false acceptance, common registration
and physical fallback are unresolved; no simulated board yield is reported.
