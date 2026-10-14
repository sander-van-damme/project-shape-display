# Owner print-test handoff

This folder provides **optional, ready-to-slice STL packages and simple result forms** for Sander. There is no autonomous print queue. An assigned Codex engineer picks a test only within a clearly requested task; Sander may not print soon or ever, without blocking other work.

- Prefer **one small plate** answering one decision. At most three total **READY** jobs, prioritized P1/P2/P3; unused slots need not be filled.
- Follow `TEST-TEMPLATE.md` with `<test-name>/test.md` and **actual validated STL(s)** in the same directory. Do not send Sander only OpenSCAD/Python or ask him to export CAD. State exact parts, label variants, slicer orientation/support/brim, material, estimated filament/time and a short, safe step-by-step test.
- Where relevant include **2–3 tolerance variants and several identical nominal samples** on a small plate. For long slender rods, check support stability through all layers, support removal and functional thread scarring; don't assert an unsupported upright part is qualified because a slicer printed no support path.
- Record printer conditions and actual fit, travel, friction, binding, damage, cleanup and other observations. An unperformed test is **unknown**, never a measured pass or failure; five coupons do not qualify thousands of parts.
- Track status DRAFT / READY / DEFERRED / COMPLETED / RETIRED. On new evidence, update genuine priority and retire stale tests/STLs with a reason. No deadline, reminders, purchase or ever-growing backlog.

Latest results: [five short screw/nut pairs](short-thread-fit/test.md) **COMPLETED** (owner hand-fit report 2026-10-14), but the 10.3-mm-wide test nuts are not compact enough to establish dense pin suitability. [Trial 5 short replica](trial5-short-replica/test.md) **DEFERRED** after supports filled its internal threaded bore; its fit is untested, distinct from the owner's historical report of a working slim Trial 5 print. No new print is scheduled. Previous [S40 offer is retired](supported-s40/test.md).
