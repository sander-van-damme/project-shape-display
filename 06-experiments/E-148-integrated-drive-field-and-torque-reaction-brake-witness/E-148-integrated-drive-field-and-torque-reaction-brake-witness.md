---
status: complete
builds-on: [E-147, E-129, E-140, E-142, E-145]
---

# Motor excitation can share brake release; torque reaction cannot guarantee it

**Retain motor-field release only as a conditional function integration; stop the
bounded torque-reaction cam and rotor-only arrest claims.** Field excitation can
exist at zero useful torque and disappear with an isolated local drive. This differs
from E-145's shared field remaining live after local drive loss. Neither excitation
nor torque authenticates a correct command, and a rotor brake cannot arrest a
separated column. No complete machine, miniature motor or fabrication is selected.

Input main `5830eb0`; LAB-248. Reproduce: `python3
tools/curated-experiment-checks/E-148/integration.py` (standard library; disposable JSON).
Evidence: sourced principles, signed force/work calculations, connectivity and
bounded state witnesses. Self-review only. No manufactured motor, assembly CAD,
field/contact solution, calibrated prior, physical measurement or yield claim.

## Architectures, sources and causal boundary

All head options use H independent reversible drives and spatial addressing. Capture
and take load before releasing a parked support; move; restore/prove support; withdraw.
Retain 6,400 parked supports/returns/guides, 5.08-mm tops and 40-mm travel. The ground
frame must carry head-pad reaction while indexing is inhibited. E-132 routing and
E-142 compliant capture remain unresolved, not inherited passes.

| Combination | Motion, retention and actual ground path | Additional local mechanisms |
|---|---|---|
| Conical rotor / motor brake | Same energized motor field shifts rotor against spring; rotor friction ring grounds shaft when off. Column → capture → transmission → rotor → ring → housing. | H axial rotor slides, springs, friction rings, thrust/guide bearings and wear adjustment; H winding sets/drivers remain. |
| Motor-field **column jaw** | A nonrotating armature in each drive's field pulls a linkage opening a spring jaw **on the column side of capture**. Column → pads → jaw bracket → fixed frame. Rotation stays independent of opening coordinate. | H armatures, pull links/levers, jaw returns, guides/stops and grounded brackets; 2H pad interfaces. A rotating rotor alternative adds H thrust transfer bearings. No separate release winding is credited or needed in the causal sketch. |
| Torque-reaction column jaw | Stator rocks against a double-sided cam. Either torque sign lifts the same jaw return. Cam and jaw react into frame. Drive rotor still moves the capture. | H floating stator bearings, paired cam faces/followers, centering returns, cable flex paths, travel stops and jaw/link assemblies. |
| Separate local brake control | Normal motor plus a locally switched coil/armature opens the same downstream jaw. Independent release cut can close it while motor remains powered. | H extra coils/magnetic circuits, H release switching/suppression functions, wiring, power, armatures/returns and jaw assemblies. An independent inhibitor is additional hardware. |

