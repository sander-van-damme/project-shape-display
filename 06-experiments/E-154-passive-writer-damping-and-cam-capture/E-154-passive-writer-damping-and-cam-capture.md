---
status: complete
builds-on: [E-153, E-148, E-131]
---

# Passive dissipation can capture a cam; the tested head and follower do not make a machine

**Retain geometric wells plus passive dissipation as a conditional combination. Stop the priced
motor/relay head and the thin-neck barrel follower at the 10-N scenario.** Strong damping
changes E-153's conservative escape; merely adding a resistor does not guarantee capture. No
machine, printing or purchase selected.

Input main `74b1235`. Reproduce with Python standard library:

```
python3 tools/curated-experiment-checks/E-154/capture.py --sweep
python3 tools/curated-experiment-checks/E-154/capture.py --low-load-check
python3 tools/curated-experiment-checks/E-154/geometry.py
```

Evidence: equations, deterministic simulations, finite implicit solids, stress/cost bounds and
primary product data. Self-review only; no calibrated process prior, measurement or qualified
circuit, dock, material, life or machine. JSON is reproducible output. E-153's undamped
counterexample remains valid.

## Passive causal paths and what is still assumed

Load path: top → guided sleeve → follower → barrel groove → thrust flange → frame. An indexed
writer drives a bilateral dog coupling. Closed jaws behind a shaft collar retain axial
engagement through torque loss; dogs transmit torque. Undocking requires top, phase and
stationarity proof; failed proof retains the head for correction. The collar below does not
construct the jaw's self-locking actuator.

Two explicit sink topologies:

- **Always connected generator:** a second geared permanent-magnet motor feeds a
  closed winding/resistor loop; another motor writes. Its field, current and heat
  sink persist without power or switching. RL includes pre-cut current. It pays
  another motor/rotor, continuous drag and cooling. Open brush/wire/resistor,
  stripped gear or separated dock removes braking and restores E-153's escape.
- **Fail-return short:** motor terminals go to DPDT commons, NO contacts to the
  drive bridge, NC contacts to a resistor loop. Spring return isolates the bridge
  and closes braking. Live-power torque faults still need a separate common-enable
  dropout. Delayed viscous cases grant zero winding current before closure;
  initial-current clamp/freewheel, coil suppression, bounce and welded/stuck-powered
  faults are **not solved**. This topology needs switched-circuit work before any
  hardware transient pass, but the priced implementation already fails cost.

