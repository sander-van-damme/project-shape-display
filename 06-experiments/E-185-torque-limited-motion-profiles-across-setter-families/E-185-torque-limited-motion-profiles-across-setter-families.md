---
status: complete
builds-on: [E-131, E-154, E-156, E-181, E-184]
---

# Motion shaping does not erase motor power or intermittent transmission inertia

**Keep direct motion as the timing control; do not reopen the tested Geneva or
resident screw machinery on constant-rpm head counts alone.** This experiment
synthesizes bounded rest-to-rest profiles under one motor model. It compares
existing operating principles, not new architectures. No machine, purchased head,
fabrication or hardware reliability is accepted.

Input main `2e53a18`. Reproduce with Python 3 + NumPy:

```
OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-185/profiles.py --sweep
```

Evidence: deterministic profile calculations; self-review only. No contact CAD,
backlash dynamics, process calibration, measurements or independent validation.
JSON is disposable. E-131/E-154/E-181 source was reconstructed; E-156 coast failures
stand. Active braking here is **not** passive outage arrest.

## Comparable causal machines, with unresolved functions exposed

| Control | Address / energy / retained state / load / verification and recovery |
|---|---|
| Direct setter | Indexed independently driven rack carriage captures a column, takes load from its resident stop, translates and hands back to that stop. Rack/pinion and guide ground motion loads. Return carriage before next site. Actual top and loaded stop proof precede withdrawal; failed proof retains capture. Dock, stop, arrest and reader remain unqualified. |
| Resident screw | Reusable reversible rotary head docks to a grounded thrust-supported screw; antirotating nut carries the column. Sliding threads conditionally retain height; top/hold proof precedes undocking. No per-site head translation reset. Bearings, thread fit, input-loss coast and recovery remain unresolved. |
| Resident Geneva | E-184 resident disk/pin and wheel drive a rack; grounded disk gives bilateral parked reaction. Reusable motor head makes 20 cycles for 40 mm. Input-phase and loaded-output proof are required before withdrawal. Relief, full-pin handover, input arrest and readback remain unresolved. |

Profiles grant ideal bilateral contact, not a manufactured contact-transition pass.
Screw flank exchange extends E-156's single-flank law to ideal opposed faces.
Replication remains 6,400 screw load paths or >=12,800 Geneva axes, versus 6,400
stops plus reusable direct heads. One 10-s resident operation totals 17.8 assembly h.

## Motor and physical bounds