[Demag's motor description](https://www.demagcranes.com/sites/default/files/media/documents/22931549_140228.pdf)
describes axial rotor displacement and a mechanically connected brake without a
separate brake controller. [DE2805063A1](https://patents.google.com/patent/DE2805063A1/en)
uses motor end flux for spring-brake release and discusses a nonrotating armature.
These establish integration principles, not our downstream linkage or miniature
performance. [US2693254A](https://patents.google.com/patent/US2693254A/en) uses a
**separate torque motor** and ball ramps; it is not evidence of free main-drive
reaction release. [MIT coenergy](https://web.mit.edu/6.013_book/www/chapter11/11.7.html)
provides the force/work method. Sources accessed 2026-10-11; no dimensions, prices
or process capability transferred from industrial devices.

Novelty check: E-129 pegs release rollers; E-140 relative screw motion controls a
grounded dissipative stack; E-142 uses a separate coil upstream of elasticity;
E-145 shares field across heads. Motor-integration sources and reciprocal-work
analysis change the release variable and location, not the spring-brake principle.
No new mechanism or broad search-saturation claim.

## Signed operation: power loss, stall and wrong command differ

Use upward-positive shaft angle, downward-positive output displacement x, radius
r=.002 m, downward generalized force F. With the jaw clear and intact bilateral
capture, steady raising **and controlled lowering** require `Tmotor=F*r` and
`omega=−xdot/r`. Consequently motor work is `Tmotor*omega=−F*xdot`: lowering must
absorb load energy. At F=10 N and |xdot|=.1 m/s, torque is +.020 N m in either
motion direction; power is +1 W raising / −1 W lowering. The drive needs a real
regenerative bus or dissipative sink, current regulation and power accounting.
This grants a controlled motor as a comparison assumption, not a built controller.

Torque is not proportional to speed. At F=0, constant nonzero speed can require
zero torque in the ideal low-loss limit. Acceleration/reversal can change torque
sign without changing command validity. A single-sided stator cam therefore loses
release on one sign; a bilateral `q=l*|phi|` cam still closes around zero torque.
Friction or a deliberate motor load could maintain reaction, but becomes an
explicit permanent dissipation source. Latching the cam open removes automatic
zero-torque return unless another trip is supplied.

A motor can maintain field while developing either signed torque or zero torque.
The table is an executable **force-availability witness**, not a motor controller
simulation. Field=1 T on 600 mm² and torque magnitudes are assigned states:

| State | Motor-field jaw | .2-rad reaction cam | Separate coil |
|---|---|---|---|
| Normal raise/lower, .020 N m | Sufficient opening force in middle box | Insufficient full-release force | Open if commanded |
| Energized stall, .5 N m | Remains open | Can remain open | Remains open if commanded |
| Wrong sustained command identical to normal motion | Indistinguishable from correct motion | Same response as correct motion | Needs independent cut |
| Field actually decayed, open-circuit free rotor | Spring return possible | Spring return possible | Return if its field removed |
| Zero-load powered motion | Can remain open | No full-release reaction | Can remain open |
| Residual inertia/load maintains excitation through connected regeneration path | May remain open until energy/field decays | Electrical reaction may maintain release | Local coil isolation can differ, if built |

Supply loss need not remove field: discharge, eddy currents, remanence, inverter
paths and regeneration count. The regeneration row is a possible state, not universal
induction-motor self-excitation. Bound actual passive isolation before assuming
field decay. Powered wrong/stalled motion needs real output observation and an
independent abort; switch, wiring, energy sink and deadlines must be counted.

## Reciprocal force/work screen

Reuse E-145's explicit friction alternatives, not product service ratings or measured
PLA coefficients. Let q be the summed jaw-opening coordinate, stroke s=.4 mm, and
`S=160*(.1/mu) N`, `k=40,000*(.1/mu) N/m`, guide shunt `G=8*(.1/mu) N`.
Spring manufacturing scenario is ±20%. Weak return at contact is `.8*S−G`;
strong opening force is `1.2*S+k*q+G`. All three boxes give 12-N minimum zero-field
holding capacity for a 10-N comparison load.

A cam with full stator motion |phi|=.2 rad has `l=s/.2`. Virtual work requires
`Treaction=Fopening*l`; opening work `W=(1.2*S+G)*s+.5*k*s²` cannot disappear
through a lever. Opposite phi gives opposite signed torque and the same positive
work. These are finite coordinate/force schedules, **not constructed cam contacts**.

| Assumed mu | Peak opening force | Opening work | Peak cam reaction | Ideal pole area at 1 T |
|---:|---:|---:|---:|---:|
| .02 | 1,080 N | .416 J | 2.160 N m | 2,714 mm² |
| .1 | 216 N | .0832 J | .432 N m | 543 mm² |
| .3 | 72 N | .02773 J | .144 N m | 181 mm² |

Middle-box peak is **21.6 times** the .020-N-m steady load torque. Even constant
.020 N m would require ≥4.16 rad to supply opening work, before loss; a .2-rad
reaction stroke supplies only .004 J. At 1 N the work-only rotation becomes
41.6 rad. Startup stall torque can open a jaw, then drop below its holding
threshold as the drive accelerates; this does not establish stable sliding
operation. Stop the tested nonlatching reaction cam. More cam travel or a separate
preload source changes the implementation; neither solves zero-torque continuous
motion or live wrong-command discrimination by itself.

For an ideal uniform gap, `Fm=B²*A/(2*mu0)`; coenergy implies that armature motion
also loads the exciting winding. At A=600 mm², B=1 T, force is 238.73 N, exceeding
216 N. This is only a necessary force allocation, not a motor design: integrated
flux must furnish it at every rotor phase, motor torque, temperature and jaw gap.
Commutation with field zeros, saturation, leakage, winding loss and motor/brake
cross-coupling can defeat it. Leverage reduces force while increasing travel; it
cannot delete .0832 J/opening or return storage. Releasing each of 6,400 outputs
once costs ≥532.48 J of opening work at the middle **strong-spring** corner, before
useful movement. Potentially recovered spring energy must be explicitly routed;
it is not all necessarily heat. At 10-N all-raising load, useful work is 2,560 J.

24 coherent corners cross mu=.02/.1/.3, extra batch preload factors .8/1.2,
stroke errors −.10/+.15 mm, and field factors .7/1.2 relative to 1 T. Batch
factors multiply the separate ±20% spring envelope; they are a deliberate wider
stress test, not independent random tolerances. Opening margin spans **−1,185.02
to +285.91 N**; zero-field contact capacity spans **9.44–14.56 N**. Weak common
preload loses the 10-N hold despite making release easier. No proportion is yield.
Local fit faults and common bias must both be considered.

## Ground connection, finite return and energy remaining at the output

The graph enumerates motor/shaft/capture/column/ground edges. Closing a motor brake
leaves **no column-to-ground path** after transmission or capture separation.
Closing a direct column jaw preserves that path when either drive edge breaks,
provided its independent jaw/frame path survives. A broken jaw contact defeats it.
Connectivity is necessary, not evidence of stiffness, capacity, placement or contact
continuity. In particular, gripping a head rod upstream of capture does not implement
this column jaw. A pull-link break can fail closed only if its return is located at
the jaw; seizure, wedging and broken springs remain distinct faults.

Finite conditional return screen: impose a gap-field envelope
`B(t)=Br+(1−Br)*exp(−t/tau)`, A=600 mm², middle-box minimum spring/guide return
120 N, armature mass .02 kg, initial opening velocity zero. **This envelope is an
assumption through motion**, not an electrical or field transient solution.
Wait until magnetic force ≤10 N, leaving ≥110 N toward closure. Then s=.4 mm
closes within `sqrt(2*s*.02/110)=.3814 ms` under the ideal no-rebound contact model.
After contact it guarantees ≥11 N friction only within these assumptions. Using
asymptotic 12-N capacity immediately at first contact would overstate the result.

Exact signed output model: free motion before this delay, then constant 11-N
Coulomb opposition. For force F, mass m and velocity v, closure position/speed are
`x=v*t+.5*F*t²/m`, `u=v+F*t/m`; with C>|F|, subsequent signed slide is
`sign(u)*.5*m*u²/(C−sign(u)*F)`. The model checks kinetic + gravity work = friction
heat, detects pre-contact reversal, and includes both motion signs. C≤|F| cannot
guarantee hold. Load force and effective inertia are independent generalized
scenarios; a real payload needs its corresponding reflected inertia.

At F=10 N, m=1.1 kg and initially .1 m/s downward:

| tau / residual Br | Conservative model delay to ≥11-N contact | Model stopping excursion |
|---|---:|---:|
| 1 ms / 0 T | 1.968 ms | 7.858 mm |
| 10 ms / 0 T | 16.245 ms | 36.565 mm |
| 10 ms / .1 T | 21.898 ms | 53.563 mm |
| 100 ms / 0 T | 159.019 ms | 1,444.78 mm, unrestricted diagnostic only |
| any / .3 or .6 T | No 11-N threshold | Asymptotic hold only 9.851 / 3.406 N |

Large unrestricted excursions show that these conservative bounds **cannot certify
40-mm containment**, not that the actual jaw must travel this far. A starting
height also limits available downward clearance. No post-end-stop dynamics or
accepted outage distance is invented. .3/.6-T residual cases have a separate static
10-N failure in the specified weak-return model. Contact bounce, frame deformation,
friction evolution and actual field decay can change results.

A separate 36-case signed ledger crosses F=0/.02/1/10 N, v=−.1/0/+.1 m/s and
accessible downstream energy E=0/5/50 mJ, granting a 10-ms delay and 12-N capacity.
Energy is inserted at contact in the motion direction; it is not counted again in
mass/inertia. Excursion extrema span −5.625…+36.477 mm. A zero-load output still
coasts and dissipates kinetic energy. This envelope is not elastic dynamics or a
repair of E-142. With a rotor brake alone, compliance already downstream must still
be resolved even when every connectivity edge remains intact.

## Machine accounting, proof and disposition

Every variant retains H winding sets/rotors/transmissions/drivers and real output/
support observations; shared readers need scan/routing time. Count independent common
abort, discharge/supply/wiring and recovery of healthy heads it interrupts. Integration
removes a separate release channel, not H opening coordinates/returns/fits. Count all
6,400 supports/returns/guides, pad wear, winding/iron fabrication, alignment, assembly,
print failures, cooling, calibration and accessible repair; none is priced here.

Sequence: capture/proof-load → prove jaw clear → release parked support → controlled
motion/top observation → restore/prove parked support → field off/jaw proof → withdraw.
Failed proof inhibits indexing and aborts while capture is retained; restore support
before one bounded retry. Loss of both capture and jaw has no demonstrated recovery.
Shaft/current readings cannot prove output support. Common reader bias is unbounded;
assumed false-accept p implies 6,400p expected misses without independence (.64 at
p=1e−4), not a measured failure rate. Proof/retry hardware and time remain obligations.

Optimistic whole-map schedule remains `T=6+ceil(6400/H)*(.45+t_extra)`: .4-s full
stroke at .1 m/s, .05-s local operations, six seconds for preparation, registration,
transport, final proof, bounded retry and settling. None is earned overlap or a
measured allocation. Extra release/proof/return .0/.01/.05/.10 s needs
**121/124/137/149 heads** for strict <30 s; adding .4-s empty return needs
229/238/247/256. At a hypothetical $250 non-head reserve and free cell hardware,
complete head purchases must be below **$2.066/$2.016/$1.825/$1.678**, including
motors. More generally `H*c_head+6400*c_cell+c_shared<500`; even with free heads
and $250 shared, cell purchases must be <$.039063. No joint BOM or regional
isolation pass; unchanged columns remain parked but frame disturbance is unproved.

These are bounds, not X1C/PLA process priors. Hole/layer/warp/alignment errors couple
jaw clearance and magnetic gap; contamination couples friction and guide drag;
creep/fatigue/anisotropy/interlayer failure/wear alter returns. Shared batch errors
cannot average over heads. Field-model uncertainty is separate. No yield/lifetime,
qualified .4/.2-mm-nozzle parts or fabrication proposal follows.

**Decision:** stop the bounded reaction-cam implementation and rotor-only fault
containment. Retain field-driven downstream release as a conditional causal
improvement for actual excitation loss; do not develop a miniature motor now.
Reopening needs a finite column-side jaw/frame/link construction, opening force
through all motor states, bounded passive field removal, loaded return/arrest and
joint cost/timing. Stall/wrong-command protection still needs independent observation
and interruption; no extra powered release may be silently introduced.

**Next learning axis: retention without a released capture path.** Compare a resident
magnetic height-detent track with a spatial noncontact writer, travelling strain-wave
friction drive against a resident rail, and resident low-lead screw control. Ask which
puts a persistent grounded energy barrier directly at the column during writing,
including wrong sustained excitation, zero-load inertia, power loss and neighboring
columns. Cross-check E-138/A-016, E-131/A-007 and existing vibration work before
crediting novelty. These are hypotheses, not reopened machine passes. Bound field/
contact stress, 40-mm work, per-cell inventory and addressing before detailed design.
This broadens the physical architecture rather than tuning another brake return.

Self-review: signed steady power for both directions; 16/64/256 midpoint virtual-work
sums agree within 3e−17 J (linear integrand, exactly integrable); graph disconnection
limits; zero-force/friction stopping formulas; signed energy residual <1e−10 J;
strict integer head counts. No time-step simulation is used. These verify the stated
reduced equations, not their transfer to hardware or independent validation.
