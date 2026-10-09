---
status: complete
builds-on: [E-087, E-086, E-083]
---

# Series torsion improves capture but does not complete the rotary writer

**Reject the tested circular torsion-rod package under the declared force/error
boxes.** Shortening the blade and increasing its approach angle clears capture
through ±0.10-mm component-error corners. Adding bearings, axial shoulders,
a spring and angular return stops exposes force, recoil and parking conflicts.
There is no complete writer survivor or hardware qualification.

Input main `e76b180`. Reproduce:
`python3 tools/curated-experiment-checks/E-088/series_joint.py`.
Source imports E-087's convex polygon operations. Dimensions, errors, elastic
properties, loads, force/stress limits and timing are **explicit assumed
scenarios**, not sourced X1C priors or physical measurements. This is one joint
embodiment with parameter variations, not new architecture families. No contact
dynamics, FEA, calibrated material law, yield or lifetime distribution is claimed.

## Finite capture and joint

Change E-087's paddle to 2.7×0.6 mm in x–z, still 1.2 mm deep in y, pivot
(x,z)=(0.6,3) mm; set approach −45°, reset its reflection. Shortening clears
stationary dog guides below z=0. Raised programming remains 1.5 mm above the
working pose, with upward 180° bypass. Separate retained column supports and
dog endpoint retention remain boundary conditions, not supplied assemblies.

Enumerate 128 corners of seven independently bounded dimensions: pivot x/z,
full blade width, dog endpoint shift, full dog width, dog height and blade
length. Each has ±e mm error. Shared rail/print biases may realize coherent
corners across a bank; no averaging or probability is credited. Replay lowering,
ideal endpoint-limited rotation and fixed-angle lifting at 20/40/80 subdivisions.
Reset is the geometric reflection. This tests restrained-rotor contact geometry;
it does **not** grant the compliant joint a controlled withdrawal trajectory.

| Error e | Capture reserve | Terminal angle range | Blade/guide reserve | Independent programming-sector reserve |
|---|---:|---:|---:|---:|
| 0.05 mm | 0.31538 mm | −7.58078…+1.08218° | 0.18086 mm | 0.35654 mm |
| 0.10 mm | 0.05503 mm | −12.79903…+4.42822° | 0.07821 mm | 0.13747 mm |

The continuous sector bound is
`P cos(45°) − (0.6+e)/2 − hypot(2.7+e,(0.6+e)/2) − 2√2 e`.
The final term allows opposing pivot x/z errors. Raised programming clearance
is at least 0.47821 mm in the wider box. These bounds concern blades, not an
ungenerated drive or a recoiling output outside the commanded angular sector.
Corner results are bounded scenarios, not a statistical manufacturing yield.

Generate a coaxial torsion rod between rotor and input hubs, captured front/rear
shafts, annular bearing plates, axial collars, a rotor return cage, a slotted
input ring with connecting spoke, bearing posts and a frame bridge. All are
finite polygonal prisms, with actual annular holes. The reference rod is
0.8 mm diameter ×2.4 mm long; the entire package spans **9.6 mm in y**.
The rod supplies series compliance; the cage contacts either side of the input
slot at ±30° relative rotation, providing positive angular pullback. Collars
provide a positive common-lift load path through the bearing plates. This is
not a constant-torque clutch or a qualified actuator transmission.

Slot/cage solids are disjoint inside ±30°; attempting 31° gives **0.007328 mm³**
overlap, a stop witness. Shaft radial clearance, collar radial overlap and axial
bearing/collar face gaps are each nominally 0.3 mm. Allowing separate ±e radius and alignment
errors leaves radial fit/shoulder reserve `0.3−3e`: 0.15 mm at e=0.05 and zero
at e=0.10. Thus the broader blade-capture result does not qualify the bearings
or positive axial capture. The cage end also touches the rear collar nominally; thrust friction and
axial-error interference receive no clearance credit. Attachment strength,
bearing friction, wear, hole
shrinkage, warp, tilt and motor packaging remain unresolved.

## Force, model sensitivity and recoil

Use a circular elastic rod with `k=Gπd⁴/(32L)` N·mm/rad,
`T=k(φ−θ)`, energy `k(φ−θ)²/2` N·mm and maximum shear `16T/(πd³)` MPa.
The competing material scenario is isotropic `G=E/[2(1+0.35)]`, E in
[1000,3000] MPa. It is not a printed-PLA constitutive law. Diameter and length
also vary independently by ±e; material and process bias can be common-cause.

