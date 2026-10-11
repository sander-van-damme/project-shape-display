---
status: complete
builds-on: [E-196, E-075, E-094, E-183, A-017]
---

# Small chemical commands exchange wet support for selection and reset obligations

**Deprioritize chemically retained passive-matrix release commands.** Under the
constructed scan, low half-voltage reaction alone is insufficient: accumulated
reaction and retention through the move demand much stronger isolation. Independently
switched fast gas commands remain conditional; a chemical impulse setting a dry
latch is a distinct escape, with an energy rather than peak-force gate. Neither
establishes an advantage over a dry writer. No machine, purchase or print selected.

Input main `8b45df6`. Reproduce:
`python3 tools/curated-experiment-checks/E-197/command_memory.py`.
Evidence: primary-source observations plus deterministic analytical/state-history
screens, self-review. No constructed contact assembly, electrochemical transport
solution, calibrated manufacturing prior, physical measurement by this project,
sourced BOM or lifetime/yield qualification. Bounds below are assumptions.

## Functional alternatives and source evidence

E-196's chemistry-to-command recombination is continued, not counted as another
independent discovery. Search of fast electrolytic microactuators exposed a newer
**impulse → dry memory** alternative. Redox strain was also considered; it changes
the force transducer but presently lacks a supported force/stroke/reset package.
Repository E-075/E-094/E-183 and A-017 already cover mechanical flags, retained
commands, magnetic and thermal alternatives. No landscape-saturation claim.

| Route | Complete causal combination and unresolved boundary |
|---|---|
| Deposited electrical bridge | Addressed electrode closes a micron contact; the contact controls a separately powered coil or heater that retracts a dry pawl. A captured setter lifts/unloads, positions and returns the column to the pawl. Dissolution clears the command. The bridge is neither mechanical stroke nor a support: driver, dry actuator, ground support and setter remain; bridge/contact persistence is not power-loss closure. |
| Gas-to-spring release | Individually contained electrodes create gas; a sealed membrane pushes a dry follower, retracting an unloaded backed pawl. Setter carries the column until gas disappears, return spring seats pawl, and load proof passes. Terrain load goes column → pawl → frame, never through membrane. A membrane seal avoids a wet sliding shaft, but not containment, follower clearance, fatigue or electrolyte service. |
| Redox strain | An ion-swelling strip/laminate bends an unloaded release dog, with spring or reverse electrochemical drive for reset. Same setter/support/proof sequence. Stored ion state need not reset on disconnection. No material law or packed candidate constructed; unknown, not rejected. |
| Chemical impulse → dry latch | A microbubble impulse sets a bistable low-work command flag; a later mechanical cam supplies release work. Positive ground pawl and captured setter still carry load. Mechanical reset and flag readback are required. Fast gas decay no longer erases the flag, but the flag may stay OPEN after source loss; a separate supported reset/arrest remains necessary. |
| Dry controls | A-017 heater/SMA plus spring reset; E-183 fixed-gap magnetic memory or E-075 spatial magnetic flag; direct mechanical head. None is a qualified machine. Thermal decay stores command too; remanence/detents can retain OPEN; direct heads retain their acquisition/arrest/readback burden. |

The gas route's normal states are PARKED → CAPTURED/UNLOADED → OPEN → MOVED →
RESEATED/PROVED → RELEASED. Failures before OPEN retain ground support; during
OPEN/MOVED, chemical reset does **not** guarantee an immediate engaged tooth or
arrest a free setter. Keep capture until actual support is proved. A stuck energized
command differs from source loss. Persistent failure isolates a supported module;
no end-state symbol is accepted as proof of contact continuity.

Primary sources accessed 2026-10-11:

