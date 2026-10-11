---
status: complete
builds-on: [E-146, E-144, E-140, E-139, A-014, E-109]
---

# Local work bounds reset only with an irreversible debit and isolated return paths

**Stop shared-recharged packets; retain only a conditional reset-energy bound.**
Local work can come from inertia, returned springs or gravity after power loss.
Source disconnection, nonrepeat and arrest are separate requirements. No machine
selection, accepted outage travel or fabrication follows.

Input main `8f0239c`; LAB-247. Reproduce with Python 3 standard library:
`python3 tools/curated-experiment-checks/E-147/authority.py`.
Evidence: explicit connection intervals, finite reset-state search, conservative
energy ledgers and analytical bounds. Self-review; no assembly CAD, calibrated
process distributions, contact dynamics, measurements or independent validation.

## Compared causal architectures

All variants keep H independent drives, spatial selection, 6,400 parked supports/
returns/guides, top/support proof and bounded retry. Arrest must act beyond compliant
capture. E-146's grounded catch is a comparator; E-132/E-142 earn no new pass.

| Encoding | Causal operation, ground path and reset |
|---|---|
| Mechanical work handshake | With output grounded on a catch, an input cam disengages its motion dog, winds a spring through a ratchet and advances a one-shot latch. Separated delivery toggles the catch once. Web → bolt → ground slide bounds motion. Coast/returned energy can do reset work. Gravity isolation and nonrecovered debit are unbuilt. |
| Flying capacitor | Charge with delivery open; disconnect source; connect capacitor to a local release coil. Repeated charge refreshes permission. Grounded catch and spring return remain separate. |
| Spring cartridge | Source dog winds while delivery dog is open; changeover disconnects source before delivery. A latch can retain OPEN indefinitely after spring work; returned energy can rearm. Needs trip, catch and proved return. |
| Fluid accumulator | Close inlet before connecting the opening chamber. E-144 bleed/return closes only while supply stays isolated; shared recharge refreshes permission. Sealed pressure may hold OPEN indefinitely. |
| Finite exhaust receiver | Output piston expels liquid into a bounded receiving piston; its endpoint returns pressure force to ground. Volume constrains motion. Emptying/reconnecting repeatedly restores the walk; A-014/E-109 remain parked. |

