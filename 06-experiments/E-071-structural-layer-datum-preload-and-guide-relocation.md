---
status: complete
builds-on: [E-070, E-069, A-022]
---

# Datum restraint trades lateral play for friction feedback

**Reject a simple short, sliding preload retrofit as a robust escape from
E-070. Retain longer datum spans only for a finite restraint/packing test.**
Preload is not a free removal of guide play: the offset fork force produces a
pitch moment, increased guide reaction increases friction, and friction increases
the required fork force. Two short guides can lose all seated sliding equilibria.
This is a scoped contact-model rejection, not a rejection of structural memory
or a finding about measured PLA friction. No printing or strength optimization.

Input main `68617ae`. Run
`python3 tools/curated-experiment-checks/E-071/datum_restraint.py`;
`--all` emits 90 bounded scenarios and rejection reasons. Standard library,
deterministic analytical inequalities and nominal finite box sweeps; no random
seed, solver mesh, physical measurements or calibrated material priors.

## Mechanisms and constructed geometry

Compare two changes to E-070's tight T guide:

1. **Local positive datum:** two 0.4-mm-tall pads fill the old left 0.20-mm
   guide gap and touch the flange. An opposing shoe pushes left at guide
   mid-height. Import the actual E-070 dog/fork/bore and construct the pads;
   they connect to the mount and remain beside the flange throughout the
   40-mm stroke, overtravel and failed-proof drop without nominal interference.
   The nominal envelope stays 5.00 × 4.95 mm. The shoe, spring, adjustment and
   actuator have **not** been packed; an ideal force source is used to derive
   necessary conditions before spending on their geometry.
2. **Separate rear bank guide:** a fixed common frame carries individual
   guide channels in a new rear lane. Even a minimum 0.8-mm neck, two 0.20-mm
   gaps, two 0.4-mm walls and a 0.15-mm relative-error reserve add 2.15 mm to
   the existing 4.95-mm dog/tongue depth: **7.10 mm > 5.08 mm**. Reject this
   side-by-side lane arrangement. It does not reject a vertically displaced
   common frame, shared walls, or a rearranged dog/tongue. A shared rigid moving
   guide cannot substitute for independent stage coordinates; neighboring
   parked columns may occupy different heights. A stationary frame still needs
   individual channels and clearance through all lower-stage offsets.

These are restraint/packing variations within A-022, not new architectures.

## Force model and independently derived limit

Use x horizontal, z vertical; take the left datum face as x=0 and guide center
as z=0. Generated geometry gives right shoe x=b=1.90 mm, assumed downward
payload W at the neck center d_w=0.95 mm, and fork vertical resultant V at
**d_v in [3.05,3.60] mm**, the actual dog/fork overlap interval. Pressure may
concentrate anywhere in that interval. Side force H acts at dog center height
`a=L/2+2.05 mm`. Its magnitude and sign are scenarios, not inferred motor data.

The left pads have nonnegative reactions N_l,N_u at z=−S/2,+S/2. Use
S=L−0.8 mm (inner pad edges) for the table; also test the more favorable S=L
(full outer span) before rejecting a short guide. These are ideal point-reaction
models, not elastic pressure predictions. The right shoe exerts preload −P.
All three sliding contacts share a Coulomb coefficient mu; vertical friction
opposes direction s=+1 upward, −1 downward. Quasistatic balance in N and mm:

```
N = N_l + N_u = P − H
V = W + s mu (2P − H)
M = d_v V − d_w W − s b mu P − a H
N_l = N/2 − M/S;  N_u = N/2 + M/S
```

Require P≥0 and both datum reactions≥0 for both travel directions. V can have
either sign; the bidirectional fork is idealized. Each inequality is affine in
P: intersect its allowed intervals analytically, without a preload grid. At
fixed P the expressions are multi-affine in the uncertain inputs; checking box
corners bounds their continuous intervals. No contact stability, elastic
stiffness or dynamic sticking is established by feasible reactions.

For upward travel with H=0 and W>0, a separate hand-derived necessary condition
at the adverse fork edge is

`P [S/2 − mu(2d_v−b)] ≥ (d_v−d_w) W`.