- [Uvarov et al., 2018, pp.2–6](https://arxiv.org/pdf/1801.00481): 500-µm-diameter,
  8-µm-deep silicon/SU-8 chamber, 30-µm PDMS membrane. At 10 Hz, 10-ms excitation
  gave 4.8-µm deflection; the reported half-relaxation was 18 ms and return about
  50 ms. Their 0.6-µN mirror load is not a mN release-force qualification.
  Other operating regimes reach higher frequencies; no single universal reset
  constant transfers to the proposed diaphragm.
- [Uvarov, Shlepakov and Svetovoy, 2024 preprint, pp.9–18](https://arxiv.org/pdf/2408.03103):
  impulse-driven ball work **1.2 µJ** for **7.3 mJ electrical input**; a separate
  loaded-plate experiment estimates **0.49 N instantaneous force**. These are
  different tests, not a 0.49-N actuator over an arbitrary stroke. Microfabricated
  Ru electrodes/containment and impulsive dynamics do not transfer to X1C PLA.
- [Sheybani and Meng, 2015, pp.919–921](https://biomems.usc.edu/publications/2015/2015_SNB_RecombinationAcceleration.pdf):
  catalyst contact, gas transport, volume and orientation change recombination.
  This supports using competing reset scenarios, not importing a probability law.

## Retained scan: an explicit arbitrary-map half-selection witness

Grant ideal V/2 addressing with no wire drop or sneak network: selected row +V/2,
selected columns −V/2, other wires zero. Gas production is polarity-insensitive.
A selected cell in the first row can receive one full pulse and no later pulse;
a never-selected cell in another column can receive **R half pulses** through
an R-row scan. Both histories coexist in one map (three columns suffice; source
constructs it). Thus the witness is a real row schedule, not arbitrary pulse noise.
Copper dissolution with signed charge is a different law and is not rejected by it.

Let q be generated-gas inventory in charge-equivalent units, `q'=I−kq`.
Production I is *net retained gas generation*; k is a hypothetical first-order
loss rate, not a fitted nanobubble model. Define r=I(V/2)/I(V); neither r=.5 nor
any intrinsic electrochemical threshold is presumed. Each row lasts τ; the first
selected command must survive `(R−1)τ+H` after its pulse through mechanical dwell H.
Positive linear dynamics give exact worst histories:

`a(k,t)=(1−exp(−kt))/k`, with `a(0,t)=t`;
`q_target/I=a(k_fast,τ) exp[−k_fast((R−1)τ+H)]`;
`q_unwanted/(r I)=a(k_slow,Rτ)`.

Allow production gain ±g, threshold ±d, and k±25% independently across sites
and coherent batches; g=d=.10 are **explicit bounds**, not priors. A common
uncalibrated amplitude exists only if
`r < (q_target/q_unwanted_at_r1)*(1−g)/(1+g)*(1−d)/(1+d)`.
Shared biases and worst spatial corners are permitted; no IID yield follows.
At k=0 nominal, **r<1/R**; with g=d=.10, **r<.669421/R**.
Increasing every current equally cannot fix a closed interval.

For τ=.01 s, H=.24 s (the prescribed 40-mm rest-to-rest leg at 200 mm/s,
5,000 mm/s²), calculated r ceilings are:

| Rows/bank | k=0 | k=1 /s | k=10 /s |
|---:|---:|---:|---:|
| 80 | .008368 | .003052 | 1.212e−7 |
| 20 | .03347 | .02093 | .0002813 |
| 10 | .06694 | .04571 | .001446 |
| 5 | .13388 | .09553 | .004558 |

At R=80,k=1 the earliest cell needs a nominal full-pulse peak at least **4.435×**
its nominal opening threshold. At k=10 it needs **483,079×**. These indicate
extrapolation/overpressure obligations, not permissible operation. A nominal
quarter-power resistive heater has r=.25 and also fails this retained 80-row law;
real thermal conduction/phase thresholds require their own model. Magnetic
hysteresis does not follow this inventory law; E-075/E-183 supply its controls.

A 1,125-case grid crosses R=80/20/10/5/1, τ=.001/.01/.05 s,
H=.05/.2/.5 s, k=0/.1/1/10/100 /s and r=.001/.01/.1/.25/.5. There are 294
conditional windows whose **minimum nominal full-only pulse** is ≤2× threshold.
That amplitude criterion is a screening preference, not a pressure-safety bound:
selected cells may also accumulate half pulses. No actual chemistry earns these
windows; calibrated site driving, active erase/refresh, nonlinear loss and extra
selectors change the model and retain their timing/electronic costs.

## Small gas displacement helps charge, not retention or load transfer

Separate favorable quasi-static gas scenario: piston-equivalent membrane area A,
stroke x, initial inert gas volume V0=A·.1 mm at P0=101325 Pa, spring preload F0
and stiffness K. Isothermal 298.15 K; no leakage, dissolution, Laplace pressure,
membrane inertia, friction or competing reaction. Liquid displacement is sealed.

`P=P0+(F0+Kx)/A`; `Q=4F[P(V0+Ax)−P0V0]/(3RT)`;
`W=F0 x+Kx²/2`. The initial dead gas is retained; only generated gas recombines.
A hard-stop preload requires a finite breakaway charge even at x=0. This chosen
cavity is not a universal lower bound or a validated model of the cited device.

For radius .5 mm, F0=.02 N, K=.1 N/mm:

| Stroke mm | Charge mC | Minimum 10-ms mean A | Spring work µJ |
|---:|---:|---:|---:|
| .025 | .2492 | .02492 | .5313 |
| .100 | .7244 | .07244 | 2.500 |
| .200 | 1.4487 | .14487 | 6.000 |

Code evaluates 27 combinations of radius .25/.5/1 mm, stroke .025/.1/.2 mm,
preload .005/.02/.1 N. At .2-mm reference stroke total one-shot board charge is
9.272 C. With k=100 /s, 10-ms charging instead needs **.2292 A/site**, followed
by **.1449 A/site** to hold; 80 held sites total 11.59 A at the electrodes.
Series wiring trades bus current for voltage/bypass, not chemical work. Return
from q_open to a stipulated .1 q_open takes ln(10)/k: **23.026/2.303/.2303/.02303 s**
for k=.1/1/10/100. This inventory threshold is not proved pawl closure time.

For the electrical-bridge route, E-196's favorable Cu(II) 1-µm growth/strip
round trip is **31.10/5.442/.5442 s** at j=.175/1/10 A/cm², unit efficiency.
A nanoscale bridge changes that distance but still commands another actuator.
For the impulse route, even ideal coupling of the reported 1.2 µJ cannot supply
the 2.5/6-µJ reference strokes. A .025-mm/low-force flag remains energetically
possible before coupling losses. Mechanical amplification cannot increase work.
One cited electrical event/site would be 46.72 J/board (1.95 W over 24 s), not
an alarming mean-energy floor; delivery, reset, manufacture and durability decide.
Do not multiply the separate peak-force result by free stroke to invent 49 µJ.

## Independent addressing escape: full-machine obligations

A per-site switch or spatial two-contact writer avoids repeated half-selection;
a continuously driven row can keep fast gas open while moving. It restores
independent release control. Keeping only 80B chemical transducers on travelling
heads reduces wet inventory but adds a mechanical release coupling to every
parked pawl; compare directly with a head-driven cam, not 6,400 wet cells.

For a direct 80-head/bank comparator, grant 200 mm/s, 5,000 mm/s² and positions
0…40 mm. Exhaustive 1-mm old/new pairs give **.520 s** maximum home→old→new→home;
continuous upper bound `80/v+3v/a` independently agrees. Row index 5.08 mm costs
.06375 s. Charge .01-s command establishment, .04-s total capture/unload/seat/proof
allocation, reset tR, 6 s preparation/registration/final settle, one complete row
retry per active bank, and carriage return from last row. Command holds through
movement; its replenishment is not free. These slots are unbuilt grants.

| Banks / complete heads | tR=.001 s | tR=.05 s | tR=.4 s |
|---:|---:|---:|---:|
| 1 / 80 | 59.40 s | 63.37 s | 91.72 s |
| 2 / 160 | 32.99 s | 35.00 s | 49.35 s |
| 4 / 320 | 19.79 s | 20.82 s | 28.17 s |
| 8 / 640 | 13.19 s | 13.73 s | 17.58 s |

Thus millisecond chemical reset alone does not eliminate bank/head duplication.
A 10-s reset misses 30 s even with eight banks. For four banks/tR=.05,
a 5×5 patch at all 76 row positions takes **9.007–10.982 s**, charging dispatch,
return and one row retry; unchanged map needs no operation. Unchanged pawls stay
supported in the proposed sequence, but physical neighbor disturbance is unbounded.
Arbitrary continuous heights need an appropriate retention geometry; the timing
calculation cannot grant a 1-mm rack acceptance or a completed support mechanism.

With $250 elsewhere, <$500 leaves <$.03906/resident site or <$.78125/complete
head at four banks **before extra resident purchases**. $400 total leaves
$.02344/site or $.46875/head. These are budget inversions, not quoted costs.
Gas residents multiply 6,400 chambers/membranes, ≥12,800 electrode surfaces,
returns/followers, electrical isolation, fill/seal and inspection operations;
dry supports/columns remain. Ten seconds/site assembly alone is 17.8 h. Printed
mass/time/scrap remain unknown without integrated geometry, not assumed zero.

Read actual height and ground engagement, not integrated charge, pressure, coil
state or flag alone. Common reader/bath/temperature faults can affect a bank;
a hypothetical 1e−4 false acceptance per cell gives .64 expected missed cells
per map without assuming independence. No such rate is established. Retry with
the same fault is not independent evidence. Repairs need captured temporary
support and isolated wet/flag cartridges; no extraction path is constructed.
X1C alignment, warp, hole bias, roughness, layer weakness and creep affect the
support/follower; membrane bonds, permeability, electrolyte ageing and catalyst
history affect k, gain and threshold. The tested boxes do not qualify them.

## Decision and checks

Stop passive retained-matrix chemical-release refinement without measured
half/full dose histories that meet the derived window and a finite supported
loss/reset sequence. Independently switched gas remains possible but has no
shown net advantage over a dry head. Do not promote the impulse lead from peak
force: reopen only with a packed low-work flag, bidirectional reset, impulse
coupling and manufacturable containment that beats magnetic/mechanical control.
No physical calibration is justified before that discriminator.

Next higher-value axis: **selection by shared manufacturing substrate**, rather
than another per-cell transducer. Compare one patterned flexure/contact sheet
with mechanically separate supported islands against assembled pawls/direct heads;
first cross-check E-076/E-172/E-177 and prior laminar selectors. Seek elimination
of repeated assembly/calibration, not merely a renamed latch. Stop if the sheet
only turns local faults into correlated release or repeats known reset/routing.

Self-review reconstructs V/2 voltages and exhausts 256 six-row histories; checks
zero loss, exact gas/Faraday conservation, zero stroke and preload breakaway;
independent RK4 inventory errors at 10/20/40 steps are 3.86e−9/2.35e−10/1.45e−11 C.
The 0.520-s route has a continuous analytical holdout. These verify reduced
calculations, not contacts, electrochemistry, source-loss arrest or hardware.
