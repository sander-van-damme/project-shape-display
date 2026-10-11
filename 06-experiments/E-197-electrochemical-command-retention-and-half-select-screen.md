---
status: complete
builds-on: [E-196, E-075, E-094, E-183, A-017]
---

# Small chemical commands exchange wet support for selection and reset obligations

**Deprioritize passive retained chemical release.** Accumulated half-selection,
release work and full-board write/erase time discriminate the embodiments below.
Independent gas and low-work flags remain conditional; no machine/print selected.

Initial input main `8b45df6`; strain/control extension input `64ef162`. Reproduce:
`python3 tools/curated-experiment-checks/E-197/command_memory.py`.
Evidence: sourced observations, analytical/state screens and self-review; no
contact CAD, calibrated constitutive/process prior, project measurement or BOM.
Scenario bounds establish no hardware/yield/lifetime qualification.
## Causal routes and source evidence

E-196 functional recombination; literature adds impulse → dry flag. Strain/lever
is not new material discovery. No landscape-saturation claim.

| Command | Address, motion, state and load |
|---|---|
| Plated electrical bridge | Addressed micron contact drives a separate coil/heater retracting an unloaded dry pawl. Captured setter moves column; dissolution erases command. Persistent conductivity is neither mechanical support nor power-loss closure. |
| Gas diaphragm | Isolated electrodes generate gas; sealed membrane/follower retracts spring-return pawl. Setter retains capture until recombination, seating and proof. Service path is column → pawl → frame, never membrane. |
| Redox strain | Isolated swelling film pulls dry release through flexible seal/lever; reverse charge and spring reset. Retained ion state need not clear on disconnection. Finite bound below. |
| Chemical impulse → flag | Gas impulse sets low-work bistable flag; later cam supplies release work. Requires mechanical erase/readback and supported reset after source loss. |
| Dry controls | A-017 SMA, E-075 spatial magnetic flags, E-183 fixed-gap magnetic memory, direct mechanical head. Each still owes capture, arrest, readback and local recovery. |

States: PARKED → CAPTURED/UNLOADED → OPEN → MOVED → RESEATED/PROVED → RELEASED.
Persistent fault isolates a supported module; source-loss/reset rules below.

Primary sources accessed 2026-10-11:

