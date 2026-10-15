# Manual positive-rack support-transfer article

**Status:** READY — fabrication files reviewed; physical result unknown.

**Priority:** P1, optional; no deadline or purchase.

**Last reviewed:** 15 October 2026.

**Technical source:** [DES-008](../../08-integrated-designs/DES-008-positive-latch-shared-lift/DES-008-positive-latch-shared-lift.md).

No physical test has been performed. This is a four-active/four-witness manual experiment, not an automatic selector, full bank lift, endurance specimen or playable miniature surface. Source freeze: `0d75dbccb58f0134b698a23b19b4550c2cabab21a4e8aa852bce8a03ef6c3964`.

The decision is whether a captured dog can move selected neighboring racks up and positively down, transfer each onto its original fixed pawl, and leave the other racks stationary. A successful result justifies integrating this load transfer with resident selection memory. A failure identifies which fit, guidance, return or support assumption needs replacement. Do not order a full array from this test.

## Released files

Open [four-pin-handoff-plate.stl](four-pin-handoff-plate.stl) directly in the slicer. It contains all 46 parts; no CAD export is needed. Use [dimensioned-rig.pdf](dimensioned-rig.pdf) for assembly and contact geometry, and [results.csv](results.csv) for observations. The [parametric CAD](../../08-integrated-designs/DES-008-positive-latch-shared-lift/cad/rack_handoff.scad) is provided for engineering reproduction.

## Parts and ordinary hardware

The released plate must contain **46 printed parts**. Keep the supplied orientations and 100% scale. Eight identical pins and four identical keys/keepers give repeated samples, not tolerance variants. The active and witness root clamps are now geometrically identical; two filenames preserve the row labels.

| Printed part | Quantity | Identification |
|---|---:|---|
| `pin` | 8 | 95-mm stem, 5×5-mm cap, two grooved faces |
| `ground_comb` | 2 | Four flexible pawls on one root |
| `root_clamp_active`, `root_clamp_witness` | 1 each | Four inter-leaf cap gaps; two bolt ears |
| `drive_key` | 4 | Rear captured tooth with front offset handle |
| `dog_keeper` | 4 | Small slotted blocks retaining ON or OFF handles |
| `ground_keeper` | 4 | Flat hooks with downward peg |
| `carriage_base`, `carriage_lid` | 1 each | Base has 18.4-mm effective bearing bores; 3.6-mm floor; lid 6 mm |
| `bottom_guide`, `lower_guide`, `ground_seat`, `upper_guide` | 1 each | Bottom5-mm bearing region; lower3; seat4; upper3 |
| `spacer_bottom` | 4 | 38 mm; front two are the carriage guide sleeves |
| `spacer_long` | 4 | 16 mm |
| `spacer_short` | 4 | 7 mm |
| `frame_foot` | 4 | 17-mm-high cups with top nut recess |

| Ordinary hardware/tool | Quantity | Actual use |
|---|---:|---|
| M3×80 socket-head screws | 4 | Complete frame stack |
| M3×10 socket-head screws | 4 | Four comb-root clamp joints |
| M3×16 socket-head screws | 2 | Two carriage lid joints |
| M3 hex nuts, nominal 5.5-mm flats / 2.4-mm thick | 10 | Matching joints |
| 2.5-mm Allen key with a straight long arm | 1 | M3 heads; root bolts reached through 3.5-mm access holes |
| Small pliers or 5.5-mm nut driver | 1 | Hold exposed nuts during gentle tightening |
| Ruler/caliper, fine marker, optional thin ordinary paper | As available | Relative heights, parked-carriage mark, gentle descent drag |

No specialized sheet, spring wire, motor, purchased selector or adhesive is required. Use suitable hardware already available; this handoff does not place an order. CAD models 5.5×3-mm socket heads and 2.4-mm nuts. Different heads, washers or nyloc nuts change the clearances and must be checked.

## Printing and inspection

Use ordinary PLA, 0.4-mm nozzle, 0.16-mm layers, three perimeters and 100% infill. Supports OFF; **3-mm brim** on the final packed plate. Pins lie on their broad side; combs on their backs; keys and keeper blocks flat; sleeves/cups upright. All supplied part files are in these poses. Remove brims gently. The solid CAD material is **48.91 g at 1.24 g/cm³**. The final PrusaSlicer comparison estimates **52.12 g and 9 h 20 min 17 s**, including the 3-mm brim, at the supplied comparison speeds; this is a modeled estimate, not a measured X1C print. The packed plate occupies **180.675 × 181.621 × 38 mm**.

