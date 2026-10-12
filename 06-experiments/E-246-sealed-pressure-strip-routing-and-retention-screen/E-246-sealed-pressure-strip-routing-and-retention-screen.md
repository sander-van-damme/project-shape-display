---
status: complete
builds-on: [E-245, E-236]
---

# Sealed pressure strips remove stiffness amplification, not individual grip risk

**Park the end-fed liquid-strip embodiment before membrane, seal or keeper detail.**
Pressure equalization is a real escape from E-245's stiffness-amplified preload:
the example row requires **400 N/face instead of 960 N/face**. It does not remove
12,800 independently necessary friction holds. At four banks the proposed machine
adds **400 resident +320 head sealed circuits**, 130.048 m of resident contact
strip, and unconstructed pressure retention/proof. An optimistic **29.244-s /
$441.40 pre-pressure-hardware** case is not a surviving machine. It leaves $58.60
for the pressure implementation and fails to establish the fast-flow regime,
individual contact or unchanged-neighbor motion. No universal hydraulic or cost
impossibility is claimed; no print is justified.

Input main `d786fff`. Reproduce:
`python3 tools/curated-experiment-checks/E-246/screen.py` (stdlib; imports E-236).
Evidence: **architecture hypotheses, deterministic calculations and model checks;
self-review**. No CAD, calibrated process prior, sourced material/price selection,
contact simulation or physical measurement. All numerical physical inputs below
are competing assumptions. E-245's unchanged ideal support logic is reused without
claiming another full-map replay.

## Construction and support obligations

Each smooth pin passes between two continuous backed membrane strips at a row
plane and another pair at a bank-column plane. Pair the two opposed faces into
one sealed circuit, with an external squeeze pouch, mechanically retained cam
and fill closure. Liquid redistributes as the walls encounter different pin
sizes. No working valve or powered pump is required **if each circuit has its own
retained displacement/force source**. Isolation walls replace valves; sharing one
open manifold across independently released rows/columns would lose independence.
Two-end feed uses branching passages to both ends, not two free pressure sources.

The shared moving head has 80 independently selected, similarly retained grip
circuits. Common cams supply squeezing work; command bits select the circuit cams.
These are unloaded commands, not actuators capable of supplying grip force directly.
The existing crossed support transaction remains: write/prove; close selected head
grips; open active row and selected column circuits; move the common datum; close
resident circuits; release head grips. Other rows retain row support, and unchanged
active-row pins retain column support. E-236's five strokes and causal retry remain.
The mapping is complete at function level; finite squeeze linkages, membranes,
branching, passages, return, readback and arrest are **unconstructed**.

A fixed-volume keeper does not establish fixed pressure over different total gaps.
A load-limited squeeze or compliant reservoir must reach pressure after contact
and retain reserve travel against creep. Count **720 force-accommodation/keeper
duties**, even if integrated into printed cam arrays. They are shared by zones,
not 6,400 private springs; their force, wear and calibration are still costs.
Source loss can retain sound sealed circuits mechanically. Leakage, a torn strip
or keeper failure can unload 80 row pins or 20 bank-column pins. During release of
the redundant path this can become an actual unsupported fault. Local downstream
lift arrest and proved reseating are still required. Repair means temporary
support, depressurization, accessible strip replacement, refill/bleed and proof;
not repair while terrain rests on the failed path. Stable wrong heights permit
one reread/reprogram; leaks, false proof and lost support require a stopped module.

## Force, volume and finite routing

Assume two A=25.6-mm² faces per hold, friction coefficient .15, total local static
weight L=1 N and holding multiplier 1.5. This is a concentrated load scenario,
not 6,400 simultaneous 1-N payloads or an established D&D requirement.

`p=1.5 L/(2 mu A)=.1953125 MPa`; each 80-pin row face reacts 400 N.

This grants full area, negligible membrane-tension loss and adequate backing.
Moving grip pressure grows to .3546 MPa for 8-m/s² ascent/braking before drag.
Pressure/area must scale if friction falls, effective contact shrinks or load grows.