Thus **mu < S/10.6** is necessary. Even granting the entire guide length as S,
L=1.6/4.0 mm requires mu<0.151/0.377. At larger coefficients no positive preload
can maintain both datum contacts under this load path. Increasing the preload
worsens the feedback. This loss of the assumed seated mode may lead to rocking,
opposite-wall contact or sticking; the model does not predict which occurs.

## Sensitivity and full-board consequence

Enumerate L=1.6/4/8/12/20 mm; mu in [0,0.2], [0,0.4], or [0,0.6]; W in
[0,0.1], [0,1], or [0,10] N; and |H|≤0 or 0.2 N. **30/90 scenarios lack an
ideal common preload; 60 admit one.** Counts describe chosen bounds, not yield
or likelihood. W=10 N is a loaded-motion sensitivity, not a requirement that
all 6,400 cells move under the earlier stationary service load.

For W≤1 N, |H|≤0.2 N, mu≤0.6:

| Guide L | Minimum P | Maximum upward V | Maximum sliding friction |
|---|---:|---:|---:|
| 1.6 / 4 mm | no equilibrium | — | — |
| 8 mm | 8.505 N | 11.326 N | 10.326 N |
| 12 mm | 1.476 N | 2.891 N | 1.891 N |
| 20 mm | 0.607 N | 1.849 N | 0.849 N |

The minimum preload is marginal: at least one corner unloads a datum pad.
It is not an acceptable specified spring setting. Force margin, preload spread,
creep and datum distortion would need to fit the complete allowable interval.
Load reduction alone does not remove side-force burden: with W≤0.1 N the
12-mm minimum is still 0.950 N. With W≤10 N it rises to 11.331 N.

At the table's common adverse sliding corner, 80 simultaneous channels require
906/231/148 N upward for L=8/12/20 mm. Friction alone over a uniform 6,400-cell
40-mm move is 2,643/484/217 J, before gravity, rail motion and losses. These are
**conditional sustained-force scenarios**, not unavoidable device demands or
measured tails; a transient H need not persist through travel. A common material
or preload error can affect an entire bank. We do not average it down by sqrt(N).
A shared preload comb reduces separate purchased springs only if its individual
compliance and common-frame deformation are actually solved. Up to 19,200 stage
sites still need two datum pads and a preload contact (57,600 sliding patches),
plus restraint adjustment/assembly and existing dogs/catches. No bought cost or
<30-s machine claim follows from three shared layer drives.

## Decision limits and next discriminating result

E-070's e=0.15-mm aggregate geometric scenario remains uncalibrated. Nominal pad
sweeps do not propagate pad tilt, bore motion, free vertical dog play, rail bias,
wear or pad compression. Do not combine this nominal contact solution with
E-069 and announce a supported assembled machine. The y guide, yaw/roll,
three-layer connectors, actual bias source, actuator/readback and proof recovery
remain unresolved. Equal friction on all contacts is one model; unequal contact
coefficients or force-controlled low-friction guidance may change the ranking.
No X1C capability, spring life, guide strength or probability is asserted.

Stop the short preload retrofit and the separate rear lane. Bound the next
geometry investigation to **12/20-mm local datum guides versus a vertically
relocated shared frame**, with finite bias hardware and two-pad dimensional
mismatch. First prove that the actual bore stays within the rail bypass and dog
engagement envelope under allowed rotation and deformation; E-070's 0.04-mm
extra lateral-play allowance is not automatically available after datuming.
Count the longer neck/depth, guide friction and all repeated restraints. Reject
on unavoidable collision or no force/position margin before stacked FEA. If no
finite realization survives, conclude this campaign with scoped rejection;
otherwise proceed to stacked contacts and the complete-system discriminator.
No fabrication is decision-relevant while these geometric gaps remain.

Self-review: all force/moment residuals, frictionless closed form, independent
friction-feedback limit, zero-load limit, both travel directions, exact nominal
pad sweeps, and an off-grid 11.137-mm/0.43-friction interior holdout pass. This is
self-review and model verification, not independent hardware evidence. Generated
JSON is reproducible and not retained.
