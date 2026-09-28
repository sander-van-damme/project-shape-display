# 03.1 — Engineering disciplines

Start broad: which engineering fields have already solved problems analogous to this Shape Display?

The sections below capture useful domains such as tactile displays, textile machinery, mechanical computing, horology, compliant mechanisms and reconfigurable tooling. They are sources of reusable mechanisms and patterns, not Shape Display architectures by themselves.

The next step is to extract concrete [mechanisms](../03.2-engineering-mechanisms/).

## D-005 — Compliant mechanisms and multistability

Compliant mechanisms replace joints and fasteners with elastic deformation.
Multistable structures can retain discrete states without continuous power.

This is attractive because printed complexity is cheap for this project.
Important risks are PLA creep, fatigue, print-direction sensitivity, snap-force
variation and the 5.08 mm pitch envelope.

## D-002 — Horology and intermittent motion

Clock and watch mechanisms are relevant for repeated indexing, detenting,
intermittent motion and compact state sequencing.

Transferable families include escapements, ratchets, Geneva mechanisms, cams,
followers, detents and hard geometric indexing.

The main lesson is geometry-backed repeatability. The main caveat is that FDM
plastic at thousands-of-parts scale is not precision watchmaking.

## D-003 — Mechanical computing and automata

Mechanical calculators, coding drums, pinwheels, punched media and automata
separate program representation from mechanical execution.

They are useful for thinking about a terrain map as a large mechanical state
vector that must be encoded, stored, decoded and verified.

Historic mechanisms can be excellent read-only or slow-write memories, so
rewritability must be evaluated separately.

## D-009 — Planar, sheet and laminated mechanisms

Patterned plates, films, laminates, shutters, flexure sheets and layered
mechanical media are relevant because inexpensive plastic geometry can replace
purchased precision parts.

The current high-value question is whether planar media can encode many cell
states and be read in parallel by a global or module-level motion.

## D-004 — Printing and office machinery

Printers, typewriters, plotters, teleprinters and sorting machinery repeatedly
address positions using travelling heads, shared shafts, impact elements and
coded sequences.

The useful analogy is high-cycle addressing with a small number of expensive
moving assemblies. It does not remove the project's 30-second / 6400-state
throughput constraint.

## D-007 — Reconfigurable tooling and fixtures

Pin tooling, flexible fixtures and adjustable forms create spatially varying
geometry from repeated supports.

The project-relevant analogy is a mechanically programmed support field rather
than a continuously powered actuator array. Industrial fixtures may tolerate
slow setup, so update-rate assumptions must not be imported uncritically.

## D-006 — Robotics and mechanical multiplexing

Underactuated robots, tendon systems and clutch-based transmissions explore how
few actuators can serve many outputs.

The transferable idea is to separate where power is generated from which output
receives it. The trap is replacing one motor per cell with one costly clutch,
cable or selector per cell.

## D-008 — Tactile and shape displays

Refreshable Braille, tactile arrays and shape-changing interfaces provide direct
references for actuator density, addressing, latching and interaction.

Many systems optimize for millimetres of travel and light fingertip loads,
whereas this project needs ~40 mm travel, tabletop load support, low cost and a
large active area.

## D-001 — Textile pattern machinery

Jacquard, dobby, knitting and related machinery solve a recurring problem:
many repeated outputs must be selected from shared machine motion.

Transferable families include punched/patterned media, hooks and followers,
sliding selector bars, pattern chains, drums and tapes. The key lesson is the
separation of **selection** from **power**.

Useful search vocabulary: Jacquard, dobby, heddle selection, needle selection,
pattern chain, selector plate and cam box.

The analogy does not solve 40 mm load-bearing terrain travel by itself.


## D-010 — Programmable mechanical metamaterials

Tileable mechanical metamaterials can store discrete state in the geometry of
their unit cells and change structural response after reprogramming.

This is relevant because a dense printed layer could act as reusable mechanical
memory or selection logic without one purchased latch per terrain column. The
most useful transfer is likely a **small-stroke memory layer that controls a
separate 40 mm lift**, not a metamaterial cell that directly becomes the visible
terrain column.

Relevant precedent: Chen, Pauly & Reis demonstrated independently writable,
bistable mechanical "m-bits" with distinct write and read phases in a tiled
array ([Nature 589, 386–390, 2021](https://doi.org/10.1038/s41586-020-03123-5)).

Main project risks are printable pitch, state cross-talk, switching-force spread,
creep/fatigue and the cost/throughput of writing thousands of cells.
