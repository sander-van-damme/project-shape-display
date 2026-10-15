# Independent final review of the resident C-guide integration

15 October 2026. Independent of the cell CAD author; frozen sources, checker
logic and saved results were inspected, then the original nominal replay,
admitted-play counterexample and bounded-variant search were regenerated in an
isolated directory. All three regenerated JSON records match their stored
records. No integrated mechanism has been physically tested.

**Disposition: retain the captured C-guide topology as a conditional research
candidate, but do not release either embodiment as a complete-machine build.**
The original embodiment fails an admissible angular-clearance case. The longer
guide/shorter tooth variant removes the failures in the finite planar screen;
it still lacks positive unloading margin, a qualified support-transfer force
limit, a buildable bank junction and a demonstrated row writer. Its precision
parts, joining operations and mass prevent a manufacturing or affordability
pass. The two small printed articles elsewhere in DES-008 do not qualify these
metal interfaces or the complete resident architecture.

## Frozen evidence and its actual scope

| Evidence | Result | Qualification boundary |
|---|---|---|
| Original [resident cell](../cad/resident_cell.scad), SHA-256 `780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157` | 270 author checks and 3,390 independently generated nominal checks contain no unexpected positive overlap | Centred rigid solids at the sampled states, including deliberate wrong-OLD obstructions; not a tolerance, contact-force or assembly pass |
| Exact original admitted-play counterexample | Dog clears its channel and guide but penetrates its own rack by **0.1013509041 mm³** | The embodiment's claimed clearance-based isolation is **FAILED**, even with perfect nominal solids |
| Directly abutting, unmirrored writer links | **14.68805388 mm³** overlap with the next bank's pin | This bank layout is **FAILED**; a mirrored or rearranged junction is unconstructed, not disproved by this example |
| [Bounded guide variant](../cad/resident_cell_guide_escape.scad), SHA-256 `24eb609bdb034dccbd72d93b6ee8af8cca14b333965516dce820bfd237af07e9` | 270 centred checks; 1,954 planar candidates, 1,924 admitted, zero sampled own-rack collisions | A finite planar screen, **not** a six-degree-of-freedom clearance proof |
| Variant neighbor search | No overlap in the extremal opposite-bit neighbor-key shortlist | Two common-A endpoint states and selected planar pose pairs; not all neighbors, intervening motion or simultaneous guide/frame errors |
| Vertical support-transfer margin | Nominal 0.10 mm margin is consumed by admitted ±0.10 mm key-guide play | Positive unloading and reliable transfer remain **UNRESOLVED** |
| Fabrication, powered operation and durability | No measurements | **UNRESOLVED** |

Reproducers are [check_resident_independent.py](../analysis/check_resident_independent.py),
[check_resident_counterexample.py](../analysis/check_resident_counterexample.py)
and [check_resident_escape.py](../analysis/check_resident_escape.py). Their
corresponding records are [resident-independent-checks.json](../analysis/resident-independent-checks.json),
[resident-counterexample.json](../analysis/resident-counterexample.json) and
[resident-escape-review.json](../analysis/resident-escape-review.json).
The closing replay used Python 3.12.14 and OpenSCAD 2021.01. These results do not
depend on interpreting a rendering as an interference check.

The original counterexample rotates the dog −4° about Z at
(3, −2.2, −30.4) mm, then translates it by
(−0.0817508698, +0.0487983689, 0) mm. Channel and guide Boolean intersections
remain zero. The tooth reaches Y = −0.47349 mm beyond the groove back at
Y = −0.55 mm. This is a geometric permission for jamming, not a prediction that
every unloaded dog will spontaneously assume that pose. No undocumented
self-centering force can be credited as a cure.

The bounded revision changes the guide bearing length from 0.5 to 1.0 mm, uses
a 4.5-mm key and reduces tooth penetration from 0.50 to 0.35 mm. It preserves
the stated side clearance. The previous counterexample is no longer a rack
collision. The planar search samples yaw from −7° to +7° in 0.1° increments,
testing vertices and centroids of its feasible translation polygons against
actual meshes. Neighbor checks use the 30 most extreme admitted poses on each
side for opposite-bit keys at a 6.35-mm Y offset. The shortened tooth trades
capture overlap for groove-root clearance, and the longer key leaves only
0.25 mm nominal mixed-bit separation. Pitch/roll, combined vertical error,
elastic deflection, full motion sweeps and minimum loaded capture overlap have
not been qualified. The narrower conclusion is nevertheless useful: this
specific planar failure has a bounded escape without assuming tighter fits.

## Selection and support sequence

The surviving topology has a mechanically intelligible selection path. Each
retained channel constrains an A lift dog and an independent B ramp follower.
A common lateral motion admits only ON dogs; B subsequently releases only
their ground pawls. An unselected pin remains on its original ground pawl.
Stored bits therefore do not require private powered selectors during a lift.
However, the common A subframe itself must be positively held against retreat;
capturing each dog in a channel does not arrest that whole frame.