Per-face gap error ±E=.35 mm plus .2-mm release clearance requires up to
`d=2E+.2=.9 mm` displacement. A coherent all-large-gap row consumes
`V=2 n A d=3.6864 mL`; mixed gaps consume less. Correlation therefore changes
both required reservoir travel and pressure, not merely an IID defect rate.
At reservoir area 40 mm²/site, a row needs **3,200 mm², 1.152-mm travel and
625-N static squeeze reaction**. Reducing to 5 mm²/site lowers reaction to
78.125 N but increases travel to 9.216 mm. Increasing area is not free force.
A row-pitch reservoir at 3,200 mm² would extend 630 mm perpendicular to its
5.08-mm allocation. External staggered reservoirs or more decks are necessary;
there is no requirement that they fit inside one surface cell.

Total reservoir projected area at 40 mm²/site is **.5248 m²**, about 3.18 times
the display footprint, before walls, links and service gaps. Total worst resident
volume movement is .590 L if both whole resident systems are cycled, not a normal
per-pulse duty. A fully selected B4 pulse cycles the column system plus four rows:
.310 L. Pressure times this free-gap volume is **not** a work lower bound: pressure
can be low during free expansion. Actual pressure-volume loops and recovery/losses
must size the drive; E-245's bulk-pad elastic work cannot be copied here.

The retained section uses E-245's .54-mm-per-face allocation. Grant a .1-mm wall
and a constant **.44-mm fluid passage** behind an 8-mm-high contact wall. Folding,
seams, backing and membrane return may require more room; the .9-mm excursion
into variable pin clearance is not finite CAD. The film is a purchased-material
hypothesis, not reliable .1-mm printed PLA. Contact strips span 406 mm and need
modular backers on the X1C; their joints can cause coherent misalignment/leaks.

## Flow and complete online timing

