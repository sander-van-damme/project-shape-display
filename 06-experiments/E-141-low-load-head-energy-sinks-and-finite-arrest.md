---
status: complete
builds-on: [E-140, E-128, E-132, E-109]
---

# Low-load arrest requires a force-time envelope, not just a speed limiter

**Retain spring-applied head braking as a conditional lead; no complete machine is
admitted.** A rigid-coordinate bound limits motion at 100 mm/s if minimum force and
millisecond closure actually exist. A faster case escapes 40 mm. Fluid closure leaves
elastic rebound; leakage defeats indefinite holding. Centrifugal limiting never holds,
and an overspeed stop can trigger too late. No outage displacement is product-approved.

Input main `22cb4ca`. Reproduce: `python3 tools/curated-experiment-checks/E-141/arrest.py`
(Python 3/NumPy; disposable JSON). Evidence: sourced principles, analytical bounds,
exact piecewise dynamics, 72 spring/24 fluid/24 governor scenarios. No assembly CAD,
process calibration, physical measurements or independent review.

## Causal architectures and source discovery

Three source axes: industrial spring-brake timing, hydraulic shutoff, centrifugal
limiting/tripping. The triggered retained stop is an additional combination, not a
claimed invention. Cross-check: E-128 first spring-pad contact; E-132 permanent drag;
E-140 load feedback; E-104–109 resident fluid valves. Here fluid damping moves to
reusable **heads** while resident mechanical supports remain. No saturation claim.

Common architecture: spatially index independently actuated heads; capture a supported
output, take load, release its parked support, command signed travel, restore/prove
support, withdraw. A spring keeper/grounded shoulder retains capture on input loss;
unselected outputs retain their supports. This is a causal proposal, **not built
capture**: E-127 dog-fit, E-128 same-tier interference and E-132 dense-jaw failures
remain. A slipping/disconnected series joint defeats upstream braking.

| Branch | Motion/energy and grounded reaction | Explicit retention/return inventory |
|---|---|---|
| Spring-applied annulus | Motor drives while coil retracts plate; loss releases spring → plate → two disc faces → frame; friction dissipates motion | Spring, guide, release coil/switch/suppression, rotor/stator, thrust frame and wear adjustment. Bidirectional hold after force rises |
| Fluid meter-out + normally closed valve | Motor drives equal-area double-rod piston parallel to captured output; cross-port restriction resists either direction; shell reacts pressure | Opposed spring-return shutoff seats, opener, piston/rod seals, lines, restriction, charge/makeup and relief. Trapped fluid remains compliant/leaky |
| Centrifugal + spring brake | Geared flyweights overcome return springs and rub fixed drum | Weights/guides, return springs, gears/inertia and **independent spring-applied holding brake** |
| Overspeed trip + retained stop | Governor releases cocked latch; stored spring applies disc brake | Trip/return spring, mechanically retained brake, reset actuator/readback; reset only on proved parked support |
| Controls | E-140 grounded ratchet/load feedback; E-132 permanent pads | Their returns/supports/routing remain; low-load feedback and adverse kinetic drag fail respectively |

Raising/lowering keep capture intact. Spring-brake reversal crosses zero under motor
control, with closure available on loss. Fluid reversal changes pressure sign; motor
force supplies low-load lowering against viscous drag. Centrifugal friction vanishes
below engagement: the independent brake cannot disappear during reversal. A trip must
stay latched after speed falls. An open parking bolt is not instantaneous fallback.

Primary sources, accessed 2026-10-11:

