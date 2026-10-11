---
status: complete
builds-on: [E-162, E-148, E-121, E-133]
---

# Direct canted support trades release clearance against friction amplification

**Stop the unpreloaded, within-cell aperture embodiment under the declared low-friction
and dimensional bounds; do not reject canted support in general.** A wide lever or
captured lateral reaction changes its force margin. Stop a free-tail stationary
capstan as height memory; an explicitly retained tail remains possible but pays a
large reversal-force penalty. Neither warrants fabrication or a new selected architecture.

Input main `90ac217`. Reproduce: `python3 tools/curated-experiment-checks/E-163/screen.py`.
Evidence: source analogies, analytical equilibrium, finite planar aperture polygons,
deterministic bounded scenarios and self-review. No calibrated manufacturing prior,
complete CAD, elastic/contact dynamics, measurements or independent review. JSON is
reproducible and not retained. Forces .2/1/10 N are sensitivity loads, not requirements.

## Discovery and complete-machine hypotheses

Two independent searches: deployable zipper/origami structures returned E-126/E-133's
existing deployed-column versus grounded-feed distinction; no new principle claimed.
Telescopic furniture/tool locks returned **direct canted-aperture amplification**,
absent from repository washer/sprag searches (E-162's washer is a thrust bearing).
A third, rope-belay functional recombination gives a **stationary** capstan plus
retained tail, different from E-121's driven loop/spool but not a new physical law.
These attempts do not establish search saturation or patent novelty.

Primary references accessed 2026-10-11:
[US7222892B2](https://patents.google.com/patent/US7222892B2/en), retrieved search
abstract/claim text (full page unavailable), describes inclined washers, opposed
supports, elastic return, release spacers and a second washer for opposite locking.
[US4411339A, description](https://patents.google.com/patent/US4411339A/en) describes
cocked end coils on a rod, fixed/rotatable bushings, release by unwinding and two
locking directions. These establish analogies, not our geometry or PLA performance.
[Harvard's capstan demonstration](https://sciencedemonstrations.fas.harvard.edu/presentations/rope-friction-around-pole)
provides the exponential tension law and cautions about bending stiff rope around
small posts. Its large nylon rope/steel pipe friction does **not** transfer here.

| Hypothesis | Addressing, motion, retention, load path | Verification/recovery and repeated liabilities |
|---|---|---|
| Direct canted aperture | Indexed bank heads capture changed rigid tails, unload and straighten a local plate, move 40 mm, then allow return tilt. Pin friction → inclined plate → grounded toe. Opposed plates proposed for bidirectional arrest. | Position plus proof unload; writer stays on failed seat. Two plates/returns and support regions per site; shared frame bends. A stuck release or loss during open travel remains unsupported without head arrest. |
| Stationary capstan | Indexed tail head draws/pays out a private cord over a grounded wrapped post; spring or positive tail keeper retains tension; gravity descends. | Read column height and tail force; keep head until keeper proof. Each site still has cord routing, keeper, return/take-up and wear. Gravity may not overcome guide drag; a second pull path is needed then. |
| Direct jaw / positive seat controls | E-148 returned jaw or E-133's ground-pin seat; bilateral writer supports while locally released. Normal preload or positive engagement grounds load. | Same failed-proof capture obligation; free-input writer arrest, seat access and head economics remain unresolved. Positive seats need no friction coefficient to carry settled axial load. |

All preserve unchanged-site commands; none establishes physical regional isolation.
Stationary posts remove rotating bearings, not the load path, selectors, stored release
command, feed arrest or 6,400 separate state variables. The capstan does not repair
E-121's geometric collision/slack witnesses; its own finite routing is unbuilt.

## Finite aperture and explicit reaction model

Use a rectangular tail with halfwidth r in the x-z section. A plate has a straight
through-slot of halfwidth a=r+c and thickness t; rotation alpha about y narrows its
projected aperture. Opposite material corners first meet the tail at `(±r,±z)`:

```
a cos(alpha) - (t/2) sin(alpha) = r
alpha = acos(r / hypot(a,t/2)) - atan2(t/2,a)
z = sqrt(a² + (t/2)² - r²)                   [mm]
```

The source generates both finite side quadrilaterals through opening→seating; their
extrema prove no tail intersection before seating and penetration just beyond it.
This is an aperture-section check, not a complete rotating washer/support sweep.
Centering is granted. End bridges, actual toe/abutment profile, return spring,
release tool, guides, neighboring plates and moving capture are not constructed.
A circular hole, rounded edges or compliant indentation need different contact geometry.

First grant an ideal vertical grounded toe reaction at horizontal distance b>r,
no lateral reaction, and a return **couple** tau. Horizontal equilibrium gives equal
contact normals N. With downward force F and downward plate tractions TL,TR:

```
TL + TR = F
2 z N = b F + r(TL - TR) + tau
|TL|,|TR| <= mu N
```

At tau=0 the optimum is TL=TR=F/2: `mu >= z/b`. Independently minimizing
`z(1+|d|)/(b+r*d)` for d=(TL-TR)/F confirms it. Minimum extra couple for the
symmetric branch is `max(0,F*(z/mu-b))`; it is a required torque, not an invented
spring. A real spring force also changes toe load and needs its own geometry.
At F=0, tau=0 the symmetric branch supplies no normal preload or zero-load arrest. Reversing F
requires negative N, so the same symmetric branch opens; an opposed plate or other
arrest is owed. No dynamic stopping-distance claim follows from static self-locking.

A second, deliberately generous reaction model allows arbitrary lateral abutment
force and all downward sliding traction at the favorable edge. It relaxes the
incipient-slip threshold to `mu >= z/(b+r)`. This is an optimistic bound, not a
constructed captured support. It prevents incorrectly generalizing the vertical-toe
failure to every canted washer. Preloaded/self-stressed or multi-contact locks are
outside both simple models.

| Nominal r / c / t (mm), b=2.4 mm | Seat angle | Vertical-toe mu minimum | Normal sum at F=10 N | Extra couple at mu=.2 |
|---|---:|---:|---:|---:|
| 1.5 / .025 / .4 | 5.30° | .142 | 70.58 N | 0 |
| 1.5 / .1 / .8 | 10.53° | .286 | 35.01 N | 10.28 N mm |
| 1.5 / .35 / .8 | 25.38° | .481 | 20.79 N | 33.72 N mm |
| .75 / .35 / .4 | 37.56° | .345 | 28.95 N | 17.46 N mm |

The narrow-clearance case amplifies normal force but concentrates ~35.3 N on each
edge at 10 N load. Assumed contact patches .1–1 mm² imply average 353–35.3 MPa;
these are stress sensitivities, not predicted contact patches or PLA allowables.
Edge rounding/creep may destroy the fitted geometry. A single .4-mm-thick printed
plate is not qualified by matching nozzle diameter. Loaded release must first
unload through the writer; forcibly uncanting under full load is no free operation.

## Manufacturing bounds and changed load-path escape

No probability law is justified. Sweep nominal r={.75,1,1.5}, c={.025,.05,.1,.2,.3,.35,.4},
t={.4,.8,1.2} mm: 63 sections. Require a nominal .4-mm outer ligament. Competing
coherent batch cases, not 6,400 independent perturbations:

- Tight-release case: slot halfwidth −.1, tail halfwidth +.1, lateral eccentricity
  .1 mm; require .05-mm residual side clearance. Thus nominal c≥.35 mm.
- Weak-hold case: slot halfwidth +.1, tail halfwidth −.1, thickness +.1 mm. Grant
  recentering for the hold calculation, favorably; do not claim off-center contact.
- mu={.1,.2,.4,.6} are competing surface conditions, not calibrated PLA distributions.
  Thickness/size bounds stand in for layer, hole/slot bias, print and assembly error;
  warp, return aging and local edge damage can worsen them and are not qualified.

Eighteen sections meet release clearance. Count only necessary-condition survivors:

| b (mm) | mu | Vertical toe | Arbitrary lateral reaction relaxation |
|---:|---:|---:|---:|
| 2.4 | .1 / .2 | 0 / 0 | 0 / 0 |
| 2.4 | .4 / .6 | 0 / 14 | 15 / 18 |
| 4 | .2 / .4 | 0 / 18 | 0 / 18 |
| 8 | .1 / .2 | 0 / 18 | 0 / 18 |

These are grid counts, **not yield**. For c=.35 and t=.4/.8, low-friction mu=.2
needs b=5.20–7.15 mm across the tested radii in the vertical-toe model. A broader
lever could be tiered below the 5.08-mm tops; internal pitch is not a product
constraint. Its route, support and neighbor interference must be constructed.
Do not call its scalar pass a packing solution. Conversely, smaller calibrated
errors or metal precision parts could recover narrow-clearance designs, subject
to contact wear, purchased cost and assembly. This is the reopening condition.

## Stationary capstan: amplification also penalizes reverse writing

For total wrap theta, `Fload <= Ttail exp(mu_s theta)`. A truly free tail with
zero tension cannot hold a finite load at any finite wrap. Keeper, deadweight or
spring tension is an indispensable state-support input. When the **tail head**
pulls to raise the column, the high-tension side reverses:
`Twriter = Fload exp(mu_k theta)` at sliding equilibrium. Static and kinetic
coefficients are separate unknowns; the following equal-coefficient cases are
sensitivity scenarios, not a material law:

| Two wraps, assumed mu_s=mu_k | Holding tail at 10 N | Raising tail at 10 N | Work for 6,400 × 1 N × 40 mm |
|---:|---:|---:|---:|
| .1 | 2.846 N | 35.14 N | 899 J |
| .2 | .810 N | 123.45 N | 3,160 J |
| .4 | .0656 N | 1,524 N | 39,016 J |

A head lifting the column directly can avoid tail-side amplification; that changes
capture/routing and forfeits the simple low-force tail writer. A rotating/freewheeling
post changes the mechanism and owes torque arrest. Small-radius cord bending,
creep, stretch, groove crossover and abrasive wear can dominate this ideal law.
Do not deepen the stationary, tail-driven version without a joint force/time/cost
advantage over the direct writer.

## Full-board accounting and disposition

Two aperture plates repeat 12,800 plates/returns and 25,600 edge contacts before
writers, guides and supports. Bought allowance at a hypothetical $250 shared
reserve is only $250/12,800 = **1.953 cents per plate** at the $500 ceiling, even
with all other site hardware free. This is a ceiling, not a sourced BOM; printing
moves cost into strain/contact qualification, material, scrap and assembly. At
10–30 s per site, handling alone is 17.8–53.3 h. Independent return mechanisms
remain repeated costs; a common stuck release remains a correlated fault.

All families owe complete service time. Optimistic `T=6+ceil(6400/H)*tcell`, with
6 s reserved for preparation, indexing outside service, verification, one bounded
retry and settling, needs H=27/68/121/221 for tcell=.1/.25/.45/.8 s at strict <30 s.
At $250 shared and free sites these allow <$9.26/$3.68/$2.07/$1.13 bought per head.
No head, power supply, reader or control BOM is earned. Cell service must include
capture, unload, release, travel, return, proof and any empty repositioning; overlap
is not credited. F=1 N/site is a work sensitivity, not simultaneous service load.

Height readback cannot prove adequate grip. Use proof unload while capture remains
available, then read height; reader false acceptance p=1e−4 implies .64 expected
missed sites/board without assuming independence. Shared datum/lighting errors can
miss whole regions. One retry is a scheduling assumption, not recovery from a
persistent jam; stop an affected module while preserving existing support. No
zero-load, power-loss or stuck-command qualification is supplied.

**Decision:** pause within-cell, unpreloaded printed canted support at the declared
low-friction bounds. Keep wide-lever/captured-abutment geometry as conditional leads,
not winners; retain positive seats and E-148 jaws as controls. Retire free-tail
capstan memory and deprioritize stationary tail-driven writing at high amplification.
A-019's distributed contact remains distinct and unqualified. No printing: current
exclusions are computational and the promising alternative still lacks a load path.

**Next discriminator:** if continuing this support family, construct a finite lateral
abutment and shared-tier arrangement that can actually realize the relaxed reaction
without tightening release clearance or disturbing neighbors. Compare its supported
release path and repeated contact stress against a broad-area direct jaw/laminate.
Stop at missing ground reaction, captured-release collision or no inventory advantage;
otherwise a finite contact model, not another coefficient sweep, earns continuation.
Broader discovery remains open; no whole-landscape exhaustion is claimed.

Self-review: rotated polygon extrema at 16/64/256 intervals agree with analytical
corner coordinates within 5e−16 mm; monotonic aperture closure makes these exact
section bounds, not a sampled full-assembly collision proof. Independent traction
allocation sweep reproduces the force threshold; frictionless, free-tail and
opposite-load limits checked. Midpoint integration of the capstan ODE at 32/128/512
steps reduces tension-ratio error .03004 → .001964 → .000124. No time-step or FEA
convergence, dynamic return, fatigue/life or hardware reliability is inferred.
