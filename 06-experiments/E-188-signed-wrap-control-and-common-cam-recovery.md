---
status: complete
builds-on: [E-187, E-163, E-147, E-185, E-140, E-085]
---

# Two controlled wrap ends change reversal; energy recovery still owes selection

**Retain two-end wrap control as a distinct conditional lead; stop a common rigid
recovery cam as an independent branch controller.** Recovery reduces command energy
in the E-187 spring model, but does not remove independent timing or source-loss
isolation. Two-end wrap control has a credible signed reaction topology absent from
the fixed-tail comparator; its loaded release, contact initiation and arrest remain
unproved. No complete machine, purchased actuator or printing is accepted.

Input main `239e958`; LAB-309. Reproduce with Python 3 standard library:

```
python3 tools/curated-experiment-checks/E-188/control.py
```

Evidence: primary-source topology, analytical band equilibrium, imposed planar
curved-rod energy scenarios, quasi-static cam work integration and conditional
stopping bounds; **self-review**. No generated assembly/contact simulation, calibrated
process prior, physical measurement or independent validation. JSON is disposable.

## Search and causal alternatives

Industrial wrap-clutch documentation and bidirectional-clutch patent search yielded
a material distinction: **both ends exchange control and load-reaction roles**.
Repository wrap searches found E-163 and E-187, without this explicit topology.
Energy-recovery inversion is a separate search axis, but recombines E-187/E-147;
it is not a new physical principle. Two local search moves do not establish saturation.

Primary sources checked 2026-10-11:

