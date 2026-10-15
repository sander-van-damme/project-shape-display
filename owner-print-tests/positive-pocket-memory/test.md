# Two-row, two-bit mechanical memory — revision 3

**Status:** DEFERRED — verified fabrication files retained; no physical test performed.

**Priority:** unranked; not a current print recommendation.

**Last reviewed:** 15 October 2026.

**Technical source:** [DES-008](../../08-integrated-designs/DES-008-positive-latch-shared-lift/DES-008-positive-latch-shared-lift.md).

**Reason:** this revision adds positively captive flag shoulders and supersedes revision 2. Final independent review found that the surviving resident mechanism needs tall guides, paired end registers and discrete programming pockets. This short-flag article cannot qualify those interfaces; its result would presently have limited effect on that design decision. Preserve the files as a principle study and prioritize the neighboring-pin support-transfer article. Do not mix revisions.

This small article tests whether two shared column code bars can rewrite one row of retained bits while a neighboring row stays unchanged. It has no terrain load, motor, powered row decoder or dog/pawl readout. Success supports further engineering of mechanical memory; it cannot establish full-display performance.

## Files, parts and printing

| File | What it contains |
|---|---|
| [two-row-memory-plate.stl](two-row-memory-plate.stl) | One complete plate: base, two cassettes, four supported flags, two code bars, four lift shims, two keeper bridges and four keys |
| [engineering-drawings.pdf](engineering-drawings.pdf) | Assembly, critical sections, loading window and support-removal diagram |
| [results.csv](results.csv) | Blank observation form |

Open the STL directly in the slicer. **No source compilation is needed.** The [parametric source](../../08-integrated-designs/DES-008-positive-latch-shared-lift/cad/memory_coupon.scad) and [verification script](../../08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_memory.py) are available for engineering reproduction. Bare diagnostic flag meshes are not owner print files.

Source SHA-256: `c6bd26a5f29215c4c34e9e8b53471034562b58a0cf65c35863cc9377d86f89fd`.

The supplied plate is **82.6 × 99.6 × 16.6 mm**. Print ordinary PLA with a 0.4 mm nozzle, 0.16 mm layers, three walls, 100% infill, supports OFF and a 1 mm brim. The comparison slice with PrusaSlicer 2.7.4 estimates **11.02 g and 2 h 1 min 24 s**. This is a comparison profile, not a measured X1C print time. No purchased hardware or special filament is needed.

The orientations and necessary bridges are explicit:

- The base pockets face upward. Its transverse key holes bridge 2 mm.
- Cassettes lie on their long side; the circular guide holes need short 2.9 mm roof bridges. The captured shoulder channel remains open along the print direction.
- Code bars lie inverted on their closed roofs, open channels upward. Keeper sockets face upward.
- Each flag lies on its broad shoulder. Two sacrificial end towers anchor **3.6 and 3.8 mm spans** at the first foot/lug layer. The towers attach through **0.16 mm-thick necks only at the foot bottom and lug top**. No support touches the functional side walls. The comparison G-code has complete paths anchored at both ends at Z = 0.96 mm; it calls these thin paths *Overhang perimeter*. Their physical bridge quality remains untested.
- Carefully clip those thin necks at the two end faces. Inspect for a dangling strand, rough bridged face, shortened flag or crack. Do not sand pocket-facing or lug side faces to force a fit. Record any cleanup. Keep clipped fragments away from the mechanism.

The slicer reported no support/stability warning. That does not qualify the bridges or fit. Supports remain OFF so they cannot fill the guide holes or captive channel.

## What revision 3 fixes

Revision 2's 10 mm sleeves limited cassette tilt but did **not** stop each flag tilting independently in its open-top trough. Its quoted 0.185 mm tolerance bound was invalid and is withdrawn.

Revision 3 traps a **3.4 × 4.0 × 1.2 mm shoulder** between the cassette floor and retaining roof, in a **4.4 mm-wide, 1.4 mm-high channel**. The 2.8 mm central opening passes the narrow foot and lug. The nominal shoulder has 0.2 mm vertical clearance. Flags enter through a separate loading window outside their operating positions, then slide left into their captured tracks. This eliminates the formerly open-top shoulder escape path.

