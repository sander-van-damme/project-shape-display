# Next research direction — externalized mechanical memory and double-buffered programming

## Why change strategy

The existing research has produced many plausible cell mechanisms, but the same
system-level bottleneck keeps returning: independently programming roughly 6400
cells quickly enough without buying thousands of actuators, selectors, sensors
or precision components.

The next research pass should therefore test a different assumption:

> **The display does not necessarily need to create the map state inside each
> cell during the visible 30-second map transition.**

Instead, investigate architectures where the terrain state is first written into
a cheap **mechanical memory medium**, then the display reads that medium with a
small number of global motions.

## Primary architecture: stacked perforated height plates

A concrete starting point is a stack of thin plastic selector plates beneath the
column array.

For a five-level terrain system (0/10/20/30/40 mm), four selector plates plus a
bottom floor are sufficient:

| Target height | 40 mm plate | 30 mm plate | 20 mm plate | 10 mm plate | Bottom |
|---|---|---|---|---|---|
| 40 mm | stop | — | — | — | — |
| 30 mm | hole | stop | — | — | — |
| 20 mm | hole | hole | stop | — | — |
| 10 mm | hole | hole | hole | stop | — |
| 0 mm | hole | hole | hole | hole | stop |

A narrow lower follower passes through programmed holes. The first plate without
a hole becomes the hard mechanical stop. The upper display column remains square;
the selector medium can therefore be much thinner and simpler than the load
surface.

This is **mechanical unary height encoding**: four binary aperture planes encode
five discrete heights.

## Why this may be interesting

- The expensive display may need only a global lift/release plus alignment.
- Height memory lives in cheap planar media rather than 6400 precision rotors or
  latches.
- The stop can be passive and hard, requiring no holding power.
- Pattern media can potentially be swapped very quickly.
- A plate can be supported by a dense printed grid so it spans only a few
  millimetres locally rather than the full 400 mm width.
- The programming system can be mechanically and physically separate from the
  display.

## The central trade-off

A disposable punched plate is cheap to *read* but potentially slow to *write*.

That suggests three distinct research branches:

### A. Disposable or reusable punched media

Punch/cut the required holes in PET/PETG/polycarbonate/card-like sheet and insert
the four height planes. This is mechanically simple and may be very cheap, but
arbitrary map creation time and consumable material become product questions.

### B. Reprogrammable planar memory

Replace destructive holes with reusable shutters, tabs, sliding strips,
rotating apertures or interleaved slats. A separate programmer changes these
small states; the display itself only reads the finished pattern.

### C. Double-buffered mechanical cartridges

Use two pattern cartridges:

1. cartridge A drives the currently displayed terrain;
2. cartridge B is programmed off-line while A remains in use;
3. one global lift clears the columns;
4. cartridges swap;
5. columns lower onto the new mechanical program.

This separates **programming time** from **visible map-change time**. The 30 s
transition can then be dominated by lift, swap, alignment and lower/settle,
rather than by 6400 individual programming transactions.

The critical product question becomes whether arbitrary maps are normally known
early enough to exploit that pipeline, and whether the off-line writer can
prepare the next cartridge within the interval between map changes.

## Research questions

The next deep research/test should quantify:

- plate material, thickness, sag and creep;
- follower shape and hole-edge chamfering;
- required hole clearance at 5.08 mm pitch;
- local support-grid spacing and load capacity;
- four-sheet alignment and registration;
- manual versus motorized insertion force;
- worst-case friction with thousands of nearby followers;
- sheet/cartridge swap time;
- failure behavior if one hole is undersized or misregistered;
- whether patterned belts/tapes are better than full plates;
- whether row strips can reduce material handling;
- whether reusable shutters can be written row-parallel;
- fastest plausible low-cost mechanical writer;
- lifecycle and cost per map for consumable media;
- end-to-end timing for pre-known maps and genuinely new maps.

## Mechanism-independent lower-bound study

Run this in parallel with the physical concept.

For every future architecture, calculate the required **mechanical information
throughput**. A five-level 6400-cell map contains at least:

```text
6400 × log2(5) ≈ 14,860 bits
```

A 30 s arbitrary-map update therefore corresponds to roughly 495 bits/s of state
change before accounting for motion, reset, verification and error recovery.

The useful metric is not merely actuator speed, but:

- cells or state-bits changed per mechanical engagement;
- engagements per complete arbitrary map;
- purchased cost per parallel channel;
- error probability per written state;
- time hidden by pipelining/double buffering.

This should help reject mechanisms before detailed CAD if their transaction
topology cannot plausibly meet the target.

## Recommended next numbered test

The next new architecture test should be named by **domain + mechanism + question**,
for example:

`test10_planar_memory_punched_height_plates`

Its first coupon should be a true-pitch 5×5 stack with four selector planes and a
bottom stop, not a full display. Test all five heights, adjacent height extremes,
checkerboards, repeated insertion, follower-edge catching, plate deflection and
load.

If that works, the next stage should test a removable 10×10 cartridge and measure
actual insertion/swap/reset time.

## Decision criterion

This direction is worth continuing only if it demonstrates a credible path to:

- reliable five-level decoding at 5.08 mm pitch;
- passive load support;
- low-cost planar media;
- a cartridge exchange comfortably inside the 30 s map-change budget;
- and a plausible method to write/rewrite pattern media without recreating the
  original 6400-actuator cost problem.
