---
status: complete
builds-on: [E-154, E-153, E-131, E-132, E-139, E-148, E-082, M-008]
---

# Compression support helps; shared dissipation trades independent motion for selective coupling

**No tested combination removes both failures at machine level.** A supported roller axle escapes
E-154's thin-neck strength contradiction under explicit bounds. An open differential exposes undamped relative motion; a rigid bus
removes that mode but the tested stopped-selection schedule needs thousands of couplings. Retain wider compression rollers and asynchronous
self-locking support as different conditional leads, not a selected machine. No fabrication.

Input main `b881ec0`. Reproduce with Python 3 and NumPy:

```
python3 tools/curated-experiment-checks/E-155/screen.py
```

Evidence: analytical bounds, finite **planar** contacts, prescribed motion and cost/error
scenarios; frictionless rigid contacts/guides, self-review only. No CAD, process prior, full transient model, BOM or hardware qualification.
JSON is reproducible output, not retained.

## Changed combinations and complete causal obligations

| Embodiment | Causal path and disposition |
|---|---|
| Flat shoe / rigid bus | Selected dogs connect corrugated rotors to common motor/generator. Top → guided shoe → shelf → rotor thrust/frame. Engaged dogs remain through power loss. Broad small-radius shoe erases parked wells. |
| Supported roller / differential | Top → guided yoke → supported axle/roller → track → rotor thrust/frame. Carrier motor/generator drives selected differential outputs. Asymmetric load excites motion invisible to carrier braking; stop this sink. |
| Supported roller / rigid bus | Same compression path, retained dog and common motor/generator. Separate upward/downward passes stop wherever any output finishes. Contact lead survives; synchronization and selection inventory prevent a machine pass. |
| Smooth high-lead screw / parking bolt | Nut/flanks → thrust/frame carry load; selected rigid bus writes, grounded index bolt parks rotor. Generator alone allows continued descent. Drive+ground handoff requires stopped bus; drive-first handoff releases torque restraint. Stop asynchronous handoff. |
| Independent roller-cam writers | Retained motor/sink per head supplies independent signed motion; same supported axle. Slower compression-preserving motion worsens priced head replication. |
| E-131 screw / E-148 downstream jaw | Screw retains loaded flanks but depends on kinetic friction/inertia. Jaw survives upstream separation but adds return/closure/excursion. Neither gets a new pass. |

The positive selector is explicitly a sleeve keyed to the bus output, entering rotor face dogs.
A nonrotating fork captures the sleeve between thrust faces; a grounded screw/nut translates the
fork and retains its axial position after power loss. Straight torque faces supply no intentional
axial eject force. A keeper retains the writer behind a rotor collar. Every fork still needs a
command actuator, travel, bearings, position proof and anti-withdrawal margin; these are **unbuilt**,
not granted cheap clutches. A motor per selector restores replication.
Mechanical mask/data-rail writing could replace those motors only with a constructed retained
command system, force budget and time accounting; M-008 and E-082 already identify that burden.
No free spring, minimum load, return force or decoder is supplied.

Sequence: read actual top/phase → stop/align bus → engage/prove dogs → write → stop/prove **each**
parked output → withdraw appropriate sleeves → index. Unchanged sites keep local wells/locks.
Failed proof retains the bank for supported correction, not blind homing. Broken axle/dog or
jammed fork needs a service prop/removable module; access remains unbuilt and is excluded from
successful-map timing.

