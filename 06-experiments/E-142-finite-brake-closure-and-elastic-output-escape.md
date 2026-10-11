---
status: complete
builds-on: [E-141, E-132]
---

# Finite closure does not make rotor arrest an output lock

**Stop individual purchased releases and adverse sliding-cam return; spring closure
remains a subsystem hypothesis.** Finite plate closure rebounds; the elastic output
can escape after rotor arrest. No machine is selected or outage drop accepted.

Input main `f5a9c31`. Reproduce with Python 3/NumPy:
`python3 tools/curated-experiment-checks/E-142/closure.py` (disposable JSON).
Evidence: sourced screening, finite sections, lumped electrical/contact simulations
and analytical energy bounds. **No assembly CAD, process calibration, physical
measurements or independent review.** Dense routing remains a separate gate.

## Release choices and necessary conditions

Inherit E-141's independent spatial heads, capture-before-support-release, signed
motion and proved support handback. The retained joint carries both force signs;
the brake grounds the shaft on loss. Neither release supplies the 6,400 parked
support/return mechanisms, selection, readback or dense route under 5.08-mm tops.

| Release | Energy and reactions | Disposition |
|---|---|---|
| Axial spring plate | Powered coil pulls plate off one shaft disc against a preloaded spring; loss dissipates magnetic energy and releases spring into pad contact. Plate keys and shaft thrust bearings return torque/normal load to frame | Finite conditional model below; custom coil, frame and controls unpriced/unqualified |
| Sliding cylindrical cam | Motor holds a ramp under the same plate; stored plate energy plus a separate torsion spring must backdrive the ramp and free motor after loss | Fails return at adverse contact friction; direct drive does not remove detent or reflected inertia |
| E-132 permanent pads | Always-grounded opposing spring pads and counterbalance; motor must drive through drag | No release latency, but adverse moving drag still produces 4.8 m/s² along travel; not repaired |

The cam has radius 6 mm, .2-mm lift in .35 rad, slope `s=.095238`; its closing
backdrive torque is `N*R*(s−mu)/(1+mu*s)`. Explicit additional return is .005649 N m
(minimum of a .007062-N m ±20% scenario). At mu=.3, N=80/120 N, net return is
**−.08991/−.13768 N m**: it stays open even with a free, zero-detent motor. At mu=.1,
only .003385/.002253 N m remains; a **labelled .005-N m detent bound** also stops it.
Opening needs .0611–.2986 N m across the six cases; spring lift work .016–.024 J,
additional return work .001977 J. The powered state is not an ideal latch. A roller,
steeper cam, stronger return or different release changes the embodiment and its
opening torque/energy/geometry. Do not extrapolate to all mechanical returns.

Sources accessed 2026-10-11:

