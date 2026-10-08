---
status: complete
builds-on: [E-063, A-020]
---

# Corrugated pressure-cell sweep and retraction bound

**Retain A-020 only as a conditional micro-diaphragm route; stop the tested
sinusoidal bellows grid.** Forty-millimetre travel can be stored in a rolling
U-section without stretching its meridian, but pitch, repeated bending,
circumference change and manufacturing errors compete. An inverse geometric
bound finds a narrow route missed by the initial coarse parameter grid. It is
not an available component, printable diaphragm, complete mechanism or hardware
qualification. No fabrication is justified by this screen.

Input main `4118863`; E-064's previously allocated empty scaffold was recovered
from the abandoned pressure task. Reproduce with Python 3 and NumPy:
`python tools/curated-experiment-checks/E-064/pressure_cell.py --all`.
JSON output is reproducible and not retained. Source records exhaustive grids,
rejection reasons, inverse generator and numerical checks. No random sampling,
measured process priors, FEA, yield or fatigue-life estimate is claimed.

## Geometries and evidence class

Two materially different membrane motions are compared within A-020's common
pressure architecture: distributed corrugation unfolding and a translating
rolling fold. These change energy delivery geometry, not the unresolved local
selector. The mechanical rack A-013 and the global elevator A-016 remain simple
comparators: neither needs 6,400 pressure seals or a multi-kilonewton lid.

