# Current prototype priorities and playable geometry

**Owner decision, 14 October 2026.** This applies to *explicitly assigned tasks*, not continuous autonomous research. Stable product criteria and original numeric comparators remain in adjacent stage-02 files.

## 1. Mechanical movement before sophisticated instrumentation

**Primary question:** Can a small practical mechanism move **several individually addressable columns both up and down** without blocking, colliding with or unintentionally moving neighboring columns?

Investigate actual screw/guide engagement, antirotation, independent selection, both directions, load support and print fit on the smallest meaningful rig. A physically raised neutral position is allowed if it has actual travel to either side. A minor height drift is **not a failure** at this early stage. Precise absolute-height sensors, projector/camera readout, drift software, elaborate self-homing and comprehensive failure recovery are **not current standalone priorities**.

Do not conflate deferment of readback with permission for unsafe test hardware, loss of structural support, collisions or unpredictable violent motion. Use a simple stop/disconnect where needed for safe bench work.

## 2. D&D geometry constrains the pitch

The play grid is **1 inch = 25.4 mm per square**. A miniature stands on the playable floor within its game square. **Walls are thin vertical panels on the grid LINES between game squares**, not bulky raised full squares replacing the floor.

For a one-square-wide corridor with walls on both sides, show a dimensioned top view and section with **actual inner wall-face clearance, real wall thickness, mini-base diameter and realistic placement tolerance**. "Small/Medium occupies one square" in game rules is not proof of the miniature's exact plastic base size. Verify the base types the product aims to support.

A full-pitch-width wall centered on each corridor boundary leaves only **20.32 mm free at 5.08-mm pitch; 19.05 mm at 6.35; 12.70 mm at 12.7**. That may fail normal minis. Finer grids are not automatically sufficient, while 12.7 mm is **only a comparison**, not the default design. A separate thin-wall interface, different cross section or another honest mechanical representation may solve it; prove it without pretending walls have zero thickness. [E-276](../06-experiments/E-276-half-square-terrain-and-direct-spindle-tradeoff.md) shows one coarse conversion that narrowed a doorway to 12.7 mm, and its fix deletes wall cells.

Keep physical ground, walls, meaningful cliffs/ravines. Trees, tiny stones and texture need not move as pins. Test pin-top support and unwanted neighbor motion at the candidate pitch before declaring a finished D&D playable machine.

## 3. Low-waste physical learning

The former READY P1 [five-pair short-thread tolerance STL](../owner-print-tests/2026-10-14-short-thread-fit/test.md) is now **COMPLETED** (owner report, 2026-10-14). All five pairs underwent five manual forward/reverse cycles without damage or postprocessing: the three 0.15-mm-clearance nominal repeats varied from mildly stiff to fairly smooth, 0.10 mm was very stiff and 0.20 mm felt best. This is hand-fit evidence, not measured motor torque or production yield. **The test nuts are 10.3 mm wide**, so fine-pitch suitability remains unproven. The owner recalls successfully printing/using the historical **4.4-mm-wide Trial 5** hollow threaded pin family; exact historical parameters are unknown. A new [short replica](../owner-print-tests/2026-10-14-trial5-short-replica/test.md) was attempted but supports filled the bore and were not removed, leaving its actual thread fit unknown. Preserve both the positive historical evidence and the remaining compact-geometry question. Do not recreate the completed job. When specifically assigned, prepare a *small* meaningful Bambu Studio `.3mf` print plate with verified X1 Carbon printer/filament/process settings and checked supports/orientation, with simple results and no owner deadline. Distinguish useful failure and print-to-print variation from an inferred array yield.

## 4. Later-stage comparisons

Complete-machine cost, reliable retention, repaired failures, optical height readback (possibly by shared 3D camera), drift correction and game interruptions are useful later. Detailed [E-293 optical work](../06-experiments/E-293-baseline-sensitivity-versus-terrain-visibility.md) is **not a prerequisite** for proving mechanical up/down movement. Reopen sensing only for a concrete immediate blocker; don't allocate another autonomous research thread because an optical model has an unresolved parameter. No purchases are authorized by a research target.