- [Uvarov et al., 2018, pp.2–6](https://arxiv.org/pdf/1801.00481): 500-µm-diameter,
  8-µm-deep silicon/SU-8 chamber, 30-µm PDMS membrane. At 10 Hz, 10-ms excitation
  gave 4.8-µm deflection; half-relaxation 18 ms, return about 50 ms. A 0.6-µN
  mirror load does not qualify a mN release; no universal reset constant transfers.
- [Uvarov et al., 2024, pp.9–18](https://arxiv.org/pdf/2408.03103): ball work
  **1.2 µJ** from **7.3 mJ electrical input**; separate loaded-plate test estimates
  **.49 N instantaneous force**. Do not multiply that force by arbitrary stroke.
  Ru microelectrodes/containment and impulses do not transfer to X1C PLA.
- [Sheybani and Meng, 2015, pp.919–921](https://biomems.usc.edu/publications/2015/2015_SNB_RecombinationAcceleration.pdf):
  catalyst contact, volume, gas transport and orientation alter recombination;
  competing scenarios are warranted, not a fitted universal probability law.

## Retained gas scan: accumulated half-selection closes the window

Grant ideal V/2 wiring, zero sneak/wire losses: selected row +V/2, selected columns
−V/2, others zero. Polarity-insensitive gas production admits a map where the
first target receives one full pulse and nothing later, while a never-target
receives R half pulses. Three columns suffice; source constructs the witness.
Signed copper dissolution is a different law and is not rejected by this result.

Inventory in charge-equivalent units follows `q'=I−kq`; I is net gas generation,
k a loss scenario; tau=row slot, H=hold. With `a(k,t)=(1−exp(−kt))/k`, `a(0,t)=t`:
`q_target/I=a(k_fast,tau) exp[−k_fast((R−1)tau+H)]`;
`q_unwanted/(r I)=a(k_slow,R tau)`, where `r=I(V/2)/I(V)`.
A common amplitude exists only when
`r<(q_target/q_unwanted_at_r1)*(1−g)/(1+g)*(1−d)/(1+d)`.
g,d bound production and thresholds; k±25% allows spatial and coherent batch
corners. No IID assumption, calibrated prior or intrinsic reaction threshold.
Increasing all currents cannot reopen a closed interval.

For tau=.01 s, H=.24 s (40 mm at 200 mm/s, 5,000 mm/s²), g=d=.10:

| Rows | r ceiling, k=0 | k=1 /s | k=10 /s |
|---:|---:|---:|---:|
| 80 | .008368 | .003052 | 1.212e−7 |
| 20 | .03347 | .02093 | .0002813 |
| 10 | .06694 | .04571 | .001446 |
| 5 | .13388 | .09553 | .004558 |

At k=0 nominal, r<1/R; bounded r<.669421/R. R=80,k=1/10 needs nominal peaks
4.435/483,079× threshold, not permissible pressures. Quarter-power heating also
fails this inventory law; actual thermal/magnetic state needs its own model.

Of 1,125 grid cases, 294 have minimum full-only peak ≤2× threshold; not a
pressure bound, since selected sites also collect half pulses.
Active erase/refresh/switches change the law and cost timing/hardware.

## Gas work/current and complete-head schedule

Favorable isothermal 298.15-K scenario: membrane-equivalent area A, stroke x,
initial inert gas V0=A·.1 mm at P0=101325 Pa, preload F0, stiffness K.
`P=P0+(F0+Kx)/A`; `Q=4F[P(V0+Ax)−P0V0]/(3RT)`;
`W=F0 x+Kx²/2`. No leakage, dissolution, Laplace pressure, membrane inertia,
friction or parasitic reactions. This is a chosen cavity, not a universal bound.
Preload at a hard stop requires finite breakaway charge even at zero stroke.

At radius .5 mm, F0=.02 N, K=.1 N/mm:

| Stroke mm | Q mC | Minimum 10-ms mean A | Work µJ |
|---:|---:|---:|---:|
| .025 | .2492 | .02492 | .5313 |
| .100 | .7244 | .07244 | 2.500 |
| .200 | 1.4487 | .14487 | 6.000 |

Source covers 27 combinations radius .25/.5/1 mm, stroke .025/.1/.2 mm,
preload .005/.02/.1 N. Reference .2-mm board dose is 9.272 C. At k=100 /s,
10-ms opening needs .2292 A/site, holding .1449 A/site (11.59 A/80 sites).
Decay to .1 q_open takes ln(10)/k =23.026/2.303/.2303/.02303 s at
k=.1/1/10/100. Inventory threshold is not proved pawl closure time.
Series wiring trades current for voltage/bypass, not chemical work.

The cited 1.2-µJ impulse cannot supply 2.5/6-µJ reference strokes even with
perfect coupling. Low-work flags survive before losses. One cited event/site
costs 46.72 J/board, 1.95 W over 24 s; energy alone is not the dominant rejection.
Cu(II) ideal 1-µm plate/strip takes 31.10/5.442/.5442 s at j=.175/1/10 A/cm²
(E-196; unit efficiency, j=10 extrapolated); electrical bridges still drive
another actuator.

Independently switched cells or spatial two-contact writers escape passive half
selection. Travelling heads reduce wet inventory to 80B but add release coupling
to each parked pawl; compare with direct cams. Grant 200 mm/s, 5,000 mm/s²:
home→old→new→home maximum .520 s over all 1-mm old/new pairs in 0…40 mm.
Continuous bound `80/v+3v/a` agrees. Index 5.08 mm costs .06375 s.
For B banks, R=ceil(80/B), charge set time tS, reset tR, .04-s total capture/
unload/seat/proof, 6 s preparation/registration/final settle and one row retry:
`T=6+(R+1)(tS+.520+tR+.04)+R*.0637495+move((R−1)*5.08)`.
These are unbuilt allocations; holding through motion costs energy. Table below
compares commands. At tS=.01,tR=.05, four-bank 5×5 patch times are 9.007–10.982 s
across all 76 start rows, including dispatch/return/retry; unchanged map needs
nothing. No measured neighbor disturbance or continuous-height retention pass.

With $250 elsewhere, <$500 permits <$.03906/resident site or <$.78125/complete
four-bank head before extra resident purchases; $400 permits $.02344/$.46875.
These are budget inversions, not quotes. Gas residents multiply 6,400 chambers,
membranes, returns/followers, ≥12,800 electrode surfaces, fill/seal/inspection
operations. Ten seconds/site is 17.8 h assembly. Print burden unknown.

Read actual height **and** support, not charge/pressure/flag. Hypothetical 1e−4
false acceptance/site gives .64 expected misses/board without independence;
common reader/bath/temperature faults survive retries. Repairs need temporary
support and isolated cartridges; extraction is unbuilt. X1C warp, holes, layers,
roughness and creep affect dry geometry; permeability, ageing/catalyst history
and bonds affect chemical gain/loss. No yield/lifetime qualification follows.

## Strain: small fast motion does not imply release work

[Madden et al., pp.3–7](https://people.ece.ubc.ca/mm/papers/Madden_SM_1999.pdf)
(accessed 2026-10-11): wet/dry moduli .5/1 GPa, 30–60-µm films, fast strain
amplitudes ~.2%, **estimated** tip force ~1 mN. Liquid tests use ±7 V/several mA;
low-frequency delamination contrasts with 120,000 cycles at 3 Hz. Encapsulated
gels lose solvent over hours. Different specimens/conditions are not an axial
package specification; large strain cannot inherit small-strain frequency.

Construct an independently switched sealed strip anchored to frame, pulling a
dry lever through a bonded flexible tab/membrane, avoiding a wet sliding shaft.
Reverse charge and a return spring reset it. Ground pawl carries service load.
Per site/head: two electrical interfaces, electrolyte/encapsulation, anchors,
flexing boundary, return and lever. Shared gel manufacture does not grant ionic
isolation. No seal geometry/bond/return preload is qualified.

**Ideal calculation:** L=20 mm, width 2 mm, thickness .03 mm, V=1.2 mm³,
E=500 N/mm²; prescribed axial eigenstrain epsilon. Lossless lever magnification m:
`F=EA*epsilon/m−EA*x/(L*m²)`. Optimize all m>0:
`m*=2x/(epsilon L)`; `Fmax=E V epsilon²/(4x)`.
Reference demand: F0=.02 N, K=.1 N/mm, x=.2 mm → .04-N endpoint, 6-µJ work.
Free stroke and blocked force are not simultaneously available outputs.

| Strain scenario | Free stroke mm | Best m | Maximum force at .2 mm | Minimum V, fixed lever |
|---|---:|---:|---:|---:|
| .2%, fast amplitude | .04 | 10 | **3 mN** | **16 mm³** |
| 2%, rate unearned | .4 | 1 | 300 mN | .16 mm³ |

The small fast strip's entire positive-force relaxation supplies only
`E V epsilon²/2=1.2 µJ`: fails 6 µJ even with variable passive gearing.
Energy-only floor is 6 mm³. Fixed-lever 16 mm³ requires .8-mm² area at L=20 mm,
e.g. .4-mm thickness at 2-mm width; thick transport cannot inherit thin-film
speed. Parallel thin films add interfaces. Repeated strokes or continued
change in eigenstrain escape this single-stroke bound, with new timing/reset.

Sixteen bound corners: E=.25/1 GPa, epsilon=.15/.25%, area ±20%, effective stroke
.15/.25 mm (mount/lost-motion scenario). Even optimizing each corner's lever,
all miss endpoint demand: Fmax=.54–15 mN; required V=3.36–80 mm³. Shared material,
film/mount biases allowed; no IID yield/prior. PLA warp, creep, alignment and
roughness add lost motion/force; membrane stiffness, ageing/delamination omitted.

**Escape:** F0=.005 N, x=.025 mm, K=.1 N/mm needs .15625 µJ/7.5-mN endpoint;
original strip ideally gives 24 mN, minimum V=.375 mm³. A low-work flag followed
by a powered cam survives; 25-µm output tolerance/reset remain unqualified.
No assembly advantage over magnetic flags is shown.
Uncalibrated charge sensitivity: `Q=qv V`, `Imean=Q/tset`:
pure sensitivity qv=.002/.02/.2 C/mm³, V=16 mm³, tset=.05 s yields
.64/6.4/64 A/site, 409.6/4,096/40,960 C/board for symmetric set/erase.
Not measured currents/rates or earned charge/strain pairs. Source bending cannot
calibrate this loaded strip; current scales linearly with uncalibrated qv.

## Compare write and erase on the same schedule

Use the direct-head schedule above without overlap. Four banks allow
**<.49726 s set+reset/row**, eight **<1.53945 s**. One/two banks miss 30 s
at zero command delay. Includes preparation, proof allocation, return and retry.

| Command / set+reset seconds | Four banks, s | Eight banks, s |
|---|---:|---:|
| Direct mechanical zero-delay lower control / 0 | 19.56 | 13.07 |
| Independent magnetic timing grant / .010+.001 | 19.79 | 13.19 |
| Gas grant / .010+.050 | 20.82 | 13.73 |
| Strain fast grant, force unearned / .050+.050 | 21.66 | 14.17 |
| Strain medium grant / .5+.5 | 40.56 | 24.07 |
| SMA guide conditions / 1+.4 | 48.96 | 28.47 |
| 1-µm Cu, j=1, eta=1 / 2.721+2.721 | 133.83 | 72.93 |
| Same, extrapolated j=10 / .2721+.2721 | **30.99** | 19.05 |

[Dynalloy](https://dynalloy.com/technical-data-wires/) (rechecked 2026-10-11)
supplies 50-µm wire, 85-mA/~1-s contraction, .4-s LT static-air cooling.
Assumed 4% strain needs 5-mm wire for .2 mm; ~.353-N pull pays ~.137-N guide
return force plus friction. Packed cooling/terminals unqualified. E-183's magnetic
state model earns no 10/1-ms timing: those are independent-drive grants.
Copper omits downstream transducer time and still fails four-bank synchronous
operation at all three rate scenarios. Eight banks/j=10, thinner gaps or parallel
resident programming escape, but require inventory/retention/isolation and
bridge-resistance, corrosion/erase-tail bounds. No whole-machine timing pass.

Quiescent state requires ground engagement and reset command. Source loss while
open: Cu bridge can persist as downstream supply dies; gas decays; PPy retains
charge/strain; SMA cools; remanence stays set. None proves tooth engagement.
Observe reset under capture; failed reset retains independently arrested setter.
Stuck supply is a separate fault. Reverse PPy drive needs bidirectional switches
or spatial contacts, isolated ionic paths and mechanical neutral readback;
shorting electrodes is not demonstrated reset. Return springs cost force/work.

Stop the small fast-strip/reference-release combination and four-bank synchronous
micron-Cu embodiment under these bounds. Other layouts, independently switched
gas and low-work strain/impulse flags remain conditional. Deeper chemistry needs
a packed supported reset and assembly/isolation advantage over dry control.

## Decision and checks

Stop retained passive-matrix gas refinement without measured dose histories
meeting the window and supported loss/reset. Independent gas remains possible;
no net dry-head advantage is established. Reopen strain/impulse flags only with
packed low-work geometry, reset, coupling and containment advantage. No print
or purchase: model-to-package discrimination has higher value now.

Next axis: shared patterned flexure/contact sheets with separate supported
islands versus assembled pawls/direct heads; cross-check E-076/E-172/E-177.
Stop if this merely shares faults or repeats known reset/routing.

Self-review reconstructs V/2 voltages and exhausts 256 six-row histories; checks
zero loss, exact gas/Faraday conservation, zero stroke and preload breakaway;
independent RK4 inventory errors at 10/20/40 steps are 3.86e−9/2.35e−10/1.45e−11 C.
The 0.520-s route has a continuous analytical holdout. These verify reduced
calculations, not contacts, electrochemistry, source-loss arrest or hardware.

Lever self-review: grid force errors 3.92e−7/2.49e−8/1.56e−9 N at 32/128/512
intervals; work quadrature 1.2 µJ. Ideal loading path, volume floors and copper
schedule checked; no seal/contact/constitutive validation or independent review.