**After importing the packed STL, split disconnected bodies into 46 separate objects while preserving their positions and orientations.** Check the count before slicing. The single-object combined mesh triggers a loose-extrusion warning in the comparison slicer even though all independently sliced part poses are clear; splitting it into objects resolves that warning without changing geometry or material. Do not auto-enable supports or stand the pins upright.

Continuous pin edge lands create short roofs over the rack pockets when side-printed. Inspect those small bridges for droop. Check every 0.6-mm spring leaf is present, every thin sidearm is continuous, sleeves remain straight, and no brim or seam blocks a guide. Do not sand a failed tooth or force a fit and then report the original geometry passed. Record any cleanup and preserve the failed sample. There are eight repeated pins, two combs and four repeated keys to expose variation. Print success and fit remain unknown until tested. The prescribed cantilever visualization leaves only about 0.09 mm between a released leaf and the root-clamp backbone near the root; actual print size and elastic shape can consume that gap. Distinguish a local print/leaf-clearance failure from failure of the positive-support principle, and stop rather than forcing the tab. Neither the ideal shape nor a clear Boolean pose establishes elastic return or fatigue.

## Assembly and operation

Follow [assembly.md](assembly.md), then [operation.md](operation.md). Read the complete signed transaction before releasing any ground pawl. These are essential steps, not optional reference notes.

## Short test sequence and stop conditions

Begin unloaded, using only pin self-weight. First test one active output at a time: height 5→10→5→0→5, with the other seven pins untouched. Then test masks 1010,0101,0011 and 1111 for5→10→5 and5→0→5. If this is smooth, exercise all 16 masks in both directions from5 mm (including empty mask 0000). Return to 5 mm between trials. Do not infer one mask passed because a different subset moved.

To demonstrate **mixed-load forced descent**, use mask 1111 and add light drag to one selected pin after confirming its dog is captured; leave the other three free. Record both the delayed pin and its freely following neighbors. One hand can hold the fixed guide while a fingertip gently rubs that pin; the other moves the carriage. Alternatively insert a thin, removable ordinary-paper strip beside a flat X face at the upper guide. Confirm it can still move with light finger force. It should briefly remain suspended when ground support is released, then move down only as the captured dog's lower flank is driven. Stop if the paper jams or the frame bends. Record how drag was applied; no calibrated force is implied.

Next, set unequal initial active heights 0/5/10/5 and witness heights 5/10/0/5 using individual transactions. Select only outputs whose target stays within 0–10 mm. Repeat alternating masks in both directions. If available, make a short video showing both the operated row and the witness caps. Minor drift is an observation to record; visible loss of support, unwanted stepped movement or contact between neighbors is a failure of the intended independence.

**Stop** on forced fit, missed/partial pawl return, a dog that cannot withdraw after seating, changed unselected rack height, visible root rocking, cracked/white-stressed leaves, skipped grooves, sleeve binding, gross frame bending or pin-tip contact with the bench. Do not press on caps or add weights during the first mechanism test. This is a low-load manual article, not a qualified 1-N-per-pin rig. The 3.6-mm carrier floor and 6-mm lid were added because the former thin rails could deflect by amounts comparable to the support-transfer allowance. Simple beam screens at 0.5 N and PLA modulus 2 GPa give approximately 0.028 mm floor, 0.031 mm lid and 0.024 mm seat deflection. Actual bolted assembly stiffness remains unmeasured; stop if its motion obscures the pin result.

Success means all chosen pins move in both directions, at least one descends against documented light drag, ground support is restored before release, and unchanged pins remain at their previous heights within the stated measurement resolution. Keep **not tested**, **not resolved by the instrument**, and **observed unchanged** distinct. No endurance, selection-cycle time, full-machine cost, miniature stability or array-yield claim follows.

## Results to record

Record printer/material/profile, any cleanup, each pin/key fit, sleeve friction, root capture, keeper seating, pawl return, used mask and direction, old/target/measured heights, untouched active and witness heights before/after, fixed-reference motion, instrument resolution, cycles and damage. Use `results.csv`. Empty results mean unknown, not passed. No print deadline or follow-up obligation is created.

## Owner results — leave blank until tested

- Test date / printer / filament / actual slicer conditions:
- Print and assembly result, cleanup and hardware differences:
- Successful masks, directions and cycle count:
- Mixed free/sticky descent and ground restoration observations:
- Untouched active/witness heights and measurement resolution:
- Root movement, frame bending, binding, damage or incomplete support:
- Optional photo/video:

**Engineering interpretation:** no result yet. An empty form is unknown, not failure. No additional print or purchase is automatically scheduled.
