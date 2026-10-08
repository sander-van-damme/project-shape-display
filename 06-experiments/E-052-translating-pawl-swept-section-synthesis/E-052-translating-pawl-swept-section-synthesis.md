---
status: complete
builds-on: [E-050, Q-012, A-013]
---

# Translating pawl: swept-section synthesis

## Decision

Retain a **conditional two-dimensional latch section**, not a complete A-013
head. Including the pawl's withdrawn position changes the packing gate:
a bounded middle-error section can fit 5.08 mm, but the wide-error section
cannot with the searched web/pawl minima. Do not inherit E-050's section
strength estimates: this geometry uses different dimensions. Gripper capture,
release linkage, grounded guide, return/retention and cost remain unresolved.
No print or product selection follows.

Input `ad61288`. Evidence: deterministic rectangle geometry, interval envelopes
and an analytical packing bound; no CAD, calibrated fabrication prior, dynamics
or physical measurement. This is parameter synthesis within one translating-pawl
topology, not architecture discovery. The complete-system comparators remain
E-050's independent heads and E-051's shared elevator; neither gets a timing
improvement from this screen.

## Geometry, uncertainty and transitions

Run `python3 tools/curated-experiment-checks/E-052/pawl_sweep.py` (standard
library). Units mm. A vertical web of width `w` carries five rectangular teeth
at 10-mm spacing over 40-mm travel, protruding `r`. A rectangular pawl of lateral
length `L` slides toward the web to overlap a tooth by nominal `o`, with its top
at z=0. Its guide must ground the service load; the guide is not represented.
An external head is **assumed** to hold and vertically position the rack.

For every unequal old/new pair: lift off the old pawl → withdraw pawl → move
to just above the target seat → insert pawl → lower onto it. Unchanged cells
receive no release command. Seated height references each actual tooth, so
manufacturing error can change terrain height; accurate output heights are not
established. Tooth/pawl boundary contact is allowed only as zero-area support
contact; positive-area overlap is interference. Swept rectangles test the whole
axis-aligned path, not discrete animation frames. Five teeth, all 20 moves,
both old/target transfer states and adverse lateral placements are checked.
Support overlap is checked geometrically; the head's load support is assumed,
not verified. No unintended-neighbor motion is predicted outside this ideal
isolated section.

Explicit competing bounds `e=0.15/0.35/0.60`, borrowing only E-050's magnitudes,
not asserting a calibrated transfer of its error model:

- Rack and pawl lateral placement each ±e/2; common bank placement ±e/2.
  Relative error ≤e; absolute swept-edge error ≤e. These include endpoint
  registration/repeatability within that envelope. No independent cell draws.
- Tooth origin differences relative to the seated tooth ≤e; actual vertical
  tooth/pawl thickness no greater than nominal+e; unload lift error ±e.
- Required residual overlap 0.40; running clearance 0.10. Both are screening
  choices, not qualified FDM limits. Rectangles assume planar parallel faces;
  angular misalignment, local bow, edge rounding, lateral dimension/shape errors
  beyond the placement envelope, wear and deflection remain model discrepancy.

The common bank bound can fail an entire row. There is no inferred yield,
probability or process capability. Roughness/friction, PLA anisotropy, creep,
fatigue, guide stiffness and first-layer effects need separate evidence before
these ideal sections can establish feasibility.

## Search and independent bound

Each error scenario enumerates 972 sections: web 1.6/2.0/2.4; reach and pawl
length each 0.8/1.2/1.6; overlap 0.6/0.9/1.2; tooth and pawl thickness each
1/2; unload lift 0.3/0.6/1.0. No random seed. Early rejection checks pitch,
web collision, overlap, unload and retracted clearance; survivors undergo swept
checks. Source prints nonexclusive rejection counts and representative survivors;
reproducible output is not retained.

| Relative error bound | Grid survivors | Continuous minimum swept width | Geometric disposition |
|---|---:|---:|---|
| 0.15 | 252/972 | 3.85 | Section survives |
| 0.35 | 0/972 | 4.85 | Between-grid witness survives |
| 0.60 | 0/972 | 6.10 | Exceeds pitch |

The middle grid miss is **not rejection**. With clearance `c=0.10`,
stroke `s=o+e+c`, left bank margin `e+c`, the withdrawn pawl gives total
width `W=w+r+L+3e+2c`. Engagement requires `o≥0.40+e` and
`r≥o+e+c`; `L≥0.40` is also necessary. With the chosen minima `w≥1.6`,
`L≥0.8`, `r≥0.8`, the exact packing lower bound is
`W≥2.6+3e+max(0.8,0.50+2e)`. For these scenarios this is `3.10+5e`.
Thus **e≤0.396 mm** is necessary for this packaging class. It is not a
universal translating-pawl limit: narrower structural parts, reduced margins,
out-of-plane/staggered supports or a different retraction path change it.
The wide bound's 6.10-mm calculation even allows reach 1.70 beyond the grid;
expanding reach alone cannot rescue the pitch failure.

An interior middle-bound witness uses web 1.60, reach 1.24, pawl length 0.80,
overlap 0.77, tooth/pawl thickness 2.0 and unload 0.47. It requires **4.89 mm
swept width**, **1.22 mm withdrawal**, retains **0.42 mm overlap**, and has
0.12 mm minimum web/unload clearance. These margins are modest and conditional
on the explicit bounds. The remaining 0.19 mm across pitch does **not** house a
proven guide, return, release link or gripper. Their possible placement in the
third dimension requires actual assembly synthesis. All 6,400 cells need that
hardware; E-050's ≥19,200 interfaces and full-system cost gate still apply.

## Verification and next discriminator

Self-review: independent packing inequalities expose the grid-resolution miss;
continuous equality witnesses are replayed by the swept evaluator. Cases at
0.395 and 0.397 straddle the analytical threshold. Checks also include boundary
contact, a mid-path collision missed by endpoints, inadequate unloading, and an
oversized-tooth/pawl pair that collides with an adjacent tooth. Axis-aligned
swept unions require no time-step convergence; curved/rotating geometry is
outside the model. This is not an independent engineering review.

Next useful work must implement the missing guide/retention and head coupling
with a complete channel BOM, or change topology to escape the identified width
penalty. Do not spend another campaign refining this grid or nominal timing.
A 1.22-mm release stroke and 0.47-mm unload are real additional operations:
the independent-head contact allowance and shared-elevator event dwell must
include their actuation, seating and support proof. No actuator speed or timing
pass is inferred. Reopen the wide-error embodiment only with changed packaging
or evidence supporting smaller bounds; preserve alternative architecture search.