Search axes: contact-footprint inversion; transmission-mode decomposition; smooth writing separated
from parking. These recombine existing principles (M-008/E-139/E-131); no saturation claim. Primary sources checked 2026-10-11:
[NPTEL cams](https://archive.nptel.ac.in/content/storage2/courses/112103174/module4/lec3/1.html)
for direct contact, follower and frame;
[Maxon generators](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators)
for generator reaction/dissipation. Neither qualifies these constructions. Cost controls reuse
E-154's same-day Pololu/Omron comparison rates, not a new quote or universal floor.

## Finite compression-contact discriminator

Use the E-153 law in mm: `h(q)=4q/(2π)+.3sin(4q)`, period `P=π/2`, one-mm height increment.
In a developed **planar strip**, x=R q. A horizontal shoe of finite width b rests at
`H(q)=max h(t), t∈[q−b/(2R), q+b/(2R)]`. Evaluate both endpoints and every enclosed local maximum
exactly. This gives nonpenetrating section contact.

At R=1.5 mm, b=1 mm leaves **.02133-mm downhill barrier**, versus .18661 mm for a point.
At b≥**1.18813 mm** the envelope is nondecreasing: no downhill retaining well. The threshold
solves `h(q_peak+b/R)=h(q_peak)` on its rising branch. A full-period window is independently
monotonic because each departing point has a one-period-higher replacement. R=6 mm and
b=1/2/3/4 mm retain barriers .17266/.13340/.07742/.02133 mm. Shoe contact is lines/edges,
not its whole area; contact-switch dynamics remain open.

For a roller, generate lower/upper polylines by offsetting `(R q,h(q))` along its normal by
`r+c`, with r=1.5 mm and c=.1 mm; evaluate every segment and vertex against the finite disk.
Finite extrusion gives a planar track and roller section; yoke/track/frame are not assembly CAD.
At R=1.5 mm these offsets fold: a large roller cannot reproduce that corrugation. At R=6 mm,
minimum sampled pitch curvature radius is **7.6135 mm**, comfortably larger than 1.6 mm, and
nominal center clearance is **.20000 mm**. Both directions use the same supporting flank; eleven turns span at least 42.9 mm for lead
3.9–4.1. Ends, wrapping, thrust faces and radial routing remain unconstructed.

The supported axle has diameter 2 mm, support span 3.2 mm and two 1-mm cheeks. At 10 N:
center-load bending `8FL/(πd³)` = **10.19 MPa**, double shear **1.59 MPa**, cheek bearing
**2.50 MPa**. At d=1.8/2.2 mm, bending is **13.97/7.65 MPa**. This avoids the former .4-mm
cantilever's 795.8 MPa within an **assumed** 20–60-MPa allowance, before notches, contact stress,
creep, fatigue and anisotropy. At 20 N the 2-mm axle needs 20.37 MPa; it loses the weak bound.
At 320 N it fails. Prescribed motion below needs ≤14.03-N normal force at 10-N load,
or 14.29-MPa nominal axle bending; contact reversal remains prohibited.

Common adverse error e moves both walls inward by e and enlarges the roller by e. At
e=0/.025/.05/.10 mm, minimum center clearance is approximately **.200/.100/0/−.200 mm**;
the tiny negative at .05 is polyline discretization, not a measured interference prediction.
These are coherent error scenarios, not X1C accuracy or probabilities. Internal 8/14/18-mm envelopes
need 4/9/16 tiers in a simple square interleave at 5.08-mm tops. Routing remains unbuilt. Sixteen
52-mm cartridges consume 832-mm depth before routing/frames; wider internals are allowed.

## Contact-aware motion, shared modes and outage

The analytic loaded roller-center curve is the pitch curve minus `c*normal`, with its x-coordinate
inverted to the imposed input. Its height differs from the pitch law by up to **.10458 mm**.
Use this actual smooth offset, not the pitch curve, for motion. Prescribe each signed well step as
`q=q_valley±P(10s³−15s⁴+6s⁵)`, s=t/T. Output acceleration is
`zddot=z''*qdot²+z'*qddot`; dropping either term gives a false contact margin.

Across both directions, lead 3.9/4/4.1 and amplitude .25/.30/.35 mm (18 scenarios), requiring
vertical reaction `F+M*zddot≥.5F` with **M=F/g** gives worst step **.100417 s**. This is a chosen
half-weight contact margin, not a requirement or a global time optimum. A zero-margin limit
reduces it by √2. Different inertance/load, guide drag or ripple wavelengths require recalculation. At zero F geometry provides no parked energy well; no bias spring
is assumed. Even this positive-contact prescribed trajectory does **not** validate the uncontrolled
outage dynamics of the larger real roller, bus, generator or its inductance/inertia.

A rigid engaged bus has `q_i=q_bus+offset_i`; thus one sink can damp its sole rigid coordinate.
For identical phases and positive loads, total potential is the sum of local potentials and
`J_eff=J_bus+Σ(J_i+M_i*z_i'^2)`. Damping/heat and reflected inertia must scale together. E-154
capture is not inherited after changing either. Illustratively scaling its strong c=.001 N m s
by 3,200 engaged cams gives c=3.2, **3.158 kW at 300 rpm** and up to **58.77 N m static cam torque**
at 10 N/site, before generator drag/acceleration. This is a warning against reusing its damping
coefficient, not a lower bound on every viable sink. Uniform 40-mm downward maps still release
5.12/256/2,560 J at .02/1/10 N; generator heat, cooling and bought power hardware remain in cost.

For an ideal open differential, generator speed is `(qdot1+qdot2)/2`. The nonzero mode
`(qdot1,qdot2)=(-1,+1)` produces **zero generator dissipation**, even with its carrier clamped.
At equal q=0, loads 10/.02 N release **.018329 W** into that mode. This local accelerating
counterexample defeats an all-state damping claim; it is not a simulated full-stroke escape.
Adding a brake to each branch or locking the differential changes inventory/topology. A common
slipping belt similarly cannot be presumed to constrain all outputs, although its **local slip
friction** may dissipate energy and is a distinct mechanism worth evaluating.

Bus stationarity is not local parking proof: two equal 10-N ideal-law cams with opposite ±.02-rad phase
bias have **opposing .811876-N mm torques** at aggregate equilibrium. Disconnecting changes their
force balance. Readback must distinguish each local seating state and loaded support from a
stationary bus. Shared shaft break, generator circuit open or mistaken mask withdrawal can affect
many outputs together; no independent-cell failure assumption is made.

Smooth screw parking has a separate exact constraint failure: with output q_i grounded and dog
engaged, `q_i=0` and `q_i−q_bus=0` force a stopped bus. Breaking drive first leaves an unrestrained
coordinate before the ground bolt enters. Overhauling (frictionless here) screw plus viscous generator
has nonzero terminal descent, not static capture. An automatically returning bolt, kinetic
self-locking thread or local brake must be constructed rather than inferred from the word parking.

## Arbitrary maps, joint cost and decision

State replay exhausts **625 old/new two-cell maps** with heights 0…4: sequential
positive and negative step masks reach targets; unchanged outputs never move. It validates the
schedule's state logic, **not** sleeve actuation, sensing or physical isolation. At full scale,
a fixed group containing all required positive/negative step distances demands up to 44 stopped
steps in each direction. Group reordering, opposite-handed drives or a different motion law
could change this schedule and would require a new physical controller.

Assume .10 s/group for docking/local proof and 6 s/map for preparation, transport/registration,
final verification, settling and one bounded retry. Include each stopped selection.
`Tmap=6+ceil(6400/H)*[88*(Tstep+t_select)+.10]`, strictly below 30 s:

| Explicit scenario | Simultaneous channels H | Calculated complete allocation |
|---|---:|---:|
| Half-weight contact margin; zero selector time | 3,200 | 23.87 s |
| Same; 2/10/20 ms selector work per step | 3,200 | 24.23/25.63/27.39 s |
| Zero contact margin; zero selector time | 2,134 | 25.05 s |
| All changes one direction, favorable only | 1,280 | 28.59 s |
| Independent ideal cams, 300/400 rpm | 640/493 | Motor+relay alone $3,266/$2,516 |

These are controller-specific allocations, not measured times or universal bounds. Independent heads grant instantaneous acceleration; selectors/readers/transport remain unbuilt. Forty nominal steps instead
of the 44-step travel allowance still needs 3,200 channels at the chosen contact margin. An
arbitrary local subset uses its own masks without deliberately releasing neighbors; common-frame
deflection and vibration remain unbounded. No regional-disturbance or miniature-stability pass.

Joint purchased constraint is `H*c_channel+6400*c_site+c_shared<500`. At H=3,200 and $250 shared,
free resident purchased parts leave **<$.078125 per complete channel**. With $.02/site this falls
to **<$.038125**. A hypothetical $.10/channel gives $570 before site parts, or $698 with them;
$.05/channel and free sites gives $410. These hypothetical costs change disposition and are not
quotes. At $150 shared and free sites, $.10/channel gives $470, still unproved. If each fork uses
even E-154's $2.30 comparison motor, selectors alone cost **$7,360**. Stop that implementation; printed command storage requires a demonstrated command path.

Count 6,400 roller/axle/yoke/guide/track/thrust sets plus thousands of dogs, forks and command
readers. One 10-s operation/site is 17.8 assembly hours. Print volume/time remain unknown. Hole bias,
layer quantization, first-layer growth, warp, alignment, roughness/friction, interlayer weakness,
creep, fatigue and wear remain uncalibrated; common phase and clearance errors defeat banks.
False support acceptance p gives 6400p expected bad releases without requiring independence;
no p is measured, and common sensor bias can defeat every check.

**Disposition:** stop broad small-radius shoes, differential-only damping, asynchronous rigid
parking handoff and motor-per-selector replication. Preserve the enlarged supported roller as a
sectional lead; a cheap rigid mask bus is conditional on physical selection, packaging, phase and
passive capture evidence. Preserve screw/jaw controls and E-154's failures; no nominal profile/generator optimization.

**Next axis:** asynchronous shared frictional writing into continuously self-locking resident
screws. A slipping belt may shed source inertia and dissipate relative motion without unlocking
support, changing E-132's independent writer. Test signed slip work, kinetic thread friction,
input loss, zero payload, reversal and common belt failure against rigid cam/jaw controls. Stop
if source inertia, selective-contact hardware, sliding heat or turn count defeats cost/time.
This is a changed coupling hypothesis, not static screw acceptance. No printing or CEO boundary.

Self-review: exact envelope threshold and full-period proof; finite segment/vertex disk clearance;
64/256/1,024 contact subdivisions approach the analytic offset (max error .206/.0257/.00168 µm);
512/2,048/8,192 motion samples give .10041705/.10041705/.10041713 s; independent finite-difference
checks of both loaded-path derivatives; periodic one-mm travel identity; exact bus null mode and
handoff constraint ranks; exhaustive signed state replay and strict integer scheduling. No
independent external validation, continuous error enclosure or printed contact dynamics claimed.
