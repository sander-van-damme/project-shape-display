---
status: complete
builds-on: [E-131, E-134, E-152, E-114, E-148]
---

# Geometric wells retain parked height; they do not absorb downhill work

**Stop the freely rotating, undamped corrugated cam as a complete mechanism;
retain its parked wells for a reusable damped-writer discriminator. Stop direct
printed-pore capillary holding at the stated 1/10-N scenarios.** Microporous
inserts and low-load capillarity remain conditional alternatives, with rearming
unbuilt. No architecture, material, print or purchase selected.

Input main `7f2f067`. Reproduce with Python standard library:
`python3 tools/curated-experiment-checks/E-153/barriers.py`.
Evidence: primary-source operating analogies, exact conservative energy/path
calculations, favorable pressure/flow bounds and deterministic scenarios;
self-review, no independent review. No constructed cam contact solids, fluid
interface simulation, X1C calibration, measured performance, BOM or reliability
claim. The failures occur before a complete geometry/flow construction earns value.

## Discovery: two different ways to ground a barrier

Two independent axes: load-induced cam detents and interfacial pressure pinning.
Patent lookup confirms cam detents are established mechanisms: novelty here is
recombining a multi-turn height path with loaded wells to escape E-131's low-lead
friction requirement, **not inventing the detent**. Capillary pressure is familiar
from E-114 but changes from retaining unloaded molten inventory to carrying
hydraulic service pressure without freezing. Neither is a new physical principle;
both add decision-relevant comparisons. No search-saturation claim.

