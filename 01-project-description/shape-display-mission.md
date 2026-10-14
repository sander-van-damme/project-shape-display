# Shape Display — product mission

Build a playable, interactive physical Dungeons & Dragons battle map. The win condition is **fun, legible, responsive play**, not technological spectacle, maximum mechanical resolution, or satisfying early numeric targets regardless of usefulness.

## Physical D&D representation

The intended grid has **one-inch (25.4-mm) game squares**. Miniatures stand *inside* those squares; Sander imagines **thin walls on the lines between squares**. The actual wall has nonzero thickness, so a one-square-wide corridor bounded by two walls must be tested with the intended physical miniature base and real clearance. A wall made from a full raised pin centered on the line may steal floor area; selecting a finer pitch alone does not automatically solve this.

Use physical columns for meaningful terrain: ordinary stable ground, hills, substantial rocks/cliffs, ravines, stairs, platforms and walls/barriers. Trees, small debris, textures, icons or furnishings may be clearer as ordinary props or optional artwork/projection. A single heightfield cannot show simultaneous stacked floors or a playable passage beneath a solid bridge.

**Resting height is a design decision.** A raised neutral/mid-travel ground plane may let water or pits descend and hills/walls rise without raising all ordinary land. It requires actual mechanical downward/upward travel, guidance and real preparation time: a software offset cannot create motion.

## What to develop now (owner direction, 14 October 2026)

**The immediate goal is a small, genuinely working mechanical principle: independently raise and lower multiple pins without touching, jamming or driving unaffected neighbors.** The previously hand-tested screw/rod family and shared actuation are promising candidates, not commitments. A few low-waste, ready-to-slice FDM tolerance prototypes can be more informative than a new chain of speculative simulations. Read [current prototype priorities](../02-design-criteria/current-prototype-priorities.md).

Small positional drift is acceptable at this stage. Advanced optical readback, a shared 3D-camera system, camera calibration, software drift correction, expensive fault automation and elaborate homing can be developed **later**, unless a specific blocker makes the minimum functionality essential. Basic mechanical safety and support are never optional.

## Legacy comparison targets

About **400 × 400 mm**, **5.08-mm pitch / 6,400 pins**, **40-mm useful terrain range**, **~30 seconds typical gameplay interruption**, and **~$500 bought components** are **benchmarks**, not automatic rejection gates. Compare **6.35-mm pitch** and even **12.7 mm** only if actual walls, corridors and miniature placement still work. Less repeated hardware is not a win when D&D geometry becomes unplayable.

A more enjoyable ~$1,000 finished concept or a $1,000–$1,500 research demonstrator can be worth analyzing; neither authorizes purchasing. Count all purchased hardware, printing, labor, wasted parts, power, setup, neighbor isolation and repair. Account for neutral preparation and real scene transitions separately from a dense stress test.

## Engineering evidence and economy

Favor simple, tolerant repeated parts and accessible shared mechanisms when system accounting supports them. Shared row/column selection, rotary heads, programmable masks and other principles are hypotheses requiring real motion, load paths and non-target isolation. Explore mechanically different principles only when explicitly requested or when evidence invalidates the chosen approach.

Use the cheapest **decision-changing** simulation, analysis, CAD or physical test. Stop speculative refinement when it cannot change an architecture decision. A calculated clearance, slicer path, CAD render or owner memory does not establish a repeatable physical mechanism. Keep genuine measured observations, scoped negative results, and reproducible source.

The current stage-02 requirements, historical stage-06 experiments and stage-07 decisions are the technical references. Historical [owner ideas](owner-ideas.md) are optional hypotheses, not a research queue.