For a rigid wide slit, integrating `mu u''=dp/dx` through gap g gives
`Q=w g³ gradient/(12 mu)`. Uniform distributed expansion along length l gives
`DeltaP=6 mu l Vface/(w g³ t)`. Feeding both ends quarters this continuum time.
This is a **quasisteady fixed-channel relaxation**, not a validated deforming-hose
model or a universal lower bound. Side-wall corrections, fittings, entrance loss,
inertia, bubbles, membrane elasticity and passage collapse are omitted.
[Chun et al., Physical Review Fluids 9, 043302](https://arxiv.org/abs/2401.05513)
experimentally study how conduit compliance changes flow/pressure relations;
that methodological warning supplies no material or rate prior for this machine.

At viscosity .001 Pa s, .9-mm expansion and allowed longitudinal pressure drop
.25p, one-end row times at g=.14/.24/.34/.44 mm are
**4.193/.832/.293/.135 s**. These gaps/viscosities are scenarios, not process
measurements. A common constriction is consequential because time scales as g^-3.
Use .001/.01/.1 Pa s; ±E=.15/.35/.70 mm; g=.14/.24/.44; one/two feeds; fill
pressure-drop ratios beta=.25/1/4; reservoir area/site=5/20/40/80 mm².
Drawback grants at most .08-MPa suction differential and ignores adhesion and
cavitation. It cannot inherit arbitrarily high positive fill overpressure.

Each of four support stages costs max(reservoir rest-to-rest travel time, flow
time)+3-ms proof. Force-rated motion is granted at .2 m/s and 8 m/s². All pair,
row and selected-column motions overlap within their stage. Charge every physical
write (2-mm stroke+3-ms proof), five lift strokes, row feed, 2-s setup/registration/
final settling, one full row retry and .185-s empty reset/read. No offline pattern
preparation or unpriced writing overlap. Nonadjacent regional seeks add actual
travel; even one changed cell retains the whole-row handoff.

| Assumed liquid feed, E=.35, g=.44 | First bank count under 30 s | Time | Inherited allocation, before pressure hardware |
|---|---:|---:|---:|
| One end, beta=.25, area/site40 | 8 | 28.576 s | $687.80 |
| Both ends, beta=.25, area/site40 | 5 | 25.750 s | $503.00 |
| Both ends, beta=1, area/site40 | 4 | 29.244 s | $441.40 |
| Both ends, beta=1, area/site5 | 8 | 26.716 s | $687.80 |
| Both ends, beta=1, area/site40, viscosity .01 | 8 | 29.697 s | $687.80 |

Only **18/648** B4 parameter combinations meet timing in this relaxed model;
these are not manufactured yields. In the favorable 24-ms two-end case, assumed
liquid density 1,000 kg/m³ gives **10.91-m/s mean inlet velocity and slit Reynolds
number 9,600**. A prescribed triangular flow pulse additionally requires about
**.185 MPa peak acceleration pressure** from a distributed inertance calculation,
before viscous losses. Thus a creeping-flow result cannot establish that rate.
Larger external passages could avoid this, but each separated circuit needs its
route; uniform pressure is not instantaneous equilibration.

## Replication, economics and decision

| Duty | Cell / row | B4 bank or head | Board |
|---|---|---|---|
| Column / ordinary guides | 1 /2; 80 /160 per row | 1,600 /3,200 | 6,400 /12,800 |
| Resident holds / contact faces | 2 /4; 160 /320 per row | 3,200 /6,400 | 12,800 /25,600 |
| Resident sealed circuits / squeeze-keeper duties | 1 shared row, crossed segments | 20 row +80 column | 400 |
| Moving selected circuit / grip / command | reused across rows | 80 each/head | 320 each |
| Fluid closures, ideal tube-route minimum | shared by circuit | 2 per circuit | 1,440 before branches/fill ports |
| Lift/arrest/feed/read systems | shared | one set/head | four sets |

A molded/welded manifold changes terminal counts but adds continuous seams and
junctions; the table is not a constructed plumbing bill. Resident face-strip length
alone is **130.048 m**, independent of banking for this two-axis topology; head
strips and reservoir connections add length. Filling/sealing/proving 720 circuits
at assumed 30–90 s each adds **6–18 h**, before 25,600 contact-area inspections.
E-245's 7.602-L smooth-stem stock, 156–469-h assumed extrusion and 8.9–26.7-h column
insertion remain. Film cutting/welding, backing print volume/time, fixture rejects,
leak scrap, mounting, assembly and replacement are unqualified, not zero.

Inherited B4 ledger is $195 common+$20/bank+$.52×320 commands=$441.40. The $58.60
remaining is **8.14 cents/circuit** if consumed entirely by pressure hardware, or
45.1 cents/metre of resident face strip with all other extras free. Neither is a
supplier quote or market impossibility. No plausible complete bill, rated squeeze
transmission, fill fixture or individual proof system has been constructed within
that residual. A cost-only $3 miss at B5 is not the reason to stop.

Pressure **and total volume** can miss a blind contact: one bridged membrane
receives no contact displacement, another expands into extra clearance, preserving
both aggregate volume and pressure. The source checks this counterexample. Local
normal-force equalization also does not bound vertical shear motion: equal
kt=10-N/mm supports sharing L=1 N still shift **.05 mm** when one is removed.
All 79 unchanged pins in a one-cell row update undergo that load transfer.
No physical disturbance limit or support verification has been demonstrated.

**Comparators and disposition:** E-236's positive combs retain 44,800 fixed shelves
but avoid 12,800 friction retention duties and all sealed circuits. Their B5
26.681-s/$503 lean case still owes finite routing, affordable writing and support
proof; it is not selected. Sealed gas strips may reduce liquid-flow resistance
but remove 65.9% of initial gas volume just to reach the example pressure
(isothermal .101-MPa initial absolute), before extra contact volume; they retain
the contact, reservoir, leak and proof duties. Distributed local squeeze avoids
longitudinal flow by adding moving backers and displacement distribution along
all strips; it is not evidence that the screened end-fed machine works.

Stop smooth friction-support detail. Reopen only with a concrete broad-margin,
serviceable pressure construction **and individual support assurance**, not a
larger passage alone. Follow the independent review's architecture-only limit and
positive-support comparator; the review cutoff precedes E-245, whose unchanged-row
counterexample remains controlling. Next return to shared **positive support and
persistent row programming**: first reconstruct E-232/E-238/E-243 and test whether
a changed transaction can eliminate repeated rewrites without adding private
loaded memories. Start with program/support state graphs and a full ledger; do
not reopen coil, membrane, pawl or guide tuning by default.

Checks: independently expanded schedule; discrete 80-sink network gives 1.0125×
the optimistic continuum pressure; two-end, viscosity and gap-cubic scaling;
pressure/volume blind-contact witness; shear-transfer witness. These are model
consistency checks, not independent validation or physical qualification.