- [Adafruit 412](https://www.adafruit.com/product/412): $6 each at 100+, 5-N
  retentive force, .5-N starting force, 5.5-mm throw, 40-ohm coil, return spring.
  Directly retracting an 80–120-N plate fails the stated force rating; even a lever
  cannot remove its price. **121/229 releases cost $726/$1,374**, above the entire
  $500 ceiling before anything else. Stop this procurement embodiment, not the market.
- [Johnson Electric return-spring table, D7](https://www.johnsonelectric.com/pub/media/image/tmp/metric-imperial/Rotary_in_17.pdf)
  lists 1-oz-in standard settings for small units, ±20%, intended for armature/light
  load return. This supplies a torque
  scenario, **not** a selected actuator or qualified friction/inertia.
- [Kendrion spring brake construction](https://www.kendrion.com/en/products-services/industrial-brakes/spring-applied-brakes/vario-line)
  supports the spring/coil/frame topology, not our miniature numerical inputs.
  E-141 retains the timing source and fluid-only/speed-only failures.

## Finite axial section and electrical/normal response

To avoid a free second friction face, change E-141's geometry: **one annular face,
16–20-mm radius**, shaft output radius r=2 mm. A shaft-mounted disc bears against a
keyed translating pressure plate; axial thrust bearings close the load path to the
housing. The torque calculation uses the minimum contact radius: `D=mu*N*16/2`.
This is a 40-mm disc plus housing, not machinery fitting inside each 5.08-mm top.
A 1-mm-thick rotor with 4-mm inner radius has .0627–.5019 kg reflected inertia at
r=2 mm for a **density bound** 1,000–8,000 kg/m³, before motor/gear inertia. Thus
M=.3 kg requires a lightweight rotor; it cannot describe the dense end of that box.
The M=3-kg escape witness does not depend on the lightweight assumption.

Axial q=0 is the powered-open hard stop; first pad contact occurs at q=g. The pad
plane separation is g−q; q>g compresses the lumped face/frame contact, rather than
passing rigid solids through each other. Plate guide travel must accommodate the
computed overtravel. The opposite magnetic gap increases as d+q. Pole area 150 mm²,
300 turns, resistance 12 ohm, holding magnetic force 1.2 times initial spring force
are **custom component allocations**, not a sourced magnet. Annulus area is 452.39 mm².
No synthesized winding/core, saturation/fringing, guide binding or bearing design is
qualified. This model is useful for sensitivity, not evidence that a coil was built.

```
a=mu0*turns²*pole_area; L(q)=a/(d+q); i=lambda/L(q)
lambda_dot=−R*i−Vclamp while lambda>0 (zero thereafter)
Fmag=lambda²/(2*a)
m*q_ddot=N+ks*(g−q)−Fmag−Fc
Fc=kc*max(q−g,0)+c*max(q_dot,0) while q>g; otherwise 0
c=2*zeta*sqrt(m*kc); q>=0 with grounded, dissipative open stop
```

Force follows magnetic energy and plate motion, with no assigned ramp, delay or
restitution. Compression-only damping cannot pull the faces. Friction omits velocity
and thermal effects; saturation, remanence and sticking remain outside this model.

| Coherent normal scenario | Fast clamp | Soft/diode |
|---|---:|---:|
| g / d, mm | .2 / .2 | .4 / .3 |
| Plate mass, kg; N at first contact | .02; 100 | .03; 80 |
| ks / kc, N/m | 2,000 / 2,000,000 | 1,600 / 500,000 |
| zeta; suppression voltage | .3; 48 V | .02; .7 V |
| Holding current/power | .754 A / 6.82 W | 1.013 A / 12.32 W |
| Spring release work | .02004 J | .03213 J |

At first contact, reopening needs at least 1.373/2.150 A; from the compressed static
state it needs more. A 24-V/12-ohm drive cannot reopen the adverse case. A proposed
36-V current-controlled pull-in supply could exceed the ideal static force threshold
but remains a **new cost obligation**, not a proven transition. A bistable magnetic latch could stay open on loss; none is credited.

At 1-µs normal steps, fast/soft first contact is **.622/1.700 ms**, but sustained
95% static force is **3.059/83.084 ms**, with **one/five separations**. Peak normal
force is about **231/176 N**; q reaches .3025/.7519 mm (including .1025/.3519 mm
contact/frame compression). Static normal is 99.900/79.745 N, not exactly the spring
force quoted at first touch. Neither case inherits E-141's 2.671-ms full-force bound.
At .3 s the residual normal oscillator energy supplies a conservative future force
floor; the tangential model uses that floor thereafter, not an arbitrary final ramp.
The fast profile is a finite **conditional** response, not hardware admission.

## Elastic output and retained capture

The isolated section has a 4×4-mm eye with 2×2-mm square bore, 2-mm axial thickness,
a 1.5×1.5-mm pin, and 3-mm head/retaining collar on opposite sides. The separate collar
must be installed/retained before load transfer (a bought keeper/fastener obligation).
Both axial stops overlap by .5 mm; either vertical bore face carries signed load
after .25-mm take-up. The source generates four eye-wall prisms, pin,
head and collar and checks both loaded faces/axial stops throughout 40-mm travel.
Coherent pin growth, bore shrink and registration e gives entry margin `.25−3e`:
.25/.10/−.05 mm for e=0/.05/.10 mm. The e=.10 case has **.170 mm³ solid overlap**,
so it cannot dock. Autonomous keeper insertion/release, wear strength and loaded proof are not
constructed. This captive test section does not repair E-132's 5.76-mm³ third-row
collision; no dense head layout is admitted.

After input loss, motor torque is zero and both coordinates remain free:
`m*x_ddot=F−f`, `M*y_ddot=f−brake`, y=r*theta, M=J/r². The bilateral joint uses
`f=K*sign(x−y)*max(abs(x−y)−b,0)`, b=.25 mm. Its two contact faces and series elasticity
remain coupled; no fixed motor input, electrical short or unpriced motor brake.

The 288 deterministic cases cross two normal profiles, F=.02/10 N, load-side effective
mass m=.05/1.1 kg, reflected rotor/gear M=.3/3 kg, K=100/1,000/10,000 N/m,
mu=.02/.1, and raising/lowering at 100 mm/s or reversal at zero speed. Initial steady
spring force is F; reversal starts with F+2*m N, from powered acceleration −2 m/s².
Initial shaft position includes preload and play. F is **net** external force,
including gravity. The load-side m can include downstream reflected inertia; it
is not necessarily all vertically carried mass. If all m were vertical, cases with
F<m*g would need an external upward force, which is not supplied by this head. No
free counterbalance is credited; these are inertia/force scenarios, not selected
load assemblies. The high-F/light-m cases require a sustained external load.

K is an **effective bound**, not measured PLA stiffness or a generated flexure. The
softest loaded case needs 100-mm static extension; compact realization is unproved.
There is no tangential damping credit. After 1.5-s sampling, the piecewise elastic
potential minus F*x gives exact turning points for a stationary rotor. The future
no-slip bound requires peak possible joint force below the normal-force floor;
otherwise indefinite holding remains uncertified.

| Conditional example | Rotor's last stop | Output extrema relative to start | Consequence |
|---|---:|---:|---|
| Fast, F=10 N, m=1.1 kg, M=3 kg, K=100 N/m, mu=.02, lowering | 52.12 ms | −7.731…+13.035 mm | Another **7.873 mm downward after rotor stop**; crosses lower end from h=12 and upper end from h=34 |
| Same, K=1,000 N/m | 60.80 ms | −.059…+5.753 mm | Fits these two heights in model; no accepted outage displacement |
| Soft, F=10 N, m=1.1 kg, M=.3 kg, K=100 N/m, mu=.02, raising | 43.24 ms | −10.519…+10.475 mm | Continues beyond h=34's 6-mm upward clearance after rotor stop; later reverses |
| Fast, F=.02 N, m=1.1 kg, M=3 kg, K=100 N/m, mu=.1, reversal | 1.20 ms | −44.489…0 mm | Stored elastic energy escapes the entire stroke despite near-zero rotor motion |

Across both profiles, K=100/1,000/10,000 N/m gives extrema
−44.489…+16.416 / −5.145…+8.820 / −2.880…+8.347 mm. These are finite scenario
results, not continuous-box bounds. One soft-profile K=1,000 N/m raising case is
stopped at 1.5 s but fails the future no-slip force bound; it remains **uncertified**.
An independent ideal instantly fixed rotor with m=1.1 kg, K=100 N/m,
v=.1 m/s still permits **10.488 mm** elastic amplitude about equilibrium: rotor
arrest cannot remove energy already downstream.

Unrestricted coordinates locate first stroke crossing, not behavior after an end-stop
impact. h is height above the lower end: allowed relative excursion is `[h−40,h]` mm.
Passing that geometric interval does **not** accept the outage drop or prove settling.
With no physical tangential damping the remaining oscillator need not settle at all.
Prove actual output height and loaded support before withdrawal; shaft readback can
falsely accept. Reader bias, false acceptance and retry completion remain unsolved.

## Verification, full-display consequence and next discriminator

Normal steps 4/2/1 µs give fast sustained-95% times 3.048/3.056/3.059 ms and
soft times 83.076/83.082/83.084 ms. Maximum normal energy residual falls
2.64e−4→1.35e−4→6.70e−5 J (fast) and 1.58e−4→7.88e−5→3.94e−5 J (soft),
against initial magnetic energies .02410/.02903 J. Contact force peaks carry roughly
1-N discretization uncertainty; no fitted restitution hides rebound.

Tangential backward Euler solves the two masses, spring contact active set and Coulomb
impulse together. Its energy ledger separates friction heat from **numerical loss**:
velocity-increment kinetic energy plus the convex joint-potential remainder. The
balance residual is <5e−14 J; this is bookkeeping accuracy, not integration accuracy.
For the soft raising witness, 40/20/10-µs steps give maximum later downward motion
from rotor-stop position 14.6823/14.6828/14.6840 mm; upward extrema
−10.5164/−10.5187/−10.5199 mm. Numerical loss halves .0001308/.00006562/.00003299 J.
The decisive 6-mm upward-clearance failure survives refinement. The higher-K batch
has up to .00150 J numerical damping; its apparent fits are screens, not certification.

Independent limits: coil-free constant-force first contact .283 ms versus analytic
.282843 ms; unbraked stiff coupled masses move .200028681 mm versus .200028571 mm
from combined-mass dynamics. Exact locked-rotor energy extrema include both faces and
the clearance interval. Finite prism sweeps verify both loaded pin faces and retaining
stops; .05-mm axial overtravel produces .250 mm³ nominal solid overlap, distinguishing
retention from a free pin.
`--checks` reruns the limiting cases, geometry and cam screen without the full batch.

Parameters are scenarios, not distributions or X1C priors. Gap/normal/contact/coil
conditions change together; mu/K/inertia cross them. Shared bank gap bias, suppression,
contamination and frame softness prohibit independent-cell yield claims. Hole bias,
layer steps, warp, roughness, anisotropy, creep, fatigue, wear and keeper alignment
remain uncalibrated.

E-141's optimistic schedule still needs 121/229 independent heads at 100 mm/s,
without/with empty return: 6-s preparation/registration/proof/retry/settling allowance
plus batches of .4-s travel and .05-s local transfer/proof. Those overheads remain
unearned, especially with a keeper and undamped output. With a scenario $250 shared
reserve and free cells, head ceilings are **<$2.066/<$1.092**. Even custom fast-profile
holding coils consume 825/1,561 W if all heads are open; their supply, switches,
clamps, wiring, cooling, motors, bearings, keepers and sensors are not free. Shared
release cannot simply divide this inventory without an independent-motion path.
All 6,400 parked support/guide/return interfaces and neighboring-region disturbance
remain machine obligations. No print or purchase has higher value at this gate.

**Next axis:** a common spring-return release crossbar opening grounded clamps on
independently moving head rods, downstream of drive elasticity. Separate motors
retain independent motion; local springs close the pads on loss. Screen summed
opening force/work, crossbar bending/warp, stuck-rod propagation, clamp placement
relative to the output joint, independent stopping/proof and joint purchased cost.
Compare per-head coils and permanent drag. Stop if a stuck-open member defeats all
returns, downstream routing fails, or deleting selection/actuator inventory is the
only budget path. This is an untested recombination, not a completed capture or cheap
shared motor. Stop isolated-annulus tuning and fluid/speed-only holding retries.
