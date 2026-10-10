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

Three independent source-domain searches were useful, rather than three synonyms:

- **Resonant tactile displays:** [Mohammadi et al., 2020](https://doi.org/10.1016/j.sna.2019.111818),
  [institutional abstract](https://researchportal.bath.ac.uk/en/publications/resonance-frequency-selective-electromagnetic-actuation-for-high-/),
  reports frequency-selective taxels sharing a coil, increasing 16 to 32 taxels
  on 25 cm². This is vibration selection, not bistable command storage or a
  6,400-channel demonstration. It confirms M-010, not a new principle.
- **Acoustofluidic microrobotics:** [Kaynak et al., 2023](https://doi.org/10.1089/soro.2021.0193)
  demonstrates tuned bubble capsules, streaming and inter-bubble radiation
  forces, including reversible bistable actuation at 85/170 kHz. Its final
  control-module example requires manual reset. Two-photon printed soft polymer
  and submerged micrometre capsules do not supply PLA/FDM properties or a dry
  display mechanism. Opposed force paths and neighbor interaction are real;
  frequency names alone do not provide reset or isolation.
- **Time-reversal haptics:** [Hudin et al., 2015, author manuscript](https://cim.mcgill.ca/~haptic/devices/pub/CH-JL-VH-TOH-15.pdf),
  [DOI](https://doi.org/10.1109/TOH.2015.2411267), uses recorded impulse responses
  and peripheral piezoelectric channels to focus bending waves. The reported
  148×210×0.5-mm glass plate uses 32 channels, 20–70 kHz and a 2-ms focusing
  time; measured focus amplitude/resolution are 7.68 µm/5.2 mm. Finger loading
  near 1 N reduces approximately 7 µm to 3 µm. This supplies a new spatial
  addressing analogy, not a switching-energy or off-target immunity result.

These are sourced facts; the combinations below are hypotheses. Nonlinear
metamaterial searches found transmission control, not a new local selector.
No saturation claim: time reversal supplied a useful new spatial axis.

| Command delivery | Selection and energy | Retention, output and recovery | Disposition |
|---|---|---|---|
| F: coded resonators | Common oscillatory bus; a tuned receiver drives an opposed set/reset pickup | Retained routing dog; powered shared collet/cam; ground pawl carries service load; read dog and height before releasing grip | M-010 recombination; frequency/energy bounds fail robust uncalibrated scale |
| X: crossed guided waves | Row and column packets add at intersection; rectifier trips a dog | Same powered output and support; separate reverse pickup or selective mechanical reset required | Without a physical gate or actual nonlinear mixing/filtering package, equivalent to A-001/A-016 threshold logic |
| T: time-reversed wave bus | Peripheral emitters replay reversed transfer responses to concentrate a packet at an identical local receiver | Opposed pickups command a retained dog, with shared cam/collet and independent ground support; recalibration/isolated repair on mismatch | Spatial phase localization is different from frequency labels; receiver loading and complete set/reset remain unbuilt |
| P: positive coincidence | Two frame-backed apertures admit a row-local powered striker only at an addressed intersection | Withdraw below both shutters before address changes; retained dog routes powered cam; selective reverse path still needed | E-076 control, with E-082/083 reset and cost limitations; not a new candidate |

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

Score `S_i=|X_i|max(1,omega/w_i)` is the square root of peak local oscillator
energy divided by `.5 w_i² s²`, with reference excursion s=1. Coupling-spring
energy is not credited as useful isolation. An **ideal energy-trip surrogate**
with barrier ±20% and forcing gain ±10% needs selected/off-target S ratio
`>sqrt(1.2/.8)*1.1/.9 = 1.49691`. This deliberately grants lossless delivery to
a command barrier. It does not implement a latch, rectifier or contact; local
energy can fail to transfer to an actual dog. A window is necessary only within
this defined surrogate, never switching acceptance.

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
Track `x²+v²`, energy in units `.5 m w²`, including off-time motion:

| Q | Single burst peak energy | 80-burst peak | Ratio |
|---|---:|---:|---:|
| 5 | .216592 | .424405 | 1.9595 |
| 20 | .021122 | .290712 | 13.7636 |
| 100 | .0009565 | .2545415 | 266.1184 |

At Q=20, a selected single burst with twice the force has peak energy .084487;
a half-selected single burst has .021122, but its train reaches .290712.
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

This model applies to incoherent extracted-energy storage; coherent amplitude
addition can be worse, as the oscillator history demonstrates. It is a useful
necessary envelope for a future measured transfer response, **not a prediction
of time-reversal sidelobes**. An additive crossed-wave half-select ratio .5
fails already at rho=.5 under these bounds. Different frequencies eliminate
the coherent factor-of-two peak advantage in a linear receiver; a difference-
frequency mixer/filter could restore localized conversion but is an additional
nonlinear device and reset path, not a free multiplication operation.

Simultaneously enabling rows {0,1} and columns {0,1} to write only the diagonal
also energizes both off-diagonal intersections; source checks this ghost. Scan
rows or supply independently coded spatial fields. P avoids wave accumulation
only while a rigid closed face and positive withdrawal remain valid. Stored
striker energy must be unloaded before opening the next address.

Unsigned vibration intensity/radiation force cannot reset by changing waveform
sign. F/X/T need opposed pickups/frequency paths, or a selectively gated reverse
cam; two independent receivers can double repeated parts and consume more
spectral space. No global command clear may disturb unchanged supports. Clear
retained commands only with output cams parked, ground seats proved, and all
pickup energy decayed or positively disconnected; then read the entire mask.

## Full-display ledger and next discriminator

At 80×80, p=5.08 mm gives 406.4-mm span, beyond the 256-mm printer volume.
Module joints affect the wave transfer matrix and shared-frame vibration.
Receivers live below the tops; a 5.2-mm literature focus is not a proven 5.08-mm
receiver-packing or adjacent isolation result. T must use a separate wave bus
and grounded support frame, with a finite command pickup between them. Vibrating
the support plate itself deliberately excites unchanged supports. A wave bus
may also leak through its mounts/pickups: separation is a design requirement,
not proof of zero terrain motion. No numeric disturbance tolerance is invented.

Repeat 6,400 receivers, extraction contacts and dogs (12,800 receivers for
two opposed paths), plus persistent grip/pawl outputs and guides. Shared
cam/lift, readers, control, piezo attachments, joints, service and calibration
remain inside the machine. Assembly/print time, wear and fatigue are unknown.
Microbubble containment/process burdens give no reason to change fabrication.

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

Costs are **allowances, not catalog quotes or BOM passes**. Reserving $150
elsewhere leaves each of 6,400 bought receiver assemblies only
$0.0078125/$0.0390625/$0.0546875 at $200/$400/$500 totals. Printed receivers
avoid that purchase line but not repeated manufacture/assembly. With $250
elsewhere, 32 complete emitter/amplifier channels allow $4.6875 each for $400
or $7.8125 at the $500 boundary; the $200 ideal is already exceeded. Equality
at a boundary leaves no contingency. Two receiver paths halve their allowance.
P's E-083 representative 16 banks instead need 1,280 data drives plus 80 row
channels and <$0.184/channel with $250 elsewhere. None has an affordable
complete implementation here.

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

Self-review: tridiagonal response agrees with independent dense solve; uncoupled
response agrees with closed form; common frequency scaling has the correct
invariance. Exact transient propagation passes zero-time and phase-continuous
composition checks and unforced energy dissipation. Doubling peak sampling
128→256 points/cycle leaves reported pulse maxima unchanged; propagation itself
has no integration step. Disjoint frequency intervals, geometric-series energy
memory and crossed-address ghosts have separate algebraic checks. These verify
the reduced model only. No spatial mesh or contact convergence claim is made.