Primary sources accessed 2026-10-11:
[US8104443B2, description of detent 270 and loaded helical tracks](https://patents.google.com/patent/US8104443B2/en)
describes axial loading producing cam torque and a recess receiving an opposing
peak. It does not construct the multi-turn law below or establish miniature life.
[The Laplace trap study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3365347/)
uses interface curvature to retain droplets and pressure or interfacial-tension
changes to release them; its fabricated devices use soft lithography/PDMS.
That is an operating analogy, not a PLA pore or hydraulic-column qualification.

| Combination | Selection / signed motion | Memory and service load path | Verification / recovery obligation |
|---|---|---|---|
| Corrugated helix | Indexed rotary heads dock to local rotors; bilateral motor torque follows an antirotating follower over multiple turns. Downward payload can return energy. | Top → follower → corrugated groove → rotor thrust bearing → frame. Payload creates geometric minima; no separate latch opens. | Read actual top and rotor phase, remove drive torque and prove stationary seating before undocking. Cut during travel needs energy absorption while dock remains captured. Sensor acceptance alone cannot establish a well. |
| Capillary hydraulic memory | Selected reversible pressure/volume head connects to local piston circuit; pinning interfaces isolate unchanged sites from reservoir pressure. | Top → piston → liquid pressure → pinned interfaces/pore walls → frame. Not a dry capillary bridge directly under the top. | Read top, pressure and retained volume; re-form interfaces after both motion directions and verify support before disconnect. A burst flooded pore is not automatically a restored valve. Head retains failed site; independent service support remains unbuilt. |
| Controls | E-131 screw with grounded thrust and sliding thread; E-148 field-opened jaw with returned clamp. | Continuous frictional thread / local returned jaw. | Their friction, coast, gap, docking and cost limitations remain. Neither receives a new pass. |

Unchanged cam rotors need not move; unchanged hydraulic sites must remain isolated.
Shared frame motion and common hydraulic pressure are disturbance paths, not free
regional isolation. Anti-rotation guidance, down-bias at low load, return routing,
readback, captured docks and repair access are real parts in both architectures.

## Cam: exact wells and an exact interrupted-motion counterexample

Grant an ideal captive follower obeying the height path, in mm and radians,

`h(q)=k q + a sin(n q)`, `k=L/(2π)`, `V(q)=F h(q)`.

This is a favorable one-coordinate constraint, **not generated roller/groove
contact geometry**. Rotor bearings fix its axis; an independent vertical guide
prevents follower rotation. A geometric realization might collide or undercut;
such failure cannot rescue the unrestrained energy path of this proposed law.
F is total downward force, including weight/bias; 0/.02/1/10 N are scenarios,
not new product requirements. No friction, structural strain energy or damping
is silently added. Generalized inertia stays positive after the drive torque
is removed; q is never frozen.

Nominal L=4 mm/rev, a=.30 mm, n=4. Wells exist iff `na>k`:
`q_peak=acos(−k/(na))/n`, `q_min=(2π−acos(−k/(na)))/n`.
At a minimum, h'=0 and h''>0, so every **positive** F supplies a stable parked
well. Their height spacing is L/n=1 mm; 41 minima span 40 mm. Arbitrary choices
among these discrete heights are kinematically independent, not a continuous
height or approved height-accuracy claim. The minimum threshold amplitude is
.159155 mm. A=.10 mm has no wells.

Nominal downhill escape rise is **.186607 mm**; uphill escape rise **1.186607 mm**.
The corresponding downhill barriers are **.003732/.186607/1.86607 N mm** at
F=.02/1/10 N. At zero total load V is flat: geometry alone neither restores nor
arrests rotation. A spring could provide bias but adds stored energy and hardware.
Peak ideal motor torque at 10 N is **18.3662 N mm**, before inertia/contact losses.
The output reverses vertically within each angular step; these .186607-mm ripples
are part of the motion, not a smooth lift or quantified miniature-disturbance pass.

**Free-input witness:** release at `q=q_peak+39(2π/n)−.01 rad`, heading downhill.
All lower maxima differ by exactly `F L/n`. Even with zero initial velocity at
10 N, total energy exceeds the first lower maximum by **9.997949 N mm** and all
38 subsequent maxima by still more. Acceleration initially points downhill.
There is no turning point before the bottom of the studied range. A moving
zero-load rotor similarly retains its kinetic energy. This proves an available
uncaught path, not a predicted impact speed or manufactured drop distance.

The executable checks all 39 lower maxima, 12 coherent L=3.9/4.1 mm,
a=.25/.35 mm, F=.02/1/10-N cases, and zero-load/moving and loaded/rest releases.
All shape corners retain wells (barrier rise **.098331–.282499 mm**) yet admit
the downhill escape. Forty steps span **39–41 mm**: common lead error does not
average away; 44 steps/11 turns give at least 42.9 mm under this box, before end
hardware. These bounds are not manufacturing probabilities. Local waviness can
create/remove extra wells: an amplitude tolerance without a spatial-wavelength
bound does not qualify derivatives or barriers.

For a descending trajectory, kinetic energy at corresponding phases increases by
`F L/n−D` per period, where D is work removed. Removing at least **10 N mm per step** at 10 N prevents
period-to-period energy growth; it does **not** guarantee capture of the initial
energy or a particular well. Mean removal torque is at least **6.3662 N mm**.
Larger identical conservative wells cannot remove net gravity work. This is why
static detents differ from passive arrest; it is not a ban on cams with damping.

**Changed combination worth probing:** keep a reusable writer mechanically docked
through motion and torque loss; give that head an explicit passive energy sink,
then undock only in a proven stationary well. This relocates dissipation to heads
while each parked column keeps a local geometric barrier. A motor plus unspecified
controller is not that sink. Circuit-open faults, return-biased shorting hardware,
mechanical dock retention, inertia, low-load capture and erroneous undocking must
be defined. E-134's free front is not reopened by asserting a fixed motor angle.

## Capillary: pressure multiplication still demands microscopic interfaces

Grant a 4×4-mm hydraulic piston, A=16 mm², two favorable opposed interfaces in
circular pores of minimum radius r, and tension γ. Each interface contributes
at most 2γ/r; use the generous sum `|Δp|≤4γ/r`, so `F≤4γA/r`.
Contact angles may make the actual difference far smaller or of the wrong sign.
Parallel pores increase flow capacity, **not pressure capacity**. Serial independent
interfaces can increase pressure, but add phase inventory and rearming operations;
that is a changed construction, not a free multiplier.

For γ=.03–.075 N/m, r=.05–.15 mm, and coherent piston side 3.8–4.2 mm,
the ideal holding ceiling ranges **.011552–.105840 N**. Even a generous
γ=.5 N/m with r=.05 mm and A=16 mm² caps force at **.64 N**. These are fluid
and geometry scenarios, not measured properties or qualified printable pores.
Stop this directly printed-pore embodiment at 1/10 N. Low-load scenarios can
change that disposition; pore printability and retention/rearming remain open.

At γ=.075 N/m and A=16 mm², maximum radii are **4.8 µm at 1 N** and
**.48 µm at 10 N** (240 µm at .02 N). Ordinary X1C nozzle size does not certify
any pore accuracy; these tiny radii imply an additional membrane/insert process.
Internal mechanisms may be larger than surface pitch: a .1-mm pore would need
at least **333.33/3,333.33 mm² piston area** at 1/10 N. This is an explicit area
trade, not a universal capillary rejection. Routing 6,400 such pistons is unbuilt.

To expose the retention/flow trade, separately grant straight fully liquid pores,
50% porosity across A, μ=.001 Pa s and **100 kPa additional viscous pressure**:
`Q=φ A r² Δp/(8 μ ell)`. This optimistic Poiseuille relaxation has removed the
interfaces; it is **not simultaneous holding, release or rearming evidence**.
At the 10-N radius it needs about **11.05 million pores/site**. A 10/100-µm-thick
insert gives optimistic .64-mL transfer times **.2778/2.7778 s**. At the 1-N radius,
the 100-µm insert gives .02778 s; the 10-µm case has length/diameter≈1 and its
pipe-law number is out of domain. Entrance losses, tortuosity, blocked pores,
wetting hysteresis, permeability variation and seal friction only add obligations.
No flow or complete-time pass is inferred. Full 40-mm board displacement is
**4.096 litres**, before reservoir/line dead volume.

Once an interface bursts and a pore floods, a stationary pore may conduct rather
than reseal. Neither a hydraulic head nor the source's trapped droplet provides
an automatic bidirectional gas/interface restoration cycle for this piston volume.
Stop insert optimization until a volume-conserving rearming topology exists.
E-114's cold carryout remains its own failure; no thermal mechanism is reopened.

## Complete-machine consequences and next action

The favorable cam needs ten turns versus E-131's **84.88 turns** for a 3-mm,
μ=.05 zero-margin square thread. This speed opportunity survives the static
comparison, but a thicker shaft, follower, bearing, guide, housing and dock have
not been packed at 5.08-mm pitch. No CAD envelope pass is claimed. Eleven turns
for the coherent travel bound worsens the following nominal schedule.

Assume .10 s/site for dock/read/seat-proof/withdraw, and 6 s/map for preparation,
indexing, final verification, settling and one bounded retry. Then
`T=6+ceil(6400/H)*(600/rpm+.10)`, with independent rotary heads and no acceleration
or additional reset travel. Required H for strict <30 s at 600/1,200/2,400 rpm:
**305/165/95**. At a $250 shared reserve and $500 ceiling, free local parts leave
**<$0.820/$1.515/$2.632 per head**. That reserve must include power, controllers,
wiring, guides, transport, sensors, bearings and fasteners; this is an allocation,
not a quote. A sourced BOM is not earned by a head count.

Each cam site repeats a rotor, follower, thrust reaction, anti-rotation guide,
wearing groove and capture/read interfaces: about **256,000 geometric periods**
across nominal 40-step cams, plus end margins. Capillary sites repeat pistons/seals,
pore inserts, phase inventories, isolation and rearming interfaces. All bought
site content alone gets **<$.03906/site** with that reserve and free heads.
At $400 the available joint head/site budget is $150; the $200 ideal is already
exceeded by the illustrative reserve. No purchased-cost pass. One 10–30-s handling
operation per site is **17.8–53.3 hours**, excluding printing, inspection/rework,
assembly and repair. Printed volume/time need actual geometry and are unknown.

Uniform 1/10-N, 40-mm lift requires at least **256/2,560 J**, with **6.4/64-kN**
frame load; these uniform loads are scenarios. Lowering needs the corresponding
energy sink. False well/pressure acceptance can release a wrong site; common
phase or pressure bias defeats repeated readings. No detection probability is
assigned. Failed proof retains the head for one supported retry; sustained jams
or interface loss require supported module service outside successful-map timing.
Unchanged-site support does not establish low vibration or shared-frame stiffness.

Process/model limits: common lead/amplitude bias, hole shrinkage, first layers,
layer quantization, warp and assembly error alter the cam path; roughness/friction,
anisotropy, contact stress, interlayer weakness, creep, fatigue and wear change
barriers and losses. Common wetting chemistry, contamination and largest connected
pore dominate fluid retention. These are unresolved correlations/model uncertainty,
not independent cell yields. No fatigue, yield, force-tail or board reliability
estimate follows from these bounds.

Self-review: stationary points/curvature signs, zero-load and no-well limits,
energy at every lower crest, exact signed 40-mm work, and independent
circumference-force/area capillary balance. Nonperiodic torque-work quadrature
errors at 64/256/1,024 intervals are **5.20e−4/3.25e−5/2.03e−6 N mm** at 1 N;
finite-difference height derivatives converge separately. These checks validate
the reduced mathematics, not contact feasibility or dynamics.

**Next discriminator:** finite corrugated cam + captured, passively damped reusable
writer. First solve free torque-loss transients against energy bounds across load,
phase, inertia and damping uncertainty; determine whether bounded capture is even
available at useful writer speeds. If it survives, construct actual finite
follower/groove contacts, thrust path and dock release around an unchanged neighbor.
Stop on runaway, reliance on powered braking, loss of sole support or inaccessible
geometry. Do not optimize membranes without reversible interface restoration, tune
smooth plastic forming, or print. This is a changed retention/dissipation split,
not a selected machine; no CEO-owned resource boundary arose.