Foot engagement increases to **2.1 mm**, row lift to **2.7 mm**, and nominal acquisition overlap to **1.6 mm**. The right guide post moves to X = 31.5 mm to clear the loading window. The minimum nominal inter-cassette gap is **0.95 mm**.

## Dimensions

| Interface | Nominal dimension, mm |
|---|---:|
| Row / column pitch | 6.35 / 6.35 |
| Stored-bit displacement | 2.0 |
| Row lift / sleeve length | 2.7 / 10.0 |
| Guide post / hole diameter | 2.4 / 2.9 |
| Foot | 0.8 × 2.4 |
| Fixed pocket | 1.2 × 2.8; 2.3 deep |
| Foot engagement / bottom clearance | 2.1 / 0.2 |
| Flag total height | 8.0 |
| Shoulder X × Y × Z | 3.4 × 4.0 × 1.2 |
| Shoulder channel Y × Z | 4.4 × 1.4 |
| Cassette central opening / outer Y width | 2.8 / 5.4 |
| Lug X width / code channel X width | 1.0 / 1.4 |
| Idle lug gap / nominal restraint overlap | 0.5 / 1.6 |
| Raised foot clearance / raised lug-roof clearance | 0.6 / 0.4 |
| Raised cassette-to-codebar clearance | 0.3 |
| Bar-top/keeper clearance | 0.2 |
| Nominal total bar lift, including key play | ≤0.4 |
| Flag loading-window X limits | 23.2–27.5 |
| Rightmost operating shoulder edge | 22.05 |

A foot positively registers a bit in its OFF or ON pocket. It is not a friction detent. At nominal geometry the top lug acquires its code channel before the foot leaves the pocket. Lowering restores pocket retention before releasing the code channel. Code bars are held down by positively keyed keeper bridges, not an operator's hand.

## Restricted planar calculation — not a tolerance guarantee

The script calculates 0.369 mm residual overlap for a **restricted planar model** using:

- post-hole diametral gap ≤0.6 mm and sleeve engagement ≥9.8 mm;
- shoulder in-plane width ≥3.3 mm, thickness ≥1.1 mm and vertical clearance ≤0.3 mm;
- flag height ≥7.9 mm, lug width ≤1.2 mm and foot/lug depth ≤2.6 mm;
- floor-to-channel gap ≤6.5 mm, plus local upward bar play ≤0.5 mm.

Cassette tilt is `atan(0.6/9.8) = 3.504°`. Independent planar flag tilt solves `3.3 sin(theta) + 1.1 cos(theta) = 1.4`, giving 5.298°. The summed 8.801° angle and maximum transverse diagonal `sqrt(1.2² + 2.6²)` yield the 0.369 mm screen.

**This assumes zero shoulder yaw and that the shoulder's extreme points remain under the floor/roof retaining rails.** The roof's central opening means this is not a general bound over coupled yaw, translation and tilt. It is **not a pass criterion**, and these dimensions are not measured print results. A full three-dimensional tolerance proof remains unresolved. Elastic deformation, friction and wear are also unqualified.

Measure actual dimensions and local codebar vertical play at **both rows**, including any tilt of its ends. Record shoulder/channel clearances. Excessive play or interference is evidence to revise the design; do not treat the planar calculation as permission to force a fit.

## Assembly