- [Kendrion BFK455-25 §§3.3/4.3](https://www.kendrion.com/fileadmin/user_upload/Downloads/Datasheets_Operating_instructions/Industrial_Brakes_INTORQ/operating-instructions-spring-applied-brake-BFK455-25-2020.10.pdf): spring clamp/electromagnetic release; delay and torque
  rise differ and depend on circuit/gap/conditions. PDF retrieved/text inspected;
  industrial ratings do **not** establish miniature 1-ms response.
- [Sun counterbalance/pilot-check note](https://prod.sunhydraulics.com/wp-content/uploads/2021/01/TT_US_Ctrbal_POCk_JAN2021.pdf): nonmodulating checks differ from load controls;
  reseating leakage is finite. Indexed primary text only (PDF returned 403), supporting
  topology, not our numerical pressure/conductance/timing assumptions.
- [SUCO centrifugal explanation](https://www.suco.de/en/transmission-technology/centrifugal-clutches-and-brakes) supplies flyweight/spring/fixed-drum causality.
  [Its combinations](https://www.suco.de/en/transmission-technology/customized-solutions) include an overspeed stop with manual reset and a limiter with
  thermal static retention. Our cocked-spring implementation is a hypothesis; its
  internal geometry is undisclosed, not reconstructed here.

## Spring closure beyond first contact

Output r=2 mm; two friction faces on an 8–12-mm annulus. N=80–120 N and
static=kinetic mu=.02–.3 give **minimum equivalent output drag D=12.8 N**:
`D=2*mu*N*R/r`, using R=8 mm for any nonnegative pressure patch in the annulus.
One lost face halves this to 6.4 N, insufficient for 10 N. Maximum box drag is
432 N: strength/shock/compliance matter. Spring and coil remain real obligations.

Plate mass .02 kg, k=2 N/mm, minimum closing force N=80 N. For gap g,
instantaneous normal impacts with restitution e<1, no residual release force or
extra excitation, conservative flight bounds are
`tc=sqrt(2*m*g/N)`, `u=sqrt((2*N*g+k*g²)/m)`,
`tflight≤tc+2*m*u/N*e/(1−e)`. Ignore friction throughout contact/rebound flights.
g=.1 mm/e≤.5 gives **.67110 ms**; .4 mm/e≤.8 gives **4.03386 ms**. e→1 destroys
the bound. Coil/shaft-driven chatter is excluded; these are not restitution priors.

The **fast design obligation** adds ≤1-ms release delay and ≤1-ms 0→D rise:
full force by T=**2.67110 ms**. Slow uses 20 ms each: T=44.03386 ms. No component
has established these times. Residual magnetism, guide sticking or a latch left open
can defeat closure. Powered opening supplies roughly N*g stored energy and coil force.

Downward x positive; F=.02…10 N; effective M=.03…3 kg includes translator and all
reflected motor/rotor/transmission inertia (`J/r²`). Initial signed speed ≤.1/.3 m/s;
input is free after loss. Independent F/M describes external service force. A carried
gravitational load also requires M≥F/g; no .03-kg/10-N weight is implied. The connection
is assumed rigid, intact and backlash-free. An independent **sufficient bound**, ignoring
all braking until T, is

```
vT=v0+F*T/M
downward excursion <= v0*T+F*T²/(2*M)+M*vT²/[2*(D−F)]    (D>F)
```

It increases with F/v0/T and is convex in M, so endpoints cover the continuous box.
At 100 mm/s: **≤6.71067 mm down**. Ignoring helpful gravity bounds up by
`v0*T+M*v0²/(2*D)` = **≤1.43899 mm**. Both fit travel from **12 and 34 mm**.
Arbitrary heights still require position-dependent speed/closure guards, including
release from rest. These distances/impacts are not accepted product tolerances.

Exact signed ramp integration resolves velocity zeros, static capture, reversal and work:

| Prescribed response, D=12.8 N | Excursion relative to start |
|---|---|
| Fast, 18 cases at 100 mm/s | Worst down 6.38538 mm; up 1.38662 mm |
| Fast, F=10 N/M=3 kg/300 mm/s down | Unrestricted stop 51.22753 mm: exceeds entire stroke |
| Slow, F=10 N/M=3 kg/100 mm/s down; gravitationally admissible | 29.66953 mm: escapes from 12 mm, fits 34-mm downward clearance |
| Slow, F=10 N/M=.03 kg/100 mm/s down; external force | Crosses 40 mm during unbraked delay alone |

Unrestricted trajectories diagnose crossing, not post-impact behavior. A loose upper
bound above travel is not itself a failure witness. Inverting the bound for 12-mm
clearance/100 mm/s/F=10 N gives maximum all-off delay **3.6711 ms at M=.03 kg**,
**12.0936 ms at M=3 kg**. Choosing fast numbers is not an achieved mechanism.
Tangential compliance may let the column rebound after rotor arrest; it is absent
here and distinct from normal plate bounce. It is the next consequential holdout.

Matched control replay reuses E-140's source at r=2 mm/M=.3 kg/100 mm/s.
At F=.02 N its stack reaches the 12-mm endpoint moving; the fast prescribed spring
profile stops in **.33320 mm**. At 1 N: **2.28116/.36937 mm** respectively.
This matches equivalent inertia, not built mechanisms. E-132's independent pad
witness remains `(10−4.4−2*.02*80)/.5` = **4.8 m/s² accelerating downward**;
permanent contact alone does not establish sufficient drag.

## Fluid closure stores energy; leakage allows drift

A=20 mm², 40-mm travel, Veff=1 ml; differential C=Veff/beta. For rigid chambers
`Veff=V1*V2/(V1+V2)`; gas/hoses/seals/walls add compliance. beta={1,100,1000} MPa
is an **effective scenario range**, not oil/X1C data. Constant C omits stroke dependence
and nonlinear gas behavior. Open G0=A²/(20 N s/m); p0=20*v0/A is a driven steady
state requiring motor force `A*p0−F`, explicitly including low-load descent. On loss:

```
M*v_dot=F−A*p; C*p_dot=A*v−G(t)*p
E=.5*M*v²+.5*C*p²; E_dot=F*v−G*p²
```

G stays open 5 ms then ramps shut over 5 ms. Springs close opposed valves; powered
opener compresses them. An unbalanced 1-mm seat at 7.05 MPa needs >5.54 N before
seal/guide drag; proposed 10-N returns/.2-mm lift are allocations, **not** built valves.
E-109's weak return is not inherited. Sticking/trapped pilot pressure can defeat closing;
valve swept volume (E-109), seal friction and nonlinear pressure response are omitted.

Exact constant-G propagation with refined midpoint closure segments leaves a lossless
oscillator at ideal G=0, **a favorable mathematical control only**. At closing state:
`p_amp=sqrt((pc−F/A)²+M*vc²/C)`;
`x_extrema=xc+C/A*(F/A−pc) ± C/A*p_amp`.

| beta | Postclosure extrema over 8 signed load/inertia cases | Largest absolute differential pressure |
|---|---:|---:|
| 1 MPa | −13.7935…+59.7544 mm | 1.1100 MPa |
| 100 MPa | −1.5870…+3.7315 mm | 2.6229 MPa |
| 1000 MPa | −1.1512…+3.4710 mm | 7.0448 MPa |

Extrema are relative to initial position. Preclosure extrema are separately sampled,
not certified bounds. Low stiffness escapes stroke despite an ideal seal; stiff cases
do not settle. Symmetric 7.0448-MPa pressure swings need >3.5224-MPa common charge
plus cavitation margin, or actual makeup/accumulator circuitry. Relief/cavitation changes
the model; neither is granted. Increasing stiffness increases pressure burden.

Leak conductance rated by a **scenario** .01/.1/1 mm³/s at .5 MPa gives terminal
`v=G_leak*F/A²`. At 10 N: .0005/.005/.05 mm/s, or 1.8/18/180 mm/hour after transients.
At .02 N divide by 500; drift remains. Leakage damps oscillations while allowing creep.
A stiction/physical lock could hold but must be added explicitly. Stop hydraulic-only
indefinite arrest; retain damping for recombination. No outage allowance is inferred.

## Governor and the late-trip alternative

Two nominal .002-kg weights at rf=8 mm, drum rb=10 mm, output r=2 mm, ratio G=1/5/10
need nominal spring preload `P=m*rf*(G*.05/r)²` = .01/.25/1 N each. Springs return
weights; rotation supplies engagement work. Cross weight/preload ±20%, mu=.02/.1
coherently. Optimistic equilibrium gives
`ve=r/G*sqrt(P/(m*rf))`,
`D(v)=2*mu*m*rf*rb*G³/r³*max(v²−ve²,0)`,
`added M=2*m*rf²*G²/r²`.

Engagement is **40.82…61.24 mm/s**; for F>0 terminal speed exceeds it, never zero.
G=10 adds **5.12–7.68 kg** before drivetrain mass: it cannot inherit M≤3 kg. Nominal
G=10/mu=.1 gives 30-N drag at 100 mm/s (3 W/head); G=1 gives .03 N. Radial flight,
gear losses, guides and drum distortion are omitted. A spring brake adds static hold
subject to its own closure and **increased inertia**, not a demonstrated machine benefit.

Even without pretrigger drag, .10→.12 m/s needs
`d=M*(vtrip²−v0²)/(2*F)`: at F=.02 N/M=.3/3/6.7 kg, **33/330/737 mm**, before
tripping/braking. Last two exceed stroke. Upward motion may slow without triggering;
zero-load subthreshold coast never trips. Governor drag delays/prevents triggering.
Stop speed-only loss detection; adding power-loss spring release changes the mechanism.

## Full-display gate and decision

Reuse retains **6,400 guided outputs, service supports/returns and capture interfaces**
under 5.08-mm tops. A 24-mm annulus needs staggered/remote routing and bearings;
existing collision failures remain. H fluid heads add ≥H pistons/2H seats/returns and
seals/plumbing; H governors add 2H weights/returns, gearing and holding brakes.

Optimistic arbitrary full-stroke timing:
`T=6+ceil(6400/H)*(.04/v+.05[+.04/v empty return])`. Assumed .05-s capture/proof and
6-s preparation/registration/final proof/bounded retry/settling are unearned; acceleration
and endpoint guards add burden. At 100 mm/s, **121/229 heads** without/with return;
at 300 mm/s, **50/86**. The latter conflicts with the tested spring envelope.
With $250 shared reserve and free cells, the <$500 ceiling leaves <$2.066/$1.092 per
100-mm/s head; <$5/$2.907 at 300 mm/s. At $400 only $150 remains; free heads at $500
still leave <$.039063/site. These are joint ceilings, not prices/BOM passes. Motors,
coils/drivers, springs, bearings, valves, readers, wiring and power all count. Printing,
assembly, cooling, repair and full-map performance are unqualified.

Verify actual height **and loaded support**, not shaft/coil/valve state, before withdrawal.
On disagreement retain capture and arrest/retry locally. Passive retention must work
without sensing. False acceptance, common reader bias, frame/neighbor disturbance and
recovery timing remain unresolved; unchanged sites remain supported only causally.

All numerical friction/timing/restitution/compliance/leakage/geometry inputs are **bounds**,
not process priors or independent-cell distributions. Shared contamination, relaxation,
coil suppression, warp, batch bias and aeration may affect banks. Roughness/layer steps,
hole bias, first layers, alignment, PLA anisotropy/creep/fatigue/wear and permeability
are uncalibrated. Lost faces, stuck release or capture loss defeats the favorable box.

Self-review: ramp work/energy residual <1e−7 J; independent constant-drag limits in
both signs/zero gravity. Fluid exact solution agrees with RK4/heat quadrature (scaled
errors 2.9e−12→1.1e−14). Closure refinement 25/100/400 segments gives nominal maximum
.91333578/.91328424/.91328101 mm; exact closed-fluid period recovers state/position/energy.
These verify equations, not actual force-time profiles or hardware.

**Decision:** stop hydraulic-only indefinite holding and speed-only limiting/tripping
as complete arrest routes in these bounds. Keep damping functions and E-140/E-132
controls. Spring braking remains a **testable obligation**, not selected architecture.
Next: finite spring/plate/release geometry and elastically coupled captured output;
compare axial closure with a materially different mechanically returned release topology.
Require real release energy, force rise, rebound and frame reactions. Stop if response
exists only as a prescribed ramp or joint routing/cost/time has no credible path.
No purchase, print or staffing; an isolated brake print is currently less informative.
