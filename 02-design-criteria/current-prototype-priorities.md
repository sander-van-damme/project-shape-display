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

There is already an **optional, unprinted READY P1** [five-pair short-thread tolerance STL](../owner-print-tests/short-thread-fit/test.md): three nominal repetitions and two clearance variants. Do not recreate the same job. When specifically assigned, prepare a *small* meaningful STL batch, supports/orientation checked, with simple results and no owner deadline. Distinguish useful failure and print-to-print variation from an inferred array yield.

## 4. Later-stage comparisons

Complete-machine cost, reliable retention, repaired failures, optical height readback (possibly by shared 3D camera), drift correction and game interruptions are useful later. Detailed [E-293 optical work](../06-experiments/E-293-baseline-sensitivity-versus-terrain-visibility.md) is **not a prerequisite** for proving mechanical up/down movement. Reopen sensing only for a concrete immediate blocker; don't allocate another autonomous research thread because an optical model has an unresolved parameter. No purchases are authorized by a research target.