Sources (2026-10-11): [Analog Devices](https://wiki.analog.com/university/courses/electronics/text/chapter-15)
describes alternating switches and break-before-make; [Parker's manual](https://www.parker.com/content/dam/Parker-com/Literature/Accumulator---Cooler-Division---Europe/service-manuals/accumulator/sb/MSG10_0609_SBManual.pdf)
separates accumulator/source/tank ports. These motivate topology, not miniature
manufacturability, fault containment or one-shot reset.

Search moves: energy-converter port switching; input work as causal reset evidence;
inversion from supplying energy to accepting finite exhaust volume. The last returns
to A-014's known trapped-volume constraints. No new storage principle or broad search
saturation is claimed.

## Source disconnection and reset-state witnesses

A hypothetical 1-mm transfer slide has charge contact closed for `q<=.4 mm` and
delivery contact closed for `q>=.6 mm`. Between them both are open. Graph edges are
`source—store` and `store—release actuator`; springs use dogs, capacitors switches,
fluid valves. This is a **specified contact schedule**, not generated solid geometry.
For all q, nominal source and delivery never connect. Adverse edge shifts ±e leave
separation `.2−2e mm`: .20/.15/.10/0/−.10 at e=0/.025/.05/.10/.15 mm.
At zero separation simultaneous contact is conservatively allowed. Exact interval
intersection agrees with 2,001 phase samples. One stuck charge contact creates a
live source path throughout delivery despite perfect nominal nonoverlap.

Recharge requires grounded support before disengaging the motion dog. A seat flag
proves neither force nor torque isolation. A jammed dog leaves gravity connected;
an ideal one-way clutch is not supplied to repair raising/lowering/reversal paths.

Executable cycle: `supported → charging → isolated/armed → released → spent/seated`.
An initially charged one-shot gives **one firing under held FIRE**. Alternating charge,
isolate, fire and seat gives **20 firings**. All store types share this command trace.
Even perfect readback of each seat accepts it. Twenty permissions can admit E-146's
40-mm walk; this state model does not claim an unloaded column moves without energy.

Breadth-first search separates RELEASE, unpowered SEAT, shared CLOSE and local WORK.
At depth 16 it finds 6 firings for seat-reset and 4 for edge-reset; the repeat cycle
extends indefinitely. Two residual work units plus an armed permission allow **3
firings** even with WORK-only reset. Seat/motion creates no work units. The 33/25/18
visited states verify the abstraction, not a physical guard or sensor.

## Local work is not proof of a live source

Let a reset cross a work barrier W, return fraction rho of that work to the local
input store, and receive fraction gamma of gravity work F*s from each downward packet.
For source disconnected and successful packets:

`E_next = E − (1−rho)*W + gamma*F*s`, with `E>=W` before firing.

Cycle energy/heat balance is checked. This is an energy-possibility witness,
**not a synthesized cam orbit**; forward cam motion cannot identify its energy source.

| Scenario, s=2 mm | Result within 20 attempted packets |
|---|---|
| E=5 mJ, W=1 mJ, rho=gamma=0 | 5 authorizations, permitting 10 mm |
| E=W=1 mJ, rho=1, F=0 | 20 authorizations; no net energy consumption. No zero-load motion inferred. |
| E=W=1 mJ, rho=0, gamma=.5, F=1 N | 20 downward packets energetically possible; gravity replenishes every 1-mJ debit |
| E=0 initially, live charger refills W each cycle | 20 authorizations independent of drive power |
| E=1.25 mJ, W=1 mJ, gamma=.5, F=.02 N | 1 authorization; only .27 mJ remains |

The strict depletion condition for this periodic ledger is
`w=(1−rho)*W > gamma*F*s`. If it fails and the first barrier is affordable, depletion
does not stop repetition. If it holds, count still depends on residual energy. It is
not enough to impose a spring barrier W while crediting its returned energy nowhere.
At 10 N and 2 mm, gravity supplies **20 mJ/packet**. A 1-mJ debit needs gamma<.05
merely to deplete; proving gamma=0 requires separation through *all* relevant phases.

Normal controlled lowering often absorbs work from the load; the same gravity can
supply shaft/reset work after power loss. This cross-checks E-140's free-input brake
and E-139's cam. A work sensor would need signed integration, power, registration,
false-accept analysis and a counted release inhibitor. A motor deliberately powered
but wrong is a different fault requiring an independently enforceable supply stop.

For the favorable **zero-backfeed** case, suppose each new reset irreversibly spends
at least w and all accessible residual energy at loss is bounded by Eu. At any failure
phase allow one already armed/partly completing packet. Then
`N<=1+floor(Eu/w)`; the current 2.4-mm window plus N shifts gives
`D<=2.4+2*N mm` before elasticity, including an unfinished selector stroke.
Each permitted transition, including the already armed one, adds up to 2 mm.
Reversal cannot restore credit; dwell adds none. This does not establish settling
or an acceptable outage distance.

Scenarios: rotor omega=50 rad/s, J=1e−6…1e−5 kg m² gives **1.25…12.5 mJ**;
capture stiffness 100,000 N/m with .1/1-mm deflection adds **.5/50 mJ** if accessible
through the reset train. Such energy must be counted once, not assumed absent because
the motor supply was removed. The 18-case sweep crosses J, deflection=0/.1/1 mm,
and w=1/5/20 mJ. With no capture energy and w=1 mJ, N<=2/13 and D<=6.4/28.4 mm.
With 1-mm capture deflection, N<=52/63: no useful 40-mm stroke protection follows.
At w=20 mJ the latter bounds become N<=3/4, D<=8.4/10.4 mm, still before impact.
These bounds do not establish reachable trajectories.

No manufactured lower bound w is established. Common friction loss, spring return,
ratchet wear or cam errors can remove it. Buying a bound with dissipation costs at
least **134.4/672/2,688 J/map** at 134,400 resets and w=1/5/20 mJ, before useful work.

## A finite release store does not constrain gravitational travel

Ideal 5-mJ stores: 10,000-N/m spring at 1-mm compression; **69.44-µF** capacitor
at 12 V; **10 mm³** delivered at constant .5 MPa (not an unspecified gas accumulator).
Conversion/force margins add capacity; these do not meet E-144's .416-J opening
corner. A latch or sealed chamber can maintain OPEN without continuous energy use.

At F=0, an unrestrained output with .1-m/s velocity crosses 40 mm in **.4 s** despite
zero new input energy. Either velocity sign coasts toward its corresponding endpoint;
at zero force AND zero speed it remains still. At F=1 N, m=1.1 kg and zero speed,
gravity alone crosses 40 mm in **.29665 s**, releasing .04 J. At 10 N it releases
.4 J. The exact constant-force witness includes initial signed velocity −.1/0/+.1
m/s and F=0/.02/1/10 N; upward motion can reverse. Force and effective inertia are
independent generalized scenarios, not a silent counterweight specification.

Arrest still requires the grounded path. For the E-146 catch used only as a control,
`Ehit=.5*m*v²+Fs*d+Es`, and `.5*k*delta²=Ehit+Fs*delta`, where Fs is signed toward
that catch. If Ehit<0, the output turns before that catch and may approach the other
one later. With m=1.1 kg, |v|=.1 m/s, d=2.4 mm, k=100,000 N/m, downward F=10 N
and Es=.05 J: **delta=1.36491 mm**, total 3.76491 mm, peak 136.49 N. Es is capture/
drive elastic energy beyond the removed supply. Zero-force and opposite-motion cases
are checked separately. This reuses the energy root, not E-146's strength as a pass.
No specified sink means rebound; no qualified catch means no hardware arrest claim.

## Inverting the packet: finite volume accepted from the load

A 2-mm-bore output piston expels liquid into an isolated receiver with grounded
end stops. Its **6.283 mm³** capacity permits 2-mm descent in the rigid, incompressible,
sealed limit: `A*x<=Vremaining`. Reaction: output piston → liquid → receiver piston
→ stop → frame. Opposite motion needs a second chamber/stop; an open tank defeats it.

For total connected volumetric compliance C and outward leak Q, a quasi-static
30-s diagnostic is `x=(Vremaining+C*F/A+Q*t)/A`. At 10 N the 2-mm piston needs
**3.183 MPa**, already outside E-144's .5-MPa illustration. Explicit competing
bounds C=0/1e−15/1e−14 m³/Pa and Q=0/1e−12/1e−10 m³/s give **2…13.087 mm**;
C=1e−15 alone adds 1.013 mm. This is not a dynamic upper bound: inertia can exceed
static pressure/compression, gas is nonlinear, and any sustained leakage removes an
indefinite position guarantee. None of these values is a measured material prior.

Emptying requires prior output isolation/support. Shared empty/reconnect cycles
restore the walk. Resident versions repeat 6,400 pressure boundaries/isolations;
reusable heads need docking. Stop: A-014/E-109's return, seal and cost failures remain.

## Whole-machine gate, uncertainty and next axis

Minimum additional inventory per H heads, beyond H drives, 6,400 parked supports/
returns/guides, capture and grounded output catches:

- Mechanical handshake: H winding cams/ratchets, H source/output disconnects,
  H packet springs, H nonrepeat latches, H qualified loss elements and latch returns;
  catch-return springs remain separate where used. The cam drives selector motion
  from the existing motor only if its actual phased transmission is constructed.
- Capacitor: H capacitors, H release coils, H local return springs, **2H switched
  connection functions** plus gate/control circuitry. Bidirectional isolation may
  require multiple devices per function; a diode is not assumed to block both ways.
- Fluid: H stores, **2H isolation/delivery functions**, H release chambers with moving
  boundaries/returns and H bleeds if finite depressurization is claimed, plus source.
- All variants: actual top/support observation for each serviced output, local fault
  identification and at least one common source-abort path. H observations need not
  mean H purchased readers, but scan/routing/latency cannot disappear. Common abort
  stops healthy heads too; still-supported handback and bounded retry must be timed.

Stuck-high, repeating recharge, welded branches and common threshold shifts are
different correlated faults. Edge errors, recovery and energy ranges are assumptions,
not X1C priors. Hole bias, layer steps, warp, roughness, alignment, strength, creep,
fatigue and wear have no calibrated mapping to these interfaces. No yield or board
reliability is inferred.

Keep 5.08-mm tops, 40-mm travel and 6,400 outputs. The optimistic inherited schedule
`T=6+ceil(6400/H)*(.45+21*t_reset)` includes .4-s motion, .05-s local capture/proof,
and six seconds for preparation, registration, transport, final proof, retry and
settling. It has no earned overlap/empty return or measured overhead. Reset overhead
0/5/10/20/50 ms requires **121/149/178/238/427 heads** for strict <30 s. With a
hypothetical $250 elsewhere, complete per-head purchases must stay below
**$2.066/$1.678/$1.404/$1.050/$.585**, even with free cell hardware. Every bought
spring, switch, drive, reader, wire and abort counts in joint <$500 purchases.
No BOM, route, schedule or regional-isolation pass.

**Decision:** close this energy-packet screen. Do not detail the yoke, add free local
releases, print or buy. Reopen the mechanical bound only with actual nonrecovered
reset work, gravity isolation throughout motion/reset, bounded residual energy and
beyond-capture support/impact. Reopen storage variants only with a changed complete
reset/isolation architecture; changing energy medium alone adds no protection.

**Next: combine local drive and return functions.** [Demag's conical-rotor motors](https://www.demagcranes.com/en/products/drives/motors/conical-rotor-brake-motors)
use a rotor/brake connection without separate brake control (manufacturer description,
2026-10-11). This industrial analogy proves no miniature scaling or cost. Compare
motor-field spring brake, torque-reaction brake and counted separate brake. Construct
local-loss, energized-stall, broken-transmission and elastic-capture ground paths;
count coils, springs, bearings, controls and shared abort. A rotor brake cannot hold
a disconnected column. Stop if it needs an assumed downstream actuator. This changes
function integration, not recharge encoding; no winner is presumed.

Self-review: exact contact-interval versus phase sampling; exhaustive bounded reset
search; cycle energy residuals <1e−12 J; ballistic and zero-force limits; signed
catch quadratic residuals <1e−11 J; spring/capacitor/pressure-volume units; strict
integer head schedule. These analytical/event models need no integration time step.
Fluid result is explicitly static. Source model, not generated JSON, is retained.
