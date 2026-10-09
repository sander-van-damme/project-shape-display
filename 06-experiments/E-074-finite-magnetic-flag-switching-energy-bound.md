---
status: complete
builds-on: [A-016, E-065]
---

# Finite reluctance flags need an energy gate as well as a static threshold

**Retain finite switching dynamics as a campaign gate.** For the ideal
soft-armature variant below, 31/48 bounded scenarios have a quasistatic selection
window, but only 20 retain a window when the half-selected flag may respond
without damping to one sufficiently long pulse. The 11 extra failures show why
an amplitude-only threshold is insufficient. These counts are chosen scenarios,
not process yield, field-solver results or fabricated switching evidence.

Input main `bc4126d`; reproduce with
`python3 tools/curated-experiment-checks/E-074/flag_barrier.py`.
The complete population, bounds and rejection windows are emitted. Deterministic
standard-library scalar optimization, 100 golden-section iterations; no random
seed. Source is retained; generated output is not.

## Mutation and physical boundary

This is a **guided reluctance/soft-armature mutation** of A-016's original
permanent-magnet torque flag. Two command windings add magnetomotive force
at a local gap; a double-well mechanical detent stores position after the pulse.
Local cam energy is routed by the resulting flag; magnetic force is not asked
to lift a miniature. Pole return geometry, leakage, saturation, winding volume,
actual detent and cam interface remain unconstructed. Results must not be
transferred numerically to the permanent-magnet torque architecture.

Let x travel from 0 to s=0.2 mm, initial gap g=0.3/0.5/1.0 mm. Assume
`U(x)=k x²(s−x)²/(2s²)` with k=0.1 N/mm, a deliberately selected double-well
potential whose small-motion well stiffness is k. It is not an FDM spring
prediction. Final gaps remain positive. One ideal air gap with 1-mm² pole area
and no leakage gives `F(x)=a/(g−x)²`, where
`a=mu0 Area (NI)²/2` with SI conversion. The source handles N/mm consistently.
No claim about achievable flux, required voltage or coil heating follows.

**A single soft pole cannot reset by reversing current:** attraction is
proportional to (NI)². A second opposed pole or a mechanically redirected force
path is necessary. The symmetric calculation can apply to an opposite pole
only when its full geometry, wiring and isolation are counted. A permanent-
magnet torque flag can reverse with field polarity but requires a different
signed torque/potential model. This distinction is a topology gate, not a
minor parameter change.

## Two independent switching limits

For quasistatic motion under any nonnegative damping, the forward force must
overcome the largest restoring-force/gap combination:

`a_static = max[U'(x)(g−x)²], 0<x<s/2`.

For a lossless flag starting at rest at x=0 under a constant-current step,
magnetic work is `a[1/(g−x)−1/g]`. It can cross the entire mechanical barrier
when that work exceeds U(x) everywhere:

`a_energy = max[k g x(s−x)²(g−x)/(2s²)], 0<x<s`.

This is the limiting **single sustained pulse from rest**, not a finite-pulse
switch time or proof of repeat-pulse immunity. Equality can take arbitrarily
long; comparisons use strict windows. Real damping, inertia, current rise/fall,
residual motion and pulse timing can change outcomes. Repeated half-select pulses
can pump energy; surviving this screen does not resolve that campaign task.

Both maximands have strictly concave logarithms on their positive intervals,
so the one-dimensional maximum is unique. Nominal energy/static ampere-turn
ratios are **0.8978/0.8910/0.8847** for g=0.3/0.5/1.0 mm. Thus an undamped flag
can cross with about 10–12% less magnetomotive force than its quasistatic
threshold in this model. This is not an observed error rate.

## Bounded selection comparison

Cross g with gap error ±0.025/0.050 mm; k spread ±15/30%; current error ±5/15%;
and parasitic contribution 0/0.06 of one nominal input. These are epistemic
scenarios, not sourced manufacturing or magnetic priors. Fix s and pole area;
variation of either remains additional uncertainty. Positive gap/k monotonicity
makes box corners exact for those two bounds. Common current/gap/material
errors apply coherently to banks; they are not averaged over 6,400 cells.

Two selected windings each deliver at least I(1−e). The adverse half-selected
site sees I(1+e+leakage). In nominal ampere-turn units per winding, require:

`I > sqrt(2 a_static,max/(mu0 Area)) / [2(1−e)]`

`I < sqrt(2 a_energy,min/(mu0 Area)) / (1+e+leakage)`.

The previous quasistatic-only comparison substitutes a_static,min in the upper
bound. Example: g=0.3 mm, gap error 0.025 mm, k error 15%, current error 15%,
zero parasitic contribution admits **9.998<I<10.519 AT** quasistatically.
The lossless half-select upper bound is **9.458 AT**, leaving no window.
Increasing current cannot repair the overlap. This is a new failure of a
specified finite-potential model, not a new rejection of E-065's air-core
geometry or proof that every guided magnetic flag fails.

## Decision and next discriminator

Stop accepting scalar static switching windows as adequate isolation evidence.
Retain the 20 window-positive scenarios solely as inputs to finite topology
synthesis. Compare a two-pole soft-armature reset path, a signed permanent-
magnet torque flag, and mechanical two-input coincidence. First establish
complete set/reset/isolation and a packed cam interface; then bound repeated
half-select energy using inertia/damping scenarios and adversarial pulse timing.
No full array driver count, cost or speed improvement follows yet; opposite-pole
reset hardware must stay inside the product boundary. No fabrication request.

Verification is self-review: an independent dense grid bounds the optimized
static maximum at two resolutions; energy/work equality and force equality
hold at the energy saddle; k scaling and unit conversion pass. At large gap,
the calculation recovers independent constant-force quartic limits
`F_static=k s/(6 sqrt(3))` and `F_energy=2 k s/27`. These checks establish
internal model consistency, not actual magnetic fields, switching reliability
or printed-detent behavior.
