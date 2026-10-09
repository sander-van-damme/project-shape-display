---
status: complete
builds-on: [E-075, E-061]
---

# Positive shutters exchange pulse-history sensitivity for reset and fanout gates

Retain a **row-local, unloaded-address-change** shutter comparator for LAB-193;
reject a single rigid full-board ram as its drive implementation. Positive
blocking can isolate a half-selected command without a magnetic threshold,
but a blocked pin arrests a rigid ram shared with selected pins. Independent
lost motion/compliance or row-local energy routing is necessary. This is a
bounded rectangular aperture and discrete-transition calculation, not a complete
cam selector, contact simulation, printable CAD or physical evidence.

Input main `d81222c`. Reproduce:
`python3 tools/curated-experiment-checks/E-076/shutter_gate.py`.
Standard library, deterministic exhaustive enumeration, no seed. Full survivor
population and failure witnesses are emitted; generated output is not retained.

## Mechanism and finite section

A vertical square command pin passes through two orthogonal, vertically
separated shutter strips. Each has periodic square apertures at p=5.08 mm.
A row strip translates along x and a column strip along y; their separate z
layers prevent strip crossings. Both apertures must align to pass the pin.
A closed aperture leaves a horizontal frame-supported blocking face; unlike
E-075, repeated subthreshold pulses cannot traverse an ideal rigid obstruction.
The pin sets a separate bistable routing dog, then retracts completely before
shutters move. The dog subsequently routes a powered cam to a collet or unloaded
pawl. Dog retention, cam isolation and its selective reverse/reset interface
remain unresolved; aperture coincidence alone does not supply those functions.

Generate pin width w=0.6/0.8/1.0, aperture width a=1.2/1.6/2.0 and shutter
stroke d=1/1.5/2 mm (27 parameter choices, one topology). Three uncertainty
boxes e=0.05/0.10/0.20 mm independently bound pin/aperture width errors and
relative registration. These are explicit epistemic bounds, not measured FDM
priors; coherent strip/batch bias is included by taking worst corners rather
than averaging cells. Stroke error is included in relative registration.

Exact interval margins in the translating direction are:

- Open clearance: `(a-w)/2-2e`.
- Closed obstruction overlap: `d+(w-a)/2-2e`.
- Separation from the adjacent periodic aperture: `p-d-(a+w)/2-2e`.

Require all strictly positive. Enumeration retains 24/21/10 choices for the
three boxes. These are geometric scenario counts, not yields. A witness
w=0.8, a=1.6, d=1.5, e=0.1 mm gives margins **0.20/0.90/2.18 mm**.
Independent rectangle-containment checks enumerate all width/registration
corners. Translation between endpoints is monotone; the nearest neighboring
aperture is closest at maximum stroke. With one shutter closed, the other can
sweep without opening a through-path in the ideal rigid model.

This checks finite lateral aperture sections, not full swept solids: strip
width, guide rails, z thickness, bending, pin tilt, aperture edge chamfers,
frame support, wear and dynamic impact remain unsolved. A 0.90-mm obstruction
is not a strength rating. No claim of 5.08-mm complete cartridge packing follows.
Separate z levels can allow a pin to enter the first aperture before stopping
at the second; both must be cleared on withdrawal before either closes.

## Transition enumeration and stored-energy failure

Start loaded at (row0,col0), request (row1,col1). Enumerate all 720 permutations
of unload, old-row-off, old-col-off, new-row-on, new-col-on, load. States contain
sets of enabled rows/columns and a loaded drive bit. A loaded cross intersection
outside the old/new pair is unintended activation. Closing either shutter while
a selected pin occupies it is a collision. Exactly 360 orders end loaded;
234 contain unintended activation and 288 contain closure collision (overlap,
not additive counts). Fifty avoid both in this binary-state abstraction.

Only **24** of those 50 unload first and load last, allowing all four address
changes in between. The other 26 energize before the address change is complete;
they pass binary checks but may release stored energy during a shutter sweep.
Do not accept them without a contact/energy model. The retained sequence is:
retract pins below both layers and verify → change addresses → verify shutter
positions → drive pins → latch/read dog → retract/verify → next address.
"Unload" means positive withdrawal, not merely removing current or cam force.
A jammed or spring-loaded pin invalidates the sequence. A common mechanical
withdrawal interlock is preferable to assuming perfect readback, but has not
been designed here. False acceptance and stuck-open shutters remain unbounded.

Example failed order: unload, old-row-off, new-row-on, new-col-on, load,
old-col-off. At load, both old and new columns are selected on the new row;
closing the old column then collides with its inserted pin. This is a concrete
stale-command/release failure, not pulse-amplitude leakage.

## Full-board implication and decision

A compliant follower per site allows a shared platen to travel while blocked
pins remain stopped, but adds repeated springs/lost-motion contacts. With one
80-cell row selected, at least 6,320 followers are blocked. At hypothetical
blocked preload 0.01/0.05/0.10 N each, shared reaction is **63.2/316/632 N**
before selected work, friction and acceleration. All-zero masks block 6,400.
A row-local drive limits blocked followers to at most 80, giving
**0.8/4/8 N** at those same assumptions. These are force sums, not motor ratings;
a supported camshaft can distribute forces, but cannot delete energy or contacts.
A rigid shared ram without lost motion cannot complete selected strokes at all.

A dual command-array implementation repeats 12,800 pins/dogs, 25,600 aperture
sites and nominally 320 row/column shutter lines, plus drive routing and readback.
Temporal reuse might reduce these counts only after retention/reset is designed.
The raw 30-s budget for one 80-row scan is <375 ms/row including every action;
if two arrays require separate scans it is <187.5 ms/row before elevator travel,
locking and settling. Concurrent arrays require counted parallel hardware.
No purchase price, viable <30-s machine, reliability or fabrication claim follows.

Next discriminator: construct the **row-local pin-to-dog set/reset and cam
transfer** through all loaded/unloaded states, including a mechanically enforced
withdrawal interlock; compare its repeated contacts and scan phases against a
seated magnetic flag. Stop this shutter embodiment if positive withdrawal or
retained-dog reset requires excessive per-cell parts or violates the timing/cost
boundary. No print request: geometry and energy routing can still reject it
cheaply. Magnetic seating remains unresolved, not displaced by this comparator.
Verification is self-review: interval corners, periodic-neighbor exclusion,
exhaustive transition permutations and force-sum checks only.