Primary sources, accessed 2026-10-11: [maxon generator
equations](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators)
support generated voltage, current and reaction torque; they do not supply a miniature braking
qualification. [Pololu 1117](https://www.pololu.com/product/1117) lists approximate 6-V no-load
11,500 rpm, 70 mA and 800-mA stall data, 3–12-V operation and $2.30 each at 100. [Omron G5V-2
datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g5v_2.pdf) lists 3-ms initial
release and 2-A/30-VDC resistive rating, not our complete commutation. [DigiKey's direct
offer](https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/G5V-2-DC5/87819)
quotes $2.80390 each at 100, excluding shipping/tax. These are comparison parts, not a selected
BOM or universal price floor.

## Energy-consistent transient and capture basin

Use SI units with E-153's `h(q)=L*q/(2π)+a*sin(4q)`, nominal L=.004 m, a=.0003 m. F is total
downward force; M is equivalent output inertance; J is rotor/head inertia reflected to the cam.
The exact one-coordinate equations are

```
A(q) = J + M*h'(q)^2
A*qddot + M*h'*h''*qdot^2 + F*h' + K*i = 0
L_e*idot = K*qdot - R*i
E = .5*A*qdot^2 + F*h + .5*L_e*i^2
Edot = -R*i^2
```

Zero inductance gives `K*i=c*qdot`, `c=K²/R`; c=0 before closure. Omitting M*h'*h'' creates
spurious energy. Normalized R=1, K=sqrt(c), inductance=L_e/R preserve energy/torque; normalized
current is **not physical motor amperes**.

At positive F, total mechanical **plus magnetic** energy below the lower adjacent crest is an
analytical trapping criterion. The numerical evaluation identifies capture; it does not imply
the requested height or forbid earlier skipped wells. Settling is reported only when remaining
energy above that well bounds every subsequent speed below .01 rad/s and equivalent height
energy below 1 µm, while this passive circuit remains closed. These are explicit reporting
conventions, not accepted product accuracy/drop limits. A stationary top alone can coincide
with a turning point; it is not a proof of seating or safe undocking.

The 288-case sweep uses F=.02/1/10 N; J=1e-7/1e-5 kg m²; M=max(.002,F/9.81) or 1.1 kg;
c=1e-5/1e-4/1e-3 N m s; initial downward 600/2,400 rpm; four phases .001/.251/.501/.751 of the
crest-to-crest period; 3-ms delay and 1-s horizon. The larger M is equivalent-inertance
sensitivity, not a 1.1-kg payload weighing .02 N or a granted transmission. Samples are basin
witnesses, not probabilities. Uncaptured at the horizon is unresolved unless the full-stroke
bound was crossed. This uses an unbounded coordinate; end-stop impact is not simulated.

Each entry is **captured / settled / full-stroke exits**, out of 32 scenarios:

| F (N) | c=1e-5 | c=1e-4 | c=1e-3 |
|---|---:|---:|---:|
| .02 | 15 / 6 / 8 | 16 / 0 / 0 | 18 / 0 / 0 |
| 1 | 0 / 0 / 16 | 24 / 16 / 0 | 32 / 1 / 0 |
| 10 | 2 / 2 / 30 | 16 / 16 / 16 | 32 / 32 / 0 |

At 10 N and c=1e-3, the sampled basin includes all 32 releases, with up to three crests
crossed, 3.187-mm height reduction, .286-s settling and .439-J heat. This is not a continuous
basin enclosure or a manufactured capture probability.

A separate nominal F=10 N, M=1.02 kg, J=1e-6 witness starts just inside a lower crest, at
−2,400 rpm. With c=0/1e-5/1e-4 it exits 40 angular periods in about .149/.187/1.103 s. With
c=1e-3 it captures after one downhill crest, with maximum height reduction **1.187 mm**,
dissipating **43.45 mJ**, settling by **.177 s**. This is a physical-model outcome, not an
acceptable-drop decision. A near-upper-crest release from rest also reproduces E-153's undamped
escape; a release below a lower crest can remain trapped yet oscillate without settling. No
damping is not equivalent to no wells.

The always-connected generator holdout uses the same F/M/J, phase .251 and −2,400 rpm, with its
steady pre-cut current. At c=1e-3 and L_e/R=0/1/10 ms, capture takes **2.8/4.2/78.8 ms**,
settling **.249/.208/.357 s**, and heat is **.0364/.0680/.3422 J**. The 10-ms case releases
magnetic energy, crosses two uphill crests and ends one well higher: maximum rise **2.164 mm**.
Passive does not mean monotonic descent. All three c=1e-4 holdouts instead leave the stroke.

For F=0 and constant J, viscous damping gives exact total travel `|omega0|*(delay+J/c)`; at
J=1e-6, c=1e-4, 1,200 rpm and 3 ms this is **1.63363 rad**. There is **no parked potential
well** after undocking at zero total force. At .02 N there are shallow wells, not a qualified
bias mechanism. Gravity/bias loss or upward loading reopens retention; no free spring is added.

At corresponding phases, kinetic-plus-magnetic energy changes by `−F*L/4−Q` uphill or
`+F*L/4−Q` downhill. Dissipating gravity work each period can sustain running without capture;
damping is not a static lock.

## A sourced motor exposes the inertia and cost coupling

From Pololu's approximate data, R≈7.5 Ω and K≈.004546 N m/A, using the no-load voltage minus
winding drop. Ideal gearing g=1/3/6 gives c≈2.756e-6/2.480e-5/ 9.921e-5 N m s. Gear losses are
not silently counted as helpful braking. Motor inertia is unpublished in that source:
**1e-8/1e-7 kg m² are bounds to test, not measured values**, and J=1e-8+g²*Jmotor. At F=10 N,
M=1.02 kg, −2,400 rpm, 3-ms assumed closure and eight phases:

- g=1 and g=3 leave the full nominal stroke in all tested cases.
- g=6 with the smaller inertia captures all eight, after up to **five downhill
  crests and 5.493-mm maximum height reduction**, with up to **.152-s** settling
  and **.1719 J** heat.
- g=6 with the larger inertia leaves the full stroke in all eight. This is a
  changed ranking under epistemic inertia bounds, not a predicted failure rate.

At g=6, initial short-circuit current is about .914 A. Merely balancing the maximum static cam
torque at 2,400 rpm requires about **11.91 V** before motor friction, gear losses and
acceleration; adding the catalog no-load current raises this to about **12.43 V**.
Constant-speed 10-N writing is therefore not established inside the listed 12-V range. The
always-connected second generator additionally loads the drive and adds reflected inertia; the
one-motor table is favorable to it.

The optimistic E-153 schedule `T=6+ceil(6400/H)*(turns*60/rpm+.10)` includes an assumed .10
s/site for docking, observation, seating and withdrawal, plus 6 s/map for preparation,
transport/registration, final proof, settling and one bounded retry. Acceleration, actual
readout and head routing remain unbuilt. Ten turns at 600/1,200/2,400 rpm need **305/165/95
heads**. Eleven turns, retaining E-153's common-lead travel allowance, need **337/178/102**. At
2,400 rpm, 102 motor/relay pairs at the favorable 100-unit rates alone total **$520.60**,
before all other purchased items. Even nominal ten-turn operation costs $484.87 at pro-rated
rates; 100 actual pairs cost $510.39. A $250 shared reserve makes even that favorable 95-head
allocation **$734.87**. Stop this priced head, not every possible passive sink. The
always-connected two-motor variant adds a motor and generator drag.

Uniform .02/1/10-N lowering through 40 mm releases **5.12/256/2,560 J per map**. This requires
heat removal or explicitly constructed energy reuse, plus kinetic, magnetic and drive energy;
it cannot disappear into wells. Permanent c=1e-4/1e-3 braking at 2,400 rpm dissipates
**1.579/15.791 J per nominal 40-mm write**, even without payload: about 10.1/101 kJ per board.
Instantaneous head heat is 6.32/63.2 W. Temperature, duty cycle and cooling remain unqualified.

## Finite contact witness: clearance is not a load-path pass

`geometry.py` defines a finite barrel of radius 1.75 mm and height 52 mm, minus a radius-.4-mm
swept-sphere groove centered on `(1.5*cos(t),1.5*sin(t),h(t))`. The groove extends one period
before the first usable well and beyond 44 usable steps. An antirotating radius-.3-mm follower
sphere sits at radial coordinate 1.5 mm, connected to the sleeve at x=2 mm by a radial
.4-mm-diameter neck. Sleeve outer/inner widths are 4.4/4.0 mm, top 4.8 mm, guide envelope 5.0
mm, neighbor pitch 5.08 mm. Thin walls are unqualified.

The loaded center is solved from the actual groove/ball offset, not placed on h(q). Distance
minimization checks sampled sphere and neck surfaces against the swept void through an entire
period; periodic translation covers the interior 44-step path in both directions. End extension
provides groove beyond both endpoints. The nominal centerline curvature radius bottoms near
.489 mm; L=3.9/4.1, a=.25/.35-mm corners reach about .416 mm, narrowly above the .4-mm cutter.
No sampled interference occurs; the neck's narrowest sampled nominal clearance is only **.00949
mm**. Phase grids 32/64/128 give loaded-offset maxima .157824/.157970/.157971 mm. Sampling is
not an interval clearance proof.

The loaded offset is **.100–.158 mm**, changing slope/inertia: the ideal-law simulation is
**not dynamics of this manufactured contact**. An independent constant-speed bound is more
severe: `hddot=−16*a*sin(4q)*omega²`. At 600/1,200/2,400 rpm, peak output acceleration is
18.95/75.80/303.19 m/s². For F=10 N, M=1.02 kg, the 2,400-rpm vertical contact reaction spans
**−299.3…+319.3 N**. Gravity-only contact reverses above about **432 rpm** when F/M=g. A .1-mm
radial-clearance tube has vertical backlash; it cannot follow the ideal bilateral law on its
loaded flank through that reversal. Opposed/preloaded contacts or a slower/nonuniform profile
change parts, loads and timing. This is a constant-speed counterexample, not a maximum speed
for every profile.

No contact refinement is justified for this neck: its nominal cantilever bending stress
`32*F*.5/(π*.4³)` is **1.59/79.6/795.8 MPa** at .02/1/10 N. Under explicitly assumed 20–60-MPa
material allowances, capacity is only **.251–.754 N** before fatigue, creep, stress
concentration and print orientation. This is a bounded strength rejection, not sourced PLA
strength or rejection of every cam follower. The neck breaks the sole support path; retaining
the rotor cannot catch that break.

Thrust flange R=2.1 mm bears on a grounded R=1.8–2.1-mm face (3.676 mm²), with an opposing
keeper. Dock neck/shoulder radii .6/.8 mm and jaw edge |x|=.65 give .15-mm overlap and .05-mm
clearance; opening past |x|=.8 permits withdrawal. Neighbor guide/top gaps are .08/.28 mm at
arbitrary heights. Collar/keeper strength, jaw locking, loaded docking transitions and frame
motion remain unqualified. These primitives do **not** earn a complete geometry pass.

Common lead/amplitude errors do not average away. Shrinkage, first layers, layer quantization,
warp, alignment and waviness can consume the tiny clearances. Friction, anisotropy, interlayer
weakness, creep, wear and fatigue are uncalibrated. Temperature/brush/contact resistance and
shared enable faults correlate arrests. No X1C yield or readback false-accept rate is inferred;
common sensor bias persists.

## Controls, verification and next decision

E-131's screw retains continuous sliding support but needs 84.88 nominal turns/40 mm at 3-mm
diameter and μ=.05 zero-margin lead; static hold does not prove arrest. E-148's downstream jaw
can support after upstream dock separation, unlike this rotor-only sink; its
excursion/friction/field-return limits remain. Cam wells save turns but add braking, skipped
heights and fine load transfer. No machine wins.

Verification: differential energy balance residual <1.9e-14 W; exact no-load travel error <2e-7
rad. RK4 steps adapt to natural frequency, speed, changing inertia, damping and electrical
time; refinements ×1/2/4 preserve the six RL capture/escape dispositions. The last two grids
differ by <8e-7 mm in maximum drop and <45 µs in survivor settling. The difficult light-rotor
escape retained its disposition at ×1/2/4/8 while energy drift fell from 1.76e-4 to 4.97e-9 J;
its motor sweep uses ×8. Other motor drift reaches 7.13e-6 J. The low-load/weak-damping group
retains its counts at ×4 (drift <1.52e-9 J); four other low-load holdouts retain capture status
at ×1/2/4, with last-grid drop differences <1.1e-5 mm. Other grid entries are not individually
convergence-qualified. Geometry uses 32/64/128 phases and finite dock open/closed/withdrawal
contact samples. These checks validate the reduced calculations, not manufactured contact
dynamics.

**Reopening:** require a materially different compression-supported follower/internal
layout, explicit minimum load, and shared/head drive that escapes cost, inertia,
contact-reversal and cooling bounds. Compare those topologies with screw/jaw controls
next. No fabrication: the current failures are computational/economic.