**Source:** [DiaCom's rolling-diaphragm theory](https://www.diacomcorp.co.uk/rolling-diaphragm-theory),
accessed 2026-10-08, describes pressure-supported piston/cylinder walls and a
semicircular convolution bearing membrane tension. It supports that load-path
principle only. The dimensions, strain limits, spring properties and tolerances
below are explicitly assumed scenarios; no supplier capability or material
property at our scale follows from the source.

**Sinusoidal synthesis:** the axisymmetric mid-surface is
`r=1.2+a cos(2πz/q)` mm. Generate 20/40/60 periods, compressed period
0.3/0.6/1 mm, amplitude 0.4/0.7/1 mm, and film thickness
0.025/0.05/0.1 mm: 81 cases. Increase period by `40/n` and solve amplitude to
preserve each period's meridian arclength. Match material points by arclength,
not cosine phase, when computing circumference change. Sample 41 stroke states;
check three adjacent periods for nonlocal skin proximity and the exact
maximum curvature `4π²a/q²`. This is a prescribed deformation path, not the
equilibrium shape under pressure. Its collapsed depths span 6–60 mm, with
40 mm added when extended; end flanges and guides are additional.

Twelve cases lack enough meridian length. All remaining 69 exceed a 10%
bending-strain scenario (`t/(2 radius)`); 51 also exceed a 20% hoop-cycle
scenario and two have sampled nonlocal skin overlap. Even the gentlest generated
compressed fold needs 19.7% nominal surface bending strain. Rejection counts
overlap. Stop this **sinusoidal grid**, not all corrugated or elastomer bellows.
A rounded fold, different wall thickness or a demonstrated larger cyclic strain
allowance changes the problem. The model does not impose constant circumference
as an unnoticed constraint: it reports the hoop deformation it requires.

**Rolling synthesis:** piston radius `rp`, hardware radial gap `g`, film
thickness `t`, cylinder wall `w`, and combined radial error `e` define midline
radii `ri=rp+t/2`, `ro=rp+g-t/2` and fold radius `(g-t)/2`.
The U has a straight outer leg from fixed clamp z=0 to zc, a semicircle below
zc, and an inner leg returning to the piston clamp z=x. A 1-mm end margin gives
`L=40+2+π radius` and `zc=(L+x-π radius)/2`. Therefore the meridian length
is invariant, both legs remain positive for `0≤x≤40`, and the fold moves 20 mm.
The executable checks 81 positions and 129 arc samples; radial extrema and
leg minima are also exact. A constant-length piston skirt long enough at x=0
sweeps to approximately **61 mm below the fixed clamp** at x=40. Top column,
latch, spring and flange envelopes remain additional.

Sleeves bound each cell independently, so neighboring 0/40-mm states have no
membrane bridge requiring the earlier 694% extension. The pitch inequality
covers sleeve outer envelopes through intermediate states. It does not check
clamp flanges, a return spring, pawl/reader packaging or lateral stability of
the long skirt. End joints and the three-dimensional seal remain undesigned.

## Inverse bound and manufacturing sensitivity

Let b be the permitted bending strain and h the permitted hoop expansion from
inner-wall to outer-wall circumference. They are competing design allowances,
not measured elastomer limits or allowable PLA strain. Under worst gap closure
for bending and worst gap opening for hoop cycling:

```
g >= t(1+1/b)+e
rp >= (g+e-t)/h-t/2
2(rp+g+w+e) <= 5.08 mm
```

Use both error signs as robust scenario requirements, not a claim that a single
part simultaneously has both signs. The inverse generator chooses the minimum
g and rp satisfying the first two, then tests pitch. It screens film
0.025/0.030/0.05/0.1 mm; walls 0.4/0.6 mm; e=0/0.05/0.15 mm;
b=5/10/20%; h=10/20/40%. The 216 inverse cases retain 57 under their own strain scenarios; 159 fail
pitch. These are different allowances, not 57 qualified designs. A separate
324-case fixed grid (rp=0.8/1.2/1.6 mm, g=0.15/0.25/0.3/0.35/0.4/0.6 mm,
t=0.025/0.05/0.1 mm, the same walls/errors) retains 0/2/71 at paired b,h
allowances of 5%,10% / 10%,20% / 20%,40%. The middle-envelope survivors both
need e=0. The inverse witness below demonstrates why that coarse grid must not
be mistaken for a family-wide impossibility proof.

The 0.030-mm case represents a +20% thickness bound
on nominal 0.025-mm film, not a statistical distribution.

For b=10%, h=20%, the exact necessary pitch condition simplifies to
`60.5t + 12e + w <= 2.54 mm`. At t=0.025, w=0.4 and e=0.05 mm:
`g=0.325`, `rp=1.7375`, required pitch **5.025 mm**. Only 0.055 mm diametric
margin remains, and both strain scenarios are active constraints. This inverse
witness is a deliberately marginal discriminator, not a robust recommendation.
With film 20% thicker, required pitch becomes **5.630 mm**, failing the product
pitch. At t=0.030 and w=0.4 the entire shared radial-error budget must be
≤0.02708 mm to preserve this particular strain envelope. With t=0.025 it is
≤0.05229 mm. These are *required tolerances*, not X1C capability claims.

Radial error includes correlated bore shrinkage, piston/bore size bias,
assembly eccentricity, roughness intrusion and local variation. Wall thickness,
warp, clamp distortion and tilt over the long skirt would consume additional
margin. A shared material/print bias can eliminate every site; an independent
cell-yield assumption is inappropriate. The 0.4-mm wall is a packing scenario,
not a pressure-qualified print. Baseline PLA printing applies to structural
parts; no thin elastomer molding process or film supply has been established.
Fatigue, creep, wear, leakage, hoop wrinkling and loss of positive pressure
support are unbounded. Larger strain allowances reopen geometries but require
different material evidence; they cannot be credited as free robustness.

## Return window and complete-board consequences

The diaphragm does not itself establish return force or controlled speed.
For spring `F0+kx`, use ±30% shared spring-force bounds, ±10% effective-area
bounds, drag D, hysteresis H, and upward payload L. Ignore favorable gravity
for descent:

```
P_raise >= [1.3(F0+40k)+D+H+L] / (0.9 A)
P_lower <= [0.7F0-D-H] / (1.1 A)
```

Convert N/mm² to kPa by multiplying by 1,000. A negative lower bound means
venting alone cannot guarantee return. Enumerate area 4/7/10 mm²;
F0=0.1/0.25/0.5 N; k=0.002/0.01/0.03 N/mm; D=0.02/0.1 N;
L=0.05/0.2/1 N; H=0/0.05/0.2 N; residual pressure 0.5/2 kPa and
pressure-cap scenarios 30/100/300 kPa. Of 2,916 combinations, 376 satisfy both
necessary windows; 2,250 fail raising and 1,134 fail return, with overlap.
These are scenario counts, not population probabilities or paired geometry
qualifications. The spring and hysteresis inputs have no calibrated link to
the generated skins.

For the inverse witness, A=π(1.9 mm)²=11.341 mm². With F0=0.25 N,
k=0.002 N/mm, D=0.02 N, H=0.05 N and L=0.2 N, required raising pressure is
**68.5 kPa**, and lowering must remain below **8.42 kPa**. A 100-kPa capability
and 2-kPa vent residual therefore have a conditional window. Raising preload
improves return but raises pump pressure and locked-cell reaction. The earlier
28.3-kPa pressure estimate omitted these terms and is not an operating point.

At 68.5 kPa the 406.4-mm-square lid sees approximately **11.3 kN** gross
pressure reaction. Nominal cap forces sum to about **4.97 kN**. Lid and cap
forces are separate free-body loads; do not add them as a net external force.
A 40-mm full-board stroke displaces **2.903 L**. Filling in 10 s requires
**17.4 L/min at operating chamber conditions**, or roughly 29.2 L/min free air
at a 101.3-kPa ambient pressure, before dead-volume pressurization and leaks.
Ideal differential-pressure work is about **199 J**; compressor input is higher.
A 10×10-cell, 50.8-mm-square sealed module still has about **177 N** gross
lid reaction at that pressure. Module framing/seals/relief and isolation hardware
are additional bought/printed parts and assembly.

Locks must retain **both upward and downward** force while pressure changes.
A conventional pawl permitting upward ratcheting does not isolate unchanged
cells. Use a bilateral ground latch as an explicit requirement; no geometry for
it is validated here. Pressure must unload the selected latch before release;
return speed needs a brake/governor and capture overlap. A puncture must leave
positive support engaged and stop/isolate the affected plenum. Releasing a latch
on pressure loss is unacceptable. The script verifies membrane kinematics and
necessary force windows, **not** those unresolved support-transfer transitions.

No <30-s claim follows: filling, exhausting, selection, pressure reversals,
proof of support, scanner time, settling and bounded retries remain unallocated.
A shared plenum pressures unchanged cells even during a local edit, so elastic
disturbance and common-fault exposure need frame analysis. E-065's restricted
magnetic margin also applies if A-020 inherits that selector. Pressure supply
does not solve addressing, readback false acceptance or release-channel cost.
At the E-063 $250 shared reserve, the $500 cap leaves only $0.03906/site for
all bought local parts; membrane/spring/latch/flag costs are unknown. No BOM
pass is claimed. Molded membranes need replaceable module access rather than
6,400 inaccessible seals, with tooling and inspection costs accounted separately.

## Verification, decision and reopening

Self-review checks the flat sine limit, unavailable arclength, independent
`L≤q+4a` bound, rolling length conservation, stroke endpoints and radial
containment, zero-stiffness force limits, and pressure-work/volume equality.
For a 40-period, 0.6-mm-period, 0.7-mm-amplitude, 0.025-mm-film witness,
129/257/513 meridian samples with 21/41/81 stroke states give hoop strain
0.250416 throughout and sampled nonlocal clearances 0.17877/0.17477/0.17318 mm.
Bend strain is 0.959545 analytically, decisively rejecting it independent of
sampling. Nonlocal proximity is a diagnostic (material separations below one
quarter-period are excluded); it is not a certified global contact solution.
No mesh convergence or pressure-shape validation is implied by these checks.

Do not deepen the rejected sine grid or procure pumps on its nominal pressure
calculation. Retain the rolling principle conditionally, with the inverse
pitch/strain bound as its reopening gate. A credible film/material process,
cyclic strain/hysteresis evidence and sleeve/latch/spring packaging must improve
that gate before fabrication. A nonaxisymmetric folded pouch could reduce hoop
cycling, but needs a different generated three-dimensional sweep and seal design;
it is an unexplored escape, not a screened survivor. Complete the campaign's
A-015 discriminator before allocating another detailed pressure study.
