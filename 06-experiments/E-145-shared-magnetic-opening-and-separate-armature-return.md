---
status: complete
builds-on: [E-138, E-143, E-144, E-141]
---

# Shared magnetic opening removes the moving bar, not shared fault exposure

**Stop the tested shared-yoke and series-lever embodiments; retain separate spring
armatures as a conditional loss-of-field improvement.** A four-armature reluctance model
exposes partial-opening starvation despite adequate all-rest force. More iron repairs
nominal force, not local-loss response or joint feasibility. No complete machine or
fabrication candidate is selected; no principle-level ban.

Input main `cb24b85`; LAB-245. Reproduce (Python 3/NumPy): `OPENBLAS_NUM_THREADS=1
python3 tools/curated-experiment-checks/E-145/shared_field.py`. Evidence: sourced
principles, calculations, finite magnetic networks, self-review. No FEM/contact CAD,
calibrated prior, supplier BOM, physical or yield evidence. JSON is disposable.

## Causal combinations and controls

All options use separate reversible spatial heads: capture/take load, release parked
support, move, restore/prove support, close/prove head clamp, withdraw. Arrest must grip
**beyond capture**; E-142 elastic escape and E-132 terminal collisions remain open. All
retain 6,400 guided columns/supports/returns, 40-mm travel and 5.08-mm tops. Larger
internal head pitch does not solve terminal access.

| Opening mechanism | Causal difference / fault |
|---|---|
| Parallel comb | One fixed coil/yoke attracts separate two-gap spring-return armatures; no moving common pole. Seated bridges divert flux; common iron saturates. |
| Series flux + 4:1 levers | Flux traverses all four independent bridges; 1.6-mm armature motion opens jaws .4 mm. No parallel flux stealing, but gaps/MMF add and a large-gap jam weakens all heads. |
| Independent coils | Separate circuits allow local turn-off, repeat drivers. E-143's $6 Adafruit 412 control costs $726 at 121 heads without motors; its work shortfall remains. Custom coils below are unpriced. |
| E-144 local bleed | Separate returns after finite supply loss survive blocked exhaust; baseline 171.7-ms equilibrium 11-N capacity, ≥29.23 W/head dwell. Sustained pressure stays OPEN. |

Recombinations, not novelty. E-138 resident permanent-magnet rotors differ from these
soft armatures; residual/stray fields still count. Parked supports must be outside the
opening field and unused heads undocked; exposure is not field-verified.

## Force/work assumptions and magnetic model

Use E-144's explicit competing friction boxes, not new product service ratings: 10-N
output load, .4-mm summed equivalent opening coordinate q; nominal spring 800 N ±20%,
slope 200 kN/m, return-guide shunt 40 N at μ=.02. Scale spring, slope and shunt together
by `.02/μ`. Peak opening force / opening work per head:

| Assumed friction floor | Peak force | Work including adverse guide shunt |
|---|---:|---:|
| .02 | 1,080 N | .416 J |
| .1 | 216 N | .0832 J |
| .3 | 72 N | .02773 J |

All give minimum zero-field contact capacity 12 N. This report's finite bank uses
**μ=.1**, explicitly a more favorable alternative, not a qualified material. At q=0
opening needs 200 N; at q=.4 mm it needs 216 N. Minimum return force at full opening is
136 N. Leverage preserves work.

