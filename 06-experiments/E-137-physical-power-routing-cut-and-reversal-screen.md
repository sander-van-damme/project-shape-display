---
status: complete
builds-on: [E-136, E-076, E-082, E-083, E-108, E-128]
---

# Physical power routing: boundary control is not an internal cut

**No new complete-machine survivor is selected.** Four varied routing searches
recover useful physical isolators, but no demonstrated reduction of both repeated
interfaces and full-map work. A new executable counterexample rejects a reciprocal
row/column network with boundary selection alone: every unselected site carries
flow in its nominal steady state. One-way checks remove alternate paths only in
one direction; opposite parallel checks restore them. This is a scoped circuit
failure, not rejection of all hydraulic, directed or nonlinear routing.

Input main `74dec07`; LAB-237. Reproduce with Python 3 + NumPy:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-137/routing_cut.py`.
Retain source; JSON is disposable. Evidence: graph enumeration, linear-network
calculation, analytical bounds and self-review. No CAD, dynamic contact/CFD,
calibrated fabrication prior, price quote, hardware measurement or yield claim.
E-136 remains unchanged: focal amplitude is not whole-history command isolation.

## Independent search axes and causal combinations

Sources accessed 2026-10-10. Patents are mechanism references, not performance
evidence. These functional proposals expose missing implementations; none earns
a free lock or release.

| Search axis / proposed combination | Selection, finite work and isolation | Retention, grounded load path and recovery | Comparison / disposition |
|---|---|---|---|
| Binary routing, by analogy with microfluidic multiplexers | Paired control rails close branches; pump routes reversible flow to one piston or rotary output. Break source flow, hold output, change branch state, condition destination pressure, then deliver work. Closed branch seats isolate unused paths only if they seal. | Guided column → resident rack pawl → frame. Selected output first takes load; a routed pilot piston retracts the pawl, output moves 40 mm, pawl returns, unloading proves its seat before venting. Pilot, return and sequencing repeat per site; partial transfer requires captured pressure plus mechanical arrest. | M-002/007/011 and A-014 relatives. Binary address bits reduce drivers, not branching seats. No new cheap output or retention mechanism; stop before seal CAD. |
| Rotary fluid commutator, injector-distributor analogy | One reusable face/rotor connects pump to one outlet, with positive dead sector and dump to return between outlets. Reversible flow requires source/return switching and a selected return path. Stationary outlets fan out to pistons. | Same rack/pawl support and explicit release as above; traps at outputs need containment or checks. Close/prove pawl, isolate pump, depressurize transfer cavity, index, condition next cavity. Stuck valve holds connection and stops bank. | M-007 plus E-108 wet routing: replaces actuated branch gates with a swept sealing surface and 6,400 outlet passages. Fewer moving valve bodies, but repeated port lands and serial work remain. No admitted machine. |
| Movable gear bridge, indexed transmission analogy | Withdraw an idler axially; index among stationary output pinions; phase/engage; shared shaft powers selected rack up/down. Independent index drive allows reverse; direction-selected index/drive alone does not. | Column rack → resident ground pawl → frame. Captured idler and shaft arrest take load before a co-located release finger opens pawl. Seat/proof precede withdrawal. Jam or power loss requires keeper and arrest throughout handover. | M-001/008/009, E-127/128. Moving coupling is real isolation, but 6,400 rack/pinion/bearing/dock and seat interfaces remain. Phase capture and arrest failures are not cured by rearranging the bus. |
| Boundary pressure steering, nonlinear-network analogy and reversal test | Connect pressure to row r and return to column c; seal other boundary ports. Put a reversible two-terminal fluid converter at each crossing. Proposed signed pressure operates the converter and a pilot release; no internal selection valve. | Converter drives column rack; spring pawl grounds it at rest. Pilot release, return, support takeover and readback would still repeat at every output. Adding an addressed pilot valve would replace the tested gate-free premise. | Reciprocal version rejected below before pilot/geometry optimization. Nonlinear flow reversal alone supplies neither zero off-path work nor a grounded hold. One-way check and antiparallel variants fail the requested reversible topology. |

[Thorsen, Maerkl & Quake, *Microfluidic Large-Scale Integration* (2002)](https://web.mit.edu/Thorsen/www/580.pdf)
uses combinatorial valve patterns with `2 log2(n)` control channels in multilayer
soft lithography. That is control-line scaling, not a claim of logarithmically
many physical valve sites or PLA compatibility. Our actual branching-tree bound
below is a separate calculation, not a count of that paper's chip.

[US20140352493A1, multiple-output transmission](https://patents.google.com/patent/US20140352493A1/en)
describes indexed idlers and a one-motor variant whose reversal changes between
indexing and output drive. It motivates the movable bridge; its selected output
cannot simply inherit independently commanded reverse motion from that variant.
A second selector/retained mode or a unidirectional crank changes that limitation,
but the latter needs a full lower/raise trajectory and selective stopping.

[EP0743447A2, fuel pumping apparatus](https://patents.google.com/patent/EP0743447A2/en)
explicitly routes its delivery passage to drain when cutting off the accumulator.
This motivates isolation plus dumping.
[Case et al., *Nature* (2019)](https://doi.org/10.1038/s41586-019-1701-6)
reports pressure-controlled internal flow reversal in nonlinear microfluidic
networks. Reversal motivates the boundary-control test; the linear counterexample
does **not** model or disprove their nonlinear device.

These four strategies change source domain or physical routing representation,
without a new complete architecture. This is bounded saturation of these attempts,
not landscape exhaustion. No new M/A object or renamed threshold is warranted.

## Executable discriminator: reciprocal crossbar and reversal

Represent an n×n crossbar by row pressures R and column pressures C. Selected
R0=1, C0=0; all other boundary ports are sealed, but internal crossings remain
connected. Each crossing has conductance g and `q_rc=g_rc(Rr−Cc)`. This is a
reciprocal dissipative two-terminal converter/load approximation, not a sealed
single-chamber piston model. Pressure and conductance are normalized. There is
no inertial/compliance,
static-friction or threshold isolation credit. Trapped-volume actuators instead
require pressure-history analysis such as E-108, not these steady numbers.

For identical g, conservation gives unselected `R=(n−1)/(2n−1)`,
`C=n/(2n−1)`. At n=80:

- 158 crossings on the selected row/column see **79/159=.496855** of target ΔP.
- 6,241 other crossings see **−1/159**: small reverse flow, not disconnection.
- Worst off-site power is **.246865** of target power; total off-site power is
  **6,241/159=39.251572** times target power. All 6,399 off sites carry flow.

A three-edge alternate path `R0→Cj→Ri→C0` remains after removing the target
edge. Even arbitrarily clamping all unselected boundaries cannot make every off
pressure difference zero: the three signed drops sum to 1, so one has magnitude
≥**1/3**. Setting all unselected R=1/3 and C=2/3 attains that minimax bound,
but drives every off site at magnitude 1/3 (equal-g aggregate off power 711).
This pressure-difference bound is independent of positive conductances. It is
not a universal power bound for unequal or nonlinear converters. A hard seat can
block motion, but selectively releasing only one then needs a real added gate.
We reject *physical isolation*, not assert that these numbers exceed every
possible nonlinear threshold; threshold history would return to E-135/136.

Nine deterministic conductance scenarios use uniform .8/1/1.2, coherent half-row,
half-column and quadrant bias, alternating sites, or target-only .8/1.2.
These ±20% bounds are epistemic perturbations, **not X1C process priors**.
Worst off ΔP ranges .496855–.553073; total off/target power 32.613–49.209.
Every scenario retains 6,399 flowing off paths. Common scaling leaves normalized
ratios unchanged. Shared row/column bias changes the worst exposure; independent
cell averaging would conceal it. Unknown roughness, passage shrinkage, wall
compliance, air and temperature preclude calibrated flow/yield estimates.
The algebraic cut failure already exists at zero manufacturing error.

An ideal one-way check on every edge, R→C, removes the three-edge bypass.
Enumerating all simple source/sink paths on 3×3 gives **1 forward / 0 reverse**.
Reverse source and return cannot lower through that same circuit. Add an opposite
parallel check at every crossing and the graph becomes reciprocal again:
**9 forward / 9 reverse** paths. Separate switched return manifolds, piloted
checks or a mechanical return are changed circuits, not rejected by this result;
they must count their extra gates, reset work and isolation histories. This
check counts topology only: even the forward-only graph can charge dead-end
compliance, so it does not establish transient motion isolation.

Verification: direct nodal solves agree with an independent symmetry solution
at n=1/2/3/8/80; every scenario checks mass conservation and source power equal
to summed dissipation. A boundary-clamp grid includes the analytically optimal
1/3,2/3 point. Discrete path enumeration reconstructs the one-check and reciprocal
circuits. No timestep exists; these checks validate equations only.

## Physical cuts, timing and full-display accounting

For a local-junction routing tree with N leaves, `sum(d_i−1)=N−1`.
Consequently N=6,400 requires at least 6,399 binary, 2,133 four-way, 915 eight-way
or 81 eighty-way branch junctions. This is **not** an actuator-count bound:
common address rods can gang junctions, and an integrated rotary plate can form
many cuts with one moving part. Larger fanout exchanges junctions for terminal
port lands/teeth and swept sealing/registration. The tree bound does not apply
to free-space beams, arbitrary networks or a traversing head.

One isolated path performing every 40-mm stroke at speed v has work time
≥`6400*.04/v`. At .4 m/s that alone is **640 s**. For balanced K-path zoning,
calculate the explicitly assumed controller
`T=6 + ceil(6400/K)*(.04/v+t)` seconds. The six seconds reserve preparation,
shared indexing, a detected supported retry, final proof and settling; t includes
local selection, takeover, release, reseating/readback, dump and withdrawal.
Neither allocation is demonstrated, and moving-head transit may exceed it.

| Assumed output speed | t=5 ms: minimum K / T | t=20 ms: minimum K / T |
|---|---:|---:|
| .1 m/s | 109 / 29.895 s | 113 / 29.940 s |
| .4 m/s | 29 / 29.205 s | 33 / 29.280 s |
| 1 m/s | 13 / 28.185 s | 17 / 28.620 s |

These are conditional concurrency requirements, not architecture passes or
necessarily K motors. Shared drives still need K simultaneous physical paths
and independently valid stop/retention sequences for arbitrary heights. Command-
only routing could be faster but transfers work to another machine and repeats
mask phases; E-083's 3,440-row adverse schedule remains a control. Preloading
cannot remove sustained arbitrary-map preparation. Local routing can retain
unchanged ground seats; frame vibration and actual displacement remain untested.

At 5.08-mm tops the board is 406.4 mm square; X1C construction needs modules.
No assembled routing geometry is claimed; internal machinery may exceed top
pitch. With hypothetical $250 shared purchases reserved, every
bought site item together must cost <**$.0390625** at the strict $500 ceiling
(<$.0234375 at $400). Binary junctions alone allow <$.039069 each if the entire
remaining $250 goes to them, leaving nothing for output seals/bearings/pilots.
For K=33, 33 complete reusable paths allow <$7.576 each **only if** no other
purchases consume that $250. These are alternative allowances, not additive
budgets or prices. None establishes <$500; <$200 is still farther away.

All proposals retain 6,400 column guides and grounded seats with finite release
and return. Fluid proposals add 6,400 piston seals or rotary converters and
pilot interfaces; the commutator adds 6,400 terminal passages and port lands.
Gear routing adds 6,400 racks/pinions and at least 12,800 bearing interfaces.
Trees add branch seats; moving couplers reuse the moving half but retain every
stationary mating interface. Printed integration need not remove precision,
wear or repairs. Print time and
material remain unknown before geometry, not zero.
Full upward travel against F newtons/site needs ≥256F joules, independent of
address bits; dump, drag and pump/gear loss add to this.

Source interruption does not dissipate distal pressure, torsional windup or
moving inertia. Before release a selected column must be carried by a captured
actuator path with real arrest; during motion, a disconnected input does not
restore a ground seat instantly (E-128). Common registration, stuck-open branch,
face debris or failed drive arrest can affect many cells. Read actual heights
and ground-seat support independently of commanded drive position; on detected
error retain capture, inhibit indexing, retry once only after restoring support,
then isolate/repair the bank. An established per-event false-accept bound p
gives at best `min(1,m*p)` for m unsafe opportunities without independence;
common reader faults prevent an invented board-yield claim.

## Decision and next discriminating action

Stop boundary-only reciprocal routing and its antiparallel-check repair. Reopen
with a changed circuit that actually cuts every unused work path, provides
controlled reverse/reset, bounds stored energy and counts repeated interfaces.
Keep positive shutters, banked clutches and moving heads as controls with their
existing failures; no further aperture, tree-ratio or commutator sweep is earned.
No fabrication, purchases, staffing or approval wait is justified.

The next useful search axis is **spatial contactless coupling at a reusable
head**, asking whether finite magnetic pole/armature geometry can avoid dock
phase and contact wear without adding local powered decoders. First cross-check
M-010, A-016 and E-063/065/074/080; a travelling head is spatial selection, not a
new magnetic threshold. Compare attraction with a steel armature, magnetic
gear/torque coupling and a direct mechanical head. Count the local material,
load-retention release and all 40-mm work before promoting any candidate. Stop
if the only isolation is an unsourced threshold or if support handover merely
repeats E-128/129. This is an exploratory next question, not a magnetic winner.
