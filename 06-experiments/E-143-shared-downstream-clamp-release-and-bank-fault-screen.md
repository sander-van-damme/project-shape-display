---
status: complete
builds-on: [E-142, E-132, E-109]
---

# Shared release saves commands, not clamp work or independent arrest

**Stop the rigidly tied crossbar, single common-return fault paths and the sourced
motor/release combinations below.** Unilateral lifters and separate slack tendons
isolate a stuck follower *if the common member returns*, but do not survive that
member staying open. No embodiment earns a finite transient/contact build yet.
This does not reject all shared releases or inexpensive motors. No machine selected.

Input main `c7bbb97`; Python 3 standard library:
`python3 tools/curated-experiment-checks/E-143/shared_release.py`.
Evidence: deterministic analytical screens, exact kinematic constraints and sourced
procurement examples; self-review. No generated assembly/contact geometry, physical
measurement, qualified spring/friction/process prior or hardware-performance claim.

## Causal combinations and location of arrest

All variants retain separately powered reversible spatial heads, 6,400 parked
supports/returns, capture before unlocking, actual output readback and proved
handback. 5.08-mm tops, 40-mm travel and ~6,400 cells remain fixed. Head equipment
may occupy larger internal pitch; shared release does not supply lift work.

The proposed series path is **motor → transmission elasticity → head rod → retained
capture → column stem → top**. Grounded jaws on the head rod eliminate only the
upstream transmission compliance. E-142's capture clearance/compliance is still
*downstream* and cannot disappear. A useful terminal clamp must grip the column-side
stem beyond that capture, or independently bound its remaining elastic energy,
backlash and stem bending. The frame must also arrest lateral docking motion;
a jaw mounted on a freely moving writer is not grounded.

E-132's lateral eye/elbow still collides with a third row; E-142's isolated eye
does not repair it. Integral extended stems could change access but need generated
clearance through unequal neighbors and docking. Permanent terminal jaws instead
repeat 6,400 assemblies. No dense terminal route is constructed. Even with an instant
fixed head rod, m=1.1 kg, v=.1 m/s and residual K=100/1,000/10,000 N/m permit
**10.488/3.317/1.049 mm** oscillation about equilibrium before backlash: an independent
placement bound, not another E-142 simulation or an allowable-drop criterion.

| Arrangement | Causal mechanism and failure |
|---|---|
| Per-head coil control | Individual coils open frame-backed spring jaws; independent closure possible. 121/229 Adafruit 412 units cost $726/$1,374 before motors: reject this purchase embodiment |
| Crossbar | Two driven ends lift a bar; 20:1 levers open jaws transverse to independent rods. Local springs and a separate bar spring return it. Rigid ties propagate follower jams; unilateral lifting faces separate on return, but common bar/drive jam still holds all open |
| Tendon payout | Separately routed tension-only branches open local levers; a powered yoke tensions them, and a separate spring pays out slack. Branch jams can stay local; yoke/guide jam defeats all. No free gravity return or backdrivable gearbox |
| Pressure manifold | Pressure opens separate spring jaws; normally open exhaust dumps on loss. Springs ground the load. A blocked branch traps one release; blocked sole exhaust traps all. Extra vents/disconnects add hardware; this is not fluid-only holding |

Tendon/unilateral lift are related decoupling variants; pressure is the different
shared arrangement. E-132 permanent drag retains its moving-arrest/heating failure.
No literature novelty or landscape saturation is claimed.

## Summed force/work, leverage and manufacturing sensitivity

**Explicit screening box, not a sourced process prior:** F=10 N service load,
100 mm/s output speed; kinetic/static friction floor .02, or competing .1/.3
assumptions; two flat opposing pads, each 4×10 mm; total spring preload NΣ=800 N
±20%; gap per pad .2–.4 mm. This gives minimum ideal drag .02×640=12.8 N,
only 2.8 N above F. These are scenario loads, not new product requirements.
Direct linear drag is μNΣ: E-142's 16-mm disc / 2-mm output amplification is gone.
Pad pressure spans **8–12 MPa** before contact nonuniformity, not qualified PLA
capacity. Normal loads are transverse and add even though their vector sum cancels.

The 20:1 opening lever trades force for travel: Finput=NΣ/20 and travel=20g.
At +20% preload and .4-mm gap, **48 N/head over 8 mm**, ≥.384 J/head;
eight heads require **384 N and ≥3.072 J**. Lower corner is .128 J/head.
These ideal preload contributions exclude spring-force rise, lever/guide friction,
bar strain and acceleration. A 2-mm short lever arm implies a 40-mm long arm;
finite swept geometry/bearings remain unconstructed. Leverage preserves work.

