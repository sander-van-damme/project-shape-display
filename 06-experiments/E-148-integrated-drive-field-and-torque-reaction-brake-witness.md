---
status: complete
builds-on: [E-147, E-129, E-140, E-142, E-145]
---

# Motor excitation can share brake release; torque reaction cannot guarantee it

**Retain field release as conditional function integration; stop the tested reaction
cam and rotor-only arrest claims.** Local excitation can exist at zero useful torque
and disappear with an isolated drive, unlike E-145's still-live shared field.
Neither excitation nor torque authenticates a correct command. No complete machine,
miniature motor, physical qualification or fabrication is selected.

Input main `5830eb0`; LAB-248. Run `python3 tools/curated-experiment-checks/E-148/integration.py`
(standard library; JSON disposable). Evidence: sourced principles, signed force/work,
connectivity and bounded state witnesses; self-review only. No assembly CAD, field/
contact solution, calibrated manufacturing prior, measurement or yield inference.

## Complete causal comparisons

Every variant retains H independent reversible drives and spatial selection, 6,400
parked supports/returns/guides, 5.08-mm tops and 40-mm travel. Capture/take load before
releasing parked support; restore/prove support before withdrawal. Frame grounding
must remain while indexing is inhibited. E-132 routing/E-142 compliance remain open.

| Combination | Motion/retention/load path | Local inventory beyond normal drive |
|---|---|---|
| Conical rotor brake | Motor field shifts rotor against spring. Off-state ring grounds rotor. Column → capture → transmission → rotor → ring → housing. | H rotor axial slides, springs, friction rings, thrust/guide bearings and wear adjustments. |
| Motor-field column jaw | Nonrotating armature in local drive field pulls linkage opening a spring jaw **on the column side of capture**. Column → pads → bracket → frame. Rotation and opening remain separate coordinates. | H armatures, links/levers, jaw returns, guides/stops/brackets; 2H pad interfaces. No separate release winding. Using rotating rotor motion instead adds H thrust-transfer bearings. |
| Torque-reaction jaw | Floating stator rocks against bilateral cam; either torque sign opens the same downstream jaw. | H stator bearings, paired cam faces/followers, centering returns, flexible leads/travel stops, plus jaw/link assemblies. |
| Separate brake control | Normal motor; independently switched coil/armature opens downstream jaw. Independent cut can close while motor stays energized. | H extra coils/magnetic circuits, release switching/suppression functions, wiring/power plus armatures/returns/jaws. Independent inhibitor hardware also counts. |

