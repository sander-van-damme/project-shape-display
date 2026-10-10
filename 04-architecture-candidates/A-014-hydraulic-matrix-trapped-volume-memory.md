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
window. Next investigate changed three-dimensional ground/axis routing with
finite return contacts. Valve synthesis remains dependent on a selector
survivor; neither the ramp scalar bound nor rail-only clearance is a machine.
