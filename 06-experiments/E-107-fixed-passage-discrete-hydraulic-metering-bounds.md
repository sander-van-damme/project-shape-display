---
status: complete
builds-on: [E-106, E-105]
---

# Fixed passages exchange lift precision for flow uncertainty

**Stop tuning this single-bank fixed-passage controller; compare changed
system arrangements before further dry-head return/frame work.** Nominal
restrictions can meet a checkerboard timing example. None of the 80 generated
passages meets that example under the stated combined dimensional/fluid/loss
bounds at diagnostic .5-mm accuracy. Even ideal independently capped coarse
flow does not restore the tested window. This excludes these controller/grid/
uncertainty combinations, **not hydraulic addressing or a product accuracy
requirement**. The best tested 1-mm case nearly meets the two-workload gate;
small changes can reopen it. No hardware, seal or economic acceptance follows.

Input main `8c479c2`. Replay:
`python3 tools/curated-experiment-checks/E-107/fixed_passage.py`.
Use `--all` for individual primary population results/rejection reasons.
Evidence: deterministic reduced hydraulic/event simulation and self-review;
no CFD, generated valve solids, measurement, process priors or independent review.

## Mechanism, source and bounds

Proposed circuit: supply → [fixed restriction parallel to binary bypass] →
normally closed chamber isolation seat → piston. Closed shuts the chamber seat;
restricted opens that seat with bypass closed; full opens both. This permits
fully open seats instead of a precision analog seat gap **at circuit level**.
A separate bypass seat/control is real added hardware. A sequential common-stem
implementation would need two opening thresholds and positive return of both
seats; its finite geometry/force/stroke separation is not established. E-105's
one-poppet .35-mm mechanism does not implement these three states. Intermediate
fluid on reopening, stem-volume exchange and pressure transients remain gates.
The following screen generously gives the full path E-105's existing port law
and charges no extra full-path loss from the new bypass seat.