The corrected ideal sequence for either signed increment is: engage A, raise
the lift **0.40 mm**, release selected ground pawls, command **+d or −d**,
restore the pawls, lower the lift **0.70 mm**, raise it **0.30 mm**, withdraw A,
then return the empty lift. Both signs need the final forced seating operation.
At the nominal geometry, 0.30 mm closes initial dog backlash and only the
remaining 0.10 mm unloads the ground pawl. A freely following downward pin can
finish the main stroke 0.10 mm above target; a sticky one can finish 0.70 mm
above target. Restoring support before the common 0.70-mm descent handles both
ideal limits. Adding 0.60 mm to the main downward stroke would instead put a
freely following pin below the insertion height and is rejected.

This closes nominal displacement accounting, not the force problem. The
0.35-mm key is 2.6 mm high in a 2.8-mm cavity. Its admitted vertical play alone
can use the entire 0.10-mm unloading allowance, before rack error, wear, frame
deflection or seat compression. During final forced seating, different sites
can meet their ground stops at different platen positions. A rigid common
drive cannot be assumed to complete the highest-drag site without overloading
the first seated site. A designed compliance/preload or force-limited interface
and a measured operating window are required. Merely reducing speed or adding
software height correction does not provide that missing load path.

The 3,390-check replay verifies sampled solid intersections. In particular,
its upward final-seat interpolation follows a freely seating pin; it does not
independently trace every sticky-pin contact transition during that interval.
No claim of a complete multibody contact solution is justified by that count.

The rack-length correction is sound: while engaged, dog and pin translate
together, so their relative rack coordinate is fixed. Separate A and ground
faces each need terrain range plus contact/end margins, not an independent
sum of terrain range and signed carriage excursion. This one-face layout uses
the union of the offset acquisition ranges: −80.4 to −0.4 mm for H = 50 mm.
The stationary C-guide must separately accommodate the foot's complete stroke.

## Scale, construction and repeated hardware

The 6.35-mm study is an isolated-bank interface model, not a packaged 5.08-mm
solution. Its nominal occupied height is **293.2 mm** before enclosure/base.
The reference solid PLA columns total about **14.93 kg** at 4,096 sites.
Complete steel channels, including modeled feet/lugs/bridges, total about
**8.25 kg** in the selection mechanism. Treating them as the earlier lighter
column and mask assumptions would understate drive and handling requirements.

The metal channel needs both end registers. Its ideal 134-mm supported-span
compliance is approximately 0.178 mm/N at E = 200 GPa; the same section in
PLA at E = 3 GPa is about 11.86 mm/N. Plain unsupported printed channels are
rejected at this section. Metal still requires a load budget for lateral
reaction, twist, end-register clearance and joint flexibility. The 0.35-mm
keys, 0.45-mm slots, 0.10-mm guide walls and 0.15-mm lips are precision metal
details, not ordinary 0.4-mm-nozzle FDM features.

For 4,096 sites, count at least 4,096 channels, A dogs, B followers, ground
pawls and terrain pins; 8,192 key-guide interfaces; 8,192 end-register
interfaces containing 16,384 pockets; 8,192 writer lugs and acquisition
pockets; and 8,192 channel-end bridge/join operations. Both feet must enter a
channel before its final closure. The model does not establish a cheap,
repeatable joining or repair process. Integrating parts into combs reduces
handling only if those repeated contacts can actually be manufactured and
assembled with sufficient yield.

The corrected writer uses 64 data setters × 32 rows per bank, with paired
upper/lower pocketed codebars. A top-only writer cannot guarantee the two
unlocked channel ends reach the same bit. Discrete acquisition pockets are
necessary because a slot parallel to data travel cannot drive the lug. At
full scale the reference paired writer weighs about 26.93 g per setter; a
1.6-mm triangular move in 20 ms contributes about 0.431 N of inertial force
before the selected channel, friction, returns and impact. Catalog static
solenoid force does not demonstrate an 80-ms complete OLD/acquire/NEW/reseat
transaction.

The 1-mm local row-cassette plate is not a released 406-mm row beam. Even an
unperforated 5.7 × 1 mm steel strip supported only at its ends deflects roughly
12 mm under the row's channel weight by an ideal beam screen, exceeding the
2-mm acquisition stroke. Distributed support/lifting or a stiffened section
is necessary, with its clearance, guides and transmission engineered. The
fixed frames, common-A arrest, row selection drive, codebar guidance and bank
junction remain incomplete. The failed abutting link arrangement cannot be
removed from the BOM or render without replacing its synchronization function.

## Final engineering boundary

The variant is a defensible next *mechanism study*, because it keeps shared
power and positive resident selection while removing a demonstrated planar
jam. It is not evidence of a fast, affordable, manufacturable full display.
Neither a nominal CAD pass nor success of the manually operated rack or memory
article establishes full-bank seating, powered writing, the junction, array
yield or D&D wall/base clearance.

The next architecture-changing evidence would be neighboring captured dogs
and ground pawls under mixed free/sticky loads, deliberate guide play and a
designed transfer-force limit, followed by powered two-ended pocketed writing
with measured complete cycle time. Before a complete-machine recommendation,
the junction, row support and closure/assembly process also need construction
details and credible costing. Those are explicit unresolved requirements; no
physical or general manufacturing pass is granted by this review.