- [Warner PSI description](https://www.warnerelectric.com/products/electromagnetic-clutch/wrap-spring-clutch-and-brake/wrap-spring-clutch-and-brake/psi)
  distinguishes start-stop from overrunning behavior. Its released clutch permits
  forward load motion; it does not supply a bilateral ground brake.
- [Warner CB service manual, pp.3–7](https://www.warnerelectric.com/-/media/Project/Altramotion/shared/files/Literature/brand/warner-electric/service-manuals/p-2026-we.pdf)
  identifies clutch, brake, anti-backup and anti-overrun springs, with adjusted
  collar overtravel. Reversing input after removing anti-overrun is not a demonstrated
  four-quadrant clutch/brake cycle.
- [WO2024011096A1, description/Figs.2,6,7](https://patents.google.com/patent/WO2024011096A1/en)
  describes a single wrap spring with two tang blocks and seats on the output frame.
  Rotation seats one block; reversing exchanges their roles. Actuation separates
  the spring ends to expand it, magnetically or through axial linkage/bearings.
  Its brake embodiment couples to a continuously resisted brake rotor. These are
  disclosed mechanisms, not verified miniature performance or a patent/legal opinion.
- [Harvard capstan demonstration](https://sciencedemonstrations.fas.harvard.edu/presentations/rope-friction-around-pole)
  supports the flexible-band tension law; its rope friction is not a PLA/wire prior.

All machine hypotheses spatially index reusable heads to 6,400 resident parked
supports at 5.08-mm tops. A head captures before releasing a stop, moves through
40 mm, reseats and proves actual top/support before withdrawing. Failed proof
retains capture. Regional isolation requires unselected stops to stay engaged;
shared-frame disturbance remains unquantified.

| Combination | Motion, command and ground path | Unresolved obligations |
|---|---|---|
| Conventional one-end wrap | Common rotary source → wrap → captured rack. Stopped collar controls wrapping. Separate grounded brake/anti-overrun supports stopping. | Fixed handedness, collar reset/impact, loaded lowering and opposite torque. The clutch alone is not retention. |
| Two-end wrap clutch plus local brake | Output frame carries two opposed tang seats. Tight-side seat carries load; either slack-side block can move toward its seat to expand the coil. Released drive and engaged local brake exchange support. | Both tang linkages/returns, rotating-force transfer, two torque interfaces, crossover, source isolation and dissipative brake. Two-end control alone does not merge clutch and brake. |
| Two-end wrap brake with independent motor | Spring couples output to a permanently resisted brake rotor on loss of opening command. Motor controls signed motion; powered tang separation releases brake. | Head motor/control plus tang actuator, return, brake rotor/pad, frame/bearings. Could reduce brake command force; does not remove drive cost. |
| Shared cam recovering E-187 springs | Source/flywheel turns a cam; captive followers open and close pad commands, returning spring work to the shaft. | Common phase cannot supply arbitrary per-head dwell. Added clutches, latches or independently phased cams must be charged and costed. |
| Direct motor control | E-185 independently driven setter plus grounded arrest and resident stops. | Motor, controller, return/proof and arrest. Remains the control; no new BOM pass. |

## Signed reactions: gain is not a loaded-release force

For a flexible band of wrap theta, radius R, incipient slip and friction mu:

```
G = exp(mu theta)
Tslack = |tau| / [R (G−1)]; Ttight = G Tslack
tau = ±R (Ttight−Tslack)
```

At tau=.002 N m (1 N through a 2-mm pinion), R=3 mm, three turns:

| mu scenario | Gain | Slack / tight tension |
|---|---:|---:|
| .05 | 2.566 | .426 / 1.092 N |
| .10 | 6.586 | .119 / .786 N |
| .20 | 43.376 | .0157 / .682 N |

A fixed physical tail swaps from slack to tight on reversal; required reaction
multiplies by G. The two-seat topology instead permits the opposite seat to carry
the tight reaction while the other block controls expansion. Seat reactions still
sum to the transmitted torque, and a free tail does not hold. Force scales linearly
with load: multiply by ten at 10 N. As mu approaches zero, required preload diverges.

These are **band equilibrium limits**, not wire-spring disengagement predictions.
They omit interference/bending normal force, tang constraint, contact peeling,
hysteresis and loaded partial release. In particular, .119 N cannot be assigned as
a solenoid specification. E-129's released-overhaul failure and E-140's distinction
between static holding and dynamic arrest remain relevant.

## Opening travel and tolerance versus stored elastic work

Use an inextensible planar curved-rod **trial shape**, constant radius along its
length; it approximates uncoiling only. Nominal hub radius is 3 mm, natural inner
radius hub−i, round rod diameter d, initial angle theta0=6pi and end reaction radius
3.5 mm. Let Rf be natural centerline radius and alpha the relative end opening:

```
L=Rf theta0; Ropen=Rf theta0/(theta0−alpha)
I=pi d^4/64; U(alpha)=E I alpha²/(2 Rf theta0)
one-end arc = .0035 alpha
trial outer-fiber stress = E d/2 |1/Ropen−1/Rf|
```

The imposed shape has no tang bends, helical torsion, hub peeling or friction work.
Its unloaded force dU/dalpha divided by 3.5 mm is **not an upper bound** on loaded
release. Stress is a model diagnostic, not an elastic-strength or fatigue acceptance.
The code subtracts initial interference energy; a loose coil starts at its natural
radius and has no earned engagement. Splitting motion between both ends can divide
the arc, but does not remove relative opening or elastic work.

Hub radius and natural coil radius each vary by ±e. Enumerate four corners, including
coherent shifts and opposite errors; demand .05-mm open radial clearance. These are
competing bounded scenarios, not distributions or independent-cell yield.
With i=.05 mm, minimum interference is i−2e: zero at e=.025 mm and **−.15 mm at
e=.10 mm**. No initial wrap contact is established in that adverse loose-coil case.
For contact geometry alone, resize i=max(.05,2e+.025) mm. This preserves at least
.025-mm interference, without proving frictional engagement or acceptable pressure.

| Radius bound on each part | Required i | One-end arc, d=.3 mm | Max incremental work / unloaded force, E=200 GPa | Max trial stress |
|---|---:|---:|---:|---:|
| 0 | .050 mm | 2.062 mm | .175 mJ / .229 N | 302 MPa |
| ±.025 mm | .075 mm | 3.580 mm | .696 mJ / .404 N | 534 MPa |
| ±.100 mm | .225 mm | 9.496 mm | 5.117 mJ / 1.158 N | 1,529 MPa |
| ±.200 mm | .425 mm | 16.978 mm | 16.952 mJ / 2.316 N | 3,058 MPa |

E=200 GPa and d=.3 mm are **wire-like assumptions**, not sourced spring stock or
allowables. E=3 GPa, d=.6 mm is a **polymer-like alternative**, not a qualified X1C
spring: at e=.10 mm its trial work is 1.070 mJ, arc 9.083 mm and stress 41.65 MPa;
at .20 mm stress is 82.93 MPa. Yield, anisotropy, tang concentration, layer geometry,
creep, fatigue and wear may invalidate the elastic shape long before operation.
No spring material is selected. Increased turns multiply opening travel/work,
but leave strain and force unchanged in this restricted family. E enters linearly;
d enters bending stiffness to the fourth power, with a smaller radius correction.

Thus E-187's nominal 59.36-mJ opening is not a universal cost of controlling
friction. A lower-energy topology is plausible, while manufacturing variation can
consume its travel/strain advantage. Smaller measured radius error, a larger hub,
matched purchased spring/hub, or changed end geometry are distinct reopening inputs.
No printing is justified by this model alone.

## What energy recovery can and cannot remove

Reuse E-187's exact pad potential U(q), S=1.4 mm and guide drag D=1 N. Prescribe a
quasi-static captive cam `q(phi)=S(1−cos(phi))/2` for one open/close cycle:

`tau_cam=U'(q) dq/dphi + D |dq/dphi|`.

Integration gives **59.36 mJ in, 56.56 mJ returned, 2.80 mJ net**. The ideal shaft
absorbs negative torque; cam/bearing losses, follower inertia and storage losses
are omitted. With returned-energy fraction eta=0/.5/.8/1 and four cycles/cell,
6,400-cell command input is **1,519.616 / 795.648 / 361.267 / 71.680 J/map**.
These are energy budgets, not electrical consumption or hardware efficiencies.

All 183 heads opening together still increase spring energy by **10.607 J** and
reach **6.366 N m** total quasi-static cam torque in this geometry. A flywheel or
four-quadrant source must supply/accept it. Counterphased followers can cancel
some torque only when their requested timing permits it; arbitrary maps include
all-opening cases. Cam speed changes power and inertia, not this work integral.

Identical rigid followers have q1=q2 at every phase. Requested states (0,S) have
minimum maximum error S/2=.7 mm for any common q. They cannot keep one head driven
after another finishes. This rejection is scoped to **identical direct followers**,
not all phased cams or programmable mechanical storage. Disconnecting one follower
requires a local latch/phase/return path; independent local cams require their own
coupling and reset. E-085's finite completion uncertainty remains. Recovered spring
energy also can keep operating after electrical loss; E-147 forbids treating it as
proof of a live command. No passive source-loss guarantee follows from lower net work.

## Board envelope, source loss and disposition

Even granting instantaneous start/stop, E-187's four .04-m passes at .3 m/s plus
.10 s/site and 6 s/map require **173 heads**, with <$1.445/head under $500 when
$250 is reserved elsewhere and every site purchase is free. Allocate an additional
0/5/10/20 ms per pass for all transitions and the head counts become
173/178/183/194, with modeled map times 29.433/29.520/29.567/29.540 s. These are
optimistic schedule allocations, not achieved arbitrary-map timing; acceleration,
short moves, reset, registration, proof, retry and settling must fit them. At 183
heads, $.02/site leaves <$0.667/head. There is no sourced wrap-head BOM.

A fail-engaged **drive clutch** can couple a column to a coasting source. It is
not a ground brake. A fail-engaged **brake clutch** needs a grounded dissipative
rotor and finite engagement. As a favorable separate bound, grant 3 N constant
braking force after a 0/5/20-ms delay, downward speed .3 m/s and 1-N gravity load.
Use translating mass 1/9.81 kg plus 1e−8 kg m² shaft inertia through a 2-mm pinion.
Total stopping travel is **2.350/4.779/14.222 mm** and brake heat
**7.049/9.479/18.922 mJ**. These are not accepted outage distances or wrap predictions.
They show why contact initiation and damping matter even if release work is small.
At braking force ≤load this constant-force model has no finite stop.

Per-head liabilities include spring/mandrel wear, two tang seats/blocks, release
linkage, actuator, return, bearing/ground reactions, dissipative interface, capture
and readback. Buying springs repeats H times; resident versions repeat 6,400 times
and lose the reusable-head cost advantage. 6,400 parked supports/guides/proof paths
remain in either case. Shared bias, source sag, cam jam and reader false acceptance
are common-cause faults, with no yield, assembly-time or life claim here.

**Decision:** retire direct identical-cam recovery as an independent controller;
retain recovery only as a power subsystem with counted independent couplings.
Do not size a wrap actuator from capstan gain or declare a bidirectional drive a
brake. Keep two-end wrap plus grounded dissipative rotor alongside direct motor
control as the next contact-level discriminator; it changes the reaction topology
and is not another E-187 pad sweep.

Next useful probe: build a finite two-end spring/mandrel/seat model with signed
loaded release, friction and free-input engagement, comparing tight and loose radius
bounds. Stop on missing initial contact, release jam, unsupported crossover or
unbounded coast; promote only with a continuous torque path and explicit return/
energy sink. Defer sourcing, detailed gears and printing until that result exists.
If the model cannot retain the low command advantage, switch to a different
architecture axis rather than repeatedly tuning this coil. No CEO boundary.

Checks: signed band torque balance and zero-friction limit; Euler contact-law
holdout errors 1.739/.1773/.01776% at 100/1,000/10,000 segments; four exact radial
corners; independent work quadrature; turn/strain scaling; exact cam energy ledger
versus 2,000/8,000/32,000-point quadrature (net-work residual 1.15e−9 to 4.50e−12 J);
two-head endpoint witness; signed braking energy conservation; strict integer head
schedule. These verify the reduced models, not the actual spring geometry or dynamics.
