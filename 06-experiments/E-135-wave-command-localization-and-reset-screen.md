---
status: complete
builds-on: [M-010, A-001, A-016, E-076, E-080, E-083, E-134]
---

# Wave command delivery: frequency crowding, energy memory and a spatial alternative

**Stop uncalibrated frequency-only addressing and bare additive crossed-wave
thresholds under the tested bounds.** Neither supplies positive isolation.
Retain time-reversed spatial focusing as an unresolved, materially different
command-delivery lead; test its loaded transfer matrix before constructing a
latch. Keep positive mechanical coincidence as the isolation control, with its
existing reset/force/channel costs. No architecture, purchase or print selected.

Input main `4d5ad7e`. Reproduce:
`python3 tools/curated-experiment-checks/E-135/wave_screen.py` (Python + NumPy).
Evidence: primary-source discovery, exact linear-response calculations,
96 deterministic coupled-bank scenarios, exact transient oscillator propagation,
and necessary-condition accounting. No measured X1C priors, stochastic yield,
full plate solver, switch/contact geometry, hardware test or external review.
Generated JSON is reproducible and not retained.

## Discovery and causal architectures

Three varied primary-source domains distinguish confirmation from novelty:

- **Resonant tactile displays:** [Mohammadi et al., 2020](https://doi.org/10.1016/j.sna.2019.111818),
  [institutional abstract](https://researchportal.bath.ac.uk/en/publications/resonance-frequency-selective-electromagnetic-actuation-for-high-/),
  reports tuned taxels sharing a coil, increasing 16 to 32 on 25 cm².
  Vibration selection confirms M-010; it does not demonstrate retained commands.
- **Acoustofluidic microrobotics:** [Kaynak et al., 2023](https://doi.org/10.1089/soro.2021.0193)
  demonstrates tuned bubbles, streaming and inter-bubble radiation forces,
  including reversible bistable actuation at 85/170 kHz. Its final controller
  requires manual reset. Submerged two-photon printed soft-polymer capsules
  supply no transferable dry PLA/FDM properties or scalable reset mechanism.
- **Time-reversal haptics:** [Hudin et al., 2015](https://cim.mcgill.ca/~haptic/devices/pub/CH-JL-VH-TOH-15.pdf),
  [DOI](https://doi.org/10.1109/TOH.2015.2411267), focuses bending waves using
  reversed impulse responses: 148×210×0.5-mm glass plate, 32 channels,
  20–70 kHz, 2-ms focusing time, measured amplitude/resolution 7.68 µm/5.2 mm.
  Near-1-N finger loading reduces approximately 7 µm to 3 µm. This is new
  spatial localization, not a switching-energy or off-target immunity result.

Those are sourced facts; these are engineering combinations:

| Delivery | Causal selection and reset | Disposition |
|---|---|---|
| F: frequency | Broadcast bus → tuned opposed set/reset pickups → retained routing dog | M-010 recombination; uncalibrated frequency/energy bounds fail |
| X: crossed waves | Row+column packets → rectifier → dog; opposed pickup/reverse cam resets | Equivalent to A-001/A-016 thresholds without actual mixing/filtering or positive isolation |
| T: time reversal | Peripheral emitters → focused packet → identical opposed pickups → dog | Different spatial principle; loaded receiver/extraction remains unbuilt |
| P: positive coincidence | Two frame-backed apertures → row-local striker → dog; withdraw before address/reset | E-076 control, retaining E-082/083 force, reset and channel costs |

Each dog routes a powered collet/cam. Height/command readback and support proof
precede release; mismatch retains support and stops motion. A further nonlinear
metamaterial search found transmission control, not a new local selector.
No saturation claim: time reversal supplied a useful spatial axis.

The **40-mm load path is separate**: column → ground pawl/seat → frame during
play; powered tail grip → elevator → frame during release. Seat re-engagement
and proof unload precede grip withdrawal. A-016's ~80-mm relative tail sweep,
finite capture and interrupted-motion recovery remain unresolved. Wave commands
do not repair E-134's free conversion coordinate.

P reuses E-076's ideal-rigid w=.8, aperture=1.6, stroke=1.5, error=.1-mm section:
.20/.90/2.18-mm open/blocked/neighbor margins. This is no new geometry proof.
A rigid full-board ram remains blocked by unselected pins; compliant followers
or local energy routing are necessary. A physical obstruction differs from a
reduced wave amplitude.

## Frequency resolution and correlated bank response

For N logarithmically spaced codes over a decade, adjacent ratio is
`r=10^(1/(N−1))`. Disjoint residual fractional-error boxes require
`r>(1+e)/(1−e)`. Even infinite Q allows at most **116/24/12 labels** for
±1/5/10% residual error. 6,400 labels require **e<0.017992%**, before finite
linewidth, couplings or margins. This is a guarantee over the specified boxes,
not a prediction that every manufactured array has a collision. Common shift
alone can be calibrated away; residual relative error and drifting load remain.
External row selection reduces labels to 80, but adds actual row isolation.

The finite numerical model is an open chain of 8 or 80 receivers, equal unit
mass, nominal angular frequencies 1–10 (normalized to the bottom frequency).
Nearest-neighbor springs have `k_ij=c min(w_i,w_j)^2`; local damping is `w_i/Q`.
Solve at each nominal code frequency:

`[diag(w_i²−omega²+i omega w_i/Q)+L(k_ij)] X = 1`.

This is uniform inertial/force excitation, not independent receiver drives.
The Laplacian includes edge degrees. Coupling c={0,.001,.01,.05}; Q={5,20,100}.
Frequency patterns are nominal, alternating ±1%, coherent +5%, and opposite
±5% half-bank biases plus alternating ±1%. These are bounded illustrative
scenarios, not a distribution, exhaustive interval proof or calibrated PLA
modal/damping values. The pattern couples common material/print bias and local
variation without averaging 6,400 independent samples.

Score `S_i=|X_i|max(1,omega/w_i)` is sqrt(peak local oscillator energy /
`.5 w_i² s²`), reference excursion s=1. Coupling energy supplies no isolation
credit. An **ideal energy-trip surrogate**, barrier ±20%, forcing gain ±10%,
needs selected/off-target ratio `>sqrt(1.2/.8)*1.1/.9 = 1.49691`. Lossless
extraction is granted; no actual rectifier/latch/contact is implemented.
A window only satisfies this surrogate, never switching qualification.

| 80-label scenario | Minimum selected/off-target ratio | Window |
|---|---:|---|
| Q=20, no coupling, nominal | 1.4491 | closed |
| Q=100, no coupling, nominal | 5.5803 | open |
| Q=100, no coupling, alternating ±1% | 1.7352 | open |
| Q=100, c=.01, nominal | 1.2025 | closed |
| Q=100, c=.01, alternating ±1% | 1.0457 | closed |
| Q=100, no coupling, common +5%, fixed codebook | .2045 | closed |

18/96 scenarios retain a window, only four with 80 labels. No sampled
fixed-codebook common/split-bank case passes. These counts are sensitivity,
not manufacturing yield. Retuning a known common shift exactly recovers the
uncoupled ratios; the source checks this scaling. Recalibrating coupled modes,
changing force routing or using isolated banks could change the answer and
requires a new transfer/selection model, not a higher amplitude.

Manufacturing sensitivity: `f ∝ t L^−2 sqrt(E/rho)` for a cantilever.
Assumed t=.6±.05 mm, L=8±.1 mm, E=2 GPa±20%, density fixed, give f/f_nominal
**.79977–1.21697** at coherent corners. These are bounds, not sourced X1C priors.
Layer quantization, wall bias, orientation, creep and load affect tuning;
friction/wear affect damping and extraction. Hole shrinkage, first layers, warp
and assembly alignment need propagation through eventual seat/pickup geometry.
±1% is a favorable calibrated-residual scenario, not promised print accuracy.

## Accumulated half-selection, finite energy and reset

Exact damped-oscillator propagation tests a fixed open-loop history: one
resonant cycle on, one cycle off, repeated 80 times, starting at rest. Unit
natural angular frequency, forcing=1/Q, phase-continuous integer-cycle bursts.
Track `x²+v²`, energy in units `.5 m w² s²`, including off-time motion:

| Q | Single burst peak energy | 80-burst peak | Ratio |
|---|---:|---:|---:|
| 5 | .216592 | .424405 | 1.9595 |
| 20 | .021122 | .290712 | 13.7636 |
| 100 | .0009565 | .2545415 | 266.1184 |

At Q=20, a selected single burst with twice the force has peak energy .084487;
a half-selected single burst has .021122, but its train reaches .290712.
For assumed m=10 mg, f=1 kHz, s=.1 mm, the energy unit is 1.974 µJ.
An ideal trip barrier .05 therefore admits the selected command and the
unintended accumulated command. This is a **linear receiver plus ideal energy
trip counterexample**, not a nonlinear latch simulation or a claim that every
admissible row schedule has that phase. It exposes the same hidden accumulation
as E-080 by a different delivery mechanism. High Q improves spectral resolution
and worsens temporal isolation; arbitrary damping tuning is not a new selector.

An independent dissipative-deposition bound uses `E_next=rho E+e_off` for
80 half-select opportunities. With the same energy/gain uncertainty, allowable
off/target amplitude is `.66804/sqrt(sum(rho^k,k=0..79))`:

| Retained energy fraction rho | Maximum off/target amplitude |
|---|---:|
| 0 | .6680 |
| .5 | .4724 |
| .9 | .2113 |
| .99 | .08988 |
| 1 | .07469 |

This is an incoherent extracted-energy envelope, not predicted time-reversal
sidelobes; coherent addition can be worse. Additive crossed-wave ratio .5 fails
at rho=.5. Different frequencies alone supply no local mixing force; a
difference-frequency selector needs an actual nonlinear converter and filter. Simultaneous rows/columns {0,1} energize both off-diagonals when only
the diagonal is wanted (source checks this ghost). Row scanning or independently
coded fields remain necessary. P's blocked face avoids accumulation only if
striker energy is unloaded before opening the next address.

Unsigned intensity cannot reset by waveform-sign reversal. Opposed pickups or
a selectively gated reverse cam add real repeated parts, spectral space and
energy. Clear commands with cams parked, ground seats proved and pickups
withdrawn/de-energized; read the entire mask. Never clear unchanged supports.

## Full-display ledger and next discriminator

At 80×80 and 5.08-mm pitch, 406.4-mm span exceeds the 256-mm printer volume;
module joints change wave transmission. The literature focus is not proven
adjacent isolation or receiver packing. T requires a separate wave bus and
support frame plus a finite pickup. Directly vibrating the load plate excites
unchanged supports; mount/pickup leakage remains a gate even with separation.
No numeric disturbance limit is invented.

Repeat 6,400 receivers, extraction contacts and dogs (12,800 for opposed
receivers), plus persistent grip/pawl outputs and guides. Shared drive, readers,
control, attachments, joints, service and calibration remain inside the machine.
Assembly/print time, wear and fatigue are unknown. Microbubble process burdens
give no reason to change fabrication.

A single serial binary set-plus-clear pass already has 12,800 events. Grant
one cycle per command, passive ringdown to 1% amplitude
`t_decay=Q ln(100)/(pi f)`, 1 ms read per event, 1% retry-time reserve and 6 s
for map preparation, registration, lift, output/support proof and settling.
For equally visited 6,400 codes across 1–10 kHz, total is **61.02/172.13/764.75 s**
at Q=5/20/100. Granting row-parallel tones, E-083's adverse 21-height workload
has 3,440 complete transactions; allocating the 1-kHz slow tone each time gives
**38.41/114.81/522.25 s**. These are specified schedules/reserves, not optimal
lower bounds; 21 levels is a workload, not a product constraint. Faster bands,
active damping, pipelining or more banks need explicit mechanisms and may
change times. One cycle does not guarantee finite switching work. Reset decay
also does not prove a mechanical command cleared.

At T's source-demonstrated 2-ms focus duration, serial set+clear alone is 25.6 s;
adding even the assumed 6-s non-command reserve exceeds 30 s before reading or
retry. Multiple simultaneous foci can change this, but must bound side energy,
per-focus work and amplifier saturation under arbitrary masks. An amplitude
plot at focus time is insufficient; off-target peaks over the whole packet
and across repeated commands govern retained-state errors.

Costs are **allowances, not quotes/BOM passes**. With $150 elsewhere, each
of 6,400 bought receivers allows $0.0078125/$0.0390625/$0.0546875 at
$200/$400/$500 totals; two receivers halve these. Printed parts still require
manufacture/assembly. With $250 elsewhere, 32 complete emitter/amplifier
channels allow $4.6875 each at $400 or $7.8125 at $500; the $200 ideal is
already exceeded. Boundaries leave no contingency. P's E-083 16-bank comparator
needs 1,280 data + 80 row channels at <$0.184 each with $250 elsewhere.
No complete affordable implementation is established.

At assumed downward load F per column, a 40-mm full lift needs at least
`6400*.04*F=256F J`; command energy supplies neither lift nor service retention.
Read the entire command mask and prove support before each output event.
E-083's adverse workload has 275,200 flag and 12,800 support observations;
without per-opportunity unsafe-accept bounds, no union-bound reliability claim
is possible. Common read/bus drift defeats retries. Detected mismatch parks the
cam with support retained, permits one isolated retry, then requires repair.

**Decision:** close this bounded comparison. Do not optimize more frequency
thresholds or reopen A-016 on nominal resonance alone. Next, construct a finite
plate/receiver transfer model for T on a mechanically separate command bus;
compare time-reversed focusing against a localized direct-drive control.
Measure in simulation whole-packet off-target energy, transfer changes with
receiver load/state and coherent module bias, and attainable reset/schedule
margins. Stop T if those require per-site drives, disturbing the load frame,
or an assumed perfect decoder. A useful result can be a coupling/energy bound
that rejects it. No fabrication until a specific remaining calibration could
change the ranking. This is a new spatial-localization probe, not selection of T.

Self-review: tridiagonal response matches dense solve; uncoupled response
matches closed form; common frequency scaling is invariant. Exact transient
propagation passes zero-time, phase-continuous composition and unforced-energy
dissipation checks. Peak sampling 128→256 points/cycle leaves reported maxima
unchanged; propagation has no integration step. Frequency intervals,
geometric-series memory and crossed ghosts have separate algebraic checks.
No spatial mesh/contact convergence or hardware validation is claimed.
