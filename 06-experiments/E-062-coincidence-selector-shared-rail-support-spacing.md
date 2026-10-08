---
status: complete
builds-on: [E-061]
---

# Coincidence rails require distributed moving support

Reject the end-supported 406.4-mm rail embodiment within the sections and
stiffness bounds tested. Retain the floating-beam coincidence principle only
with an explicit distributed moving support/frame or different transmission.
Do not count modularization as solved: grounded supports cannot hold a rail
that must translate 2.5 mm. No print, procurement or architecture selection.

Input main `242b2db`; reproduce with
`python3 tools/curated-experiment-checks/E-062/rail_bound.py`.
Evidence: linear elastic calculation with discrete point loads, not CAD,
contact simulation, calibrated material data or physical measurements.
This bounded investigation asks whether shared-line bending alone consumes
E-061's motion window. It stops at necessary support-spacing constraints;
complete geometry and timing remain unresolved.

## Model and assumptions

Simply supported rail, span n×5.08 mm, n equal shoe loads at cell centers,
rectangular section width 2 mm and vertical depth 4/8/12 mm. Elastic modulus
500/1500/3000 MPa and per-shoe follower preload 0/0.1 N are **assumed sensitivity
bounds**, not PLA priors, strength allowables or a qualified preload design.
Uniform low modulus represents shared material/orientation uncertainty; loads
are correlated by row selection. No random distributions or yield claims.
A single selected row loads all its 80 valves; an active column may load one
selected valve plus the follower preload of all its shoes. Dense loading is
therefore a real row case, not 6,400 simultaneously open valves.

E-061's 1-mm seat, 1.5-MPa closing differential and 1-N spring-plus-drag bound
imply 1.08905 N per endpoint. Add follower preload separately. For E-061's
s=2.5/g=1.6-mm witness allocate at most 0.1 mm to rail bending inside its
0.2-mm load-dependent lost motion; retain the other 0.1 mm for stem/contact
compliance. Equal downward endpoint deflections average, not add. This is an
investigation allocation, not a new product requirement. Support motion/error
must still fit the original ±0.1-mm endpoint bound; it is not free margin.

For x≤a, a point force P at a on span L gives
`v(x)=P(L−a)x[L²−(L−a)²−x²]/(6LEI)`; reflect coordinates for x>a.
Superpose shoe forces with `I=bh³/12`. Symmetric dense loads maximize deflection
at midspan. A central point load gives the worst placement for one selected
valve, plus the uniform discrete preload. Positive Green functions mean dense
activation bounds any subset under these same downward loads.

## Results and scaling

Enumerate 18 section/modulus/preload scenarios and integer spans of 1…80 cells.
Maximum spans meeting **bending alone** ≤0.1 mm range from 4 to 14 cells
(20.32…71.12 mm). These are necessary upper limits, not accepted support pitches.
At E=1500 MPa, b=2 mm, h=8 mm:

| Cells/span | Dense row, preload 0.1 N | One central valve plus preload |
|---|---:|---:|
| 8 | 0.06536 mm | 0.01739 mm |
| 10 | 0.15920 mm | 0.03663 mm |
| 12 | 0.32972 mm | 0.06788 mm |

The largest integer span is eight cells with preload and nine without it.
An eight-cell choice leaves only 0.03464 mm of the allocated rail allowance for
omitted bending-model effects. Shear flexibility, contact indentation, guide
play and supporting-frame deformation can remove this apparent window. Short
spans/deep sections are particularly sensitive to shear; no survivor is cleared
without it. Strength, creep, friction, dynamic overshoot and pressure reversal
are not modeled. Positive beam deflection results alone do not bound those.

For a full 80-cell span, even the stiffest/deepest tested section has a formal
linear result of 88.14 mm without preload. Such large values violate small-
deflection applicability: they are stiffness rejection diagnostics, **not**
credible physical sag predictions. Solving the same beam expression for 0.1-mm
sag with preload requires depths 118.47…215.28 mm at 2-mm width. These depths
also invalidate a slender-beam interpretation and are not proposed designs.
The calculation rejects only this end-supported slender-section embodiment;
trusses, bought metal sections, moving distributed bearings and other topologies
are not evaluated or forbidden by product dimensions.

At eight cells/span, 80 cells need ten spans. For 160 rails, ideal continuous
rails need 1,760 support stations (11 per rail); isolated segments instead need
3,200 end-support interfaces. These are conditional interface counts, not bought
part counts: a shared molded/printed frame may combine them but must transmit
motion and force without violating the budget. The fully selected row carries
95.124 N including the assumed preload. Across both axes, 12,800 shoes at
0.1 N impose 1,280 N total follower reaction even before selected-valve load;
its structural path and preload energy cannot disappear into the schematic.
This is distributed reaction, not a requirement for one actuator to lift 1,280 N.

## Decision and evidence limits

Stop full-width unsupported printed-rail layout. Continue hydraulic coincidence
only through a cartridge geometry that explicitly routes crossing rails and
moving support, retains E-061's sliding beam ends, supplies follower preload and
fits 1.1-mm maximum poppet travel. Its next discriminator is support-frame and
swept-contact geometry, followed by shear/contact compliance if geometry survives.
Reopen end support with a materially different section/material/transmission and
complete cost/packing evidence. A-013's grounded service-load path remains a
comparator; this calculation neither solves its channel cost nor ranks complete
machines. The A-014 mechanical-lock hybrid remains unexplored. No <30-s, leakage,
readback or reliability conclusion follows; these gates remain open.

Self-review: independent central-point-load identity, Maxwell reciprocity,
zero load/support displacement, inverse modulus scaling and convergence to the
uniform-load formula pass. At fixed span/total force, quadrature error falls
fourfold for each doubling 10→20→40→80 cells; final relative error <0.0002.
This checks algebra/summation, not discretization of actual contact geometry or
validation of beam theory. No independent review or hardware evidence claimed.