[Mortensen, Okkels and Bruus (2005)](https://arxiv.org/html/physics/0412015v3)
derive steady Newtonian no-slip flow in rigid straight channels. We use circular
Poiseuille resistance and the rectangular Fourier-series result, with 101 odd
terms. This supports the ideal resistance law, not printed-channel accuracy,
roughness, deformation or developing-flow performance. Source accessed 2026-10-10.

Source evaluates `Δp = R Q + K ρ(Q/Ac)²/2` plus E-105 full-open port losses
in series; `Q=A_piston v`. Circular `R=128 μL/(πd⁴)`; rectangular resistance
uses the exact series rather than a thin-slot approximation. Density 1000 kg/m³,
Cd=.6, entry K=0…2 are **assumed competing loss models**, not calibrated bounds
on all real losses. No-slip, incompressible, steady, Newtonian flow is assumed.
Reynolds/length ratios are reported to expose extrapolation. The nominal best
round passage has L/d=5: developing-flow discrepancy is unresolved. The tight
best has L/Dh≥62.72 and terminal-cap Re≤195.65. Broad-fluid cap Re can exceed
3272; its large predicted times are model diagnostics, not reliable fluid results.

Deterministic generator: round diameter or slot height .15/.2/.25/.3/.4/.5/.6/.8 mm,
length 2/5/10/20/40 mm; slot width .8 mm. Two cross sections of **one metering
topology**, not 80 architectures. Straight axial channels may extend below the
cell; full cartridge packing is absent. No random seed/distribution or yield.

Nominal: μ=.01 Pa·s, K=2 and exact geometry/pressure. Tight scenario:
finished cross-section dimensions ±.025 mm, length ±2%, μ=.008….012 Pa·s,
K=0…2, shared pressure error ±1 kPa. Wide dimensions use ±.05 mm; broad fluid
uses .001….1 Pa·s. These are labelled epistemic scenarios, **not X1C tolerances
or selected fluids**. Hole shrinkage, roughness and section distortion could
exceed them. Viscosity/model/pressure bias is common; dimension extremes can
be common to a batch or local to a cell. No independent-cell averaging is used.

## Executable control and outcomes

Retain E-106's eight known payload levels spanning .1 N, .3-N downward bias,
.05-N drag, 2-mm bore, 8 L/min both ways, 40-mm travel and full schedule/recovery.
Knowing load thresholds exactly is optimistic. Coarse binary pressure targets
400 mm/s at the hardest load/high viscosity, bounded by .01….5-MPa supply/return.
Easier loads can move faster. Pump saturation solves pressure, not a common
velocity scale. Reserve each coarse terminal band using its maximum possible
speed ×2 ms + .05-mm read error; conservatively traverse that entire band again
at fine speed. Stopped coarse/fine transition costs an additional 2 ms/direction;
initial direction overhead is 10 ms. Fine pressure is the highest shared setting
that bounds the **fastest** passage/load at `(e−.05)/.002` mm/s. Completion uses
the slowest passage corner. An empty forward/accuracy pressure interval rejects
that case. Fine flow fits the pump even at every tested cap and 80 open channels.
This is a robust fixed policy without batch retuning, not an optimal controller.

The slow completion corner is a coherent common small-section/high-viscosity/
high-loss batch. Fast-corner sizing protects against the opposite corner or
unidentified local geometry. These worst-case guarantees can be conservative;
calibration and changed scheduling require their own time/observability budget.
The ideal coarse comparator independently caps each channel at 400 mm/s and
still uses the fixed fine passage; it is an unimplemented regulator comparator,
not a universal lower bound on all policies.

Primary grid: 80 passages × five bounds × two coarse policies = 800 cases.
Each best value below selects **only by checkerboard**; candidate identities and
failure counts are emitted by the source. Times include one conservative
full-stroke recovery of all changed channels in one row, in both directions.

| Scenario, .5-mm diagnostic e | Binary coarse best / under-30 count | Ideal capped coarse best / under-30 count |
|---|---:|---:|
| Nominal | 29.371 s / 23 | 29.026 s / 27 |
| Tight | 31.183 s / 0 | 30.448 s / 0 |
| Wide dimensions | 32.313 s / 0 | 31.328 s / 0 |
| Broad fluid (model extrapolation) | 272.984 s / 0 | 209.721 s / 0 |
| Tight plus .22-N common drag | no completion | no completion |

Respectively 22/35/39/62 passages fail the fine-pressure window in each policy
for the first four scenarios. The remaining extra-drag cases fail unloaded
lowering: .03-N net bias is less than .031416-N return force even before losses.

Nominal binary best: round .4×2 mm; **30.113 s on 79-up/1-down**, despite its
29.371-s checkerboard. Tight binary best: round .6×40 mm; minimum fine speed
49.844 mm/s, coarse band up to 1.629 mm, **31.427 s on 79/1**. It takes 29.787 s
on the graded mixed map and 29.624 s on sparse mixed pairs across all rows.
Four 10×10 corner-patch/start-edge cases take 4.443…6.261 s, with recovery;
this is not an all-placement or arbitrary-map bound. Closed-neighbor command
isolation is assumed, not measured disturbance or sealing.

A further 480 candidate cases select against **both** checkerboard and 79/1:

| Change from tight binary scenario | Best maximum of both workloads |
|---|---:|
| Known μ=.01 (other errors retained) | 30.666 s |
| Known K=2 | 30.974 s |
| Zero pressure error | 31.214 s |
| e=.2 mm | 37.493 s |
| e=.3 mm | 33.776 s |
| e=1 mm | **30.036 s** (.6×.8×40-mm slot) |

Thus neither perfect pressure nor knowing viscosity alone restores this grid's
.5-mm window. The 1-mm near miss prevents a broad impossibility claim. Stage 02
sets no numerical height accuracy. Pressure-target optimization, shorter delays,
other passages or coarser terrain accuracy can change rankings; do not mistake
this grid minimum for a global optimum. Closure-volume and transient errors
would consume additional accuracy/time beyond this optimistic screen.

## Portfolio decision and reopening

This result does not justify printing small passages: no survivor yet earns
calibration ahead of the remaining selection/return/seal/economic problems.
Compare changed complete arrangements next, using these restrictions as bounds:

| Arrangement | Potential escape | Added burden / unresolved discriminator |
|---|---|---|
| Two independently supplied dry-head banks | Split rows and pressure schedules, increasing time margin | 160 complete heads; duplicated transport/control and possibly pump/reader. At $250 shared plus $.01/cell, head allowance drops from $2.325 to $1.1625; these are inverse budgets, not sourced prices |
| Moving wet docking bank with reused metering | Put restrictions/bypass control in 80 reusable heads instead of 6,400 cells | Repeated wet acquisition, seal wear, trapped docking volume, spills/air and chamber-check opening. Must isolate before undocking and control pressure-volume exchange |
| Direct rack heads, A-013 / ADR-017 | Positive support without fluid state or high-speed closure | Sourced servo route exceeds budget; complete cheap drives and support transfer remain unresolved |

No Pareto winner follows; missing components cannot receive zero cost. A second
bank or wet head must satisfy joint `Cshared+Nhead Chead+6400 Ccell ≤ $500`,
full/regional preparation, recovery and actual isolation. Cartridge fine/bypass
replication increases seat/passages/assembly count; moving those to reusable
heads changes acquisition physics. That is the next architecture discrimination,
not another seat-gap or channel-size sweep. Retain E-106's ideal independent
throttling and grouped-pressure cases as comparators. Stop this fixed-passage
embodiment pending a materially changed schedule, calibrated narrower bounds,
or justified accuracy/response allocation plus complete added hardware.

Self-review verifies SI pressure reconstruction, Poiseuille length/diameter
scaling, the square-duct resistance limit, rectangular-series convergence,
16 uncertainty corners, terminal speed bound, event volume conservation and
an independently inverted fixed-step holdout (100/50/25 μs; errors below one
step). This verifies the reduced model implementation only. Reproducible JSON
is omitted; retain source. Reader false acceptance, persistent faults, reverse
sealing, lifetime, affordability and manufacturing qualification remain open.