Re-sizing to the same 12.8-N minimum ideal drag at μ=.1/.3 reduces nominal NΣ to
160/53.33 N; an eight-head adverse preload/gap case still costs **≥.6144/.2048 J**.
These alternative coefficients are uncertainty choices, not material selection.
[Adafruit 412](https://www.adafruit.com/product/412), accessed 2026-10-11, lists .5-N
starting force, 5-N retentive force, 5.5-mm throw and $6 at 100+. Even *granting*
5 N throughout its stroke gives .0275 J. Under that optimistic flat-force envelope,
the three eight-head cases need at least **112/23/8 units' work**, not one actuator.
This envelope is an assumption based on the endpoint rating, not a measured force
curve or universal solenoid bound. The actual .5-N start also contradicts direct
48-N/head opening. Levers cannot repair an energy deficit. A motor release can
supply repeated work, but a self-locking reducer needs a separate loss-safe disconnect.

Guide friction can shunt spring force into the housing before pad loading. A bounded
0/40/80/160-N total shunt at −20% preload leaves **12.8/12.0/11.2/9.6 N** drag at
μ=.02. Last corner fails static hold; even 80 N cuts arrest margin to 1.2 N. This
bound labels uncertainty in guide alignment, roughness and side load, not an invented
probability. For eight freely following ideal levers, local return forces total
256 N at the bar; a **separate assumed 10-N ±20% bar spring** adds ≥8 N. With common
bar/drive resistance 0/50/300 N, net return is **264/214/−36 N**. One head gives
40/−10/−260 N. Unknown motor detent, guide wedging or cable seizure cannot be erased
by setting motor torque to zero. A stuck-open follower supplies no return assistance;
all followers stuck leave only the dedicated spring. No return actuator is selected.

For the pressure arrangement, an assumed .5 MPa opening supply requires ≥1,920 mm²
summed piston area/head at 960 N (equivalent single diameter 49.44 mm); eight heads
with .4-mm piston motion displace ≥6.144 ml. Levers can reduce area only by increasing
travel/volume-related work. Diaphragm strain, seals, exhaust conductance, tubing,
pressure supply and local vent failure are unpriced; no closure time is assigned.

## Crossbar deflection and stuck-member discriminator

An optimistic straight, simply supported beam with both ends **driven together**
carries discrete 48-N lever loads at 40-mm internal head pitch. Rectangular section
width 10 mm, depth 10/20/40 mm; effective E=1–3 GPa is a labelled competing bound,
not an X1C PLA property. Exact point-load Green functions give the midspan maximum.
For .4-mm commanded pad gap, reserve .1 mm running clearance and .2 mm coherent
pad-equivalent gap/warp/alignment error: only .1 mm remains for beam deflection/20.

| Heads / end-drive span | Beam depth | Gap lost at E=1 GPa | Remaining pad margin |
|---|---:|---:|---:|
| 2 / 80 mm | 10 mm | .04224 mm | +.05776 mm |
| 4 / 160 mm | 20 mm | .07872 mm | +.02128 mm |
| 8 / 320 mm | 40 mm | .15456 mm | **−.05456 mm** |

At E=3 GPa the last loss is .05152 mm: positive .04848-mm margin. At .4-mm
coherent error all fail even with infinite beam stiffness; at .1 mm the 320-mm
case fits. Model choice changes the result. Deflections >span/20 are flagged outside
small-deflection validity, not precise failures. Shear, joints, bearings, return-
spring and actuator compliance are omitted favorably. Intermediate *driven* supports
reduce span but need force distribution; stationary supports cannot react along
the allowed opening motion for free. A 320-mm part needs diagonal-build analysis
or a joint on the 256-mm printer, not an assumed free seam.

The executable solves reduced kinematic constraints, **not finite contact geometry**:
with jaw opening qi≥0 and bar opening u≥0, rigid ties impose qi=u; unilateral lifters
impose qi≥u and springs minimize qi. At loss, grant u=0 unless the common mechanism
is jammed. One qi fixed open leaves **0/8** closed with rigid ties, **7/8** with
unilateral followers. A common u fixed open leaves **0/8** in both. A lagging follower
has the same isolation advantage while its opening remains positive; none of these
counts proves that its own loaded rod is arrested. Tendon slack realizes the same
constraint only with separately routed branches and no trapped tension. Pressure
release has an analogous common-exhaust fault, not a proven equivalent transient.
A bar-return sensor can therefore falsely accept a stuck local release. Local rod
stopping and jaw-force/support proof must be separate from common release readback.

## Independent stopping, local isolation, schedule and joint cost

Transverse opening permits different rod speeds/directions, but not independent
clamp application while the bank is open. Normal independent stops need powered
motor control or proved parked-support handback; neither supplies outage arrest.
A bank scheduler waits for the slowest rod before closing, paying dwell/proof;
a local disconnect adds inventory. Keep unused heads undocked and unchanged
columns on parked supports. Sharing this release with parked supports would
release unchanged regions. Frame vibration/displacement remain unbounded.

An optimistic terminal stop with no downstream elasticity/motor energy, delay τ,
then instant 12.8-N drag has distance `vτ+Fτ²/(2m)+m(v+Fτ/m)²/[2(D−F)]`.
For m=1.1 kg, F=10 N, v=.1 m/s and τ=0/2/10 ms: **1.964/2.962/8.614 mm**.
These conditional lower screens are not predicted crossbar closure or accepted drops.
The .05-kg/10-N case needs imposed external force; at 10 ms it crosses 40 mm.
No post-impact trajectory is claimed. Jam/routing failures prevent promotion, so no
finite contact/closure transient is earned by these embodiments.

Retain E-142's optimistic full-map schedule `6+ceil(6400/H)*cycle <30 s`, with six
seconds for preparation/registration/proof/retry/settling. .4-s travel plus .05-s
local operations needs **121 heads / 29.85 s**, or **229 / 29.8 s** with .4-s empty
return. An additional .05-s bank operation raises these to **137/247**. These are
allocations, not demonstrated completion; synchronous grouping, reader failures,
release work and docking can only increase this specific schedule. A detected
unsupported head inhibits withdrawal/indexing; retain capture, restore support,
then bounded retry or isolate repair. No recovery of a jammed release is constructed.

Procurement snapshots, accessed 2026-10-11, exclude tax/shipping and do not select motors:

| Concrete motor per independent head | 121 / 229 motors | Consequence with scenario $250 shared reserve |
|---|---:|---|
| [Adafruit 858](https://www.adafruit.com/product/858), $3.96 at 100+ | $479.16 / $906.84 | Total already $729.16 / $1,156.84 before releases/cells; reject this combination |
| [Adafruit 711](https://www.adafruit.com/product/711), $1.56 at 100+ | $188.76 / $357.24 | 121 leaves **<$61.24 total**; 229 exceeds remaining $250 by $107.24 |

For 121 inexpensive motors the $61.24 must cover *all* remaining releases, drivers,
gearing, sensors, wiring, clamps, guides, bearings, fasteners and cell purchases not
already inside the $250 reserve: **<$0.5061/head with free cells**, or **<$0.00957/cell
with every other remaining part free**. These are alternatives, not additive budgets.
The reserve is an assumption; reducing it reopens cost, not physics. Ideal <$200 and
acceptable $200–400 remain farther away. No market-wide lower price bound is claimed.

711's 10 gf·cm rated torque at loaded 4,500±1,500 rpm gives **.308–.616 W**, versus
**1 W** for 10 N at .1 m/s before losses. Gearing cannot repair rated power;
undocumented peak operation or another motor needs evidence. This is not absolute
maximum power. 858 advises under 6 rpm at 5 V; holding torque is not dynamic torque.
Neither listing qualifies reversal, proof, backdrive or endurance. 6,400 support/
return interfaces and per-head spring/pad wear remain; material, print time and
assembly are unquantified, not zero.

## Decision, verification and next discriminator

Stop detailed crossbar tuning and shared-release purchases for these single-return
embodiments. Preserve unilateral/slack decoupling as a useful local-fault improvement;
it does not cure the common jam, distal capture or independent-stop problem. Reopen
with a concrete means for local closure despite a held-open common command, plus a
dense terminal route and joint channel cost. A changed mechanism, not a stronger
nominal spring or another annulus sweep, must escape the failure.

**Next discriminator:** can local closure become independent of a held-open common
release? Compare a travel-limited pickup that runs off its follower with pressure
release having a permanent local bleed and no accumulator, plus rigid-tie control.
The bleed changes the failed sole-exhaust topology: supply loss can vent even if
the common exhaust is blocked. Screen pump coast/stored pressure, bleed power,
clogging, rearm, sustained arbitrary-motion dwell and local command inventory.
E-109's valve spring/pressure failure remains a control, not this release circuit.
Stop if closure still depends on a trapped common member or only works by adding
an individually powered release. Then revisit dense terminal capture and joint
motor budget before any contact model. No fabrication is justified.

Self-review: leverage/work identity; beam end conditions and PL³/(48EI) center-load
limit; independent curvature integration at 256/512/1024 segments gives .7872-mm
reference with errors 9.38e−6/2.34e−6/5.86e−7 mm; E scaling; exact jam constraints;
strict integer scheduling and SI torque/power conversion. No yield estimates:
coherent spring/gap/E changes and common faults prevent independent-cell averaging.
Layer quantization, hole shrinkage, first layers, warp, roughness, anisotropy,
creep/fatigue, wear and alignment have no transferable prior here. These omissions
limit promotion, not optimistic failures. No purchase, print or CEO boundary.
