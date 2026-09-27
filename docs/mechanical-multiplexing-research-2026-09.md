# Cross-disciplinary mechanical multiplexing research — September 2026

This document records the results of the second broad mechanism survey. It is a
research input, not a validated architecture. The detailed hypotheses live in
[research-backlog.md](research-backlog.md).

## Summary

The survey looked across historical and modern mechanism families including
Jacquard/textile selection, horology, mechanical calculators, printers and
coding drums, compliant mechanisms, tendon/cable systems and mechanical
multiplexing.

The recurring useful idea is to stop treating the cell actuator as one indivisible
component. The strongest mechanism families separate:

1. **selection/addressing** — decide which cells respond;
2. **power delivery** — provide motion/energy to many cells;
3. **height/state memory** — preserve the programmed state;
4. **load support** — hold miniatures without powered holding;
5. **reset/reprogramming** — preferably global or group-parallel.

## Relevant disciplines

- **Jacquard and textile machinery:** punched media and selector mechanisms can
  choose many outputs from shared machine motion.
- **Horology and intermittent-motion mechanisms:** Geneva wheels, escapements,
  detents and indexed sequencing provide repeatable mechanical states.
- **Mechanical calculators and automata:** coded drums, pinwheels and mechanical
  program media show how a small number of inputs can sequence many outputs.
- **Printer and office machinery:** travelling heads, impact pins and coded
  mechanical selection show high-cycle, repeated addressing.
- **Compliant mechanisms:** monolithic snap-through elements may provide passive
  state retention with few or no purchased cell-level parts.
- **Cable/tendon robotics:** remote power routing moves expensive actuators away
  from a dense output region.
- **Mechanical multiplexing:** shared shafts plus selectively engaged outputs
  separate the power source from output selection.

## Architecture families screened

| Family | Main advantage | Main concern |
|---|---|---|
| Jacquard-style selector | Broadcast selection; potentially very low actuator count | Dynamic reprogramming and tolerances |
| Global lift + bistable latch | One large motion source, passive cell memory | Tiny reliable latches at 5.08 mm pitch |
| Ratchet / escapement | Indexed height plus passive holding | Reset, wear and accumulated actuation force |
| Printed multistable cell | Very low purchased part count | Print variation, fatigue and creep |
| Geneva / coded drum | Self-indexed sequencing | May remain too serial |
| Shared shaft + clutch | One motor can power multiple outputs | Dense clutch/selector implementation |
| Cable / tendon bus | Remote actuation and flexible routing | Hysteresis, preload, routing and wear |
| Frequency-selective addressing | Broadcast signal can theoretically select outputs | Manufacturing variation and cross-coupling |
| Sliding selector matrix | Edge-driven mechanical row/column selection | Friction and combinatorial transaction count |
| Pinwheel / stepped drum | Compact mechanical sequencing | Arbitrary 2D programmability |

None of these was established as product-qualified. The useful output of the
survey is a broader library of selection, memory and power-routing mechanisms,
not a claim that one of them already satisfies the full product target.

## Cheap falsification experiments

The survey recommends small, mechanism-specific coupons before any full-scale
build:

- a 5×5 Jacquard/selector plate with several adversarial patterns;
- a 2×2 or 3×2 global-lift/bistable-latch coupon;
- a single ratchet cell followed by a 1×5 shared-drive row;
- a parameter sweep of printed snap-through elements;
- a small Geneva/indexer under realistic speed and load;
- a four-output shared-shaft/clutch demonstrator;
- a five-output cable/tendon bus.

These experiments should record force, displacement error, cross-talk, missed
states, reset behavior, wear and print-to-print variation.

## Interpretation

The most interesting families are those that move complexity away from purchased
cell-level hardware and into inexpensive repeated geometry. The survey therefore
supports continuing work on Jacquard-like broadcast selection, passive latching
and mechanical multiplexing, but it does not resolve the hardest combination:
**arbitrary 6400-cell programming, under 30 seconds, under the purchased-cost
limit, with sufficiently low failure probability.**

That unresolved combination motivates the next research direction:
[externalized mechanical memory and double-buffered programming](research-direction-2026-09.md).