[MIT, energy/coenergy and force](https://web.mit.edu/6.013_book/www/chapter11/11.7.html)
provides the governing method. Each bridge has two moving gaps g and pole area A per
gap. Flux φ gives `F=φ²/(μ0 A)`; reluctance is `2g/(μ0 A)` plus finite iron. Use a
monotone piecewise constitutive **scenario**, `H=B/(μ0 μr)` below knee Bk, then slope
`1/μ0` above it. Baseline μr=1,000, Bk=1.5 T. This is neither a fitted B-H curve nor a
hard flux cap. Extreme post-knee currents are not design predictions.

[ARMCO Pure Iron data, table 6 and stress
discussion](https://www.aksteel.nl/files/downloads/clf_productdata__armco_pure_iron_pdb_euro_final_072022_92.pdf)
reports as-received maximum permeability 1,000–2,500 and coercivity 95–200 A/m;
annealing and machining stress change the response. Maximum permeability is not a
constant working permeability. We therefore use competing μr=200/5,000, Bk=1.3/1.8-T
bounds, not a purchased-steel or printed-material prior. Sources accessed 2026-10-11;
their data do not qualify machined miniature assemblies.

## Finite four-head section: startup is not every-state opening

The direct bank uses 400-mm² poles (20×20 mm), two per bridge, 30-mm pole legs, 60-mm
bridge path, and two 160-mm rails at 40-mm internal tap pitch. Rail/root section is
1,600 mm², with a 60-mm root link. Independent bridges translate .4 mm; nonmagnetic
stops leave .2-mm attracted gaps, hence .6-mm resting gaps. The pole faces never touch
in the model. Pivot/guide fits, spring packaging, support/frame deflection and the
connection to terminal jaws are **not constructed**.

Two models: common-path surrogate (.32-m shared/.06-m local iron) and distributed
four-tap network (.06-m root/.04-m segments per rail/.12-m local iron including legs).
The surrogate deliberately omits .06 m of local iron; it is not a force bound. Both include
bypass permeance .2 times four nominal gap-only branches. The surrogate solves MMF/flux
balance; an independent Newton energy solve resolves each rail segment. This finite bank
exposes the fault before full contact CAD is warranted.

At 1,100 ampere-turns (AT):

| State | Common-path force on resting head | Distributed-rail force on resting head |
|---|---:|---:|
| All four at rest | 224.16 N | 236.96–282.59 N |
| One bridge attracted | 206.36 N | Not evaluated |
| Three bridges attracted | **167.70 N** | **162.54 N far tap / 186.56 N near tap** |

Attracted means **jaw OPEN**. All-rest passes 216 N, but three already-attracted or
stuck-OPEN bridges leave the fourth below **200-N start force** in both models. This is
a static fault witness, not nominal sequence prediction. A missing armature (10-mm gap)
instead raises its three neighbors to 246.05 N in the surrogate.

Enumerating all 15 endpoint states with at least one resting armature, and requiring 216
N there as a sufficient static margin, needs worst-case 3,309 AT at 1,600-mm² root.
Doubling root section to 3,200 mm² lowers that to 1,018 AT; halving to 800 mm² needs
>20,000 AT in this constitutive model and is stopped. Changed iron allocation repairs
nominal starvation; endpoints do not certify intermediate motion or spring/guide
geometry.

32 coherent all-rest corners cross gap bias −.10/+.15 mm, effective overlap area .8/1.0,
μr 200/5,000, knee 1.3/1.8 T and bypass factor 0/.5. Force spans **28.74–525.33 N**;
11/32 exceed 216 N. These are equally enumerated scenarios, **not samples, probabilities
or yield**. Separate force-discrepancy multipliers .7/1/1.2 change nominal 224.16 N to
156.91/224.16/268.99 N. These bound unknown fringing/nonuniform stress, not validated
field error. A +20% correction can reverse marginal starvation; resolved fields are
needed.

Gap/shim bias, warp, overlap, magnetic batch and coil temperature are correlated. X1C
PLA would locate bought iron; layer/hole/first-layer errors, anisotropic compliance,
creep, wear and thermal drift have no calibrated prior. Local seizure, spring breakage
and bank distortion remain separate faults; no yield follows.

## Series lever, copper and sustained dwell

The series alternative uses A=100 mm², four 4:1 levers, .2-mm residual gaps and 1.6-mm
armature travel (initial g=1.8 mm). A .4-m iron path links all eight gaps. A 54-N
armature force requires B=.824 T and **9,702 AT** at all-rest. Three attracted bridges
reduce this to 3,409 AT; one bridge jammed at rest retains that burden during hold.
Bearings/stops/returns and output coupling remain unconstructed.

Explicit winding scenario: 400 turns, gross window 400 mm², .5 copper fill, ρCu=1.72e−8
Ωm. `R=ρ N² lturn/Acu`, `P=ρ (NI)² lturn/Acu`. Parallel mean turn .25 m gives **3.44 Ω,
2.75 A, 26.02 W/bank**, .448 kg copper. A nominal all-attracted reduction to 600 AT
gives **7.74 W/bank**, only after individual clearance proof; reducing current early can
worsen starvation. 31 banks give ~806 W pull / 240 W hold before rod drives, supply and
switching losses. Four independent custom circuits (.10-m turns, 100-mm² copper window)
need ~852 AT and **12.49 W/head pull**, .0896 kg copper/head, but repeat drivers. These
are allocations, not manufacturable winding drawings or component prices.

Series mean turn .12 m at the same copper window gives **971 W/bank pull**, 120 W with
one bridge still at rest. More copper trades heating for material/space. the parallel
fixed-rest linear model reaches its 200-N start threshold after **93.77 ms at 12 V /
31.99 ms at 24 V**, before armature travel. Peak-and-hold needs real current regulation
and transient supply. All-rest stored energy is .894 J/bank; opening four springs costs
at least .333 J in the μ=.1 box.

Sustained/stalled dwell dissipates I²R; no cooling or temperature limit is earned.
Resistance drift changes voltage-fed force or regulated-current heating. The air bleed
penalty is avoidable in principle, not a response qualification. At assumed iron/copper densities 7,870/8,960 kg/m³, rectangular stock for
this direct section: **6.296 kg iron + .448 kg copper/bank**; 31 banks use **195.18 +
13.89 kg**. This is unoptimized inventory, not a universal bound. Larger yokes or
laminations add material, insulation, joining and alignment.

## Loss, sustained OPEN and recovery are different states

Proposed independent bank cut: supply → normally-off high-side enable → coil → normal
current switch, with passive diode+48-V clamp across coil. A separate non-retriggerable
hardware one-shot drops enable after ≤.6 s; reset requires proved local closure and
parked support. This is an **unbuilt obligation**: switch/timer/clamp/reset/proof
hardware all count. It interrupts a stuck normal switch, not a shorted enable, bypass
wiring or unsafe reset. A fuse cannot detect a normal-current stuck OPEN command.

**Local drive loss with live field leaves its jaw OPEN.** Per-head
voltage/motion/support proof must independently abort the bank or a passive local
mechanism must intervene; detection deadline/false acceptance remain unknown and
hardware counts. A .6-s timeout permits 60-mm zero-force coast at .1 m/s. Bank closure
also interrupts healthy heads.

After actual field removal, a jammed armature does not tie neighbors open; their springs
must still defeat residual attraction/drag. Shared distortion/history remains
correlated.

[TI SLVAE59A, fast discharge](https://www.ti.com/lit/an/slvae59a/slvae59a.pdf) explains
why freewheel and clamped decay differ. Integrate `dt=−d(N Φ)/(R I+Vclamp)` with all
armatures **frozen** at attracted stops and instantaneous anhysteretic magnetic
response. From 1,100 AT, attraction falls below minimum 136-N return force at 418.48 AT:

| Suppression | Force-threshold time | Frozen-coil zero-current time |
|---|---:|---:|
| .7-V diode | 83.454 ms | 310.60 ms |
| 48-V clamp | 9.515 ms | 18.563 ms |

Stored energy at cut: **1.072 J/bank**. Rate clamp pulse energy/voltage and
switch/wiring margin; passive discharge needs no powered gate. These frozen-position
results are **not closure/arrest bounds**: motion, impact, hysteresis and eddy currents
alter flux linkage.

[MIT magnetic diffusion](https://web.mit.edu/6.013_book/www/chapter10/10.6.html)
motivates a discrepancy check: for a uniform slab with zero-field boundaries, `τ=μ0
μdiff d²/(π²ρiron)`. At explicitly assumed μdiff=50–1,000 and ρiron=1e−7 Ωm, 20-mm stock
gives **25.5–509 ms**, 40-mm stock **102–2,037 ms**; .5-mm laminations would give
.0159–.318 ms. These are another boundary problem's characteristic times, not yoke
delays. A coupled transient model is needed before inferring mechanical closure from
9.5-ms electrical decay.

Residual **gap field at jaw contact**, not material Br, is independently bounded at
0/.1/.3/.6 T: remaining μ=.1 holding capacity is **12/11.68/9.14/.54 N**. An 11-N
comparison threshold requires residual field below .177 T. These are stress scenarios,
not values inferred from coercivity. Shims mitigate sticking but increase MMF. Reversed
polarity still attracts soft iron.

Rearm requires actual output/support and local jaw closure/clearance proof; root
flux/current cannot prove four local states. Failed proof retains capture, inhibits
indexing, restores support, then permits one bounded retry or isolates the bank. Common
reader bias, unpowered recovery and retry time remain unresolved.

## Full-display disposition and next discriminator

Count H drives/armatures/returns/proof channels, 2H pole gaps/pads, guides/bearings,
shims/frames; series adds H pivots. Add ceil(H/4) coils/yokes, switches/enables,
suppression/timers, sensing, wiring/power/cooling; retain 6,400 support/return/capture
interfaces. Winding/cutting/annealing, printing, assembly, inspection and repair are
unpriced; no free precision assemblies.

E-143's optimistic `6+ceil(6400/H)*(.45+t_extra)<30 s` includes .4-s travel/.05-s local
operations and six seconds preparation/registration/proof/retry/settling. Extra
.01/.05/.1/.2 s needs 124/137/149/178 heads versus 121 with none. Rise/proof/return must
fit; no earned overlap, free empty return or 9.5-ms mechanical closure. Regional
supports stay loaded; frame/adjacent displacement remains unqualified.

Joint purchases stay <$500, ideally <$200. E-143's hypothetical $250 reserve and $1.56
motors leave <$61.24 at 121 heads. Allocating all to 13.89-kg copper permits only
<$4.41/kg with everything else free: a break-even ceiling, not a market quote. No joint
BOM passes; changed reserve/motors/yokes can reopen cost. Cheap-motor rated power still
fails E-143 independently.

**Decision:** preserve field-off mechanical separation and the circuit model; stop
deeper shared-release optimization now. Reopening needs an economical finite yoke with
all-state margin, bounded coupled field/mechanical return, and an actual local-loss
response while the shared command persists. More nominal ampere-turns alone do not
provide those. No purchase, printing or CEO boundary.

**Next: output-displacement-metered permission instead of duration-held OPEN.** Compare
output-driven finite run-off/rearm, alternating positive catches and continuous opening;
cross-check E-079/E-139/E-144. Seek finite state/geometry bounds under free drive and
stuck OPEN at arbitrary phase, including reversal, dwell, subthreshold coast and impact
absorption. Stop if uncontrolled motion replenishes permission or local powered release
is uncounted. Count 40-mm throughput; report excursion without inventing accepted drop.
This changes closure causality; no new mechanism or search saturation claimed.

Self-review: SI/work and winding I²R identities; zero-field/infinite-root limits; MMF
residual <1e−7 AT; magnetic stress versus coenergy derivative agrees <1e−6 relative.
Distributed energy minimization independently reproduces the fault, with residual <3e−11
AT. Decay 64/128/256/512 subdivisions converges clamp threshold
9.514892/9.514932/9.514934/9.514935 ms; corresponding diode-zero time
310.375/310.547/310.591/310.602 ms. This verifies reduced equations, not hardware.
