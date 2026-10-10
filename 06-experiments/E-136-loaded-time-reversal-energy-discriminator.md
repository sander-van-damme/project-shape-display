---
status: complete
builds-on: [E-135]
---

# Loaded time-reversal bus: whole-packet extraction discriminator

**Stop the tested passive, identical-receiver time-reversal command bus.** Its
baseline unselected receivers absorb more work than its target even with fresh
loaded calibration. The most favorable guarded dispersion holdout gives .628
off/target work, still above the E-135 uncertainty limit .446. Increasing
amplitude cannot open a switching-energy window under these bounds.
This rejects the tested delivery/pickup combination, not time reversal as a
physical principle, haptic focusing, or every possible inverse-filtered bus.
No architecture, print, purchase or latch/CAD development is selected.

Input main `50220e2`. Reproduce with Python 3 + NumPy:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-136/loaded_bus.py`.
JSON is reproducible output, not retained. Evidence: deterministic finite linear
network, frequency-domain packet propagation, energy accounting, bounded
parameter scenarios and self-review. No physical measurements, calibrated PLA
priors, nonlinear switching geometry, stochastic yield or independent review.

## Model and its limits

One bus module has 40×40 receiver sites at 5.08-mm pitch, separate from the
column support frame. Its 203.2-mm top footprint has a mathematical simply
supported boundary one grid spacing beyond the outer node: 208.28-mm support
span. Four ideally independent buses address 6,400 tops over 406.4 mm. Boundary
packaging, overlapping margins/mounts and inter-module coupling are unresolved;
perfect module isolation is a favorable assumption, not an assembled design.
The baseline finite network has 1,600 bus + 1,600 receiver coordinates.
A guard variant extends to 48×48 sites: the inner 40×40 command receivers
are surrounded by four rows of identical dummy dissipative loads with no
command latch. Its bus support span is 248.92 mm, below the nominal printer
build width but needing additional packaging depth/overlap to tile the tops.
Dummy losses remain in the work balance; they are excluded only from the
false-command test. Emitters are now outside the active array.

Let `x` be bus displacement, `y` receiver displacement, `S` the orthonormal
2-D discrete sine basis and `q=Sᵀx`. Grid pitch p, plate mass/node
`mp=rho h p²`; flexural rigidity `D=E h³/[12(1−nu²)]`. Network modal frequencies:

`w_ab = sqrt(D/(rho h)) (lambda_a+lambda_b)`,
`lambda_a=4 sin²(pi a/[2(n+1)])/p²`.

Bus stiffness is `S diag(mp w_ab²) Sᵀ`; modal damping is `2 zp mp w_ab`.
Each absolute receiver mass m connects to its bus site through k and parallel
viscous terms `ci+ce`. Extraction ce changes propagation, not just readout.

With `s=k+i w(ci+ce)`, elimination gives `H=y/x=s/(s−m w²)` and bus loading
`Zload=−m w² H`. Solve each mode with
`Zq=mp(w_ab²−w²+2i zp w_ab w)+Zload`. A changed receiver is an exact rank-one
impedance update. Relative velocity is `i w(y−x)`; extracted energy is
`Ei=integral ce_i |y'_i−x'_i|² dt`. Input work uses actual velocity at force
ports, not force-squared as an energy surrogate. Parseval integration includes
the complete packet and ringdown. All credited extraction is optimistically
available for useful work: no actual rectifier, storage, latch or reset exists.

Sixteen peripheral force ports/module, four per edge, lie on the second grid
row. Loaded target **relative-velocity** impulse responses to a 0.1-ms sine²
force pulse are recorded for 2 ms, reversed and applied at those same ports.
Calibration at every receiver is granted; its physical access/readout is not.
A 10-µs sample interval and 81.92-ms FFT period approximate isolated causal
packets. Normalize total `sum integral F_j² dt=1 N² s`; linear scaling makes
energy ratios independent of amplitude. This normalization is not amplifier
power, a feasible force rating or a physical operating amplitude.

The control directly forces the target mass: 2-ms, 5-kHz sine burst with a
sine² envelope and equal force-squared normalization. Reaction still loads the
bus; each site needs a local drive/address. This is not a cheap architecture.

All numerical inputs below are **illustrative bounds**, not sourced process
priors: E=2 GPa, rho=1,240 kg/m³, nu=.35, h=1 mm; receiver m=10 mg,
f=5 kHz, `k=m(2 pi f)²=9,869.6 N/m`; zp=.03 and receiver damping ratio .05,
half of receiver damping assigned to ce. There is no validated printable
5-kHz pickup. E±20%, h+5%, zp=.01–.10, receiver damping=.02–.15, whole-module
receiver mass×2 at fixed k/damping ratio (c increases by sqrt(2)),
target mass×2 at fixed k/c, target k+20%, and a neighbor's
ce×4 are competing deterministic scenarios. Coherent E/thickness/loading
changes model module/batch and state correlations, not 1,600 independent draws.
A target/neighbor change tests local state and extraction drift. They do not
exhaust arbitrary load masks, geometry variability or switching during a packet.

Layer/wall bias and orientation change `Eh³`, mass and tuning; joints/warp
change modes; friction, creep and wear change pickup impedance. First-layer,
hole, alignment, fatigue and support-leakage effects need actual geometry.
These remain unknown; scenario counts imply no manufacturing yield.

## Discriminator and results

Use E-135's energy/gain uncertainty unchanged: barrier ±20%, forcing gain ±10%.
For an identical unsigned work trip, even with perfect clearing between
packets, `max(Eoff)/Etarget < (.8/1.2)(.9/1.1)² = .44628` is necessary.
With 80 exposure opportunities and energy retention r, divide .44628 by
`sum(r^j,j=0..79)`: limits are .22314/.04464/.00808/.00558 at
r=.5/.9/.99/1. The geometric envelope describes dissipatively deposited energy;
it does not promise favorable phases for coherent mechanical storage.

| Case (nominal codebook unless noted) | Worst off/target energy |
|---|---:|
| Nominal loaded 40×40 | 14.403 |
| Coherent E−20% / E+20% | 31.034 / 12.780 |
| Coherent h+5% | 12.154 |
| Low / high damping bounds | 2.036 / 160.175 |
| All receiver masses×2 / target mass×2 | 12.384 / 2.596 |
| Target k+20% / neighbor extraction×4 | 15.052 / 14.471 |
| Recalibrated at E+20% | 8.225 |
| 48×48 bus, guarded inner 40×40 active receivers | 4.268 |
| Same guard, recalibrated continuum dispersion | .62779 |
| Off-center target (9,13), zero-based grid | 12.459 |
| Direct local receiver force, control | .09698 |

All listed wave cases fail even the perfect-clear .44628 limit. Direct force
passes that necessary single-packet condition and r=.5, but fails r=.9 and
higher retention; it is not a qualified reset or decoder. Guarding does not
remove active-array leakage: the worst active site is its corner. Merely
excluding four border rows from the original baseline leaves an off/target
ratio 3.228, so this is not solely a co-located emitter/receiver error.
The .628 holdout could have a window with exact gains/barriers and perfect
clearing; it is not an impossibility proof for that topology. It fails the
existing uncertainty envelope and retained histories. Lowering assumed
uncertainty to declare success would need evidence and an explicit reset path.

The nominal worst off-target site is a corner near peripheral forcing. The
failure is energy deposited during travel and ringdown, not just imperfect
resolution at the focal instant. A decoder that ignored this energy until a
chosen instant would add the very local gate/clock being assumed away.
Waveform sign reversal leaves extracted energy unchanged and supplies no reset.

For unknown finite set/reset work W, nominal input work is `W/eta`, where eta
is the reported target-extraction/input-work fraction. Normalizing to 1 µJ
is an illustration only, not a latch requirement. Nominal eta=.000184876
requires 5.409 mJ input per 1 µJ credited at the target; the worst off-target
then receives 14.403 µJ. No amplitude can both deliver
W to the target and keep the worst identical receiver below its barrier here.
A different nonlinear pickup could change this inference only through an
explicit safe state history, finite reset and loaded transfer model.

## Verification and scope of rejection

The off/target ratio changes 14.403119→14.403936 when sampling changes
10→5 µs (0.0057%), and to 14.403137 when the FFT period doubles
81.92→163.84 ms (0.00013%). Target energy changes by 0.0032% and
0.000003%, respectively. Sampled peak velocity changes 2.2%; no precise focal
peak claim is used. Nominal target relative-velocity energy in the final quarter
of the original record is <4e−10 of its total; even the low-damping case is
<3e−7. Period doubling, rather than that target-only tail, checks packet work.

Truncation to 20²/32²/40² bus modes gives off/target ratios
3.226/12.950/14.403. Coarse truncation substantially understates leakage;
retain the full network. All reject, but these numbers do not establish a
converged continuum. The recalibrated continuum-dispersion holdout gives 1.707,
still above .44628; combining that holdout with the larger guard gives .62779.
These large model discrepancies are retained, not averaged away.

Conservation is checked as positive input work = bus viscous loss + intrinsic
receiver loss + credited extraction for every case. A separate dense
physical-coordinate 4×4 bus/receiver solve, including a doubled-mass,
0.7-stiffness defect, agrees with modal elimination to 2.3e−15 relative norm.
Zero-frequency receiver dynamic load vanishes. These independent algebraic
checks validate implementation, not material choice or hardware.

The dispersion holdout substitutes `lambda=(pi a/[(n+1)p])²`, then
recalibrates on the same receiver grid. Unresolved sub-pitch modes, contacts,
anisotropy, boundary compliance and module transmission prevent transferring
these finite-network numbers to an arbitrary manufactured plate.

## Full-machine accounting and next decision

Four simultaneous isolated modules consume **64 emitter/amplifier channels**;
serial reuse saves channels while losing concurrency and adding switching.
A fresh one-direction calibration already needs at least 6,400×2 ms=12.8 s
of site recordings serially, or 3.2 s with four concurrent probes/modules,
**granting all 16 transfer channels acquired together** by a valid reciprocal
relative-force probe or coded experiment. One-emitter-at-a-time calibration
multiplies these to 204.8/51.2 s, before probe movement, ringdown or fitting.
Loaded receiver access is granted. Peripheral-only local-state readback is
unproven. Stable power-on calibration may be excluded from map time;
load/state-dependent recalibration may not.

A single set+clear event per column means 12,800 packets: 25.6 s serially at
2 ms, or 6.4 s with four independent modules, before ringdown, reading,
retries and powered motion. Opposed pickups may double repeated receivers to
12,800. This is a favorable one-event workload, not arbitrary height scheduling.
The E-083/E-135 multi-height workload can require repeated masks/support
transfers. The long numerical integration window is not an established safe
command separation; overlapping packets would need their own accumulated-energy
and load-transition calculation. Thus module parallelism removes the simple
25.6-s serial bottleneck but does not demonstrate a <30-s map.

Four simultaneous targets on one module use the same 16 force channels and
same summed force-squared budget. The weakest target gets only 41.04% of the
single central target's energy, while worst off/weakest target rises to 64.30.
Delivering the central-command reference work to every focus needs 1.56× drive
amplitude and 2.63× the central single-command input energy in the same 2 ms.
That is a real power/amplifier demand, not four free commands; it is not a
comparison against an optimized sequence of those four different targets.
Arbitrary multifocus masks, saturation and concurrent load changes are untested.
This example supplies no command margin and cannot earn a map-time pass.

Repeat 6,400 pickup interfaces/retainers (12,800 if opposed), plus guides,
powered captures and ground seats. With $250 reserved elsewhere, 64 complete
channels allow $2.34375/$3.90625 each at $400/$500, leaving no receiver budget.
With $150 elsewhere, receiver allowance at $400 is $0.0390625 each before extra
channels. These are alternative budget slices, not additive allocations or
quotes. Printed assembly, wear, fatigue, repair and lifetime remain unknown.

Service load must run column → positive seat → frame. Powered capture takes
the load before unlocking, positions ≥40 mm, re-engages the seat and proves
support before release. Full 40-mm lift needs ≥256F J at F/column. The bus
provides neither this lift nor retention. Separate mounts/pickups still need
leakage qualification; vibrating the support plate fails regional isolation.
Read the entire command mask and prove changed supports. Detected mismatch
parks supported motion, allows one isolated retry, then repair. Common drift
can repeat errors; no false-accept or hardware-reliability claim is available.

**Decision:** retire this ungated identical-receiver embodiment from active
optimization. Keep direct local force routing and E-076 positive coincidence
as controls with their known channel/contact costs. Reopen only for a materially
changed bus/pickup with whole-packet and repeated-history energy margin under
loaded drift, explicit set/reset, and no free per-site decoder. Better focal
resolution, amplitude or a fresh nominal calibration alone are insufficient.
No print is decision-relevant while the tested isolation mechanism fails.

Next, return to architectural discovery of **positive energy-path isolation**:
compare physically broken/connected paths or shared movable addressing against
field focusing, with real enable/withdrawal and grounded-support transfer.
Screen existing M-002/007/008/009/011 and E-076 relatives before calling any
combination new. Stop renamed threshold schemes and mechanisms that simply
move 6,400 precision decoders into another layer. Do not automatically optimize
inverse filters or full latch CAD after this negative discriminator.

Source context: [Hudin et al., 2015](https://doi.org/10.1109/TOH.2015.2411267)
is the time-reversal haptic starting point from E-135, not a source for this
network's material parameters. A fresh primary-source search found
[Reardon et al., 2026, preprint](https://arxiv.org/html/2606.05572v1): resonator
loading engineers a slow-wave branch; an acrylic/brass implementation uses eight
actuators and inverse filtering for tactile patches around 2 cm². This supports
treating loading as part of propagation and leaves dispersion engineering open.
It does not establish 5.08-mm command-energy isolation, passive work retention,
set/reset or a grounded column machine. No parameters are transferred to PLA.
