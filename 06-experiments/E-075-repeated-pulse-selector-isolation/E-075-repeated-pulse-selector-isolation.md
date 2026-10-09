---
status: complete
builds-on: [E-074, A-016]
---

# Half-selection needs a mechanical boundary, not just a pulse threshold

**Require explicit seating/contact and pulse-history isolation before choosing
magnetic geometry.** Two separated positive half-select pulses can switch the
unstopped E-074 detent although a single sustained pulse of the same amplitude
cannot. A finite-angle permanent-magnet torque surrogate has the same failure.
This rejects pulse-amplitude-only acceptance of these embodiments, not magnetic
selection as a physical principle. An ideal inelastic seat changes the result;
its restitution, clearance and reset path are now decision-driving inputs.

Input main `e3fb785`. Reproduce with
`python3 tools/curated-experiment-checks/E-075/pulse_isolation.py`.
Source emits the full deterministic population and reproducible open-loop pulse
witnesses. No random seed, fabrication or external material/field priors. All
parameter ranges below are labelled hypothetical bounds, not X1C process data.

## Model and complete reset alternatives

Use q=x/s, dimensionless time tau=t sqrt(k/m), and
`V=q²(1−q)²/2`; equation `q''+2 zeta q'+V'(q)=u D(q)`.
Energy is in units k s² and the barrier is 1/32. For a rotating flag replace
x by angular displacement, s by angular stroke beta, k by angular stiffness
and m by rotational inertia. No physical switching time follows without these
parameters. This is a finite detent model, not an actual manufactured spring.

Compare five force laws (three are parameters of one topology, not three new
architectures):

- Constant signed generalized force: D=a, a simple comparator.
- Finite permanent-magnet torque: beta=pi/3, theta=beta(q−1/2),
  D=a cos(theta), with `a=mu B/(k beta)`. A uniform transverse field gives
  physical torque mu B cos(theta); reversal changes its sign throughout the
  assumed −30 to +30 degree stroke. This assumes a fixed dipole and uniform
  applied field, not a solved return circuit or a qualified magnet.
- E-074 soft attraction: D=a/(G−q)², G=g/s=1.5, 2.5, 5.
  Opposed-pole reset would give
  `D=a_R/(G−q)²−a_L/(G−1+q)²` with independent nonnegative coefficients.
  Setting left rather than right is the mirrored transition. Current reversal
  in the same pole still cannot reset. The dynamic run energizes only the
  destination pole; off-pole remanence/coupling is absent and would need bounds.

For signed force/torque, polarity reversal and q→1−q give exact mirrored reset
in this symmetric model. For the opposed-pole topology, pole exchange supplies
that symmetry but requires two force paths, windings/steering and isolation;
it does not establish the previous 320-line count for that mutation. These are
complete *force-law* reset alternatives; neither is a complete packed cam
selector. No claim about cam routing, electrical cost or thermal duty follows.

For each force law set a to 0.80 or 0.95 times its lossless single-step energy
threshold `max V(q)/integral_0^q [D(y)/a]dy`. For constant force this is exactly
2/27. Torque work uses the exact sine integral; soft attraction recovers E-074.
For soft attraction these coefficient fractions correspond to sqrt(0.80) or
sqrt(0.95) times threshold ampere-turns, not 80/95% current.

## Pulse and manufacturing/model sensitivity

Cross five force laws with zeta=0, 0.02, 0.10 and four lower-boundary models:
no stop, or q=0 stop with velocity restitution e=0, 0.5, 1. These 120 coherent
scenarios are not independent cell samples or production yield. A whole strip
may share damping, material and seat errors. No distribution is assigned.

Start from rest at q=0. The adversarial generator turns drive on when velocity
is nonnegative and off when negative. It records time edges, then replays key
witnesses as fixed open-loop schedules. Thus the counterexample does not
require a sensor at every flag. It also does not assert that a specific row
scan produces these timings: a scheduler that excludes them needs its own
verified timing/parameter envelope. Run until q>=1 (complete stroke) or tau=150.

Why this matters: `dE/dtau=u D(q) q'−2 zeta q'²`. Applying force on forward
motion and removing it on return can accumulate energy. Current amplitude
alone cannot describe that history. Unstopped witnesses move behind the initial
well by roughly 0.1 stroke; a real seat can invalidate those witnesses, so that
negative excursion must not be hidden in a scalar threshold model.

75/120 scenarios complete a stroke under the generated pulse train.
All 120 crossing/noncrossing classifications agree after halving the step.

| Lower boundary | Complete strokes / scenarios |
| --- | --- |
| No stop | 30/30 |
| Stop, e=0 | 0/30 |
| Stop, e=0.5 | 15/30 |
| Stop, e=1 | 30/30 |

At 0.80 amplitude and zero damping, no-stop counterexamples are:

| Force law | On / off / on edges (tau) | Complete stroke (tau) | Minimum q |
| --- | --- | --- | --- |
| Constant | 0.00 / 4.36 / 7.74 | 13.49 | -0.1272 |
| torque | 0.00 / 4.38 / 7.74 | 13.73 | -0.1224 |
| 1.5 | 0.00 / 4.32 / 7.63 | 13.78 | -0.1095 |
| 2.5 | 0.00 / 4.34 / 7.68 | 13.72 | -0.1168 |
| 5.0 | 0.00 / 4.35 / 7.71 | 13.62 | -0.1221 |


An inelastic stop's absence of observed switching is **not** an arbitrary-pulse
safety proof. The chosen pulse generator is not an exhaustive optimal control
search, and the e=0 impact rule deletes kinetic energy instantaneously. Real
contact compliance, rebound, stiction, guide friction, magnetic remanence,
stop offset/wear and detent asymmetry remain uncertain. A finite-horizon
noncrossing is only a result for that waveform and model. Higher damping alone
has not been qualified as an isolation design. Neighbor fields and bank motion
can add common forcing; no 6,400-cell reliability follows.

## Numerical verification and next decision

Self-review only. RK4 with tau step 0.01; repeat all 120 classifications at
0.005. Fixed-schedule unstopped witnesses replay at 0.005 and 0.0025 with stroke
crossing times agreeing within 0.02 tau. Energy conservation in an unforced
trajectory, exact signed reset symmetry, and lossless single sustained pulses
below their analytical threshold are checked. Contact uses step-end projection
and restitution; classification refinement is not contact-force convergence.
There is no FEM/field solver, contact stress or fatigue evidence here.

Continue with a **positive two-input mechanical gate** comparator and a seated
magnetic flag: synthesize the actual blocking faces, stop, release/reset and
cam engagement sweep at the product pitch. Both inputs must clear the gate
before shared cam energy reaches a command flag; a half-selected input must
meet a frame-supported stop rather than merely experience a smaller force.
Check release ordering and stored elastic energy so resetting one line cannot
fire the previously armed gate. This mechanism change, unlike current tuning,
can eliminate the energy-pumping path. Retain magnetic routes conditionally
until seat/contact and field geometry are bounded; do not request a print or
claim complete-system affordability/update performance from this screen.
