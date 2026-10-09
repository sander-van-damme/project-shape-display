---
status: candidate
builds-on: [M-013]
---

# Binary displacement layers with positive load stops

**Bounded; retain as a distinct structural-memory comparator.** Descriptors:
layer/row/column coupling dogs; binary telescopic-extension memory; three shared
layer drives; serial positive shoulders carrying top load; three guided linear
stages per surface element. Binary arithmetic is followed by explicit local
motion and locking paths.

Three nested stages give displacements 10/20/40 mm. At each layer, a shared
bidirectional rack rail couples through a locally addressed dog to one stage;
the stage extends/retracts until it reaches a positive shoulder and engages a
catch. To change a bit, acquire its carriage, lift/unload the catch, retract
it, move, reseat/proof the opposite shoulder and disengage. Other layers remain
caught and travel as a rigid payload when a lower layer moves. Crossed magnetic
flags supply commands; they do not carry structural force. E-067 identifies an
alternative to following lower-layer offsets: clear all
bits on changed columns bottom-up, then set target bits top-down. Every active
layer then has zero lower binary displacement. A fixed-reference drive still
needs stroke travel, retractable coupling and bypass of unselected carriages;
co-moving/offset-following drives remain alternatives if that geometry fails.

Outputs 0/10/20/30/40 use five of eight codes. Clearing old-only bits then
setting new-only bits reaches every endpoint arithmetically but fails fixed-
reference access for some pairs (E-067). Normalizing changed columns preserves
reach while adding contact cycles; 10→30 becomes 10→0→20→30. Some transitions
descend first
(30→40 passes zero); only changed columns move. Intermediate unsupported states
are forbidden: the active layer drive holds load while its catch is open;
all other shoulders remain engaged. Unsupported gaps or neighboring slider
contact reject a realization even if the bit sequence passes.

Three 6,400-site shoulders/catches/dogs and guides repeat: 19,200 load-bearing
stage interfaces before selection. A 10-N load passes through *each* layer;
it is not divided by three. 40-mm stroke layer needs 40 mm telescoping travel
plus overlap. Three nested 0.4-mm walls use 2.4 mm of opposing wall thickness
before gaps and core, a demanding 5.08-mm packaging allocation. Separate stacked
layers avoid nesting but increase depth, alignment and moving rail burden.
At $250 reserve each complete bought layer-site gets at most $0.0130; foil/
magnet/driver purchases can exhaust this despite free printed shoulders.

Underside absolute tail marks verify final sum; per-layer flags and endstop
sensing disambiguate wrong code and wrong latch. Proof unload each changed
layer before disengaging its drive. Retry under held drive once; persistent
failure isolates the module and inserts service support before cartridge repair.
Regional motion is local in the abstract; shared rails must remain clear of
all unselected carriage states. A six-pass clear/set schedule at three layers
charges travel, addressing and proof; cost/time cannot be inferred from three
bits alone. E-068 generates a finite retractable dog/fork section: 15 tight-bound cases
clear the shared rail, including arbitrary parked lower-stage offsets. Its
continuous minimum pitch is 2.6+8e mm, rejecting this section at middle/wide
relative-error bounds (5.40/7.40 mm). This is exterior access geometry, not a
three-layer machine or supported handoff. A rigid rail acquiring unequal dogs
also needs differential latch unload travel: upper-layer tight bounds require
0.60 mm across opposite regional errors, versus 0.30 mm within a coherent
region. Common batch/registration bias cancels from that difference.
E-069 retains an isolated rigid-dog/latch contact path with split-region
nominal overtravel minima 0.40/0.60/0.80 mm, including its explicit fit erosion
and unload margin. A free floating dog with one hard stop preserves the same
mismatch. Deposition proof needs additional fork clearance; failed proof must
retain all bank dogs, and a failed upper seat may descend 0.65 mm on the held
rail. A false acceptance can remove its only support.

E-070 connects the dog bore, latch shelves, backbone and mount in three guide
profiles. A closed sleeve blocks the shelves; an open C guide permits escape.
A captured T guide fits a prescribed straight path only at tight bounds and
0.2-mm residual lip engagement: 5.00 × 4.95 mm including relative-error reserves.
Its actual lateral free play invalidates that path assumption. A permitted
0.19-mm carriage offset plus a −0.15-mm common rail datum shift makes the bore
walls collide with the fork. Allowing nominal guide play raises the necessary
width to at least 5.40 mm, before tilt or overlap loss. Longer guides do not
remove translation play. **Reject this clearance-only interleaved guide under
these bounds; neither isolated contact paths nor centered assembled geometry
passes the machine gate.** Reopening needs changed datum restraint/packing or
process evidence, not finer sampling of the same profile. No stacked geometry,
strength, hardware qualification or fabrication follows. Shared/external guides
and positively biased datum mechanisms remain unproved escapes and must count
their extra constraints, friction and repeated interfaces.

E-067 charges 5.1314 s for serial loaded plus unloaded rail traversals under its
assumed motion limits, before six complete contact events and other overhead.
E-068/E-069's added transfer/proof motion must enter that budget. No complete
cost or timing advantage over the rack/mask comparators has been established.

E-071 tests the next restraint alternatives. A positive datum with a sliding
preload shoe removes nominal translation play but introduces friction feedback
from the offset fork. Even favorable full-length reactions require mu<0.151/0.377
for 1.6/4-mm guides; beyond those scenario bounds no preload maintains seated
upward sliding. The 12/20-mm guides admit ideal reaction solutions at mu≤0.6,
with 1.476/0.607-N minimum preload for W≤1 N and |H|≤0.2 N. These are marginal
necessary conditions, not specified springs or manufactured position control.
A separate rear guide lane needs 7.10 mm and fails pitch. Retain only longer
local datum or vertically relocated shared-frame packing for a bounded finite
restraint/tilt test; no full-system survival or print request follows.
