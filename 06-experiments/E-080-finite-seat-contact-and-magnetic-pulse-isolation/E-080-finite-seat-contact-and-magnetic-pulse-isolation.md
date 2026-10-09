---
status: complete
builds-on: [E-075, E-079]
---

# A compliant magnetic seat must be checked under signed pulse histories

**Passive seating alone does not establish magnetic command isolation.** The
finite-contact sweep crosses the detent saddle in 147/216 bounded cases;
fixed positive-only and signed pulse histories reproduce two failures. Retain
noncrossing cases only as conditional model comparators, not accepted selectors.

Finite-contact investigation of A-016's signed dipole flag, continuing E-075
instead of tuning E-079's narrow mechanical ramp. This is a contact-model
refinement within one topology, not a new architecture family. Input main `c0292aa`.
Reproduce with `python3 tools/curated-experiment-checks/E-080/finite_seat.py`
(Python, NumPy and a C++17 compiler). Deterministic bounded ODE scenarios; no seed, sourced
manufacturing prior, field solution, printable CAD or physical measurements.

## Finite seat and energy accounting

Retain E-075's dimensionless angular coordinate q, 60-degree stroke beta,
time tau, detent `V=q²(1−q)²/2`, and signed dipole torque
`a*u*cos(beta*(q−1/2))`. Here a is torque relative to detent stiffness, not
coil current or ampere-turns. The two wells lie at q=0 and q=1. Stop on first
crossing of q=0.5: this tests escape from the original command basin, **not**
completed seating or correct cam engagement.

A point on a rotor of radius R meets a stop plane through its position at q=b,
with the plane normal tangent to the circular trajectory there. For q<b, normalized normal penetration is
`p=−sin(beta*(q−b))/beta`, and contact Jacobian is
`J=cos(beta*(q−b))`. Else contact is absent. A small rounded nose with its
radius incorporated into the plane position has this same center penetration;
contact stress and deformation shape are not solved. The force law assumes
normal compliance concentrated at the seat, not distributed rotor bending.

Define normal stiffness ratio `K=k_normal*R²/k_angular`. Contact potential is
`U_c=K*p²/2`, in the same energy units as V. Generalized seat force is
`F_c=K*p*(1+alpha*max(−q_dot*J,0))*J` during contact. The assumed dashpot acts
only on compression and smoothly vanishes at zero penetration; unloading
returns elastic energy. This explicit hypothetical law has no tensile force
or instantaneous velocity deletion. Alpha is an inverse dimensionless velocity
coefficient, **not** a restitution or damping ratio and not a material property
estimate. The original ideal e=0 impact seat is not a finite-K member of this
law.

The equation is `q_ddot=a*u*cos(beta*(q−1/2))−V'(q)−2*zeta*q_dot+F_c`.
Contact damping removes `alpha*K*p*(q_dot*J)²` during compression, and bulk
damping removes `2*zeta*q_dot²`. The total energy includes U_c; the seat can
return stored energy on unloading but cannot generate it. This distinguishes
compliant rebound from an artificial restitution reset.

The initial condition is the no-field equilibrium, found by force balance.
For b>0 it includes finite preload/compression against the detent. For b≤0 it
is q=0 with zero contact load. Symmetric reset uses the mirrored seat at 1−b
and reversed torque. The simulation stops before that seat, so reset symmetry
is a force-law check, not a complete two-stop geometry or reset qualification.

## Generator and evidence boundary

Cross K={10,100,1000}, alpha={0,10,100}, b={−0.02,0,+0.02},
zeta={0.02,0.10}, and half-drive fraction f={0.80,0.95}, with two histories:
positive drive on outward motion and zero on return; or positive on outward
motion and negative on return. The latter represents signed set/reset
half-selection. Both are adversarial waveform generators, not a proposed scan
schedule. Fixed-time replay establishes that selected counterexamples do not
need local velocity feedback. Neither generator exhausts possible waveforms.

Fractions use the bare-well lossless constant-step threshold
`a_step=max V(q)/W(q)=0.07930615`, where
`W(q)=[sin(beta*(q−1/2))+sin(beta/2)]/beta`. Nonzero b changes the initial
state and therefore need not preserve that single-step threshold. The f label
is a shared reference, not a claim that every offset case has the same margin.
All parameter choices are epistemic bounds. For R=1 mm, |b|=0.02 corresponds
to 1.2 degrees or about 0.0209 mm tangential location error. This is a tight
illustration, not a qualified X1C process bound; larger relative errors remain
uncovered. K and damping may shift coherently across a strip. Counts are not
independent-cell samples, probabilities or full-board yield.

## Independent impact limit

For an isolated flat seat, no detent or bulk damping, incoming normal speed
v0>0 and compression delta, `delta_ddot=−K*delta*(1+alpha*delta_dot)`.
Integrating `v/(1+alpha*v) dv=−K*delta ddelta` through compression and returning
all remaining spring energy on unloading gives
`e²=2*(x−ln(1+x))/x²`, x=alpha*v0. Its alpha=0 limit is e=1.
K cancels: within this law a stiffer seat shortens contact and reduces
penetration, but does not by itself lower the impact restitution. Also
`e→1` as impact speed approaches zero for every finite alpha. A single fixed
e=0 or e=0.5 cannot describe this contact over all impact speeds.