[Demag](https://www.demagcranes.com/sites/default/files/media/documents/22931549_140228.pdf)
describes axial rotor/brake integration without separate brake control.
[DE2805063A1](https://patents.google.com/patent/DE2805063A1/en) uses motor end flux
and discusses a nonrotating armature. These establish principles, not our downstream
linkage or miniature performance. [US2693254A](https://patents.google.com/patent/US2693254A/en)
uses a **separate torque motor** with ball ramps, not free main-drive reaction release.
[MIT coenergy](https://web.mit.edu/6.013_book/www/chapter11/11.7.html) supplies the
force/work method. Accessed 2026-10-11; no industrial dimensions/prices transferred.

Novelty check: E-129 pegs release rollers; E-140 relative screw motion controls a
grounded dissipative stack; E-142 uses a separate coil upstream of elasticity;
E-145 shares excitation across heads. This changes the local release variable and
support location, not the spring-brake principle. Motor-integration sources plus
reciprocal-work analysis add discrimination; no global saturation claim.

## Signed states and reciprocal work

Upward-positive shaft angle, downward-positive x, equivalent radius r=.002 m and
load F give steady `Tmotor=F*r`, `omega=−xdot/r`. Raising **and controlled lowering**
use the same torque sign; motor power `−F*xdot` changes sign. At F=10 N and
|xdot|=.1 m/s: +.020 N m, +1 W raising / −1 W lowering. Count real current control,
regenerative bus or dissipative sink. An ideal controlled motor is granted for this
screen, not constructed. At F=0, steady nonzero speed can need zero torque.
Acceleration/reversal can change torque sign without changing command validity.

Reuse E-145's **assumed**, unqualified friction boxes. Summed pad opening q has
stroke s=.4 mm, nominal spring `S=160*(.1/mu) N`, stiffness `k=40,000*(.1/mu) N/m`,
guide shunt `G=8*(.1/mu) N`; spring envelope ±20%. Minimum contact return `.8*S−G`
gives 12-N zero-field holding. Strong opening force is `1.2*S+k*q+G`.
For a bilateral cam `q=l*|phi|`, full stator travel .2 rad gives l=s/.2.
Virtual work requires `T=sign(phi)*Fopening*l` and
`W=(1.2*S+G)*s+.5*k*s²`. These are specified coordinate/force schedules, **not cam CAD**.

| mu | Peak opening force | Opening work | Peak reaction torque | Ideal pole area at 1 T |
|---:|---:|---:|---:|---:|
| .02 | 1,080 N | .416 J | 2.160 N m | 2,714 mm² |
| .1 | 216 N | .0832 J | .432 N m | 543 mm² |
| .3 | 72 N | .02773 J | .144 N m | 181 mm² |

Middle-box peak is **21.6×** the .020-N-m steady load torque. At constant .020 N m,
opening work alone needs ≥4.16 rad; .2 rad supplies only .004 J. At 1 N it needs
41.6 rad. Startup stall torque may open the jaw then disappear as speed increases:
no stable released branch follows. Single-sided cam loses one torque sign; bilateral
cam still loses release near zero torque. Added drag, preload, latch/trip or extra
travel must be counted; latching OPEN removes automatic zero-torque return.
Stop this nonlatching reaction-cam embodiment, not every torque-mediated mechanism.

Ideal uniform-gap stress `Fm=B²*A/(2*mu0)` gives 238.73 N at 1 T/600 mm², above
216 N. Motor field can supply axial force independently of useful torque, but its
winding must supply opening work too. All rotor phases, gap, saturation, leakage,
commutation, temperature and motor/brake coupling remain unbuilt. Leverage exchanges
force/travel, not work. Middle strong-spring opening work is ≥532.48 J/6,400 services;
returned spring energy needs an explicit destination, not assumed heat or free work.
All-raising 10-N/40-mm useful work is separately 2,560 J.

Executable assigned-state witnesses use B=1 T, A=600 mm² and the middle force box.
They test force availability, not actual motor transients:

| State | Field jaw | Reaction cam | Separate coil |
|---|---|---|---|
| Normal raise/lower, .020 N m | Can open | Insufficient full-release force | Open if commanded |
| Energized stall, .5 N m | Can stay open | Can stay open | Open if commanded |
| Wrong sustained command matching normal motion | Same as correct motion | Same as correct motion | Needs independent cut |
| Excitation decayed; free open-circuit rotor | Return possible | Return possible | Return if its field removed |
| Zero-load powered motion | Can stay open | No full-release reaction | Can stay open |
| Inertia/load sustains field through connected regeneration | Can stay open | Electrical reaction may hold open | Differs only with real coil isolation |

Supply loss need not remove field: discharge, eddy currents, remanence, inverter
paths and regeneration count. Last row is a possible state, not universal induction
self-excitation. Bound actual passive isolation before assuming decay. Wrong/stalled
motion needs actual output observation and independent abort, with switches, wiring,
energy handling, fault coverage and deadlines counted. No source authentication.

24 coherent corners cross mu=.02/.1/.3, extra batch preload factors .8/1.2, stroke
errors −.10/+.15 mm, field factors .7/1.2. Batch factors multiply the separate ±20%
spring envelope: deliberately wider bounds, not random independent errors. Opening
margin spans **−1,185.02…+285.91 N**; zero-field hold **9.44…14.56 N**. Common weak
preload helps release but loses 10-N hold. Fractions of corners are not yield.

## Downstream support and finite return

Connectivity enumeration: a closed motor brake leaves **no column ground path** after
transmission or capture separation. A closed column jaw keeps that path if its own
pad/bracket/frame survives. Broken jaw defeats it; upstream head-rod grip does not
implement it. A broken pull link can fail closed only with return at the jaw;
seizure/spring fracture differ. Graph connectivity proves neither stiffness nor
capacity. Even intact capture can retain E-142's downstream elastic escape.

Conditional return model: impose `B(t)=Br+(1−Br)*exp(−t/tau)` throughout motion,
A=600 mm², minimum return 120 N, armature mass .02 kg, zero initial opening velocity.
**No electrical transient is solved.** Wait until Fm≤10 N, then ≥110-N return closes
.4 mm within `sqrt(2*.0004*.02/110)=.3814 ms`, assuming bounded stroke and no rebound.
Contact thereafter gives ≥11-N friction in this model. Crediting asymptotic 12 N at
first contact would overstate arrest. Residual field can prevent the 11-N threshold.

Signed output witness: free before contact; constant grounded Coulomb capacity C
afterward. At delay t, `x=v*t+.5*F*t²/m`, `u=v+F*t/m`; C>|F| gives extra signed
slide `sign(u)*.5*m*u²/(C−sign(u)*F)`. Checks include reversal before closure and
kinetic + gravity work = heat. F and effective m are independent generalized bounds;
real payload requires corresponding reflected inertia. C≤|F| cannot guarantee hold.

F=10 N, m=1.1 kg, initial downward .1 m/s, C=11 N:

| tau / Br | Conditional delay to ≥11-N contact | Model stopping excursion |
|---|---:|---:|
| 1 ms / 0 T | 1.968 ms | 7.858 mm |
| 10 ms / 0 T | 16.245 ms | 36.565 mm |
| 10 ms / .1 T | 21.898 ms | 53.563 mm |
| 100 ms / 0 T | 159.019 ms | 1,444.78 mm, unrestricted diagnostic |
| any / .3 or .6 T | No 11-N threshold | Asymptotic capacity 9.851 / 3.406 N |

Large conservative excursions **cannot certify 40-mm containment**; they are not proof
that a real jaw travels that far. Initial height further limits clearance. No accepted
outage distance or post-end-stop dynamics. .3/.6-T cases separately fail static 10-N
hold in the weak-return model. Bounce, field/motion coupling and friction evolution
are missing. Another 36 cases cross F=0/.02/1/10 N, v=−.1/0/+.1 m/s, accessible
energy E=0/5/50 mJ, granting 10-ms delay/12-N capacity. E is inserted at contact in
the motion direction, not also counted as inertia. Extrema −5.625…+36.477 mm are
scenario results, not elastic dynamics or a repair of E-142. Zero load still coasts.

## Full-display gate and decision

Count H winding sets/rotors/transmissions/drivers and output/support observations;
shared readers need scan/routing time. Count common independent abort, discharge,
supply/wiring and supported recovery of healthy heads it interrupts. Integration
removes a powered release channel, not opening coordinates/returns/fits. Inventory
above excludes no pad wear, winding/iron fabrication, alignment, assembly, print
failure, cooling, calibration or accessible repair; none is priced here.

Sequence: capture/proof-load → prove jaw clear → release parked support → controlled
motion/top observation → restore/prove support → field off/jaw proof → withdraw.
Failed proof inhibits indexing and aborts; retain capture and restore support before
one bounded retry. Loss of capture plus jaw has no demonstrated recovery. Shaft/current
readback cannot prove support. Common bias is unbounded; assumed false-accept p gives
6,400p expected misses without independence (.64 at p=1e−4), not measured reliability.

Optimistic `T=6+ceil(6400/H)*(.45+t_extra)` grants .4-s motion, .05-s local work and
6 s preparation/registration/transport/final proof/retry/settling. No measured timing
or earned overlap. Extra .0/.01/.05/.10 s requires **121/124/137/149 heads** for
strict <30 s; .4-s empty return raises these to 229/238/247/256. With hypothetical
$250 elsewhere/free cells, complete head purchase ceilings are **$2.066/$2.016/$1.825/
$1.678** including motors. Joint `H*c_head+6400*c_cell+c_shared<500`; free heads and
$250 shared permit only <$.039063/cell. No BOM/regional-isolation pass; parked
neighbors retain support but frame disturbance remains unproved.

Bounds are not X1C/PLA process priors. Hole/layer/first-layer/warp/alignment errors
couple clearance and magnetic gap; contamination couples friction/guide drag;
creep/fatigue/anisotropy/interlayer weakness/wear alter returns. Common errors cannot
average over heads. Field-model uncertainty is separate. No qualified .4/.2-mm-nozzle
geometry, yield, lifetime or reason to print before constructing the load path.

**Decision:** retire tested reaction cam and rotor-only containment; retain field-driven
downstream jaw as a conditional excitation-loss improvement. No miniature-motor detailing.
Reopen with finite column-side jaw/frame/link, all-state field margin, bounded passive
field removal, loaded arrest and joint cost/time. Powered stall/wrong command still
needs independent proof/abort; no hidden powered release permitted.

**Next axis: retention without a released capture path.** Compare resident magnetic
height detents with spatial noncontact writing, travelling strain-wave friction drive
on a resident rail, and low-lead screw control. Cross-check E-138/A-016, E-131/A-007
and vibration work before novelty claims. Seek persistent grounded barriers during
writing, including wrong excitation, zero-load inertia, power loss and neighbors.
Bound stress, work, 40-mm travel, per-cell inventory and addressing first; these are
hypotheses, not machine passes. Broaden architecture instead of another brake return.

Self-review: signed steady power; both-sign 16/64/256 midpoint virtual-work sums
within 3e−17 J (exact linear integral); graph disconnection limits; signed stopping
limits/energy residual <1e−10 J; strict integer schedules. No time-step simulation
or independent hardware validation claimed.
