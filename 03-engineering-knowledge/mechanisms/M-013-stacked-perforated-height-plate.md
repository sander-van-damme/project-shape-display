---
status: active
---

**Core principle:** Aligned planar stop layers encode height by first obstruction: a follower passes
through holes until it reaches the first solid layer.

For five terrain levels, four binary aperture planes plus a bottom stop can encode
0/10/20/30/40 mm.

**What it solves well:** Parallel passive readout, cheap planar memory and potentially hard load support.

**What it does not solve:** The pattern still needs a fast write/rewrite method, and full-board sheets are
poor for local fog-of-war updates.

**Cheapest discriminating experiment:** Two adjacent 5×5 tile stacks; repeatedly change one while measuring disturbance,
registration, edge catching and load in the untouched tile.
