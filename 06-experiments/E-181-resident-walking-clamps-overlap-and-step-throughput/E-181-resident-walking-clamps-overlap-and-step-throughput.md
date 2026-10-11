---
status: complete
builds-on: [E-150, E-139, E-164, E-156, E-148, E-131]
---

# Resident walking grips exchange pickup travel for repeated support transfers

**Pause the indexed short-stroke walker; retain timed grip overlap as a conditional
alternative to resonant contact.** A finite dwell separates clamp exchange from axial
motion and avoids E-150's simultaneous-contact gap in the stated model. It does not
ground a free carrier, remove a second grip, or establish a complete-machine advantage.
At 1/2-mm steps, optimistic timing needs 915/582 heads; enforcing the weak-grip
acceleration bound raises these to 1,600/915. No selected
machine, physical qualification, purchase or printing follows.

Input main `0ce734e`; LAB-297. Reproduce with standard-library Python:
`python3 tools/curated-experiment-checks/E-181/walk.py`.
Evidence: sourced operating analogies, prescribed compliant-contact schedules, finite
pad/runner sections, exact hybrid fault witness and analytical timing. Self-review;
no actuator dynamics, manufactured spring/guide geometry, calibrated process prior,
independent review or measurement. JSON is reproducible and discarded.

## Search and complete causal combinations