At alpha=100, e is 0.78339 for v0=0.01 and 0.38993 for v0=0.10.
Six holdouts at K=1000, alpha={0,10,100} and v0={0.01,0.10} compare this
independent flat-impact limit with the curved-seat ODE including its detent.
Maximum absolute discrepancy is <0.00016 at step 0.00005. This checks the
implemented contact response in a short-impact regime; it does not validate
the assumed material law or small-speed extrapolation.

The nominal static selected-drive threshold is
`max V'(q)/cos(beta*(q−1/2))=0.10094848` on 0≤q≤0.5. Two exactly additive
half inputs at f=0.80 give a=0.12688984, above that threshold. A check at
K=1000, alpha=100, b=0.02, zeta=0.10 reaches the saddle at tau=4.88375 with
that constant selected drive. This separates nominal selected-force sufficiency
from history isolation; it is not a finite-field/current margin or a physical
switching time. Field spread, dipole variation and detent asymmetry would
further alter the ratio.

## Bounded pulse sweep

The 216 cases run to tau=120 or first saddle crossing, with RK4 steps 0.0025
and 0.00125. All 216 crossing/noncrossing classifications agree. A compiled
C++ runner accelerates this specific ensemble; its extrema and crossing times
are checked against the separately implemented NumPy runner on two 15-tau
holdouts before the sweep. Build artifacts and JSON output are transient.

| Compression coefficient alpha | Positive-only crossings / 36 | Signed crossings / 36 |
|---|---:|---:|
| 0 | 36 | 36 |
| 10 | 27 | 36 |
| 100 | 5 | 7 |

There are 11 signed-only failures, and no positive-only failures in the paired
population. The 69 noncrossing cases are finite-horizon outcomes for these two
generators, not arbitrary-pulse isolation certificates. The largest contact
excursion is 0.07649 stroke, within the positive-J local branch of the actual
sine contact geometry. At R=1 mm this is about 0.080 mm normal penetration;
whether such compliance is realizable without damaging the stop is unproved.

Two fixed-waveform witnesses have K=1000, b=0 and zeta=0.02:

- Positive-only, alpha=10, f=0.80: u changes at tau
  0/+1, 4.3025/0, 6.3425/+1, 10.5925/0, 13.1375/+1.
- Signed, alpha=100, f=0.95: u changes at tau
  0/+1, 5.1975/−1, 6.885/+1.

The inputs remain at their last value after the final edge. Three positive
pulses defeat the first finite seat; one positive/negative/positive sequence
defeats the second. These are admissible single-site force histories, not
proof that a particular full-board scheduler generates them. A scheduler may
exclude them only with an explicit waveform and mechanical-parameter bound.


| Replay step | Positive-only saddle time | Signed saddle time |
|---|---:|---:|
| 0.00125 | 18.56000 | 18.21250 |
| 0.000625 | 18.55813 | 18.25625 |
| 0.0003125 | 18.55813 | 18.25219 |
| 0.00015625 | 18.55797 | 18.25063 |

The first two signed replay times differed by 0.04375, so population
classification agreement was insufficient timing evidence. The final
refinement changes are 0.00015625 and 0.0015625. Crossing is stable; quote
only about tau=18.56/18.25, without converting to seconds. Final peak seat
forces are 6.5345/20.7565 in generalized normalized units; their last changes
are <0.00006/<0.013. These are numerical responses, not contact-strength bounds.
Both fixed waveforms also agree between C++ and Python at step 0.00125.

## Decision and verification boundary

Reject the argument that adding a hard or strongly damped passive seat, without
a bounded constitutive law and pulse schedule, resolves E-075's isolation gate.
This result does **not** reject all seated magnetic selectors or demonstrate a
manufactured failure rate. Keep the noncrossing cases as conditional references;
stop refining assumed restitution/current alone. A reopening input must be a
mechanically realizable detent/stop and bounded signed scheduler, or a positive
blocking topology that removes the pumping path. More arbitrary pulse counts
without those inputs have low decision value.

The next campaign discrimination is a finite detent/stop/return-circuit package
and its command schedule, checked against the mechanical comparator's complete
retention/return inventory and strip scan budget. Use this contact source to
challenge that package; do not transfer a guessed K, alpha or zeta to PLA.
Actual flux nonuniformity, rotor inertia, detent geometry and stiffness, wear,
creep, guide friction, stop stress, cam readback and recovery remain unresolved.
No fabrication request follows: there is not yet a representative packed
assembly whose calibration would decide between complete machines. Neither
magnetic nor mechanical route earns a replacement or hardware qualification.

Self-review, not external validation: sine-geometry energy derivative, exact
magnetic work, unilateral/passive contact, zero-damping energy conservation,
mirrored reset force law, no-field preload equilibrium and nominal selected
crossing. An independent trapezoidal dissipation budget has residuals
6.41e-7 / 1.54e-7 / 3.57e-8 energy units at steps 0.001 / 0.0005 / 0.00025.
The independent flat-impact bound and six curved-impact holdouts are described
above. `--check` runs these short model checks; the default command also emits
the full population, two-step classification comparison and four-step fixed
replays. Discretization evidence does not validate material or field assumptions.
