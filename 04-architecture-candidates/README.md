# 04 — Architecture candidates

This stage contains **Shape Display-specific system hypotheses** built from the reusable mechanisms and principles in stage 03.

An architecture should state how it handles at least:

- selection;
- power delivery;
- height/state memory;
- load support;
- reset and reprogramming;
- regional updates;
- sensing or verification where needed;
- full-scale timing, cost and packaging implications.

Architecture sections are hypotheses until supported by evidence. Their unresolved assumptions should become explicit items in [`05-research-questions/`](../05-research-questions/) and be tested in [`06-experiments/`](../06-experiments/).

## A-004 — Double-buffered mechanical map cartridges

### System concept
One cartridge drives visible terrain while another is programmed off-line, then
the media are swapped during a short visible transition.

### Strength
Can hide mechanical write time behind gameplay.

### Weakness
A single full-board cartridge conflicts with unexpected local reveals. The idea is
stronger when applied at tile level and combined with A-003.

### Decision state
Keep as a buffering principle, not the preferred monolithic architecture.

## A-002 — Global lift with passive bistable cell memory

### System concept
A global lift supplies most vertical energy. Local selectors toggle passive cell
latches at one or more height planes.

### Main unknowns
Reliable tiny latches, selector density, reset strategy and correlated failure at
6400 cells.

### Cheapest falsification path
3×3 full-pitch latch array plus shared selector motion and measured cycle/load
tests.

## A-003 — Planar mechanical memory with independently updateable tiles

### System concept
Partition the board into local tiles. Each tile contains planar height memory and
can be cleared/reprogrammed without resetting neighboring terrain.

### Functional decomposition
- selection: module/tile selector;
- power: shared module lift;
- memory: perforated or reprogrammable planar layers;
- load support: first-stop plate or local hard support;
- regional update: independent tile operation.

### Main unknowns
Tile size, seams, sheet registration, local lift coupling, insertion force and a
writer that does not recreate thousands of bought channels.

### Cheapest falsification path
Two adjacent 5×5 tiles; modify one while measuring motion of the loaded untouched
tile.

## A-001 — Rotary-stop array with shared programming head

### System concept
Each cell stores one of several heights in a rotary stepped stop. A common platen
provides long-stroke lift while a wide programming head writes rotor angles.

### Evidence and history
Test08 produced a conditional 26.25 s schedule. Test09 reproduced timing but found
unresolved detent, coupling, structure and sourcing gates.

### Decision state
Useful reference architecture; not product-qualified.

## A-006 — Shared power with selective module lift

### System concept
One or a few power sources feed a module-level mechanical bus. A clutch or matrix
selector couples only requested tiles to the lift. An "all modules" mode can
support fast full-board reset.

### Why it may fit
The selector problem is reduced from ~6400 cells to tens of modules while local
reveals remain possible.

### Cheapest falsification path
Two-module lift with one shared actuator and selective coupling; one module stays
loaded and stationary while the other cycles.

## A-005 — High-speed travelling multi-row programmer

### System concept
A fast carriage services several rows and many columns during each dwell.

### Main unknowns
Selector implementation, moving mass, carriage dynamics, loaded engagement time,
fault recovery and full BOM.

### Decision state
Especially interesting as a writer for mechanical memory rather than as the
load-bearing display mechanism itself.

## Shape-display applicability matrix

Current **project interpretation**, not validated scores.

| Mechanism | 5.08 mm packaging | 40 mm compatibility | Passive hold | Low bought-part potential | Full-map parallelism | Regional update |
|---|---|---|---|---|---|---|
| M-001 travelling head | difficult | yes | no | medium | conditional | strong |
| M-002 Jacquard selector | plausible | indirect | no | strong | strong | tile-dependent |
| M-003 bistable latch | difficult | indirect | strong | strong | shared-lift dependent | strong |
| M-004 ratchet/pawl | difficult | yes | strong | strong | multi-pass | moderate |
| M-005 compliant multistable | difficult | indirect | potentially strong | very strong | selector-dependent | strong |
| M-008 shared shaft/clutch | module-scale plausible | yes | no | conditional | strong | strong |
| M-011 sliding matrix | module-scale plausible | indirect | no | strong | conditional | strong |
| M-012 rotary stop | CAD at pitch | yes | strong | conditional | conditional | weak unless modular |
| M-013 perforated plates | plausible | yes | strong | very strong | very strong readout | strong when tiled |
| M-014 reprogrammable aperture | unknown | yes | potentially strong | conditional | strong readout | strong |

Unknowns remain unknown until calculation, CAD or measurement exists.