Contact changes branch at θ=0. For negative angles the dog contacts the side
at its top; its displacement derivative is
`j=(2+h−z) sec²θ +(0.6+dw) secθ tanθ/2` mm/rad.
For positive angles it contacts the lower tip, with
`j=(2.7+dl) cosθ −(0.6+dw) sinθ/2`.
Both one-sided derivatives are retained at zero. Frictionless virtual work gives
`T=F j`. Numerical derivatives independently check each smooth branch.

For every geometry corner choose the smallest common input angle that meets
required force: `φ=max(θ+Freq*j/kmin)`. Then evaluate all corners at kmax.
This is an optimistic zero-friction static screen, not a force-controller model.
Search d={0.6,0.8,1.0}, L={1.2,2.4,4.8,9.6} mm, e={0.05,0.10} mm and
Freq={0.1,0.3} N: **48 scenarios**. Require force ≤1 N, shear ≤10 or 20 MPa,
relative travel ≤30°, and minimum actual rod diameter ≥0.6 mm. None of these
limits is a sourced process allowable.

**All 48 exceed the 1-N force cap; 46 exceed even the 20-MPa shear cap.**
Eighteen exceed angular travel and sixteen violate the chosen minimum section.
No survivor exists. Large linear predictions beyond the stress limit mean the
elastic model crosses its allowed envelope; they are not actual post-yield loads.
Cases beyond 30° fail the hard-stop gate first; their continued elastic-rod
numbers are counterfactual, since shoulder contact bypasses series compliance.

| d / L / e, mm | Required force | Predicted peak | Shear | Stored energy |
|---|---:|---:|---:|---:|
| 0.8 / 2.4 / 0.05 | 0.1 N | 2.679 N | 41.99 MPa | 0.529 mJ |
| 0.8 / 2.4 / 0.05 | 0.3 N | 4.177 N | 65.48 MPa | 1.286 mJ |
| 0.8 / 2.4 / 0.10 | 0.1 N | 6.435 N | 81.43 MPa | 2.183 mJ |
| 0.8 / 9.6 / 0.05 | 0.1 N | 1.201 N | 18.83 MPa | 0.432 mJ |

The lowest peak, 1.021 N, uses a 0.6×9.6-mm rod whose minimum diameter is
0.55 mm, shear is 35.79 MPa and required twist is 54.23°. A softer/longer rod
reduces geometry-induced force spread while increasing travel and package depth.
The executable also reports the counterfactual with exactly known E=2000 MPa
and exact rod dimensions, retaining the contact-geometry errors; this changes
force rankings but supplies no calibration evidence: the 0.8×4.8-mm rod at
e=0.05 and Freq=0.1 drops from 1.688 to 0.639 N in that counterfactual. Narrowing uncertainty is
not a manufacturing result. The necessary inequality `Fcap≥(kmax/kmin)Freq`
already excludes many cases before contact-angle spread is added.

Positive return does not suppress recoil. Opposed outputs at +75/−75° are
allowed by the ±30° shoulders around the ±45° approach commands; their actual
blades intersect by **0.084850 mm²**. This is an admissible-pose collision, not
a prediction that every release reaches it. A sufficient all-phase lateral
separation bound reduces allowable return slack to **12.3126°** at e=0.05 or
**7.7234°** at e=0.10. Tighter stops compete with completion twist. Stored
energy has no measured damping or settling bound; a four-millisecond proof
slot cannot supply one. No dynamic integration or numerical time-step claim.

A stuck lowered blade intersects the next zero-state dog by **0.149871 mm²**.
A shaft/collar return path is not proof that every output followed it: inhibit
indexing until each blade is clear. For a declared 1-N normal-contact scenario,
80 coherent contacts require up to 12.0/35.97 N vertical extraction at assumed
friction 0.1/0.4, before bearing friction and inertia. This uses
`80*(|sinθ|+μ|cosθ|)` at the nominal terminal angle, not a jam-force guarantee.
Unknown adhesion, broken parts or a seized bearing retain the fault hold under
independently supported columns. No actual reader or qualified extraction drive
is supplied.

## Regional route and machine comparison

