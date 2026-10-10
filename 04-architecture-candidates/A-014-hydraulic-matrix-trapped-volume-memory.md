---
status: candidate
---

# Hydraulic matrix with trapped-volume height memory

Explore a distinct operating principle: fluid volume stores continuous height;
a shared reversible pressure/return source supplies energy; two series gates
per cell implement row/column coincidence. Each row control operates its 80
upstream gates, each column control its 80 downstream gates. Closing gates
traps fluid below a guided piston. A downward bias enables lowering; return
pressure, cavitation avoidance and miniature support need explicit design.
A scanned height reader closes the selected intersection at its target.
Recovery isolates a leaking cartridge and repositions after readback.

This is an unbuilt architecture hypothesis, not a valve or seal design.
Descriptors: matrix addressing; analog volume memory; hydraulic shared energy;
pressure-supported piston; 6,400 sliding seals, 12,800 shutoff seats and
intermediate cavities; 160 shared gate drives plus pump, plumbing and reader.
No head-to-tail acquisition is required, but precision fluid interfaces replace
pawls. Regional isolation must hold against pressure history and leakage.
Printed manifolds need modular construction, sealing and accessible cartridges.
Stage-02 PLA/X1C is not qualified for these seals or pressure containment.

Complete-system gates: two controlled flow directions, supported lowering,
pressure regulation, relief, leak containment, fill/bleed, height feedback,
false-accept detection, service isolation and sustained arbitrary-map timing.
No cost advantage is established. At $250 shared reserve, all bought cell
hardware together must be below $0.0390625/cell under the $500 ceiling;
160 drives, pump and reader must actually fit that reserve. Printing seals
or gates moves burden to manufacturing and wear, not to zero burden.

Do not pursue detailed two-series-gate geometry yet. Compressible intermediate
volume means logical AND does not guarantee motion isolation: opening the
chamber-side gate can displace a half-selected piston while the upstream gate
is closed. Reopen that embodiment with bounded intermediate compliance and
pressure history, or a materially changed chamber-side coincidence valve that
never opens on a half-select. A normally closed chamber valve opened only by
two mechanical inputs could escape; it requires a real force/isolation/reset
mechanism and still repeats 6,400 qualified valves. Positive mechanical locks
could remove dwell compliance/leakage but add release and support-transfer work.
The floating-beam chamber-side coincidence embodiment now has a conditional
kinematic window (E-061); swept packaging, shared-rail force/deflection and
bidirectional closure remain unresolved. The lock hybrid remains unexplored.
Neither is accepted hardware. No print or purchase.

E-062 rejects end-supported full-width rails for the tested 2-mm-wide,
4…12-mm-deep bounded-stiffness sections. Distributed moving support is required:
the illustrative 2×8-mm rail at 1500 MPa permits at most eight cells/span with
0.1-N/shoe preload and a 0.1-mm bending allocation, before shear/contact/frame
compliance. Support stations must translate with the rails; fixed grounding is
not a solution. Continue only with explicit support and crossed-rail geometry;
no cartridge fit or stiffness qualification follows from this necessary bound.

E-101 rejects two finite moving-support embodiments: straight upper-tier ground
posts collide with captured lower ramp forks, while coplanar positive-reset
radial cam webs collide with neighboring shafts even if disks are staggered.
Captured-ramp clearance also changes half-select isolation and maximum stem
travel; positive return alone does not guarantee the original coincidence
window. E-102 escapes the coplanar-shaft collision using alternating shaft
heights and four axial cam phases; two phases still collide. Selected finite
bearing/follower/ground-neck envelopes clear, but slender follower forks fail
stability/axial-loss bounds and the original beam risers intersect 3-mm shafts.
Upper ground posts are restraint-sensitive under the correct sparse column
load. E-103's narrower guide portal clears its tested neck crossings, but the
retained sphere-ended beam intersects the solid shoe floor in nominal
half-selection. Capsule floors escape square-corner packing but retain that
actual rod/floor collision. Cam plus shoe return gaps also consume isolation.
Park this assembled route before shaft-phase/valve refinement; reopening needs
changed contact/return and a complete load path. Neither a thicker follower nor
another radius sweep establishes a machine. About 1,600 cams/3,200 bearing
interfaces precede boundaries, valves and readback.

The next distinct addressing comparison is a moving row bank of **80 reusable
short-stroke chamber-valve heads**. Spatial row registration replaces row-rail
coincidence; independent head open/close states select columns. A common
reversible hydraulic supply provides the 40-mm positioning work. Closed
fixed-base chamber valves retain volume; each target closes and is read back
before heads retract and the bank indexes. This removes floating beams and
long support shafts but retains 6,400 chamber valves, piston seals, fluid
plumbing and unqualified volume memory. It is a hypothesis, not completed head
geometry or an accepted timing/cost survivor. Count head acquisition, independent closure,
reader false acceptance, indexing, controlled lowering and recovery. Unlike
A-013, each channel need not individually drive the column through 40 mm;
short valve stroke alone does not establish cheap actuators.

E-104's executable schedule screen rejects the nominal 3-mm/8-L/min/400-mm/s
route for arbitrary maps: all-up takes 25.127 s and checkerboard 28.356 s,
but 79 up / 1 down in every row takes **33.758 s**, including bounded overhead
and one detected row retry. Only the 2-mm/8-L/min/400-mm/s case survives all
81 direction splits in the 27-case ideal grid; a common 20% speed reduction
makes it 32.266 s. A 3-mm/12-L/min control escapes nominally at 29.177 s.
These are unqualified flow/speed/overhead allocations, not pump or head ratings.
Sparse mixed changes spanning all rows retain the two-phase timing penalty.

Retain a conditional finite-head investigation, not architecture acceptance.
Resolve acquisition/withdrawal, port flow, unloaded lowering and closure timing
before elaborating seals: a diagnostic .2-mm height/.05-mm read-error budget at
400 mm/s permits only .375 ms residual closure delay. Slower approach or
predictive control must be modeled explicitly. No stage-02 height tolerance is
created. At assumed $250 shared reserve, $2 complete heads leave just
$.0140625/cell for **all** purchases; head and cell maxima cannot both be spent.
E-104 retains the inverse budgets, shared/local sensitivity, local alignments,
pressure/power and recovery limits. No priced BOM, print, purchase, seal or
hardware acceptance follows.

E-105 generates a finite dry-stem valve/interface subset. A short tail makes the
head enter its gland; a longer tail and three actuator lanes clear the tested
subset, with .339…2.750-mm input strokes. Return springs, grounded guides and
actual actuators remain absent. This route adds 6,400 stem seals. Port flow can
support high speed conditionally, but unloaded lowering and fine-gap metering
are sensitive to net bias/drag, pressure and fluid model. A specified two-speed
controller takes 30.032 s at the illustrative .2-mm accuracy/2-ms response,
versus 28.808 s at .5 mm; neither accuracy is a product requirement. This rejects
that fine-control allocation, not the family. Compare binary full-open heads
with charged shared coarse/fine pressure phases before refining analog lift or
claiming a complete finite head. No seal, cost or hardware pass follows.