1. Remove brim and clip each flag's two end towers as described above. Inspect all four nominal samples; do not selectively use only the easiest flags. Check that the channels and guide holes are clear without scraping their functional surfaces.
2. **Load each cassette off the base.** Place a flag's foot through the large loading window centered at X = 25.35 mm. Lower its shoulder into the channel, then slide it left to X = 12 mm. Load the second flag through the same window and slide it to X = 18.35 mm. Both shoulders must remain trapped beneath the roof. The right-hand loading window is for assembly only; it is outside both working bit positions.
3. Hold the two flags over their OFF/left pockets and lower the cassette onto the two posts at X = 4 and 31.5 mm. The cassette rests on the base pads. Repeat for the second row. Confirm that each cassette can rise and lower without forcing or disturbing the other row.
4. Place the code bars with long channels downward in their base end-guide slots. Set both to the OFF/left stops.
5. Lower a keeper bridge over each pair of square end piers. Insert two flat keys through each bridge and its piers, four keys total, with their heads close to the collars. Keep all four fully inserted throughout testing. These removable keys are not vibration-qualified fasteners.
6. Verify 2 mm free codebar travel, no keeper rubbing in normal travel, and positive retention against lifting the bars out. Measure vertical play locally over each row.
7. The two **2.7 mm shims** beneath the ends of one cassette hold that row raised. Its spare pair is for the other row; raise only one row during writing. Do not put a shim beneath the central flags.

## Write sequence

1. With both rows down, set the code bars to the **current OLD bits** of the row to change. The other row remains pocket-locked.
2. Lift the selected cassette and insert its two shims. Its lugs acquire the OLD code channels and its feet leave their pockets.
3. Slide the two bars to NEW. Only the selected row's flags should follow.
4. Hold the bars at NEW, remove the shims, and lower the cassette completely. Confirm both feet seat in the NEW pockets.
5. Only after seating may the bars move to another row's OLD values.

A wrong OLD setting is deliberately blocked by nominal geometry. **Do not force it.** Restore the correct setting. Initialization and recovery after uncertain stored state remain full-machine engineering obligations.

## Minimum physical experiment and decisions

Begin with A `00 → 11`, B `00 → 10`, A `11 → 01`, B `10 → 01`, A `01 → 00`. Check the unchanged row and keeper keys after every transaction.

If those work, exercise all sixteen two-bit OLD/NEW combinations on each row, including unchanged writes, with the other row at a contrasting value. Record every incomplete acquisition, lost flag, cocked shoulder, missed pocket, neighboring motion, key movement or forced fit.

Repeat slow acquisition and lowering with the cassette **gently biased toward each side of its available guide play**, then with the codebar gently lifted through its available play over the row. Try front/back and diagonal bias separately, within free clearance only. Keep hands clear of pinch points and stop before visible bending. Complete the subsequent NEW write and seating each time; an incomplete move, jam or escaped flag means the handoff failed. This is a deliberate challenge of the unresolved three-dimensional tolerance behavior, not proof of every possible configuration.

Photograph or note where a failure occurs. Record printer/material/layer conditions, all four flag fits, cleanup, measured clearances, local bar play, damage and whether biased handoffs differ from centered handoffs. A coupon that only works when carefully centered has **not** demonstrated tolerant mechanical memory. A successful coupon still does not qualify thousands of parts, terrain loads or an 80 ms powered row cycle.

## Digital evidence and remaining boundary

The engineering verification script regenerates the part meshes and complete plate. It checks nineteen watertight plate bodies and **83 sampled nominal CSG cases** covering assembly-port insertion, in-channel loading, row acquisition, intermediate writing, adjacent flags/bars/cassettes, unselected rows, keeper mounting and keys. All have zero positive intersection volume. Wrong-OLD acquisition has **2.112 mm³ blocking overlap**.

The collision checks are nominal samples, not a continuous tolerance or elastic analysis. No physical result is claimed. The next decision is whether positive pocket registration, captive shoulders and shared code bars provide repeatable acquisition and isolation under actual printed variation. Memory-to-dog/ground-pawl integration, powered row selection, aggregate force and full-system timing remain separate unbuilt tasks.


## Owner results — leave blank until tested

- Test date:
- Printer / filament / actual slicer settings:
- Print: [ ] not performed [ ] complete [ ] partial [ ] failed
- Worked as printed / cleanup / clipped-end condition:
- Centered writes and unchanged-row observations:
- Deliberately biased writes and exact failure, if any:
- Damage / cycle count / measured clearance or bar play:
- Optional photo/video:

**Engineering interpretation after owner feedback:** not yet available. An empty form is unknown, not failure. No further print or purchase is automatically scheduled.
