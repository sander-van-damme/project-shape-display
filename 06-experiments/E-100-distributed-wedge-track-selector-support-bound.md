---
status: complete
builds-on: [E-061, E-062, E-099]
---

# Distributed ramp support trades rail bending for track shortening

**Do not grant rigid distributed support to the hydraulic coincidence rail.**
A sliding track carrying repeated ramps can lift grounded rail feet together,
but its accumulated friction force and axial elasticity consume the coincidence
window. Keep shallow, segmented tracks for finite geometry comparison; stop the
reference full-width 2×8-mm, 30° track under the stated bounds. This starts a
changed support/transmission investigation, not a qualified valve architecture.

Input main `185231c`. Reproduce with
`python3 tools/curated-experiment-checks/E-100/wedge_support.py`.
Evidence: quasistatic statics, work and axial-elastic calculations with explicit
scenario bounds; self-review only. No contact geometry, sourced material/friction
priors, fatigue, physical measurements or hardware qualification. JSON output
is reproducible and not retained.

## Changed load path and bounded model

A ground-backed horizontal track has one rising ramp beneath each vertically
guided selector-rail foot. Translating the track lifts the feet/rail by 2.5 mm;
the ground bed carries their vertical load. The track transmits horizontal
force along its length, so it is not E-062's unsupported rail. The rail still
bends between feet. Follower preload keeps contact while valves are closed;
positive reset/return and crossing access require actual geometry next.
Separate vertical layers may route crossed inputs but have no established
stack height or pitch fit.

Grant a uniform track base area A=width×depth, a rigid bed/feet and isolated
simply supported rail spans of eight cells (40.64 mm). At 80 cells, eleven feet
receive eight-cell loads internally and half that at the two ends. These loads
sum to E-062's **95.12389 N**: 80 times (1.089049-N selected endpoint force plus
.1-N follower preload). Symmetric shoe-force transfer is inherited only as a
model hypothesis. Imperfect heights can unload feet and invalidate those
support reactions. No support-load redistribution is modeled here.

The raising-force multiplier for ramp slope t=tan(angle), equal Coulomb friction
mu on inclined contact and flat lower bed, is

`K = (t+mu)/(1−mu*t) + mu`.

The first term follows the inclined contact force balance; the second is lower
bed friction under the same total vertical load. F=K×vertical load; required
horizontal travel is `2.5/t`. Forces from each downstream foot act in the track
back to the end drive. Integrating axial strain gives far-end displacement
`dx = sum(F_i*x_i)/(E*A)`; lost lift is `t*dx`. For these symmetric loads,
`dx = F*L/(2*E*A)`. Compression buckling, guide friction and distributed bed
compliance are excluded; there is no automatic positive return from this
raising-only model. Friction can lock the track on reset.

Enumerate angle 15/30/45°, mu=0/.1/.3/.5, effective axial E=500/1500/3000 MPa,
base width=2/4 mm, depth=4/8/12 mm, and one/two separately driven equal segments:
**432 parameter cases in one topology**. Modulus/friction are competing bounds,
not X1C PLA accuracy or measured material priors. Full-line modulus and friction
are correlated, and the selected row's loads accumulate. No cell independence,
probability or yield is inferred. Wider bases/deeper stacks are only allocations;
actual crossed-rail/manifold/support packaging may exclude them.

The comparison ceiling is **0.1 mm**, optimistically assigning the entire
E-062 non-rail share of its .2-mm load-dependent allowance to track shortening.
E-062 still charges rail bending separately; stem/contact/bed lost motion cannot
also receive that same .1 mm. Of the parameter cases, 144 meet this scalar
ceiling; none is accepted geometry or a robust full mechanism.

## Calculated tradeoff

For E=1500 MPa and 2×8-mm base:

| Angle | Friction mu | Track travel mm | Whole-line force N | Whole-line lost lift mm | Half-line lost lift mm |
|---:|---:|---:|---:|---:|---:|
| 15° | .1 | 9.330 | 45.477 | .103170 | .025793 |
| 15° | .3 | 9.330 | 87.285 | .198018 | .049505 |
| 30° | .1 | 4.330 | 77.893 | .380757 | .095189 |
| 30° | .3 | 4.330 | 129.478 | .632916 | .158229 |
| 45° | .1 | 2.500 | 125.775 | 1.064894 | .266224 |
| 45° | .3 | 2.500 | 205.196 | 1.737325 | .434331 |

Two equal isolated segments halve load and length, quartering shortening.
They require **320 independently driven inputs**, versus 160 full lines,
and **1,920** support contacts instead of 1,760. A mechanically synchronized
single actuator could change that count only with an explicit transmission,
stiffness and reset budget; synchronization is not free. Each segment retains
its full stroke. No timing or complete drive price is inferred.

The 30°/.1 full track needs at least **60.921 mm²** axial area at 1500 MPa to
meet .1-mm track loss; the half track needs 15.230 mm². The half-track reference
therefore leaves only **.004811 mm** of the allocated non-rail share for other
losses. The .06536-mm reference rail bending from E-062 remains additional.
A shallow 15° half-track has more travel and more loss to friction relative to
useful work, but materially more displacement margin. A .3 friction bound
changes the 30° split case from a favorable scalar bound to failure, while the
15° split case remains below .1 mm before omitted compliance.

At 30°/.1, a full line with only .1-N follower loads loses .032022 mm, compared
to .380757 mm when fully selected. This **state-dependent correlated error**
cannot be removed with one unloaded home calibration. If the valves fail to
open, loads will differ; the model predicts required-load inadequacy, not that
this exact deflection occurs on every stalled valve. A high-dwell cam or other
transmission could avoid this ramp sensitivity and deserves a changed finite
comparison rather than a thinner-track parameter sweep.

## Next discriminator and checks

Generate actual moving ramp/foot/ground-bed sections and crossed-input access
for the shallow segmented option, compared with distributed rotational lift
with positive dwell/reset. Include the E-061 floating beam's sliding ends,
1.1-mm possible stem travel, unintended half-select and both pressure directions.
A cam alternative must account for torque, shaft/bearing deformation, phase,
isolation and reset; a long tiny shaft is not an assumed solution. Reject on
packing, contact loss or consumed coincidence margin before fluid sealing work.
No manufacturing coupon, purchase or machine acceptance follows from this screen.

Virtual work at zero friction, positive dissipation, independent axial integral,
inverse stiffness and quarter-loss segmentation checks pass. This is algebraic
verification, not a discretization/convergence or independent physical validation
claim. Rail bending/shear, actual support-height correlation, bed compliance,
compression buckling, creep, wear, stick-slip, valve sealing and recovery remain
unresolved. The next model must restore them where they decide between survivors.