Adjacent same-height packages one pitch apart have **4.56 mm³** frame/frame
overlap. Elevating an idle head by **8.42179 mm** relative to its working pivot
bounds its lowest possible blade above the active head/frame even during the
active 1.5-mm lifted index, including the declared size/z errors and 0.1-mm gap.
This grants space above the assembly; it does not fit the surrounding machine.

High parking is safe only with a complete route: park at row-zero home; descend
there; index/write while neighboring banks stay high; return home at the ordinary
raised height; then rise to park. Raising at the final row would recreate the
same-height collision with the neighboring parked head. The changed return
itinerary therefore includes home return, not just a larger lift. Global scans
can run banks synchronously when their centers remain farther apart than the
package depth. The reference package fits that nominal separation through
40 banks (only 0.56 mm reserve there); 80 banks collide and receive no time credit.
Longer rods increase depth to `7.2+L` mm and require recomputation.

Use the same 43-mask workload and six-second allowance elsewhere as E-087.
Reference angular legs are 225°, 45°, 180°, at assumed 10,000 rad/s²;
linear moves use `2√(distance/a)`, with 4 ms proof per row. Include lower/raise,
indexes, high parking and final home return. These are **reference schedule
calculations**, not rigorous lower bounds or deadline passes: actual spring
loading, unloading, force feasibility, damping, velocity limits and drive mass
are absent. There is no hidden concurrency credit.

| Banks / a, m/s² | Full reference | Residual mean complete channel allowance, $250 elsewhere |
|---|---:|---:|
| 8 / 100 | 59.881 s | <$0.3811 |
| 16 / 100 | 32.658 s | <$0.1905 |
| 20 / 20 | 32.851 s | <$0.1524 |
| 20 / 100 | 27.212 s | <$0.1524 |
| 40 / 100 | 16.318 s | <$0.07622 |

The 20-bank fast reference leaves 2.788 s, or 16.208 ms per row transaction,
for every omitted joint/settling operation and retry beyond the assumed slots.
A five-row, five-column patch represented by 35 writes costs 5.631/4.391 s
of writer actions at a=20/100 in an 8- or 16-bank layout, including return to
home. Support operations are additional. A five-row patch spans banks in the
20/40-bank layouts; the source deliberately gives no single-bank patch time.
No physical non-target displacement bound exists.

Inverting this same reference schedule gives at most **19 masks at eight banks**
or **38 at sixteen banks** at a=100 m/s² under the strict 30-s target (14/30
at a=20). These are useful workload-reduction targets for a changed multilevel
state mechanism, not evidence that one exists. An eight-bank successor must
reduce 43 row-mask sweeps by at least 2.26× before retaining this motion budget;
it still needs a joint, support transfer, reader and affordable channel.

At B=20 count 1600 data axes, 20 lifts and 20 transports; 1600 spring/cage/slot
couplings and 3200 bearing sites, plus 6400 retained dogs and independently
retained output supports. Controllers, readers, power, motors and transmissions
must fit the complete channel allowance; none is priced at zero. No print-time,
assembly-time or wear advantage is demonstrated. E-083/E-085/E-086/E-087 retain
their documented failure envelopes; there is no accepted Pareto winner.
At least 275,200 dog and 275,200 blade-clearance observations remain per adverse
full map. Unknown false acceptance and common-cause faults preclude a reliability
number or independent repeated-read credit.

## Disposition and verification

Stop this series-rod package. Retain the shorter blade's capture result, finite
joint/stop and parking witnesses, corner-aware force model and complete return
accounting. Reopen only with a materially changed force-limiting/return mechanism
or calibrated material/fit envelope **and** a credible complete data channel
inside its allowance. Further nominal spring sweeps or a print of this failed
package would not resolve the campaign's addressing economics. No fabrication,
purchase or new agent is justified.

Self-review: E-087 clipping controls; independent side/tip derivatives and energy
finite difference; 128 error corners at three path resolutions; continuous blade
separation bounds; 24/48/96-facet package checks; positive stop, recoil, neighbor
and failed-withdrawal witnesses. Contact-intersection roundoff stays below
2×10⁻¹⁶ mm², guide reserve changes by <7×10⁻⁷ mm with refinement, and the finite
collision witnesses persist. This checks calculations and scoped geometry;
there is no independent review, dynamic verification or hardware validation.