Two searches: nonresonant precision walking drives and integrated self-locking linear
actuators. [PI's walking-drive description](https://www.pi-usa.us/en/expertise/technology/piezoelectric-drives/piezowalk-piezo-motors)
uses preloaded actuators that clamp and lift a runner; parked preload provides holding.
[PiezoMotor's sequence](https://piezomotor.com/technology/piezo-legs-technology/) alternates
contacting feet and notes load-dependent step length. These establish an operating
principle, not affordable piezo parts or printed performance. [US12607256B2](https://patents.google.com/patent/US12607256B2/en)
adds a grounded interference friction ring to a drive shaft: it is a permanent-drag
control, not free retention. Sources accessed 2026-10-11; no prices/material parameters
transferred. No legal conclusion or landscape-exhaustion claim.

| Causal combination | Selection, energy, memory, load and recovery |
|---|---|
| Resident A/B walker, probed | Indexed H-channel writer operates two release keys and a signed short-stroke carrier key at a fixed datum. A is a grounded spring-closed opposed-pad grip; B is another grip on an axial slide with finite stops. Repeated B feed advances a plain guided column; A holds during B reset and after writer removal. Read actual height and grip/support response; keep writer until A holds, retry once, otherwise stop module. |
| Shared bank carrier + retained local enables | Broadcast short axial cycles to B carriers; locally enable each grip sequence for the required number and sign of steps. A supports inactive columns. Removes long writer travel but needs 6,400 isolated carrier couplings or local B releases, retained step commands, actual readback, bank restraint and fault recovery. A live common motion cannot simply be connected to every closed B. Not constructed. |
| Resident electrically driven walking feet | Per-cell normal/tangential actuators ground directly, alternately move/grip, and retain through preload. Removes travelling capture; repeats active material, drivers/addressing, preload and moving contacts at 6,400 sites. Read actual height; isolate failed channel while its grounded grip holds. No cost or fabrication route established. |
| Integrated shaft drag | Reversible indexed torque writer drives resident screw/rack conversion against permanent grounded drag. Read height, prove holding before disengaging. Repeats rotor, drag fit and transmission; E-156 coast/heat and E-131 sliding controls already cover its liabilities. No new probe justified. |
| Direct / field / aperture controls | Direct full-stroke heads retain capture plus resident supports. E-148 field sharing removes a release winding, not jaw/return/capture. E-164 canted plates repeat pivots/edge contacts and still need a supported writer. None receives a new pass. |

The useful changed axis is **nonresonant normal/tangential sequencing with explicit
stationary overlap**, not a new friction law. E-150 coupled oscillating feet to a
resonant head; E-139 had a free captive-cam input; E-164 was stationary retention.
Here B remains resident at a fixed axial datum, avoiding acquisition at each old
height, but is still a second moving support. No removed-function claim for that
support. Neither search produced a new basic retention principle; broader function
integration remains unsaturated. Existing documentation volume gives no preference.

## Contact sequence and finite section

Use mm, N, s. A runner has x/y halfwidth .75 and z=[h−50,h+3], h=0…40;
a 4.8-square top occupies z=[h+3,h+5]. Each grip has opposed pad bodies of radial
thickness 1, height 1.2, y=[−.6,.6]. A center z=0, B center z=−5+xB with
xB in [−s/2,+s/2]. Symmetric radial spring compression is aggregated into one
normal-force coordinate per grip, so N below is **sum of both pad normals**.

For the 1-N downward-load scenario, effective stiffness k=40 N/mm and nominal
compression .4 mm give N=16 N/grip. Assigned compression is d=.4*b+e, where
b=.8/1.2 is common preload bias and e is a separate contact-offset error. Opening
command q ranges 0… .7 mm. `N=k*max(d−q,0)`, physical pad gap `max(q−d,0)`;
compliance absorbs compression, not rigid-body penetration. Holding capacity is
C=mu*N. This constitutive section is prescribed, not a generated spring/release cam.
At 10 N the compared stiffness/preload scale 10×; stronger hardware is not free.
Loads .02/1/10 N are scenarios, not new requirements. Friction .02/.1 are bounds,
not measured PLA properties; upward loads and dynamic capacities remain unqualified.

Cycle starts with A closed, B open at −s/2. Close B → dwell → open A → guard →
feed B to +s/2 → guard → close A → dwell → open B → guard → reset B to −s/2 →
guard. Reversing the axial path lowers. Both grips are stationary during overlap;
feed reverses sign without changing which grip carries the column. Partial final
steps give logical arbitrary heights; all 25 five-level old/new pairs at five
step sizes are checked, not physical state reach or readback. Startup/parking at
carrier center and writer engagement are included only in the timing allowance.

Piecewise-linear q and xB are explicit. For phase errors ±epsilon on each q,
collect every ramp endpoint and force-zero crossing: capacity is affine between
those events, so event minima cover continuous time for each scenario. A dwell
2*epsilon ensures the new grip is fully closed before the old begins opening;
guards epsilon keep axial travel outside every normal transition. This construction
also covers interior phase offsets within the bound, provided d stays between
0 and .7. No zero-error synchronization is granted.

| Error e / phase bound / guard | Minimum C_A+C_B, N | Axial travel with wrong grip touching, mm/cycle |
|---|---:|---:|
| 0 / 0 / 0; preload still ±20% | 1.28 | 0 |
| ±.05 / ±1 ms / 0 | 1.08 | .01357 |
| ±.05 / ±1 ms / 1 ms | 1.08 | 0 |
| ±.10 / ±1 ms / 1 ms | .88 | 0 |
| ±.05 / ±1 ms / 1 ms, mu=.02 | .216 | 0 |

32 labelled corners/row include separate A/B offsets, common preload and timing
signs (degenerate zero cases repeat); these are not yield statistics. Ramps are
3 ms and each prescribed axial stroke 40 ms for this contact check, not measured
motion or the acceleration-limited timing model below. A 1-ms-ramp no-guard witness
has .03786-mm wrong-grip travel. With tangential stiffness 10 N/mm per grip,
forced relative mismatch delta creates opposing force `5*delta N` while both stick;
.1/.5 mm give .5/2.5 N before frictional slip. Overlap during motion is not free.
The sum above is **contact capacity, not ground capacity** when B's carrier is free.

Generated pad prisms remain outside the runner; analytic envelope gaps separate
A/B bodies by `5−s/2−1.2` mm. At s=1/2/4 mm this is 3.3/2.8/1.8 mm; adjacent
5.08-mm-pitch pad envelopes have ≥.72-mm horizontal gap for d≥.27. Runner end
coverage is ≥2.4 mm for these strokes throughout h=0…40. Caps have .28-mm nominal
gap. At s=8, full-close handover produces **.24 mm³ pad intersection per side**;
this is an actual witness, not only overlapping bounding boxes. Increasing A/B
spacing/tail length or staggering pads would change this geometry. Guides, springs,
keys, stops, frame and service access remain unbuilt, so this is no complete pitch
or stiffness pass. Common warp and body-size errors need added envelopes.

## Input loss: a bounded carrier is not a bounded column

When A alone holds, its pads ground the column. When B alone holds, the axial
writer/slide restraint must ground the carrier. A normal return spring does not
supply that axial restraint. On input loss, A may close, but release decay, spring
acceleration, sticking and contact force growth require a dynamic mechanism.
The prescribed q schedule proves nothing about an unpowered transition.

Exact **single-fault witness**, not a normal-outage prediction: A release remains
stuck open; B has intact pads with constant C=1.08 N and a frictionless unpowered
1-g vertical slide, no axial spring. A 1-N column has m=1/g kg. Cut at carrier
center with downward .05 m/s, s=1 mm. Both masses fall at g until the carrier hits
its lower stop after .5 mm / **6.213 ms**, at .110950 m/s. Before impact no pad
shear is needed. Grant a perfectly inelastic carrier stop; the finite-friction
column retains velocity, then slides through B by
`m*v²/[2*(C−W)] = 7.84276 mm`, before stopping. Energy equals `(C−W)*slide`.
Thus even intact short carrier stops do not geometrically confine the column to
one step. A timely A closure changes this witness and must be demonstrated; there
is no invented allowable drop, universal rejection, or assumed stop strength.
C≤W additionally loses static holding in this model.

Separate conservative energy scenarios (not solved transients) combine output+
carrier kinetic energy, gravity over one carrier stroke and a grounded axial
spring's maximum stored energy: `.5*M*v²+(W+.001*g)*s+.5*K*(s/2)²` in SI.
They make return/stop energy explicit; they do not prove arrest because pad slip,
spring force, rebound, source inertia and remaining powered input are not bounded
by a carrier travel limit. Avoid using the carrier bound as an output certificate.

## Board accounting and decision

Optimistic allocations: v=200 mm/s, a=5,000 mm/s²; each stroke uses triangular or
trapezoidal rest-to-rest time m(s). Normal ramps tc=3 ms, phase bound epsilon=1 ms,
dwells 2epsilon, guards epsilon. `tstep=4tc+8epsilon+2m(s)`,
`tservice=.1+ceil(40/s)*tstep`, `T=6+ceil(6400/H)*tservice`.
The .1 s covers local acquire/park/read/proof/release; 6 s covers map preparation,
registration/transport, final verification, one bounded retry and settling. These
are unearned allocations; no sensing/proof is performed between cycles in this
optimistic calculation. Stroke speed/acceleration must fit available grip force.
All cells change 40 mm; independent signed channels granted. A shared signed
source needing separate raise/lower passes can be slower.

| Step mm | Cycles/cell | T at H=160, s | Minimum H for strict <30 s | Complete head ceiling, $250 elsewhere/free cells |
|---:|---:|---:|---:|---:|
| .5 | 80 | 202.00 | 1600 | $.156 |
| 1 | 40 | 132.51 | 915 | $.273 |
| 2 | 20 | 90.00 | 582 | $.430 |
| 4 | 10 | 63.25 | 400 | $.625 |
| 8, section collides | 5 | 46.00 | 279 | $.896 |

The weak .05-mm contact corner has only .08 W spare traction. With output mass
W/g, upward acceleration and downward braking are limited to **784.8 mm/s²**,
before guide drag; nominal 5,000 mm/s² is incompatible with that corner. Applying
this bound to the loaded feed only, leaving empty reset at 5,000, gives minimum
H=2,134/1,600/915/640/458 for .5/1/2/4/8-mm steps. At 2 mm, T(H=160)=138.77 s.
At that step size, 27 alternatives crossing ramps 1/3/10 ms, phase bounds
0/1/3 ms and speed caps 100/200/500 mm/s require **800–1,280 heads**. Increasing
speed does little while short strokes are acceleration limited. These are
conditional schedules, not machine optima; synchronizing bank strokes or variable
force/preload changes the construction. The 8-mm geometry still fails.

Matched direct control with one 40-mm feed and return has .58-s service, 29.2 s
at H=160 and minimum H=157. Its full-stroke capture, support and cost remain open;
this is schedule comparison, not hardware selection. Strict 30-s equality is
excluded with a numerical guard; 267 heads at 8 mm give exactly 30 s, not a pass.

At 1-mm steps there are **512,000 loaded grip transfers/map** and 6,400 permanent
A/B pairs: 12,800 grip/return functions, 25,600 pad surfaces, 6,400 B slide/stops,
column guides and H three-coordinate writer interfaces. Normal opening commands
owe up to the actual spring force/work: nominal elastic preload energy is 3.2 mJ
per grip at 1 N, scaling to 32 mJ at the 10-N design. Return energy recovery is
unbuilt. Springs may be shared in sheets but independent motion/grounding remains.
Ten seconds per grip installation alone is 35.6 h; not measured assembly time.
No print-time/yield estimate without full geometry. Bought inequality is
`Cshared+H*chead+6400*ccell<500`; at $400 and $250 shared only $150 remains.
No sourced BOM or affordability pass. Repeated friction/spring interfaces retain
wear, creep, fatigue, anisotropy, interlayer, hole/first-layer and calibration risks.
Common bias can defeat a bank; no fabricated distributions or lifetime claims.

Unselected indexed cells keep A and B uncommanded. A shared moving B carrier with
both grips closed instead forces strain/slip in the unchanged column, so bank
sharing owes real isolation. Shared frame compliance still couples indexed cells.
Actual top position and load-support proof are required, not writer position or
step count. At per-transfer false acceptance p, expected missed transfers are
512,000p at 1-mm steps without needing independence (51.2 for illustrative 1e−4);
this is not predicted failures or a measured p. Common bias and abort/retry time
are unqualified. Faulted supports require a real prop/service path.

**Decision:** stop detailed indexed 1/2-mm walker development on this schedule;
its retained contact advantage does not offset head count and transfer inventory.
Do not print or tune springs. Keep deliberate stationary overlap as a changed
contact-control option; stop the literal 8-mm section on collision. Reopen with
an explicit bank-isolated enable/feed construction that reduces control count
without reintroducing a separate pickup, or a materially better complete time/cost
bound. Ordinary electrically driven piezo walking remains an unpriced reference.

Next useful axis: **direct writing of resident mechanical state using shared
spatial fields**, with local load path retained. Revisit source domains outside
contact-drive refinements: magnetic reluctance routing versus E-138's rotating
head and A-016's switches; ask whether passive spatial shielding can remove local
release wiring while preserving arbitrary-map isolation. First bound field/force
contrast and shield saturation including adjacent unselected states; stop if it
only renames the existing crossed-field selector or hides 6,400 active gates.
No broad landscape saturation or CEO boundary is asserted.

Self-review: exact event minima versus 1k/4k/16k time-sample holdouts; zero-friction,
load scaling and signed reach limits; analytic pad-envelope separation and positive
intersection witness; hybrid work balance; grip/acceleration consistency; strict
integer scheduling. These check the stated models, not manufactured contact or an
independent validation.