[Pololu 1117](https://www.pololu.com/product/1117), checked 2026-10-11, lists
approximate 6-V free speed 11,500 rpm, 70-mA free current and 800-mA stall current;
25-/100-unit prices are $2.50/$2.30. These are approximate comparator data, not continuous-duty, inertia or thermal
qualification, availability commitment or a market price floor.
Use `R=6/.8=7.5 ohm`, `K=(6-R*.07)/(11500*2pi/60)=.0045463 N m/A`, and constant
loss torque `T0=K*.07`. Their idealization is uncertain. No-load data do not
qualify a thermal model.

The signed equations `i=(tau/g+T0)/K`, `V=R*i+K*g*qdot` and electrical power `V*i`
include negative current and bus regeneration. The [maxon generator
explanation](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators)
supports these linear relations and separation of winding loss from useful power;
it does not characterize this low-cost motor. Zero inductance, instantaneous
current control and ideal gears are favorable assumptions; current/torque jumps,
commutation, jerk, PWM/freewheel and controller cost are unbuilt.

Base scenario: downward load W=1 N, translated inertance `M=max(.002,W/9.81)` kg,
motor inertia Jm=1e-8 kg m² plus 1e-8 kg m² at the driven shaft, |V|<=6 V,
|i|<=.8 A, regenerative electrical absorption <=2 W/head, and absolute column
reaction <=20 N. These are **engineering bounds**, not requirements or X1C priors. Both travel signs
must pass with the same gear/profile. Motor speed is g times input speed; g<1 is
an unpriced speed increaser. Gear inertia/loss and Geneva output-wheel rotary inertia are omitted; input drag is
screened separately.

Even before gears, this motor model has at most
`(6-R*.07)^2/(4R)=.99919 W` mechanical shaft power. A 40-mm raise requires >=.04003 s
at 1 N or >=.40033 s at 10 N; no choice of gear removes this bound. It is a model
bound, not a measured motor output. All-raising maps cannot borrow energy from
lowering neighbors. A 10-N all-lowering map releases 2,560 J, before kinetic and
electrical losses; no energy disappears into a dwell.

## Profile synthesis and checks

Use positive progress q, increasing from 0 to L in either output direction.
Direct pinion radius is 2 mm. Screw mean radius is 1.5 mm and lead slope t=.04,
so lead is .37699 mm, 106.10 turns/40 mm. At assumed sliding mu=.05 it requires
positive torque even to lower; mu=.02 instead overhauls. [Roton's explanation](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/)
supports that distinction, not a PLA friction prior. Geneva uses E-184's ideal
four-slot, 6-mm-center, 2-mm-step law; start/end at mid-dwell, with 20 full turns.

For mean slope hbar=.04/L, define density `r(q)=1+b*h'(q)/hbar` and
`s(q)=min(1,q/(aL),(L-q)/(aL))`. The constructed speed is
`qdot=k*sqrt(s)/r`, and acceleration is `qddot=k²*(s'/(2r²)-s*r'/r³)`.
The b=0 control is a trapezoidal input-speed profile; positive b allocates more
time to the active index and less to dwell. a is the ramp-distance fraction.
Rest endpoints are exact; no instantaneous velocity reset is used. Profiles are
continuous with piecewise acceleration, not jerk-qualified trajectories.

For direction d=+1/-1, column acceleration is `d*(h'*qddot+h''*qdot²)` and contact
reaction `C=W+M*zddot`. Direct/Geneva require input torque
`(1e-8+g²Jm)*qddot+C*d*h'`. Screw thread torque instead equals
`abs(C)*radius*(mu+t)/(1-mu*t)` when C*d>=0 and
`abs(C)*radius*(mu-t)/(1+mu*t)` otherwise; add rotary inertia and assumed drag.
This retains reflected inertia, signed contact, thread dissipation and rotor
acceleration. Losing a flank or crossing backlash receives no damping credit.

Search g={.125,.25,.5,1,2,4,8,16,32,64}, a={.005,.05,.25}, and Geneva
b={0,.25,1,4}: 180 geometry/profile/ratio combinations per scenario (30+30+120).
For each, scan 80 logarithmic k values .05–16,000 rad/s, then bisect the last
sampled feasible interval twelve times and keep a 1% speed reserve. This is a
**finite candidate search**, not a globally optimal time or proof that unsampled
feasible islands do not exist. Rank at 128 intervals/input turn, refit the selected
shape at 1,024, and hold out at 2,048. Include both sides of Geneva acceleration
edges and ramp corners. Uniform-input controls are separately fitted.

A coarse-grid high-inertia Geneva candidate exceeded 6 V at fine resolution
(6.01662 V) despite its 1% speed reserve. It was rejected and refitted; coarse
solver success was insufficient. Numerical evidence below refers to the refined
profiles. Independent checks include constant-ratio trapezoid duration, signed
motor power identity, square-thread frictionless/overhaul limits, kinetic-work
cancellation, Cartesian second-derivative holdout and Geneva travel integration. At 128/512/2,048 intervals per turn,
40-mm travel integral errors are 10.222/.639/.03995 micrometres, reducing about
16-fold each fourfold refinement. No hardware error bars follow.

## Results and complete-board implications

All 24 loaded and eight unloaded return profiles pass the 2,048-interval holdout.
Direct return uses the **same gear/motor**, zero payload and assumed 2-g carriage;
Jm/input inertia persist. Joint loaded-plus-return time is not optimized: these are
sampled model schedules, not minimum possible architecture head counts.

Service is `.10 + loaded_time + return_time` for direct, `.10 + loaded_time` for
resident rotary controls. The .10 s/site allocation covers docking, observation,
seating proof and withdrawal. Add 6 s/map for preparation, addressing transport,
registration, final read, settling and one bounded retry:
`T=6+ceil(6400/H)*service <30 s`. These are optimistic **unvalidated allocations**;
no readback latency, false-accept rate, settling or repair duration is established.
H is the smallest integer for that schedule. Arbitrary independent signs are
admitted by the tested bidirectional actuator envelope; actual address routing is
not constructed. No all-board reset of unchanged cells is required in these causal
controls, but shared-frame disturbance and local head travel remain unquantified.

| Coherent scenario | Direct loaded + return (s); H | Screw stroke (s); H | Shaped Geneva stroke (s); H |
|---|---:|---:|---:|
| Base: 1 N, Jm=1e-8 | .13780 + .06305; **82** | .38251; **131** | .68228; **214** |
| 10 N | .56191 + .33142; **267** | 1.14196; **337** | 2.60095; **800** |
| Jm=1e-7 | .16826 + .10526; **100** | .42689; **143** | 1.42188; **427** |
| 10 N and Jm=1e-7 | .75497 + .49257; **377** | 1.39359; **400** | 4.73203; **1,600** |
| Bus sink .2 W/head | .13780 + .06837; **83** | .40190; **137** | .68228; **214** |
| Current ceiling .2 A | .23457 + .18538; **140** | .50917; **165** | 1.87526; **534** |
| Screw mu=.20 | .13780 + .06305; **82** | .53126; **169** | .68228; **214** |
| Extra input drag .001 N m | .16193 + .11184; **100** | 1.01244; **305** | .78415; **238** |

These eight scenarios are competing assumptions, not eight draws from a prior.
Drag reverses screw/indexer timing ordering; no universal ranking follows.
With direct return conservatively fixed to the loaded speed, base H=102 and
10-N/high-inertia H=458: screw H=400 then appears better. Accounting for the actual
unloaded return removes that crossover in this finite search. Reset cannot be
omitted, nor should its speed automatically inherit the payload limit.

Base selected `(g,a,b)` is `(2,.25,0)` direct, `(.25,.25,0)` screw and `(2,.005,.25)`
Geneva. At 10 N the respective g values are 16/1/16. The base screw needs about
**24,965 input rpm**, despite only 6,241 motor rpm; printed-thread speed, wear,
balance and bearing requirements are **not** qualified. The favorable gear is a
speed increaser, not a justification for using the motor's rpm at the screw.

Nonuniform Geneva input reduces the base stroke from **1.63442 to .68228 s**
(58.3%); at 10 N, 5.21877 to 2.60095 s (50.2%). Improvement falls to about 8.6%
under the .2-A ceiling. Base output reaction spans **-5.99 to +7.99 N**, demanding
flank exchange/preload; actual E-184 clearance geometry has no corresponding
contact-dynamics pass. The constant-input calculation is also rest-to-rest and
current-limited, unlike E-184's granted constant rpm. These results therefore do
not overwrite the old conditional arithmetic.

For the selected Geneva shapes, refitting at 256 versus 1,024 intervals changes
time by at most about **.079%** across the eight scenarios; the 2,048 evaluation of
the selected fixed speed changes integrated time by about .00082%. Worst integrated
motor energy-identity residual is **5.06e-6 J**, versus 0.4-J useful work at 10 N.
Maximum voltage/current/reaction constraints pass at the fine holdout, but finite
sampling does not certify all intersample extrema or a globally optimal profile.

Base direct loaded raising uses **.17885 J electrical / .12612 J winding heat**
per site, before return, gearbox and electronics: **1,144.6 J input per board**.
10-N direct lowering regenerates .11739 J/site net in this active-controller model,
with .26866 W peak bus absorption/head; base screw needs up to .23186 W sink during
braking despite positive total lowering input. Lower sink capacity really changes
its profile. A four-quadrant bridge, bus clamp/storage, supply, wiring and cooling
are obligations, not free benefits. .8 A is a test ceiling, not a continuous
rating; the .2-A case shows sensitivity without claiming it is thermally qualified.

At base H=82, the applicable listed 25-unit motor tier gives **$205**, leaving only
**$45** after an assumed $250 shared reserve under the $500 ceiling. That remainder
must cover unreserved gears, drivers, supports, wiring, observation, capture and
arrest; it is not a BOM pass. Buying 100 at $2.30 costs $230. Screw H=131 and Geneva
H=214 already cost **$551.30/$742.20 with the reserve**, before all other resident
purchases and head hardware. At $400, base direct motors plus reserve alone fail;
the $200 ideal is already below the assumed reserve. Other motors, volume sourcing
and a different reserve can change this conditional comparison.

At the .10-s site allocation base direct T(H=82)=29.7678 s, leaving only .2322 s
in the modeled map; an additional shared fault/retry delay can erase it. Failed
support proof keeps the head captured for service, not a promised successful map.
No board reliability, print-volume/time or scrap estimate follows.

## Scope, disposition and next discriminator

All cells may share high friction, supply sag, motor temperature, dimensional bias
or reader registration. The scenario table treats them coherently; it does not
average independent cells or infer yield. Lead error, hole shrinkage, first layers,
layer quantization, warp, bearing alignment, roughness, wear, anisotropy, creep and
fatigue remain outside this kinematic model. No fabrication or yield claim follows.

Retain this common motor/profile evaluator and conditional comparisons. Stop
constant-rpm-only claims of head affordability and further Geneva lock refinement
justified only by nominal speed. Reopening requires a **complete** drive/transmission,
actual contact/retention and sensing route within joint cost/time, plus a bounded
outage path. A larger shared motor could change the power/cost comparison but adds
selection, isolation and source-energy recovery obligations; this experiment does
not reject that principle or all small screws/indexers.

**Next: EXPLORE / SCREEN shared power with grounded branch control.** Repository
queries for planetary/epicyclic/differential-gear mechanisms found no explicit
object; this is not novelty proof. Compare a two-output planetary/differential with
grounded branch brakes, a dog-clutch bus and direct setter. Cross-check E-082/E-137/
E-156 first. Test signed motion/torque, branch switching and source loss with one
output held while the other travels. Stop if brakes merely replace equally costly
motors, a free grounded coordinate is hidden, unchanged outputs move or source
coast reaches them. No preferred architecture, print, purchase or approval gate.
